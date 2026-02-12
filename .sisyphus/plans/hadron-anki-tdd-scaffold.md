# hadron_anki: Strict TDD scaffold for Anki APKG + SVG pipeline

## TL;DR

> **Quick Summary**: Scaffold a new Python package with strict TDD tests (intentionally RED via explicit `NotImplementedError`) for a future pipeline that builds `.apkg` Anki decks with SVG media.
>
> **Deliverables**:
> - `pyproject.toml` + `src/` package layout
> - `src/hadron_anki/{domain,catalog,render,cards,deck}/...` with importable stubs
> - `tests/` with 4 test modules + `tests/fixtures/catalog_min.yaml`

**Estimated Effort**: Short
**Parallel Execution**: YES - 2 waves
**Critical Path**: Project scaffold -> tests + stubs -> verification (collect + intentional failures)

---

## Context

### Original Request
Create a strict TDD pipeline scaffold in a new Python repo (`hadron_anki`) to generate exportable Anki decks (`.apkg`) with SVG media and notes, keeping dependencies minimal.

### Interview Summary
**Key Discussions**:
- Strict TDD: tests first; code is minimal import stubs and explicit `raise NotImplementedError`.
- Minimal dependencies: runtime `genanki`, `pyyaml`; dev `pytest`.
- Module boundaries: pure modules in `domain`, `catalog`, `render`, `cards`, `deck`; avoid business logic in CLI.
- Deterministic IDs must derive from `particle_id + template_version + model_version`.
- PR expectation: tests intentionally fail at explicit `NotImplementedError` points (no `ImportError`).

**Primary source of truth captured during interview**:
- `.sisyphus/drafts/hadron-anki-tdd-scaffold.md`

### Metis Review
**Identified gaps (addressed via defaults / guardrails)**:
- Clarify SVG generation approach and visuals; clarify media lifecycle; clarify CLI inclusion; prevent genanki leakage into domain; add explicit verification for RED state.

---

## Work Objectives

### Core Objective
Establish a working Python package scaffold and a strict TDD test suite that defines the intended behavior for catalog parsing, SVG rendering, card templates, deterministic IDs, and `.apkg` packaging.

### Concrete Deliverables
- `pyproject.toml` with a src-layout package and `pytest` as a dev extra
- Source layout:
  - `src/hadron_anki/__init__.py`
  - `src/hadron_anki/domain/{__init__.py,spec.py,composer.py}`
  - `src/hadron_anki/catalog/{__init__.py,loader.py}`
  - `src/hadron_anki/render/{__init__.py,svg.py}`
  - `src/hadron_anki/cards/{__init__.py,templates.py}`
  - `src/hadron_anki/deck/{__init__.py,ids.py,apkg.py}`
- Tests + fixtures:
  - `tests/test_composer.py`
  - `tests/test_renderer_svg.py`
  - `tests/test_templates.py`
  - `tests/test_deck_apkg.py`
  - `tests/fixtures/catalog_min.yaml`
  - `tests/conftest.py` (shared fixture for loading YAML)

### Definition of Done
- [ ] `python -m pip install -e ".[dev]"` succeeds
- [ ] `pytest --collect-only` collects exactly the four required test modules
- [ ] `pytest` fails (non-zero) due to explicit `NotImplementedError` in the planned stubs (and NOT due to `ImportError`)

### Must Have
- Strict TDD RED state with explicit `NotImplementedError` from planned APIs
- Minimal dependency set: runtime `genanki`, `pyyaml`; dev `pytest`
- Data conventions:
  - `ParticleSpec` fields: `id`, `name`, `type` (baryon|meson), `quarks: list[str]`
  - Antiquark token normalization to `anti-` prefix (e.g. `anti-u`)
- Template front HTML must match exactly: `<img src="FILENAME.svg">`
- SVG renderer returns an SVG string with `<svg` root
- APKG tests specify: zip includes `collection.anki2` and `media` JSON mapping and a numeric media file

### Must NOT Have (Guardrails)
- No full implementation logic (keep stubs; do not “green” the suite)
- No additional dependencies (no svgwrite, no click/typer, no heavy graphics libs)
- No CLI entrypoint in this scaffold (library-only for now)
- No genanki objects in `hadron_anki.domain.*` (keep `domain` pure)

---

## Verification Strategy (MANDATORY)

