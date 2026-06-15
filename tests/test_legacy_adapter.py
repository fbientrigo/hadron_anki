import pytest
import yaml

from hadron_anki.domain.legacy_adapter import canonical_to_legacy_particlespec


def _load_example_particles() -> list[dict]:
    with open("data/examples/hadron_schema_example.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["particles"]


def test_adapter_converts_proton_to_legacy_particlespec():
    particles = _load_example_particles()
    proton = next(p for p in particles if p["id"] == "proton")

    spec = canonical_to_legacy_particlespec(proton)

    assert spec.id == "proton"
    assert spec.name == "Proton"
    assert spec.type == "baryon"
    assert spec.quarks == ["u", "u", "d"]
    assert spec.symbol == "p"
    assert spec.mass == pytest.approx(938.272088)


def test_adapter_populates_multiplet_and_pedagogical_fields():
    particles = _load_example_particles()
    proton = next(p for p in particles if p["id"] == "proton")

    spec = canonical_to_legacy_particlespec(proton)

    assert spec.multiplet == "baryon_octet"
    assert spec.diagram_mode == "simple_triplet"
    assert spec.display_quark_summary == "u u d"
    # bucket + rounded display + precise value
    assert spec.mass_summary == "intermediate · ≈938 MeV (938.27 MeV)"


def test_adapter_handles_flavor_superposition():
    particles = _load_example_particles()
    pi0 = next(p for p in particles if p["id"] == "pi0")

    spec = canonical_to_legacy_particlespec(pi0)

    assert spec.id == "pi0"
    assert spec.quarks == []
    assert spec.diagram_mode == "flavor_superposition"
    assert spec.display_quark_summary == "(u ubar - d dbar)/sqrt(2)"
