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

def generate_cards(spec: ParticleSpec, svg_filename: str) -> list[CardSpec]:
    """
    Transforms a ParticleSpec into a list of learning cards.
    """
    cards = []
    display_name = spec.symbol if spec.symbol else spec.name

    # 1) MASS CARD
    if spec.mass is not None:
        mass_front = templates.render_mass_front(display_name)
        mass_back = templates.render_mass_back(spec)
        cards.append(CardSpec("mass", mass_front, mass_back))

    # 2) COMPOSITION CARD
    comp_front = templates.render_composition_front(display_name)
    comp_back = templates.render_composition_back(spec, svg_filename)
    cards.append(CardSpec("composition", comp_front, comp_back, media=svg_filename))

    # 3) IDENTITY CARD
    id_front = templates.render_identity_front(spec)
    id_back = templates.render_identity_back(spec, display_name)
    cards.append(CardSpec("identity", id_front, id_back))

    return cards
