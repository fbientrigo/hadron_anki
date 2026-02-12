from hadron_anki.domain.spec import ParticleSpec

def front_html(media_filename: str) -> str:
    return f'<img src="{media_filename}">' 

def back_html(spec: ParticleSpec) -> str:
    quarks_str = ", ".join(spec.quarks)
    return (
        "<div>"
        f"<div>{spec.name}</div>"
        f"<div>{spec.id}</div>"
        f"<div>{quarks_str}</div>"
        "</div>"
    )