> **UNIVERSAL RULE: ZERO HUMAN INTERVENTION**
>
> Every task must be verifiable by agent-run commands. No “user manually checks”.

### Test Decision
- **Infrastructure exists**: NO (new repo baseline)
- **Automated tests**: YES (TDD strict, intentionally RED)
- **Framework**: `pytest`

### Agent-Executed QA Scenarios (MANDATORY)

All scenarios in this plan use Bash commands (no UI).

Evidence capture convention:
- Store command outputs in `.sisyphus/evidence/` (create directory if missing)

---

## Execution Strategy

### Parallel Execution Waves

Wave 1 (Scaffold + contracts):
- Task 1: Project packaging scaffold (`pyproject.toml`, src-layout, pytest baseline)
- Task 2: Fixture + catalog contract + domain contracts (dataclass + stub modules)

Wave 2 (Test suite + stubs wired end-to-end):
- Task 3: `tests/test_templates.py` + `hadron_anki.cards.templates`
- Task 4: `tests/test_renderer_svg.py` + `hadron_anki.render.svg`
- Task 5: `tests/test_composer.py` + `hadron_anki.domain.composer`
- Task 6: `tests/test_deck_apkg.py` + `hadron_anki.deck.{ids,apkg}`

Critical Path: Task 1 -> (Tasks 3-6) -> final verification

---

## TODOs

> Implementation + Test = ONE Task.
> This plan intentionally ends in a RED test suite (explicit `NotImplementedError`).

- [x] 1. Create Python packaging scaffold + pytest baseline

  **What to do**:
  - Create `pyproject.toml` with:
    - Project name `hadron-anki` and package module `hadron_anki`
    - Python `>=3.11`
    - Runtime deps: `genanki`, `pyyaml`
    - Dev extra: `pytest`
    - src-layout packaging (`package-dir` / equivalent)
  - Create `src/hadron_anki/__init__.py` (empty ok)
  - Add `tests/` package baseline (directory + `__init__.py` optional)

  **Must NOT do**:
  - Add other deps (no `svgwrite`, no `click`)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: straightforward scaffold and config files
  - **Skills**: (none)
  - **Skills Evaluated but Omitted**:
    - `playwright`: no browser/UI verification

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 3-6 (tests need install/imports)
  - **Blocked By**: None

  **References**:
  - `.sisyphus/drafts/hadron-anki-tdd-scaffold.md` - authoritative constraints, file list, API surface
  - `README.md` - repo identity; keep scaffold aligned with project intent
  - Official docs: https://packaging.python.org/en/latest/specifications/pyproject-toml/ - pyproject basics
  - Official docs: https://docs.pytest.org/en/stable/ - pytest conventions

  **Acceptance Criteria**:
  - [ ] `python -m pip install -e ".[dev]"` -> exits 0
  - [ ] `python -c "import hadron_anki; print('ok')"` -> prints `ok`
  - [ ] `pytest --version` -> exits 0

  **Agent-Executed QA Scenarios**:

  ```
  Scenario: Editable install works
    Tool: Bash
    Preconditions: none
    Steps:
      1. mkdir -p .sisyphus/evidence
      2. python -m pip install -e ".[dev]" | tee .sisyphus/evidence/task-1-pip-install.txt
      3. python -c "import hadron_anki; print(hadron_anki.__name__)" | tee .sisyphus/evidence/task-1-import.txt
    Expected Result: install succeeds; import prints hadron_anki
    Evidence: .sisyphus/evidence/task-1-pip-install.txt, .sisyphus/evidence/task-1-import.txt
  ```

