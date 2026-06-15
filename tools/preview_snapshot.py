"""
Curated card-preview snapshot generator.

Builds a small, self-explanatory gallery (~8 particles) that shows the five
pedagogical concepts of a card — octet/multiplet, mass, composition, decay and
Feynman diagram — so reviewers can see "how cards are generated" and check the
state at a glance, without rebuilding the whole deck.

It reuses the exact same renderers as the full build (`generate_preview` /
`generate_feynman_preview`); the only difference is that it feeds them a curated
subset of specs. Run from the repo root:

    python tools/preview_snapshot.py --out site
"""
import argparse
import sys

from hadron_anki.catalog.loader import load_catalog
from hadron_anki.catalog.canonical_loader import load_canonical_catalog
from hadron_anki.catalog.build import build_specs
from hadron_anki.preview.generator import generate_preview, generate_feynman_preview

CANONICAL_CATALOG = "catalogs/core_particles.canonical.yaml"
DECAYS_CATALOG = "catalogs/core_decays.yaml"

# Same set the full deck builds, kept here so the snapshot mirrors a real card.
CARD_TYPES = ["summary", "composition", "identity", "mass", "decay"]

# Curated subset: covers the three multiplets and the pedagogical edge cases.
#   proton, neutron     -> baryon_octet (neutron has a hand-made W decay)
#   lambda_0, sigma_plus -> baryon_octet (strangeness)
#   omega_minus         -> baryon_decuplet
#   pi_plus, k_plus     -> pseudoscalar_nonet, weak decay via W
#   pi_zero             -> pseudoscalar_nonet, flavour superposition
CURATED_IDS = [
    "proton",
    "neutron",
    "lambda_0",
    "sigma_plus",
    "omega_minus",
    "pi_plus",
    "pi_zero",
    "k_plus",
]


def select_curated(specs):
    """Return specs whose id is in CURATED_IDS, preserving CURATED_IDS order."""
    by_id = {spec.id: spec for spec in specs}
    selected = []
    for pid in CURATED_IDS:
        spec = by_id.get(pid)
        if spec is None:
            print(f"WARNING: curated id '{pid}' not found in catalog", file=sys.stderr)
            continue
        selected.append(spec)
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default="site",
        help="Output directory for the curated gallery (default: site)",
    )
    args = parser.parse_args()

    canonical = load_canonical_catalog(CANONICAL_CATALOG)
    decays_by_id = load_catalog(DECAYS_CATALOG)
    specs = build_specs(canonical, decays_by_id)

    curated = select_curated(specs)
    if not curated:
        print("ERROR: no curated particles resolved; aborting.", file=sys.stderr)
        return 1

    # Feynman previews for the curated particles that actually decay.
    feynman_decays = [
        {
            "id": f"{spec.id}_decay",
            "label": f"{spec.name} decay",
            "decay_diagram": spec.decay_diagram,
        }
        for spec in curated
        if spec.decay_diagram
    ]
    feynman_html = generate_feynman_preview(feynman_decays, args.out)

    generate_preview(
        curated,
        args.out,
        card_types=CARD_TYPES,
        feynman_html=feynman_html,
    )

    # Summary for the CI step summary / local sanity check.
    from pathlib import Path

    svg_count = len(list(Path(args.out).rglob("*.svg")))
    print(f"Curated snapshot written to {args.out}/index.html")
    print(f"  particles: {len(curated)} ({', '.join(s.id for s in curated)})")
    print(f"  feynman diagrams: {len(feynman_decays)}")
    print(f"  svg files: {svg_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
