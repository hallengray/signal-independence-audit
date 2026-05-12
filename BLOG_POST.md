> **Note:** This is the canonical Markdown source. The published version at <HOSTING_PLATFORM_URL — to be filled at launch in Task 15> has links rewritten to absolute GitHub URLs.

# Four crypto strategy failures, and the tool that caught one in 3 seconds

> _Or: what happens when you bring software-engineering ADR discipline to retail quant research, then watch it produce an honest negative result._

## Hook (TODO: 200-300 words)

<KEY CLAIMS — to expand in Task 10:>

- Most retail quant content is "I found a strategy that backtests well." This post is the inverse.
- Four crypto strategies tested under pre-committed Sharpe > 1.0 AND PF > 1.4 bars. All four failed. With mechanism.
- One of them — FundingConditionedMFD — was killed in 3 seconds of pure-Python testing by the SIA harness, BEFORE any of the planned 1000-epoch × 2-seed × 3-window hyperopt compute ran.
- The SIA harness is the public artefact this post ships. The negative result is the case study that produced it.

## Phase 2 — MFD (price-only trend-following) → §14 FAIL, Sharpe-bound

<TODO: 250-350 words. Macro-Filtered Donchian Breakout strategy. Hyperopt + walk-forward + OOS over 4 windows. Best OOS Sharpe 0.314; per-window best 0.553 (W3). PF generally passed (1.6-2.5 range across the windows). The binding constraint was Sharpe — returns per unit volatility too low. Failure mode: "edge per trade is real but too small relative to trade-noise variance." Link evidence: `./case-study/01-mfd-kill-adr-0011.md`.>

## Phase 3 — BMR (mean reversion) → §14 FAIL, Sharpe-AND-PF bound

<TODO: 250-350 words. Bollinger Mean Revert strategy. Hyperopt over 2 seeds, 15 candidates evaluated, ALL unprofitable (PF < 1.0). Best OOS Sharpe -0.083. Failure mode different from MFD's: the macro filter dominated entries, leaving very few mean-reversion opportunities. Link: `./case-study/02-bmr-kill-adr-0013.md`.>

## Phase 4 — FCMFD (funding-rate-conditioned MFD) → SIA-killed PRE-HYPEROPT in 3 seconds (THE LEAD WORKED EXAMPLE)

<TODO: 500-700 words. THE strongest example. After two §14-bar OOS-stage kills (MFD, BMR), the plan was to add a funding-rate gate as an orthogonal signal to MFD. Before spending another ~Hetzner-day of hyperopt compute, I built the Signal Independence Audit (SIA) framework — four screens that test whether a candidate signal adds information over a price-only baseline.

The SIA orchestrator ran in ~3 seconds on the laptop. It returned `exit 1` because:

- Screen 2 (lift test): treatment-vs-control gap was 0.147σ on 5d, 0.098σ on 10d, 0.016σ on 20d — all well below the 0.5σ bar.
- Screen 4 (information-split): vol-tercile separation on the 10d horizon was 6.93pp (low 5.14%, mid -1.79%, high 3.95%); funding-tercile separation was 2.45pp (low 3.50%, mid 2.77%, high 1.05%). Vol explained more than funding added.

The result: the funding signal carries information (the direction is right — low funding correlates with better forward returns) but it's quantitatively too weak vs. a vol-aware baseline. SIA caught this BEFORE compute was spent. Phase 2's and Phase 3's same shape of "candidate signal weaker than expected after accounting for what's already captured" was discovered ~Hetzner-hour after the hyperopt budget had already been spent.

Link evidence: `./case-study/04-fcmfd-sia-kill-adr-0015.md` + `./case-study/03-sia-framework-adr-0014.md`.>

## Phase 5 — literature audit, pre-committed gates, and the corrigendum

<TODO: 400-600 words. After three in-universe failures with different failure modes, the next question was no longer "what strategy should we try next?" — it was "is §14 empirically achievable on this surface at all?" That's an evidence question, not a strategy-building question.

A 2-day literature audit surveyed published academic crypto-trading research. The audit produced:

