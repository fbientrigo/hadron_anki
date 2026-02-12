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
