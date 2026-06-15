from dataclasses import dataclass
from typing import Optional

@dataclass
class ParticleSpec:
    id: str
    name: str
    type: str
    quarks: list[str]
    symbol: Optional[str] = None
    symbol_tex: Optional[str] = None
    pdg_id: Optional[int] = None
    aliases: Optional[list[str]] = None
    mass: Optional[float] = None
    decay_diagram: Optional[dict] = None
    decay_label: Optional[str] = None
    # Canonical/pedagogical enrichments (optional so legacy callers stay valid).
    multiplet: Optional[str] = None
    mass_summary: Optional[str] = None
    display_quark_summary: Optional[str] = None
    diagram_mode: Optional[str] = None
    decay: Optional[dict] = None

