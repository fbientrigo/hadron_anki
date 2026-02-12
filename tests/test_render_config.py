import json
import pytest
from pathlib import Path
from hadron_anki.render.config import load_style_config, get_flavor_color

def test_load_style_config_missing_file_uses_defaults(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config = load_style_config()
    # Assuming some defaults exist, e.g. a 'flavors' key
    assert "flavors" in config
    assert isinstance(config["flavors"], dict)

def test_load_style_config_reads_repo_json_when_present(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config_data = {
        "flavors": {
            "latte": {"rosewater": "#dc8a78"}
        }
    }
    config_file = tmp_path / "hadron.json"
    config_file.write_text(json.dumps(config_data))
    
    config = load_style_config()
    assert config["flavors"]["latte"]["rosewater"] == "#dc8a78"

def test_get_flavor_color_strips_anti_prefix():
    # Test that "anti-mocha" becomes "mocha" and we get the correct color
    config = {
        "flavors": {
            "mocha": {"blue": "#89b4fa"}
        }
    }
    color = get_flavor_color(config, "anti-mocha", "blue")
    assert color == "#89b4fa"
    
    # Test without prefix
    color = get_flavor_color(config, "mocha", "blue")
    assert color == "#89b4fa"

def test_load_style_config_preserves_comment_markers_in_strings(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # JSONC with comments and "//" inside a string
    jsonc_content = """
    {
        // This is a comment
        "url": "https://example.com/not/a/comment",
        "nested": {
            /* Block comment */
            "path": "//still/not/a/comment"
        }
    }
    """
    config_file = tmp_path / "hadron.json"
    config_file.write_text(jsonc_content)
    
    config = load_style_config()
    assert config["url"] == "https://example.com/not/a/comment"
    assert config["nested"]["path"] == "//still/not/a/comment"
