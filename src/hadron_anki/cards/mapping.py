from dataclasses import dataclass
from typing import Optional

from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.domain.composer import format_quark_display

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
    quarks_display = " ".join(format_quark_display(q) for q in spec.quarks)
    display_name = spec.symbol if spec.symbol else spec.name

    # 1) MASS CARD
    if spec.mass is not None:
        mass_front = (
            f'<div class="hadron-card hadron-front">'
            f'<div class="prompt">{display_name}</div>'
            f'<div class="prompt">What is the mass?</div>'
            f'</div>'
        )
        mass_back = (
            f'<div class="hadron-card hadron-back">'
            f'<div class="particle-name">{spec.name}</div>'
            f'<div class="property-value">{spec.mass} MeV</div>'
            f'</div>'
        )
        cards.append(CardSpec("mass", mass_front, mass_back))

    # 2) COMPOSITION CARD
    comp_front = (
        f'<div class="hadron-card hadron-front">'
        f'<div class="prompt">{display_name}</div>'
        f'<div class="prompt">What is its quark composition?</div>'
        f'</div>'
    )
    # The back needs SVG
    comp_back = (
        f'<div class="hadron-card hadron-back">'
        f'<div class="diagram"><img src="{svg_filename}"></div>'
        f'<div class="quark-composition">{quarks_display}</div>'
        f'</div>'
    )
    cards.append(CardSpec("composition", comp_front, comp_back, media=svg_filename))

    # 3) IDENTITY CARD
    id_front = (
        f'<div class="hadron-card hadron-front">'
        f'<div class="prompt">{quarks_display}</div>'
        f'<div class="prompt">Which particle is this?</div>'
        f'</div>'
    )
    id_back = (
        f'<div class="hadron-card hadron-back">'
        f'<div class="particle-name">{spec.name}</div>'
        f'<div class="prompt">{display_name}</div>'
        f'</div>'
    )
    cards.append(CardSpec("identity", id_front, id_back))

    return cards
