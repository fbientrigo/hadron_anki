from typing import Any

def enrich_particle_metadata(particle: dict[str, Any], pdg_name: str = None) -> dict[str, Any]:
    """
    Enrich a particle dictionary with metadata from the Scikit-HEP 'particle' package.
    
    Args:
        particle: The basic dictionary with at least 'id', 'name', 'type', 'quarks'.
        pdg_name: The name to look up in the particle package (e.g. 'p', 'pi+', 'K-').
                  If not provided, tries to guess from 'name'.
                  
    Returns:
        A new combined dictionary. If particle is not found, returns the original metadata unchanged.
    """
    try:
        from particle import Particle, ParticleNotFound
    except ImportError:
        raise ImportError(
            "The 'particle' package is required for catalog bootstrapping. "
            "Install it via `pip install particle`."
        )

    res = dict(particle)
    name_to_search = pdg_name if pdg_name else res.get("name")
    
    try:
        # Simplistic find
        found = Particle.findall(name=name_to_search)
        if not found and pdg_name:
            # Let's try exact string matching in names if findall fails
            pass
            
        if found:
            # Use the first match
            p = found[0]
            if p.pdgid:
                res["pdg_id"] = int(p.pdgid)
            if p.mass is not None:
                res["mass"] = float(p.mass)
            # Maybe aliases from p.name
            if p.name and "aliases" not in res:
                res["aliases"] = [p.name]
                
    except Exception:
        pass  # Fail gracefully on lookup
        
    return res
