import pytest

from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.cards.mapping import generate_cards, CardSpec

def test_mass_card_generated_only_if_mass_present():
    spec_with_mass = ParticleSpec(id="p", name="Proton", type="baryon", quarks=["u", "u", "d"], mass=938.27)
    spec_no_mass = ParticleSpec(id="n", name="Neutron", type="baryon", quarks=["u", "d", "d"], mass=None)
    
    cards_with = generate_cards(spec_with_mass, "p.svg")
    assert any(c.card_type == "mass" for c in cards_with)
    
    cards_without = generate_cards(spec_no_mass, "n.svg")
    assert not any(c.card_type == "mass" for c in cards_without)

def test_particle_generates_three_cards():
    spec = ParticleSpec(id="p", name="Proton", type="baryon", quarks=["u", "u", "d"], mass=938.27)
    cards = generate_cards(spec, "p.svg")
    assert len(cards) == 3
    types = {c.card_type for c in cards}
    assert types == {"mass", "composition", "identity"}

def test_composition_card_contains_svg_reference():
    spec = ParticleSpec(id="p", name="Proton", type="baryon", quarks=["u", "u", "d"])
    cards = generate_cards(spec, "p.svg")
    
    comp_card = next(c for c in cards if c.card_type == "composition")
    assert "p.svg" in comp_card.back_html

def test_identity_card_reverses_mapping():
    spec = ParticleSpec(id="p", name="Proton", type="baryon", quarks=["u", "u", "d"])
    cards = generate_cards(spec, "p.svg")
    
    id_card = next(c for c in cards if c.card_type == "identity")
    # Front has quarks
    assert "u" in id_card.front_html
    assert "d" in id_card.front_html
    # Back has particle name
    assert "Proton" in id_card.back_html
