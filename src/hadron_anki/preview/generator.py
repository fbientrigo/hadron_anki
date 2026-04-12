"""
Preview generator for styled hadron Anki cards.

Generates SVG files + a styled index.html showing front/back
card pairs in a gallery layout for visual verification.
"""
from pathlib import Path
from hadron_anki.cards.styles import CARD_CSS
from hadron_anki.cards.mapping import generate_cards
from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.render.svg import render_svg
from hadron_anki.render.feynman import render_feynman_svg
from typing import Any, Optional


_PREVIEW_CSS = """\
/* ── Preview gallery layout ── */
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: "Inter", "Segoe UI", system-ui, sans-serif;
    background: #f0ece7;
    padding: 32px 16px;
    min-height: 100vh;
}
h1 {
    text-align: center;
    font-size: 20px;
    font-weight: 600;
    color: #2d2a26;
    margin-bottom: 28px;
    letter-spacing: -0.01em;
}
h2 {
    text-align: center;
    font-size: 18px;
    font-weight: 600;
    color: #4a4642;
    margin: 40px 0 20px 0;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.gallery {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    justify-content: center;
    max-width: 960px;
    margin: 0 auto 40px auto;
}
.card-pair {
    display: flex;
    gap: 12px;
    flex-direction: column;
}
.card-pair .side-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #9a9590;
    text-align: center;
    font-weight: 600;
}
.card-frame {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(45,42,38,0.08);
    background: #faf8f5;
    width: 320px;
}
"""


def generate_preview(
    specs: list[ParticleSpec], 
    output_dir: str | Path, 
    card_types: Optional[list[str]] = None,
    feynman_html: Optional[list[str]] = None
) -> None:
    """Generates SVG files and a styled preview gallery grouped by semantic card subsets."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    sorted_specs = sorted(specs, key=lambda s: s.id)
    sections = ["mass", "composition", "identity"]

    # Write SVG files into semantic subdirectories
    for section in sections:
        if card_types is not None and section not in card_types:
            continue
        section_dir = output_path / section
        section_dir.mkdir(exist_ok=True)
        for spec in sorted_specs:
            svg_content = render_svg(spec)
            (section_dir / f"{spec.id}.svg").write_text(svg_content, encoding="utf-8")

    # Build card pairs HTML grouped by section
    grouped_html: list[str] = []
    
    for section in sections:
        if card_types is not None and section not in card_types:
            continue
            
        grouped_html.append(f"<h2>{section.capitalize()} Cards</h2>")
        grouped_html.append('<div class="gallery">')
        
        for spec in sorted_specs:
            cards = generate_cards(spec, f"{section}/{spec.id}.svg", include_types=[section])
            for card in cards:
                front = card.front_html
                back = card.back_html
                grouped_html.append(
                    '<div class="card-pair">'
                    f'<div class="side-label">Front: {card.card_type}</div>'
                    f'<div class="card-frame">{front}</div>'
                    f'<div class="side-label">Back: {card.card_type}</div>'
                    f'<div class="card-frame">{back}</div>'
                    '</div>'
                )
        grouped_html.append("</div>")

    if feynman_html:
        grouped_html.extend(feynman_html)

    index_content = (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<title>Hadron Anki Preview</title>\n"
        "<script src=\"https://polyfill.io/v3/polyfill.min.js?features=es6\"></script>\n"
        "<script id=\"MathJax-script\" async src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js\"></script>\n"
        f"<style>\n{CARD_CSS}\n{_PREVIEW_CSS}\n</style>\n"
        "</head>\n"
        "<body>\n"
        "<h1>Hadron Anki — Card Preview</h1>\n"
        + "\n".join(grouped_html) +
        "\n</body>\n"
        "</html>"
    )
    (output_path / "index.html").write_text(index_content, encoding="utf-8")


def generate_feynman_preview(
    feynman_specs: list[dict[str, Any]],
    output_dir: str | Path,
) -> list[str]:
    """
    Renders Feynman diagram SVGs into output_dir/feynman/{id}.svg.
    Also returns grouped HTML snippet for index.html integration.

    Each entry in feynman_specs must have:
        id: str
        label: str          (human-readable particle / process name)
        decay_diagram: dict  (nodes + edges schema)
    """
    output_path = Path(output_dir)
    feynman_dir = output_path / "feynman"
    feynman_dir.mkdir(parents=True, exist_ok=True)

    feynman_sorted = sorted(feynman_specs, key=lambda s: s["id"])

    section_html: list[str] = []
    section_html.append("<h2>Feynman Diagrams</h2>")
    section_html.append('<div class="gallery">')

    for spec in feynman_sorted:
        diagram_spec = spec.get("decay_diagram", {})
        svg_content = render_feynman_svg(diagram_spec, math_cache_dir=feynman_dir)
        fname = f"{spec['id']}.svg"
        (feynman_dir / fname).write_text(svg_content, encoding="utf-8")

        label = spec.get("label", spec["id"])
        section_html.append(
            f'<div class="card-pair">'
            f'<div class="side-label">{label}</div>'
            f'<div class="card-frame"><img src="feynman/{fname}" '
            f'style="width:100%;height:auto;"/></div>'
            f'</div>'
        )

    section_html.append("</div>")
    return section_html

