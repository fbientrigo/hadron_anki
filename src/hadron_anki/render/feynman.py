"""
Feynman diagram SVG renderer for hadron_anki.

Generates deterministic, pedagogical Feynman diagrams from a
declarative diagram_spec dictionary (loaded from YAML catalog or inline).

Supported edge types:
  - fermion : straight line with arrowhead
  - boson   : sinusoidal wavy path
  - scalar  : dashed straight line

Schema:
  diagram_spec = {
      "nodes": [{"id": str, "x": int, "y": int}, ...],
      "edges": [{"from": str, "to": str, "type": str, "label": str?}, ...]
  }
"""

import math
import re
from pathlib import Path
from typing import Any, Optional

from hadron_anki.render.math_labels import generate_math_label_asset


# ── SVG canvas constants ─────────────────────────────────────────────
_W = 320
_H = 180
_FONT = "Georgia, 'Times New Roman', serif"

# ── Colour palette (warm paper-and-ink) ─────────────────────────────
_COL_INK   = "#2d2a26"
_COL_FERM  = "#2d2a26"
_COL_BOSON = "#6b4f2a"
_COL_SCAL  = "#4a6b6b"
_COL_VERT  = "#ffffff"
_COL_VBRD  = "#2d2a26"


# ── Helpers ─────────────────────────────────────────────────────────

def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


def _arrow_marker(marker_id: str, color: str) -> str:
    """Returns an SVG <defs> arrowhead marker definition."""
    return (
        f'<marker id="{marker_id}" markerWidth="8" markerHeight="8" '
        f'refX="6" refY="3" orient="auto">'
        f'<path d="M0,0 L0,6 L8,3 z" fill="{color}"/>'
        f'</marker>'
    )


def _label_offset(x1: float, y1: float, x2: float, y2: float) -> tuple[float, float]:
    """Returns a perpendicular offset point for a mid-line label."""
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    # Perpendicular unit vector
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy) or 1.0
    # Normal direction, 14px offset
    nx, ny = -dy / length * 14, dx / length * 14
    return mx + nx, my + ny


# ── Line primitives ─────────────────────────────────────────────────

def _fermion_line(x1: float, y1: float, x2: float, y2: float, marker_id: str) -> str:
    # Shorten end so arrow doesn't overlap vertex circle
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy) or 1.0
    ux, uy = dx / length, dy / length
    ex, ey = x2 - ux * 10, y2 - uy * 10
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
        f'stroke="{_COL_FERM}" stroke-width="1.5" '
        f'marker-end="url(#{marker_id})"/>'
    )


def _boson_path(x1: float, y1: float, x2: float, y2: float) -> str:
    """Sinusoidal wavy path approximated with cubic Bezier curves."""
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy) or 1.0
    ux, uy = dx / length, dy / length
    # Perpendicular
    px, py = -uy, ux

    n_waves = max(2, int(length / 16))
    step = length / n_waves
    amp = 8.0

    pts = [f"M {x1:.1f} {y1:.1f}"]
    for i in range(n_waves):
        t0 = i / n_waves
        t1 = (i + 0.5) / n_waves
        t2 = (i + 1) / n_waves

        sx = x1 + ux * (t0 * length)
        sy = y1 + uy * (t0 * length)
        cx1x = x1 + ux * (t0 * length + step * 0.25) + px * amp * (1 if i % 2 == 0 else -1)
        cx1y = y1 + uy * (t0 * length + step * 0.25) + py * amp * (1 if i % 2 == 0 else -1)
        cx2x = x1 + ux * (t1 * length) + px * amp * (1 if i % 2 == 0 else -1)
        cx2y = y1 + uy * (t1 * length) + py * amp * (1 if i % 2 == 0 else -1)
        ex = x1 + ux * ((i + 1) / n_waves * length)
        ey = y1 + uy * ((i + 1) / n_waves * length)

        pts.append(f"C {cx1x:.1f},{cx1y:.1f} {cx2x:.1f},{cx2y:.1f} {ex:.1f},{ey:.1f}")

    return (
        f'<path d="{" ".join(pts)}" '
        f'fill="none" stroke="{_COL_BOSON}" stroke-width="1.5"/>'
    )


