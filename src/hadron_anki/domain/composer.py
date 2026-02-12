from hadron_anki.domain.spec import ParticleSpec

def normalize_quark_token(token: str) -> str:
    """
    Normalizes quark/antiquark tokens to canonical form.
    Canonical form uses 'anti-' prefix for antiquarks (e.g., 'anti-u').
    """
    raise NotImplementedError()

def validate_quark_count(spec: ParticleSpec) -> None:
    """
    Validates that the number of quarks matches the particle type.
    - baryon: 3 quarks
    - meson: 2 quarks
    
    Raises:
        ValueError: If quark count is invalid for the type.
    """
    raise NotImplementedError()
