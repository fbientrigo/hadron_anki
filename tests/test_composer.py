import pytest
from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.domain.composer import normalize_quark_token, validate_quark_count

def test_normalize_quark_token_canonicalizes_antiquarks():
    """canonical antiquark token uses anti- prefix"""
    assert normalize_quark_token("ubar") == "anti-u"
    assert normalize_quark_token("dbar") == "anti-d"

def test_normalize_quark_token_is_idempotent():
    """idempotent on already-normalized tokens"""
    assert normalize_quark_token("anti-u") == "anti-u"
    assert normalize_quark_token("anti-d") == "anti-d"

def test_normalize_quark_token_leaves_regular_quarks_unchanged():
    """regular quarks (e.g., 'u', 'd') -> output unchanged"""
    assert normalize_quark_token("u") == "u"
    assert normalize_quark_token("d") == "d"

def test_validate_quark_count_baryon_must_have_3_quarks():
    """baryon must have 3 quarks"""
    spec = ParticleSpec(id="p", name="proton", type="baryon", quarks=["u", "u"])
    with pytest.raises(ValueError, match="baryon must have 3 quarks"):
        validate_quark_count(spec)

def test_validate_quark_count_meson_must_have_2_quarks():
    """meson must have 2 quarks"""
    spec = ParticleSpec(id="pi_plus", name="pi+", type="meson", quarks=["u", "anti-d", "d"])
    with pytest.raises(ValueError, match="meson must have 2 quarks"):
        validate_quark_count(spec)

def test_validate_quark_count_valid_specs():
    """Valid specs -> no exception"""
    proton = ParticleSpec(id="p", name="proton", type="baryon", quarks=["u", "u", "d"])
    pion = ParticleSpec(id="pi_plus", name="pi+", type="meson", quarks=["u", "anti-d"])
    
    # Should not raise
    validate_quark_count(proton)
    validate_quark_count(pion)
