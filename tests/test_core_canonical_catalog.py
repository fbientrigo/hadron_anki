"""Tests for the core canonical catalog and the spec assembly pipeline."""
from hadron_anki.catalog.loader import load_catalog
from hadron_anki.catalog.canonical_loader import load_canonical_catalog
from hadron_anki.catalog.build import build_specs

CANONICAL_PATH = "catalogs/core_particles.canonical.yaml"
DECAYS_PATH = "catalogs/core_decays.yaml"

EXPECTED_IDS = {
    "proton", "neutron", "lambda_0",
    "sigma_plus", "sigma_zero", "sigma_minus",
    "xi_zero", "xi_minus", "omega_minus",
    "pi_plus", "pi_minus", "pi_zero",
    "k_plus", "k_minus", "k_zero",
}


def test_canonical_catalog_loads_and_validates_all_particles():
    catalog = load_canonical_catalog(CANONICAL_PATH)
    ids = {p["id"] for p in catalog["particles"]}
    assert ids == EXPECTED_IDS


def test_every_particle_carries_a_multiplet():
    catalog = load_canonical_catalog(CANONICAL_PATH)
    for particle in catalog["particles"]:
        assert particle["exact"]["multiplet"]


def test_build_specs_enriches_with_octet_mass_and_decay():
    catalog = load_canonical_catalog(CANONICAL_PATH)
    decays = load_catalog(DECAYS_PATH)
    specs = {s.id: s for s in build_specs(catalog, decays)}

    proton = specs["proton"]
    assert proton.multiplet == "baryon_octet"
    assert "MeV" in proton.mass_summary

    # Unstable particles get a decay + a diagram for the Feynman card.
    lambda_0 = specs["lambda_0"]
    assert lambda_0.decay["children"] == ["proton", "pi_minus"]
    assert lambda_0.decay_diagram is not None


def test_every_unstable_particle_has_a_decay_diagram():
    catalog = load_canonical_catalog(CANONICAL_PATH)
    decays = load_catalog(DECAYS_PATH)
    for spec in build_specs(catalog, decays):
        if spec.decay:
            assert spec.decay_diagram is not None, f"{spec.id} missing decay diagram"


def test_hand_authored_diagram_overrides_generated_one():
    catalog = load_canonical_catalog(CANONICAL_PATH)
    decays = load_catalog(DECAYS_PATH)
    specs = {s.id: s for s in build_specs(catalog, decays)}

    # pi_plus has a hand-authored W-boson diagram in the catalog.
    edge_types = {e["type"] for e in specs["pi_plus"].decay_diagram["edges"]}
    assert "boson" in edge_types
