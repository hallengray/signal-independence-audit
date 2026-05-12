"""Tests for SIA Screen 2: lift test."""

from __future__ import annotations

import numpy as np
import pandas as pd

from sia.screen_2_lift import evaluate_lift

RNG_SEED = 42


def _synthetic_returns(
    n_control: int, n_treatment: int, gap_sigma: float, *, rng=None
) -> tuple[pd.Series, pd.Series]:
    """Two Gaussian samples: control mean 0, treatment mean = gap_sigma * pooled_sigma."""
    if rng is None:
        rng = np.random.default_rng(RNG_SEED)
    sigma = 0.02
    control = pd.Series(rng.normal(0.0, sigma, size=n_control))
    treatment = pd.Series(rng.normal(gap_sigma * sigma, sigma, size=n_treatment))
    return control, treatment


def test_parametric_passes_at_0_5_sigma_on_two_of_three_horizons() -> None:
    rng = np.random.default_rng(RNG_SEED)
    # Three horizons: 5d, 10d, 20d. Make 5d and 10d show 0.6σ, 20d show 0.2σ.
    horizons = {
        5: _synthetic_returns(1000, 200, 0.6, rng=rng),
        10: _synthetic_returns(1000, 200, 0.6, rng=rng),
        20: _synthetic_returns(1000, 200, 0.2, rng=rng),
    }
    treatment_series = {h: t for h, (_, t) in horizons.items()}
    control_series = {h: c for h, (c, _) in horizons.items()}
    inversion_series = {h: c.iloc[:200] for h, c in control_series.items()}
    out = evaluate_lift(
        control_b=control_series, treatment=treatment_series, inversion=inversion_series
    )
    assert out["verdict"] == "PASS"
    assert out["evidence"]["horizons_passing"] >= 2


def test_parametric_fails_at_0_5_sigma_on_only_one_horizon() -> None:
    rng = np.random.default_rng(RNG_SEED)
    horizons = {
        5: _synthetic_returns(1000, 200, 0.6, rng=rng),
        10: _synthetic_returns(1000, 200, 0.2, rng=rng),
        20: _synthetic_returns(1000, 200, 0.2, rng=rng),
    }
    treatment_series = {h: t for h, (_, t) in horizons.items()}
    control_series = {h: c for h, (c, _) in horizons.items()}
    inversion_series = {h: c.iloc[:200] for h, c in control_series.items()}
    out = evaluate_lift(
        control_b=control_series, treatment=treatment_series, inversion=inversion_series
    )
    assert out["verdict"] == "FAIL"


def test_inversion_triggers_at_1_sigma_on_two_of_three_horizons() -> None:
    rng = np.random.default_rng(RNG_SEED)
    # Treatment FAILS its parametric on every horizon (0.2σ). But the
    # inversion direction shows 1.1σ on 5d and 10d.
    treatment = {
        h: pd.Series(rng.normal(0.2 * 0.02, 0.02, size=200)) for h in (5, 10, 20)
    }
    control_b = {
        h: pd.Series(rng.normal(0.0, 0.02, size=1000)) for h in (5, 10, 20)
    }
    inversion = {
        5: pd.Series(rng.normal(1.1 * 0.02, 0.02, size=200)),
        10: pd.Series(rng.normal(1.1 * 0.02, 0.02, size=200)),
        20: pd.Series(rng.normal(0.2 * 0.02, 0.02, size=200)),
    }
    out = evaluate_lift(control_b=control_b, treatment=treatment, inversion=inversion)
    assert out["verdict"] == "FAIL"
    assert out["inversion_trigger"] is True


def test_cohort_under_10_marks_skip() -> None:
    rng = np.random.default_rng(RNG_SEED)
    treatment = {5: pd.Series(rng.normal(0.0, 0.02, size=9))}
    control_b = {5: pd.Series(rng.normal(0.0, 0.02, size=1000))}
    inversion = {5: pd.Series(rng.normal(0.0, 0.02, size=200))}
    out = evaluate_lift(control_b=control_b, treatment=treatment, inversion=inversion)
    assert "cohort_size_too_small" in out["notes"].lower()


def test_cohort_under_30_marks_review_required() -> None:
    rng = np.random.default_rng(RNG_SEED)
    treatment = {h: pd.Series(rng.normal(0.6 * 0.02, 0.02, size=20)) for h in (5, 10, 20)}
    control_b = {h: pd.Series(rng.normal(0.0, 0.02, size=1000)) for h in (5, 10, 20)}
    inversion = {h: pd.Series(rng.normal(0.0, 0.02, size=200)) for h in (5, 10, 20)}
    out = evaluate_lift(control_b=control_b, treatment=treatment, inversion=inversion)
    assert out["review_required"] is True
