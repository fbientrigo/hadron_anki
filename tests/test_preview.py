"""Tests for the preview generator."""
import pytest
from pathlib import Path
from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.render.svg import render_svg
from hadron_anki.preview.generator import generate_preview


def test_generate_preview_creates_files(tmp_path):
    specs = [
        ParticleSpec(id="p1", name="Proton", type="baryon", quarks=["u", "u", "d"]),
        ParticleSpec(id="n1", name="Neutron", type="baryon", quarks=["u", "d", "d"]),
    ]
    output_dir = tmp_path / "preview"
    generate_preview(specs, output_dir)

    assert (output_dir / "index.html").exists()
    assert (output_dir / "mass").is_dir()
    assert (output_dir / "composition").is_dir()
    assert (output_dir / "identity").is_dir()
    assert (output_dir / "mass" / "p1.svg").exists()
    assert (output_dir / "composition" / "n1.svg").exists()


def test_generate_preview_content_integrity(tmp_path):
    spec = ParticleSpec(id="p1", name="Proton", type="baryon", quarks=["u", "u", "d"])
    output_dir = tmp_path / "preview"
    generate_preview([spec], output_dir)

    svg_path = output_dir / "mass" / "p1.svg"
    expected_svg = render_svg(spec)
    assert svg_path.read_text(encoding="utf-8") == expected_svg
    
    # Also verify it's in composition dir
    comp_svg_path = output_dir / "composition" / "p1.svg"
    assert comp_svg_path.read_text(encoding="utf-8") == expected_svg


def test_preview_index_has_styled_structure(tmp_path):
    """Preview HTML must embed CSS and show card structure."""
    specs = [
        ParticleSpec(id="p1", name="Proton", type="baryon", quarks=["u", "u", "d"]),
        ParticleSpec(id="n1", name="Neutron", type="baryon", quarks=["u", "d", "d"]),
    ]
    output_dir = tmp_path / "preview"
    generate_preview(specs, output_dir)

    content = (output_dir / "index.html").read_text()

    # Must embed CSS
    assert "<style>" in content
    assert "card-shell" in content

    # Sections must be present
    assert "<h2>Mass Cards</h2>" in content
    assert "<h2>Composition Cards</h2>" in content
    assert "<h2>Identity Cards</h2>" in content

    # Must contain img references with correct subpaths
    assert 'src="composition/p1.svg"' in content

    # Must show card pairs (front + back)
    assert "front" in content
    assert "back" in content

    # Must have gallery structure
    assert "gallery" in content


def test_preview_shows_particle_data(tmp_path):
    """Preview must render particle information for each card."""
    specs = [
        ParticleSpec(id="p1", name="Proton", type="baryon", quarks=["u", "u", "d"]),
    ]
    output_dir = tmp_path / "preview"
    generate_preview(specs, output_dir)

    content = (output_dir / "index.html").read_text()

    # Back card data (mass card example)
    assert "Proton" in content
    assert "baryon" in content
    assert "title" in content
    assert "badge" in content

def test_preview_deterministic_structure(tmp_path):
    """Ensure preview folder output relies strictly on inputs and avoids random state."""
    specs = [
        ParticleSpec(id="p1", name="Proton", type="baryon", quarks=["u", "u", "d"]),
        ParticleSpec(id="n1", name="Neutron", type="baryon", quarks=["u", "d", "d"]),
    ]
    out1 = tmp_path / "run1"
    out2 = tmp_path / "run2"
    generate_preview(specs, out1)
    generate_preview(specs, out2)

    assert (out1 / "index.html").read_text(encoding="utf-8") == (out2 / "index.html").read_text(encoding="utf-8")
    assert (out1 / "mass" / "p1.svg").read_text(encoding="utf-8") == (out2 / "mass" / "p1.svg").read_text(encoding="utf-8")


def test_preview_generates_feynman_svgs(tmp_path):
    """Feynman preview creates subdir and SVG files."""
    from hadron_anki.preview.generator import generate_feynman_preview

    feynman_specs = [
        {
            "id": "pi_plus_decay",
            "label": "pi+ decay",
            "decay_diagram": {
                "nodes": [
                    {"id": "in",   "x": 50,  "y": 90},
                    {"id": "v1",   "x": 160, "y": 90},
                    {"id": "out1", "x": 270, "y": 45},
                    {"id": "out2", "x": 270, "y": 135},
                ],
                "edges": [
                    {"from": "in",  "to": "v1",   "type": "scalar",  "label": "pi+"},
                    {"from": "v1",  "to": "out1",  "type": "fermion", "label": "mu+"},
                    {"from": "v1",  "to": "out2",  "type": "fermion", "label": "nu_mu"},
                ],
            },
        }
    ]

    out = tmp_path / "preview"
    generate_feynman_preview(feynman_specs, out)

    assert (out / "feynman").is_dir()
    svg_file = out / "feynman" / "pi_plus_decay.svg"
    assert svg_file.exists()
    svg_content = svg_file.read_text(encoding="utf-8")
    assert "<svg" in svg_content
    assert "<circle" in svg_content   # vertices