def _scalar_line(x1: float, y1: float, x2: float, y2: float) -> str:
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{_COL_SCAL}" stroke-width="1.5" stroke-dasharray="5,4"/>'
    )


# ── Public renderer ──────────────────────────────────────────────────

def render_feynman_svg(diagram_spec: dict[str, Any], math_cache_dir: Optional[str | Path] = None) -> str:
    """
    Render a Feynman diagram to an SVG string.

    Args:
        diagram_spec: dict with 'nodes' and 'edges' keys.
        math_cache_dir: (Optional) If provided, edges with 'label_tex' will be
                        rendered as formal SVG assets in this directory and referenced.

    Returns:
        UTF-8 SVG string.
    """
    nodes_raw: list[dict] = diagram_spec.get("nodes", [])
    edges_raw: list[dict] = diagram_spec.get("edges", [])

    # Build node lookup
    nodes: dict[str, tuple[float, float]] = {
        n["id"]: (float(n["x"]), float(n["y"]))
        for n in sorted(nodes_raw, key=lambda n: n["id"])
    }

    # Collect SVG parts
    defs: list[str] = []
    edges_svg: list[str] = []
    vertices_svg: list[str] = []
    labels_svg: list[str] = []

    # Arrow marker (shared for all fermion edges)
    marker_id = "arrow"
    defs.append(_arrow_marker(marker_id, _COL_FERM))

    # Edges — sorted for determinism
    for edge in sorted(edges_raw, key=lambda e: (e["from"], e["to"])):
        src_id = edge["from"]
        dst_id = edge["to"]
        etype = edge.get("type", "fermion")
        label = edge.get("label", "")
        label_tex = edge.get("label_tex", "")

        x1, y1 = nodes[src_id]
        x2, y2 = nodes[dst_id]

        if etype == "fermion":
            edges_svg.append(_fermion_line(x1, y1, x2, y2, marker_id))
        elif etype == "boson":
            edges_svg.append(_boson_path(x1, y1, x2, y2))
        else:  # scalar / default
            edges_svg.append(_scalar_line(x1, y1, x2, y2))

        lx, ly = _label_offset(x1, y1, x2, y2)
        if label_tex and math_cache_dir:
            # Render and cache the formal math label asset (preserves Anki asset reuse)
            asset_path = generate_math_label_asset(label_tex, cache_dir=math_cache_dir)
            
            asset_svg = asset_path.read_text(encoding="utf-8")
            
            import re
            vb_match = re.search(r'viewBox="([^"]+)"', asset_svg)
            vb = vb_match.group(1) if vb_match else "0 0 120 40"
            
            svg_start = asset_svg.find("<svg")
            content_start = asset_svg.find(">", svg_start) + 1
            content_end = asset_svg.rfind("</svg>")
            inner_content = asset_svg[content_start:content_end] if (content_start > 0 and content_end > 0) else ""

            # Math labels scale neatly into a centered bounding box
            w, h = 48, 24
            labels_svg.append(
                f'<svg x="{lx - w/2:.1f}" y="{ly - h/2:.1f}" width="{w}" height="{h}" viewBox="{vb}">'
                f'{inner_content}'
                f'</svg>'
            )
        elif label:
            labels_svg.append(
                f'<text x="{lx:.1f}" y="{ly:.1f}" '
                f'font-family="{_FONT}" font-size="12" '
                f'fill="{_COL_INK}" text-anchor="middle" '
                f'dominant-baseline="middle">{_esc(label)}</text>'
            )

    # Vertices — sorted for determinism
    for node_id in sorted(nodes):
        x, y = nodes[node_id]
        vertices_svg.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" '
            f'fill="{_COL_VERT}" stroke="{_COL_VBRD}" stroke-width="1.5"/>'
        )

    defs_block = f'<defs>{"".join(defs)}</defs>' if defs else ""

    body = (
        defs_block
        + "".join(edges_svg)
        + "".join(vertices_svg)
        + "".join(labels_svg)
    )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{_W}" height="{_H}" viewBox="0 0 {_W} {_H}">'
        f'<rect width="{_W}" height="{_H}" fill="#faf8f5"/>'
        f'{body}'
        f'</svg>'
    )
