import pytest
import yaml
import pathlib

@pytest.fixture
def catalog_min():
    path = pathlib.Path(__file__).parent / "fixtures" / "catalog_min.yaml"
    return yaml.safe_load(path.read_text())
