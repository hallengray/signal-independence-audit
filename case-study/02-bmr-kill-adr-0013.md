> **For external readers:** This document is one of 10 curated case-study artefacts from Project Aṣe, a quantitative crypto-trading research project that produced a documented negative result with mechanism across four strategy attempts plus a literature audit, all under pre-committed criteria (Sharpe > 1.0 AND profit-factor > 1.4 OOS, called "§14" internally) that held without bar erosion across 19 ADRs. The full project repo is private (scope B of the Phase 5e shipping spec). Start with `./00-readme.md` for the reading guide. Read order context: The second §14-bar kill: Phase 3's BMR (Bollinger Mean Revert) post-mortem. Different failure mode from Phase 2. The substance of the document below is unchanged from the internal version; only this framing block and personal/identifying content scrubs are added.

---

# ADR-0013: BMR §14 FAIL post-mortem — no live ship, no re-tuning

- **Status:** Accepted
- **Date:** 2026-05-11
- **Deciders:** Femi Adedayo
- **Approves:** Phase 3 spec §7.6 PASS/FAIL routing FAIL branch
- **Triggers:** `phase-3-bmr-killed` tag

## Context

Phase 3 ran the §14 evaluation protocol for BMR (Bollinger Mean-Reversion) — the second strategy attempt of Project Aṣe after MFD's Phase 2e FAIL (ADR-0011). The harness output:

```
VERDICT: FAIL
**Binding constraint:** no OOS candidate passes crit 1-5
```

The Phase 3 protocol was abbreviated per Plan Option B (recorded in the verdict report): walk-forward (crit 6) was skipped because OOS evidence (15 candidates across 3 seeds × top-5 epochs each) was decisive enough that walk-forward would only have confirmed the result.

## Decision

