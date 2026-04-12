r"""
Internal SVG text backend for math labels.

This backend renders TeX expressions as plain SVG <text> fragments using
a deterministic Unicode mapping for common physics symbols. It does NOT
require any external dependencies.

Design intent:
 - This is the DEFAULT backend. It covers the ~30 symbols needed for hadron physics.
 - It is NOT a general TeX renderer.
 - It is 100% deterministic and dependency-free.
 - A future `mathtext_backend.py` (matplotlib) or `latex_dvisvgm_backend.py`
   can replace it transparently by conforming to the same interface.

Supported expression shape (simplified TeX subset):
  \pi^+   → π⁺
  \mu^+   → μ⁺
  \nu_\mu → νμ
  \bar{\nu}_e → ν̄ₑ
  \Sigma^- → Σ⁻
  etc.

The rendering is always a compact SVG strip (single text element).
"""

# ── SYMBOL TABLES ──────────────────────────────────────────────────

_GREEK = {
    r"\pi":    "π",
    r"\mu":    "μ",
    r"\nu":    "ν",
    r"\tau":   "τ",
    r"\eta":   "η",
    r"\rho":   "ρ",
    r"\omega": "ω",
    r"\phi":   "φ",
    r"\Lambda": "Λ",
    r"\Sigma":  "Σ",
    r"\Xi":     "Ξ",
    r"\Omega":  "Ω",
    r"\Delta":  "Δ",
    r"\Gamma":  "Γ",
    r"\alpha":  "α",
    r"\beta":   "β",
    r"\gamma":  "γ",
    r"\delta":  "δ",
    r"\epsilon":"ε",
}

_SUPER = {
    "+": "⁺", "-": "⁻", "0": "⁰",
    "1": "¹", "2": "²", "3": "³",
}

_SUB = {
    "0": "₀", "1": "₁", "2": "₂", "3": "₃",
    "e": "ₑ", "u": "ᵤ",  # best unicode coverage
}


# ── PARSER ────────────────────────────────────────────────────────

def _tex_to_unicode(expr: str) -> str:
    r"""
    Best-effort conversion of a physics TeX expression to Unicode text.
    Handles: Greek letters, superscripts (^), subscripts (_), \bar{...}.
    """
    s = expr.strip()

    # Handle \bar{X} → X̄
    import re
    def _bar_replace(m):
        inner = _tex_to_unicode(m.group(1))
        return inner + "\u0304"  # combining overline
    s = re.sub(r"\\bar\{([^}]+)\}", _bar_replace, s)

    # Handle \\anti → bar (our internal notation)
    s = s.replace(r"\anti", r"\bar")

    # Replace Greek tokens (longest match first)
    for token, char in sorted(_GREEK.items(), key=lambda x: -len(x[0])):
        s = s.replace(token, char)

    # Handle groups: {X} → X  (strip braces)
    s = re.sub(r"\{([^}]*)\}", r"\1", s)

    # Handle superscripts: ^X or ^{X}
    def _sup(m):
        chars = m.group(1)
        return "".join(_SUPER.get(c, c) for c in chars)
    s = re.sub(r"\^(.)", _sup, s)

    # Handle subscripts: _X
    def _sub(m):
        chars = m.group(1)
        return "".join(_SUB.get(c, c) for c in chars)
    s = re.sub(r"_(.)", _sub, s)

    # Clean any remaining backslashes (e.g. \mu already replaced → nothing)
    s = re.sub(r"\\[a-zA-Z]+", "", s)

    return s


# ── SVG RENDERER ──────────────────────────────────────────────────

_W = 120
_H = 40
_FONT = "Georgia, 'Times New Roman', serif"
_INK  = "#2d2a26"


def render_svg(expr_tex: str) -> str:
    """
    Render a TeX expression to a compact SVG string using Unicode substitution.

    Args:
        expr_tex: TeX string, e.g. r"\\pi^+"

    Returns:
        UTF-8 SVG string (no XML declaration).
    """
    display = _tex_to_unicode(expr_tex)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{_W}" height="{_H}" viewBox="0 0 {_W} {_H}">'
        f'<text x="{_W // 2}" y="{_H // 2 + 6}" '
        f'font-family="{_FONT}" font-size="22" '
        f'fill="{_INK}" text-anchor="middle" '
        f'dominant-baseline="middle"'
        f'>{display}</text>'
        f'</svg>'
    )
    return svg
