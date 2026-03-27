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

