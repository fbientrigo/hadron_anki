import os

from hadron_anki.catalog.loader import load_catalog
from hadron_anki.catalog.canonical_loader import load_canonical_catalog
from hadron_anki.catalog.build import build_specs
from hadron_anki.deck.apkg import build_apkg
from hadron_anki.preview.generator import generate_preview, generate_feynman_preview
from hadron_anki.render.math_labels import generate_math_label_preview

# --- CONFIGURATION ---
# "summary" is the big descriptive card (octet + mass + composition + decay + Feynman).
# The per-concept types stay available so the summary can be split apart later.
CARD_TYPES = ["summary", "composition", "identity", "mass", "decay"]

CANONICAL_CATALOG = "catalogs/core_particles.canonical.yaml"
DECAYS_CATALOG = "catalogs/core_decays.yaml"


def main():
    out_dir = "decks"
    os.makedirs(out_dir, exist_ok=True)
    out_apkg = os.path.join(out_dir, "hadron_core.apkg")

    deck_name = "Hadron Anki::Core Particles"
    preview_dir = "_preview_out"

    # 1. Load canonical particles + decay data, then assemble display-ready specs.
    canonical = load_canonical_catalog(CANONICAL_CATALOG)
    decays_by_id = load_catalog(DECAYS_CATALOG)
    specs = build_specs(canonical, decays_by_id)

    # 2. Build the combined deck.
    print(f"Building full deck ({len(specs)} particles) to {out_apkg}...")
    build_apkg(
        specs=specs,
        out_path=out_apkg,
        deck_name=deck_name,
        template_version="v3.0-canonical",
        model_version="v3.0-canonical",
        card_types=CARD_TYPES,
    )

    # 3. Build modular decks, one card type per deck.
    for ctype in CARD_TYPES:
        modular_apkg = os.path.join(out_dir, f"hadron_{ctype}.apkg")
        modular_deck = f"Hadron Anki::{ctype.capitalize()}"
        print(f"Building modular deck to {modular_apkg}...")
        build_apkg(
            specs=specs,
            out_path=modular_apkg,
            deck_name=modular_deck,
            template_version=f"v3.0-canonical-{ctype}",
            model_version=f"v3.0-canonical-{ctype}",
            card_types=[ctype],
        )

    # 4. Feynman diagram previews (from the same specs).
    feynman_decays = [
        {
            "id": f"{spec.id}_decay",
            "label": f"{spec.name} decay",
            "decay_diagram": spec.decay_diagram,
        }
        for spec in specs
        if spec.decay_diagram
    ]
    print("Generating Feynman diagram previews...")
    feynman_html = generate_feynman_preview(feynman_decays, preview_dir)

    # 5. HTML preview gallery (includes the summary card).
    print(f"Generating HTML preview gallery to {preview_dir}...")
    generate_preview(
        specs,
        preview_dir,
        card_types=CARD_TYPES,
        feynman_html=feynman_html,
    )

    # 6. Math label preview.
    math_label_exprs = [
        r"\pi^+", r"\pi^-", r"\pi^0",
        r"\mu^+", r"\nu_\mu",
        r"\bar{\nu}_e",
        r"\Sigma^+", r"\Omega^-",
        r"\Lambda^0", r"K^+",
    ]
    math_label_dir = f"{preview_dir}/math_labels"
    print(f"Generating math label preview to {math_label_dir}...")
    generate_math_label_preview(math_label_exprs, math_label_dir)

    print("Done. Check the 'decks/' folder for the generated packages.")


if __name__ == "__main__":
    main()
