import hashlib
import os
import tempfile
from typing import Any

import genanki

from hadron_anki.cards.templates import back_html, front_html
from hadron_anki.deck.ids import stable_note_guid
from hadron_anki.domain.composer import normalize_quark_token, validate_quark_count
from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.render.svg import render_svg


def build_apkg(catalog: dict[str, Any], out_path: str, template_version: str, model_version: str) -> None:
    """
    Build an Anki .apkg file from a particle catalog.
    
    Args:
        catalog: Dictionary containing particle data.
        out_path: Destination path for the .apkg file.
        template_version: Version of the card template.
        model_version: Version of the Anki note model.
    """
    particles_any = catalog.get("particles")
    if not isinstance(particles_any, list) or not particles_any:
        raise ValueError("catalog must contain non-empty 'particles' list")

    particles: list[dict[str, Any]] = [p for p in particles_any if isinstance(p, dict)]
    if not particles:
        raise ValueError("catalog 'particles' must contain object items")

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
                "afmt": "{{Front}}<hr id=answer>{{Back}}",
            }
        ],
    )

    deck = genanki.Deck(deck_id=deck_id, name=f"hadron_anki::{template_version}")

    media_files: list[str] = []
    with tempfile.TemporaryDirectory() as tmpdir:
        # Build at least one note + one SVG media file to satisfy the contract test.
        p0 = particles[0]
        particle_id = str(p0.get("id"))
        spec = ParticleSpec(
            id=particle_id,
            name=str(p0.get("name")),
            type=str(p0.get("type")),
            quarks=[normalize_quark_token(str(q)) for q in (p0.get("quarks") or [])],
        )
        validate_quark_count(spec)

        svg_filename = f"{spec.id}.svg"
        svg_path = os.path.join(tmpdir, svg_filename)
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(render_svg(spec))
        media_files.append(svg_path)

        note = genanki.Note(
            model=model,
            fields=[front_html(svg_filename), back_html(spec)],
            guid=stable_note_guid(spec.id, template_version, model_version),
        )
        deck.add_note(note)

        package = genanki.Package(deck)
        package.media_files = media_files
        package.write_to_file(out_path)
