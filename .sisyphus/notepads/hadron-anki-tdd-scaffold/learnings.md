
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

## 2026-02-11: SVG Renderer Contract (Task 4)
- Defined `render_svg` stub in `src/hadron_anki/render/svg.py`.
- Established contract tests in `tests/test_renderer_svg.py`.
- Contract expectations:
    - Output must be a string.
    - Output must contain `<svg` root element.
    - Output must include quark text tokens from the `ParticleSpec`.
- Verified RED state with `NotImplementedError` as planned.
- Confirmed src-layout imports work correctly for the new `render` package.

## 2026-02-11 - Task 3: Templates Contract Tests
- Defined  and  stubs in .
- Established contract tests in .
-  must return exactly `<img src="{filename}">`.
-  must include particle name, ID, and a comma-separated list of quarks.
- Verified RED state with  as expected.

## 2026-02-11 - Task 3: Templates Contract Tests
- Defined `front_html` and `back_html` stubs in `src/hadron_anki/cards/templates.py`.
- Established contract tests in `tests/test_templates.py`.
- `front_html` must return exactly `<img src="{filename}">`.
- `back_html` must include particle name, ID, and a comma-separated list of quarks.
- Verified RED state with `NotImplementedError` as expected.

## 2026-02-11 - Task 5: Quark Normalization and Validation Contracts
- Canonical antiquark notation: Use `anti-` prefix (e.g., `anti-u`).
- Contract defined: `normalize_quark_token` must handle `*bar` notation and be idempotent.
- Validation contract: Baryons must have exactly 3 quarks; Mesons must have exactly 2 quarks.
- Exceptions: Use `ValueError` with descriptive messages for validation failures.
- Verification: Tests created in `tests/test_composer.py` are RED with `NotImplementedError`.

## [2026-02-11] Task 6: Deck APKG and ID Contract Tests
- Defined contract for `stable_note_guid` ensuring determinism, hex format, and sensitivity to inputs.
- Defined contract for `build_apkg` verifying zip structure, presence of `collection.anki2` and `media` JSON.
- Verified that Anki's `media` file uses numeric keys mapping to original filenames, and those numeric files must exist in the zip root.
- All tests currently RED (failing with `NotImplementedError`) as part of TDD cycle.
