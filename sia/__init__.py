"""Signal Independence Audit (SIA) — pre-hyperopt screening framework.

A four-screen test (coverage, lift, jaccard, information-split) for
whether a candidate signal adds information over a baseline. Originally
developed for cryptocurrency strategy triage (see case-study/ for the
worked example) but the methodology applies to any signal hypothesis
on any asset class.

Quick start (CLI):
    python -m sia.orchestrator --pair BTC/USDT --train-start 2021-01-01 \\
        --train-end 2024-12-31 --out report.json

The orchestrator's main() entry point is the canonical interface. It
emits exit code 0 on PASS, 1 on FAIL, and 2 on FAIL+INVERT (the
inversion-clause triggered).
"""

from sia.orchestrator import main

__all__ = ["main"]
