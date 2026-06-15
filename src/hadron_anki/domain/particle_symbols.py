"""
Display symbols for particles, keyed by repo ID.

Shared by card rendering (decay text like "64% -> p + pi-") and by the
generated Feynman diagram labels, so both stay consistent. IDs not in the
table fall back to the raw ID, which keeps rendering safe for new particles.
"""

PARTICLE_DISPLAY_SYMBOLS: dict[str, str] = {
    # Baryons
    "proton": "p",
    "neutron": "n",
    "lambda_0": "Λ⁰",     # Λ⁰
    "sigma_plus": "Σ⁺",   # Σ⁺
    "sigma_zero": "Σ⁰",   # Σ⁰
    "sigma_minus": "Σ⁻",  # Σ⁻
    "xi_zero": "Ξ⁰",      # Ξ⁰
    "xi_minus": "Ξ⁻",     # Ξ⁻
    "omega_minus": "Ω⁻",  # Ω⁻
    # Mesons
    "pi_plus": "π⁺",      # π⁺
    "pi_minus": "π⁻",     # π⁻
    "pi_zero": "π⁰",      # π⁰
    "k_plus": "K⁺",            # K⁺
    "k_minus": "K⁻",           # K⁻
    "k_zero": "K⁰",            # K⁰
    # Leptons and photon (decay products)
    "mu_plus": "μ⁺",      # μ⁺
    "mu_minus": "μ⁻",     # μ⁻
    "e_plus": "e⁺",            # e⁺
    "e_minus": "e⁻",           # e⁻
    "nu_mu": "ν_μ",       # ν_μ
    "nu_e": "ν_e",             # ν_e
    "anti_nu_mu": "ν̄_μ",  # ν̄_μ
    "anti_nu_e": "ν̄_e",        # ν̄_e
    "nubar_e": "ν̄_e",          # ν̄_e (PDG-bootstrap spelling)
    "nubar_mu": "ν̄_μ",    # ν̄_μ
    "gamma": "γ",              # γ
}


def display_symbol(particle_id: str) -> str:
    """Return the display symbol for a particle ID, or the ID itself if unknown."""
    return PARTICLE_DISPLAY_SYMBOLS.get(particle_id, particle_id)