- [x] 2. Add fixture + catalog/domain module skeleton (importable)

  **What to do**:
  - Create `tests/fixtures/catalog_min.yaml` with entries for `proton`, `neutron`, `pi_plus`.
    - Default YAML schema (tests should target this unless overridden later):
      - Top-level mapping with key `particles` (list)
      - Each particle item has: `id`, `name`, `type`, `quarks`, `aliases`
    - `aliases` should include at least one alias per particle (can be empty list if you prefer; make the test decide).
  - Add skeleton modules (importable) for the planned API surface:
    - `hadron_anki.domain.spec.ParticleSpec` (dataclass; data-only)
    - `hadron_anki.catalog.loader.load_catalog(path)` (stub: `raise NotImplementedError`)
  - Create package directories and `__init__.py` files for:
    - `src/hadron_anki/domain/`
    - `src/hadron_anki/catalog/`
    - `src/hadron_anki/render/`
    - `src/hadron_anki/cards/`
    - `src/hadron_anki/deck/`
  - Create `tests/conftest.py` with a shared fixture that loads `tests/fixtures/catalog_min.yaml` via `yaml.safe_load`.

  **Must NOT do**:
  - Add extra fields (mass/charge/spin)
  - Implement business logic beyond dataclass wiring

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: (none)

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Task 1)
  - **Blocks**: Tasks 5-6 (tests rely on fixture/schema)
  - **Blocked By**: None

  **References**:
  - `.sisyphus/drafts/hadron-anki-tdd-scaffold.md` - required fixture content + conventions
  - External docs: https://pyyaml.org/wiki/PyYAMLDocumentation - YAML parsing assumptions used in tests

  **Acceptance Criteria**:
  - [ ] `python -c "import yaml; import pathlib; p=pathlib.Path('tests/fixtures/catalog_min.yaml'); print(type(yaml.safe_load(p.read_text())))"` -> exits 0
  - [ ] `python -c "from hadron_anki.domain.spec import ParticleSpec; print(ParticleSpec)"` -> exits 0

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: Fixture is valid YAML
    Tool: Bash
    Preconditions: tests/fixtures/catalog_min.yaml exists
    Steps:
      1. mkdir -p .sisyphus/evidence
      2. python -c "import yaml; import pathlib; p=pathlib.Path('tests/fixtures/catalog_min.yaml'); print(yaml.safe_load(p.read_text()))" | tee .sisyphus/evidence/task-2-yaml-print.txt
    Expected Result: prints parsed YAML object without exception
    Evidence: .sisyphus/evidence/task-2-yaml-print.txt
  ```

- [x] 3. Define templates contract tests + stub API

  **What to do**:
  - Create `tests/test_templates.py` specifying:
    - `front_html(media_filename)` returns exactly `<img src="FILENAME.svg">` for a given filename
    - `back_html(spec)` includes at least the particle name/id and quark list (define exact string requirements in the test)
  - Create `src/hadron_anki/cards/templates.py` with `front_html` and `back_html` stubs that raise `NotImplementedError`.

  **Must NOT do**:
  - Implement HTML rendering (keep RED)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: (none)

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Final verification
  - **Blocked By**: Task 1

  **References**:
  - `.sisyphus/drafts/hadron-anki-tdd-scaffold.md` - exact front template requirement

  **Acceptance Criteria**:
  - [ ] `pytest -q tests/test_templates.py` -> FAIL with `NotImplementedError` (and NOT `ImportError`)

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: Template tests run and fail at NotImplementedError
    Tool: Bash
    Preconditions: editable install succeeded (Task 1)
    Steps:
      1. mkdir -p .sisyphus/evidence
      2. pytest -q tests/test_templates.py | tee .sisyphus/evidence/task-3-pytest-templates.txt
    Expected Result: non-zero exit; output includes "NotImplementedError"
    Evidence: .sisyphus/evidence/task-3-pytest-templates.txt
  ```

