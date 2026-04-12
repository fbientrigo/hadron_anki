from copy import deepcopy

import pytest
import yaml

from hadron_anki.domain.canonical_validator import validate_particle_record


def _load_example_particles() -> list[dict]:
    with open("data/examples/hadron_schema_example.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["particles"]


def test_pi0_flavor_superposition_validates():
    particles = _load_example_particles()
    pi0 = next(p for p in particles if p["id"] == "pi0")
    validate_particle_record(pi0)


def test_eta8_record_validates():
    particles = _load_example_particles()
    eta8 = next(p for p in particles if p["id"] == "eta8")
    validate_particle_record(eta8)


def test_invalid_quark_model_mode_fails():
    particles = _load_example_particles()
    proton = deepcopy(next(p for p in particles if p["id"] == "proton"))
    proton["exact"]["quark_model"]["mode"] = "invalid_mode"

    with pytest.raises(ValueError, match="unknown quark_model.mode"):
        validate_particle_record(proton)


def test_missing_exact_name_fails():
    particles = _load_example_particles()
    proton = deepcopy(next(p for p in particles if p["id"] == "proton"))
    del proton["exact"]["name"]

    with pytest.raises(ValueError, match="canonical particle missing exact.name"):
        validate_particle_record(proton)


def test_missing_mass_rank_in_family_does_not_fail():
    particles = _load_example_particles()
    proton = deepcopy(next(p for p in particles if p["id"] == "proton"))
    del proton["pedagogical"]["mass_rank_in_family"]

    validate_particle_record(proton)


def test_exact_name_must_be_non_empty_string():
    particles = _load_example_particles()
    proton = deepcopy(next(p for p in particles if p["id"] == "proton"))
    proton["exact"]["name"] = "   "

    with pytest.raises(ValueError, match="exact.name must be a non-empty string"):
        validate_particle_record(proton)


def test_exact_symbol_must_be_non_empty_string():
    particles = _load_example_particles()
    proton = deepcopy(next(p for p in particles if p["id"] == "proton"))
    proton["exact"]["symbol"] = ""

    with pytest.raises(ValueError, match="exact.symbol must be a non-empty string"):
        validate_particle_record(proton)


def test_exact_family_must_be_non_empty_string():
    particles = _load_example_particles()
    proton = deepcopy(next(p for p in particles if p["id"] == "proton"))
    proton["exact"]["family"] = ""

    with pytest.raises(ValueError, match="exact.family must be a non-empty string"):
        validate_particle_record(proton)


def test_exact_multiplet_must_be_non_empty_string():
    particles = _load_example_particles()
    proton = deepcopy(next(p for p in particles if p["id"] == "proton"))
    proton["exact"]["multiplet"] = ""

    with pytest.raises(ValueError, match="exact.multiplet must be a non-empty string"):
        validate_particle_record(proton)


def test_simple_valence_role_must_be_quark_or_antiquark():
    particles = _load_example_particles()
    proton = deepcopy(next(p for p in particles if p["id"] == "proton"))
    proton["exact"]["quark_model"]["constituents"][0]["role"] = "gluon"

    with pytest.raises(ValueError, match="simple_valence constituent.role must be one of"):
        validate_particle_record(proton)
