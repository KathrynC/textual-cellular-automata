from pathlib import Path

from text_ca.text_ca_corpus import load_corpus_jsonl


def test_load_seed_corpus_jsonl():
    path = Path("artifacts/text_ca/corpus/seed_corpus.jsonl")
    corpus = load_corpus_jsonl(path)

    assert len(corpus.records) >= 3  # expanded from 3 to 17+
    assert corpus.records[0].genre.value == "drama"
    assert len(corpus.records[0].source_cells) == 2
    assert len(corpus.records[2].target_cells) == 2
    assert corpus.records[2].source_cells[0].unit_type.value == "stanza_line"
