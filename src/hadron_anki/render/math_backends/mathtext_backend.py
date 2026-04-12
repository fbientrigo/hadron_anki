"""
Scaffold for a matplotlib.mathtext backend.

This module activates only when matplotlib is installed.
The internal_backend.py is used by default when matplotlib is absent.

HOW TO ACTIVATE:
1. pip install matplotlib
2. In math_labels.py, set DEFAULT_BACKEND = "mathtext"

INTERFACE CONTRACT (must match internal_backend.py):
  render_svg(expr_tex: str) -> str
"""

def is_available() -> bool:
    try:
        import matplotlib  # noqa: F401
        return True
    except ImportError:
        return False


def render_svg(expr_tex: str) -> str:
    """
    Render a TeX expression to SVG using matplotlib.mathtext.
    Falls back cleanly if matplotlib is not installed.
    """
    if not is_available():
        raise EnvironmentError(
            "matplotlib is not installed. "
            "Run: pip install matplotlib  to enable this backend."
        )
    # Future implementation:
    # from matplotlib import mathtext, figure
    # Use mathtext parser to get a SVG path set, serialize to SVG string.
    raise NotImplementedError(
        "mathtext_backend is scaffolded but not yet implemented. "
        "Install matplotlib and implement the SVG export here."
    )
