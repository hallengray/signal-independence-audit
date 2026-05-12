# Signal Independence Audit (SIA)

**Signal Independence Audit (SIA)** is a pre-hyperopt screening framework for testing whether a candidate signal adds information over a baseline. The methodology applies to any signal hypothesis on any asset class; this repo's case study uses cryptocurrency as the worked example because that's the surface where the methodology was developed and stress-tested.

The four screens (coverage, lift, jaccard, information-split) run in seconds on a laptop. They are designed to catch the failure modes that would otherwise consume hours of hyperopt compute before being discovered.

## What this repo contains

- [`sia/`](./sia/) — the four-screen harness, packaged for `pip install -e .`.
- [`tests/`](./tests/) — 16 unit tests covering the screens and orchestrator. Run via `pytest`.
- [`case-study/`](./case-study/) — 10 curated documents from the original crypto project that produced this methodology. See [`case-study/00-readme.md`](./case-study/00-readme.md) for the reading guide.
- [`examples/fcmfd_replay.ipynb`](./examples/fcmfd_replay.ipynb) — runnable Jupyter notebook replaying an FCMFD-style SIA-kill on **genuinely synthetic data** (NOT a copy of the real Phase 4 data the case study describes).
- [`BLOG_POST.md`](./BLOG_POST.md) — canonical Markdown source for the project blog post telling the negative-result-with-mechanism story across four crypto strategy attempts. (Hosted version: <https://hallengray.github.io/signal-independence-audit/BLOG_POST.html>.)

## Why this exists

In the original project that produced this methodology, two ~Hetzner-hour hyperopt runs were spent discovering that the candidate strategies (trend-following at 4h, then mean reversion at 4h) didn't clear the project's pre-committed evaluation bar (Sharpe > 1.0 AND PF > 1.4 OOS). The methodology now in this repo was developed to **catch the same shape of failure pre-hyperopt, in seconds**, by formalising what "does this signal add information?" means as four mechanical screens. The first application of the framework — to a funding-rate-conditioned variant of the trend-following strategy — produced a clean exit code 1 in ~3 seconds on a laptop, saving the next ~Hetzner-hour of compute that the prior two strategies had each cost.

The full negative-result story (four crypto strategy attempts, all failing the criteria under pre-committed discipline, with mechanism) lives in [`BLOG_POST.md`](./BLOG_POST.md) + [`case-study/`](./case-study/).

## Install

```bash
pip install -e git+https://github.com/hallengray/signal-independence-audit
```

Or, if you've cloned:

```bash
cd signal-independence-audit
pip install -e ".[test]"
```

Python 3.11+. Hard dependencies: `pandas`, `numpy`. Optional extras: `[test]` adds `pytest` + `mypy`; `[notebook]` adds `jupyter` + `matplotlib` for the example notebook.

## Quick start

Two ways to invoke the harness.

### Library API — `sia.run_screens`

Use this from notebooks or any in-memory pipeline. You construct the pooled signal dataframe (synthetic or real); SIA runs the four screens and returns the verdict.

```python
import pandas as pd
from sia import run_screens

# Build a per-candle dataframe with the columns Screens 1, 2, and 4 read.
# (See examples/fcmfd_replay.ipynb for a complete worked example using
# genuinely synthetic data; the column conventions are documented there.)
pooled: pd.DataFrame = ...  # macro_pass, breakout_pass, funding_gate_pass,
                            # funding_gate_inversion, funding_4h, vol_20d,
                            # fwd_ret_{5,10,20}d, pair

# A single-pair frame for Screen 3's hyperparameter grid (typically
# the first per-pair frame if pooled is multi-pair).
jaccard_frame: pd.DataFrame = ...

verdict = run_screens(pooled, jaccard_frame)
print(verdict["verdict"])    # "PASS" | "FAIL" | "FAIL+INVERT"
print(verdict["exit_code"])  # 0 | 1 | 2
print(verdict["evidence"]["screen_2_lift"])  # per-screen detail
```

### CLI — `sia.main`

Use this when your data lives on disk in Freqtrade JSON format.

```bash
python -m sia.orchestrator \
    --pair BTC/USDT --pair ETH/USDT \
    --train-start 2021-01-01 --train-end 2024-12-31 \
    --data-dir /path/to/binance-data/ \
    --out sia-verdict.json
```

`--data-dir` must contain `<PAIR_underscored>-4h.json`, `<PAIR_underscored>-1d.json`, and `funding_rates/<PAIR_underscored>-funding-8h.json` files. Exit code: 0 PASS, 1 FAIL, 2 FAIL+INVERT.

For a runnable worked example on genuinely synthetic data, see [`examples/fcmfd_replay.ipynb`](./examples/fcmfd_replay.ipynb).

## Read the blog post

[`BLOG_POST.md`](./BLOG_POST.md) (in this repo) — canonical Markdown source. ~3500 words covering the four-phase negative-result story with mechanism, the literature audit, the AI-assisted-research corrigendum, and the framework artefacts that survive.

[**Hosted version on GitHub Pages**](https://hallengray.github.io/signal-independence-audit/BLOG_POST.html) — relative case-study links auto-resolved by GitHub Pages, so off-repo readers can navigate the whole story without leaving the published site.

## Read the case study

[`case-study/00-readme.md`](./case-study/00-readme.md) — reading guide for the 10 curated documents. Three reading paths:

- **Chronological** — the full project trajectory in numbered order.
- **SIA-methodology-focused** — for readers who want the tool, not the project history.
- **Negative-result-focused** — for readers who want the honest disconfirmation story.

The 10th document, [`case-study/10-audit-corrigendum.md`](./case-study/10-audit-corrigendum.md), is a self-contained teaching artefact about a specific AI-assisted-research failure mode (paywall reliance + abstract-only summarisation produces attribution errors that survive review). Worth reading on its own if your work involves LLM-assisted literature surveys.

## License

[Apache 2.0](./LICENSE). Patent grant clauses included because this is the kind of tool that may be used inside trading firms.

## Maintenance posture

This repository is published as a case study of a finished research project, not as an actively-maintained tool. Issues are welcome — bug reports, methodology questions, suggested improvements — and may be responded to selectively, but there is no response time commitment. PRs may not be reviewed. If you want to fork and maintain a variant, please do.

## Author

Femi Adedayo — hallengray@gmail.com
