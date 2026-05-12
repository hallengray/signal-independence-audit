"""SIA Screen 4: information split.

Bin candidate candles by funding tercile vs realised-vol tercile (control).
For each binning compute {mean 10d fwd ret, win rate, Sharpe per bin}. PASS
iff funding-tercile binning shows wider tercile separation than vol-tercile
control on >= 2 of 3 metrics.
"""

from __future__ import annotations

from typing import Any, TypedDict

import numpy as np
import pandas as pd

METRICS_REQUIRED = 2


class InfoSplitResult(TypedDict):
    screen: int
    verdict: str
    evidence: dict[str, Any]
    notes: str


def _tercile_metrics(df: pd.DataFrame) -> dict[str, float]:
    """df has columns: bin (low/mid/high), fwd_ret_10d."""
    out: dict[str, float] = {}
    for label in ("low", "mid", "high"):
        bin_df = df[df["bin"] == label]
        if bin_df.empty:
            out[f"{label}_mean"] = float("nan")
            out[f"{label}_winrate"] = float("nan")
            out[f"{label}_sharpe"] = float("nan")
            continue
        out[f"{label}_mean"] = float(bin_df["fwd_ret_10d"].mean())
        out[f"{label}_winrate"] = float((bin_df["fwd_ret_10d"] > 0).mean())
        sd = float(bin_df["fwd_ret_10d"].std(ddof=1))
        out[f"{label}_sharpe"] = (
            float(bin_df["fwd_ret_10d"].mean()) / sd if sd > 0 else 0.0
        )
    return out


def _separation(metrics: dict[str, float], stat: str) -> float:
    """Max-minus-min across the three terciles."""
    vals = [metrics[f"{label}_{stat}"] for label in ("low", "mid", "high")]
    vals = [v for v in vals if not np.isnan(v)]
    if not vals:
        return 0.0
    return max(vals) - min(vals)


def evaluate_information_split(
    *,
    funding_binned: pd.DataFrame,
    vol_binned: pd.DataFrame,
) -> InfoSplitResult:
    fm = _tercile_metrics(funding_binned)
    vm = _tercile_metrics(vol_binned)

    funding_seps = {stat: _separation(fm, stat) for stat in ("mean", "winrate", "sharpe")}
    vol_seps = {stat: _separation(vm, stat) for stat in ("mean", "winrate", "sharpe")}

    funding_wins = sum(1 for stat in funding_seps if funding_seps[stat] > vol_seps[stat])
    verdict = "PASS" if funding_wins >= METRICS_REQUIRED else "FAIL"
    return {
        "screen": 4,
        "verdict": verdict,
        "evidence": {
            "funding_metrics": fm,
            "vol_metrics": vm,
            "funding_separations": funding_seps,
            "vol_separations": vol_seps,
            "funding_wins": funding_wins,
        },
        "notes": (
            f"funding wider on {funding_wins}/3 metrics "
            f"(separation thresholds: mean / winrate / sharpe)"
        ),
    }
