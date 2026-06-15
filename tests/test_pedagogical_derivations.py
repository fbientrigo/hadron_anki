from __future__ import annotations

from copy import deepcopy

import pytest
import yaml

from hadron_anki.domain.legacy_adapter import canonical_to_legacy_particlespec
from hadron_anki.domain.pedagogical_derivations import (
    derive_catalog_pedagogical_fields,
    derive_diagram_mode,
    derive_display_quark_summary,
    derive_mass_bucket,
    derive_mass_display,
    derive_mass_rank_in_family,
    derive_pedagogical_fields,
)


def _load_example_particles() -> list[dict]:
    with open("data/examples/hadron_schema_example.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["particles"]


def _particle_by_id(particles: list[dict], particle_id: str) -> dict:
    return next(p for p in particles if p["id"] == particle_id)


def test_derive_mass_display_examples():
    particles = _load_example_particles()
    proton = _particle_by_id(particles, "proton")
    neutron = _particle_by_id(particles, "neutron")
    eta8 = _particle_by_id(particles, "eta8")

    assert derive_mass_display(proton["exact"]["mass_mev_exact"]) == "938 MeV"
    assert derive_mass_display(neutron["exact"]["mass_mev_exact"]) == "940 MeV"
    assert derive_mass_display(eta8["exact"]["mass_mev_exact"]) == "548 MeV"
    assert derive_mass_display(1314.86) == "1310 MeV"


@pytest.mark.parametrize(
    ("mass_mev_exact", "expected"),
    [
        (100.0, "ultralight"),
        (200.0, "light"),
        (700.0, "intermediate"),
        (1200.0, "heavy"),
    ],
)
def test_derive_mass_bucket_bins(mass_mev_exact: float, expected: str):
    assert derive_mass_bucket(mass_mev_exact) == expected


def test_derive_diagram_mode_examples():
    particles = _load_example_particles()
    proton = _particle_by_id(particles, "proton")
    pi_plus = _particle_by_id(particles, "pi_plus")
    pi0 = _particle_by_id(particles, "pi0")

    assert derive_diagram_mode(proton) == "simple_triplet"
    assert derive_diagram_mode(pi_plus) == "simple_pair"
    assert derive_diagram_mode(pi0) == "flavor_superposition"


def test_derive_display_quark_summary_examples():
    particles = _load_example_particles()
    proton = _particle_by_id(particles, "proton")
    pi_plus = _particle_by_id(particles, "pi_plus")
    pi0 = _particle_by_id(particles, "pi0")
    eta8 = _particle_by_id(particles, "eta8")

    assert derive_display_quark_summary(proton) == "u u d"
    assert derive_display_quark_summary(pi_plus) == "u anti-d"
    assert derive_display_quark_summary(pi0) == "(u ubar - d dbar)/sqrt(2)"
    assert derive_display_quark_summary(eta8) == "(u ubar + d dbar - 2 s sbar)/sqrt(6)"


def test_derive_mass_rank_in_family_nucleon_order():
    particles = _load_example_particles()
    nucleon_records = [
        _particle_by_id(particles, "proton"),
        _particle_by_id(particles, "neutron"),
    ]

    rank_map = derive_mass_rank_in_family(nucleon_records)
    assert rank_map == {"proton": 1, "neutron": 2}


def test_derive_mass_rank_in_family_tiebreaker_lexicographic_id():
    records = [
        {
            "id": "b_particle",
            "exact": {"family": "testfam", "mass_mev_exact": 100.0},
        },
        {
            "id": "a_particle",
            "exact": {"family": "testfam", "mass_mev_exact": 100.0},
        },
    ]

    rank_map = derive_mass_rank_in_family(records)
    assert rank_map == {"a_particle": 1, "b_particle": 2}


def test_derive_pedagogical_fields_minimal_block_and_optional_rank():
    particles = _load_example_particles()
    proton = _particle_by_id(particles, "proton")
    eta8 = _particle_by_id(particles, "eta8")

    proton_fields = derive_pedagogical_fields(proton)
    assert proton_fields["mass_display"] == "938 MeV"
    assert proton_fields["mass_bucket"] == "intermediate"
    assert proton_fields["diagram_mode"] == "simple_triplet"
    assert proton_fields["display_quark_summary"] == "u u d"
    assert "mass_rank_in_family" not in proton_fields

    eta8_fields = derive_pedagogical_fields(eta8, family_records=[eta8])
    assert "mass_rank_in_family" not in eta8_fields


def test_derive_catalog_pedagogical_fields_enriches_and_keeps_exact():
    particles = _load_example_particles()
    original = deepcopy(particles)

    enriched = derive_catalog_pedagogical_fields(particles)
    assert len(enriched) == len(particles)

    original_exact_by_id = {p["id"]: p["exact"] for p in original}
    for record in enriched:
        assert record["exact"] == original_exact_by_id[record["id"]]
        assert "pedagogical" in record

    pi0_enriched = _particle_by_id(enriched, "pi0")
    eta8_enriched = _particle_by_id(enriched, "eta8")
    assert pi0_enriched["pedagogical"]["diagram_mode"] == "flavor_superposition"
    assert eta8_enriched["pedagogical"]["diagram_mode"] == "flavor_superposition"
    assert pi0_enriched["pedagogical"]["display_quark_summary"] == "(u ubar - d dbar)/sqrt(2)"
    assert (
        eta8_enriched["pedagogical"]["display_quark_summary"]
        == "(u ubar + d dbar - 2 s sbar)/sqrt(6)"
    )


def test_legacy_adapter_supports_flavor_superposition_pi0():
    particles = _load_example_particles()
    pi0 = _particle_by_id(particles, "pi0")

    spec = canonical_to_legacy_particlespec(pi0)

    assert spec.quarks == []
    assert spec.diagram_mode == "flavor_superposition"
    assert spec.display_quark_summary == "(u ubar - d dbar)/sqrt(2)"
