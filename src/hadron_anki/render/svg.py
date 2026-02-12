from hadron_anki.domain.spec import ParticleSpec

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


def _quark_style(token: str) -> dict[str, str]:
    style = {"fill": "white", "stroke": "black", "stroke-width": "2"}
    if token.startswith("anti-"):
        style["stroke-dasharray"] = "4"
    return style


def _render_meson(quarks: list[str]) -> str:
    p1 = (100, 60)
    p2 = (300, 60)

    d = "M 100 60 Q 150 40, 200 60 T 300 60"
    path = f'<path {_attr({"d": d, "fill": "none", "stroke": "gray", "stroke-width": "2"})}/>'

    nodes: list[str] = []
    for i, q in enumerate(quarks):
        cx, cy = p1 if i == 0 else p2
        style = _quark_style(q)
        nodes.append(f'<circle {_attr({"cx": cx, "cy": cy, "r": 20, **style})}/>')
        nodes.append(
            f'<text {_attr({"font-family": "monospace", "font-size": "14", "text-anchor": "middle", "x": cx, "y": cy + 5})}>{_escape_text(q)}</text>'
        )

    return path + "".join(nodes)


def _render_baryon(quarks: list[str]) -> str:
    pts = [(200, 30), (130, 90), (270, 90)]

    lines: list[str] = []
    for i in range(3):
        p1 = pts[i]
        p2 = pts[(i + 1) % 3]
        lines.append(
            f'<line {_attr({"stroke": "gray", "stroke-width": "2", "x1": p1[0], "x2": p2[0], "y1": p1[1], "y2": p2[1]})}/>'
        )

    nodes: list[str] = []
    for i, q in enumerate(quarks):
        cx, cy = pts[i]
        style = _quark_style(q)
        nodes.append(f'<circle {_attr({"cx": cx, "cy": cy, "r": 20, **style})}/>')
        nodes.append(
            f'<text {_attr({"font-family": "monospace", "font-size": "14", "text-anchor": "middle", "x": cx, "y": cy + 5})}>{_escape_text(q)}</text>'
        )

    return "".join(lines) + "".join(nodes)


def render_svg(spec: ParticleSpec) -> str:
    """Renders a ParticleSpec to an SVG string."""
    if spec.type == "meson" and len(spec.quarks) == 2:
        body = _render_meson(spec.quarks)
    elif spec.type == "baryon" and len(spec.quarks) == 3:
        body = _render_baryon(spec.quarks)
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
