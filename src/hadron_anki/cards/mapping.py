from dataclasses import dataclass
from typing import Optional

from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.cards import templates

@dataclass
class CardSpec:
    card_type: str
    front_html: str
    back_html: str
    media: Optional[str] = None

def generate_cards(
    spec: ParticleSpec, 
    svg_filename: str, 
    include_types: Optional[list[str]] = None,
    decay_svg_filename: Optional[str] = None
) -> list[CardSpec]:
    """
    Transforms a ParticleSpec into a list of learning cards.
    Valid include_types: 'mass', 'composition', 'identity', 'decay'.
    If None, all applicable cards are generated.
    """
    cards = []
    display_name = spec.symbol if spec.symbol else spec.name
    
    def should_include(card_type):
        return include_types is None or card_type in include_types

    # 1) MASS CARD
    if spec.mass is not None and should_include("mass"):
        mass_front = templates.render_mass_front(display_name, spec)
        mass_back = templates.render_mass_back(spec, display_name)
        cards.append(CardSpec("mass", mass_front, mass_back))

    # 2) COMPOSITION CARD
    if should_include("composition"):
        comp_front = templates.render_composition_front(display_name, spec)
        comp_back = templates.render_composition_back(spec, svg_filename)
        cards.append(CardSpec("composition", comp_front, comp_back, media=svg_filename))

    # 3) IDENTITY CARD
    if should_include("identity"):
        id_front = templates.render_identity_front(spec)
        id_back = templates.render_identity_back(spec, display_name)
        cards.append(CardSpec("identity", id_front, id_back))

    # 4) DECAY CARD
    if spec.decay_diagram and decay_svg_filename and should_include("decay"):
        decay_front = templates.render_decay_front(display_name, spec)
        decay_back = templates.render_decay_back(spec, display_name, decay_svg_filename)
        cards.append(CardSpec("decay", decay_front, decay_back, media=decay_svg_filename))

    return cards
