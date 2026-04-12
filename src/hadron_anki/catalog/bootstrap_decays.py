"""
Decay bootstrap module.

Programmatically extracts dominant decay modes for the core particle catalog
using the PDG Python API (pdg package) as the primary data source.

Source priority:
  1. PDG Python API (pdg package, SQLite-backed, offline after install)
  2. If unavailable, raises ImportError with clear guidance.

This module is NOT responsible for diagram generation or routing.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# ── Name normalization table ────────────────────────────────────────────────

# Maps PDG particle names to our repo snake_case IDs.
_PDG_TO_REPO: dict[str, str] = {
    # Stable / long-lived hadrons
    "p":          "proton",
    "n":          "neutron",
    # Pions
    "pi+":        "pi_plus",
    "pi-":        "pi_minus",
    "pi0":        "pi_zero",
    # Kaons
    "K+":         "k_plus",
    "K-":         "k_minus",
    "K0":         "k_zero",
    "K0bar":      "k_zero",           # same physical particle for our scope
    "K_S0":       "k_zero",
    "K_L0":       "k_zero",
    # Strange baryons
    "Lambda":     "lambda_0",
    "Lambda0":    "lambda_0",
    "Sigma+":     "sigma_plus",
    "Sigma0":     "sigma_zero",
    "Sigma-":     "sigma_minus",
    "Xi0":        "xi_zero",
    "Xi-":        "xi_minus",
    "Omega-":     "omega_minus",
    # Leptons
    "e+":         "e_plus",
    "e-":         "e_minus",
    "mu+":        "mu_plus",
    "mu-":        "mu_minus",
    "nu_e":       "nu_e",
    "nu_mu":      "nu_mu",
    "nu_tau":     "nu_tau",
    "nu_ebar":    "anti_nu_e",
    "nu_mubar":   "anti_nu_mu",
    "nu_taubar":  "anti_nu_tau",
    # Photon
    "gamma":      "gamma",
}

# Stability threshold: ctau > this value (mm) → treated as effectively stable
# The proton is infinite; neutron ~2.6e14 mm is not stable for educational purposes.
# We only mark infinite (proton) as stable.
_STABLE_CTAU_THRESHOLD_MM = float("inf")


def normalize_pdg_name(pdg_name: str) -> str:
    """
    Convert a PDG particle name to a repo-safe snake_case ID.

    Falls back to lowercasing and replacing special characters when
    no explicit mapping exists.
    """
    if pdg_name in _PDG_TO_REPO:
        return _PDG_TO_REPO[pdg_name]

    # Generic fallback: lowercase, replace +/-/() with words
    name = pdg_name
    name = name.replace("+", "_plus").replace("-", "_minus")
    name = name.replace("(", "").replace(")", "").replace(" ", "_")
    name = name.lower()
    return name


def is_effectively_stable(particle_data: dict) -> bool:
    """
    Determine whether a particle should be considered stable for deck purposes.

    A particle is stable if its ctau is infinite (proton).
    All other particles — including the very long-lived neutron — are unstable.
    """
    ctau = particle_data.get("ctau_mm", 0.0)
    return ctau == float("inf")


@dataclass
class DecayRecord:
    """Dominant decay information for a single particle."""
    parent: str                        # repo ID (e.g. "pi_plus")
    children: list[str]               # repo IDs of decay products
    branching_ratio: float            # fraction in [0, 1]
    description: str                  # raw PDG description string
    source: str                       # e.g. "PDG Python API 2025"
    source_kind: str                  # "pdg_python_api" | "fixture" | "manual"


def parse_dominant_decay(
    repo_id: str,
    particle_data: dict,
    source: str = "fixture",
    source_kind: str = "fixture",
) -> Optional[DecayRecord]:
    """
    Extract the dominant (highest branching ratio) decay mode from particle_data.

    particle_data format:
      {
        "pdg_name": str,
        "ctau_mm": float,
        "branching_fractions": [
          {
            "description": str,
            "value": float | None,
            "is_limit": bool,
            "decay_products": [str, ...]   # PDG names
          }, ...
        ]
      }

    Returns None if the particle is stable or has no decay data.
    """
    if is_effectively_stable(particle_data):
        return None

    bfs = particle_data.get("branching_fractions", [])
    # Filter: must have a real (non-limit) numeric value
    valid = [
        bf for bf in bfs
        if not bf.get("is_limit", False)
    ]
    if not valid:
        return None

    # For modes with no value (e.g. neutron, Sigma0), treat as exclusive (value ≈ 1)
    def _bf_value(bf: dict) -> float:
        return bf["value"] if bf.get("value") is not None else 1.0

    # Dominant = highest branching ratio
    dominant = max(valid, key=_bf_value)
    dominant_value = _bf_value(dominant)

    children_repo = [
        normalize_pdg_name(p) for p in dominant.get("decay_products", [])
    ]

    return DecayRecord(
        parent=repo_id,
        children=children_repo,
        branching_ratio=dominant_value,
        description=dominant["description"],
        source=source,
        source_kind=source_kind,
    )


# ── PDG Python API fetch layer ──────────────────────────────────────────────

# Map from repo particle ID to PDG API name(s) to try
_REPO_TO_PDG_NAMES: dict[str, list[str]] = {
    "proton":      ["p"],
    "neutron":     ["n"],
    "pi_plus":     ["pi+"],
    "pi_minus":    ["pi-"],
    "pi_zero":     ["pi0"],
    "k_plus":      ["K+"],
    "k_minus":     ["K-"],
    "k_zero":      ["K(S)0", "K0S", "KS"],   # K_S0 = MC 310
    "lambda_0":    ["Lambda"],               # try mcid=3122 fallback
    "sigma_plus":  ["Sigma+"],
    "sigma_zero":  ["Sigma0"],
    "sigma_minus": ["Sigma-"],
    "xi_zero":     ["Xi0"],
    "xi_minus":    ["Xi-"],
    "omega_minus": ["Omega-"],
}

# MC IDs for particles where name lookup is unreliable
_REPO_TO_MCID: dict[str, int] = {
    "k_zero":     310,    # K_S0
    "lambda_0":   3122,
    "sigma_zero": 3212,
}


def fetch_particle_data_pdg(repo_id: str) -> dict:
    """
    Fetch particle data from the PDG Python API.

    Raises ImportError if pdg is not installed.
    Raises ValueError if the particle cannot be found.
    """
    try:
        import pdg as pdgapi
    except ImportError as exc:
        raise ImportError(
            "PDG Python API not installed. Run: pip install pdg"
        ) from exc

    api = pdgapi.connect()

    pdg_names = _REPO_TO_PDG_NAMES.get(repo_id, [])
    particle = None
    for name in pdg_names:
        try:
            particle = api.get_particle_by_name(name)
            break
        except Exception:
            continue

    # Fallback to mcid lookup for particles with non-unique name
    if particle is None and repo_id in _REPO_TO_MCID:
        try:
            particle = api.get_particle_by_mcid(_REPO_TO_MCID[repo_id])
        except Exception:
            pass

    if particle is None:
        raise ValueError(f"Could not find PDG particle for repo_id={repo_id!r}")

    # ctau from the `particle` scikit-hep package for stability check
    try:
        from particle import Particle as SkhepParticle
        sk = SkhepParticle.from_name(pdg_names[0])
        ctau_mm = float(sk.ctau) if sk.ctau is not None else 0.0
    except Exception:
        ctau_mm = 0.0

    # Branching fractions
    bfs_raw = []
    try:
        for bf in particle.exclusive_branching_fractions():
            try:
                products = [p.item.name for p in bf.decay_products]
                bfs_raw.append({
                    "description": bf.description,
                    "value": bf.value,
                    "is_limit": bool(bf.is_limit),
                    "decay_products": products,
                })
            except Exception:
                continue
    except Exception:
        pass

    return {
        "pdg_name": pdg_names[0] if pdg_names else repo_id,
        "ctau_mm": ctau_mm,
        "branching_fractions": bfs_raw,
    }


def bootstrap_all_decays(repo_ids: list[str]) -> dict[str, dict]:
    """
    Fetch and parse dominant decays for all given repo particle IDs.

    Returns a dict keyed by repo_id with the following structure:
      {
        "stable": bool,
        "main_decay": DecayRecord | None,
        "raw_bf_count": int,
        "source_kind": str,
      }
    """
    results = {}
    for repo_id in repo_ids:
        try:
            data = fetch_particle_data_pdg(repo_id)
            source = "PDG Python API 2025"
            source_kind = "pdg_python_api"
        except Exception as exc:
            print(f"  [{repo_id}] fetch failed: {exc}")
            data = {"pdg_name": repo_id, "ctau_mm": 0.0, "branching_fractions": []}
            source = "unknown"
            source_kind = "unknown"

        stable = is_effectively_stable(data)
        decay_record = None
        if not stable:
            decay_record = parse_dominant_decay(
                repo_id, data, source=source, source_kind=source_kind
            )

        results[repo_id] = {
            "stable": stable,
            "main_decay": decay_record,
            "raw_bf_count": len(data.get("branching_fractions", [])),
            "source_kind": source_kind,
        }

    return results
