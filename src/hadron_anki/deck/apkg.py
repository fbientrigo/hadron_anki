def build_apkg(catalog: dict, out_path: str, template_version: str, model_version: str) -> None:
    """
    Build an Anki .apkg file from a particle catalog.
    
    Args:
        catalog: Dictionary containing particle data.
        out_path: Destination path for the .apkg file.
        template_version: Version of the card template.
        model_version: Version of the Anki note model.
    """
    raise NotImplementedError("build_apkg is not implemented")
