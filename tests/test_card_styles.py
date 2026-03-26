"""Tests for the card CSS design system."""
from hadron_anki.cards.styles import CARD_CSS


def test_card_css_returns_nonempty_string():
    """CARD_CSS must be a non-empty string."""
    assert isinstance(CARD_CSS, str)
    assert len(CARD_CSS) > 0


def test_card_css_contains_required_selectors():
    """CSS must define selectors for all structural card elements."""
    required = [
        ".card-shell",
        ".title",
        ".badge",
        ".baryon",
        ".meson",
        ".prompt",
        ".answer",
        ".media-wrap",
        ".quark-text",
        ".mass-value",
        ".meta",
    ]
    for selector in required:
        assert selector in CARD_CSS, f"Missing CSS selector: {selector}"


def test_card_css_is_deterministic():
    """Importing CARD_CSS twice must yield the identical string."""
    from hadron_anki.cards.styles import CARD_CSS as second
    assert CARD_CSS == second


def test_card_css_contains_font_family():
    """CSS must declare a custom font stack (not browser default)."""
    assert "font-family" in CARD_CSS
