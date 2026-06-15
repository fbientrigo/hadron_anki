"""
Modular, per-concept card section renderers.

Each function renders one self-contained HTML fragment for a single concept
(octet, mass, composition, decay, Feynman diagram). The big "summary" card
composes them today, and each can become its own focused card later without
changing this module. Fragments rely on the shared CSS in
``hadron_anki.cards.styles``.
"""
from typing import Optional

from hadron_anki.domain.composer import format_quark_display
from hadron_anki.domain.particle_symbols import display_symbol
from hadron_anki.domain.spec import ParticleSpec


def _section(label: str, body: str, extra_class: str = "") -> str:
    cls = f"section {extra_class}".strip()
    return (
        f'<div class="{cls}">\n'
        f'  <div class="section-label">{label}</div>\n'
        f'  {body}\n'
        f'</div>'
    )


def format_decay(decay: Optional[dict]) -> str:
    """Format a decay as 'NN% -> a + b'. Empty string if there is nothing to show."""
    if not decay:
        return ""
    products = " + ".join(display_symbol(c) for c in decay.get("children") or [])
    branching_ratio = decay.get("branching_ratio")
    if isinstance(branching_ratio, (int, float)):
        percent = f"{round(branching_ratio * 100)}%"
        return f"{percent} → {products}" if products else percent
    return f"→ {products}" if products else ""


def render_octet_section(spec: ParticleSpec) -> str:
    if not spec.multiplet:
        return ""
    label = spec.multiplet.replace("_", " ")
    return _section("Multiplet", f'<span class="badge octet">{label}</span>', "octet-section")


def render_mass_section(spec: ParticleSpec) -> str:
    text = spec.mass_summary or (f"{spec.mass} MeV" if spec.mass is not None else "")
    if not text:
        return ""
    return _section("Mass", f'<div class="mass-summary">{text}</div>', "mass-section")


def render_composition_section(spec: ParticleSpec, svg_filename: Optional[str] = None) -> str:
    summary = spec.display_quark_summary or " ".join(
        format_quark_display(q) for q in spec.quarks
    )
    image = ""
    if svg_filename:
        image = (
            f'<div class="media-wrap">\n'
            f'<img src="{svg_filename}" alt="Composition diagram" />\n'
            f'</div>\n'
        )
    body = f'{image}<div class="quark-text">{summary}</div>'
    return _section("Composition", body, "composition-section")


def render_decay_section(spec: ParticleSpec) -> str:
    if not spec.decay:
        return ""
    return _section("Main decay", f'<div class="decay-line">{format_decay(spec.decay)}</div>', "decay-section")


def render_feynman_section(spec: ParticleSpec, decay_svg_filename: Optional[str] = None) -> str:
    if not decay_svg_filename:
        return ""
    body = (
        f'<div class="media-wrap">\n'
        f'<img src="{decay_svg_filename}" alt="Feynman decay diagram" />\n'
        f'</div>'
    )
    return _section("Feynman diagram", body, "feynman-section")
