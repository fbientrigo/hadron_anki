"""
TDD tests for the math label rendering subsystem.

This module validates:
- deterministic cache key generation
- filesystem-safe hashed filenames
- SVG output correctness
- caching / deduplication behaviour
- preview generation
- pipeline determinism
"""
import hashlib
import re
from pathlib import Path
import pytest

from hadron_anki.render.math_labels import (
    MathLabelSpec,
    render_math_label_svg,
    generate_math_label_asset,
    generate_math_label_preview,
)


# ── fixtures ─────────────────────────────────────────────────────────

SAMPLE_EXPRS = [
    r"\pi^+",
    r"\mu^+",
    r"\nu_\mu",
    r"\bar{\nu}_e",
]


def _spec(expr: str) -> MathLabelSpec:
    return MathLabelSpec(expr_tex=expr)


# ── 1) cache key ─────────────────────────────────────────────────────

def test_math_label_cache_key_is_deterministic():
    s = _spec(r"\pi^+")
    assert s.cache_key == _spec(r"\pi^+").cache_key


def test_math_label_cache_key_differs_for_different_exprs():
    assert _spec(r"\pi^+").cache_key != _spec(r"\mu^+").cache_key


def test_math_label_cache_key_is_hex_string():
    key = _spec(r"\pi^+").cache_key
    assert re.fullmatch(r"[0-9a-f]+", key)


# ── 2) filename ───────────────────────────────────────────────────────

def test_math_label_filename_is_safe_and_hashed():
    s = _spec(r"\pi^+")
    fname = s.filename
    # must be safe for Anki media (no special chars except underscore, dash, dot)
    assert re.fullmatch(r"[A-Za-z0-9_.\\-]+", fname), f"unsafe filename: {fname}"
    assert fname.endswith(".svg")


def test_math_label_filename_contains_hash():
    s = _spec(r"\pi^+")
    assert s.cache_key[:8] in s.filename


def test_math_label_filenames_are_unique_per_expression():
    fnames = {_spec(e).filename for e in SAMPLE_EXPRS}
    assert len(fnames) == len(SAMPLE_EXPRS), "filename collision detected"


# ── 3) SVG output ─────────────────────────────────────────────────────

def test_render_math_label_returns_nonempty_svg():
    svg = render_math_label_svg(r"\pi^+")
    assert svg.strip().lower().startswith("<svg")
    assert len(svg) > 50


def test_render_math_label_svg_is_valid_fragment():
    svg = render_math_label_svg(r"\mu^+")
    assert "</svg>" in svg
    assert "<text" in svg or "<path" in svg  # must have some content


def test_render_math_label_svg_contains_expression_or_encoded():
    """SVG must somehow encode the original expression."""
    svg = render_math_label_svg(r"\pi^+")
    # Either the raw tex or something derived from it is present
    has_content = "pi" in svg.lower() or "text" in svg.lower() or "path" in svg.lower()
    assert has_content


# ── 4) caching ─────────────────────────────────────────────────────

def test_identical_expressions_reuse_cached_asset(tmp_path):
    cache_dir = tmp_path / "cache"
    a_path = generate_math_label_asset(r"\pi^+", cache_dir=cache_dir)
    b_path = generate_math_label_asset(r"\pi^+", cache_dir=cache_dir)
    assert a_path == b_path
    assert a_path.exists()


def test_different_expressions_produce_different_assets(tmp_path):
    cache_dir = tmp_path / "cache"
    a = generate_math_label_asset(r"\pi^+", cache_dir=cache_dir)
    b = generate_math_label_asset(r"\mu^+", cache_dir=cache_dir)
    assert a != b


def test_cached_asset_not_regenerated(tmp_path):
    """Second call must not overwrite the first (no re-render)."""
    cache_dir = tmp_path / "cache"
    path = generate_math_label_asset(r"\pi^+", cache_dir=cache_dir)
    mtime1 = path.stat().st_mtime
    path2 = generate_math_label_asset(r"\pi^+", cache_dir=cache_dir)
    mtime2 = path2.stat().st_mtime
    assert mtime1 == mtime2, "Cache file was overwritten on second call"


# ── 5) preview ────────────────────────────────────────────────────────

def test_math_label_preview_generates_index(tmp_path):
    generate_math_label_preview(SAMPLE_EXPRS, tmp_path)
    assert (tmp_path / "index.html").exists()


def test_math_label_preview_generates_svg_assets(tmp_path):
    generate_math_label_preview(SAMPLE_EXPRS, tmp_path)
    svg_files = list(tmp_path.glob("*.svg"))
    assert len(svg_files) == len(SAMPLE_EXPRS)


def test_math_label_preview_index_references_svgs(tmp_path):
    generate_math_label_preview(SAMPLE_EXPRS, tmp_path)
    content = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert "<img" in content
    assert ".svg" in content
    # Each expression must appear in the index
    for expr in SAMPLE_EXPRS:
        assert expr in content or expr.replace("\\", "") in content


# ── 6) determinism ────────────────────────────────────────────────────

def test_math_label_pipeline_remains_deterministic(tmp_path):
    cache1 = tmp_path / "run1"
    cache2 = tmp_path / "run2"
    for expr in SAMPLE_EXPRS:
        p1 = generate_math_label_asset(expr, cache_dir=cache1)
        p2 = generate_math_label_asset(expr, cache_dir=cache2)
        assert p1.read_text(encoding="utf-8") == p2.read_text(encoding="utf-8"), (
            f"Non-deterministic output for {expr}"
        )
