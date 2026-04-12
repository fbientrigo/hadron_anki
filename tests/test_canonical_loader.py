from pathlib import Path

import pytest

from hadron_anki.catalog.canonical_loader import (
    load_canonical_catalog,
    load_canonical_particles,
)


EXAMPLE_PATH = Path("data/examples/hadron_schema_example.yaml")


def test_load_canonical_catalog_valid_example():
    catalog = load_canonical_catalog(EXAMPLE_PATH)
    assert catalog["schema_version"] == 1
    assert isinstance(catalog["particles"], list)
    assert len(catalog["particles"]) >= 5


def test_load_canonical_particles_contains_proton_and_neutron():
    particles = load_canonical_particles(EXAMPLE_PATH)
    ids = {p["id"] for p in particles}
    assert "proton" in ids
    assert "neutron" in ids


def test_load_canonical_particles_contains_eta8():
    particles = load_canonical_particles(EXAMPLE_PATH)
    ids = {p["id"] for p in particles}
    assert "eta8" in ids


def test_load_canonical_catalog_rejects_jsonc_suffix(tmp_path):
    path = tmp_path / "catalog.jsonc"
    path.write_text('{"schema_version": 1, "particles": []}', encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported catalog format"):
        load_canonical_catalog(path)
