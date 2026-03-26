import sys

from hadron_anki.catalog.loader import load_catalog
from hadron_anki.catalog.bootstrap_particle import enrich_particle_metadata

def main():
    if len(sys.argv) > 1:
        catalog_path = sys.argv[1]
    else:
        catalog_path = "catalogs/core_particles.yaml"
        
    try:
        catalog = load_catalog(catalog_path)
    except Exception as e:
        print(f"Error loading catalog: {e}")
        return

    particles = catalog.get("particles", [])
    print(f"Loaded {len(particles)} particles from {catalog_path}")
    
    baryons = [p for p in particles if p.get('type') == 'baryon']
    mesons = [p for p in particles if p.get('type') == 'meson']
    
    print(f"Baryons: {len(baryons)}")
    print(f"Mesons: {len(mesons)}")
    print("\nParticle IDs:")
    for p in particles:
        print(f"  - {p['id']}")
    
    print("\nAttempting to enrich a few particles...")
    for p in particles[:3]:
        # Basic hardcoded maps for testing the enrichment
        pdg_name = None
        if p["id"] == "proton": pdg_name = "p"
        elif p["id"] == "neutron": pdg_name = "n"
        elif p["id"] == "pi_plus": pdg_name = "pi+"
        
        try:
            enriched = enrich_particle_metadata(p, pdg_name=pdg_name)
            print(f"  Enriched {p['id']}: pdg_id={enriched.get('pdg_id')}, mass={enriched.get('mass')}")
        except ImportError as e:
            print(f"  Skipping enrichment: {e}")
            break

if __name__ == "__main__":
    main()
