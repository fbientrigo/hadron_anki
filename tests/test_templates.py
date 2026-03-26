"""Tests for Anki card shared visual templates."""
import pytest
from hadron_anki.cards.templates import (
    render_mass_front, render_mass_back,
    render_composition_front, render_composition_back,
    render_identity_front, render_identity_back,
    render_card_shell
)
from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.cards.styles import CARD_CSS

def test_mass_card_uses_shared_shell_classes():
    spec = ParticleSpec(id="p", name="Proton", type="baryon", quarks=["u", "u", "d"], mass=938.27)
    front = render_mass_front("p")
    back = render_mass_back(spec)
    
    # Must use shared shell
    assert 'class="card-shell front"' in front
    assert 'class="card-shell back"' in back
    
    # Check mass block specifics
    assert "938.27 MeV" in back
    assert "mass-value" in back

def test_composition_card_contains_svg_wrapper_and_quark_text():
    spec = ParticleSpec(id="p", name="Proton", type="baryon", quarks=["u", "u", "d"])
    back = render_composition_back(spec, "proton.svg")
    
    assert 'class="card-shell back"' in back
    
    # Check SVG wrapper
    assert 'class="media-wrap"' in back
    assert '<img src="proton.svg">' in back
    
    # Check Quark structure
    assert 'class="answer quark-text"' in back
    assert "u" in back and "d" in back

def test_identity_card_uses_reverse_recall_layout():
    spec = ParticleSpec(id="p", name="Proton", type="baryon", quarks=["u", "u", "d"])
    front = render_identity_front(spec)
    back = render_identity_back(spec, "p")
    
    assert 'class="card-shell front"' in front
    assert 'class="card-shell back"' in back
    
    # Front is quark text
    assert 'class="prompt quark-text"' in front
    assert "u" in front
    
    # Back is textual name and symbol and badge
    assert 'class="title"' in back
    assert "Proton" in back
    assert 'class="badge baryon"' in back
    assert 'class="answer"' in back
    assert ">p<" in back

def test_shared_css_contains_expected_tokens_or_classes():
    assert ".card-shell" in CARD_CSS
    assert ".badge" in CARD_CSS
    assert ".title" in CARD_CSS
    assert ".prompt" in CARD_CSS
    assert ".answer" in CARD_CSS
    assert ".media-wrap" in CARD_CSS
    assert ".meta" in CARD_CSS
    assert ".quark-text" in CARD_CSS
    assert ".mass-value" in CARD_CSS
