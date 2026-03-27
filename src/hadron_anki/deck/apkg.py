import hashlib
import os
import tempfile
from typing import Any, Optional
import zipfile

import genanki

from hadron_anki.cards.styles import CARD_CSS
from hadron_anki.cards.mapping import generate_cards
from hadron_anki.deck.ids import stable_note_guid
from hadron_anki.domain.composer import normalize_quark_token, validate_quark_count
from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.render.svg import render_svg
from hadron_anki.cards.tags import build_tags


_DETERMINISTIC_ZIP_DT = (1980, 1, 1, 0, 0, 0)


def _rewrite_apkg_deterministic(in_path: str, out_path: str) -> None:
    def _writestr(z: zipfile.ZipFile, name: str, data: bytes) -> None:
        info = zipfile.ZipInfo(filename=name, date_time=_DETERMINISTIC_ZIP_DT)
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, data)

    with zipfile.ZipFile(in_path, "r") as zin:
        with zipfile.ZipFile(out_path, "w") as zout:
            _writestr(zout, "collection.anki2", zin.read("collection.anki2"))
            _writestr(zout, "media", zin.read("media"))

            numeric_names = [n for n in zin.namelist() if n.isdigit()]
            for name in sorted(numeric_names, key=lambda s: int(s)):
                _writestr(zout, name, zin.read(name))


def _particle_spec_from_mapping(p: dict[str, Any]) -> ParticleSpec:
    particle_id = p.get("id")
    name = p.get("name")
    typ = p.get("type")
    quarks = p.get("quarks")

    if not isinstance(particle_id, str) or not particle_id:
        raise ValueError("particle.id must be a non-empty string")
    if not isinstance(name, str) or not name:
        raise ValueError(f"particle {particle_id}: name must be a non-empty string")
    if typ not in {"baryon", "meson"}:
        raise ValueError(f"particle {particle_id}: type must be 'baryon' or 'meson'")
    if not isinstance(quarks, list) or not all(isinstance(q, str) for q in quarks):
        raise ValueError(f"particle {particle_id}: quarks must be list[str]")

    spec = ParticleSpec(
        id=particle_id,
        name=name,
        type=typ,
        quarks=[normalize_quark_token(q) for q in quarks],
        symbol=p.get("symbol"),
        symbol_tex=p.get("symbol_tex"),
        pdg_id=p.get("pdg_id"),
        aliases=p.get("aliases"),
        mass=p.get("mass"),
    )
    validate_quark_count(spec)
    return spec


def build_apkg(
    catalog: dict[str, Any], 
    out_path: str, 
    template_version: str, 
    model_version: str,
    card_types: Optional[list[str]] = None
) -> None:
    """
    Build an Anki .apkg file from a particle catalog.
    
    Args:
        catalog: Dictionary containing particle data.
        out_path: Destination path for the .apkg file.
        template_version: Version of the card template.
        model_version: Version of the Anki note model.
        card_types: List of card types to include. If None, all are generated.
    """
    particles_any = catalog.get("particles")
    if not isinstance(particles_any, list) or not particles_any:
        raise ValueError("catalog must contain non-empty 'particles' list")

    particles: list[dict[str, Any]] = [p for p in particles_any if isinstance(p, dict)]
    if not particles:
        raise ValueError("catalog 'particles' must contain object items")

    specs = [_particle_spec_from_mapping(p) for p in particles]
    specs.sort(key=lambda s: s.id)

    # Deterministic integer IDs (genanki expects int; Anki uses signed 64-bit).
    def _stable_int_id(tag: str) -> int:
        digest = hashlib.sha256(tag.encode("utf-8")).digest()
        return int.from_bytes(digest[:8], "big") & ((1 << 63) - 1)

    deck_id = _stable_int_id(f"deck|hadron_anki|{template_version}|{model_version}")
    model_id = _stable_int_id(f"model|hadron_anki|{template_version}|{model_version}")

    model = genanki.Model(
        model_id=model_id,
        name=f"hadron_anki::{model_version}",
        fields=[{"name": "Front"}, {"name": "Back"}],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Front}}",
                "afmt": "{{FrontSide}}<hr id=answer>{{Back}}",
            }
        ],
        css=CARD_CSS,
    )

    deck = genanki.Deck(deck_id=deck_id, name=f"hadron_anki::{template_version}")

    media_files: list[str] = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for spec in specs:
            svg_filename = f"{spec.id}.svg"
            svg_path = os.path.join(tmpdir, svg_filename)
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(render_svg(spec))
            media_files.append(svg_path)

            cards = generate_cards(spec, svg_filename, include_types=card_types)
            for card in cards:
                note = genanki.Note(
                    model=model,
                    fields=[card.front_html, card.back_html],
                    guid=stable_note_guid(f"{spec.id}:{card.card_type}", template_version, model_version),
                    tags=build_tags(spec, card.card_type)
                )
                deck.add_note(note)

        media_files.sort(key=lambda p: os.path.basename(p))

        package = genanki.Package(deck)
        package.media_files = media_files

        tmp_apkg = os.path.join(tmpdir, "out.apkg")
        package.write_to_file(tmp_apkg, timestamp=0.0)
        _rewrite_apkg_deterministic(tmp_apkg, out_path)
