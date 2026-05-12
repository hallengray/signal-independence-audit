"""Donchian channel indicators using .shift(1) to exclude the current candle.

This is the look-ahead guard for breakout strategies — the donchian high at
index N must NOT include candle N's own high in the rolling-window max.
"""

from __future__ import annotations

import pandas as pd


def donchian_high(high: pd.Series, period: int) -> pd.Series:
    """Rolling N-period max of `high`, shifted by one to exclude the current candle."""
    return high.rolling(window=period).max().shift(1)


def donchian_low(low: pd.Series, period: int) -> pd.Series:
    """Rolling N-period min of `low`, shifted by one to exclude the current candle."""
    return low.rolling(window=period).min().shift(1)
