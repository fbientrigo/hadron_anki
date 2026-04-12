# Pedagogical Schema V1 (Canonical Contract)

## Purpose
`hadron_anki` needs a canonical, versioned source of truth in-repo, independent from exported `.apkg` decks.  
This schema defines stable particle data for physics truth plus derived pedagogical fields for study UX.

## Exact vs Derived
Use two explicit blocks per particle:

- `exact`: physics data that should be traceable and versioned as truth.
- `pedagogical`: derived fields for study flow, ranking, and display.

Rule: `pedagogical` can be regenerated from `exact` + deterministic rules.  
Rule: do not overwrite `exact` with teaching approximations.

## Canonical Shape
Each particle record should include at least:

- `id`
- `name`
- `symbol`
- `hadron_type`
- `family`
- `multiplet`
- `quark_model`
- `mass_mev_exact`
- `quantum_numbers`

Suggested top-level record:

```yaml
id: proton
exact: {...}
pedagogical: {...}
```

## `quark_model` Block
`quark_model` must be structured, not plain string.

### Mode 1: `simple_valence`
For unmixed valence content (typical baryons, charged pions, kaons, etc.).

```yaml
quark_model:
  mode: simple_valence
  constituents:
    - quark: u
      role: quark
    - quark: u
      role: quark
    - quark: d
      role: quark
```

### Mode 2: `flavor_superposition`
For flavor-mixed neutral states (`pi0`, `eta`, `eta_prime`, future states).

```yaml
quark_model:
  mode: flavor_superposition
  basis: quark_antiquark_flavor
  terms:
    - coefficient:
        sign: 1
        kind: sqrt_fraction
        numerator: 1
        denominator: 2
        decimal: 0.70710678
      pair: {quark: u, antiquark: u}
    - coefficient:
        sign: -1
        kind: sqrt_fraction
        numerator: 1
        denominator: 2
        decimal: -0.70710678
      pair: {quark: d, antiquark: d}
  normalized: true
  latex: "\\frac{u\\bar u - d\\bar d}{\\sqrt{2}}"
```

Notes:
- `latex` optional helper for rendering, never only representation.
- `terms[*].coefficient.decimal` optional but useful for ordering and numeric transforms.
- `normalized` allows consistency checks in future validator.

## `quantum_numbers` Block
Minimum required in V1:

- `jp`
- `isospin_i`
- `isospin_i3`
- `charge`
- `strangeness`
- `charm`
- `bottomness`

Example:

```yaml
quantum_numbers:
  jp: "1/2+"
  isospin_i: "1/2"
  isospin_i3: "+1/2"
  charge: +1
  strangeness: 0
  charm: 0
  bottomness: 0
```

## Pedagogical Derived Fields
Minimum V1:

- `mass_display`
- `mass_bucket`
- `mass_rank_in_family`
- `diagram_mode`
- `display_quark_summary`

### `mass_display`
Human-facing rounded mass string from `mass_mev_exact`.

Simple deterministic rule:
- if `mass_mev_exact < 1000`: round to nearest `1 MeV`.
- else: round to nearest `10 MeV`.
- format: `"<value> MeV"`.

Examples:
- `938.272 -> "938 MeV"`
- `547.862 -> "548 MeV"`
- `1314.86 -> "1310 MeV"`

### `mass_bucket`
Coarse study bucket (not PDG classification).

Default V1 thresholds (MeV):
- `ultralight`: `< 200`
- `light`: `200 - < 600`
- `intermediate`: `600 - < 1200`
- `heavy`: `>= 1200`

These are pedagogical bins and may be tuned without changing `exact`.

### `mass_rank_in_family`
Rank by ascending `mass_mev_exact` among particles with same `family`.
- deterministic tie-breaker: `id` lexicographic.
- store as integer starting at `1`.
- derive only when dataset context for that family has at least 2 records.
- if family has fewer than 2 records in provided dataset slice, omit this field.

### `diagram_mode`
Renderer hint derived from structure:
- `flavor_superposition` if `quark_model.mode == flavor_superposition`
- else `simple_triplet` if `hadron_type == baryon`
- else `simple_pair` if `hadron_type == meson`

### `display_quark_summary`
Study-ready compact text from `quark_model`:
- `simple_valence`: `"u u d"` or `"u dbar"` style.
- `flavor_superposition`: short basis summary, e.g. `"(u ubar - d dbar)/sqrt(2)"`.

## Criteria: `simple_valence` vs `flavor_superposition`
Choose `simple_valence` when one valence assignment is pedagogically and physically valid as primary representation.  
Choose `flavor_superposition` when state is defined by mixed flavor basis and simplification to one pair would be wrong.

Mandatory `flavor_superposition` support in V1 bridge: at least `pi0` and octet-basis `eta8` examples.

## Legacy Adapter Constraint (Stage 1 Bridge)
Temporary adapter from canonical schema to legacy `ParticleSpec` supports only:
- `quark_model.mode == simple_valence`

If record uses `flavor_superposition`, adapter must fail loudly (no silent collapse).

## Worked Examples

### Proton
- `hadron_type`: baryon
- `quark_model.mode`: `simple_valence`
- constituents: `u u d`
- `diagram_mode`: `simple_triplet`

### Neutron
- `hadron_type`: baryon
- `quark_model.mode`: `simple_valence`
- constituents: `u d d`
- `diagram_mode`: `simple_triplet`

### Pi Plus (`pi_plus`)
- `hadron_type`: meson
- `quark_model.mode`: `simple_valence`
- constituents: `u anti-d`
- `diagram_mode`: `simple_pair`

### Pi Zero (`pi0`)
- `hadron_type`: meson
- `quark_model.mode`: `flavor_superposition`
- terms include `u ubar` and `d dbar` with opposite-sign coefficients
- `diagram_mode`: `flavor_superposition`

### Eta8 Basis State (`eta8`)
- `hadron_type`: meson
- `quark_model.mode`: `flavor_superposition`
- terms include `u ubar`, `d dbar`, `s sbar`
- `diagram_mode`: `flavor_superposition`
- this example is octet-basis state (`eta8`), not fully mixed physical `eta`.

## What Is Out of Scope for V1
- Full PDG tables.
- Branching-ratio integration in canonical particle records.
- Full spectroscopic state taxonomy beyond needed `family/multiplet`.
- Final Anki back template redesign for all cards.
- Full renderer migration for mixed-state diagrams.
- Auto-inference of advanced physics quantities not present in source data.
