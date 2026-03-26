import os
import re
import json
import zipfile
import pytest
import sqlite3
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
    assert re.match(r"^[a-f0-9]{32,}$", guid)

def test_stable_note_guid_sensitivity():
    base_args = ["proton", "1.0.0", "v1"]
    base_guid = stable_note_guid(*base_args)
    
    args = base_args.copy()
    args[0] = "neutron"
    assert stable_note_guid(*args) != base_guid
    
    args = base_args.copy()
    args[1] = "1.0.1"
    assert stable_note_guid(*args) != base_guid
    
    args = base_args.copy()
    args[2] = "v2"
    assert stable_note_guid(*args) != base_guid

def test_total_cards_count_matches_particles_x3():
    catalog = {
        "particles": [
            {"id": "p1", "name": "P1", "type": "baryon", "quarks": ["u", "u", "u"], "mass": 1000},
            {"id": "p2", "name": "P2", "type": "meson", "quarks": ["u", "anti-u"], "mass": 500},
        ]
    }
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = os.path.join(tmpdir, "test.apkg")
        build_apkg(catalog, out_path, "1.0.0", "v1")
        
        with zipfile.ZipFile(out_path, 'r') as z:
            z.extract("collection.anki2", tmpdir)
            
        db_path = os.path.join(tmpdir, "collection.anki2")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM notes")
        notes_count = cursor.fetchone()[0]
        
        # 2 particles * 3 cards = 6 notes
        assert notes_count == 6
        
        cursor.close()
        conn.close()

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
                
                svg_values = [v for k, v in media_data.items() if k.isdigit() and v.endswith(".svg")]
                assert "proton.svg" in svg_values
