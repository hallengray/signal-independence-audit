> **For external readers:** This is an epilogue artefact from Project Aṣe, a quantitative crypto-trading research project that produced a documented negative result with mechanism across four strategy attempts plus a literature audit, all under pre-committed criteria (Sharpe > 1.0 AND profit-factor > 1.4 OOS, called "§14" internally) that held without bar erosion across the first 19 ADRs. This document records what happened **after** the decision to stop (Path E): one owned, pre-committed exception. The Markov-Switched Strategy (MSS) combined the already-failed trend and mean-reversion strategies under a regime detector, and was tested against a deliberately revised scorecard (§14-v2) that lowered the out-of-sample Sharpe pass mark from 1.0 to 0.85. That revision was an owned operator choice, recorded as such in ADR-0024; it is not bar-erosion-by-stealth, but it is a real relaxation of the one criterion that bound every prior kill, and the project says so plainly. MSS failed anyway, out-of-sample, by a wide margin. The narrative version is at [`../MSS_POST.md`](../MSS_POST.md); the reading guide is [`./00-readme.md`](./00-readme.md). The substance below is unchanged from the internal ADR-0027; only this framing block and light copy-edits are added.

---

# ADR-0027: Phase 5f / MSS terminal kill, §14-v2 backtest fail (State B, via Option B)

- **Status:** Accepted
- **Date:** 2026-05-23
- **Deciders:** Femi Adedayo
- **Closes:** Phase 5f (Markov-Switched Strategy), the final pre-committed in-universe strategy attempt.
- **Triggers:** `phase-5f-section-14-v2-killed` tag.

## Context

Phase 5f tested whether a regime-conditional router could combine the project's two failed strategies into something that clears the bar where the components could not. The design:

- **Bull regime** (rising market): trend-following via a Donchian breakout (the Phase-2 strategy, MFD).
- **Sideways regime**: mean reversion via a Bollinger Band signal (the Phase-3 strategy, BMR), with its old macro filter removed.
- **Bear regime** (falling market): cash, no trades.

Regime is a daily 20-day-return classifier (at or above +5% bull, at or below -5% bear, between the two sideways), looked up on each 4-hour candle in a look-ahead-safe way. The strategy was authorised as an explicit, owned exception to the earlier decision to stop (recorded in ADR-0023), under a revised scorecard, §14-v2 (ADR-0024), whose only relaxation versus the original §14 is the Sharpe pass mark, lowered from 1.0 to 0.85.

- **Pre-hyperopt screen (SIA Screen 5):** PASSED. The first signal in the project's history to clear the Signal Independence Audit. It was a thin pass and carried a flagged risk that the regime gate might behave as a weak trend filter, but it cleared.
- **Hyperopt plus out-of-sample (5f-d):** three independent tuning runs (seeds 42, 1337, 9001; 1000 epochs each) on 2021 to 2024, then the survivors evaluated on held-out 2025-01-01 to 2026-05-12 data, with realistic friction (a 0.10% taker fee plus 0.05%-per-side slippage). The only two tunable parameters were the ATR-scaled stop-loss multipliers for each leg.

## Decision

**MSS reaches terminal State B: it does not clear §14-v2, and the in-universe research program is closed.** The verdict is adjudicated on the 5f-d out-of-sample evidence by invoking **Option B**, the documented precedent from Phase 3 (ADR-0013): when the out-of-sample result is decisive, the walk-forward step is skipped because it cannot change a verdict already settled by the full-window result. This is an owned operator decision. The §14-v2 bar was not met.

## Evidence (the mechanical result)

All five candidates (the top five by training Sharpe, identical across all three seeds, see "On the tiny grid" below) fail §14-v2 criteria 1 to 8 on the out-of-sample window. **Zero of five pass.**

