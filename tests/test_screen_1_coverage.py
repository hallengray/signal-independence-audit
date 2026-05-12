"""Tests for SIA Screen 1: coverage."""

from __future__ import annotations

import pandas as pd

from sia.screen_1_coverage import evaluate_coverage


def _frame(macro: list[bool], breakout: list[bool], gate: list[bool]) -> pd.DataFrame:
    return pd.DataFrame({
        "macro_pass": macro,
        "breakout_pass": breakout,
        "funding_gate_pass": gate,
    })


def test_passes_with_moderate_reduction() -> None:
    # 100 candles. 60 macro+breakout pass. 30 (50% reduction) macro+breakout+gate pass.
    n = 100
    macro = [True] * n
    breakout = [True] * 60 + [False] * 40
    gate = [True] * 30 + [False] * 70
    out = evaluate_coverage(_frame(macro, breakout, gate))
    assert out["verdict"] == "PASS"
    assert 0.45 < out["evidence"]["reduction_pct"] < 0.55


def test_fails_when_reduction_under_20_pct() -> None:
    # macro+breakout = 50 candles; macro+breakout+gate = 41 (18% reduction).
    n = 100
    macro = [True] * n
    breakout = [True] * 50 + [False] * 50
    gate = [True] * 41 + [False] * 59
    out = evaluate_coverage(_frame(macro, breakout, gate))
    assert out["verdict"] == "FAIL"
    assert "redundant" in out["notes"].lower()


def test_fails_when_under_30_trades() -> None:
    # conjunction yields 29 candles only.
    n = 100
    macro = [True] * n
    breakout = [True] * 50 + [False] * 50
    gate = [True] * 29 + [False] * 71
    out = evaluate_coverage(_frame(macro, breakout, gate))
    assert out["verdict"] == "FAIL"
    assert "over-restrictive" in out["notes"].lower() or "trades" in out["notes"].lower()


def test_passes_at_30_trades_exactly() -> None:
    n = 200
    macro = [True] * n
    breakout = [True] * 100 + [False] * 100
    gate = [True] * 30 + [False] * 170
    out = evaluate_coverage(_frame(macro, breakout, gate))
    # 30 trades is exactly the threshold; reduction is 70%, well above 20%.
    assert out["verdict"] == "PASS"
