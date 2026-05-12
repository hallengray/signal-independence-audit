> **For external readers:** This document is one of 10 curated case-study artefacts from Project Aṣe, a quantitative crypto-trading research project that produced a documented negative result with mechanism across four strategy attempts plus a literature audit, all under pre-committed criteria (Sharpe > 1.0 AND profit-factor > 1.4 OOS, called "§14" internally) that held without bar erosion across 19 ADRs. The full project repo is private (scope B of the Phase 5e shipping spec). Start with `./00-readme.md` for the reading guide. Read order context: The decision ADR that locked Path C first + pre-committed the four Path D escalation gates. The substance of the document below is unchanged from the internal version; only this framing block and personal/identifying content scrubs are added.

---

# ADR-0017: Phase 5b Decision — Path C first, Path D gated, Path E in reserve

- **Status:** Accepted
- **Date:** 2026-05-12
- **Deciders:** Femi Adedayo
- **Approves:** Phase 5 scope §5.1 mechanical application; ADR-0015 §"next operator conversation is universe revision" handoff.
- **Triggers:** `phase-5b-decided` tag.

## Context

Phase 5a executed the pre-Phase-5 literature audit specified in `docs/phases/phase-5-scope.md` §4. The audit is committed in two parts: the v1 report at commit `8fdb5e4` and the open-source verification update at commit `389b756`. Together they constitute the evidence base on which Phase 5 scope §5.1's pre-committed criteria fire.

The binding question from scope §4.1 was:

> _"What Sharpe ratios and profit factors do published / open-source crypto trading strategies actually achieve on retail-accessible surfaces, particularly BTC/ETH spot long-only at various timeframes?"_

After two waves of search across 12 queries, ~25 candidate sources reviewed and 14 cited (8 Tier-1 peer-reviewed, 2 Tier-2 working papers, 3 Tier-3 institutional, 1 absence-as-finding), the audit's central findings are:

