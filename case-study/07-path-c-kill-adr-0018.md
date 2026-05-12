> **For external readers:** This document is one of 10 curated case-study artefacts from Project Aṣe, a quantitative crypto-trading research project that produced a documented negative result with mechanism across four strategy attempts plus a literature audit, all under pre-committed criteria (Sharpe > 1.0 AND profit-factor > 1.4 OOS, called "§14" internally) that held without bar erosion across 19 ADRs. The full project repo is private (scope B of the Phase 5e shipping spec). Start with `./00-readme.md` for the reading guide. Read order context: Path C's verdict: 0/4 windows clear §14 at 8h. Timeframe shift was not directionally helpful per-window. The substance of the document below is unchanged from the internal version; only this framing block and personal/identifying content scrubs are added.

---

# ADR-0018: Phase 5c PATH-C-KILL — timeframe was not the constraint

- **Status:** Accepted
- **Date:** 2026-05-12
- **Deciders:** Femi Adedayo
- **Approves:** Phase 5c spec §7 row 2 FAIL routing; ADR-0017 §"Path D escalation gates" entry condition.
- **Triggers:** `phase-5c-path-c-killed` tag.

## Context

Phase 5c ran a pure diagnostic test of the timeframe-shift hypothesis raised by ADR-0017: take Phase 2's **locked** MacroDonchian default parameters (no hyperopt, no signal-class change) and re-run them at 8h primary timeframe across the same four walk-forward calendar windows that Phase 2 used. The question was narrowly framed: _was 4h the binding constraint?_

The four-window §14 verdict is FAIL across the board:

| Window                       | Trades | Sharpe |    PF | Max DD | §14?          |
| ---------------------------- | -----: | -----: | ----: | -----: | ------------- |
| W1 (2023H1)                  |     25 |  0.586 | 1.841 |  4.10% | FAIL (Sharpe) |
| W2 (2023H2)                  |     22 |  0.203 | 1.446 | 10.36% | FAIL (Sharpe) |
| W3 (2024H1)                  |     25 |  0.531 | 2.065 |  8.85% | FAIL (Sharpe) |
| W4 (2024H2)                  |     19 |  0.341 | 1.606 |  3.51% | FAIL (Sharpe) |
| W5 (2025-01 → 2026-05, supp) |     37 |  0.208 | 1.546 |  8.16% | FAIL          |
| Full-span (2023-2024, supp)  |     88 |  0.389 | 1.916 |  8.85% | FAIL          |

Per spec §7 row 2 + ADR-0017 §"Path D escalation gates", a 0/4 §14 outcome at 8h routes the decision to the four pre-committed gates from ADR-0017 §7.4. This ADR records the kill, the diagnostic interpretation, and the routing forward.

## Decision

`MacroDonchian8h` is killed. PRD §6 stays at **4h primary** (spec §8 explicitly forbids amendment except on PASS; the verdict is FAIL, so no amendment fires). Decision routes to **ADR-0017 §"Path D escalation gates"** — the four §7.4 gates must all be satisfied before any Path D scope is written. If any gate fails, routing escalates to **Path E** (stop in-universe; ship the SIA framework as the carry-over deliverable).

The tag `phase-5c-path-c-killed` is applied at this ADR's commit.

## What bound, in plain English

Sharpe was **below 1.0 in all four primary walk-forward windows** AND in both supplementary windows (the 2025-onward holdout and the full-span aggregate). PF passed comfortably in every window (1.45–2.07 range). The binding constraint is exactly the same as Phase 2 at 4h: **returns per unit volatility are too low** for this universe at this strategy class, regardless of which primary candle cadence the breakout is drawn against.

Per-window apples-to-apples 4h vs 8h:

| Window   | 4h Sharpe | 8h Sharpe | Δ Sharpe |     4h PF |     8h PF |     Δ PF |
| -------- | --------: | --------: | -------: | --------: | --------: | -------: |
| W1       |     0.400 |     0.586 |     +47% |     1.614 |     1.841 |     +14% |
| W2       |     0.359 |     0.203 |     −44% |     2.208 |     1.446 |     −35% |
| W3       |     0.553 |     0.531 |      −4% |     2.509 |     2.065 |     −18% |
| W4       |     0.388 |     0.341 |     −12% |     1.699 |     1.606 |      −5% |
| **Mean** | **0.425** | **0.415** |  **−2%** | **2.008** | **1.740** | **−13%** |

The shift from 4h to 8h does not move Sharpe in a directionally helpful way — the per-window means are essentially flat (4h 0.425, 8h 0.415). PF regresses on three windows out of four. The 8h experiment was operationally clean (Hetzner-deterministic, data manifest verified, no integrity issues — see Task 8 closeout), and the answer is clear: **timeframe alone was not the binding constraint**.

