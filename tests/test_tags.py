from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.cards.tags import build_tags

def test_tags_include_particle_type():
    spec = ParticleSpec(id="p", name="Proton", type="baryon", quarks=["u", "u", "d"])
    tags = build_tags(spec, "mass")
    assert "particle:baryon" in tags

def test_tags_include_quark_content():
    spec = ParticleSpec(id="p", name="Proton", type="baryon", quarks=["u", "u", "d"])
    tags = build_tags(spec, "mass")
    assert "quark:u" in tags
    assert "quark:d" in tags
    # Ensure deduplication
    assert tags.count("quark:u") == 1

def test_tags_are_deterministic():
    spec = ParticleSpec(id="p", name="Proton", type="baryon", quarks=["u", "u", "d"])
    tags1 = build_tags(spec, "mass")
    tags2 = build_tags(spec, "mass")
    assert tags1 == tags2
    # Ensure they are sorted (list equality checks ordered)
    assert tags1 == sorted(tags1)
    
    assert "difficulty:basic" in tags1
    assert "source:core" in tags1