- **Row A1 of the achievability matrix is empty.** No Tier-1/2 study identifies an OOS-Sharpe-and-PF-passing strategy on BTC/ETH 4h spot long-only specifically. Academic crypto literature concentrates on daily, weekly, or sub-hour intraday horizons; the 4h window is essentially absent.
- **Hudson & Urquhart 2021** (Tier-1 _Annals of Operations Research_, ~14,919 trading rules, 2010–2017 sample): no out-of-sample predictability for Bitcoin specifically. Predictability persists for other cryptocurrencies.
- **Cross-sectional crypto momentum literature shows Sharpe-passing results in some specifications.** Fieberg/Liedtke/Metko/Zaremba 2023 (Quantitative Finance) reports long-only winner-portfolio Sharpe 1.28 weekly-rebalanced on 3,900+ coins. Cryptocurrency Market Risk-Managed Momentum 2025 reports Sharpe 1.42 (risk-managed) / 1.12 (plain).
- **The verification pass refined those positive readings materially.** Sharpe across Tier-1 specifications ranges 0.45–1.42 (Liu/Tsyvinski/Wu's 1-week top quintile yields Sharpe 0.45). The papers themselves acknowledge "substantial trading costs," tail risk, and "considerable uncertainty implying greater risk than previous research has suggested." Profit factor is universally unverified.
- **The Grobys & Shahzad 2024 dissent** (Tier-1 _International Journal of Finance & Economics_) argues realised variance of crypto momentum follows a power-law process such that the Sharpe metric is mathematically undefined for crypto momentum.

The audit's §9 summary one-liner: _"Criterion D fires. The §5.1 decision routes to Path C first. Path D escalation requires satisfying the four post-verification gates in §7.4 — failing which the decision re-routes to Path E."_

## Decision

**Phase 5c begins on Path C.** Concretely: PRD §6 will be amended to move the primary timeframe from 4h to 8h, and MFD will be re-run on 8h BTC/USDT + ETH/USDT spot data as the cheap test of the timeframe-shift hypothesis. Estimated duration per scope §6 Path C: 1–2 weeks. The Phase 5c scope document is the next deliverable after this ADR.

**Path D is authorised conditionally, not unconditionally.** If Path C fails its own SIA or §14, Path D may only proceed after all four gates in audit §7.4 are satisfied (re-listed in §"Path D escalation gates" below). If any gate cannot be satisfied, the decision re-routes to Path E (stop in-universe, ship the SIA framework).

**Path B is rejected.** The literature does not support "a fifth signal class within the same 4h BTC/ETH long-only universe" as the highest-leverage move. Three signal classes have already failed §14 in distinct ways under different binding constraints.

**Path E is in reserve, not triggered today.** Cross-sectional positive Sharpe evidence (caveated and specification-dependent) is present in the literature, so strict Criterion E does not fire at this audit. Bar revision is therefore NOT a legitimate option at this point per scope §7.5.

## Mechanical application of §5.1 criteria

Pre-committed criteria from `docs/phases/phase-5-scope.md` §5.1, applied to the audit findings:

| Criterion | Requirement                                                                                 | Audit evidence                                                                                                          | Verdict           |
| --------- | ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----------------- |
| **A**     | ≥ 2 Tier 1/2 studies, Sharpe > 1.0 AND PF > 1.4 OOS friction-adj, BTC/ETH 4h spot long-only | 0 qualifying studies. Matrix row A1 empty. Hudson & Urquhart finds no BTC OOS predictability.                           | **Does not fire** |
| **B**     | Multiple studies showing Sharpe improvement on 8h+ timeframes for majors long-only          | Directional improvement only (Quantpedia: 0.33 → 0.80). No Tier-1/2 study clears §14 on majors long-only at any non-4h. | **Does not fire** |
| **C**     | Long-only cross-sectional perp evidence achieving §14, mechanism not long-short asymmetry   | Sharpe 0.45–1.42 across Tier-1 specifications. PF unverified everywhere. Sources self-flag "substantial trading costs." | **Does not fire** |
| **D**     | Mixed/inconclusive: cells with partial evidence, no clean winner                            | A empty, B partial, C partial-positive with material caveats (range 0.45–1.42, PF unverified, methodological dissent).  | **FIRES**         |
| **E**     | No published evidence §14 achievable anywhere on retail-accessible long-only crypto spot    | Cross-sectional has positive Sharpe evidence even if caveated. Strict E does not fire today.                            | **Does not fire** |

Criterion D's decision branch (verbatim from scope §5.1): _"Path C first (smaller change, cheaper test). If C fails its own SIA or §14, escalate to Path D."_ The audit's verification update tightens that escalation: Path D is gate-conditional, not automatic.

## Why this routing is honest given the evidence

- **Criterion A's strict reading is honored.** No 4h-specific Tier-1/2 study clears §14 on BTC/ETH long-only spot. The strict 4h scope locked pre-execution forecloses Criterion A by construction _given the literature's granularity_, which is the discipline working as designed — not a deficiency.
- **Criterion B's directional signal exists but doesn't clear the bar.** Timeframe shift toward daily/weekly shows _some_ improvement; nothing meets the strict §14 threshold on majors long-only spot. This is what makes "8h is cheap to test" different from "8h is empirically supported" — and Path C is a test, not a commitment.
- **Criterion C's evidence is real but specification-dependent.** The cleanest Sharpe-clearance claims are on the broader cryptocurrency universe (3,900+ coins, weekly rebalanced), not BTC/ETH alone. Liu/Tsyvinski/Wu's long-leg-degrades-with-volume finding implies top-N perps would land at the _weakest_ part of the momentum cross-section. This is why Path D needs gates, not green light.
- **The Grobys & Shahzad dissent cannot be ignored.** It's peer-reviewed in IJFE, not a fringe view. It tempers Sharpe-1.28-to-1.42 readings into "the strategies generate returns but the standard risk-adjusted metric may not apply." Any Path D plan must address this or substitute metrics.
- **Path C as a first step is consistent with "smaller change, cheaper test."** If 8h MFD passes §14, the constraint was timeframe and Phase 5c closes with a §14-clearing strategy. If it fails, the failure itself is informative — it locates the constraint as not _just_ timeframe — and the Path D gate-check executes with sharper context.

## Path D escalation gates (pre-committed, binding)

Lifted verbatim from audit §7.4. These are pre-committed in this ADR as binding constraints on any future Path D scope document. **Path D is not authorised until all four gates are satisfied.** If any gate fails, the decision re-routes to Path E.

**Gate 1 — Full-text PF verification.** The Fieberg/Liedtke/Metko/Zaremba 2023 _Quantitative Finance_ paper must be obtained in full text. Profit factor for the long-only winner portfolio (or closest reported analogue) must be extracted. If PF < 1.4 net of fees, Criterion C strictly fails on the AND-clause of §14, and the decision re-routes to Criterion E (Path E), not Path D.

**Gate 2 — Universe match.** Path D scope as currently drafted (top-N liquid perps, BTC/ETH/SOL/BNB/XRP minimum) does not match the literature's evidentiary universe (3,900+ coins). Either (a) Path D scope is expanded to top-20 or top-50 perp universe with explicit liquidity gates, OR (b) full-text retrieval of Fieberg et al / Liu-Tsyvinski-Wu confirms the cross-sectional momentum effect persists when restricted to top-10 by volume. Without one of these, Path D's empirical foundation is inadequate.

**Gate 3 — Net-of-fees Sharpe verification.** The 2025 Risk-Managed Momentum paper's "robust to transaction costs" claim must be quantified. What friction magnitude was tested (1 bp? 10 bp? 50 bp?), and what is actual net Sharpe at realistic crypto retail fees (typically 10–20 bp round-trip on Binance spot)? If the paper tested friction at < 10 bp, the result does not generalise to retail Binance and Path D's foundation weakens further.

**Gate 4 — Methodological dissent resolution.** Grobys & Shahzad's Sharpe-undefinability finding must be addressed. Either Path D plan acknowledges the strategy is built on a metric the literature itself contests, OR substitutes a metric not requiring finite second moments (Calmar, Sterling, max-drawdown-relative). The first is acceptable if explicit; the second is preferable.

## What invalidates this decision

This decision is invalidated, in whole or in part, by any of the following:

1. **Path C MFD-on-8h outcome:** This is the obvious downstream branch.
   - _Path C passes §14:_ Decision validated — universe was the constraint, project has a §14-clearing strategy. ADR-0017 closes successfully.
   - _Path C fails §14 (most likely):_ Decision routes to the Path D gate-check above. If all four gates pass → Path D scope authorised. If any gate fails → Path E.
   - _Path C fails SIA pre-§14:_ Same routing as §14 fail, but with stronger Path E pull (constraint is structural, not strategy-specific).

2. **New Tier-1 evidence surfaces that PF-verifies the literature.** If a peer-reviewed paper appears that reports full-text profit factor > 1.4 net of realistic retail fees for long-only crypto momentum (especially on a top-N-by-volume universe), Gate 1 is satisfied pre-emptively. This could route Phase 5c around Path C directly into gated Path D — but only with a new ADR amending this one.

3. **Path C surprise pass that invalidates the universe-constraint read.** If Path C passes §14 but inspection reveals the pass is driven by an artefact (e.g., a single regime window, look-ahead in 8h data alignment, lookahead in macro-1d filter at 8h cadence), the validation does not transfer to a sound §14 clearance. Re-open the audit's interpretation of Phases 2/3/4 failures and the cross-phase universe-constraint hypothesis.

4. **Friction reality at Binance retail diverges materially from Path C's backtest assumptions.** If during Path C execution we discover that realistic Binance spot retail fees (incl. partial-fill slippage, withdrawal-cost amortisation, taker-fee tier reality) are materially higher than the 10–20 bp the audit assumed, the §14 bar's net interpretation shifts. A Path C net-Sharpe pass at 20 bp may not survive at 35 bp, in which case the routing changes.

5. **Bar revision (§14 itself) is NOT a valid invalidation route from this ADR.** Per scope §7.5 and §8.2, bar revision is only legitimate under Criterion E with documented evidence. Today Criterion E does not fire. If Path C fails AND any Path D gate fails, Criterion E becomes the routing — and only at that point does bar revision become a documented option for separate ADR-led discussion.

Triggers 2 and 3 require a new ADR amending or superseding ADR-0017. Trigger 1 fires per the routing already specified above. Trigger 4 is handled inside the Path C scope document (the audit constraint becomes the friction-cost spec).

## What we keep, what we don't

### Carry-over from Phase 4 to Phase 5c (Path C)

- **`run-backtest.sh`, `run-hyperopt.sh`, `run-walk-forward.sh` default strategy targets** — these point at `FundingConditionedMFD` today (commit `5d76757`). Path C will introduce a new strategy file (8h MFD variant) and update these defaults.
- **MFD strategy logic** (`freqtrade/user_data/strategies/macro_donchian.py` and the underlying `_lib/` indicators) — reused unchanged at 8h primary. This is the entire point of Path C as a cheap test.
- **Data manifest infrastructure** (`scripts/write-data-manifest.sh`, the `.gitignore` negation pattern, cross-platform LF handling at commit `ffef580`) — extended to cover the 8h candle set.
- **SIA harness** (`scripts/sia/*.py` + tests) — reused if Path C introduces any new signal class beyond the timeframe shift. If Path C is a pure timeframe-shift test of pure-price MFD, SIA does not apply (no orthogonal signal to audit).
- **§14 evaluation pipeline** — the OOS-Sharpe-and-PF evaluator from Phases 2/3 remains the verdict gate.

### Discarded for Phase 5c

- **The 4h primary timeframe lock in PRD §6.** Path C amends PRD §6 to 8h primary. This is the universe revision Phase 5c executes; it is _allowed_ explicitly because Phase 4 was designated the final 4h attempt per ADR-0015 §"next operator conversation."
- **The 4h funding-conditioned variant.** `freqtrade/user_data/strategies/funding_conditioned_mfd.py` stays in-tree as historical record (per ADR-0015), but is not the Path C target.

### Preserved as historical record (do not delete, do not cite as live evidence)

- `docs/reports/2026-05-12-phase-4b-smoke.md` — the misleading-pre-SIA 6-month smoke.
- `docs/reports/2026-05-12-phase-4-sia.md` — the SIA verdict that gated FCMFD out.
- `docs/reports/2026-05-12-pre-phase-5-literature-audit.md` — the v1+verification audit this ADR concludes from.

## Cross-phase context

Three consecutive in-universe attempts failed §14 under three different binding constraints (ADR-0011, ADR-0013, ADR-0015):

| Phase | Strategy | Binding gate                  | Compute cost              | What it ruled out                                 |
| ----- | -------- | ----------------------------- | ------------------------- | ------------------------------------------------- |
| 2     | MFD      | §14 OOS Sharpe (best 0.31)    | Hetzner-hours × 4 windows | "Price-only trend-following on 4h BTC/ETH"        |
| 3     | BMR      | §14 OOS PF (all 15 < 1.0)     | Hetzner-hours × 2 seeds   | "Mean-reversion on 4h BTC/ETH"                    |
| 4     | FCMFD    | SIA pre-hyperopt (lift gap σ) | ~3 seconds laptop         | "Funding-rate as an orthogonal entry gate to MFD" |

The Phase 5a literature audit then asked the meta-question Phases 2-4 could not answer in isolation: _is the §14 bar empirically achievable on this surface at all?_ The audit's evidentiary answer:

- **Not on 4h** (row A1 empty across all Tier-1/2 sources).
- **Maybe on daily/weekly** for cross-sectional ranking strategies, _on a broader universe than BTC/ETH alone_, _with PF unverified everywhere_, _with publication bias tilting positive results_, _with one Tier-1 dissent on metric reliability_.
- **No clean evidence anywhere** that the strict §14 (Sharpe > 1.0 AND PF > 1.4 OOS friction-adjusted) is jointly satisfied on retail-accessible BTC/ETH long-only at any timeframe.

The mechanical-criterion application above resolves this distribution-of-evidence as Criterion D, not Criterion C (the literature is genuinely caveated, not unambiguous) and not Criterion E (some positive evidence does exist).

## What discipline held

- **No bar erosion.** §14 (Sharpe > 1.0 AND PF > 1.4) is not revised by this ADR. The audit verifies it is not yet refuted as achievable; that's a different question from lowering it.
- **No criterion revision.** §5.1's A–E were pre-committed in scope `9c767b4`. The audit findings determined which fires; the criteria themselves were not re-shaped to favour a preferred outcome.
- **No "evidence is X but I feel Y" routing.** Criterion D fires by mechanical application of the matrix. The decision branch (Path C first, Path D conditional, Path E in reserve) follows §5.1's text verbatim.
- **Verification before lock.** The operator raised three caveats on the v1 audit (compression, PF unverified across Criterion C sources, universe-mismatch for Path D). The audit performed an open-source second pass before this ADR was written. The verification refined Criterion C's strength downward and operationalised the Path D escalation gates — both of which materially strengthen Path E's standing as a real downstream option.
- **Pre-committed gates.** The §7.4 Path D gates are recorded in this ADR before Path C runs, which is exactly the discipline the operator's recommendation 2 asked for: tighten the Path D bar _now_, while we still don't know Path C's outcome, so that the gates cannot be retroactively softened if Path C fails and the path forward feels narrow.

## References

- Phase 5 scope: `docs/phases/phase-5-scope.md` (commit `9c767b4`)
- Phase 5a audit v1: `docs/reports/2026-05-12-pre-phase-5-literature-audit.md` (commit `8fdb5e4`)
- Phase 5a audit verification update: same file, §5.6 + §7.4 added (commit `389b756`)
- PRD: `docs/PRD.md` §§6, 7, 14, 15
- ADR-0011 (MFD §14 kill): `docs/decisions/0011-mfd-§14-fail-post-mortem.md`
- ADR-0013 (BMR §14 kill): `docs/decisions/0013-bmr-§14-fail-post-mortem.md`
- ADR-0014 (SIA framework): `docs/decisions/0014-sia-framework.md`
- ADR-0015 (Phase 4 SIA kill): `docs/decisions/0015-phase-4-sia-kill.md`
- Predecessor tag: `phase-4-sia-killed` at `1efa022`
- Successor tag (this decision): `phase-5b-decided`
