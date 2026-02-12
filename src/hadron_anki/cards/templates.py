from hadron_anki.domain.spec import ParticleSpec

def front_html(media_filename: str) -> str:
    raise NotImplementedError("front_html is not implemented")

def back_html(spec: ParticleSpec) -> str:
    raise NotImplementedError("back_html is not implemented")
