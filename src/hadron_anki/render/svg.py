from hadron_anki.domain.spec import ParticleSpec

def render_svg(spec: ParticleSpec) -> str:
    """Renders a ParticleSpec to an SVG string."""
    # Minimal, dependency-free SVG that includes quark tokens as visible text.
    quarks = " ".join(spec.quarks)
    title = f"{spec.name} ({spec.id})"
    return (
        "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"400\" height=\"120\" viewBox=\"0 0 400 120\">"
        "<rect x=\"0\" y=\"0\" width=\"400\" height=\"120\" fill=\"white\" stroke=\"black\"/>"
        f"<text x=\"12\" y=\"28\" font-family=\"monospace\" font-size=\"16\">{title}</text>"
        f"<text x=\"12\" y=\"60\" font-family=\"monospace\" font-size=\"14\">{quarks}</text>"
        "</svg>"
    )
