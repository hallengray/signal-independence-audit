"""Funding-gate utilities: load 8h funding aligned to 4h candle index with
strict-less-than look-ahead enforcement, and the funding-gate boolean.

The look-ahead invariant is enforced via pandas.merge_asof(
allow_exact_matches=False) inside load_funding_aligned_to_4h. There is no
other code path by which strategy or SIA code can obtain aligned funding
values — this is the single enforcement point.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Final

import pandas as pd

MAX_GAP_HOURS: Final[int] = 24


def _load_and_validate_raw(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"funding rate file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        rows = json.load(f)
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"funding file is empty or not a list: {path}")
    # Validate every row before constructing the DataFrame.
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"row {i} is not an object: {row!r}")
        if "fundingTime" not in row or "fundingRate" not in row:
            raise ValueError(f"row {i} missing fundingTime or fundingRate: {row!r}")
        if row["fundingRate"] is None:
            raise ValueError(
                f"row {i} has null fundingRate at fundingTime={row['fundingTime']}"
            )
        try:
            float(row["fundingRate"])
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"row {i} has malformed fundingRate at "
                f"fundingTime={row['fundingTime']}: {row['fundingRate']!r}"
            ) from exc
    df = pd.DataFrame(rows)
    df["fundingTime"] = pd.to_datetime(df["fundingTime"], unit="ms", utc=True)
    df["fundingRate"] = df["fundingRate"].astype(float)
    # Monotonic timestamp check.
    if not df["fundingTime"].is_monotonic_increasing:
        raise ValueError(f"fundingTime timestamps are not monotonic in {path}")
    # Gap check.
    deltas = df["fundingTime"].diff().dt.total_seconds().div(3600.0)
    over_threshold = deltas[deltas > MAX_GAP_HOURS]
    if not over_threshold.empty:
        idx = int(over_threshold.index[0])
        prev_ts = df["fundingTime"].iloc[idx - 1]
        this_ts = df["fundingTime"].iloc[idx]
        raise ValueError(
            f"funding gap > 24h in {path}: between {prev_ts} and {this_ts} "
            f"({over_threshold.iloc[0]:.1f} hours)"
        )
    return df[["fundingTime", "fundingRate"]]


def load_funding_aligned_to_4h(
    funding_json_path: Path,
    candle_index: pd.DatetimeIndex,
) -> pd.Series:
    """Load 8h funding rates and reindex to a 4h candle index using strict
    less-than look-ahead semantics.

    A 4h candle at time `t` may use only funding rows where `fundingTime < t`
    (strict). Implemented via merge_asof(direction='backward',
    allow_exact_matches=False). The returned Series is indexed by
    candle_index; values are pandas NaN where no funding history exists yet.
    """
    if not isinstance(candle_index, pd.DatetimeIndex):
        raise TypeError(f"candle_index must be a DatetimeIndex, got {type(candle_index)}")
    raw = _load_and_validate_raw(Path(funding_json_path))
    left = pd.DataFrame({"candle_open": candle_index}).reset_index(drop=True)
    # Normalize merge-key dtypes: pd.date_range may use us-precision while
    # pd.to_datetime(unit='ms') uses ms-precision. merge_asof requires
    # identical dtypes on the join keys. Casting is purely representational
    # and does not affect the strict-less-than semantics.
    left["candle_open"] = left["candle_open"].astype(raw["fundingTime"].dtype)
    aligned = pd.merge_asof(
        left=left,
        right=raw,
        left_on="candle_open",
        right_on="fundingTime",
        direction="backward",
        allow_exact_matches=False,
    )
    # Belt-and-braces runtime assertion (cheap, runs once per backtest).
    valid = aligned["fundingTime"].notna()
    if valid.any():
        assert (
            aligned.loc[valid, "fundingTime"] < aligned.loc[valid, "candle_open"]
        ).all(), "look-ahead invariant violated"
    out = pd.Series(aligned["fundingRate"].values, index=candle_index, name="funding")
    return out


CANDLES_PER_DAY: Final[int] = 6  # 4h candles


def funding_gate(
    funding_4h: pd.Series,
    rolling_days: int = 7,
    lookback_days: int = 90,
    threshold_pct: float = 0.60,
) -> pd.Series:
    """Per-candle boolean: True when the rolling-mean funding is strictly
    below the threshold-percentile of the trailing-lookback funding window.

    Returns False during the (rolling_days + lookback_days) warm-up period.
    Strict less-than: equality returns False.
    """
    if not 0.0 < threshold_pct < 1.0:
        raise ValueError(f"threshold_pct must be in (0, 1), got {threshold_pct}")
    rolling_window = rolling_days * CANDLES_PER_DAY
    lookback_window = lookback_days * CANDLES_PER_DAY
    rolling_mean = funding_4h.rolling(window=rolling_window, min_periods=rolling_window).mean()
    # Trailing-window percentile, EXCLUDING the current rolling-mean window.
    # The strategy compares "current 7d mean" against "the 60th pct of the 90
    # days that came before". Disjoint windows make the comparison clean and
    # match the spec's ~97-day warm-up (rolling_days + lookback_days).
    # window=lookback_window + 1 (and matching min_periods): the +1 makes the
    # warm-up exactly rolling_days + lookback_days = 97 days. Without it, the
    # gate would first fire at 96.83 days elapsed (one 4h candle early).
    # pandas requires min_periods <= window, so both are bumped together; the
    # trailing window therefore contains 541 candles (90 days + 1 candle).
    trailing_pct = (
        funding_4h.shift(rolling_window)
        .rolling(window=lookback_window + 1, min_periods=lookback_window + 1)
        .quantile(threshold_pct)
    )
    gate = (rolling_mean < trailing_pct).fillna(False)
    return gate.astype(bool)
