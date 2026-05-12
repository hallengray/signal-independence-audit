"""SIA Screen 2 — Lift test (the headline screen).

Does the gated cohort beat the ungated cohort on forward returns by a margin
worth banking on? Compares the *treatment* cohort (baseline filters AND the
candidate signal) against the *control* cohort (baseline filters only) on
three forward-return horizons: 5d, 10d, and 20d. The horizons are read from
the dataframe's ``fwd_ret_{5,10,20}d`` columns.

PASS iff the treatment mean exceeds the control mean by ≥ 0.5 × pooled-stddev
on ≥ 2 of 3 horizons. Bootstrap 95% CIs are reported per cohort and the screen
flags CI overlap at the threshold for explicit reviewer attention. Cohorts
smaller than 30 raise a review-required flag; cohorts smaller than 10 cause
the horizon to be skipped.

The **inversion clause** runs in parallel against the inverted-direction
cohort (baseline filters AND the inverted candidate signal). If that cohort
shows ≥ 1.0σ separation from control on ≥ 2 of 3 horizons AND the locked
direction failed, the ``inversion_trigger`` flag fires — the orchestrator
then maps the overall verdict to ``FAIL+INVERT``, signalling that the
wrong-direction hypothesis is worth a separate, pre-committed retest rather
than a quiet kill.
"""

from __future__ import annotations

from typing import Any, TypedDict

import numpy as np
import pandas as pd

PASS_SIGMA_THRESHOLD = 0.5
INVERSION_SIGMA_THRESHOLD = 1.0
MIN_COHORT_SIZE = 10
REVIEW_COHORT_SIZE = 30
BOOTSTRAP_RESAMPLES = 1000
HORIZONS_REQUIRED = 2
RNG_SEED = 42


class LiftResult(TypedDict):
    screen: int
    verdict: str
    evidence: dict[str, Any]
    inversion_trigger: bool
    ci_overlaps: bool
    review_required: bool
    notes: str


def _pooled_sigma(a: pd.Series, b: pd.Series) -> float:
    var_a = a.var(ddof=1)
    var_b = b.var(ddof=1)
    n_a = len(a)
    n_b = len(b)
    pooled_var = ((n_a - 1) * var_a + (n_b - 1) * var_b) / max(n_a + n_b - 2, 1)
    return float(np.sqrt(pooled_var))


def _gap_in_sigma(treatment: pd.Series, control: pd.Series) -> float:
    sigma = _pooled_sigma(treatment, control)
    if sigma <= 0:
        return 0.0
    return float((treatment.mean() - control.mean()) / sigma)


def _gap_in_cohort_sigma(cohort: pd.Series, control: pd.Series) -> float:
    """Inversion-clause measure: separation in units of the cohort's own stddev.

    The locked-direction lift uses pooled-stddev (Cohen's-d-like effect size).
    For the inversion clause the spec's "N sigma separation" reads as the
    cohort's own typical spread, which is the standard statistical convention
    when one cohort is the reference being characterised.
    """
    sigma = float(cohort.std(ddof=1))
    if sigma <= 0:
        return 0.0
    return float((cohort.mean() - control.mean()) / sigma)


def _bootstrap_ci(
    series: pd.Series, n_resamples: int = BOOTSTRAP_RESAMPLES
) -> tuple[float, float]:
    rng = np.random.default_rng(RNG_SEED)
    arr = series.to_numpy()
    means = np.array(
        [
            rng.choice(arr, size=len(arr), replace=True).mean()
            for _ in range(n_resamples)
        ]
    )
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def evaluate_lift(
    *,
    control_b: dict[int, pd.Series],
    treatment: dict[int, pd.Series],
    inversion: dict[int, pd.Series],
) -> LiftResult:
    horizons = sorted(treatment.keys())
    notes_parts: list[str] = []
    per_horizon: list[dict[str, Any]] = []
    horizons_passing = 0
    ci_overlaps = False
    review_required = False
    skipped = False

    for h in horizons:
        t = treatment[h]
        c = control_b[h]
        if len(t) < MIN_COHORT_SIZE:
            skipped = True
            notes_parts.append(f"h={h}: cohort_size_too_small ({len(t)})")
            per_horizon.append(
                {
                    "horizon": h,
                    "treatment_n": len(t),
                    "control_n": len(c),
                    "gap_sigma": None,
                    "verdict": "SKIP",
                }
            )
            continue
        if len(t) < REVIEW_COHORT_SIZE:
            review_required = True
            notes_parts.append(
                f"h={h}: cohort_size {len(t)} < 30 -> review_required"
            )
        gap = _gap_in_sigma(t, c)
        ci_t = _bootstrap_ci(t)
        ci_c = _bootstrap_ci(c)
        passes = gap >= PASS_SIGMA_THRESHOLD
        if passes:
            horizons_passing += 1
        # CI overlap: treatment lower CI <= control upper CI suggests noise.
        if passes and ci_t[0] <= ci_c[1]:
            ci_overlaps = True
        per_horizon.append(
            {
                "horizon": h,
                "treatment_n": len(t),
                "control_n": len(c),
                "treatment_mean": float(t.mean()),
                "control_mean": float(c.mean()),
                "gap_sigma": gap,
                "treatment_ci": ci_t,
                "control_ci": ci_c,
                "verdict": "PASS" if passes else "FAIL",
            }
        )

    locked_verdict = (
        "PASS" if horizons_passing >= HORIZONS_REQUIRED and not skipped else "FAIL"
    )

    # Inversion clause: same machinery applied to inverted cohort.
    inv_horizons_passing = 0
    inv_per_horizon: list[dict[str, Any]] = []
    for h in horizons:
        inv = inversion.get(h)
        c = control_b[h]
        if inv is None or len(inv) < MIN_COHORT_SIZE:
            inv_per_horizon.append({"horizon": h, "verdict": "SKIP"})
            continue
        gap = _gap_in_cohort_sigma(inv, c)
        passes = gap >= INVERSION_SIGMA_THRESHOLD
        if passes:
            inv_horizons_passing += 1
        inv_per_horizon.append(
            {
                "horizon": h,
                "inversion_n": len(inv),
                "gap_sigma": gap,
                "verdict": "PASS" if passes else "FAIL",
            }
        )
    inversion_trigger = (
        locked_verdict == "FAIL" and inv_horizons_passing >= HORIZONS_REQUIRED
    )

    return {
        "screen": 2,
        "verdict": locked_verdict,
        "evidence": {
            "horizons": per_horizon,
            "horizons_passing": horizons_passing,
            "inversion": inv_per_horizon,
            "inversion_horizons_passing": inv_horizons_passing,
        },
        "inversion_trigger": inversion_trigger,
        "ci_overlaps": ci_overlaps,
        "review_required": review_required,
        "notes": "; ".join(notes_parts)
        or f"horizons_passing={horizons_passing}/{len(horizons)}",
    }
