import hashlib
from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.render.svg import render_svg

def test_render_svg_returns_svg_string():
    # Contract: renderer returns an SVG string.
    spec = ParticleSpec(id="p", name="proton", type="baryon", quarks=["u", "u", "d"])
    output = render_svg(spec)
    assert isinstance(output, str)
    assert output.lstrip().lower().startswith("<svg")

def test_render_svg_contract_expectations():
    """
    This test defines the contract for the SVG renderer.
    Once implemented, it should:
    1. Return a string
    2. Contain <svg as root element
    3. Include quark tokens from the spec
    """
    spec = ParticleSpec(id="p", name="proton", type="baryon", quarks=["u", "u", "d"])
    
    output = render_svg(spec)
    assert isinstance(output, str)
    assert "<svg" in output.lower()
    for quark in spec.quarks:
        assert quark in output

def test_meson_svg_has_two_circles_and_connector():
    spec = ParticleSpec(id="pi+", name="pion", type="meson", quarks=["u", "anti-d"])
    output = render_svg(spec)
    assert output.count("<circle") == 2
    assert "<path" in output

def test_baryon_svg_has_three_circles():
    spec = ParticleSpec(id="p", name="proton", type="baryon", quarks=["u", "u", "d"])
    output = render_svg(spec)
    assert output.count("<circle") == 3

def test_svg_includes_expected_labels():
    spec = ParticleSpec(id="pi-", name="pion minus", type="meson", quarks=["d", "anti-u"])
    output = render_svg(spec)
    assert "d" in output
    assert "anti-u" in output

def test_svg_deterministic_hash_for_fixed_input():
    spec = ParticleSpec(id="p", name="proton", type="baryon", quarks=["u", "u", "d"])
    output = render_svg(spec)
    h = hashlib.sha256(output.encode()).hexdigest()
    # Placeholder hash - will fail initially
    expected_hash = "DETERMINISTIC_HASH_PLACEHOLDER"
    assert h == expected_hash
