import sys

from hadron_anki.catalog.loader import load_catalog
from hadron_anki.catalog.bootstrap_particle import enrich_particle_metadata
from hadron_anki.deck.apkg import build_apkg
from hadron_anki.preview.generator import generate_preview

def main():
    catalog_path = "catalogs/core_particles.yaml"
    out_apkg = "hadron_core.apkg"
    preview_dir = "_preview_out"
    
    # 1. Load catalog
    catalog = load_catalog(catalog_path)
    particles = catalog.get("particles", [])
    
    # 2. Enrich with 'particle'
    enriched_particles = []
    print("Enriching particles with PDG metadata...")
    for p in particles:
        # We can map some explicitly if needed, but let's try the simple map
        pdg_name = None
        if p["id"] == "proton": pdg_name = "p"
        elif p["id"] == "neutron": pdg_name = "n"
        elif p["id"] == "pi_plus": pdg_name = "pi+"
        elif p["id"] == "pi_minus": pdg_name = "pi-"
        elif p["id"] == "pi_zero": pdg_name = "pi0"
        elif p["id"] == "k_plus": pdg_name = "K+"
        elif p["id"] == "k_minus": pdg_name = "K-"
        elif p["id"] == "k_zero": pdg_name = "K0"
        elif p["id"] == "lambda_0": pdg_name = "Lambda"
        elif p["id"] == "sigma_plus": pdg_name = "Sigma+"
        elif p["id"] == "sigma_zero": pdg_name = "Sigma0"
        elif p["id"] == "sigma_minus": pdg_name = "Sigma-"
        elif p["id"] == "xi_zero": pdg_name = "Xi0"
        elif p["id"] == "xi_minus": pdg_name = "Xi-"
        elif p["id"] == "omega_minus": pdg_name = "Omega-"
        
        try:
            enriched = enrich_particle_metadata(p, pdg_name=pdg_name)
        except ImportError:
            enriched = p
            print("Note: 'particle' package not found, skipping enrichment.")
        enriched_particles.append(enriched)

    catalog["particles"] = enriched_particles
    
    # 3. Build Deck
    print(f"Building deck ({len(enriched_particles)} particles) to {out_apkg}...")
    build_apkg(catalog, out_apkg, template_version="2.0.0", model_version="v2")
    
    # 4. Generate visual HTML preview
    from hadron_anki.deck.apkg import _particle_spec_from_mapping
    specs = [_particle_spec_from_mapping(p) for p in enriched_particles]
    print(f"Generating HTML preview gallery to {preview_dir}...")
    generate_preview(specs, preview_dir)
    
    print("Done. Import hadron_core.apkg into Anki to verify.")

if __name__ == "__main__":
    main()
