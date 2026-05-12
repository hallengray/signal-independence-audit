"""Tests for SIA Screen 4: information split (funding tercile vs vol tercile)."""

from __future__ import annotations

import numpy as np
import pandas as pd

from sia.screen_4_information_split import evaluate_information_split


def _bin_data(n_per_bin: int, means: tuple[float, float, float], sigma: float = 0.02) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []
    for label, mean in zip(("low", "mid", "high"), means):
        rows.extend([(label, rng.normal(mean, sigma)) for _ in range(n_per_bin)])
    return pd.DataFrame(rows, columns=["bin", "fwd_ret_10d"])


def test_passes_when_funding_terciles_separate_more_than_vol() -> None:
    funding_binned = _bin_data(50, (0.005, 0.010, 0.015))  # 0.5pp gaps
    vol_binned = _bin_data(50, (0.008, 0.010, 0.012))      # 0.2pp gaps (control narrower)
    out = evaluate_information_split(
        funding_binned=funding_binned, vol_binned=vol_binned
    )
    assert out["verdict"] == "PASS"


def test_fails_when_vol_separates_more_than_funding() -> None:
    funding_binned = _bin_data(50, (0.008, 0.010, 0.012))  # narrow
    vol_binned = _bin_data(50, (0.005, 0.010, 0.015))      # wider control
    out = evaluate_information_split(
        funding_binned=funding_binned, vol_binned=vol_binned
    )
    assert out["verdict"] == "FAIL"
