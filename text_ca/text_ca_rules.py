"""Rule definitions for textual semantic cellular automata."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .text_ca_schema import TextCellState


@dataclass
class TextCASurfaceOperation:
    """Named surface-level realization strategy."""

    operation: str
    params: Dict[str, str] = field(default_factory=dict)


@dataclass
class TextCARule:
    """Serializable local textual CA rule."""

    rule_id: str
    name: str
    domains: List[str] = field(default_factory=list)
    preconditions: Dict[str, object] = field(default_factory=dict)
    state_updates: Dict[str, object] = field(default_factory=dict)
    surface_operations: List[TextCASurfaceOperation] = field(default_factory=list)
    neighborhood_radius: Dict[str, int] = field(default_factory=lambda: {"seq": 1, "thread": 1, "memory": 1})
    lakoff_frames: List[str] = field(default_factory=list)
    confidence: float = 0.5
    support: int = 0


def _get_channel_value(state: TextCellState, path: str) -> object:
    """Resolve dotted channel paths like 'dramaturgical.surveillance'."""

    current: object = state
    for segment in path.split("."):
        if not hasattr(current, segment):
            return None
        current = getattr(current, segment)
    return current


def _matches_range(value: object, expected: object) -> bool:
    """Evaluate simple equality or inclusive range conditions."""

    if isinstance(expected, tuple) and len(expected) == 2:
        if not isinstance(value, (int, float)):
            return False
        return expected[0] <= value <= expected[1]
    if isinstance(expected, list):
        return value in expected
    return value == expected


def rule_matches(
    rule: TextCARule,
    state: TextCellState,
    neighborhood: Dict[str, List["tuple[TextCellState, float]"]],
) -> bool:
    """Check whether a rule applies to a state and its weighted neighborhood.

    Neighborhood values are (TextCellState, compatibility_weight) tuples.
    For motifs_any preconditions, the total weight of neighbors carrying the
    motif must exceed 0.3 (not just set membership).
    """

    self_spec = rule.preconditions.get("self", {})
    for path, expected in self_spec.items():
        value = _get_channel_value(state, path)
        if not _matches_range(value, expected):
            return False

    neighborhood_spec = rule.preconditions.get("neighborhood", {})
    motifs_any = neighborhood_spec.get("semantic.motifs_any", [])
    if motifs_any:
        motif_weights: Dict[str, float] = {}
        for bucket in neighborhood.values():
            for neighbor, weight in bucket:
                for motif in neighbor.semantic.motifs:
                    motif_weights[motif] = motif_weights.get(motif, 0.0) + weight
        if not any(motif_weights.get(motif, 0.0) > 0.3 for motif in motifs_any):
            return False

    return True


def apply_state_updates(state: TextCellState, updates: Dict[str, object]) -> None:
    """Apply in-place symbolic state updates to a textual cell state."""

    for path, value in updates.items():
        if path.endswith("_add"):
            base_path = path[:-4]
            target = _get_channel_value(state, base_path)
            if isinstance(target, list):
                for item in value:
                    if item not in target:
                        target.append(item)
            continue

        segments = path.split(".")
        target = state
        for segment in segments[:-1]:
            target = getattr(target, segment)
        leaf = segments[-1]
        current = getattr(target, leaf)
        if isinstance(current, (int, float)) and isinstance(value, (int, float)):
            setattr(target, leaf, max(0.0, min(1.0, current + value)))
        else:
            setattr(target, leaf, value)


DEFAULT_TEXT_CA_RULES: List[TextCARule] = [
    TextCARule(
        rule_id="dramatic_exposure_001",
        name="procedure_to_performance_surveillance",
        domains=["drama", "fiction"],
        preconditions={
            "self": {
                "cell.unit_type": ["dialogue_line", "stage_direction"],
                "affect.authority": (0.5, 1.0),
            },
            "neighborhood": {
                "semantic.motifs_any": ["testing", "consent", "anxiety"],
            },
        },
        state_updates={
            "dramaturgical.surveillance": 0.2,
            "dramaturgical.doubling": 0.15,
            "narrative.temporal_recursion": 0.1,
            "semantic.motifs_add": ["compatibility_test", "mirrored_identity"],
            "semantic.pattern_refs_add": ["recording_loop"],
        },
        surface_operations=[
            TextCASurfaceOperation("institution_to_stage_metaphor"),
            TextCASurfaceOperation("add_recording_lexicon"),
        ],
        lakoff_frames=["CONTAINER", "FORCE"],
        confidence=0.8,
        support=1,
    ),
    TextCARule(
        rule_id="poetic_refrain_001",
        name="image_field_intensification",
        domains=["poetry", "fiction"],
        preconditions={
            "self": {
                "prosodic.sound_recurrence": (0.2, 1.0),
            },
            "neighborhood": {
                "semantic.motifs_any": ["image_echo", "refrain", "parallelism"],
            },
        },
        state_updates={
            "prosodic.lineation_pressure": 0.1,
            "prosodic.sound_recurrence": 0.1,
            "semantic.operators_add": ["refrain_intensification"],
        },
        surface_operations=[
            TextCASurfaceOperation("repeat_image_cluster"),
        ],
        lakoff_frames=["CYCLE", "FLOW"],
        confidence=0.65,
        support=1,
    ),
]
