from __future__ import annotations

from typing import Any, Mapping


_REQUIRED_EXACT_FIELDS = (
    "name",
    "symbol",
    "hadron_type",
    "family",
    "multiplet",
    "quark_model",
    "mass_mev_exact",
    "quantum_numbers",
)
_REQUIRED_QNUM_FIELDS = (
    "jp",
    "isospin_i",
    "isospin_i3",
    "charge",
    "strangeness",
    "charm",
    "bottomness",
)
_ALLOWED_HADRON_TYPES = {"baryon", "meson"}
_ALLOWED_QMODEL_MODES = {"simple_valence", "flavor_superposition"}
_ALLOWED_DIAGRAM_MODES = {"simple_pair", "simple_triplet", "flavor_superposition"}
_ALLOWED_CONSTITUENT_ROLES = {"quark", "antiquark"}


def _as_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be an object")
    return value


def validate_quantum_numbers(qnums: Any) -> None:
    qnums_map = _as_mapping(qnums, "exact.quantum_numbers")
    for key in _REQUIRED_QNUM_FIELDS:
        if key not in qnums_map:
            raise ValueError(f"canonical particle missing exact.quantum_numbers.{key}")


def validate_quark_model(quark_model: Any) -> None:
    model = _as_mapping(quark_model, "exact.quark_model")
    mode = model.get("mode")
    if mode not in _ALLOWED_QMODEL_MODES:
        raise ValueError(f"unknown quark_model.mode: {mode}")

    if mode == "simple_valence":
        constituents = model.get("constituents")
        if not isinstance(constituents, list) or len(constituents) == 0:
            raise ValueError("simple_valence requires constituents")
        for idx, constituent in enumerate(constituents):
            part = _as_mapping(constituent, f"exact.quark_model.constituents[{idx}]")
            if "quark" not in part or "role" not in part:
                raise ValueError("simple_valence constituent requires quark and role")
            role = part.get("role")
            if role not in _ALLOWED_CONSTITUENT_ROLES:
                raise ValueError(
                    "simple_valence constituent.role must be one of: "
                    f"{_ALLOWED_CONSTITUENT_ROLES}"
                )
        return

    terms = model.get("terms")
    if not isinstance(terms, list) or len(terms) == 0:
        raise ValueError("flavor_superposition requires non-empty terms")
    for idx, term in enumerate(terms):
        term_map = _as_mapping(term, f"exact.quark_model.terms[{idx}]")
        if "coefficient" not in term_map or "pair" not in term_map:
            raise ValueError("flavor_superposition term requires coefficient and pair")
        pair = _as_mapping(term_map["pair"], f"exact.quark_model.terms[{idx}].pair")
        if "quark" not in pair or "antiquark" not in pair:
            raise ValueError("flavor_superposition pair requires quark and antiquark")


def validate_particle_record(record: Any) -> None:
    record_map = _as_mapping(record, "particle")

    particle_id = record_map.get("id")
    if not isinstance(particle_id, str) or not particle_id.strip():
        raise ValueError("canonical particle missing id")

    exact = record_map.get("exact")
    exact_map = _as_mapping(exact, "exact")
    for field in _REQUIRED_EXACT_FIELDS:
        if field not in exact_map:
            raise ValueError(f"canonical particle missing exact.{field}")
    for field in ("name", "symbol", "family", "multiplet"):
        value = exact_map.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"exact.{field} must be a non-empty string")

    hadron_type = exact_map.get("hadron_type")
    if hadron_type not in _ALLOWED_HADRON_TYPES:
        raise ValueError(f"exact.hadron_type must be one of: {_ALLOWED_HADRON_TYPES}")

    mass_mev_exact = exact_map.get("mass_mev_exact")
    if not isinstance(mass_mev_exact, (int, float)) or mass_mev_exact <= 0:
        raise ValueError("exact.mass_mev_exact must be a positive number")

    validate_quark_model(exact_map.get("quark_model"))
    validate_quantum_numbers(exact_map.get("quantum_numbers"))

    pedagogical = record_map.get("pedagogical")
    if pedagogical is None:
        return
    pedagogical_map = _as_mapping(pedagogical, "pedagogical")

    diagram_mode = pedagogical_map.get("diagram_mode")
    if diagram_mode is not None and diagram_mode not in _ALLOWED_DIAGRAM_MODES:
        raise ValueError(f"pedagogical.diagram_mode must be one of: {_ALLOWED_DIAGRAM_MODES}")
