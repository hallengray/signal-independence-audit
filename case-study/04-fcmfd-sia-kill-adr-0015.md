> **For external readers:** This document is one of 10 curated case-study artefacts from Project Aṣe, a quantitative crypto-trading research project that produced a documented negative result with mechanism across four strategy attempts plus a literature audit, all under pre-committed criteria (Sharpe > 1.0 AND profit-factor > 1.4 OOS, called "§14" internally) that held without bar erosion across 19 ADRs. The full project repo is private (scope B of the Phase 5e shipping spec). Start with `./00-readme.md` for the reading guide. Read order context: The strongest worked example: Phase 4's FCMFD (Funding-Conditioned MFD) killed pre-hyperopt in ~3 seconds. The substance of the document below is unchanged from the internal version; only this framing block and personal/identifying content scrubs are added.

---

# ADR-0015: Phase 4 SIA FAIL — no hyperopt, no live ship

- **Status:** Accepted
- **Date:** 2026-05-12
- **Deciders:** Femi Adedayo
- **Approves:** Phase 4 design spec §4.5 FAIL routing; ADR-0014 §"Verdict routing" exit-1 branch.
- **Triggers:** `phase-4-sia-killed` tag.

## Context

Phase 4 ran the Signal Independence Audit (ADR-0014) against `FundingConditionedMFD` over the pooled BTC/USDT + ETH/USDT training window 2021-04-08 → 2024-12-31 (16,368 candles after the funding gate's 97-day warm-up). The orchestrator output:

```
SIA verdict: FAIL (exit 1)
horizons_passing=0/3 (Screen 2)
funding wider on 0/3 metrics (Screen 4)
inversion_trigger=false
```

Two of the four screens passed (1 and 3 — framework plumbing). Two failed (2 and 4 — the actual thesis). The inversion clause did not trigger, so Phase 4-prime is not authorised. This is a clean kill, no branch.

## Decision

`FundingConditionedMFD` does NOT enter hyperopt. The Phase 4 final tag is `phase-4-sia-killed`. Phase 7 (paper-trading) is NOT entered. The funding-rate signal — at the locked rule (`7-day rolling mean < 60th percentile of trailing 90-day distribution`) — is structurally inadequate as a binary entry gate for this universe (BTC/USDT + ETH/USDT spot, 4h primary timeframe).

The next operator conversation is universe revision (Phase 5 brainstorm: different signal class, different universe, or different timeframe), NOT another strategy attempt within the current universe. Phase 4 was designated the final attempt under the current PRD universe lock; that designation now binds.

## What bound, in plain English

The funding gate is **directionally correct but quantitatively too weak**. Across the 313 macro+breakout+funding-gate-pass candles, forward returns ordered correctly with funding tercile (lower funding → better future returns):

| Funding tercile | Mean 10d fwd ret | Win rate | Per-tercile Sharpe |
| --------------- | ---------------- | -------- | ------------------ |
| Low             | 3.50%            | 62.9%    | 0.377              |
| Mid             | 2.77%            | 53.5%    | 0.211              |
| High            | 1.05%            | 52.2%    | 0.081              |

So the locked direction ("low funding = uncrowded positioning = fresher breakout fuel") is qualitatively confirmed. The problem is the _magnitude_: the gap between treatment (funding-gated entries) and control (price-only MFD) at the 0.5σ-pooled-stddev test is far below threshold:

| Horizon | Treatment mean | Control mean | Gap σ | Threshold | Verdict |
| ------- | -------------- | ------------ | ----- | --------- | ------- |
| 5d      | 2.97%          | 1.86%        | 0.147 | 0.5       | FAIL    |
| 10d     | 3.66%          | 2.44%        | 0.098 | 0.5       | FAIL    |
| 20d     | 3.99%          | 3.69%        | 0.016 | 0.5       | FAIL    |

Treatment outperforms control by 60–110 bps depending on horizon, but the cohort variance is large enough that this lift is in the statistical noise floor. At 20d the lift is effectively zero (gap σ = 0.016, control mean is already 3.69%).

The information-split control (Screen 4) makes the diagnosis sharper: **realised volatility splits forward returns much more strongly than funding rate does**. Vol-tercile separation on the 10d horizon is 6.93 pp (low 5.14%, mid -1.79%, high 3.95%); funding-tercile separation is 2.45 pp (low 3.50%, mid 2.77%, high 1.05%). Funding loses on 3/3 metrics (mean / win rate / Sharpe separations). The conclusion is not "funding carries no information" — it does, monotonically — but **vol already explains more than funding adds**, so a vol-aware MFD baseline would absorb most of funding's signal anyway.

## Why the Phase 4b smoke was misleading

The Phase 4b smoke (Jan–Jun 2024, +16.84%, Sortino 2.04, daily wallet Sharpe 1.98) looked materially better than anything Phase 2 or 3 ever produced — and that read was honest given what we knew at the smoke moment. The SIA put it in context: 18 trades over 6 months in a +46%-market-change window, with a single Mar 2024 winner (+174 USDT) driving most of the PnL. Across the full 3.5-year training window (313 conjunction trades, multiple regimes), the gate doesn't carry a tradeable lift.

This is the value of the SIA hard gate: it converted a 6-month-window result that _could_ have justified a full 1000-epoch × 2-seed × 3-window hyperopt+OOS+walk-forward run into a 3-second mechanical verdict that says "don't spend the compute." Phase 2 and Phase 3 burned multi-hour hyperopt runs to learn the same shape of fact. ADR-0014 worked exactly as designed.

## Why the inversion clause did not trigger

ADR-0014 reserves Phase 4-prime authorisation for the case where the _inverted_ gate (funding > 40th percentile) shows ≥ 1.0σ separation on ≥ 2 of 3 horizons AND the locked direction fails Screen 2. The locked direction did fail Screen 2 (as documented above). But the inversion cohort (244 candidates, funding > 40th pct) underperformed control on **all three** horizons with **negative** gap σ:

| Horizon | Inversion mean | Control mean | Gap σ  | Threshold | Verdict |
| ------- | -------------- | ------------ | ------ | --------- | ------- |
| 5d      | —              | 1.86%        | -0.200 | 1.0       | FAIL    |
| 10d     | —              | 2.44%        | -0.155 | 1.0       | FAIL    |
| 20d     | —              | 3.69%        | -0.028 | 1.0       | FAIL    |

The inverted direction is not just non-significant — it's worse than the price-only baseline by a small consistent amount, in the same direction as the locked test (consistent with "low funding = better future returns" being the right ordering, even though the magnitudes are too small to clear bars in either direction).

So inversion is firmly not authorised. No Phase 4-prime.

## Why not re-tune

PRD §15 principle 2 forbids "kept tuning until it worked." The SIA bars are pre-committed in ADR-0014 and tested against the full training window with parametric + bootstrap evidence. The protocol made every methodologically allowed move:

- Three forward-return horizons searched (5d, 10d, 20d) per spec.
- Both the locked direction and the inverted direction tested (Screen 2 + inversion cohort).
- The vol-tercile control (Screen 4) explicitly normalises against the most obvious confounder.
- A 5×5 hyperparameter grid (Screen 3) confirmed the search space is meaningful.
- Code-path parity: SIA imports `_lib/` (`donchian_high`, `macro_filter`, `funding_gate`, `load_funding_aligned_to_4h`) which is the **same code the strategy class uses**. No "but the strategy implementation is slightly different from the audit" escape hatch.

Lowering the 0.5σ-pooled-stddev bar on Screen 2 to ~0.15σ to pass with the observed lifts would be exactly the bar erosion PRD §15.2 forbids. The thesis "funding rate carries entry-relevant information beyond price" was tested with pre-committed thresholds and failed.

## What we keep (carry-over to Phase 5)

The Phase 4 infrastructure remains in-tree as reusable framework for any Phase 5 strategy:

- **Funding-rate ingestion pipeline:** `scripts/pull-funding-rates.{py,sh}`, the `.gitignore` negation for `funding_rates/`, and the pinned `data-manifest.json` extension (`funding_rates` block alongside `files`).
- **Shared indicator package:** `freqtrade/user_data/strategies/_lib/` (donchian, macro_ema, funding_gate, load_funding_aligned_to_4h). The `funding_gate` and `load_funding_aligned_to_4h` modules implement the look-ahead-safe `pandas.merge_asof(direction="backward", allow_exact_matches=False)` pattern, which is reusable for any future signal joining 8h-or-other-cadence data into 4h candles.
- **SIA harness:** `scripts/sia/{screen_1_coverage,screen_2_lift,screen_3_jaccard,screen_4_information_split,run_sia}.py` plus the 16 unit tests. Reusable as a generic "does this auxiliary signal add information over the price-only baseline?" gate for any future Phase N strategy that introduces a new signal.
- **ADR-0014:** the SIA framework itself remains the authoritative protocol for testing orthogonal signal hypotheses pre-hyperopt.
- **`run-backtest.sh`** default now points at `FundingConditionedMFD` (commit `5d76757`). Any Phase 5 strategy will need to update this default the same way `run-hyperopt.sh` and `run-walk-forward.sh` were updated in `f2e6bcf`.
- **Cross-platform manifest LF parity fix:** `scripts/write-data-manifest.sh` now strips CR (commit `ffef580`); needed permanently regardless of which signals get pinned.

## What we don't keep

- `freqtrade/user_data/strategies/funding_conditioned_mfd.py` stays in-tree but is no longer a live candidate. Future Phase N strategies are new files alongside it.
- The Phase 4b 6-month smoke result (`docs/reports/2026-05-12-phase-4b-smoke.md`) stays as historical record. Its +16.84% / Sortino 2.04 should NOT be cited as evidence for any Phase 5 strategy — the SIA verdict is the binding context for that smoke.

## Cross-strategy comparison: Phase 2 MFD vs Phase 3 BMR vs Phase 4 FCMFD

| Dimension               | MFD (Phase 2e FAIL)          | BMR (Phase 3 FAIL)           | FCMFD (Phase 4 FAIL)               |
| ----------------------- | ---------------------------- | ---------------------------- | ---------------------------------- |
| Gate of failure         | §14 (post-hyperopt OOS)      | §14 (post-hyperopt OOS)      | **SIA (pre-hyperopt)**             |
| Compute cost to verdict | ~Hetzner-hour × 4 windows    | ~Hetzner-hour × 2 seeds      | **~3 seconds laptop**              |
| Best OOS Sharpe         | 0.314                        | -0.083                       | n/a (gated out)                    |
| Best OOS PF             | > 1.4 multiple               | < 1.0 all 15                 | n/a                                |
| Binding failure         | Sharpe-only                  | Sharpe AND PF                | Lift gap σ AND vol-control         |
| Direction confirmed?    | Yes (price breakouts work)   | Yes (mean-reversion fired)   | Yes (low funding ordered first)    |
| Thesis defect           | Edge too small for frequency | Macro filter dominates entry | Signal too weak vs vol-control     |
| Inverted variant?       | No symmetric inverse         | No symmetric inverse         | **Tested explicitly — also fails** |

Three consecutive strategies have failed under three different binding constraints. The patterns across the three failures sharpen the universe-revision hypothesis: **the universe + timeframe (BTC/USDT + ETH/USDT spot, 4h primary + 1d informative) may not support strategies with both high enough Sharpe AND high enough profitability AND independently informative orthogonal signals to clear the bars**. Phase 5 brainstorm should explicitly consider:

- A different signal class entirely (orderbook microstructure, on-chain flows, options skew, term-structure between perp and quarterly).
- A wider universe (top-10 alts, not just BTC/ETH).
- A different timeframe (1h or 15m for higher trade frequency to drive Sharpe at lower per-trade edge; or daily for swing-style horizon matching).
- A different strategy class (mean-reversion variants on alts where funding-driven liquidations create reversal opportunities; or pairs/basket relative-value strategies).

## What discipline held

- **No re-tuning.** SIA bars were pre-committed in ADR-0014 and applied verbatim.
- **No bar erosion.** Screen 2's 0.5σ threshold and Screen 4's "wider on ≥ 2/3 metrics" criterion are exactly what ADR-0014 §"Screen verdict criteria" specifies.
- **No selective reading.** The Phase 4b smoke result is in-tree as historical record; this ADR explicitly recontextualises it against the SIA evidence rather than retconning it.
- **No hidden mechanics.** The full SIA evidence JSON is committed in `docs/reports/2026-05-12-phase-4-sia.md`.
- **In-flight code fix recorded.** The `_screen_4_terciles` qcut bug (raw-value qcut with duplicates='drop' failing on clustered funding values) was fixed mid-run with a rank-first qcut. Documented in the SIA verdict commit message (`5227749`) and the Phase 4 plan Task 20 closeout note. No re-run with cherry-picked behaviour.

## References

- SIA verdict report: `docs/reports/2026-05-12-phase-4-sia.md` (full evidence JSON)
- Phase 4a data closeout: `docs/reports/2026-05-12-phase-4a-data.md`
- Phase 4b smoke report: `docs/reports/2026-05-12-phase-4b-smoke.md`
- Phase 4 spec: `docs/superpowers/specs/2026-05-11-phase-4-funding-conditioned-mfd-design.md`
- Phase 4 plan: `docs/superpowers/plans/2026-05-11-phase-4-funding-conditioned-mfd.md`
- ADR-0014 (SIA framework): `docs/decisions/0014-sia-framework.md`
- ADR-0011 (MFD §14 kill): `docs/decisions/0011-mfd-§14-fail-post-mortem.md`
- ADR-0013 (BMR §14 kill, template for this ADR): `docs/decisions/0013-bmr-§14-fail-post-mortem.md`
- PRD §15 principle 2 (no re-tuning), §15.2 (no bar erosion)
- Predecessor tag: `phase-3-bmr-killed` at `5e4a410`
- Successor tag (this kill): `phase-4-sia-killed`