## Why the timeframe-shift hypothesis is decisively refuted

Phase 2's best per-window walk-forward OOS Sharpe was **0.553 (W3 @ 4h)**. Phase 5c's best per-window OOS Sharpe is **0.586 (W1 @ 8h)**. The two are statistically indistinguishable. No window crossed 1.0; no window came close. On the same calendar windows, 8h MFD does not produce regime-robust §14-clearing performance.

This is the cheapest experiment design that could have falsified the hypothesis: same strategy, same defaults, same universe, same eval pipeline, different primary candle cadence. The hypothesis "timeframe was the binding constraint across Phases 2-4" is now empirically refuted at this strategy + universe combination. The constraint sits elsewhere — universe composition, signal class, or both — and ADR-0017's Criterion D fired correctly when it routed us to Path C first as the cheap test.

## Why not re-tune / re-hyperopt at 8h

Phase 5c spec §3.4 and §3.5 forbid both hyperopt and signal-class introduction within Phase 5c. The diagnostic discipline was binding by design — Path C tests whether the **locked** Phase 2 strategy clears at 8h, not whether _some_ 8h variant clears after re-tuning. Re-tuning at 8h would be a separate phase entirely (Phase 5d Path D or Phase 6), not a Phase 5c retry. PRD §15.2 forbids bar erosion; the §14 bar (Sharpe > 1.0 AND PF > 1.4) is not revised under any scenario except ADR-0017's Criterion E pathway with documented evidence, and Criterion E does not fire today — it becomes the routing only if one of the four Path D gates fails downstream.

Lowering Sharpe from 1.0 to ~0.55 to pass the best window would be exactly the bar erosion PRD §15.2 forbids.

## Cross-strategy comparison

Extending ADR-0015's three-phase table with the Phase 5c column:

| Dimension                  | MFD (Phase 2e FAIL)       | BMR (Phase 3 FAIL)      | FCMFD (Phase 4 FAIL)       | **MacroDonchian8h (Phase 5c FAIL)** |
| -------------------------- | ------------------------- | ----------------------- | -------------------------- | ----------------------------------- |
| Gate of failure            | §14 (post-hyperopt OOS)   | §14 (post-hyperopt OOS) | SIA (pre-hyperopt)         | **§14 (no hyperopt, diagnostic)**   |
| Compute cost to verdict    | ~Hetzner-hour × 4 windows | ~Hetzner-hour × 2 seeds | ~3 seconds laptop          | **~5 minutes laptop (6 backtests)** |
| Best per-window OOS Sharpe | 0.553 (W3 @ 4h)           | -0.083                  | n/a (gated out)            | **0.586 (W1 @ 8h)**                 |
| Best per-window OOS PF     | 2.509 (W3 @ 4h)           | < 1.0 all 15            | n/a                        | **2.065 (W3 @ 8h)**                 |
| Binding constraint         | Sharpe (PF mostly OK)     | Sharpe AND PF           | Lift gap σ AND vol-control | **Sharpe (PF clears in all 4)**     |
| Inverted variant tested?   | No                        | No                      | Yes — also fails           | n/a (no signal to invert)           |

Four consecutive strategies under four different operational profiles, three different binding constraints (Phase 2's and Phase 5c's are the same shape). The pattern across all four sharpens the universe-revision hypothesis ADR-0015 identified and ADR-0017 formalised: **the BTC/USDT + ETH/USDT spot universe at any single-asset primary timeframe may not support strategies that jointly clear Sharpe > 1.0 AND PF > 1.4 OOS friction-adjusted**. ADR-0017's Criterion D fired correctly. Path C's failure confirms the literature audit's interpretation: the constraint is structural, not strategy-specific.

## The four Path D escalation gates (from ADR-0017 §7.4, verbatim)

These are the binding entry conditions for any future Path D scope document. Re-listed here so this ADR is self-contained:

- **Gate 1 — Full-text PF verification.** The Fieberg/Liedtke/Metko/Zaremba 2023 _Quantitative Finance_ paper must be obtained in full text. Profit factor for the long-only winner portfolio (or closest reported analogue) must be extracted. If PF < 1.4 net of fees, Criterion C strictly fails on the AND-clause of §14, and the decision re-routes to **Criterion E (Path E)**, not Path D.
- **Gate 2 — Universe match.** Path D scope as currently drafted (top-N liquid perps, BTC/ETH/SOL/BNB/XRP minimum) does not match the literature's evidentiary universe (3,900+ coins). Either (a) Path D scope is expanded to top-20 or top-50 perp universe with explicit liquidity gates, OR (b) full-text retrieval of Fieberg et al / Liu-Tsyvinski-Wu confirms the cross-sectional momentum effect persists when restricted to top-10 by volume.
- **Gate 3 — Net-of-fees Sharpe verification.** The 2025 Risk-Managed Momentum paper's "robust to transaction costs" claim must be quantified at realistic crypto retail fees (typically 10–20 bp round-trip on Binance spot). If the paper tested friction at < 10 bp, the result does not generalise to retail Binance and Path D's foundation weakens further.
- **Gate 4 — Methodological dissent resolution.** Grobys & Shahzad's Sharpe-undefinability finding must be addressed. Either Path D plan acknowledges the strategy is built on a metric the literature itself contests, OR substitutes a metric not requiring finite second moments (Calmar, Sterling, max-drawdown-relative).

