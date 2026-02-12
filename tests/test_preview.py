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
    assert (output_dir / "p1.svg").exists()
    assert (output_dir / "n1.svg").exists()

def test_generate_preview_content_integrity(tmp_path):
    spec = ParticleSpec(id="p1", name="Proton", type="baryon", quarks=["u", "u", "d"])
    output_dir = tmp_path / "preview"
    generate_preview([spec], output_dir)
    
    svg_path = output_dir / "p1.svg"
    expected_svg = render_svg(spec)
    assert svg_path.read_text() == expected_svg

def test_preview_index_structure(tmp_path):
    specs = [
        ParticleSpec(id="p1", name="Proton", type="baryon", quarks=["u", "u", "d"]),
        ParticleSpec(id="n1", name="Neutron", type="baryon", quarks=["u", "d", "d"]),
    ]
    output_dir = tmp_path / "preview"
    generate_preview(specs, output_dir)
    
    index_content = (output_dir / "index.html").read_text()
    assert '<img' in index_content
    assert 'src="p1.svg"' in index_content
    assert 'src="n1.svg"' in index_content
