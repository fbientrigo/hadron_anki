from __future__ import annotations

from math import gcd, isqrt
from typing import Any, Mapping


def _as_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be an object")
    return value


def _pair_label(pair: Mapping[str, Any]) -> str:
    quark = str(pair.get("quark", "")).strip()
    antiquark = str(pair.get("antiquark", "")).strip()
    if not quark or not antiquark:
        raise ValueError("flavor_superposition pair requires quark and antiquark")
    return f"{quark} {antiquark}bar"


def _lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)


def derive_mass_display(mass_mev_exact: float) -> str:
    if not isinstance(mass_mev_exact, (int, float)) or mass_mev_exact <= 0:
        raise ValueError("mass_mev_exact must be a positive number")
    if mass_mev_exact < 1000:
        rounded = round(mass_mev_exact)
    else:
        rounded = int(round(mass_mev_exact / 10.0) * 10)
    return f"{rounded} MeV"


def derive_mass_bucket(mass_mev_exact: float) -> str:
    if not isinstance(mass_mev_exact, (int, float)) or mass_mev_exact <= 0:
        raise ValueError("mass_mev_exact must be a positive number")
    if mass_mev_exact < 200:
        return "ultralight"
    if mass_mev_exact < 600:
        return "light"
    if mass_mev_exact < 1200:
        return "intermediate"
    return "heavy"


def derive_diagram_mode(record: dict) -> str:
    exact = _as_mapping(record.get("exact"), "exact")
    hadron_type = exact.get("hadron_type")
    quark_model = _as_mapping(exact.get("quark_model"), "exact.quark_model")
    mode = quark_model.get("mode")

    if mode == "flavor_superposition":
        return "flavor_superposition"
    if mode == "simple_valence":
        if hadron_type == "baryon":
            return "simple_triplet"
        if hadron_type == "meson":
            return "simple_pair"
        raise ValueError(f"cannot derive diagram_mode: unknown hadron_type {hadron_type!r}")
    raise ValueError(f"cannot derive diagram_mode: unknown quark_model.mode {mode!r}")


def _factored_superposition_summary(terms: list[Any]) -> str | None:
    parsed_terms: list[tuple[int, int, int, str]] = []
    common_denominator = 1

    for idx, term in enumerate(terms):
        term_map = _as_mapping(term, f"exact.quark_model.terms[{idx}]")
        coefficient = _as_mapping(
            term_map.get("coefficient"), f"exact.quark_model.terms[{idx}].coefficient"
        )
        pair = _as_mapping(term_map.get("pair"), f"exact.quark_model.terms[{idx}].pair")
        label = _pair_label(pair)

        kind = coefficient.get("kind")
        sign = coefficient.get("sign")
        numerator = coefficient.get("numerator")
        denominator = coefficient.get("denominator")
        if kind != "sqrt_fraction":
            return None
        if sign not in {-1, 1}:
            return None
        if not isinstance(numerator, int) or numerator <= 0:
            return None
        if not isinstance(denominator, int) or denominator <= 0:
            return None
        common_denominator = _lcm(common_denominator, denominator)
        parsed_terms.append((sign, numerator, denominator, label))

    if not parsed_terms:
        return None

    factor_denominator: int | None = None
    for scale in range(1, 65):
        candidate = common_denominator * scale
        all_square = True
        for _, numerator, denominator, _ in parsed_terms:
            value = numerator * candidate
            if value % denominator != 0:
                all_square = False
                break
            scaled = value // denominator
            if isqrt(scaled) ** 2 != scaled:
                all_square = False
                break
        if all_square:
            factor_denominator = candidate
            break

    if factor_denominator is None:
        return None

    chunks: list[str] = []
    for idx, (sign, numerator, denominator, label) in enumerate(parsed_terms):
        scaled = (numerator * factor_denominator) // denominator
        magnitude = isqrt(scaled)

        coeff_label = label if magnitude == 1 else f"{magnitude} {label}"
        if idx == 0:
            prefix = "- " if sign < 0 else ""
        else:
            prefix = "- " if sign < 0 else "+ "
        chunks.append(f"{prefix}{coeff_label}")

    expr = " ".join(chunks)
    return f"({expr})/sqrt({factor_denominator})"


def _coefficient_text(coefficient: Mapping[str, Any]) -> tuple[int, str]:
    sign = coefficient.get("sign")
    if sign not in {-1, 1}:
        sign = -1 if str(sign).strip().startswith("-") else 1

    kind = coefficient.get("kind")
    numerator = coefficient.get("numerator")
    denominator = coefficient.get("denominator")
    decimal = coefficient.get("decimal")

    if kind == "sqrt_fraction" and isinstance(numerator, int) and isinstance(denominator, int):
        if numerator == 1:
            return sign, f"1/sqrt({denominator})"
        return sign, f"sqrt({numerator}/{denominator})"
    if kind == "fraction" and isinstance(numerator, int) and isinstance(denominator, int):
        return sign, f"{numerator}/{denominator}"
    if isinstance(decimal, (int, float)):
        return sign, f"{abs(float(decimal)):.6g}"
    return sign, "1"


