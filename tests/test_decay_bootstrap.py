"""
TDD tests for src/hadron_anki/catalog/bootstrap_decays.py

Fetch layer is isolated: parser/normalization are unit-tested with
fixed fixtures so tests work offline.
"""
import pytest
from hadron_anki.catalog.bootstrap_decays import (
    normalize_pdg_name,
    is_effectively_stable,
    parse_dominant_decay,
    DecayRecord,
)


# ── Fixtures (offline) ─────────────────────────────────────────────────────

STABLE_FIXTURE = {
    "pdg_name": "p",
    "ctau_mm": float("inf"),
    "branching_fractions": [],  # no decays
}

PI_PLUS_FIXTURE = {
    "pdg_name": "pi+",
    "ctau_mm": 7804.42,
    "branching_fractions": [
        {
            "description": "pi+ --> mu+ nu_mu",
            "value": 0.999877,
            "is_limit": False,
            "decay_products": ["mu+", "nu_mu"],
        },
        {
            "description": "pi+ --> e+ nu_e",
            "value": 1.23e-4,
            "is_limit": False,
            "decay_products": ["e+", "nu_e"],
        },
    ],
}

NEUTRON_FIXTURE = {
    "pdg_name": "n",
    "ctau_mm": 2.633e14,
    "branching_fractions": [
        {
            "description": "n --> p e- nu_ebar",
            "value": 1.0,
            "is_limit": False,
            "decay_products": ["p", "e-", "nu_ebar"],
        }
    ],
}

SIGMA_ZERO_FIXTURE = {
    "pdg_name": "Sigma0",
    "ctau_mm": 2.217e-8,  # effectively stable: EM decay, sub-fm
    "branching_fractions": [
        {
            "description": "Sigma0 --> Lambda gamma",
            "value": 1.0,
            "is_limit": False,
            "decay_products": ["Lambda", "gamma"],
        }
    ],
}


# ── Tests: Stability ───────────────────────────────────────────────────────

def test_decay_bootstrap_handles_stable_particle():
    """Proton should be marked stable (ctau = inf)."""
    assert is_effectively_stable(STABLE_FIXTURE) is True


def test_proton_is_stable():
    """Proton ctau is infinite, so it is stable."""
    assert is_effectively_stable({"pdg_name": "p", "ctau_mm": float("inf"), "branching_fractions": []}) is True


def test_pion_is_not_stable():
    """pi+ (ctau ~7.8m) is not stable."""
    assert is_effectively_stable(PI_PLUS_FIXTURE) is False


def test_neutron_is_not_stable():
    """Neutron (ctau ~2.6e14 mm) is very long-lived, but not stable for deck purposes."""
    assert is_effectively_stable(NEUTRON_FIXTURE) is False


def test_sigma_zero_treated_as_unstable():
    """Sigma0 decays electromagnetically — very short, but still marked unstable."""
    assert is_effectively_stable(SIGMA_ZERO_FIXTURE) is False


# ── Tests: Dominant decay extraction ──────────────────────────────────────

def test_decay_bootstrap_extracts_main_decay_for_pi_plus():
    """pi+ dominant decay should be pi+ -> mu+ nu_mu with BR ~0.9999."""
    record = parse_dominant_decay("pi_plus", PI_PLUS_FIXTURE)
    assert record is not None
    assert record.parent == "pi_plus"
    assert "mu_plus" in record.children
    assert "nu_mu" in record.children
    assert abs(record.branching_ratio - 0.999877) < 1e-6


def test_decay_bootstrap_extracts_main_decay_for_neutron():
    """Neutron dominant decay should be n -> p e- anti_nu_e."""
    record = parse_dominant_decay("neutron", NEUTRON_FIXTURE)
    assert record is not None
    assert record.parent == "neutron"
    assert "proton" in record.children
    assert record.branching_ratio == pytest.approx(1.0, rel=1e-4)


def test_dominant_decay_selects_highest_bf():
    """When multiple decay modes exist, the highest BR is selected."""
    record = parse_dominant_decay("pi_plus", PI_PLUS_FIXTURE)
    assert record.branching_ratio > 0.99


def test_stable_particle_returns_none_decay():
    """parse_dominant_decay returns None for a stable particle."""
    record = parse_dominant_decay("proton", STABLE_FIXTURE)
    assert record is None


# ── Tests: Name normalization ──────────────────────────────────────────────

def test_decay_children_are_normalized_to_repo_ids():
    """Children names should be repo-safe snake_case IDs."""
    record = parse_dominant_decay("pi_plus", PI_PLUS_FIXTURE)
    for child in record.children:
        assert " " not in child, f"child '{child}' has whitespace"
        assert child == child.lower() or child.startswith("nu"), f"child '{child}' is not normalized"


def test_normalize_pdg_name_pi_plus():
    assert normalize_pdg_name("pi+") == "pi_plus"


def test_normalize_pdg_name_antiparticle():
    assert normalize_pdg_name("nu_ebar") == "anti_nu_e"


def test_normalize_pdg_name_proton():
    assert normalize_pdg_name("p") == "proton"


def test_normalize_pdg_name_neutron():
    assert normalize_pdg_name("n") == "neutron"


def test_normalize_pdg_name_mu_plus():
    assert normalize_pdg_name("mu+") == "mu_plus"


def test_normalize_pdg_name_mu_minus():
    assert normalize_pdg_name("mu-") == "mu_minus"


def test_normalize_pdg_name_lambda():
    assert normalize_pdg_name("Lambda") == "lambda_0"


def test_normalize_pdg_name_gamma():
    assert normalize_pdg_name("gamma") == "gamma"


# ── Tests: DecayRecord schema ──────────────────────────────────────────────

def test_decay_record_has_source_fields():
    """DecayRecord must carry source and source_kind fields."""
    record = parse_dominant_decay("pi_plus", PI_PLUS_FIXTURE)
    assert hasattr(record, "source")
    assert hasattr(record, "source_kind")
    assert record.source_kind in ("pdg_python_api", "fixture", "manual")