BollingerMeanRevert does NOT ship. The Phase 3 final tag is `phase-3-bmr-killed`. Phase 7 (paper-trading) is NOT entered for BMR. Phase 4 (new strategy thesis — Project Aṣe's third strategy attempt) becomes the immediate next phase.

## What bound, in plain English

Both Sharpe (crit 3, threshold > 1.0) AND profit factor (crit 2, threshold > 1.4) failed across every OOS candidate (15 of 15). The best OOS Sharpe across the 15 candidates was −0.083 (seed=42 epoch=51), with the worst being −0.361 (seed=9001 epoch=35). Mean OOS Sharpe across the 15: −0.180. Mean PF: 0.59 (the best was 0.85, the worst 0.31). **Every candidate was both unprofitable AND low-conviction.**

This is a structurally worse failure shape than MFD's. MFD's OOS run produced Sharpe ≈ 0.31 with profitable PF > 1.4 on multiple candidates — MFD was profitable-but-inconsistent. BMR is unprofitable-AND-inconsistent.

Diagnostic evidence from the hyperopt phase reinforces the kill:

- All three seeds independently produced negative best in-sample Sharpe (−0.066 to −0.111).
- Seed-9001 had 638 of 1000 epochs tied at the global-best objective, indicating the hyperopt search found no informative ridge in the parameter landscape — the strategy's per-trade payoff doesn't respond to parameter variation in a way the optimizer can exploit.
- 3-way overlap across seeds' top-5 was empty, so ADR-0009's consilience-by-overlap rule would have foreclosed live-ship even if §14 had somehow passed.

The deeper finding: the BMR entry signal is dominated by ONE binding indicator (likely the daily EMA-stack macro filter, which is very restrictive on trades). The Bollinger band parameters do not materially shift WHICH candles fire — they only affect the per-trade exit timing within a macro-filter-selected trade set. This is a fundamental thesis-level defect, not a tuning failure.

## Why walk-forward was skipped

Plan Option B (recorded 2026-05-11) authorized skipping walk-forward (Plan Task 14) when OOS evidence is decisive. The criteria for triggering Option B were:

- Best OOS Sharpe < 0 across all candidates (BMR: −0.08 worst-case-best, decisive). ✓
- Multiple candidates failing two or more §14 crits (BMR: all 15 fail crits 2 AND 3). ✓
- 3-way overlap = 0 (BMR confirmed empty). ✓

Under these conditions, walk-forward (35 min Hetzner CPU + ~5 min of analysis) is statistically guaranteed to confirm rather than refute the OOS-only verdict. Running it would be methodologically thorough but operationally redundant.

This precedent applies to future Phase N strategies IF the same Option B trigger conditions hold. If any of the three triggers fails (e.g. OOS Sharpe is positive but below 1.0; only one crit binds; non-zero overlap exists), walk-forward is REQUIRED — the protocol defaults to belt-and-braces.

The harness's manifest validator was relaxed in commit `8ac7a4e` to accept `walk_forward_windows` count of either 4 (normal) OR 0 (Option B skip); any other count is still rejected as malformed.

## Why not re-tune

PRD §15 principle 2 forbids "kept tuning until it worked." The protocol made every methodologically allowed move:

- Three seeds searched (42, 1337, 9001) at 1000 epochs each.
- HP-Moderate parameter space (4 tuned) per spec §5.1.
- 3-way overlap selection rule applied per ADR-0009.
- Cross-machine determinism verified for both smoke (Phase 3a) and OOS (Phase 3d) backtests.

A fourth seed, a fifth tuned parameter, or a different exit mechanism (fixed-percent take-profit, time-stop tiebreaker — deferred per spec §9.7) would be re-tuning. The thesis is wrong; we don't lower the bar.

## Cross-strategy comparison: MFD vs BMR failure modes

| Dimension          | MFD (Phase 2e FAIL)                          | BMR (Phase 3 FAIL)                                |
| ------------------ | -------------------------------------------- | ------------------------------------------------- |
| Best OOS Sharpe    | 0.314 (positive, ~3× below threshold)        | −0.083 (negative)                                 |
| Best OOS PF        | > 1.4 on multiple candidates                 | < 1.0 on all 15 candidates                        |
| Hit rate           | 35-45% (trend-following profile)             | 66% (mean-reversion as predicted)                 |
| Profitability      | Profitable but inconsistent                  | Unprofitable AND inconsistent                     |
| Binding §14 crit   | Sharpe only                                  | Sharpe AND PF                                     |
| Hyperopt landscape | Distinct candidates per seed (no overlap)    | Degenerate plateaus (638/1000 tied for seed-9001) |
| Diagnostic         | Per-trade edge too small for trade frequency | Wrong thesis: macro-filter dominates entry signal |

Two consecutive strategies have failed §14 in two different ways — the protocol is doing its job, and the project's discipline is intact (the strategies were killed; the bar was not lowered). The pattern across the two failures suggests that **the universe + timeframe (BTC/ETH spot, 4h primary + 1d informative) may be too narrow to support strategies with both high enough Sharpe AND high enough profitability to clear §14**. Phase 4's brainstorm should consider that hypothesis explicitly.

## What we keep (carry-over to Phase 4)

The full Phase 1-3 infrastructure remains usable for the next strategy:

- Pinned data manifest (`data-manifest.json` at sha256 `42982a04…`).
- Pinned freqtrade image (`sha256:6cb70a1b…`).
- Scripts: `run-hyperopt.sh` (with `--spaces buy sell` and `--strategy BollingerMeanRevert` defaults — both will need updating for the next strategy's class name and any new parameter spaces), `run-backtest.sh`, `run-walk-forward.sh`, `evaluate-pass-fail.py` (strategy-name parametrized, supports back-compat MFD evaluation; manifest validator now accepts 0 OR 4 walk-forward windows for Option B).
- Playbook: `docs/playbooks/phase-2-server-operations.md` §7.1 (long-run), §7.2 (OOS recipe).
- ADRs: 0008 (walk-forward), 0009 (selection rule), 0012 (BMR design rationale — historical record of the thesis selected and the alternatives rejected).
- Plan Option B precedent (recorded above) for OOS-decisive strategies.

## What we don't keep

`freqtrade/user_data/strategies/bollinger_mean_revert.py` stays in-tree but is no longer the live strategy. Phase 4 produces a new strategy file alongside it; the runtime selector (now in the run scripts as a `--strategy` flag default) selects which is active.

ADR-0010 (atr_mult range widening) remains MFD-specific. ADR-0012's decision-criteria lock (BMR-specific) is historical record only.

## References

- Verdict report: `docs/reports/2026-05-11-bmr-evaluation.md`
- Phase 3 spec: `docs/superpowers/specs/2026-05-11-phase-3-bmr-design.md` §7.6, §7.7 (predicted modal outcome — partial match: predicted PASS prior 30-50%; actual is FAIL with worse-than-predicted PF as binding)
- Phase 3 plan: `docs/superpowers/plans/2026-05-11-phase-3-bmr.md` (Plan Option B recorded in execution-time decision-stream)
- Hyperopt summary: `docs/reports/2026-05-11-phase-3b-hyperopt.md`
- ADR-0011 (MFD kill): `docs/decisions/0011-mfd-§14-fail-post-mortem.md`
- ADR-0012 (BMR thesis): `docs/decisions/0012-bmr-thesis-and-design-rationale.md`
- PRD §15 principle 2 (no re-tuning), principle 5 (no hidden mechanics)
- ADR-0008 (walk-forward), ADR-0009 (selection)
- Predecessor tag: `phase-3-bmr-killed`