def _termwise_superposition_summary(terms: list[Any]) -> str:
    chunks: list[str] = []
    for idx, term in enumerate(terms):
        term_map = _as_mapping(term, f"exact.quark_model.terms[{idx}]")
        coefficient = _as_mapping(
            term_map.get("coefficient"), f"exact.quark_model.terms[{idx}].coefficient"
        )
        pair = _as_mapping(term_map.get("pair"), f"exact.quark_model.terms[{idx}].pair")
        label = _pair_label(pair)

        sign, coeff_text = _coefficient_text(coefficient)
        term_text = label if coeff_text == "1" else f"{coeff_text} {label}"
        if idx == 0:
            prefix = "- " if sign < 0 else ""
        else:
            prefix = "- " if sign < 0 else "+ "
        chunks.append(f"{prefix}{term_text}")
    return " ".join(chunks)


def derive_display_quark_summary(record: dict) -> str:
    exact = _as_mapping(record.get("exact"), "exact")
    quark_model = _as_mapping(exact.get("quark_model"), "exact.quark_model")
    mode = quark_model.get("mode")

    if mode == "simple_valence":
        constituents = quark_model.get("constituents")
        if not isinstance(constituents, list) or not constituents:
            raise ValueError("simple_valence requires non-empty constituents")
        tokens: list[str] = []
        for idx, constituent in enumerate(constituents):
            part = _as_mapping(constituent, f"exact.quark_model.constituents[{idx}]")
            quark = str(part.get("quark", "")).strip()
            role = part.get("role")
            if not quark:
                raise ValueError("simple_valence constituent.quark must be non-empty")
            if role == "quark":
                tokens.append(quark)
            elif role == "antiquark":
                tokens.append(f"anti-{quark}")
            else:
                raise ValueError(
                    "simple_valence constituent.role must be one of: {'quark', 'antiquark'}"
                )
        return " ".join(tokens)

    if mode == "flavor_superposition":
        terms = quark_model.get("terms")
        if not isinstance(terms, list) or not terms:
            raise ValueError("flavor_superposition requires non-empty terms")
        return _factored_superposition_summary(terms) or _termwise_superposition_summary(terms)

    raise ValueError(f"cannot derive display_quark_summary: unknown quark_model.mode {mode!r}")


def derive_mass_rank_in_family(records: list[dict]) -> dict[str, int]:
    family_to_records: dict[str, list[dict]] = {}
    for idx, record in enumerate(records):
        record_map = _as_mapping(record, f"records[{idx}]")
        particle_id = record_map.get("id")
        exact = _as_mapping(record_map.get("exact"), f"records[{idx}].exact")
        family = exact.get("family")
        mass = exact.get("mass_mev_exact")

        if not isinstance(particle_id, str) or not particle_id.strip():
            raise ValueError(f"records[{idx}].id must be non-empty string")
        if not isinstance(family, str) or not family.strip():
            raise ValueError(f"records[{idx}].exact.family must be non-empty string")
        if not isinstance(mass, (int, float)) or mass <= 0:
            raise ValueError(f"records[{idx}].exact.mass_mev_exact must be positive number")

        family_to_records.setdefault(family, []).append(record_map)

    ranks: dict[str, int] = {}
    for family_records in family_to_records.values():
        if len(family_records) < 2:
            continue
        ordered = sorted(
            family_records,
            key=lambda item: (float(item["exact"]["mass_mev_exact"]), str(item["id"])),
        )
        for rank, rec in enumerate(ordered, start=1):
            ranks[str(rec["id"])] = rank
    return ranks


def derive_pedagogical_fields(record: dict, family_records: list[dict] | None = None) -> dict:
    record_map = _as_mapping(record, "record")
    exact = _as_mapping(record_map.get("exact"), "exact")

    mass_mev_exact = exact.get("mass_mev_exact")
    if not isinstance(mass_mev_exact, (int, float)) or mass_mev_exact <= 0:
        raise ValueError("exact.mass_mev_exact must be a positive number")

    derived: dict[str, Any] = {
        "mass_display": derive_mass_display(float(mass_mev_exact)),
        "mass_bucket": derive_mass_bucket(float(mass_mev_exact)),
        "diagram_mode": derive_diagram_mode(record_map),
        "display_quark_summary": derive_display_quark_summary(record_map),
    }

    if family_records is not None:
        rank_map = derive_mass_rank_in_family(family_records)
        particle_id = record_map.get("id")
        if particle_id in rank_map:
            derived["mass_rank_in_family"] = rank_map[particle_id]

    return derived


def derive_catalog_pedagogical_fields(records: list[dict]) -> list[dict]:
    family_to_records: dict[str, list[dict]] = {}
    for idx, record in enumerate(records):
        record_map = _as_mapping(record, f"records[{idx}]")
        exact = _as_mapping(record_map.get("exact"), f"records[{idx}].exact")
        family = exact.get("family")
        if not isinstance(family, str) or not family.strip():
            raise ValueError(f"records[{idx}].exact.family must be non-empty string")
        family_to_records.setdefault(family, []).append(record_map)

    enriched: list[dict] = []
    for idx, record in enumerate(records):
        record_map = _as_mapping(record, f"records[{idx}]")
        exact = _as_mapping(record_map.get("exact"), f"records[{idx}].exact")
        family = str(exact["family"])
        family_records = family_to_records[family]
        out = dict(record_map)
        out["pedagogical"] = derive_pedagogical_fields(record_map, family_records=family_records)
        enriched.append(out)
    return enriched
