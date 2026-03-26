"""
Anki card HTML templates for hadron particles.

These functions produce HTML fragments that use shared CSS classes
defined in hadron_anki.cards.styles.
"""
from typing import Optional
from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.domain.composer import format_quark_display

def render_card_shell(content: str, card_side: str, card_type: str) -> str:
    """Renders the shared base shell for all cards."""
    return f'<div class="card-shell {card_side} {card_type}-layout">\n{content}\n</div>'

def render_mass_front(display_name: str) -> str:
    content = (
        f'<div class="title">{display_name}</div>\n'
        f'<div class="prompt">What is the mass?</div>'
    )
    return render_card_shell(content, "front", "mass")

def render_mass_back(spec: ParticleSpec) -> str:
    content = (
        f'<div class="title">{spec.name}</div>\n'
        f'<div class="badge {spec.type}">{spec.type}</div>\n'
        f'<div class="answer mass-value">{spec.mass} MeV</div>'
    )
    return render_card_shell(content, "back", "mass")

def render_composition_front(display_name: str) -> str:
    content = (
        f'<div class="title">{display_name}</div>\n'
        f'<div class="prompt">What is its quark composition?</div>'
    )
    return render_card_shell(content, "front", "composition")

def render_composition_back(spec: ParticleSpec, svg_filename: str) -> str:
    quarks_display = " ".join(format_quark_display(q) for q in spec.quarks)
    content = (
        f'<div class="media-wrap">\n<img src="{svg_filename}" alt="Composition diagram" />\n</div>\n'
        f'<div class="answer quark-text">{quarks_display}</div>\n'
        f'<div class="meta">{spec.id}</div>'
    )
    return render_card_shell(content, "back", "composition")

def render_identity_front(spec: ParticleSpec) -> str:
    quarks_display = " ".join(format_quark_display(q) for q in spec.quarks)
    content = (
        f'<div class="prompt quark-text">{quarks_display}</div>\n'
        f'<div class="prompt">Which particle is this?</div>'
    )
    return render_card_shell(content, "front", "identity")

def render_identity_back(spec: ParticleSpec, display_name: str) -> str:
    content = (
        f'<div class="title">{spec.name}</div>\n'
        f'<div class="badge {spec.type}">{spec.type}</div>\n'
        f'<div class="answer">{display_name}</div>'
    )
    return render_card_shell(content, "back", "identity")