| Candidate (bull, sideways ATR mult) | Trades | Sharpe | Sortino | Calmar | Profit factor | Max drawdown | Verdict |
| ----------------------------------- | ------ | ------ | ------- | ------ | ------------- | ------------ | ------- |
| (1.5, 3.0)                          | 77     | -0.231 | -0.494  | -2.011 | 0.779         | 16.78%       | FAIL    |
| (1.6, 3.0)                          | 77     | -0.230 | -0.491  | -1.998 | 0.780         | 16.78%       | FAIL    |
| (3.2, 3.0)                          | 77     | -0.378 | -0.662  | -2.615 | 0.688         | 16.35%       | FAIL    |
| (3.1, 3.0)                          | 77     | -0.367 | -0.653  | -2.570 | 0.695         | 16.44%       | FAIL    |
| (1.5, 2.9)                          | 77     | -0.239 | -0.502  | -2.064 | 0.774         | 16.96%       | FAIL    |

Every candidate clears only max-drawdown, trade-count, and average-duration. Every one fails the four return and quality criteria: Sharpe (needs at least 0.85), Sortino (1.2), Calmar (0.5), profit factor (1.4), and recovery factor (1.5). The binding metric is, once again, Sharpe: negative on every candidate, the same axis that bound every prior kill. The pre-committed nomination rule (ADR-0026, locked before any out-of-sample number was seen) yields no nomination, and the rule was not relaxed.

## Per-state attribution (the regime-router finding)

Summed across all five candidates: the trend-following (Bull, MFD) leg fired 145 trades for +237 units of profit; the mean-reversion (Sideways, BMR) leg fired 240 trades for -723 units. So the regime router did route to both legs. This is **not** the failure mode the scope feared (the regime gate collapsing into a pure trend filter, with the mean-reversion trigger contributing nothing). MSS failed for a cleaner reason: the mean-reversion leg is unprofitable out-of-sample (it bought dips that kept dipping), and the modestly-profitable trend leg could not carry it. The composition does not produce a portfolio-level edge.

## Why the walk-forward was skipped (Option B)

1. The out-of-sample result is decisive, not marginal: zero of five, on both pairs, with negative Sharpe.
2. The walk-forward asks whether at least three of four sub-windows each clear criteria 1 to 8. A strategy that fails those criteria across the entire window, unprofitable on every candidate, cannot clear them in three of four narrower slices of the same window.
3. The walk-forward was never the binding evidence. The only genuine forward evidence is the 60-day live paper test, which runs only if the backtest passes. The backtest did not pass; the paper test does not open.
4. Direct precedent: Phase 3 (BMR) closed via this exact Option B.

## Honest accounting

- The bar was not lowered to reach this verdict. §14-v2 already relaxed Sharpe from 1.0 to 0.85, an owned choice. MSS posts negative Sharpe out-of-sample; it fails the relaxed bar by a wide margin, not a hair.
- The SIA Screen 5 pass did not predict survival. It was thin and carried a flagged risk; the out-of-sample result is consistent with that caution. A pass means "not obviously dead, proceed to the expensive test," not "this works."
- This is the most likely outcome the scope predicted. The experiment ran to a clean, mechanical, honest negative.

## On the tiny grid (provenance honesty)

MSS has only two one-decimal hyperopt parameters, so the search grid is only about 546 combinations. The 1000-epoch, three-seed run exhausted it, so all three seeds converged on the identical top five and the cross-seed agreement check was satisfied by construction. That "three seeds agreed" robustness signal is therefore weak here, retained for symmetry with the project's other selection rules rather than as strong evidence. It does not affect the verdict, which rests on out-of-sample performance, and that is unambiguous.

## Consequences

1. The bounded in-universe research program ends. MSS was its final pre-committed attempt; there is no further variant of the killed theses without fresh evidence.
2. The evaluation bar is not revised again on the strength of this result.
3. The surviving result is the Signal Independence Audit framework, already shipped publicly. MSS becomes this epilogue: the final attempt, tested honestly, killed mechanically.
4. The decision to keep researching new ideas (and to re-run the same test on any credible new candidate) is separate from, and not in conflict with, closing this bounded program. New evidence has always been allowed to reopen evaluation; that is what the framework is for.

## Status

Accepted. Phase 5f is closed. The Markov-Switched Strategy does not graduate.
