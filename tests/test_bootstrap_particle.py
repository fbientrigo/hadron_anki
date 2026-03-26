import pytest

from hadron_anki.catalog.bootstrap_particle import enrich_particle_metadata

def test_enrich_particle_metadata_proton():
    # We simulate passing the name "proton" or perhaps it finds it via basic querying
    # In particle package, proton name is "p" and pdgid is 2212.
    # The user passes a partial dictionary and we mock/enrich it.
    p = {
        "id": "proton",
        "name": "Proton",
        "type": "baryon",
        "quarks": ["u", "u", "d"]
    }
    
    # "Proton" or "p" usually yields PDG ID 2212
    enriched = enrich_particle_metadata(p, pdg_name="p")
    
    assert enriched["id"] == "proton"
    assert enriched["pdg_id"] == 2212
    assert "mass" in enriched
    assert enriched["mass"] > 938.0
    assert enriched["mass"] < 939.0

def test_enrich_particle_metadata_missing():
    p = {
        "id": "unknown_0",
        "name": "Unknown",
        "type": "meson",
        "quarks": ["x", "y"]
    }
    
    enriched = enrich_particle_metadata(p, pdg_name="unknown_particle_123")
    
    # Should not throw by default, just returns without enriching?
    # Or maybe raises ValueError. The implementation will decide.
    # We will test it expecting unchanged if not found, or None. Let's say unchanged.
    assert "pdg_id" not in enriched
