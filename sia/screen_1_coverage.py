"""SIA Screen 1: coverage test.

Counts candles satisfying macro, breakout, gate, and the full conjunction.
PASS iff:
  - new-gate reduces trade frequency by >= 20% vs macro+breakout, AND
  - full conjunction yields >= 30 trades across training.
"""

from __future__ import annotations

from typing import Any, TypedDict

import pandas as pd


class CoverageResult(TypedDict):
    screen: int
    verdict: str  # "PASS" | "FAIL"
    evidence: dict[str, Any]
    notes: str


MIN_REDUCTION_PCT = 0.20
MIN_CONJUNCTION_TRADES = 30


def evaluate_coverage(df: pd.DataFrame) -> CoverageResult:
    """df has boolean columns: macro_pass, breakout_pass, funding_gate_pass."""
    n_macro = int(df["macro_pass"].sum())
    n_macro_breakout = int((df["macro_pass"] & df["breakout_pass"]).sum())
    n_conjunction = int(
        (df["macro_pass"] & df["breakout_pass"] & df["funding_gate_pass"]).sum()
    )

    if n_macro_breakout == 0:
        reduction_pct = 0.0
    else:
        reduction_pct = 1.0 - (n_conjunction / n_macro_breakout)

    verdict = "PASS"
    notes_parts: list[str] = []

    if reduction_pct < MIN_REDUCTION_PCT:
        verdict = "FAIL"
        notes_parts.append(
            f"gate is redundant: reduction {reduction_pct:.1%} < {MIN_REDUCTION_PCT:.0%}"
        )

    if n_conjunction < MIN_CONJUNCTION_TRADES:
        verdict = "FAIL"
        notes_parts.append(
            f"gate is over-restrictive: {n_conjunction} trades < {MIN_CONJUNCTION_TRADES}"
        )

    if verdict == "PASS":
        notes_parts.append(
            f"reduction {reduction_pct:.1%}, conjunction trades {n_conjunction}"
        )

    return {
        "screen": 1,
        "verdict": verdict,
        "evidence": {
            "n_macro": n_macro,
            "n_macro_breakout": n_macro_breakout,
            "n_conjunction": n_conjunction,
            "reduction_pct": reduction_pct,
        },
        "notes": "; ".join(notes_parts),
    }
