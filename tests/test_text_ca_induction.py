from text_ca.text_ca_corpus import CellAlignment, TextTransformCorpus, TextTransformRecord
from text_ca.text_ca_induction import (
    annotate_text_cell,
    collect_candidate_rule_clusters,
    induce_rules_from_corpus,
    induce_rules_from_record,
)
from text_ca.text_ca_schema import CellCoordinates, CellUnitType, TextCell, TextGenre


def _make_cell(cell_id: str, text: str, position: int, *, genre: TextGenre = TextGenre.DRAMA) -> TextCell:
    return TextCell(
        cell_id=cell_id,
        doc_id="doc",
        coordinates=CellCoordinates(thread_id="thread", position=position, iteration=0),
        surface_text=text,
        unit_type=CellUnitType.DIALOGUE_LINE,
        genre=genre,
        speaker="VOICE",
    )


def test_annotate_text_cell_extracts_motifs_and_operators():
    cell = _make_cell("c1", "The monitor records a reflected copy again.", 0)
    state = annotate_text_cell(cell)

    assert "surveillance" in state.semantic.motifs
    assert "reflection" in state.semantic.motifs
    assert "refrain" in state.semantic.motifs
    assert "add_recording_lexicon" in state.semantic.operators
    assert state.dramaturgical.surveillance > 0.0
    assert state.dramaturgical.doubling > 0.0


def test_induce_rules_from_record_emits_symbolic_delta_rule():
    source = _make_cell("s1", "Sign the form.", 0)
    target = _make_cell("t1", "Sign the script; the monitor is already recording.", 0)
    record = TextTransformRecord(
        doc_id="record_1",
        source_id="src",
        target_id="tgt",
        genre=TextGenre.DRAMA,
        transformation_family="radical_restaging",
        source_cells=[source],
        target_cells=[target],
        alignments=[CellAlignment(source_cell_ids=["s1"], target_cell_ids=["t1"], confidence=0.9)],
    )

    rules = induce_rules_from_record(record)

    assert len(rules) == 1
    rule = rules[0]
    assert rule.support == 1
    assert "semantic.motifs_add" in rule.state_updates
    assert "surveillance" in rule.state_updates["semantic.motifs_add"]
    assert any(op.operation == "add_recording_lexicon" for op in rule.surface_operations)


def test_collect_candidate_rule_clusters_groups_identical_signatures():
    sources = [
        _make_cell("s1", "Sign the form.", 0),
        _make_cell("s2", "Sign the waiver.", 1),
    ]
    targets = [
        _make_cell("t1", "Sign the script; the monitor is already recording.", 0),
        _make_cell("t2", "Sign the script; the monitor is already recording.", 1),
    ]
    record = TextTransformRecord(
        doc_id="record_2",
        source_id="src",
        target_id="tgt",
        genre=TextGenre.DRAMA,
        transformation_family="radical_restaging",
        source_cells=sources,
        target_cells=targets,
        alignments=[
            CellAlignment(source_cell_ids=["s1"], target_cell_ids=["t1"], confidence=0.8),
            CellAlignment(source_cell_ids=["s2"], target_cell_ids=["t2"], confidence=0.85),
        ],
    )

    clusters = collect_candidate_rule_clusters(record)

    assert len(clusters) == 1
    assert len(clusters[0].examples) == 2


def test_induce_rules_from_corpus_requires_repeated_support():
    record_1 = TextTransformRecord(
        doc_id="record_a",
        source_id="src_a",
        target_id="tgt_a",
        genre=TextGenre.DRAMA,
        transformation_family="radical_restaging",
        source_cells=[_make_cell("sa1", "Sign the form.", 0)],
        target_cells=[_make_cell("ta1", "Sign the script; the monitor is already recording.", 0)],
        alignments=[CellAlignment(source_cell_ids=["sa1"], target_cell_ids=["ta1"], confidence=0.8)],
    )
    record_2 = TextTransformRecord(
        doc_id="record_b",
        source_id="src_b",
        target_id="tgt_b",
        genre=TextGenre.DRAMA,
        transformation_family="radical_restaging",
        source_cells=[_make_cell("sb1", "Sign the waiver.", 0)],
        target_cells=[_make_cell("tb1", "Sign the script; the monitor is already recording.", 0)],
        alignments=[CellAlignment(source_cell_ids=["sb1"], target_cell_ids=["tb1"], confidence=0.9)],
    )
    corpus = TextTransformCorpus(records=[record_1, record_2])

    rules = induce_rules_from_corpus(corpus, min_support=2)

    assert len(rules) == 1
    assert rules[0].support == 2
    assert rules[0].confidence > 0.8
