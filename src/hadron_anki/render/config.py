import json
import re
from pathlib import Path

from typing import Any

DEFAULT_STYLE: dict[str, Any] = {
    "palette": {
        "flavors": {
            "u": "#ff0000",
            "d": "#0000ff",
            "s": "#00ff00",
            "c": "#ffff00",
            "b": "#ff00ff",
            "t": "#00ffff",
        },
        "defaults": {
            "unknown": "#cccccc"
        }
    },
    "flavors": {},
    "connector": {"stroke": "gray", "stroke-width": "2"},
    "label": {"font-family": "monospace", "font-size": "14", "text-anchor": "middle"}
}


def _strip_jsonc_comments(text: str) -> str:
    """Removes JSONC comments from a string using a regex callback."""
    pattern = r'("(?:\\.|[^"\\])*")|//[^\r\n]*|/\*[\s\S]*?\*/'

    def replace(match: re.Match[str]) -> str:
        if match.group(1):
            return match.group(1)
        return ""

    return re.sub(pattern, replace, text)


def _deep_merge(base: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
    """Deep merges two dictionaries."""
    res = base.copy()
    for k, v in update.items():
        if k in res and isinstance(res[k], dict) and isinstance(v, dict):
            res[k] = _deep_merge(res[k], v)
        else:
            res[k] = v
    return res


def load_style_config(path: str | None = None) -> dict[str, Any]:
    """Loads a JSONC style config file and merges it with DEFAULT_STYLE."""
    if path is None:
        path = "hadron.json"

    p = Path(path)
    if not p.exists():
        return DEFAULT_STYLE.copy()

    try:
        text = p.read_text(encoding="utf-8")
        clean_text = _strip_jsonc_comments(text)
        data = json.loads(clean_text)

        if not isinstance(data, dict):
            return DEFAULT_STYLE.copy()

        return _deep_merge(DEFAULT_STYLE, data)
    except Exception:
        return DEFAULT_STYLE.copy()


def get_flavor_color(style: dict[str, Any], token: str, color_key: str = "base") -> str:
    """Gets the color for a given token/flavor."""
    flavor = token.replace("anti-", "")

    # 1. Try style["flavors"][flavor][color_key] (Test-compatible)
    if "flavors" in style and flavor in style["flavors"]:
        f_val = style["flavors"][flavor]
        if isinstance(f_val, dict):
            return f_val.get(color_key, style.get("palette", {}).get("defaults", {}).get("unknown", "#cccccc"))
        return str(f_val)

    # 2. Try style["palette"]["flavors"][flavor] (Task-compatible)
    palette = style.get("palette", {})
    flavors = palette.get("flavors", {})
    if flavor in flavors:
        return str(flavors[flavor])

    # 3. Fallback to unknown
    return str(palette.get("defaults", {}).get("unknown", "#cccccc"))


def node_svg_attrs(token: str, style: dict[str, Any]) -> dict[str, str]:
    """Returns SVG attributes for a node based on its token and style."""
    color = get_flavor_color(style, token)

    attrs = {
        "fill": color,
        "stroke": "black",
        "stroke-width": "2"
    }
    if token.startswith("anti-"):
        attrs["stroke-dasharray"] = "4"

    return attrs
