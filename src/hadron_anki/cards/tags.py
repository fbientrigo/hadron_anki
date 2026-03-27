from hadron_anki.domain.spec import ParticleSpec

def build_tags(spec: ParticleSpec, card_type: str) -> list[str]:
    """
    Build a deterministic list of tags for an Anki card.
    """
    tags = set()
    
    # Base structured tags
    tags.add("source:core")
    tags.add("difficulty:basic")
    
    # Particle type
    if spec.type:
        tags.add(f"particle:{spec.type}")
        
    # Quark content
    for q in set(spec.quarks):
        tags.add(f"quark:{q}")
        
    return sorted(list(tags))
