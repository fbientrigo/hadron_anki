def stable_note_guid(particle_id: str, template_version: str, model_version: str) -> str:
    """
    Generate a deterministic ID for an Anki note.
    
    Args:
        particle_id: Unique identifier for the particle.
        template_version: Version of the card template.
        model_version: Version of the Anki note model.
        
    Returns:
        A deterministic lowercase ASCII hex string.
    """
    raise NotImplementedError("stable_note_guid is not implemented")
