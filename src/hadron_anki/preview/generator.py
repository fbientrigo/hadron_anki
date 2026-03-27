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
from typing import Optional


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
.gallery {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    justify-content: center;
    max-width: 960px;
    margin: 0 auto;
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


def generate_preview(specs: list[ParticleSpec], output_dir: str | Path, card_types: Optional[list[str]] = None) -> None:
    """Generates SVG files and a styled preview gallery."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    sorted_specs = sorted(specs, key=lambda s: s.id)

    # Write SVG files
    for spec in sorted_specs:
        svg_content = render_svg(spec)
        svg_filename = f"{spec.id}.svg"
        (output_path / svg_filename).write_text(svg_content, encoding="utf-8")

    # Build card pairs HTML
    card_pairs: list[str] = []
    for spec in sorted_specs:
        svg_filename = f"{spec.id}.svg"
        
        # We also need an SVG available locally for preview rendering
        cards = generate_cards(spec, svg_filename, include_types=card_types)
        for card in cards:
            front = card.front_html
            back = card.back_html
            # Add a small text telling what type of card it is
            card_pairs.append(
                '<div class="card-pair">'
                f'<div class="side-label">Front: {card.card_type}</div>'
                f'<div class="card-frame">{front}</div>'
                f'<div class="side-label">Back: {card.card_type}</div>'
                f'<div class="card-frame">{back}</div>'
                '</div>'
            )

    index_content = (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<title>Hadron Anki Preview</title>\n"
        f"<style>\n{CARD_CSS}\n{_PREVIEW_CSS}\n</style>\n"
        "</head>\n"
        "<body>\n"
        "<h1>Hadron Anki — Card Preview</h1>\n"
        '<div class="gallery">\n'
        + "\n".join(card_pairs) +
        "\n</div>\n"
        "</body>\n"
        "</html>"
    )
    (output_path / "index.html").write_text(index_content, encoding="utf-8")
