import os
from hadron_anki.catalog.loader import load_catalog
from hadron_anki.catalog.bootstrap_particle import enrich_particle_metadata
from hadron_anki.deck.apkg import build_apkg
from hadron_anki.preview.generator import generate_preview, generate_feynman_preview
from hadron_anki.render.math_labels import generate_math_label_preview

# --- CONFIGURATION ---
# Options: "mass", "composition", "identity", "decay"
# Set to None for all types.
CARD_TYPES = ["composition", "identity", "mass", "decay"] 

def main():
    catalog_path = "catalogs/core_particles.yaml"
    out_dir = "decks"
    os.makedirs(out_dir, exist_ok=True)
    out_apkg = os.path.join(out_dir, "hadron_core.apkg")
    
    deck_name = "Hadron Anki::Core Particles"
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
    
    # 3. Build Deck (Combined)
    print(f"Building full deck ({len(enriched_particles)} particles) to {out_apkg}...")
    build_apkg(
        catalog, 
        out_apkg, 
        deck_name=deck_name,
        template_version="v2.2-stable", 
        model_version="v2.2-stable",
        card_types=CARD_TYPES
    )

    # 4. Build Modular Decks (Mass, Composition, Identity)
    for ctype in CARD_TYPES:
        modular_apkg = os.path.join(out_dir, f"hadron_{ctype}.apkg")
        modular_deck = f"Hadron Anki::{ctype.capitalize()}"
        print(f"Building modular deck to {modular_apkg}...")
        build_apkg(
            catalog,
            modular_apkg,
            deck_name=modular_deck,
            template_version=f"v2.2-stable-{ctype}",
            model_version=f"v2.2-stable-{ctype}",
            card_types=[ctype]
        )

    from hadron_anki.deck.apkg import _particle_spec_from_mapping
    specs = [_particle_spec_from_mapping(p) for p in enriched_particles]
    
    # 5. Feynman diagrams preview
    # 5. Feynman diagrams preview (from loaded catalog)
    feynman_decays = []
    for p in enriched_particles:
        if p.get("decay_diagram"):
            feynman_decays.append({
                "id": p["id"] + "_decay",
                "label": p.get("decay_label", f"{p['name']} Decay"),
                "decay_diagram": p["decay_diagram"]
            })
    print("Generating Feynman diagram previews...")
    feynman_html = generate_feynman_preview(feynman_decays, preview_dir)

    print(f"Generating HTML preview gallery to {preview_dir}...")
    generate_preview(
        specs,
        preview_dir,
        card_types=CARD_TYPES,
        feynman_html=feynman_html
    )

    # 6. Math label preview
    MATH_LABEL_EXPRS = [
        r"\pi^+", r"\pi^-", r"\pi^0",
        r"\mu^+", r"\nu_\mu",
        r"\bar{\nu}_e",
        r"\Sigma^+", r"\Omega^-",
        r"\Lambda^0", r"K^+",
    ]
    math_label_dir = f"{preview_dir}/math_labels"
    print(f"Generating math label preview to {math_label_dir}...")
    generate_math_label_preview(MATH_LABEL_EXPRS, math_label_dir)

    print("Done. Check the 'decks/' folder for the generated packages.")

if __name__ == "__main__":
    main()
