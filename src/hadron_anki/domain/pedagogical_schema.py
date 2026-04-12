"""Minimal typed contract for canonical hadron schema (V1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, NotRequired, TypeAlias, TypedDict


QuarkFlavor = Literal["u", "d", "s", "c", "b", "t"]
ConstituentRole = Literal["quark", "antiquark"]
HadronType = Literal["baryon", "meson"]
DiagramMode = Literal["simple_pair", "simple_triplet", "flavor_superposition"]
MassBucket = Literal["ultralight", "light", "intermediate", "heavy"]
CoefficientKind = Literal["sqrt_fraction", "fraction", "decimal"]


@dataclass(frozen=True)
class QuantumNumbers:
    jp: str
    isospin_i: str
    isospin_i3: str
    charge: int
    strangeness: int
    charm: int
    bottomness: int


@dataclass(frozen=True)
class ValenceConstituent:
    quark: QuarkFlavor
    role: ConstituentRole


@dataclass(frozen=True)
class SuperpositionCoefficient:
    sign: Literal[-1, 1]
    kind: CoefficientKind
    numerator: int | None = None
    denominator: int | None = None
    decimal: float | None = None


@dataclass(frozen=True)
class QuarkPairTerm:
    quark: QuarkFlavor
    antiquark: QuarkFlavor


@dataclass(frozen=True)
class FlavorSuperpositionTerm:
    coefficient: SuperpositionCoefficient
    pair: QuarkPairTerm


@dataclass(frozen=True)
class SimpleValenceModel:
    mode: Literal["simple_valence"]
    constituents: tuple[ValenceConstituent, ...]


@dataclass(frozen=True)
class FlavorSuperpositionModel:
    mode: Literal["flavor_superposition"]
    terms: tuple[FlavorSuperpositionTerm, ...]
    basis: str = "quark_antiquark_flavor"
    normalized: bool = True
    latex: str | None = None


QuarkModel = SimpleValenceModel | FlavorSuperpositionModel


@dataclass(frozen=True)
class ExactParticleData:
    id: str
    name: str
    symbol: str
    hadron_type: HadronType
    family: str
    multiplet: str
    quark_model: QuarkModel
    mass_mev_exact: float
    quantum_numbers: QuantumNumbers


@dataclass(frozen=True)
class PedagogicalDerivedData:
    mass_display: str
    mass_bucket: MassBucket
    diagram_mode: DiagramMode
    display_quark_summary: str
    mass_rank_in_family: int | None = None


@dataclass(frozen=True)
class PedagogicalParticleRecord:
    id: str
    exact: ExactParticleData
    pedagogical: PedagogicalDerivedData | None = None


CanonicalParticle: TypeAlias = dict[str, Any]


class DerivedPedagogicalBlock(TypedDict):
    mass_display: str
    mass_bucket: MassBucket
    diagram_mode: DiagramMode
    display_quark_summary: str
    mass_rank_in_family: NotRequired[int]
