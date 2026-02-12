from pathlib import Path
from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.render.svg import render_svg

def generate_preview(specs: list[ParticleSpec], output_dir: str | Path) -> None:
    """Generates an SVG preview and an index.html for a list of ParticleSpecs."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    sorted_specs = sorted(specs, key=lambda s: s.id)

    img_tags = []
    for spec in sorted_specs:
        svg_content = render_svg(spec)
        svg_filename = f"{spec.id}.svg"
        (output_path / svg_filename).write_text(svg_content, encoding="utf-8")
        img_tags.append(f'<img src="{svg_filename}">')

    index_content = (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head><title>Hadron Anki Preview</title></head>\n"
        "<body>\n"
        + "\n".join(img_tags) +
        "\n</body>\n"
        "</html>"
    )
    (output_path / "index.html").write_text(index_content, encoding="utf-8")
