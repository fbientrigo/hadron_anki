"""
Generate a simple, deterministic Feynman diagram spec from a decay.

This is the fallback used when a particle has no hand-authored ``decay_diagram``
in the catalog. It draws a single vertex topology:

    initial --> vertex --> child_1
                       --> child_2
                       ...

Hand-authored diagrams (with intermediate particles like the W boson) override
this whenever present in the catalog. The output matches the schema consumed by
``render.feynman.render_feynman_svg``: ``{"nodes": [...], "edges": [...]}``.
"""
from __future__ import annotations

from typing import Any, Optional

from hadron_anki.domain.particle_symbols import display_symbol
from hadron_anki.domain.spec import ParticleSpec

# Canvas geometry (matches the Feynman renderer's 320x180 canvas).
_X_IN = 50
_X_VERTEX = 160
_X_OUT = 270
_Y_MID = 90
_Y_TOP = 45
_Y_BOTTOM = 135


def build_decay_diagram(spec: ParticleSpec, decay: dict[str, Any]) -> Optional[dict]:
    """Build a basic decay diagram spec, or None if there are no decay products."""
    children = list((decay or {}).get("children") or [])
    if not children:
        return None

    in_type = "scalar" if spec.type == "meson" else "fermion"
    nodes: list[dict] = [
        {"id": "in", "x": _X_IN, "y": _Y_MID},
        {"id": "v", "x": _X_VERTEX, "y": _Y_MID},
    ]
    edges: list[dict] = [
        {"from": "in", "to": "v", "type": in_type, "label": display_symbol(spec.id)},
    ]

    n = len(children)
    if n == 1:
        ys: list[float] = [float(_Y_MID)]
    else:
        ys = [_Y_TOP + (_Y_BOTTOM - _Y_TOP) * i / (n - 1) for i in range(n)]

    for i, (child, y) in enumerate(zip(children, ys)):
        out_id = f"out{i + 1}"
        nodes.append({"id": out_id, "x": _X_OUT, "y": int(round(y))})
        edges.append({"from": "v", "to": out_id, "type": "fermion", "label": display_symbol(child)})

    return {"nodes": nodes, "edges": edges}
