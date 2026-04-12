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

def _render_title_row(display_name: str, spec: ParticleSpec) -> str:
    name_str = f'<span class="title-name">{display_name}</span>'
    if spec and spec.symbol_tex:
        tex_str = f'<span class="title-tex">\\( {spec.symbol_tex} \\)</span>'
        return f'<div class="title-row">\n  {name_str}\n  {tex_str}\n</div>'
    return f'<div class="title-row">\n  {name_str}\n</div>'

def render_mass_front(display_name: str, spec: ParticleSpec) -> str:
    content = (
        f'<div class="prompt">What is the mass of...</div>\n'
        f'{_render_title_row(display_name, spec)}'
    )
    return render_card_shell(content, "front", "mass")

def render_mass_back(spec: ParticleSpec, display_name: str) -> str:
    content = (
        f'{_render_title_row(display_name, spec)}\n'
        f'<div class="badge {spec.type}">{spec.type}</div>\n'
        f'<div class="answer mass-value">{spec.mass} MeV</div>'
    )
    return render_card_shell(content, "back", "mass")

def render_composition_front(display_name: str, spec: ParticleSpec) -> str:
    content = (
        f'<div class="prompt">What is the quark composition of...</div>\n'
        f'{_render_title_row(display_name, spec)}'
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
        f'<div class="prompt">Identify this particle:</div>\n'
        f'<div class="quark-text large-quarks">{quarks_display}</div>'
    )
    return render_card_shell(content, "front", "identity")

def render_identity_back(spec: ParticleSpec, display_name: str) -> str:
    content = (
        f'{_render_title_row(display_name, spec)}\n'
        f'<div class="badge {spec.type}">{spec.type}</div>\n'
        f'<div class="answer">{display_name}</div>'
    )
    return render_card_shell(content, "back", "identity")

def render_decay_front(display_name: str, spec: ParticleSpec) -> str:
    content = (
        f'<div class="prompt">What are the primary decay modes of...</div>\n'
        f'{_render_title_row(display_name, spec)}'
    )
    return render_card_shell(content, "front", "decay")

def render_decay_back(spec: ParticleSpec, display_name: str, decay_svg_filename: str) -> str:
    decay_label_str = f'<div class="meta">{spec.decay_label}</div>' if spec.decay_label else ""
    content = (
        f'{_render_title_row(display_name, spec)}\n'
        f'<div class="media-wrap" style="max-height: 250px;">\n<img src="{decay_svg_filename}" alt="Feynman Decay Diagram" />\n</div>\n'
        f'{decay_label_str}'
    )
    return render_card_shell(content, "back", "decay")
