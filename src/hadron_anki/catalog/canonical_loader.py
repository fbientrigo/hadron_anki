from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from hadron_anki.domain.canonical_validator import validate_particle_record
from hadron_anki.domain.pedagogical_schema import CanonicalParticle


def _load_raw(path: str | Path) -> dict[str, Any]:
    catalog_path = Path(path)
    suffix = catalog_path.suffix.lower()
    with catalog_path.open("r", encoding="utf-8") as f:
        if suffix in {".yaml", ".yml"}:
            data = yaml.safe_load(f)
        elif suffix == ".json":
            data = json.load(f)
        else:
            raise ValueError("Unsupported catalog format: must be .json/.yaml/.yml")

    if not isinstance(data, dict):
        raise ValueError("canonical catalog root must be an object")
    return data


def _validate_catalog_shape(data: dict[str, Any]) -> None:
    if "schema_version" not in data:
        raise ValueError("canonical catalog missing schema_version")

    particles = data.get("particles")
    if not isinstance(particles, list) or len(particles) == 0:
        raise ValueError("canonical catalog 'particles' must be a non-empty list")

    for record in particles:
        validate_particle_record(record)


def load_canonical_catalog(path: str | Path) -> dict[str, Any]:
    data = _load_raw(path)
    _validate_catalog_shape(data)
    return data


def load_canonical_particles(path: str | Path) -> list[CanonicalParticle]:
    data = load_canonical_catalog(path)
    particles = data["particles"]
    return list(particles)
