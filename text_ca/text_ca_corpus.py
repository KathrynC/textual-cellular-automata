"""Corpus and alignment helpers for textual semantic cellular automata."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from .text_ca_schema import CellCoordinates, CellUnitType, TextGenre, TextCell


@dataclass
class ProvenanceRecord:
    """Source and target provenance for one corpus item."""

    author_source: str = ""
    author_target: str = ""
    date_source: str = ""
    date_target: str = ""


@dataclass
class CellAlignment:
    """Alignment between source and target cell identifiers."""

    source_cell_ids: List[str]
    target_cell_ids: List[str]
    confidence: float = 1.0
    notes: str = ""


@dataclass
class TextTransformRecord:
    """Aligned source/target transformation record."""

    doc_id: str
    source_id: str
    target_id: str
    genre: TextGenre
    transformation_family: str
    language: str = "en"
    alignment_quality: float = 1.0
    provenance: ProvenanceRecord = field(default_factory=ProvenanceRecord)
    source_cells: List[TextCell] = field(default_factory=list)
    target_cells: List[TextCell] = field(default_factory=list)
    alignments: List[CellAlignment] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)

    def aligned_pairs(self) -> List[tuple[List[TextCell], List[TextCell], float]]:
        """Resolve alignments into concrete source/target cell lists."""

        source_lookup = {cell.cell_id: cell for cell in self.source_cells}
        target_lookup = {cell.cell_id: cell for cell in self.target_cells}
        pairs: List[tuple[List[TextCell], List[TextCell], float]] = []
        for alignment in self.alignments:
            src = [source_lookup[cell_id] for cell_id in alignment.source_cell_ids if cell_id in source_lookup]
            tgt = [target_lookup[cell_id] for cell_id in alignment.target_cell_ids if cell_id in target_lookup]
            pairs.append((src, tgt, alignment.confidence))
        return pairs


@dataclass
class TextTransformCorpus:
    """A collection of aligned textual transformations."""

    records: List[TextTransformRecord] = field(default_factory=list)

    def by_genre(self, genre: TextGenre) -> List[TextTransformRecord]:
        """Return all records matching a genre."""

        return [record for record in self.records if record.genre == genre]

    def by_transformation_family(self, family: str) -> List[TextTransformRecord]:
        """Return all records matching a transformation family."""

        return [record for record in self.records if record.transformation_family == family]

    def get(self, doc_id: str) -> Optional[TextTransformRecord]:
        """Lookup by document identifier."""

        for record in self.records:
            if record.doc_id == doc_id:
                return record
        return None


def _parse_cell(raw: Dict[str, object], *, doc_id: str, default_genre: TextGenre, iteration: int) -> TextCell:
    """Parse one JSON cell object into a TextCell."""

    genre = TextGenre(raw.get("genre", default_genre.value))
    unit_type = CellUnitType(raw.get("unit_type", CellUnitType.LINE.value))
    return TextCell(
        cell_id=str(raw["cell_id"]),
        doc_id=doc_id,
        coordinates=CellCoordinates(
            thread_id=str(raw.get("thread_id", "thread")),
            position=int(raw.get("position", 0)),
            iteration=iteration,
        ),
        surface_text=str(raw["surface_text"]),
        unit_type=unit_type,
        genre=genre,
        speaker=raw.get("speaker"),
        addressee=raw.get("addressee"),
        structure=dict(raw.get("structure", {})),
        metadata=dict(raw.get("metadata", {})),
    )


def load_corpus_jsonl(path: str | Path) -> TextTransformCorpus:
    """Load a textual CA corpus from a JSONL artifact."""

    corpus = TextTransformCorpus()
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            raw = json.loads(line)
            genre = TextGenre(raw.get("genre", TextGenre.HYBRID.value))
            provenance_raw = raw.get("provenance", {})
            record = TextTransformRecord(
                doc_id=raw["doc_id"],
                source_id=raw["source_id"],
                target_id=raw["target_id"],
                genre=genre,
                transformation_family=raw["transformation_family"],
                language=raw.get("language", "en"),
                alignment_quality=float(raw.get("alignment_quality", 1.0)),
                provenance=ProvenanceRecord(
                    author_source=provenance_raw.get("author_source", ""),
                    author_target=provenance_raw.get("author_target", ""),
                    date_source=provenance_raw.get("date_source", ""),
                    date_target=provenance_raw.get("date_target", ""),
                ),
                source_cells=[
                    _parse_cell(cell, doc_id=raw["doc_id"], default_genre=genre, iteration=0)
                    for cell in raw.get("source_cells", [])
                ],
                target_cells=[
                    _parse_cell(cell, doc_id=raw["doc_id"], default_genre=genre, iteration=1)
                    for cell in raw.get("target_cells", [])
                ],
                alignments=[
                    CellAlignment(
                        source_cell_ids=list(alignment.get("source_cell_ids", [])),
                        target_cell_ids=list(alignment.get("target_cell_ids", [])),
                        confidence=float(alignment.get("confidence", 1.0)),
                        notes=alignment.get("notes", ""),
                    )
                    for alignment in raw.get("alignments", [])
                ],
                metadata=dict(raw.get("metadata", {})),
            )
            corpus.records.append(record)
    return corpus
