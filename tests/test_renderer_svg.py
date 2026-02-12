import pytest
from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.render.svg import render_svg

def test_render_svg_fails_with_not_implemented():
    # This test is EXPECTED TO FAIL to demonstrate RED state
    spec = ParticleSpec(id="p", name="proton", type="baryon", quarks=["u", "u", "d"])
    render_svg(spec)

def test_render_svg_contract_expectations():
    """
    This test defines the contract for the SVG renderer.
    Once implemented, it should:
    1. Return a string
    2. Contain <svg as root element
    3. Include quark tokens from the spec
    """
    spec = ParticleSpec(id="p", name="proton", type="baryon", quarks=["u", "u", "d"])
    
    # In TDD RED state, this will raise NotImplementedError
    # We wrap it to show we are testing the stub
    with pytest.raises(NotImplementedError):
        output = render_svg(spec)
        
        # Future assertions (contract):
        # assert isinstance(output, str)
        # assert "<svg" in output.lower()
        # for quark in spec.quarks:
        #     assert quark in output
