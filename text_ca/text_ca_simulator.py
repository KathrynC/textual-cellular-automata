"""Minimal synchronous simulator for textual semantic cellular automata."""

from __future__ import annotations

import random
from collections import defaultdict
from typing import Dict, List, Sequence, Tuple

from .lakoff_taxonomy import TAXONOMY
from .text_ca_rules import DEFAULT_TEXT_CA_RULES, TextCARule, apply_state_updates, rule_matches
from .text_ca_schema import TextCARunRecord, TextCellState


def _compute_text_cell_compatibility(cell_a: TextCellState, cell_b: TextCellState) -> float:
    """Compute Lakoff frame compatibility between two cells.

    Returns 0.0-1.0 based on Jaccard similarity of lakoff_frames
    with a bonus for commonly_cooccurs relationships.
    """
    frames_a = set(cell_a.semantic.lakoff_frames)
    frames_b = set(cell_b.semantic.lakoff_frames)
    if not frames_a and not frames_b:
        return 0.0

    # Jaccard similarity
    intersection = frames_a & frames_b
    union = frames_a | frames_b
    jaccard = len(intersection) / len(union) if union else 0.0

    # Bonus for commonly_cooccurs relationships
    cooccur_bonus = 0.0
    for fid in frames_a:
        try:
            frame = TAXONOMY.get(fid)
            for co in frame.commonly_cooccurs:
                if co in frames_b:
                    cooccur_bonus += 0.05
        except KeyError:
            pass
    cooccur_bonus = min(cooccur_bonus, 0.3)

    return min(1.0, jaccard + cooccur_bonus)


def build_local_neighborhood(
    states: Sequence[TextCellState], index: int
) -> Dict[str, List[Tuple[TextCellState, float]]]:
    """Build a weighted neighborhood around one state.

    Returns dict mapping neighborhood type to list of (state, compatibility_weight) tuples.
    """
    state = states[index]
    thread_id = state.cell.coordinates.thread_id
    iteration = state.cell.coordinates.iteration

    neighborhood: Dict[str, List[Tuple[TextCellState, float]]] = defaultdict(list)
    # Sequence-adjacent cells get a minimum proximity weight of 0.55
    # to allow contagion even before shared frames develop
    if index > 0:
        w = max(0.55, _compute_text_cell_compatibility(state, states[index - 1]))
        neighborhood["prev_seq"].append((states[index - 1], w))
    if index + 1 < len(states):
        w = max(0.55, _compute_text_cell_compatibility(state, states[index + 1]))
        neighborhood["next_seq"].append((states[index + 1], w))

    for other in states:
        if other is state:
            continue
        if other.cell.coordinates.thread_id == thread_id and other.cell.coordinates.iteration == iteration:
            w = _compute_text_cell_compatibility(state, other)
            neighborhood["same_thread_window"].append((other, w))

    return dict(neighborhood)


# Templatic surface operation transforms: operation_name -> (pattern, replacement)
# Each maps a source word/pattern to a transformed variant.
SURFACE_OPERATION_TEMPLATES: Dict[str, List[Tuple[str, str]]] = {
    "institution_to_stage_metaphor": [
        ("form", "script"),
        ("office", "stage"),
        ("procedure", "performance"),
        ("meeting", "rehearsal"),
        ("report", "monologue"),
    ],
    "add_recording_lexicon": [
        ("said", "recorded"),
        ("spoke", "transmitted"),
        ("wrote", "logged"),
        ("heard", "monitored"),
    ],
    "echo_split": [
        ("voice", "voice and its echo"),
        ("thought", "thought and its double"),
        ("word", "word and its reflection"),
    ],
    "ritual_closure": [
        ("stopped", "fell silent, as in benediction"),
        ("ended", "ceased, blessed into stillness"),
        ("left", "departed, absolved"),
    ],
    "repeat_image_cluster": [
        ("light", "light, again light"),
        ("fire", "fire, again fire"),
        ("window", "window upon window"),
    ],
    "refrain_intensification": [
        ("again", "again, and again"),
        ("once", "once, and once more"),
    ],
    "semantic_intensification": [],  # no-op for generic motif additions
    "gothic_doubling": [
        ("room", "room and its shadow-room"),
        ("house", "house and the house that watches"),
        ("door", "door and the door behind the door"),
    ],
    "temporal_fold": [
        ("remembered", "remembered, or was remembered by"),
        ("before", "before, which was also after"),
    ],
    "cascade_metaphor": [
        ("fell", "fell, and the falling spread"),
        ("broke", "broke, and the breaking echoed"),
        ("collapsed", "collapsed, each collapse seeding the next"),
    ],
}


def _apply_templatic_transforms(text: str, operations: List[str]) -> str:
    """Apply deterministic lexical substitutions from SURFACE_OPERATION_TEMPLATES."""
    result = text
    for op_name in operations:
        templates = SURFACE_OPERATION_TEMPLATES.get(op_name, [])
        for pattern, replacement in templates:
            # Case-insensitive single replacement per pattern
            lower = result.lower()
            idx = lower.find(pattern)
            if idx >= 0:
                result = result[:idx] + replacement + result[idx + len(pattern):]
                break  # one substitution per operation
    return result


