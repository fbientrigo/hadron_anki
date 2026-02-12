
# Learning: 2026-02-11
- Successfully initialized a Python src-layout project using `pyproject.toml`.
- Use `setuptools.packages.find` with `where = ["src"]` to correctly handle src-layout.
- Verified that `pip install -e ".[dev]"` correctly installs the package and its dev dependencies.
- Confirmed that the package can be imported as `hadron_anki` while the project name is `hadron-anki`.

# Learning: 2026-02-11 (Task 2)
- Established a basic domain model with  dataclass and a skeleton loader.
- Created a standard YAML fixture for particle data (, , ).
- Implemented a shared ============================= test session starts ==============================
platform linux -- Python 3.12.7, pytest-7.4.4, pluggy-1.0.0
rootdir: /mnt/c/Users/Asus/Documents/FisicoFabi/hadron_anki
plugins: anyio-4.2.0
collected 0 items

============================ no tests ran in 0.68s ============================= fixture in  for easy access to the catalog fixture.
- Confirmed that  successfully parses the custom particle schema.
- Enforced  layout by setting up  files across all planned modules.

# Learning: 2026-02-11 (Task 2)
- Established a basic domain model with `ParticleSpec` dataclass and a skeleton loader.
- Created a standard YAML fixture for particle data (`proton`, `neutron`, `pi_plus`).
- Implemented a shared `pytest` fixture in `conftest.py` for easy access to the catalog fixture.
- Confirmed that `PyYAML` successfully parses the custom particle schema.
- Enforced `src/` layout by setting up `__init__.py` files across all planned modules.
