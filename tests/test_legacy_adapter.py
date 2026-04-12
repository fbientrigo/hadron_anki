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


def test_adapter_fails_explicitly_for_flavor_superposition():
    particles = _load_example_particles()
    pi0 = next(p for p in particles if p["id"] == "pi0")

    with pytest.raises(
        ValueError,
        match="legacy adapter does not support flavor_superposition for particle pi0",
    ):
        canonical_to_legacy_particlespec(pi0)
