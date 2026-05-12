"""SIA Screen 3 — Hyperparameter-collapse test (Jaccard overlap).

Across a 5×5 grid of nearby hyperparameter settings, do the resulting trade
sets remain meaningfully distinct? If every grid point picks essentially the
same candles, the signal is collapsed onto one effective hyperparameter and
a downstream walk-forward optimisation will just re-fit that one — the test
catches strategies whose apparent tunability is illusory.

PASS iff the **mean pairwise Jaccard overlap** across all C(25,2)=300 grid-
point pairs is ≤ 0.85. Higher overlap means the grid is collapsing onto a
single entry set, which is the failure mode this screen exists to detect.
LOWER overlap is healthier.

In the original case study the grid axes were ``atr_mult × funding_threshold_pct``;
the framework is agnostic to which axes you pick — the caller builds the
``grid`` dict mapping hyperparameter-tuples to sets of admitted-candle indices.
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
