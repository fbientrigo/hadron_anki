"""
Math label rendering subsystem for hadron_anki.

Provides:
  - MathLabelSpec: spec dataclass with deterministic cache key + filename
  - render_math_label_svg(): render a TeX expression to SVG (string)
  - generate_math_label_asset(): render + cache to filesystem
  - generate_math_label_preview(): HTML gallery of rendered labels

Backends (selectable via `backend` parameter):
  "internal"        : built-in Unicode substitution (default, zero deps)
  "mathtext"        : matplotlib.mathtext (requires: pip install matplotlib)
  "latex_dvisvgm"   : latex + dvisvgm toolchain (requires TeX distribution)
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ── DEFAULT BACKEND ─────────────────────────────────────────────────
DEFAULT_BACKEND = "internal"


# ── SPEC ────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class MathLabelSpec:
    """
    Describes a single math label to be rendered.

    Attributes:
        expr_tex  : TeX expression, e.g. r"\\pi^+"
        backend   : which rendering backend to use
        font_size : hint passed to backends that support it (ignored by internal)
    """
    expr_tex: str
    backend: str = DEFAULT_BACKEND
    font_size: int = 22

    @property
    def cache_key(self) -> str:
        """Deterministic hex hash of (expr_tex, backend, font_size)."""
        payload = f"{self.expr_tex}|{self.backend}|{self.font_size}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @property
    def filename(self) -> str:
        """Filesystem-safe filename for the cached SVG asset."""
        return f"mathlabel_{self.cache_key[:16]}.svg"


# ── BACKEND DISPATCH ────────────────────────────────────────────────

def _get_backend_render(backend: str):
    """Returns the render_svg callable for the requested backend."""
    if backend == "internal":
        from hadron_anki.render.math_backends import internal_backend
        return internal_backend.render_svg
    if backend == "mathtext":
        from hadron_anki.render.math_backends import mathtext_backend
        return mathtext_backend.render_svg
    if backend == "latex_dvisvgm":
        from hadron_anki.render.math_backends import latex_dvisvgm_backend
        return latex_dvisvgm_backend.render_svg
    raise ValueError(f"Unknown backend '{backend}'. "
                     f"Valid options: 'internal', 'mathtext', 'latex_dvisvgm'")


# ── PUBLIC API ──────────────────────────────────────────────────────

def render_math_label_svg(
    expr_tex: str,
    *,
    backend: str = DEFAULT_BACKEND,
    font_size: int = 22,
) -> str:
    """
    Render a TeX expression to an SVG string.

    Args:
        expr_tex  : e.g. r"\\pi^+"
        backend   : "internal" | "mathtext" | "latex_dvisvgm"
        font_size : hint for supporting backends

    Returns:
        UTF-8 SVG string.
    """
    render = _get_backend_render(backend)
    return render(expr_tex)


def generate_math_label_asset(
    expr_tex: str,
    *,
    cache_dir: str | Path,
    backend: str = DEFAULT_BACKEND,
    font_size: int = 22,
) -> Path:
    """
    Render a TeX expression and cache the resulting SVG to the filesystem.

    If the file already exists (cache hit), the file is NOT overwritten.

    Args:
        expr_tex  : TeX expression string
        cache_dir : directory where SVG assets are stored
        backend   : rendering backend
        font_size : hint for supporting backends

    Returns:
        Path to the cached SVG file.
    """
    spec = MathLabelSpec(expr_tex=expr_tex, backend=backend, font_size=font_size)
    cache_path = Path(cache_dir)
    cache_path.mkdir(parents=True, exist_ok=True)

    asset_path = cache_path / spec.filename
    if not asset_path.exists():
        svg = render_math_label_svg(expr_tex, backend=backend, font_size=font_size)
        asset_path.write_text(svg, encoding="utf-8")

    return asset_path


def generate_math_label_preview(
    expressions: list[str],
    output_dir: str | Path,
    *,
    backend: str = DEFAULT_BACKEND,
) -> None:
    """
    Render a list of TeX expressions and write SVG assets + HTML index.

    Output layout:
        output_dir/
            mathlabel_<hash>.svg   (one per expression)
            index.html

    Args:
        expressions : list of TeX strings
        output_dir  : target directory (created if missing)
        backend     : rendering backend
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    rows: list[str] = []
    for expr in expressions:
        path = generate_math_label_asset(expr, cache_dir=output_path, backend=backend)
        rows.append(
            f'<tr>'
            f'<td><img src="{path.name}" style="height:48px;"/></td>'
            f'<td style="font-family:monospace;padding-left:16px;">'
            f'{_html_esc(expr)}</td>'
            f'<td style="font-family:monospace;color:#888;padding-left:16px;">'
            f'{path.name}</td>'
            f'</tr>'
        )

    html = (
        "<!DOCTYPE html>\n<html>\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<title>Math Label Preview</title>\n"
        "<style>"
        "body{font-family:system-ui,sans-serif;background:#f5f3f0;padding:32px;}"
        "h1{font-size:20px;margin-bottom:24px;}"
        "table{border-collapse:collapse;}"
        "td{padding:8px 4px;border-bottom:1px solid #e0ddd9;vertical-align:middle;}"
        "img{display:block;}"
        "</style>\n</head>\n<body>\n"
        "<h1>Math Label Preview</h1>\n"
        "<table>\n"
        "<tr><th>Rendered</th><th>TeX Source</th><th>Filename</th></tr>\n"
        + "\n".join(rows) +
        "\n</table>\n</body>\n</html>"
    )
    (output_path / "index.html").write_text(html, encoding="utf-8")


def _html_esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
