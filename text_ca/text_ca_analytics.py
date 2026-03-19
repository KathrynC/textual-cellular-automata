"""Analytics for textual semantic cellular automata runs."""

from __future__ import annotations

import sys
from collections import Counter
from typing import Dict, List

import numpy as np

from .text_ca_schema import DEFAULT_NUMERIC_CHANNELS, TextCARunRecord, TextCellState

# Import wolfram_classify from NADJA
_NADJA_MATH = "/Users/gardenofcomputation/scenario-forward-investing-lab"
if _NADJA_MATH not in sys.path:
    sys.path.insert(0, _NADJA_MATH)
from stock_simulator.math.wolfram_classify import classify_from_trajectory as _wolfram_classify


def _read_channel_value(state: TextCellState, path: str) -> float:
    """Read a dotted numeric channel from a state."""

    current: object = state
    for segment in path.split("."):
        current = getattr(current, segment)
    return float(current)


def compute_channel_means(states: List[TextCellState]) -> Dict[str, float]:
    """Compute mean values for the default numeric channels."""

    if not states:
        return {channel: 0.0 for channel in DEFAULT_NUMERIC_CHANNELS}

    means: Dict[str, float] = {}
    for channel in DEFAULT_NUMERIC_CHANNELS:
        means[channel] = sum(_read_channel_value(state, channel) for state in states) / len(states)
    return means


def compute_motif_persistence(run: TextCARunRecord) -> Dict[str, int]:
    """Count in how many steps each motif appears."""

    persistence: Counter[str] = Counter()
    for step_states in run.state_history:
        seen = set()
        for state in step_states:
            seen.update(state.semantic.motifs)
        for motif in seen:
            persistence[motif] += 1
    return dict(persistence)


def compute_state_entropy_proxy(states: List[TextCellState]) -> float:
    """A lightweight entropy proxy over motif occupancy.

    This is intentionally simple for the initial scaffold. A more faithful
    entropy metric can be added once symbolic alphabet projections are defined.
    """

    motifs = [motif for state in states for motif in state.semantic.motifs]
    if not motifs:
        return 0.0

    counts = Counter(motifs)
    total = sum(counts.values())
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * __import__("math").log(p, 2)
    return entropy


def compute_frame_contagion_rate(run: TextCARunRecord) -> float:
    """Measure the rate of Lakoff frame spread across steps.

    Returns the average number of new frame acquisitions per cell per step.
    """
    if len(run.state_history) < 2:
        return 0.0

    total_acquisitions = 0
    total_cells = 0
    for step_idx in range(1, len(run.state_history)):
        prev_step = run.state_history[step_idx - 1]
        curr_step = run.state_history[step_idx]
        for prev_state, curr_state in zip(prev_step, curr_step):
            prev_frames = set(prev_state.semantic.lakoff_frames)
            curr_frames = set(curr_state.semantic.lakoff_frames)
            total_acquisitions += len(curr_frames - prev_frames)
            total_cells += 1

    return total_acquisitions / max(1, total_cells)


def compute_frame_diversity(states: List[TextCellState]) -> float:
    """Compute Shannon entropy of Lakoff frame distribution across cells."""
    all_frames: List[str] = []
    for state in states:
        all_frames.extend(state.semantic.lakoff_frames)
    if not all_frames:
        return 0.0

    counts = Counter(all_frames)
    total = sum(counts.values())
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * __import__("math").log(p, 2)
    return entropy


def compute_compatibility_histogram(run: TextCARunRecord) -> Dict[str, int]:
    """Histogram of frame count per cell across all steps.

    Returns dict mapping frame-count buckets to number of cell-step observations.
    """
    buckets: Counter = Counter()
    for step_states in run.state_history:
        for state in step_states:
            n = len(state.semantic.lakoff_frames)
            bucket = f"{(n // 5) * 5}-{(n // 5) * 5 + 4}"
            buckets[bucket] += 1
    return dict(buckets)


def binarize_trajectory(
    run: TextCARunRecord,
    channels: tuple[str, ...] | None = None,
    threshold: float = 0.5,
) -> List[np.ndarray]:
    """Convert multi-channel text CA trajectory to binary for Wolfram classification.

    Each step becomes a 1D binary array: one bit per (cell, channel) pair,
    set to 1 if the channel value >= threshold, else 0.

    Parameters
    ----------
    run : TextCARunRecord
        A completed text CA run.
    channels : tuple of str, optional
        Numeric channel paths to binarize. Defaults to DEFAULT_NUMERIC_CHANNELS.
    threshold : float
        Value at or above which a channel is considered "on".

    Returns
    -------
    List[np.ndarray]
        Binary trajectory suitable for wolfram_classify.classify_from_trajectory.
    """
    channels = channels or DEFAULT_NUMERIC_CHANNELS
    trajectory: List[np.ndarray] = []
    for step_states in run.state_history:
        bits: List[int] = []
        for state in step_states:
            for ch in channels:
                val = _read_channel_value(state, ch)
                bits.append(1 if val >= threshold else 0)
        trajectory.append(np.array(bits, dtype=np.int64))
    return trajectory


def wolfram_classify_text_ca(
    run: TextCARunRecord,
    channels: tuple[str, ...] | None = None,
    threshold: float = 0.5,
) -> Dict:
    """Classify a text CA run into Wolfram classes I-IV.

    Binarizes the multi-channel semantic trajectory then delegates
    to stock_simulator.math.wolfram_classify.classify_from_trajectory.
    """
    binary_traj = binarize_trajectory(run, channels=channels, threshold=threshold)
    return _wolfram_classify(binary_traj)


def analyze_text_ca_run(run: TextCARunRecord) -> Dict[str, object]:
    """Compute initial textual CA observables for a run."""

    entropy_curve = [compute_state_entropy_proxy(step_states) for step_states in run.state_history]
    mean_channels_by_step = [compute_channel_means(step_states) for step_states in run.state_history]
    motif_persistence = compute_motif_persistence(run)
    rule_counts = Counter(rule_id for step in run.fired_rule_ids for rule_id in step)

    quiescence_time = None
    for index, step in enumerate(run.fired_rule_ids, start=1):
        if not step:
            quiescence_time = index
            break

    frame_contagion_rate = compute_frame_contagion_rate(run)
    frame_diversity = [compute_frame_diversity(step_states) for step_states in run.state_history]
    compatibility_histogram = compute_compatibility_histogram(run)

    wolfram = wolfram_classify_text_ca(run)

    return {
        "entropy_curve": entropy_curve,
        "mean_channels_by_step": mean_channels_by_step,
        "motif_persistence": motif_persistence,
        "rule_counts": dict(rule_counts),
        "quiescence_time": quiescence_time,
        "frame_contagion_rate": frame_contagion_rate,
        "frame_diversity": frame_diversity,
        "compatibility_histogram": compatibility_histogram,
        "wolfram_class": wolfram["wolfram_class"],
        "wolfram_evidence": wolfram["evidence_scores"],
        "wolfram_metrics": {
            k: wolfram[k]
            for k in ("entropy_rate", "lyapunov_estimate", "periodicity", "transient_length")
        },
    }
