import json
import yaml
from typing import Any

def load_catalog(path: str) -> dict[str, Any]:
    """
    Load a particle catalog from a JSON or YAML file.
    
    Returns the schema expected by `build_apkg` (a dictionary with a 'particles' list).
    """
    with open(path, "r", encoding="utf-8") as f:
        if path.endswith(".json") or path.endswith(".jsonc"):
            data = json.load(f)
        elif path.endswith(".yaml") or path.endswith(".yml"):
            data = yaml.safe_load(f)
        else:
            raise ValueError("Unsupported catalog format: must be .json or .yaml")
            
    return data
