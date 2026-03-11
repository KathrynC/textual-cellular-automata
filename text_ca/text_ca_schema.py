"""Typed schemas for textual semantic cellular automata.

This module defines genre-aware text cells, multichannel semantic state, and
run records for a higher-dimensional textual CA subsystem. The types are kept
generic so the subsystem can live inside NADJA now and be extracted later if
needed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class TextGenre(str, Enum):
    """Supported high-level literary domains."""

    DRAMA = "drama"
    FICTION = "fiction"
    POETRY = "poetry"
    HYBRID = "hybrid"


class CellUnitType(str, Enum):
    """Supported segmentation units."""

    TOKEN = "token"
    PHRASE = "phrase"
    LINE = "line"
    SENTENCE = "sentence"
    CLAUSE = "clause"
    DIALOGUE_LINE = "dialogue_line"
    STAGE_DIRECTION = "stage_direction"
    SCENE_HEADER = "scene_header"
    STANZA_LINE = "stanza_line"
    PARAGRAPH_BEAT = "paragraph_beat"
    SYSTEM_INSERT = "system_insert"


@dataclass
class CellCoordinates:
    """Higher-dimensional cell coordinates."""

    thread_id: str
    position: int
    iteration: int = 0


@dataclass
class TextCell:
    """A single textual CA cell before or after annotation."""

    cell_id: str
    doc_id: str
    coordinates: CellCoordinates
    surface_text: str
    unit_type: CellUnitType
    genre: TextGenre
    speaker: Optional[str] = None
    addressee: Optional[str] = None
    structure: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class LexicalFeatures:
    lemmas: List[str] = field(default_factory=list)
    register: str = "unknown"
    compression: float = 0.0


@dataclass
class SyntacticFeatures:
    mood: str = "unknown"
    clause_count: int = 0
    fragmentation: float = 0.0


@dataclass
class RhetoricalFeatures:
    speech_act: str = "unknown"
    interrogativity: float = 0.0
    imperative_force: float = 0.0


@dataclass
class AffectFeatures:
    anxiety: float = 0.0
    authority: float = 0.0
    intimacy: float = 0.0


@dataclass
class NarrativeFeatures:
    temporal_recursion: float = 0.0
    ontological_instability: float = 0.0
    focalization_shift: float = 0.0


@dataclass
class DramaturgicalFeatures:
    doubling: float = 0.0
    surveillance: float = 0.0
    ritualization: float = 0.0
    ghosting: float = 0.0
    witness: float = 0.0
    remorse: float = 0.0
    quiescence: float = 0.0


@dataclass
class ProsodicFeatures:
    lineation_pressure: float = 0.0
    sound_recurrence: float = 0.0
    rhyme_field: List[str] = field(default_factory=list)


@dataclass
class SemanticFeatures:
    lakoff_frames: List[str] = field(default_factory=list)
    motifs: List[str] = field(default_factory=list)
    pattern_refs: List[str] = field(default_factory=list)
    operators: List[str] = field(default_factory=list)


@dataclass
class LinkFeatures:
    echo_of: List[str] = field(default_factory=list)
    mirrors: List[str] = field(default_factory=list)
    quoted_from: List[str] = field(default_factory=list)


@dataclass
class TextCellState:
    """Multichannel symbolic state for one textual cell."""

    cell: TextCell
    lexical: LexicalFeatures = field(default_factory=LexicalFeatures)
    syntactic: SyntacticFeatures = field(default_factory=SyntacticFeatures)
    rhetorical: RhetoricalFeatures = field(default_factory=RhetoricalFeatures)
    affect: AffectFeatures = field(default_factory=AffectFeatures)
    narrative: NarrativeFeatures = field(default_factory=NarrativeFeatures)
    dramaturgical: DramaturgicalFeatures = field(default_factory=DramaturgicalFeatures)
    prosodic: ProsodicFeatures = field(default_factory=ProsodicFeatures)
    semantic: SemanticFeatures = field(default_factory=SemanticFeatures)
    links: LinkFeatures = field(default_factory=LinkFeatures)
    dynamical_signatures: Dict[str, object] = field(default_factory=dict)
    annotations: Dict[str, str] = field(default_factory=dict)

    def copy_for_iteration(self, iteration: int, surface_text: Optional[str] = None) -> "TextCellState":
        """Create a shallowly updated state for the next iteration."""

        new_cell = TextCell(
            cell_id=self.cell.cell_id,
            doc_id=self.cell.doc_id,
            coordinates=CellCoordinates(
                thread_id=self.cell.coordinates.thread_id,
                position=self.cell.coordinates.position,
                iteration=iteration,
            ),
            surface_text=surface_text if surface_text is not None else self.cell.surface_text,
            unit_type=self.cell.unit_type,
            genre=self.cell.genre,
            speaker=self.cell.speaker,
            addressee=self.cell.addressee,
            structure=dict(self.cell.structure),
            metadata=dict(self.cell.metadata),
        )
        return TextCellState(
            cell=new_cell,
            lexical=LexicalFeatures(**self.lexical.__dict__),
            syntactic=SyntacticFeatures(**self.syntactic.__dict__),
            rhetorical=RhetoricalFeatures(**self.rhetorical.__dict__),
            affect=AffectFeatures(**self.affect.__dict__),
            narrative=NarrativeFeatures(**self.narrative.__dict__),
            dramaturgical=DramaturgicalFeatures(**self.dramaturgical.__dict__),
            prosodic=ProsodicFeatures(
                lineation_pressure=self.prosodic.lineation_pressure,
                sound_recurrence=self.prosodic.sound_recurrence,
                rhyme_field=list(self.prosodic.rhyme_field),
            ),
            semantic=SemanticFeatures(
                lakoff_frames=list(self.semantic.lakoff_frames),
                motifs=list(self.semantic.motifs),
                pattern_refs=list(self.semantic.pattern_refs),
                operators=list(self.semantic.operators),
            ),
            links=LinkFeatures(
                echo_of=list(self.links.echo_of),
                mirrors=list(self.links.mirrors),
                quoted_from=list(self.links.quoted_from),
            ),
            dynamical_signatures=dict(self.dynamical_signatures),
            annotations=dict(self.annotations),
        )


@dataclass
class NeighborhoodRef:
    """References to neighboring cells across sequence, topology, and memory."""

    prev_seq: List[str] = field(default_factory=list)
    next_seq: List[str] = field(default_factory=list)
    same_thread_window: List[str] = field(default_factory=list)
    cross_thread_echoes: List[str] = field(default_factory=list)
    prior_iteration_self: List[str] = field(default_factory=list)
    ancestral_links: List[str] = field(default_factory=list)


@dataclass
class TextCARunRecord:
    """Top-level record for a textual CA simulation run."""

    run_id: str
    source_doc_id: str
    steps: int
    state_history: List[List[TextCellState]] = field(default_factory=list)
    fired_rule_ids: List[List[str]] = field(default_factory=list)
    realized_text_by_step: List[List[str]] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)


DEFAULT_NUMERIC_CHANNELS: Tuple[str, ...] = (
    "affect.anxiety",
    "affect.authority",
    "affect.intimacy",
    "narrative.temporal_recursion",
    "narrative.ontological_instability",
    "narrative.focalization_shift",
    "dramaturgical.doubling",
    "dramaturgical.surveillance",
    "dramaturgical.ritualization",
    "dramaturgical.ghosting",
    "dramaturgical.witness",
    "dramaturgical.remorse",
    "dramaturgical.quiescence",
    "prosodic.lineation_pressure",
    "prosodic.sound_recurrence",
)