- [x] 4. Define SVG renderer contract tests + stub API

  **What to do**:
  - Create `tests/test_renderer_svg.py` specifying:
    - `render_svg(spec)` returns a `str` containing `<svg` as the root
    - Must not rely on heavy graphics libs (string-based SVG)
    - Include at least one assertion about quark text inclusion (define exact expectations)
  - Create `src/hadron_anki/render/svg.py` with `render_svg` stub raising `NotImplementedError`.

  **Must NOT do**:
  - Add SVG dependencies
  - Implement SVG rendering (keep RED)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: (none)

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Final verification
  - **Blocked By**: Task 1

  **References**:
  - `.sisyphus/drafts/hadron-anki-tdd-scaffold.md` - SVG constraints and required output shape

  **Acceptance Criteria**:
  - [ ] `pytest -q tests/test_renderer_svg.py` -> FAIL with `NotImplementedError` (not import errors)

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: SVG tests run and fail at NotImplementedError
    Tool: Bash
    Preconditions: editable install succeeded (Task 1)
    Steps:
      1. mkdir -p .sisyphus/evidence
      2. pytest -q tests/test_renderer_svg.py | tee .sisyphus/evidence/task-4-pytest-svg.txt
    Expected Result: non-zero exit; output includes "NotImplementedError"
    Evidence: .sisyphus/evidence/task-4-pytest-svg.txt
  ```

- [x] 5. Define quark normalization/validation contract tests + stub API

  **What to do**:
  - Create `tests/test_composer.py` specifying contracts for:
    - `normalize_quark_token(token)`:
      - canonical antiquark token uses `anti-` prefix
      - idempotent on already-normalized tokens
    - `validate_quark_count(spec)`:
      - baryon must have 3 quarks
      - meson must have 2 quarks
      - define the exception type/message contract in the test
  - Create `src/hadron_anki/domain/composer.py` with these functions as stubs raising `NotImplementedError`.

  **Must NOT do**:
  - Implement the logic (keep RED)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: (none)

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Final verification
  - **Blocked By**: Task 1

  **References**:
  - `.sisyphus/drafts/hadron-anki-tdd-scaffold.md` - data conventions, type values, antiquark prefix

  **Acceptance Criteria**:
  - [ ] `pytest -q tests/test_composer.py` -> FAIL with `NotImplementedError` (not import errors)

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: Composer tests run and fail at NotImplementedError
    Tool: Bash
    Preconditions: editable install succeeded (Task 1)
    Steps:
      1. mkdir -p .sisyphus/evidence
      2. pytest -q tests/test_composer.py | tee .sisyphus/evidence/task-5-pytest-composer.txt
    Expected Result: non-zero exit; output includes "NotImplementedError"
    Evidence: .sisyphus/evidence/task-5-pytest-composer.txt
  ```

- [x] 6. Define deterministic ID + APKG contract tests + stub API

  **What to do**:
  - Create `tests/test_deck_apkg.py` specifying contracts for:
    - `stable_note_guid(particle_id, template_version, model_version)`:
      - deterministic: same inputs -> same output
      - format: ASCII hex string (define exact regex in the test)
      - sensitivity: changing any component changes the guid
    - `build_apkg(catalog, out_path, template_version, model_version)`:
      - writes a `.apkg` (zip) at `out_path`
      - zip contains `collection.anki2` and `media`
      - `media` JSON contains numeric keys mapping to `*.svg`
      - corresponding numeric media file exists in zip
  - Create stubs:
    - `src/hadron_anki/deck/ids.py` with `stable_note_guid` raising `NotImplementedError`
    - `src/hadron_anki/deck/apkg.py` with `build_apkg` raising `NotImplementedError`
  - Ensure tests avoid depending on `genanki` internals beyond observable zip outputs.

  **Must NOT do**:
  - Implement packaging logic (keep RED)
  - Leak `genanki` types into domain modules

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
    - Reason: test authoring requires careful zip/media assertions
  - **Skills**: (none)

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: Final verification
  - **Blocked By**: Task 1

  **References**:
  - `.sisyphus/drafts/hadron-anki-tdd-scaffold.md` - deterministic ID and apkg structure requirements
  - External: https://github.com/kerrickstaley/genanki - library used later for implementation

  **Acceptance Criteria**:
  - [ ] `pytest -q tests/test_deck_apkg.py` -> FAIL with `NotImplementedError` (not import errors)

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: Deck/APKG tests run and fail at NotImplementedError
    Tool: Bash
    Preconditions: editable install succeeded (Task 1)
    Steps:
      1. mkdir -p .sisyphus/evidence
      2. pytest -q tests/test_deck_apkg.py | tee .sisyphus/evidence/task-6-pytest-deck.txt
    Expected Result: non-zero exit; output includes "NotImplementedError"
    Evidence: .sisyphus/evidence/task-6-pytest-deck.txt
  ```

---

## Success Criteria

### Verification Commands

```bash
python -m pip install -e ".[dev]"
pytest --collect-only
pytest
```

Expected outcomes:
- `pytest --collect-only` shows collection of:
  - `tests/test_composer.py`
  - `tests/test_renderer_svg.py`
  - `tests/test_templates.py`
  - `tests/test_deck_apkg.py`
- `pytest` exits non-zero and failures/errors are attributable to explicit `NotImplementedError` in the planned stubs.

### Defaults Applied (override if needed)
- SVG generation approach (future implementation): pure string-based SVG (f-strings), text-only visuals
- Media lifecycle (future implementation): generate SVGs to a temporary build directory during `.apkg` creation (no persistent cache)
- CLI: no CLI included in scaffold
- ID strategy (future implementation): recommend SHA256 -> take first 63 bits for int IDs; GUID as lowercase ASCII hex
