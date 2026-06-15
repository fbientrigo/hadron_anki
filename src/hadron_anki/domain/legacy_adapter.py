from __future__ import annotations

from typing import Any, Mapping

from hadron_anki.domain.canonical_validator import validate_particle_record
from hadron_anki.domain.pedagogical_derivations import derive_pedagogical_fields
from hadron_anki.domain.spec import ParticleSpec


def _as_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be an object")
    return value


def _simple_valence_quarks(quark_model: Mapping[str, Any]) -> list[str]:
    quarks: list[str] = []
    for constituent in quark_model["constituents"]:
        part = _as_mapping(constituent, "exact.quark_model.constituent")
        flavor = str(part["quark"])
        if part["role"] == "antiquark":
            quarks.append(f"anti-{flavor}")
        else:
            quarks.append(flavor)
    return quarks


def canonical_to_legacy_particlespec(record: Any) -> ParticleSpec:
    """Convert a canonical particle record into a display-ready ParticleSpec.

    Flavor-superposition states (e.g. pi0) carry an empty ``quarks`` list and
    rely on ``display_quark_summary`` / ``diagram_mode`` for rendering.
    """
    validate_particle_record(record)
    record_map = _as_mapping(record, "particle")

    exact = _as_mapping(record_map["exact"], "exact")
    quark_model = _as_mapping(exact["quark_model"], "exact.quark_model")
    mode = quark_model["mode"]

    quarks = _simple_valence_quarks(quark_model) if mode == "simple_valence" else []

    derived = derive_pedagogical_fields(record_map)

    return ParticleSpec(
        id=str(record_map["id"]),
        name=str(exact["name"]),
        type=str(exact["hadron_type"]),
        quarks=quarks,
        symbol=str(exact["symbol"]),
        symbol_tex=exact.get("symbol_tex"),
        mass=float(exact["mass_mev_exact"]),
        multiplet=str(exact["multiplet"]),
        mass_summary=derived["mass_summary"],
        display_quark_summary=derived["display_quark_summary"],
        diagram_mode=derived["diagram_mode"],
    )