def realize_surface_text(
    state: TextCellState,
    fired_rules: List[TextCARule],
    mode: str = "templatic",
) -> str:
    """Surface realization with 3 modes.

    Modes:
        conservative: original text + operator markers (debugging)
        templatic: deterministic lexical substitutions from templates
        hybrid: templatic + optional narrative enrichment wiring
    """
    operators: List[str] = []
    for rule in fired_rules:
        operators.extend(op.operation for op in rule.surface_operations)

    if not operators:
        return state.cell.surface_text

    if mode == "conservative":
        marker = " | ".join(sorted(set(operators)))
        return f"{state.cell.surface_text} [{marker}]"

    if mode in ("templatic", "hybrid"):
        text = _apply_templatic_transforms(state.cell.surface_text, operators)

        if mode == "hybrid":
            # Wire to narrative_enrichment if available
            try:
                from .mathematical_metaphors import poetic_rewrite
                flagged = poetic_rewrite(text)
                if flagged:
                    # Apply first alternative found
                    first = flagged[0]
                    text = text.replace(first["phrase"], first["alternative"])
            except (ImportError, Exception):
                pass

        return text

    return state.cell.surface_text


def _compute_text_rule_compatibility(rule: TextCARule, state: TextCellState) -> float:
    """Compute compatibility between a rule and a cell state (0.5-2.0 range).

    Considers attractor type alignment between rule's Lakoff frames and
    cell's dynamical signatures.
    """
    if not rule.lakoff_frames:
        return 1.0  # neutral if rule has no frame annotation

    cell_frames = set(state.semantic.lakoff_frames)
    rule_frame_set = set(rule.lakoff_frames)

    # Frame overlap: how many of the rule's frames are present in the cell?
    if not cell_frames:
        return 0.5  # low compatibility when cell has no frames

    overlap = len(rule_frame_set & cell_frames) / len(rule_frame_set)

    # Dynamical signature alignment bonus
    dyn_bonus = 0.0
    for fid in rule.lakoff_frames:
        if fid in state.dynamical_signatures:
            sig = state.dynamical_signatures[fid]
            # Higher basin width → more stable → bonus for matching
            dyn_bonus += sig.get("basin_width", 0.5) * 0.2
    dyn_bonus = min(dyn_bonus, 0.5)

    # Map to 0.5-2.0 range: 0 overlap → 0.5, full overlap + bonus → up to 2.0
    return 0.5 + overlap * 1.0 + dyn_bonus


def _apply_frame_contagion(
    state: TextCellState,
    neighborhood: Dict[str, List[Tuple[TextCellState, float]]],
    contagion_rate: float = 0.3,
    compat_threshold: float = 0.5,
    rng: random.Random | None = None,
) -> List[str]:
    """Spread Lakoff frames from compatible neighbors to the focal cell.

    Returns list of newly acquired frame IDs.
    """
    _rng = rng or random
    current_frames = set(state.semantic.lakoff_frames)
    acquired: List[str] = []
    for bucket in neighborhood.values():
        for neighbor, weight in bucket:
            if weight < compat_threshold:
                continue
            for frame_id in neighbor.semantic.lakoff_frames:
                if frame_id not in current_frames:
                    if _rng.random() < weight * contagion_rate:
                        acquired.append(frame_id)
                        current_frames.add(frame_id)
    if acquired:
        state.semantic.lakoff_frames = sorted(current_frames)
    return acquired


def step_text_ca(
    states: Sequence[TextCellState],
    rules: Sequence[TextCARule] | None = None,
    rng: random.Random | None = None,
) -> tuple[List[TextCellState], List[str]]:
    """Advance all cells by one synchronous CA step."""

    active_rules = list(rules) if rules is not None else DEFAULT_TEXT_CA_RULES
    next_states: List[TextCellState] = []
    fired_rule_ids: List[str] = []

    for index, state in enumerate(states):
        neighborhood = build_local_neighborhood(states, index)
        applicable = [rule for rule in active_rules if rule_matches(rule, state, neighborhood)]

        # Sort by confidence * rule-cell compatibility, apply top 3
        scored = [(rule, rule.confidence * _compute_text_rule_compatibility(rule, state)) for rule in applicable]
        scored.sort(key=lambda x: x[1], reverse=True)
        top_rules = [rule for rule, _ in scored[:3]]

        next_state = state.copy_for_iteration(state.cell.coordinates.iteration + 1)
        for rule in top_rules:
            apply_state_updates(next_state, rule.state_updates)
            fired_rule_ids.append(rule.rule_id)

        # Frame contagion: compatible neighbors spread Lakoff frames
        _apply_frame_contagion(next_state, neighborhood, rng=rng)

        next_state.cell.surface_text = realize_surface_text(next_state, top_rules)
        next_states.append(next_state)

    return next_states, fired_rule_ids


def simulate_text_ca(
    initial_states: Sequence[TextCellState],
    steps: int,
    rules: Sequence[TextCARule] | None = None,
    run_id: str = "text_ca_run",
    seed: int | None = None,
) -> TextCARunRecord:
    """Run a textual CA for a fixed number of synchronous steps."""

    rng = random.Random(seed) if seed is not None else random.Random()
    history: List[List[TextCellState]] = [list(initial_states)]
    fired_per_step: List[List[str]] = []
    realized_text_by_step: List[List[str]] = [[state.cell.surface_text for state in initial_states]]

    current = list(initial_states)
    for _ in range(steps):
        current, fired_rule_ids = step_text_ca(current, rules, rng=rng)
        history.append(current)
        fired_per_step.append(fired_rule_ids)
        realized_text_by_step.append([state.cell.surface_text for state in current])

    return TextCARunRecord(
        run_id=run_id,
        source_doc_id=initial_states[0].cell.doc_id if initial_states else "unknown",
        steps=steps,
        state_history=history,
        fired_rule_ids=fired_per_step,
        realized_text_by_step=realized_text_by_step,
    )
