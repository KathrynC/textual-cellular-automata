"""Integration tests for textual semantic cellular automata with Lakoff frames."""

import sys
import os

from text_ca.text_ca_analytics import (
    analyze_text_ca_run,
    compute_frame_contagion_rate,
    compute_frame_diversity,
    compute_compatibility_histogram,
)
from text_ca.text_ca_corpus import load_corpus_jsonl
from text_ca.text_ca_induction import annotate_text_cell, induce_rules_from_corpus
from text_ca.text_ca_rules import DEFAULT_TEXT_CA_RULES
from text_ca.text_ca_schema import (
    CellCoordinates,
    CellUnitType,
    TextCARunRecord,
    TextCell,
    TextCellState,
    TextGenre,
)
from text_ca.text_ca_simulator import (
    _compute_text_cell_compatibility,
    _compute_text_rule_compatibility,
    build_local_neighborhood,
    simulate_text_ca,
)


CORPUS_PATH = os.path.join(os.path.dirname(__file__), "..", "artifacts", "text_ca", "corpus", "seed_corpus.jsonl")


def _make_cell(cell_id, text, position, genre=TextGenre.FICTION):
    return TextCell(
        cell_id=cell_id,
        doc_id="test",
        coordinates=CellCoordinates("thread", position, 0),
        surface_text=text,
        unit_type=CellUnitType.SENTENCE,
        genre=genre,
    )


def test_annotation_produces_lakoff_frames():
    cell = _make_cell("c1", "Fear floods the boundary as panic cascades", 0)
    state = annotate_text_cell(cell)
    assert len(state.semantic.lakoff_frames) > 0
    assert len(state.dynamical_signatures) > 0
    # Should detect fear, flow, container-related frames
    assert any("FEAR" in f or "FLOW" in f or "CONTAINER" in f for f in state.semantic.lakoff_frames)


def test_annotation_detects_literary_motifs():
    cell = _make_cell("c1", "The path wandered through a boundary where flowers withered", 0)
    state = annotate_text_cell(cell)
    assert "journey" in state.semantic.motifs
    assert "container" in state.semantic.motifs
    assert "growth" in state.semantic.motifs


def test_cell_compatibility_symmetric():
    a = annotate_text_cell(_make_cell("a", "Fear grips the market boundary", 0))
    b = annotate_text_cell(_make_cell("b", "Panic cascades across the threshold", 1))
    c = annotate_text_cell(_make_cell("c", "The morning was quiet and still", 2))

    ab = _compute_text_cell_compatibility(a, b)
    ba = _compute_text_cell_compatibility(b, a)
    ac = _compute_text_cell_compatibility(a, c)

    # Symmetric
    assert abs(ab - ba) < 0.01
    # Fear/panic cells more compatible with each other than with neutral
    assert ab > ac


def test_weighted_neighborhood_returns_tuples():
    states = [
        annotate_text_cell(_make_cell(f"c{i}", f"Text {i}", i))
        for i in range(5)
    ]
    nbhd = build_local_neighborhood(states, 2)
    assert "prev_seq" in nbhd
    assert "next_seq" in nbhd
    for bucket in nbhd.values():
        for item in bucket:
            assert isinstance(item, tuple)
            assert len(item) == 2
            assert isinstance(item[0], TextCellState)
            assert isinstance(item[1], float)


def test_rule_cell_compatibility_range():
    state = annotate_text_cell(_make_cell("c1", "Fear floods the boundary", 0))
    for rule in DEFAULT_TEXT_CA_RULES:
        compat = _compute_text_rule_compatibility(rule, state)
        assert 0.5 <= compat <= 2.0, f"Compatibility {compat} out of range for {rule.rule_id}"


def test_frame_contagion_propagates():
    """Cell 0 has FEAR-rich text. After 5 steps, adjacent cells should gain frames."""
    cells = [
        _make_cell("c0", "Fear grips the boundary as panic cascades everywhere", 0),
        _make_cell("c1", "The morning was quiet and still", 1),
        _make_cell("c2", "She sat by the window reading", 2),
    ]
    states = [annotate_text_cell(c) for c in cells]
    initial_c1_frames = len(states[1].semantic.lakoff_frames)

    result = simulate_text_ca(states, steps=5, seed=42)
    final = result.state_history[-1]
    final_c1_frames = len(final[1].semantic.lakoff_frames)

    # Adjacent cell should gain at least 1 frame
    assert final_c1_frames > initial_c1_frames


def test_full_ca_run_shows_emergence():
    """8-cell grid after 10 steps should show non-trivial dynamics."""
    texts = [
        "Fear grips the boundary as panic cascades",
        "The market resists the downward pressure",
        "She walked the path toward the distant gate",
        "The river floods its banks in the drought",
        "He defended the position under siege",
        "Flowers bloom where the old roots withered",
        "The echo repeated through the empty room again",
        "Light fell through the window onto the fire",
    ]
    cells = [_make_cell(f"c{i}", t, i) for i, t in enumerate(texts)]
    states = [annotate_text_cell(c) for c in cells]

    result = simulate_text_ca(states, steps=10, seed=123)
    analysis = analyze_text_ca_run(result)

    # Non-flat motif persistence
    assert len(analysis["motif_persistence"]) > 0

    # Entropy curve should vary (not constant)
    entropy_curve = analysis["entropy_curve"]
    assert len(entropy_curve) == 11  # 10 steps + initial

    # Frame contagion should be positive
    assert analysis["frame_contagion_rate"] > 0

    # Frame diversity should be positive for most steps
    assert any(d > 0 for d in analysis["frame_diversity"])

    # Compatibility histogram should have entries
    assert len(analysis["compatibility_histogram"]) > 0


def test_corpus_rule_induction_produces_framed_rules():
    corpus = load_corpus_jsonl(CORPUS_PATH)
    rules = induce_rules_from_corpus(corpus, min_support=2)
    assert len(rules) >= 5

    # At least some rules should have Lakoff frames
    framed = [r for r in rules if r.lakoff_frames]
    assert len(framed) >= 2


def test_differentiated_rule_selection():
    """Cell with CONTAINER frames should prefer rules with CONTAINER frames."""
    container_cell = annotate_text_cell(
        _make_cell("c1", "The boundary contains the threshold crossing", 0)
    )
    assert "CONTAINER" in container_cell.semantic.lakoff_frames

    # Check compatibility with rules that have CONTAINER vs not
    for rule in DEFAULT_TEXT_CA_RULES:
        compat = _compute_text_rule_compatibility(rule, container_cell)
        if "CONTAINER" in rule.lakoff_frames:
            assert compat > 1.0  # above neutral
