"""Rule induction for textual semantic cellular automata.

This module turns aligned source/target textual transformations into candidate
local rewrite rules over symbolic state rather than raw text alone.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Sequence, Tuple

from .lakoff_taxonomy import TAXONOMY
from .text_ca_corpus import TextTransformCorpus, TextTransformRecord
from .text_ca_rules import TextCARule, TextCASurfaceOperation
from .text_ca_schema import TextCell, TextCellState


@dataclass
class InducedRuleExample:
    """One aligned example contributing evidence for a candidate rule."""

    doc_id: str
    source_cell_ids: List[str]
    target_cell_ids: List[str]
    confidence: float
    source_text: str
    target_text: str


@dataclass
class CandidateRuleCluster:
    """A cluster of repeated symbolic deltas suitable for rule emission."""

    signature: Tuple[str, ...]
    examples: List[InducedRuleExample] = field(default_factory=list)
    source_genres: List[str] = field(default_factory=list)
    transformation_families: List[str] = field(default_factory=list)


def annotate_text_cell(cell: TextCell) -> TextCellState:
    """Annotate a text cell with simple deterministic heuristics.

    This is intentionally lightweight. It provides enough symbolic state for
    rule induction and can later be replaced or enriched with deeper semantic
    spelunking.
    """

    state = TextCellState(cell=cell)
    text = cell.surface_text.lower()

    state.lexical.lemmas = [token.strip(".,;:!?\"'()[]") for token in text.split() if token.strip()]
    state.lexical.compression = 1.0 / max(1, len(state.lexical.lemmas))

    if "?" in cell.surface_text:
        state.rhetorical.interrogativity = 1.0
        state.rhetorical.speech_act = "question"
    elif cell.unit_type.value in {"dialogue_line", "stage_direction"}:
        state.rhetorical.speech_act = "statement"

    if cell.speaker:
        state.affect.authority = 0.6

    motif_lexicon = {
        "testing": ["test", "compatib", "qualif", "interview"],
        "consent": ["consent", "sign", "forms", "signature"],
        "anxiety": ["wonder", "nervous", "afraid", "question"],
        "reflection": ["reflect", "mirror", "glass", "echo"],
        "surveillance": ["camera", "record", "monitor", "log", "tally"],
        "ghosting": ["ghost", "afterimage", "whisper", "static"],
        "ritual": ["ceremony", "ritual", "bless", "witness"],
        "refrain": ["again", "repeat", "rehears", "return"],
        "parallelism": ["chorus", "double", "copy", "version"],
        "image_echo": ["light", "window", "fire", "dog", "voice"],
        "container": ["boundary", "threshold", "crossing", "enclosure", "contain"],
        "journey": ["path", "wander", "arrive", "depart", "destination", "travel"],
        "force": ["push", "resist", "pressure", "compel", "gravity", "momentum"],
        "flow": ["current", "flood", "drought", "ebb", "stream", "drain"],
        "war": ["siege", "defend", "attack", "retreat", "surrender", "battle"],
        "growth": ["bloom", "wither", "rot", "sprout", "harvest", "grow"],
        "fear": ["panic", "dread", "terror", "fear", "fright"],
        "loss": ["grief", "mourn", "sorrow", "loss", "bereft"],
        "cascade": ["cascade", "collapse", "domino", "chain", "contagion"],
    }
    for motif, stems in motif_lexicon.items():
        if any(stem in text for stem in stems):
            state.semantic.motifs.append(motif)

    operator_lexicon = {
        "institution_to_stage_metaphor": ["stage", "theater", "auditorium", "script"],
        "add_recording_lexicon": ["record", "monitor", "camera", "tally", "log"],
        "echo_split": ["echo", "double", "copy", "reflection"],
        "ritual_closure": ["silence", "peace", "bless", "absolve"],
    }
    for operator, stems in operator_lexicon.items():
        if any(stem in text for stem in stems):
            state.semantic.operators.append(operator)

    # --- Lakoff frame detection ---
    _STOP_WORDS = frozenset({
        "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "shall",
        "should", "may", "might", "must", "can", "could", "of", "in", "to",
        "for", "with", "on", "at", "from", "by", "as", "or", "and", "but",
        "if", "so", "no", "not", "it", "its", "he", "she", "they", "we",
        "you", "i", "me", "my", "his", "her", "our", "their", "this", "that",
        "these", "those", "than", "then", "up", "out", "into", "all",
    })
    detected_frame_ids: set = set()
    for token in state.lexical.lemmas:
        if len(token) < 3 or token in _STOP_WORDS:
            continue
        for frame in TAXONOMY.find_frames_by_keyword(token):
            detected_frame_ids.add(frame.id)
    for motif in state.semantic.motifs:
        for frame in TAXONOMY.find_frames_by_keyword(motif):
            detected_frame_ids.add(frame.id)
    state.semantic.lakoff_frames = sorted(detected_frame_ids)

    # --- Dynamical signatures from matched frames ---
    for frame_id in state.semantic.lakoff_frames:
        try:
            frame = TAXONOMY.get(frame_id)
            state.dynamical_signatures[frame_id] = {
                "attractor_type": frame.attractor_type.value,
                "basin_width": frame.basin_width,
                "bifurcation_sensitivity": frame.bifurcation_sensitivity,
                "dynamical_signature": frame.dynamical_signature.value,
            }
        except KeyError:
            pass

    state.narrative.temporal_recursion = 0.5 if any(stem in text for stem in ("again", "already", "repeat", "loop")) else 0.0
    state.narrative.ontological_instability = 0.5 if any(stem in text for stem in ("ghost", "double", "copy", "version")) else 0.0
    state.dramaturgical.doubling = 0.6 if any(stem in text for stem in ("double", "reflect", "mirror", "echo", "copy")) else 0.0
    state.dramaturgical.surveillance = 0.7 if any(stem in text for stem in ("camera", "record", "monitor", "log", "tally")) else 0.0
    state.dramaturgical.ghosting = 0.6 if any(stem in text for stem in ("ghost", "afterimage", "static", "whisper")) else 0.0
    state.dramaturgical.ritualization = 0.7 if any(stem in text for stem in ("ceremony", "ritual", "bless", "witness", "absolve")) else 0.0
    state.dramaturgical.quiescence = 0.8 if any(stem in text for stem in ("silence", "cease", "peace", "blank")) else 0.0

    if cell.genre.value == "poetry":
        state.prosodic.lineation_pressure = 0.5
        repeated_prefixes = {lemma[:3] for lemma in state.lexical.lemmas if len(lemma) >= 3}
        state.prosodic.sound_recurrence = min(1.0, len(repeated_prefixes) / max(1, len(state.lexical.lemmas)))

    return state


def _delta_signature(source: TextCellState, target: TextCellState) -> Tuple[str, ...]:
    """Compute a compact symbolic signature for an aligned source/target pair."""

    deltas: List[str] = []

    source_motifs = set(source.semantic.motifs)
    target_motifs = set(target.semantic.motifs)
    for motif in sorted(target_motifs - source_motifs):
        deltas.append(f"motif+:{motif}")

    source_ops = set(source.semantic.operators)
    target_ops = set(target.semantic.operators)
    for operator in sorted(target_ops - source_ops):
        deltas.append(f"op+:{operator}")

    numeric_channels = [
        ("narrative.temporal_recursion", source.narrative.temporal_recursion, target.narrative.temporal_recursion),
        ("narrative.ontological_instability", source.narrative.ontological_instability, target.narrative.ontological_instability),
        ("dramaturgical.doubling", source.dramaturgical.doubling, target.dramaturgical.doubling),
        ("dramaturgical.surveillance", source.dramaturgical.surveillance, target.dramaturgical.surveillance),
        ("dramaturgical.ghosting", source.dramaturgical.ghosting, target.dramaturgical.ghosting),
        ("dramaturgical.ritualization", source.dramaturgical.ritualization, target.dramaturgical.ritualization),
        ("dramaturgical.quiescence", source.dramaturgical.quiescence, target.dramaturgical.quiescence),
        ("prosodic.lineation_pressure", source.prosodic.lineation_pressure, target.prosodic.lineation_pressure),
        ("prosodic.sound_recurrence", source.prosodic.sound_recurrence, target.prosodic.sound_recurrence),
    ]
    for name, before, after in numeric_channels:
        if after - before >= 0.2:
            deltas.append(f"inc:{name}")

    if target.rhetorical.interrogativity > source.rhetorical.interrogativity:
        deltas.append("inc:rhetorical.interrogativity")

    return tuple(sorted(deltas))


def _preconditions_from_state(state: TextCellState) -> Dict[str, object]:
    """Create lightweight rule preconditions from an annotated source state."""

    conditions: Dict[str, object] = {
        "cell.unit_type": [state.cell.unit_type.value],
    }
    if state.affect.authority >= 0.5:
        conditions["affect.authority"] = (0.5, 1.0)
    if state.prosodic.sound_recurrence >= 0.2:
        conditions["prosodic.sound_recurrence"] = (0.2, 1.0)
    return conditions


def _state_updates_from_signature(signature: Tuple[str, ...]) -> Dict[str, object]:
    """Convert a symbolic delta signature into rule state updates."""

    updates: Dict[str, object] = {}
    motif_add: List[str] = []
    op_add: List[str] = []

    for item in signature:
        if item.startswith("motif+:"):
            motif_add.append(item.split(":", 1)[1])
        elif item.startswith("op+:"):
            op_add.append(item.split(":", 1)[1])
        elif item.startswith("inc:"):
            channel = item.split(":", 1)[1]
            updates[channel] = 0.25

    if motif_add:
        updates["semantic.motifs_add"] = motif_add
    if op_add:
        updates["semantic.operators_add"] = op_add
    return updates


def _surface_operations_from_signature(signature: Tuple[str, ...]) -> List[TextCASurfaceOperation]:
    """Project a signature into coarse surface realization operators."""

    operations: List[TextCASurfaceOperation] = []
    for item in signature:
        if item.startswith("op+:"):
            operations.append(TextCASurfaceOperation(item.split(":", 1)[1]))
    if not operations and any(item.startswith("motif+:") for item in signature):
        operations.append(TextCASurfaceOperation("semantic_intensification"))
    return operations


def collect_candidate_rule_clusters(record: TextTransformRecord) -> List[CandidateRuleCluster]:
    """Collect repeated symbolic delta clusters from one aligned transform record."""

    clusters: Dict[Tuple[str, ...], CandidateRuleCluster] = {}
    for source_cells, target_cells, confidence in record.aligned_pairs():
        if len(source_cells) != 1 or len(target_cells) != 1:
            continue

        source_state = annotate_text_cell(source_cells[0])
        target_state = annotate_text_cell(target_cells[0])
        signature = _delta_signature(source_state, target_state)
        if not signature:
            continue

        cluster = clusters.setdefault(
            signature,
            CandidateRuleCluster(signature=signature),
        )
        cluster.examples.append(
            InducedRuleExample(
                doc_id=record.doc_id,
                source_cell_ids=[source_cells[0].cell_id],
                target_cell_ids=[target_cells[0].cell_id],
                confidence=confidence,
                source_text=source_cells[0].surface_text,
                target_text=target_cells[0].surface_text,
            )
        )
        cluster.source_genres.append(record.genre.value)
        cluster.transformation_families.append(record.transformation_family)

    return list(clusters.values())


def induce_rules_from_record(record: TextTransformRecord, min_support: int = 1) -> List[TextCARule]:
    """Induce candidate rules from one aligned transform record."""

    rules: List[TextCARule] = []
    for cluster in collect_candidate_rule_clusters(record):
        if len(cluster.examples) < min_support:
            continue
        example = cluster.examples[0]
        source_lookup = {cell.cell_id: cell for cell in record.source_cells}
        source_cell = source_lookup[example.source_cell_ids[0]]
        source_state = annotate_text_cell(source_cell)
        confidence = sum(item.confidence for item in cluster.examples) / len(cluster.examples)
        rules.append(
            TextCARule(
                rule_id=f"induced_{record.doc_id}_{len(rules):03d}",
                name="_".join(cluster.signature)[:120] or "no_op_delta",
                domains=sorted(set(cluster.source_genres)),
                preconditions={"self": _preconditions_from_state(source_state)},
                state_updates=_state_updates_from_signature(cluster.signature),
                surface_operations=_surface_operations_from_signature(cluster.signature),
                lakoff_frames=list(source_state.semantic.lakoff_frames),
                confidence=confidence,
                support=len(cluster.examples),
            )
        )
    return rules


def induce_rules_from_corpus(corpus: TextTransformCorpus, min_support: int = 2) -> List[TextCARule]:
    """Induce rules across a corpus and merge identical signatures."""

    aggregated: Dict[Tuple[str, ...], CandidateRuleCluster] = defaultdict(lambda: CandidateRuleCluster(signature=()))
    exemplar_records: Dict[Tuple[str, ...], Tuple[TextTransformRecord, str]] = {}

    for record in corpus.records:
        for cluster in collect_candidate_rule_clusters(record):
            current = aggregated.get(cluster.signature)
            if current is None or current.signature == ():
                current = CandidateRuleCluster(signature=cluster.signature)
                aggregated[cluster.signature] = current
            current.examples.extend(cluster.examples)
            current.source_genres.extend(cluster.source_genres)
            current.transformation_families.extend(cluster.transformation_families)
            if cluster.signature not in exemplar_records and cluster.examples:
                exemplar_records[cluster.signature] = (record, cluster.examples[0].source_cell_ids[0])

    rules: List[TextCARule] = []
    for index, signature in enumerate(sorted(aggregated.keys())):
        cluster = aggregated[signature]
        if len(cluster.examples) < min_support:
            continue
        record, source_cell_id = exemplar_records[signature]
        source_lookup = {cell.cell_id: cell for cell in record.source_cells}
        source_state = annotate_text_cell(source_lookup[source_cell_id])
        confidence = sum(item.confidence for item in cluster.examples) / len(cluster.examples)
        rules.append(
            TextCARule(
                rule_id=f"induced_corpus_{index:03d}",
                name="_".join(signature)[:120] or "no_op_delta",
                domains=sorted(set(cluster.source_genres)),
                preconditions={"self": _preconditions_from_state(source_state)},
                state_updates=_state_updates_from_signature(signature),
                surface_operations=_surface_operations_from_signature(signature),
                lakoff_frames=list(source_state.semantic.lakoff_frames),
                confidence=confidence,
                support=len(cluster.examples),
            )
        )
    return rules
