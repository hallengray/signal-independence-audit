> **For external readers:** This document is one of 10 curated case-study artefacts from Project Aṣe, a quantitative crypto-trading research project that produced a documented negative result with mechanism across four strategy attempts plus a literature audit, all under pre-committed criteria (Sharpe > 1.0 AND profit-factor > 1.4 OOS, called "§14" internally) that held without bar erosion across 19 ADRs. The full project repo is private (scope B of the Phase 5e shipping spec). Start with `./00-readme.md` for the reading guide. Read order context: The methodology that emerged from the first two kills. SIA = Signal Independence Audit. Reference this for the four-screen framework. The substance of the document below is unchanged from the internal version; only this framing block and personal/identifying content scrubs are added.

---

# ADR-0014: Signal Independence Audit (SIA) framework

- **Status:** Accepted
- **Date:** 2026-05-11
- **Deciders:** Femi Adedayo
- **Approves:** Phase 4 design spec `docs/superpowers/specs/2026-05-11-phase-4-funding-conditioned-mfd-design.md`
- **Predecessors:** ADR-0011 (MFD §14 fail), ADR-0013 (BMR §14 fail).

## Context

BMR's Phase 3 §14 failure (ADR-0013) had a deeper finding: the failure was **diagnosable from BMR's design** (the macro-EMA stack dominated the entry signal; the Bollinger parameters did not materially shift WHICH candles fire) but was only discovered after ~30 hours of Hetzner hyperopt + OOS + walk-forward compute. This is wasted compute on a thesis-level defect that could have been caught pre-compute with a small battery of pre-hyperopt screens.

The Signal Independence Audit (SIA) is the formalised "would BMR have died here?" check, applied prospectively to every new strategy thesis from Phase 4 onward.

## Decision

The SIA is a **hard gate** before any hyperopt compute. A new strategy thesis cannot enter hyperopt until SIA passes. If SIA fails, the strategy is killed and a kill ADR is written. The SIA consists of four screens applied to the training window only (`2021-01-01 → 2024-12-31`), with the first ~97 days excluded as warm-up for any rolling-window indicators.

### Screen 1 — Coverage test

- Count candles satisfying each rule independently (macro, breakout, new-gate) and the full conjunction across training.
- Fail: new-gate reduces trade frequency by < 20% (redundant) OR full conjunction yields < 30 trades (over-restrictive).
- Per-year breakdown reported to surface market-structure confounds.

### Screen 2 — Lift test

- For three forward horizons (5d, 10d, 20d), compute returns following macro-only, macro+breakout, and macro+breakout+gate candles.
- **Headline pass/fail (parametric):** treatment cohort mean exceeds macro+breakout-control mean by ≥ 0.5 × pooled-stddev on ≥ 2 of 3 horizons.
- **Supporting evidence (bootstrap):** 1000-resample 95% CIs reported alongside. If parametric passes but CIs overlap meaningfully, the screen flags `ci_overlaps=True` for explicit review (verdict unchanged).
- **Cohort guards:** cohorts < 10 → `cohort_size_too_small` (skip); cohorts 10–29 → `review_required` flag (verdict unchanged).
- **Inversion-clause measurement (always run for direction-gated strategies):** the symmetrically inverted direction is evaluated with identical machinery. If the inverted direction shows ≥ 1.0σ separation on ≥ 2 of 3 horizons, the inversion clause triggers — see §"Inversion clause" below.

### Screen 3 — Entry-set stability (Jaccard)

- Sweep a 5×5 grid over the strategy's hyperoptable parameter (axis A) and one fixed-in-production gate parameter (axis B, swept here solely to provide a second Jaccard axis).
- Compute mean pairwise Jaccard overlap of triggered-candle sets across all C(25,2)=300 pairs.
- Fail: mean pairwise Jaccard > 0.85 (parameter-plateau / BMR-shape failure mode incoming).

### Screen 4 — Information split

- Bin candidate candles into terciles by the new gate signal. Independently bin by realised 20-day volatility (control).
- Per binning, compute {mean 10d forward return, win rate, Sharpe-per-bin}.
- Pass: new-gate tercile binning produces wider tercile separation than vol-tercile control on ≥ 2 of 3 metrics, with bootstrap CIs reported.

### Statistical methodology

Brainstorm 2026-05-11 selected **Option B**: parametric headline thresholds for fast mechanical verdict (matching the existing §14 report style) + bootstrap 95% CIs as supporting evidence in the SIA report. Pure parametric (Option A) was rejected as too loose; strict hypothesis tests with Bonferroni correction (Option C) were rejected as too strict for the 4-year sample size.

### Verdict logic

| Condition                                 | Verdict     | Exit code | Next action                               |
| ----------------------------------------- | ----------- | --------- | ----------------------------------------- |
| All 4 screens PASS                        | PASS        | 0         | Proceed to hyperopt + OOS                 |
| Any screen FAIL, no inversion trigger     | FAIL        | 1         | Kill ADR written; strategy phase closes   |
| Any screen FAIL, inversion trigger active | FAIL+INVERT | 2         | Phase-prime authorised under separate ADR |

### Inversion clause (Phase 4 application)

For Phase 4 specifically: the funding gate is locked at `funding < 60th pct` based on Option D of the design brainstorm (locked thesis: low funding = uncrowded positioning = fresher fuel for breakout). The brainstorm noted a ~50% prior on direction with mild lean against the locked direction. To buy insurance against the false-negative scenario at the cost of one pre-committed contingency:

- The inversion test runs the **symmetric inversion** (`funding > 40th pct`) with identical Screen 2 machinery.
- **Inversion trigger:** if the inverted direction shows ≥ 1.0σ forward-return separation on ≥ 2 of 3 horizons (5d/10d/20d) AND the locked direction fails Screen 2, the orchestrator exits with code 2 and ADR-0016 authorises Phase 4-prime: a separately-tracked rerun with the inverted gate.
- The inversion threshold (1.0σ) is 2× the Screen 2 pass threshold (0.5σ) — the margin prevents arbitrary tie-breaking.

## Generality

The SIA framework is strategy-agnostic. For non-direction-gated strategies (no inversion clause needed), Screen 2's inversion test simply isn't run; Verdict logic still applies.

## Consequences

- Every new strategy thesis must produce an SIA verdict before hyperopt budget is allocated.
- The SIA harness (`scripts/sia/`) is preserved as reusable framework infrastructure across all subsequent strategy phases.
- An SIA fail is an acceptable terminal state and is treated identically to a §14 fail for project-discipline purposes (PRD §15 principle 4).
- PRD §15 gains an implicit principle: "every thesis passes SIA before hyperopt." A formal PRD amendment can be made if/when convenient; this ADR documents the principle in the meantime.

## References

- Phase 4 design spec: `docs/superpowers/specs/2026-05-11-phase-4-funding-conditioned-mfd-design.md`
- Phase 4 scope: `docs/phases/phase-4-scope.md`
- ADR-0011 (MFD kill): `docs/decisions/0011-mfd-§14-fail-post-mortem.md`
- ADR-0013 (BMR kill): `docs/decisions/0013-bmr-§14-fail-post-mortem.md`
- PRD §15 principles 2, 4, 5
