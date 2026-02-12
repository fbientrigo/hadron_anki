import os
import re
import json
import zipfile
import pytest
import tempfile
from hadron_anki.deck.ids import stable_note_guid
from hadron_anki.deck.apkg import build_apkg

def test_stable_note_guid_is_deterministic():
    args = ("proton", "1.0.0", "v1")
    id1 = stable_note_guid(*args)
    id2 = stable_note_guid(*args)
    assert id1 == id2

def test_stable_note_guid_format():
    guid = stable_note_guid("proton", "1.0.0", "v1")
    # Lowercase ASCII hex, at least 32 chars
    assert re.match(r"^[a-f0-9]{32,}$", guid)

def test_stable_note_guid_sensitivity():
    base_args = ["proton", "1.0.0", "v1"]
    base_guid = stable_note_guid(*base_args)
    
    # Change particle_id
    args = base_args.copy()
    args[0] = "neutron"
    assert stable_note_guid(*args) != base_guid
    
    # Change template_version
    args = base_args.copy()
    args[1] = "1.0.1"
    assert stable_note_guid(*args) != base_guid
    
    # Change model_version
    args = base_args.copy()
    args[2] = "v2"
    assert stable_note_guid(*args) != base_guid

def test_build_apkg_contract(catalog_min):
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = os.path.join(tmpdir, "test.apkg")
        build_apkg(catalog_min, out_path, "1.0.0", "v1")
        
        assert os.path.exists(out_path)
        assert zipfile.is_zipfile(out_path)
        
        with zipfile.ZipFile(out_path, 'r') as z:
            namelist = z.namelist()
            assert "collection.anki2" in namelist
            assert "media" in namelist
            
            with z.open("media") as f:
                media_data = json.load(f)
                assert isinstance(media_data, dict)
                
                # Check numeric string keys and .svg values
                svg_keys = []
                svg_values = []
                for key, value in media_data.items():
                    assert key.isdigit()
                    if value.endswith(".svg"):
                        svg_keys.append(key)
                        svg_values.append(value)

                assert len(svg_keys) >= 3
                assert "proton.svg" in svg_values
                assert "neutron.svg" in svg_values
                assert "pi_plus.svg" in svg_values
                
                # Verify corresponding numeric file exists in zip
                for key in svg_keys:
                    assert key in namelist