If any of Gates 1-4 fails, the decision re-routes to Path E.

## What we keep (carry-over to Phase 5d Path-D-gate-check or Phase 5e Path-E)

- **`MacroDonchian8h` strategy file** (`freqtrade/user_data/strategies/macro_donchian_8h.py`) stays in-tree as historical record. Future Phase 5d/5e strategies are new files alongside it.
- **8h data manifest and ingestion pipeline.** The 8h candle set, `scripts/write-data-manifest.sh` extensions for 8h, and the cross-platform LF handling remain reusable for any future timeframe-shift work.
- **Data-integrity cross-check script** (`scripts/verify-8h-vs-aggregated-4h.py`) — generic and reusable for any future cross-timeframe consistency audit.
- **`_lib/` indicator package** (`donchian_high`, `macro_filter`) — continues to be the shared base across the strategy family.
- **§14 evaluation pipeline** — unchanged; the OOS Sharpe-and-PF evaluator remains the verdict gate.
- **SIA harness from Phase 4** — preserved per ADR-0015. Still the live framework for any future orthogonal-signal hypothesis test.

## What we don't keep

- **PRD §6 amendment is NOT applied.** Primary timeframe stays at 4h. Per spec §8, amendment fires only on PASS.
- **`run-*.sh` defaults are NOT flipped to `MacroDonchian8h`.** `FundingConditionedMFD` remains the carried default per ADR-0015 §"What we keep" (a Phase 4 historical lock, not a live-candidate signal).
- The "timeframe was the binding constraint across Phases 2-4" **hypothesis is empirically refuted** and should NOT be revisited without materially new evidence (e.g., a Tier-1 paper showing §14 clearance at a specific non-4h, non-8h cadence on the BTC/ETH universe specifically).

## What discipline held

- **No bar erosion.** §14 bar unchanged (Sharpe > 1.0 AND PF > 1.4 OOS friction-adjusted).
- **No re-tuning post-result.** The 0/4 verdict was applied mechanically per spec §7 row 2.
- **No selective reading.** The evaluation report includes all 6 backtest outputs (4 primary + 2 supplementary) with Sharpe AND PF AND trade count AND max drawdown per window.
- **Cross-machine determinism verified BEFORE this ADR was written.** Hetzner reproduced laptop W1 exactly (Sharpe 0.586, PF 1.841, 25 trades, DD 4.10%); MANIFEST OK on both machines. Spec §11 operating discipline #3 satisfied.
- **Pre-committed Option C decision inherited verbatim.** Spec §13 change log entry 3 fixed Phase 2's locked defaults as the Path C parameter set; no parameter re-derivation occurred within Phase 5c.
- **No hidden mechanics.** The Phase 5c evaluation report (`docs/reports/2026-05-12-phase-5c-mfd-8h-evaluation.md` at commit `d800fe6` + determinism update `71dd221`) is the authoritative record; this ADR draws from it without restating intermediate JSON.

## References

- Phase 5c evaluation report: `docs/reports/2026-05-12-phase-5c-mfd-8h-evaluation.md` (commits `d800fe6`, `71dd221`)
- Phase 5c spec: `docs/superpowers/specs/2026-05-12-phase-5c-mfd-8h-design.md`
- Phase 5c plan: `docs/superpowers/plans/2026-05-12-phase-5c-mfd-8h.md`
- ADR-0017 (Phase 5b Path C + Path D gates): `docs/decisions/0017-phase-5b-path-c-and-path-d-gates.md`
- ADR-0015 (Phase 4 SIA kill, template for this ADR): `docs/decisions/0015-phase-4-sia-kill.md`
- ADR-0013 (BMR §14 kill): `docs/decisions/0013-bmr-§14-fail-post-mortem.md`
- ADR-0011 (MFD §14 kill): `docs/decisions/0011-mfd-§14-fail-post-mortem.md`
- Phase 2 evaluation report (4h baseline): `docs/reports/2026-05-11-mfd-evaluation.md`
- PRD §6 (primary timeframe lock), §15 principle 2 (no re-tuning), §15.2 (no bar erosion)
- Predecessor tag: `phase-4-sia-killed` at `1efa022`
- Successor tag (this kill): `phase-5c-path-c-killed`
