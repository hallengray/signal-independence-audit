"""Signal Independence Audit (SIA) — pre-hyperopt screening framework.

A four-screen test (coverage, lift, jaccard, information-split) for
whether a candidate signal adds information over a baseline. Originally
developed for cryptocurrency strategy triage (see case-study/ for the
worked example) but the methodology applies to any signal hypothesis
on any asset class.

Two entry points:

- `sia.run_screens(pooled, jaccard_frame)` — library API. Pass a
  pre-built pooled signal dataframe (and one single-pair frame for
  Screen 3's hyperparameter grid). Returns a verdict dict with the
  PASS/FAIL/FAIL+INVERT routing + per-screen evidence. Use this from
  notebooks or any in-memory pipeline.

- `sia.main()` — CLI entry point. `python -m sia.orchestrator
  --pair BTC/USDT --train-start 2021-01-01 --train-end 2024-12-31
  --out report.json --data-dir /path/to/freqtrade-json/`. Loads data
  from disk, builds signals, calls `run_screens`, writes a Markdown
  verdict report, exits 0/1/2 for PASS/FAIL/FAIL+INVERT.
"""

from sia.orchestrator import main, run_screens

__all__ = ["main", "run_screens"]