- Criterion D (mixed/inconclusive evidence) → routed to "Path C first, then Path D conditional on gates."
- Path C: test the timeframe hypothesis cheaply by re-running MFD at 8h. Result (Phase 5c): 0/4 windows clear §14. Per-window Sharpe means at 4h vs 8h: 0.425 vs 0.415. Timeframe alone was not the constraint. Link: `./case-study/07-path-c-kill-adr-0018.md`.
- Path D gate-check: four pre-committed gates, including PF verification on the foundational paper (Fieberg et al 2023 Quantitative Finance). Link: `./case-study/06-phase-5b-decision-adr-0017.md`.

Gate 1 retrieved the full text of the Fieberg paper (the audit had only abstract-level access). Findings: PF is NEVER reported in the paper. No transaction-cost analysis exists. All figures are gross. Criterion C strictly fails on §14's AND-clause. Path D is foreclosed; Path E (stop in-universe, ship the framework) is routed. Link: `./case-study/08-gate-1-pf-verification.md` + `./case-study/09-path-e-routing-adr-0019.md`.

**The corrigendum (its own section coming up — this is the teaching artefact).**>

## The audit corrigendum — what AI-assisted literature research got wrong, and how it was caught

<TODO: 500-700 words. THIS SECTION IS LOAD-BEARING. The Phase 5a audit attributed two specific phrases to Fieberg et al 2023:

- "incurs substantial trading costs"
- "extracts alphas largely from short positions"

Neither phrase appears in the paper. The audit conflated Fieberg et al with another source — most likely Liu/Tsyvinski/Wu 2022 or another Zaremba paper. The misattribution survived the 2-hour focused audit because the original retrieval relied on search-result snippets and abstracts; the paywall prevented full-text verification at audit time.

The Gate 1 task forced full-text retrieval (using the CC-BY 4.0 OA copy on open.icm.edu.pl). The corrigendum was caught when the full text didn't contain the attributed phrases.

Lesson (for AI-assisted research, not specific to crypto): **paywall reliance + abstract-only summarisation is a failure mode** that produces attribution errors that survive review. The defence is full-text verification for any load-bearing claim — codified as Gate 1 of Path D in ADR-0017, before this specific error was known to exist. The pre-committed gate caught the error by construction.

Link: `./case-study/10-audit-corrigendum.md` (the standalone teaching artefact).>

## What survives — the SIA harness and the framework artefacts

<TODO: 400-500 words. The genuine reusable output of this project. The SIA harness is the publishable artefact:

- Four screens (coverage, lift, jaccard, information-split) that any signal hypothesis can be tested against pre-hyperopt.
- Generic Python implementation. Apache 2.0. `pip install -e git+https://github.com/hallengray/signal-independence-audit`.
- 16 unit tests; mypy --strict clean.
- One example notebook (`examples/fcmfd_replay.ipynb`) replaying an FCMFD-style SIA-kill on genuinely synthetic data.

Other framework artefacts named in ADR-0019 §"What we keep" but NOT extracted as separate packages in this Phase 5e (could be later phases):

- Deterministic backtest pipeline (image-pinned + sha256-manifest + cross-machine determinism check)
- Look-ahead-safe alignment patterns (`merge_informative_pair(ffill=True)` discipline + custom non-OHLCV joiners)
- Data manifest tooling
- ADR + audit methodology

Link to the case-study reading guide: `./case-study/00-readme.md`. Link to the SIA repo `README.md`: `./README.md`.>

## What this isn't

<TODO: 200-300 words. Honest negative-result framing. Path E is NOT "project failed." It is "the project produced a documented disconfirmation of the in-universe hypothesis with mechanism, on a surface where the literature itself does not have positive evidence." The §14 bar held throughout — no bar erosion at any of 19 ADRs. The bar transitions from "contested-theoretical" to "documented-empirical."

If anyone wants to deploy capital on BTC/USDT + ETH/USDT 4h spot long-only in the future, the case-study directory is the receipt: this surface doesn't support §14-clearing strategies per documented evidence across four attempts + literature audit + Path D Gate 1 verification.>

## Footnotes / references

<TODO at Task 10: condensed reference list. Crypto-ase repo (private — explain why if asked: scope B locked, see `./case-study/00-readme.md`). The SIA harness repo (this repo). Apache 2.0 license. Author + contact.>

---

_Word count target at completion (Task 10): 3000-4500. Currently a skeleton at ~800-900 words of TODO markers + claim sentences._
