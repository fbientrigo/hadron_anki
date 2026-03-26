import json
import pytest
import yaml

from hadron_anki.catalog.loader import load_catalog

def test_load_catalog_json(tmp_path):
    catalog_path = tmp_path / "catalog.json"
    catalog_data = {
        "particles": [
            {
                "id": "p_plus",
                "name": "Proton",
                "type": "baryon",
                "quarks": ["u", "u", "d"]
            }
        ]
    }
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f)
        
    loaded = load_catalog(str(catalog_path))
    assert "particles" in loaded
    assert len(loaded["particles"]) == 1
    assert loaded["particles"][0]["id"] == "p_plus"

def test_load_catalog_yaml(tmp_path):
    catalog_path = tmp_path / "catalog.yaml"
    catalog_data = {
        "particles": [
            {
                "id": "n_0",
                "name": "Neutron",
                "type": "baryon",
                "quarks": ["u", "d", "d"],
                "symbol": "n",
                "pdg_id": 2112,
                "aliases": ["neutron"],
                "mass": 939.565
            }
        ]
    }
    with open(catalog_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(catalog_data, f)
        
    loaded = load_catalog(str(catalog_path))
    particle = loaded["particles"][0]
    assert particle["id"] == "n_0"
    assert particle["symbol"] == "n"
    assert particle["pdg_id"] == 2112
    assert particle["aliases"] == ["neutron"]
    assert particle["mass"] == 939.565

def test_load_catalog_unsupported_format(tmp_path):
    catalog_path = tmp_path / "catalog.xml"
    catalog_path.write_text("<catalog></catalog>", encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported catalog format"):
        load_catalog(str(catalog_path))
