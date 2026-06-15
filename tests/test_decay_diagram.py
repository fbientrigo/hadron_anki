"""Tests for the generated decay diagram fallback."""
from hadron_anki.domain.spec import ParticleSpec
from hadron_anki.render.decay_diagram import build_decay_diagram
from hadron_anki.render.feynman import render_feynman_svg


def test_generates_one_vertex_topology_for_baryon():
    spec = ParticleSpec(id="lambda_0", name="Lambda", type="baryon", quarks=["u", "d", "s"])
    decay = {"children": ["proton", "pi_minus"]}

    diagram = build_decay_diagram(spec, decay)

    node_ids = {n["id"] for n in diagram["nodes"]}
    assert node_ids == {"in", "v", "out1", "out2"}
    # baryon initial line is a fermion; meson would be scalar
    in_edge = next(e for e in diagram["edges"] if e["from"] == "in")
    assert in_edge["type"] == "fermion"
    # children become outgoing fermion edges labelled with display symbols
    out_labels = sorted(e["label"] for e in diagram["edges"] if e["from"] == "v")
    assert out_labels == sorted(["p", "π⁻"])


def test_meson_initial_edge_is_scalar():
    spec = ParticleSpec(id="pi_zero", name="Pion Zero", type="meson", quarks=[])
    diagram = build_decay_diagram(spec, {"children": ["gamma", "gamma"]})
    in_edge = next(e for e in diagram["edges"] if e["from"] == "in")
    assert in_edge["type"] == "scalar"


def test_returns_none_without_children():
    spec = ParticleSpec(id="proton", name="Proton", type="baryon", quarks=["u", "u", "d"])
    assert build_decay_diagram(spec, {"children": []}) is None


def test_generated_diagram_renders_to_svg():
    spec = ParticleSpec(id="omega_minus", name="Omega", type="baryon", quarks=["s", "s", "s"])
    diagram = build_decay_diagram(spec, {"children": ["lambda_0", "k_minus"]})
    svg = render_feynman_svg(diagram)
    assert svg.startswith("<svg")
    assert "</svg>" in svg
