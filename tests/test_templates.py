import pytest
from hadron_anki.cards.templates import front_html, back_html
from hadron_anki.domain.spec import ParticleSpec

def test_front_html_returns_exact_img_tag():
    filename = "proton.svg"
    expected = f'<img src="{filename}">'
    assert front_html(filename) == expected

def test_back_html_contains_required_fields():
    spec = ParticleSpec(
        id="p",
        name="Proton",
        type="baryon",
        quarks=["u", "u", "d"]
    )
    html = back_html(spec)
    
    assert "Proton" in html
    assert "p" in html
    assert "u, u, d" in html
