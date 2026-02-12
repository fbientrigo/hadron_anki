from dataclasses import dataclass

@dataclass
class ParticleSpec:
    id: str
    name: str
    type: str
    quarks: list[str]
