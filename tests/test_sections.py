"""Tests for the modular per-concept card sections."""
from hadron_anki.cards import sections
from hadron_anki.domain.spec import ParticleSpec


def _spec(**kwargs) -> ParticleSpec:
    base = dict(id="lambda_0", name="Lambda Zero", type="baryon", quarks=["u", "d", "s"])
    base.update(kwargs)
    return ParticleSpec(**base)


def test_format_decay_shows_percent_and_products():
    decay = {"branching_ratio": 0.641, "children": ["proton", "pi_minus"]}
    assert sections.format_decay(decay) == "64% → p + π⁻"


def test_format_decay_handles_missing_branching_ratio():
    decay = {"children": ["gamma", "gamma"]}
    assert sections.format_decay(decay) == "→ γ + γ"


def test_format_decay_empty_for_none():
    assert sections.format_decay(None) == ""


def test_octet_section_renders_multiplet_badge():
    html = sections.render_octet_section(_spec(multiplet="baryon_octet"))
    assert 'class="badge octet"' in html
    assert "baryon octet" in html


def test_octet_section_empty_without_multiplet():
    assert sections.render_octet_section(_spec()) == ""


def test_mass_section_prefers_summary():
    html = sections.render_mass_section(_spec(mass_summary="light · ≈500 MeV (493.68 MeV)"))
    assert "493.68 MeV" in html
    assert 'class="mass-summary"' in html


def test_composition_section_uses_summary_and_image():
    html = sections.render_composition_section(
        _spec(display_quark_summary="u d s"), "lambda_0.svg"
    )
    assert "u d s" in html
    assert '<img src="lambda_0.svg"' in html


def test_decay_section_renders_line():
    spec = _spec(decay={"branching_ratio": 0.641, "children": ["proton", "pi_minus"]})
    html = sections.render_decay_section(spec)
    assert "64% → p + π⁻" in html


def test_feynman_section_empty_without_diagram_file():
    assert sections.render_feynman_section(_spec()) == ""
