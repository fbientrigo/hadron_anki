from __future__ import annotations

from typing import Any, Mapping

from hadron_anki.domain.canonical_validator import validate_particle_record
from hadron_anki.domain.spec import ParticleSpec


def _as_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be an object")
    return value


def canonical_to_legacy_particlespec(record: Any) -> ParticleSpec:
    validate_particle_record(record)
    record_map = _as_mapping(record, "particle")

    particle_id = record_map["id"]
    exact = _as_mapping(record_map["exact"], "exact")
    quark_model = _as_mapping(exact["quark_model"], "exact.quark_model")
    mode = quark_model["mode"]

    if mode == "flavor_superposition":
        raise ValueError(
            f"legacy adapter does not support flavor_superposition for particle {particle_id}"
        )
    if mode != "simple_valence":
        raise ValueError(f"unknown quark_model.mode: {mode}")

    constituents = quark_model["constituents"]
    quarks: list[str] = []
    for constituent in constituents:
        part = _as_mapping(constituent, "exact.quark_model.constituent")
        flavor = str(part["quark"])
        role = part["role"]
        if role == "antiquark":
            quarks.append(f"anti-{flavor}")
        else:
            quarks.append(flavor)

    return ParticleSpec(
        id=str(particle_id),
        name=str(exact["name"]),
        type=str(exact["hadron_type"]),
        quarks=quarks,
        symbol=str(exact["symbol"]),
        mass=float(exact["mass_mev_exact"]),
    )
