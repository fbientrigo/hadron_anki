"""Tests for the Feynman diagram SVG renderer."""
import pytest
from hadron_anki.render.feynman import render_feynman_svg

# ── Shared fixture ───────────────────────────────────────────────────

PI_PLUS_DECAY = {
    "nodes": [
        {"id": "in",   "x": 50,  "y": 90},
        {"id": "v1",   "x": 160, "y": 90},
        {"id": "out1", "x": 270, "y": 45},
        {"id": "out2", "x": 270, "y": 135},
    ],
    "edges": [
        {"from": "in",  "to": "v1",   "type": "scalar",  "label": "pi+", "label_tex": r"\pi^+"},
        {"from": "v1",  "to": "out1", "type": "fermion", "label": "mu+", "label_tex": r"\mu^+"},
        {"from": "v1",  "to": "out2", "type": "fermion", "label": "nu_mu", "label_tex": r"\nu_\mu"},
    ],
}

BOSON_DIAGRAM = {
    "nodes": [
        {"id": "a", "x": 60,  "y": 90},
        {"id": "b", "x": 260, "y": 90},
    ],
    "edges": [
        {"from": "a", "to": "b", "type": "boson", "label": "W+"},
    ],
}


# ── Tests ─────────────────────────────────────────────────────────────

def test_feynman_svg_returns_svg_string():
    out = render_feynman_svg(PI_PLUS_DECAY)
    assert isinstance(out, str)
    assert out.strip().lower().startswith("<svg")


def test_feynman_svg_contains_nodes():
    out = render_feynman_svg(PI_PLUS_DECAY)
    # 4 nodes → 4 vertex circles + 1 background rect
    assert out.count("<circle") == 4


def test_feynman_svg_contains_edges():
    out = render_feynman_svg(PI_PLUS_DECAY)
    # 1 scalar (dashed line) + 2 fermion lines
    assert "<line" in out       # scalar + fermions
    assert "stroke-dasharray" in out   # scalar present


def test_feynman_svg_has_arrowhead_path():
    out = render_feynman_svg(PI_PLUS_DECAY)
    # Arrowheads are flat <path> triangles, not <marker>-referenced
    assert "<marker" not in out
    assert "marker-end" not in out
    assert "<path" in out


def test_feynman_svg_contains_labels():
    out = render_feynman_svg(PI_PLUS_DECAY)
    assert "pi+" in out
    assert "mu+" in out
    assert "nu_mu" in out


def test_feynman_svg_boson_uses_path():
    out = render_feynman_svg(BOSON_DIAGRAM)
    assert "<path" in out          # wavy boson path
    assert "W+" in out


def test_feynman_svg_deterministic():
    out1 = render_feynman_svg(PI_PLUS_DECAY)
    out2 = render_feynman_svg(PI_PLUS_DECAY)
    assert out1 == out2


def test_feynman_svg_empty_diagram():
    """Gracefully handle an empty diagram."""
    out = render_feynman_svg({"nodes": [], "edges": []})
    assert "<svg" in out
    assert "<circle" not in out


def test_feynman_renderer_uses_math_label_assets_when_available(tmp_path):
    """When a math_cache_dir is provided, math labels render as flat <g transform> groups."""
    out = tmp_path / "math_labels"
    svg = render_feynman_svg(PI_PLUS_DECAY, math_cache_dir=out)

    # Single flat outer SVG, no nested <svg> viewports
    assert svg.count("<svg") == 1
    assert svg.count('<g transform="translate') == 3

    # Make sure text fallback is no longer used for these explicitly tex'd nodes
    assert ">pi+<" not in svg

    # Also the assets should have been written explicitly!
    generated = list(out.glob("mathlabel_*.svg"))
    assert len(generated) == 3


def test_identical_math_labels_are_reused(tmp_path):
    out = tmp_path / "math_labels"
    # Create a diagram with two identical labels
    dag = {
        "nodes": [
            {"id": "a", "x": 0, "y": 0},
            {"id": "b", "x": 50, "y": 0},
            {"id": "c", "x": 100, "y": 0},
        ],
        "edges": [
            {"from": "a", "to": "b", "label_tex": r"\pi^+"},
            {"from": "b", "to": "c", "label_tex": r"\pi^+"},
        ]
    }
    svg = render_feynman_svg(dag, math_cache_dir=out)

    # Single flat outer SVG + 2 flattened <g transform> label groups
    assert svg.count("<svg") == 1
    assert svg.count('<g transform="translate') == 2

    # We should only have 1 file generated since it's cached!
    generated = list(out.glob("mathlabel_*.svg"))
    assert len(generated) == 1


def test_feynman_svg_remains_deterministic_with_math_assets(tmp_path):
    out1 = tmp_path / "run1"
    out2 = tmp_path / "run2"
    svg1 = render_feynman_svg(PI_PLUS_DECAY, math_cache_dir=out1)
    svg2 = render_feynman_svg(PI_PLUS_DECAY, math_cache_dir=out2)
    assert svg1 == svg2


def test_feynman_renderer_falls_back_safely_when_no_cache_dir():
    """If no math cache, it uses standard text label, ignoring label_tex."""
    svg = render_feynman_svg(PI_PLUS_DECAY)
    assert svg.count("<svg") == 1  # No nested SVGs
    assert "<text" in svg
    assert ">pi+<" in svg
