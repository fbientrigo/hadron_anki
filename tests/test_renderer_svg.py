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
    style = {
        "flavors": {
            "u": "#FF0000",
            "d": "#0000FF"
        }
    }
    output = render_svg(spec, style=style)
    h = hashlib.sha256(output.encode()).hexdigest()
    expected_hash = "8584d404fa9a68e578d3e642f8d65918005a509a8fced6c42c169e3b10bf8624"
    assert h == expected_hash

def test_svg_applies_fill_colors_from_config():
    spec = ParticleSpec(id="p", name="proton", type="baryon", quarks=["u", "u", "d"])
    style = {
        "flavors": {
            "u": "#FF0000",
            "d": "#0000FF"
        }
    }
    output = render_svg(spec, style=style)
    assert 'fill="#FF0000"' in output
    assert 'fill="#0000FF"' in output

def test_antiquark_has_dashed_stroke_and_flavor_color():
    spec = ParticleSpec(id="pi+", name="pion", type="meson", quarks=["u", "anti-d"])
    style = {
        "flavors": {
            "u": "#FF0000",
            "d": "#0000FF"
        }
    }
    output = render_svg(spec, style=style)
    assert 'fill="#0000FF"' in output
    assert 'stroke-dasharray' in output
