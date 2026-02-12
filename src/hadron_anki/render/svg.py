from typing import Any
from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.render.config import load_style_config, node_svg_attrs, DEFAULT_STYLE

def _escape_text(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _attr(attrs: dict[str, object]) -> str:
    return " ".join(f'{k}="{v}"' for k, v in sorted(attrs.items()))


def _render_meson(quarks: list[str], style: dict[str, Any]) -> str:
    p1 = (100, 60)
    p2 = (300, 60)

    d = "M 100 60 Q 150 40, 200 60 T 300 60"
    path = f'<path {_attr({"d": d, "fill": "none", **style.get("connector", DEFAULT_STYLE["connector"])})}/>'

    nodes: list[str] = []
    for i, q in enumerate(quarks):
        cx, cy = p1 if i == 0 else p2
        node_style = node_svg_attrs(q, style)
        nodes.append(f'<circle {_attr({"cx": cx, "cy": cy, "r": 20, **node_style})}/>')
        nodes.append(
            f'<text {_attr({**style.get("label", DEFAULT_STYLE["label"]), "x": cx, "y": cy + 5})}>{_escape_text(q)}</text>'
        )

    return path + "".join(nodes)


def _render_baryon(quarks: list[str], style: dict[str, Any]) -> str:
    pts = [(200, 30), (130, 90), (270, 90)]

    lines: list[str] = []
    for i in range(3):
        p1 = pts[i]
        p2 = pts[(i + 1) % 3]
        lines.append(
            f'<line {_attr({**style.get("connector", DEFAULT_STYLE["connector"]), "x1": p1[0], "x2": p2[0], "y1": p1[1], "y2": p2[1]})}/>'
        )

    nodes: list[str] = []
    for i, q in enumerate(quarks):
        cx, cy = pts[i]
        node_style = node_svg_attrs(q, style)
        nodes.append(f'<circle {_attr({"cx": cx, "cy": cy, "r": 20, **node_style})}/>')
        nodes.append(
            f'<text {_attr({**style.get("label", DEFAULT_STYLE["label"]), "x": cx, "y": cy + 5})}>{_escape_text(q)}</text>'
        )

    return "".join(lines) + "".join(nodes)


def render_svg(spec: ParticleSpec, style: dict[str, Any] | None = None) -> str:
    """Renders a ParticleSpec to an SVG string."""
    if style is None:
        style = load_style_config()

    if spec.type == "meson" and len(spec.quarks) == 2:
        body = _render_meson(spec.quarks, style)
    elif spec.type == "baryon" and len(spec.quarks) == 3:
        body = _render_baryon(spec.quarks, style)
    else:
        title = f"{spec.name} ({spec.id})"
        quarks = " ".join(spec.quarks)
        body = (
            f'<rect {_attr({"fill": "white", "height": 120, "stroke": "black", "width": 400, "x": 0, "y": 0})}/>'
            f'<text {_attr({"font-family": "monospace", "font-size": "16", "x": 12, "y": 28})}>{_escape_text(title)}</text>'
            f'<text {_attr({"font-family": "monospace", "font-size": "14", "x": 12, "y": 60})}>{_escape_text(quarks)}</text>'
        )

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="120" viewBox="0 0 400 120">'
        f"{body}"
        "</svg>"
    )
