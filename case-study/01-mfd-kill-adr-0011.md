> **For external readers:** This document is one of 10 curated case-study artefacts from Project Aṣe, a quantitative crypto-trading research project that produced a documented negative result with mechanism across four strategy attempts plus a literature audit, all under pre-committed criteria (Sharpe > 1.0 AND profit-factor > 1.4 OOS, called "§14" internally) that held without bar erosion across 19 ADRs. The full project repo is private (scope B of the Phase 5e shipping spec). Start with `./00-readme.md` for the reading guide. Read order context: The first §14-bar kill: Phase 2's MFD (Macro-Filtered Donchian) post-mortem. The substance of the document below is unchanged from the internal version; only this framing block and personal/identifying content scrubs are added.

---

# ADR-0011: MFD §14 FAIL post-mortem — no live ship, no re-tuning

- **Status:** Accepted
- **Date:** 2026-05-11
- **Deciders:** Femi Adedayo
- **Approves:** Phase 2e spec §1 goal 6, §7.6
- **Triggers:** `phase-2-mfd-killed` tag

## Context

Phase 2e ran the full §14 evaluation protocol (Phase 2e spec §4): widened-`atr_mult` smoke (seed 9001), branch-decision, OOS candidate-union evaluation across three seeds, 4-window walk-forward per ADR-0008, and the formal `scripts/evaluate-pass-fail.py` harness. The harness output:

```
VERDICT: FAIL
**Binding constraint:** no OOS candidate passes crit 1-5
```

Phase 2d already flagged this as the modal expected outcome (Phase 2e spec §7.6). The OOS Sharpe gap from Phase 2d (best 0.27 vs threshold > 1.0) was ~4×; walk-forward + a third seed + atr_mult widening could plausibly close some of that gap but not the full 4×.

## Decision

Macro Donchian Filter (MFD) does NOT ship. The Phase 2 final tag is `phase-2-mfd-killed`. Phase 7 (paper-trading) is NOT entered for MFD. Phase 3 (new strategy thesis) becomes the immediate next phase.

## What bound, in plain English

Sharpe (crit 3, threshold > 1.0) was the binding constraint across every single OOS candidate (15 of 15, best 0.314 at seed=42 epoch=4 with params `(36, 7, 171, 2.3)`) and every walk-forward window (0 of 4 consistent, best W3 Sharpe 0.553 testing Jan–Jun 2024). The best OOS Sharpe of 0.314 was a marginal +0.04 improvement over Phase 2d's 0.27 — directionally consistent with the predicted "some gap closure but not the full 4×" but nowhere near the threshold. The diagnostic shift confirmed by the stoploss-firing breakdown is decisive: ~100% of exits fire as `exit_signal` (the donchian_exit lower-band crossing), with near-zero `stop_loss` and zero `roi` exits — meaning the strategy's edge depends on exit-signal timing rather than stoploss tightness, and ADR-0010's `atr_mult` widening to 1.5–6.0 was therefore a methodological no-op for §14 outcomes (which is itself useful evidence: the per-trade edge is structurally too small relative to trade frequency, regardless of seed or regime).

## Why not re-tune

PRD §15 principle 2 forbids "kept tuning until it worked." The protocol made every methodologically allowed move:

- Three seeds searched (42, 1337, 9001).
- Two `atr_mult` ranges searched (1.5-4.0 and, if Branch B, 1.5-6.0; cap is hard at two iterations per ADR-0010).
- 4-window walk-forward applied per ADR-0008 (rolling, in-training, single seed for regime-isolation).
- 3-way overlap selection rule applied per ADR-0009.

A fourth seed, a third widening, or alternative hyperopt-loss functions would be "kept tuning until it worked" — the exact antipattern §15 principle 2 forbids. Future strategies will run the same protocol; if the protocol fails three strategies in a row, that's evidence the protocol is too strict (revise PRD), not that the strategies were close to working (re-tune them).

## What we keep

The full Phase 2 infrastructure remains usable for the next strategy:

- Pinned data manifest (`data-manifest.json` at sha256 `42982a04…`).
- Pinned freqtrade image (`sha256:6cb70a1b…`).
- Scripts: `run-hyperopt.sh` (with `--timerange-override`), `run-backtest.sh`, `run-walk-forward.sh`, `evaluate-pass-fail.py`.
- Playbook: `docs/playbooks/phase-2-server-operations.md` §7.1 (long-run) + §7.2 (OOS recipe).
- ADRs: 0008 (walk-forward), 0009 (selection), 0010 (atr_mult widening; only if Branch B was taken).

The §14 harness in particular is strategy-agnostic — Phase 3's strategy will reuse it unchanged.

## What we don't keep

`freqtrade/user_data/strategies/macro_donchian.py` stays in-tree but is no longer the live strategy. Phase 3 produces a new strategy file alongside it; the runtime config selects which is active.

## References

- Verdict report: `docs/reports/2026-05-11-mfd-evaluation.md`
- Phase 2e spec: `docs/superpowers/specs/2026-05-10-phase-2e-mfd-verdict-design.md` §7.6
- PRD §15 principle 2 (no re-tuning), §15 principle 5 (no hidden mechanics)
- ADR-0008 (walk-forward), ADR-0009 (selection), ADR-0010 (atr_mult widening, if Branch B)
- Phase 2d closeout (which already flagged FAIL as modal): `docs/reports/phase-2d-hyperopt-oos.md`
