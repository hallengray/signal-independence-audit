"""SIA Screen 3: entry-set stability (Jaccard).

Sweep a 5×5 grid over (atr_mult, funding_threshold_pct) and compute the mean
pairwise Jaccard overlap of triggered-candle sets across all C(25,2)=300
pairs. PASS iff mean pairwise Jaccard <= 0.85.
"""

from __future__ import annotations

from itertools import combinations
from typing import Any, TypedDict

JACCARD_MAX = 0.85


class JaccardResult(TypedDict):
    screen: int
    verdict: str
    evidence: dict[str, Any]
    notes: str


def jaccard(a: set[int], b: set[int]) -> float:
    if not a and not b:
        return 1.0
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def evaluate_jaccard(grid: dict[tuple[Any, ...], set[int]]) -> JaccardResult:
    """grid maps (param_a, param_b) -> set of candle-index ints."""
    pairs = list(combinations(grid.values(), 2))
    if not pairs:
        return {
            "screen": 3,
            "verdict": "FAIL",
            "evidence": {"mean_jaccard": float("nan"), "n_pairs": 0},
            "notes": "grid empty or single-point",
        }
    values = [jaccard(a, b) for a, b in pairs]
    mean_j = sum(values) / len(values)
    verdict = "PASS" if mean_j <= JACCARD_MAX else "FAIL"
    return {
        "screen": 3,
        "verdict": verdict,
        "evidence": {
            "mean_jaccard": mean_j,
            "n_pairs": len(pairs),
            "min_jaccard": min(values),
            "max_jaccard": max(values),
        },
        "notes": f"mean_jaccard={mean_j:.3f} (threshold {JACCARD_MAX})",
    }
