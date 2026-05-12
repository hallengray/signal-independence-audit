#!/usr/bin/env python3
"""SIA orchestrator: build training-window inputs, run all 4 screens, write verdict report.

Usage:
    python -m sia.orchestrator \\
        --pair BTC/USDT --pair ETH/USDT \\
        --train-start 2021-04-08 --train-end 2024-12-31 \\
        --out report.json

Exit codes:
    0 — PASS (all 4 screens pass; proceed to hyperopt)
    1 — FAIL (no inversion trigger; kill ADR documents the failure)
    2 — FAIL+INVERT (inversion clause triggered; investigate the wrong-direction hypothesis)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
from typing import Any

import pandas as pd

from sia._internal import (
    donchian_high,
    funding_gate,
    load_funding_aligned_to_4h,
    macro_filter,
)
from sia.screen_1_coverage import evaluate_coverage
from sia.screen_2_lift import evaluate_lift
from sia.screen_3_jaccard import evaluate_jaccard
from sia.screen_4_information_split import evaluate_information_split

HORIZONS = (5, 10, 20)  # forward-return horizons in days
DONCHIAN_ENTRY = 20
MACRO_EMA = 200
FUNDING_ROLLING_DAYS = 7
FUNDING_LOOKBACK_DAYS = 90
FUNDING_THRESHOLD_PCT = 0.60
INVERSION_THRESHOLD_PCT = 0.40  # symmetric inversion of 0.60


def _load_ohlcv(pair: str, timeframe: str, data_dir: Path) -> pd.DataFrame:
    """Load Freqtrade-format OHLCV JSON for a single pair/timeframe.

    Expects `<data_dir>/<PAIR_underscored>-<timeframe>.json` containing a
    list of [timestamp_ms, open, high, low, close, volume] rows.
    """
    pair_underscored = pair.replace("/", "_")
    path = data_dir / f"{pair_underscored}-{timeframe}.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    df = pd.DataFrame(rows, columns=["date", "open", "high", "low", "close", "volume"])
    df["date"] = pd.to_datetime(df["date"], unit="ms", utc=True)
    return df.set_index("date").sort_index()


def _build_signals(
    pair: str,
    train_start: str,
    train_end: str,
    threshold_pct: float,
    data_dir: Path,
) -> pd.DataFrame:
    """Build the per-candle dataframe needed by Screens 1, 2, 4."""
    h4 = _load_ohlcv(pair, "4h", data_dir)
    d1 = _load_ohlcv(pair, "1d", data_dir)
    h4_aug = h4.copy()
    h4_aug["donchian_high"] = donchian_high(h4_aug["high"], DONCHIAN_ENTRY)
    d1["daily_ema"] = d1["close"].ewm(span=MACRO_EMA, adjust=False).mean()
    daily_4h = d1[["close", "daily_ema"]].reindex(h4_aug.index, method="ffill")
    daily_4h = daily_4h.rename(columns={"close": "daily_close"})
    h4_aug["daily_close"] = daily_4h["daily_close"]
    h4_aug["daily_ema"] = daily_4h["daily_ema"]
    h4_aug["macro_pass"] = macro_filter(h4_aug["daily_close"], h4_aug["daily_ema"])
    h4_aug["breakout_pass"] = h4_aug["close"] > h4_aug["donchian_high"]
    pair_underscored = pair.replace("/", "_")
    funding_path = data_dir / "funding_rates" / f"{pair_underscored}-funding-8h.json"
    funding_4h = load_funding_aligned_to_4h(funding_path, h4_aug.index)
    h4_aug["funding_4h"] = funding_4h.values
    h4_aug["funding_gate_pass"] = funding_gate(
        pd.Series(h4_aug["funding_4h"].values, index=h4_aug.index),
        rolling_days=FUNDING_ROLLING_DAYS,
        lookback_days=FUNDING_LOOKBACK_DAYS,
        threshold_pct=threshold_pct,
    ).values
    # Inversion gate: funding > 40th pct (symmetric inversion of < 60th pct).
    h4_aug["funding_gate_inversion"] = ~funding_gate(
        pd.Series(h4_aug["funding_4h"].values, index=h4_aug.index),
        rolling_days=FUNDING_ROLLING_DAYS,
        lookback_days=FUNDING_LOOKBACK_DAYS,
        threshold_pct=1.0 - INVERSION_THRESHOLD_PCT,
    ).values
    for h_days in HORIZONS:
        h_candles = h_days * 6
        h4_aug[f"fwd_ret_{h_days}d"] = (
            h4_aug["close"].shift(-h_candles) / h4_aug["close"] - 1.0
        )
    h4_aug["vol_20d"] = h4_aug["close"].pct_change().rolling(20 * 6).std()
    return h4_aug.loc[train_start:train_end]


def _screen_2_cohorts(
    df: pd.DataFrame,
) -> tuple[dict[int, pd.Series], dict[int, pd.Series], dict[int, pd.Series]]:
    treatment: dict[int, pd.Series] = {}
    control_b: dict[int, pd.Series] = {}
    inversion: dict[int, pd.Series] = {}
    for h_days in HORIZONS:
        col = f"fwd_ret_{h_days}d"
        treatment_mask = (
            df["macro_pass"] & df["breakout_pass"] & df["funding_gate_pass"]
        )
        control_b_mask = df["macro_pass"] & df["breakout_pass"]
        inversion_mask = (
            df["macro_pass"] & df["breakout_pass"] & df["funding_gate_inversion"]
        )
        treatment[h_days] = df.loc[treatment_mask, col].dropna()
        control_b[h_days] = df.loc[control_b_mask, col].dropna()
        inversion[h_days] = df.loc[inversion_mask, col].dropna()
    return treatment, control_b, inversion


def _screen_3_grid(df: pd.DataFrame) -> dict[tuple[Any, ...], set[int]]:
    """5x5 grid: atr_mult x funding_threshold_pct → set of candle index ints.

    atr_mult is a stop-side parameter (doesn't affect entry candle set) so the
    grid effectively varies only the funding threshold. This is a 1×5 sweep
    duplicated 5 times to provide the Jaccard pairs the spec requires.
    """
    atr_mults = (1.5, 2.0, 2.5, 3.0, 3.5)
    thresholds = (0.40, 0.50, 0.60, 0.70, 0.80)
    grid: dict[tuple[Any, ...], set[int]] = {}
    for am, th in product(atr_mults, thresholds):
        gate = funding_gate(
            pd.Series(df["funding_4h"].values, index=df.index),
            rolling_days=FUNDING_ROLLING_DAYS,
            lookback_days=FUNDING_LOOKBACK_DAYS,
            threshold_pct=th,
        )
        mask = df["macro_pass"].to_numpy() & df["breakout_pass"].to_numpy() & gate.to_numpy()
        grid[(am, th)] = set(int(i) for i in df.index[mask].astype("int64").tolist())
    return grid


def _screen_4_terciles(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    candidates = df[df["macro_pass"] & df["breakout_pass"]].copy()
    candidates = candidates.dropna(subset=["funding_4h", "fwd_ret_10d", "vol_20d"])
    if candidates.empty:
        empty = pd.DataFrame(columns=["bin", "fwd_ret_10d"])
        return empty, empty
    # Rank first to break ties: funding_4h is highly clustered (all 4h candles
    # within an 8h funding period share the same value), so raw qcut produces
    # collapsed quantile boundaries. Rank-then-qcut guarantees three balanced
    # terciles. Within a tie-group the assignment is arbitrary but balanced.
    candidates["funding_bin"] = pd.qcut(
        candidates["funding_4h"].rank(method="first"),
        q=3,
        labels=["low", "mid", "high"],
    )
    candidates["vol_bin"] = pd.qcut(
        candidates["vol_20d"].rank(method="first"),
        q=3,
        labels=["low", "mid", "high"],
    )
    funding_binned = candidates[["funding_bin", "fwd_ret_10d"]].rename(
        columns={"funding_bin": "bin"}
    )
    vol_binned = candidates[["vol_bin", "fwd_ret_10d"]].rename(
        columns={"vol_bin": "bin"}
    )
    return funding_binned.dropna(), vol_binned.dropna()


def _write_report(out_path: Path, results: list[dict[str, Any]], overall_verdict: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    screen_names = {1: "Coverage", 2: "Lift", 3: "Jaccard", 4: "Information split"}
    lines = [
        "# Phase 4 — Signal Independence Audit (SIA) verdict",
        f"_Generated by `scripts/sia/run_sia.py` at "
        f"{datetime.now(timezone.utc).isoformat(timespec='seconds')}._",
        "",
        "---",
        "",
        f"## Headline verdict: **{overall_verdict}**",
        "",
        "## Per-screen results",
        "",
        "| # | Screen | Verdict | Notes |",
        "| - | ------ | ------- | ----- |",
    ]
    for r in results:
        lines.append(
            f"| {r['screen']} | {screen_names[r['screen']]} | "
            f"{r['verdict']} | {r['notes']} |"
        )
    lines += ["", "## Evidence", "", "```json"]
    lines.append(json.dumps(results, indent=2, default=str))
    lines += ["```", "", "_End of SIA verdict._"]
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pair", action="append", required=True)
    p.add_argument("--train-start", required=True)
    p.add_argument("--train-end", required=True)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument(
        "--data-dir",
        required=True,
        type=Path,
        help="Directory containing <PAIR>-<TIMEFRAME>.json OHLCV files in Freqtrade JSON format, plus funding_rates/<PAIR>-funding-8h.json for the funding signal.",
    )
    args = p.parse_args()

    frames: list[pd.DataFrame] = []
    for pair in args.pair:
        frames.append(
            _build_signals(
                pair,
                args.train_start,
                args.train_end,
                FUNDING_THRESHOLD_PCT,
                args.data_dir,
            )
        )
    pooled = pd.concat(frames, keys=args.pair, names=["pair", "date"])
    pooled = pooled.reset_index(level="pair")
    print(
        f"pooled signal frame: {len(pooled)} rows across {len(args.pair)} pairs",
        file=sys.stderr,
    )

    r1 = evaluate_coverage(pooled)
    treatment, control_b, inversion = _screen_2_cohorts(pooled)
    r2 = evaluate_lift(control_b=control_b, treatment=treatment, inversion=inversion)
    grid = _screen_3_grid(frames[0])
    r3 = evaluate_jaccard(grid)
    funding_binned, vol_binned = _screen_4_terciles(pooled)
    r4 = evaluate_information_split(
        funding_binned=funding_binned, vol_binned=vol_binned
    )

    results: list[dict[str, Any]] = [dict(r1), dict(r2), dict(r3), dict(r4)]
    all_pass = all(r["verdict"] == "PASS" for r in results)
    inversion_active = bool(r2.get("inversion_trigger"))
    if all_pass:
        overall = "PASS"
        exit_code = 0
    elif inversion_active:
        overall = "FAIL+INVERT"
        exit_code = 2
    else:
        overall = "FAIL"
        exit_code = 1
    _write_report(args.out, results, overall)
    print(f"SIA verdict: {overall} (exit {exit_code}) → {args.out}", file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
