"""Macro filter: daily close above daily EMA.

A trivial pandas comparison extracted for naming clarity. Per Phase 4 spec
§9.5, deliberately not unit-tested (pandas owns the underlying op).
"""

from __future__ import annotations

import pandas as pd


def macro_filter(daily_close: pd.Series, daily_ema: pd.Series) -> pd.Series:
    """Returns True where the daily close exceeds the daily EMA."""
    return daily_close > daily_ema
