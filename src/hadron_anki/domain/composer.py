from hadron_anki.domain.spec import ParticleSpec

_KNOWN_QUARKS = {"u", "d", "s", "c", "b", "t"}

def normalize_quark_token(token: str) -> str:
    """
    Normalizes quark/antiquark tokens to canonical form.
    Canonical form uses 'anti-' prefix for antiquarks (e.g., 'anti-u').
    """
    token = token.strip()
    if token.startswith("anti-"):
        return token

    if token.endswith("bar"):
        base = token[: -len("bar")]
        if base in _KNOWN_QUARKS:
            return f"anti-{base}"

    return token

def validate_quark_count(spec: ParticleSpec) -> None:
    """
    Validates that the number of quarks matches the particle type.
    - baryon: 3 quarks
    - meson: 2 quarks
    
    Raises:
        ValueError: If quark count is invalid for the type.
    """
    if spec.type == "baryon" and len(spec.quarks) != 3:
        raise ValueError("baryon must have 3 quarks")
    if spec.type == "meson" and len(spec.quarks) != 2:
        raise ValueError("meson must have 2 quarks")
