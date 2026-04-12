"""
Scaffold for a future latex + dvisvgm backend.

This module is NOT functional yet. It documents the interface and
the intended upgrade path for when we need pixel-perfect LaTeX rendering.

HOW TO ACTIVATE:
1. Install a TeX distribution (e.g. MiKTeX on Windows, TeX Live on Linux).
2. Verify: `latex --version` and `dvisvgm --version`.
3. Implement `render_svg()` below.
4. In math_labels.py, set DEFAULT_BACKEND = "latex_dvisvgm".

INTERFACE CONTRACT (must match internal_backend.py):
  render_svg(expr_tex: str) -> str
    - Returns a UTF-8 SVG string
    - Must be deterministic for identical inputs
    - Must not produce side effects beyond the returned string
"""

import shutil


def is_available() -> bool:
    """Returns True only if both latex and dvisvgm binaries are found on PATH."""
    return shutil.which("latex") is not None and shutil.which("dvisvgm") is not None


def render_svg(expr_tex: str) -> str:
    """
    [SCAFFOLD] Render expr_tex via latex + dvisvgm pipeline.

    Not yet implemented. Will raise NotImplementedError if called.
    """
    if not is_available():
        raise EnvironmentError(
            "latex or dvisvgm not found on PATH. "
            "Install a TeX distribution to use this backend."
        )
    raise NotImplementedError(
        "latex_dvisvgm_backend is scaffolded but not yet implemented. "
        "Use backend='internal' (default) until this is ready."
    )
