"""
Assemble display-ready ParticleSpec objects from the canonical catalog.

This is the orchestration seam between data and rendering: it bridges a
canonical particle record (via the legacy adapter) with decay data
(``core_decays.yaml``) and resolves a Feynman diagram for the main decay,
preferring a hand-authored ``decay_diagram`` over the generated fallback.
"""
from __future__ import annotations

from typing import Any, Optional

from hadron_anki.domain.legacy_adapter import canonical_to_legacy_particlespec
from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.render.decay_diagram import build_decay_diagram


def build_particle_spec(
    record: dict[str, Any],
    decays_by_id: Optional[dict[str, Any]] = None,
) -> ParticleSpec:
    """Build a full ParticleSpec from a canonical record plus decay data."""
    spec = canonical_to_legacy_particlespec(record)

    entry = (decays_by_id or {}).get(spec.id)
    if entry and not entry.get("stable") and entry.get("main_decay"):
        main_decay = entry["main_decay"]
        spec.decay = {
            "branching_ratio": main_decay.get("branching_ratio"),
            "children": list(main_decay.get("children") or []),
            "description": main_decay.get("description"),
        }

    override = record.get("decay_diagram")
    if override:
        spec.decay_diagram = override
    elif spec.decay:
        spec.decay_diagram = build_decay_diagram(spec, spec.decay)

    return spec


def build_specs(
    canonical_catalog: dict[str, Any],
    decays_by_id: Optional[dict[str, Any]] = None,
) -> list[ParticleSpec]:
    """Build ParticleSpecs for every particle in a canonical catalog."""
    particles = canonical_catalog.get("particles") or []
    return [build_particle_spec(record, decays_by_id) for record in particles]
