> **For external readers:** This document is one of 10 curated case-study artefacts from Project Aṣe, a quantitative crypto-trading research project that produced a documented negative result with mechanism across four strategy attempts plus a literature audit, all under pre-committed criteria (Sharpe > 1.0 AND profit-factor > 1.4 OOS, called "§14" internally) that held without bar erosion across 19 ADRs. The full project repo is private (scope B of the Phase 5e shipping spec). Start with `./00-readme.md` for the reading guide. Read order context: The Path E routing ADR + framework artefacts catalogue. Path E ≠ project failure; documented disconfirmation with mechanism. The substance of the document below is unchanged from the internal version; only this framing block and personal/identifying content scrubs are added.

---

# ADR-0019: Phase 5d Gate 1 FAIL — Path E routed, in-universe attempts terminated

- **Status:** Accepted
- **Date:** 2026-05-12
- **Deciders:** Femi Adedayo
- **Approves:** Phase 5 scope §5.1 Criterion E branch; ADR-0017 §"Path D escalation gates" Gate 1 verbatim routing.
- **Triggers:** `phase-5d-gate-1-killed` AND `phase-5e-path-e-routed` tags (two tags, same commit).

## Context

Phase 5d Gate 1 was a pre-committed, full-text verification step on the Fieberg / Liedtke / Metko / Zaremba (2023) _Quantitative Finance_ paper that ADR-0017 designated as the Tier-1 evidence base for Criterion C (cross-sectional factor momentum). ADR-0017 §7.4 fixed the gate language verbatim:

> "The Fieberg/Liedtke/Metko/Zaremba 2023 _Quantitative Finance_ paper must be obtained in full text. Profit factor for the long-only winner portfolio (or its closest reported analogue) must be extracted. If PF < 1.4 net of fees, Criterion C strictly fails on the AND-clause of §14, and the decision re-routes to **Criterion E (Path E)**, not Path D."

The Phase 5d Gate 1 report (`docs/reports/2026-05-12-phase-5d-gate-1-pf-verification.md`, commit `95bb62c`) executed this gate. Full text was obtained (CC-BY open-access PDF, channel #8 of the search trail). The findings, verbatim from the report:

1. **PF is not reported in the paper.** Anywhere. Not in Table 4 (headline performance), not in Table 13 (long-only winners financed with risk-free rate or BTC), not in Table 12 (liquidity subsamples), not in Table 8 (768-design-choice robustness), not in Table 5 (subperiod). The paper's risk-adjusted metric is Sharpe only. PF, gain-loss ratio, hit rate, win rate, success rate — none are computed.
2. **No transaction-cost analysis is reported.** Zero matches for "transaction cost", "trading cost", "fees", "basis points", "bps", "net of", "round-trip". All headline figures (Sharpe 1.28 CS winners; Sharpe 1.43 most-liquid-25% long-only winners; Sharpe 1.09 CS winners minus rf, Table 13 Panel A) are **gross** of friction.

Both findings are independently sufficient to FAIL the gate. The case is **strictly weaker** than the §7.4 verdict-table row "Full text obtained, PF reported only gross" (which already maps to FAIL): here, PF is not reported at all, and the net-of-fees clause cannot even be examined.

## Decision

**Path E is routed.** Per ADR-0017 §7.4 Gate 1 verbatim, Criterion E fires; Path D is foreclosed. In-universe strategy attempts on the BTC/USDT + ETH/USDT 4h spot long-only universe are terminated.

PRD §6 stays at **4h primary** indefinitely. The PRD §6 amendment clause requires a PASS to fire; the verdict is a final-form FAIL, so no amendment is applied.

The §14 bar (Sharpe > 1.0 AND PF > 1.4 OOS friction-adjusted) is **not lowered, not contested, not revised**. The bar transitions to a new status (see §"§14 bar status" below) — it is documented-not-met-on-this-universe, not eroded.

Two tags are applied at this ADR's commit:

- `phase-5d-gate-1-killed` — marks the Gate 1 FAIL transition.
- `phase-5e-path-e-routed` — marks the Path E entry / in-universe-attempts-terminated transition.

The two tags mark different decisions at the same commit and are kept distinct so future-readers can cite either transition specifically.

## What bound, in plain English

The Fieberg et al. paper, on direct full-text reading, does not actually publish the evidence ADR-0017 required it to publish. The headline Sharpe figures (1.28 cross-sectional winners; 1.43 in the most-liquid-25% subsample) are not contested — they are exactly what the audit said they were. The problem is that Sharpe alone does not clear §14's AND-clause. §14 requires PF > 1.4 _as well as_ Sharpe > 1.0, both net of fees. The paper:

- Does not report PF for any strategy in any table.
- Does not subtract any friction estimate from any strategy in any table.

Gate 1's premise — "extract PF for the long-only winner portfolio at retail-realistic net fees" — has no source data in the paper to extract from. There is no inferability path either: PF cannot be derived from (Mean, SD, t-stat, Sharpe) alone without distributional assumptions the paper does not make, and the gate language pre-committed in ADR-0017 §7.4 is explicit that PF must be _extracted_ from the paper, not estimated. So the gate's premise fails by construction. Criterion E fires.

The literature's "Sharpe 1.28" claim is real; it just does not reach §14's bar on paper, let alone after retail-realistic friction is subtracted.

## Why Path D is foreclosed

ADR-0017 §"Path D escalation gates" is structured as a logical AND across four gates. **Any single FAIL is terminal for Path D.** Gate 1 has FAILed in the strongest possible form — not "PF < 1.4 net" but "PF undefined in source, gross-only data". Gates 2–4 (universe match, net-of-fees Sharpe verification, methodological dissent resolution) are not executed because their value as gates was strictly conditional on Gate 1 passing. With Gate 1 failed, Gates 2–4 would only be relevant to a Path D scope that the AND-structure already forecloses.

To be explicit: a Path D scope document cannot be authored without satisfying _all four_ gates. Today's verdict makes the first gate unsatisfiable from the designated source.

## Why we don't re-evaluate

- **The paper's contents are fixed.** No additional literature search will change what Fieberg et al. (2023) reports. PF is not in the published version of record; that is final.
- **PRD §15.2 forbids bar erosion.** Lowering §14's PF clause or removing the "net of fees" clause to make Path D viable would be exactly the move PRD §15.2 prohibits.
- **PRD §15 principle 2 forbids re-tuning post-result.** Substituting a different Tier-1 paper after seeing Gate 1 fail would be cherry-picking the evidence base in the same shape as cherry-picking hyperparameters. If genuinely new Tier-1 evidence surfaces independent of this verdict, a fresh ADR can amend ADR-0017 — but not within this decision cycle.
- **The §14 bar held throughout.** It is not the bar that failed today. The universe + literature combination did not produce evidence that meets the bar.

## Cross-strategy comparison

Extending ADR-0018's four-column table with a Phase 5d Gate 1 column:

| Dimension                  | MFD (Phase 2e FAIL)       | BMR (Phase 3 FAIL)      | FCMFD (Phase 4 FAIL)       | MacroDonchian8h (Phase 5c FAIL) | **Phase 5d Gate 1 (Fieberg verification) FAIL** |
| -------------------------- | ------------------------- | ----------------------- | -------------------------- | ------------------------------- | ----------------------------------------------- |
| Gate of failure            | §14 (post-hyperopt OOS)   | §14 (post-hyperopt OOS) | SIA (pre-hyperopt)         | §14 (no hyperopt, diagnostic)   | **Literature gate (pre-strategy-build)**        |
| Compute cost to verdict    | ~Hetzner-hour × 4 windows | ~Hetzner-hour × 2 seeds | ~3 seconds laptop          | ~5 minutes laptop (6 backtests) | **~1 hour reading PDF + search trail**          |
| Best per-window OOS Sharpe | 0.553 (W3 @ 4h)           | -0.083                  | n/a (gated out)            | 0.586 (W1 @ 8h)                 | **n/a — never reached strategy build**          |
| Best per-window OOS PF     | 2.509 (W3 @ 4h)           | < 1.0 all 15            | n/a                        | 2.065 (W3 @ 8h)                 | **n/a — PF not reported in source paper**       |
| Binding constraint         | Sharpe (PF mostly OK)     | Sharpe AND PF           | Lift gap σ AND vol-control | Sharpe (PF clears in all 4)     | **PF not reported AND no net-of-fees data**     |
| Inverted variant tested?   | No                        | No                      | Yes — also fails           | n/a (no signal to invert)       | **n/a (no signal under test)**                  |

Five consecutive FAILs across five different binding constraints. Phase 2 and Phase 5c failed on the same shape (Sharpe-only). Phase 3 failed on both Sharpe and PF. Phase 4 failed on lift-gap σ (SIA framework). Phase 5d failed at the literature-evidence layer **before** a strategy was ever scoped. The convergent pattern: across in-universe strategy classes (breakout, mean-reversion, funding-conditioned, timeframe-shifted) and across the literature base ADR-0017 designated as the foundation for the next class to try (cross-sectional momentum), no path to §14 is supported by evidence on this universe.

## §14 bar status

The §14 bar (Sharpe > 1.0 AND PF > 1.4 OOS friction-adjusted) enters **documented-not-met-on-this-universe** status as of this ADR.

This is **not bar erosion**. The bar:

- Was set in PRD §14 before any strategy was built.
- Was held verbatim through Phase 2 (FAIL), Phase 3 (FAIL), Phase 4 (gated out by SIA), Phase 5c (FAIL), and Phase 5d Gate 1 (FAIL).
- Was never lowered, never softened, never amended.
- Was never the bottleneck in the sense of being unreasonable — the literature audit identified candidate strategy classes that the audit estimated _could_ clear it; the empirical verification today found that the cited Tier-1 evidence does not actually publish the metric the bar requires.

The bar transitions from a **contested-theoretical** state ("§14 might be achievable on this universe with the right strategy class — let's see") to a **documented-empirical** state ("across four strategy attempts plus a literature audit plus full-text verification of the designated Tier-1 source, §14 has not been met on this universe").

**This ADR is the receipt.** If any future operator — the original author, a collaborator, a fork — considers deploying capital on BTC/USDT + ETH/USDT 4h spot long-only, this ADR is the binding record that says: this surface has been tested under documented discipline and does not support §14-clearing strategies per current evidence. The receipt does not say "never possible". It says "not demonstrated, on documented evidence, as of this date".

## Phase 5a audit §5.6 corrigendum (primary finding)

The Phase 5a literature audit (`docs/reports/2026-05-12-pre-phase-5-literature-audit.md` §5.6) attributed the phrases _"incurs substantial trading costs"_ and _"extracts alphas largely from short positions"_ to Fieberg et al. (2023). Direct full-text reading (Gate 1 report §4.4, commit `95bb62c`) confirms:

- Neither phrase appears in the Fieberg et al. (2023) paper.
- The substantive content of the phrases is not in the paper either — the paper does not quantify trading costs anywhere, and does not claim alphas are concentrated in short positions. §4.4.2 of the paper discusses short-sale constraints as a research-design motivation for long-only variants in Table 13, but it does not characterise the paper's reported alphas as short-driven.
- The most plausible attribution conflation is with **Liu / Tsyvinski / Wu (2022)** ("Common Risk Factors in Cryptocurrency", _Journal of Finance_), which does discuss trading-cost realism and short-position contributions explicitly, or with one of **Zaremba**'s other cryptocurrency-anomalies papers (e.g., his 2024 cryptocurrency anomalies and economic constraints work that explicitly tackles implementation friction).

This corrigendum is recorded as a **primary finding of this ADR**, not a footnote, because it documents a specific failure mode of AI-assisted literature research that is independently valuable to future-readers:

> **Failure mode:** Paywall reliance + abstract-only summarisation = attribution errors that look authoritative.

The Phase 5a audit was executed under realistic constraints (no full-text access at the time; multiple Zaremba papers in the citation graph; abstract-level summarisation as the available evidence base). The conflation that resulted was an honest one, but it was load-bearing for ADR-0017's framing of Path C / Path D, and it would have remained load-bearing for any Path D scope document built on top of it. The pre-committed Gate 1 step is what exposed it, before — not after — 4–8 weeks of strategy work were sunk into a foundation that misread the source.

**The corrigendum strengthens the Gate 1 FAIL, not weakens it.** If the audit's verification-pass framing had been correct (i.e., if the paper itself had acknowledged "substantial" costs), Gate 1 would still FAIL because PF was never reported. The corrected reading is even more pristine: the paper does not comment on the cost question at all, leaving the gross-only evidence base unqualified.

**Teaching artefact.** Future literature audits under this framework should treat unverified-from-full-text claims as **provisional** and tag them in the audit text. Any pre-committed downstream gate that is load-bearing on a specific paper claim should include a full-text retrieval step _before_ a scope document is authored on top of it. The Path D gate structure already had this property by accident-of-design (Gate 1 fired before Path D scope was written); future audits should make it explicit-by-design.

## What we keep — the framework artefacts catalogue

These are the framework artefacts that survive the in-universe kill and constitute the genuine project output. They are listed with their reusability scope so future-readers can extract any subset independently.

### Publishable

- **SIA harness** — `scripts/sia/{screen_1_coverage,screen_2_lift,screen_3_jaccard,screen_4_information_split,run_sia}.py` plus the 16 unit tests, plus ADR-0014 as the protocol specification.
  - **Reusability:** applicable to **any signal hypothesis on any asset class** — not crypto-specific. Tests whether an auxiliary signal adds information over a price-only baseline using four pre-committed screens (coverage, lift, Jaccard overlap with control, information-split vs vol-control).
  - **Why publishable:** caught the BMR-class failure pattern in ~3 seconds of pure-Python testing where the Phase 2 and Phase 3 equivalents burned multi-hour hyperopt compute to learn the same shape of fact. The "test signal independence pre-hyperopt" pattern is rare in retail quant tooling.

### Reusable infrastructure

- **Deterministic backtest pipeline** — Hetzner-pinned Docker image + `data-manifest.json` schema with sha256 verification + cross-platform LF parity fix (`scripts/write-data-manifest.sh` CR-strip) + cross-machine determinism check (laptop vs Hetzner byte-for-byte JSON match).
  - **Reusability:** applicable to any Freqtrade-class strategy on any data. Cross-machine determinism for backtest outputs is not free out of the box.

- **Look-ahead-safe alignment patterns** — `freqtrade/user_data/strategies/_lib/load_funding_aligned_to_4h.py` (the `pandas.merge_asof(direction="backward", allow_exact_matches=False)` discipline) and the `merge_informative_pair(ffill=True)` usage pattern from the macro-EMA path.
  - **Reusability:** applicable to **any cadence-mixing problem**. The same code-shape works for 8h funding into 4h candles, 1d EMA into 4h or 8h candles, and any future non-OHLCV signal joining at a different cadence than the primary timeframe.

- **Data manifest tooling** — `scripts/write-data-manifest.sh`, `scripts/pull-historical-data.sh`, `scripts/pull-funding-rates.{py,sh}`, the `data-manifest.json` schema (files + funding_rates blocks), and the cross-platform LF parity fix.
  - **Reusability:** applicable to **any sha256-pinned data workflow** with cross-machine determinism requirements. Not Freqtrade-specific; not crypto-specific.

- **Data-integrity cross-check** — `scripts/verify-8h-vs-aggregated-4h.py` and its 6 unit tests.
  - **Reusability:** applicable to **any multi-timeframe data ingestion that needs aggregation verification**. The "aggregate the higher-resolution candle and check it equals the exchange-provided lower-resolution candle, byte-for-byte" pattern is generic.

- **Shared indicator package** — `freqtrade/user_data/strategies/_lib/` (`donchian_high`, `macro_filter`, `funding_gate`, `load_funding_aligned_to_4h`).
  - **Reusability:** crypto-strategy-specific; reusable across any future Freqtrade strategy on this codebase.

### Workflow discipline (the meta-artefact)

- **ADR discipline + pre-committed audit methodology.** The workflow itself:
  - Literature audit **before** strategy attempts (Phase 5a).
  - Pre-committed criteria mechanically applied (Phase 5b ADR-0017 fixed Path C / Path D / Path E gates in advance of any 5c work).
  - Post-mortem ADRs with cross-strategy comparison tables (ADR-0011, ADR-0013, ADR-0015, ADR-0018, this ADR).
  - Two-stage spec-then-quality review during execution (the superpowers spec + plan + review pattern under `docs/superpowers/`).
  - Tag-per-phase with phase predecessor / successor cross-references.
  - **Reusability:** applicable to **any quant research project**, and likely to any research project where the temptation to retrofit conclusions after seeing data is non-trivial. Not domain-specific.

## What we don't keep

- **In-universe strategy attempts: terminated.** No further hyperopt, no further walk-forward, no further smoke backtests, no further SIA runs against the BTC/USDT + ETH/USDT 4h spot long-only universe, under this PRD lock.
- **PRD §6 (4h primary timeframe): stays unchanged indefinitely.** The amendment clause requires PASS to fire.
- **The "timeframe was the binding constraint" hypothesis: empirically refuted** by Phase 5c (ADR-0018, see "Why the timeframe-shift hypothesis is decisively refuted"). Do not revisit without materially new evidence.
- **The "cross-sectional momentum literature supports retail-realistic strategies on this universe" hypothesis: empirically refuted** by Phase 5d Gate 1 today. Do not revisit without a different Tier-1 paper that reports PF and net-of-fees figures for a long-only winner portfolio at retail-realistic friction.
- **Funding-conditioned variants, mean-reversion variants, breakout variants on this universe: not to be revisited** without new evidence. This is the pattern-farming discipline — three negative results plus a literature-evidence failure is not an invitation to try variant #4 on the same surface.

## What discipline held

- **No bar erosion.** §14 bar unchanged across all five FAILs (Phases 2, 3, 4, 5c, 5d). Not lowered to fit Phase 2's best 0.553 Sharpe. Not lowered to fit Phase 3's negative Sharpe. Not lowered to fit Phase 5c's 0.586. Not lowered to fit Fieberg's gross-only data.
- **No parameter farming.** Each phase's parameter set was locked before the verdict (Phase 2 default → Phase 5c reuse; Phase 4 SIA pre-committed; Phase 5d gate language pre-committed in ADR-0017 §7.4). No post-result tuning to "rescue" a verdict.
- **No retconning.** ADR-0011, ADR-0013, ADR-0015, ADR-0018, and this ADR all describe their verdicts as the post-mortem of pre-committed criteria, not as opportunistic reinterpretation. Phase 5a audit's §5.6 corrigendum is treated as a corrigendum, not airbrushed.
- **No quiet escalation to Path D on weak evidence.** This is the load-bearing one. The natural temptation after ADR-0018 (Path C FAIL) was to scope Path D immediately on the cross-sectional momentum hypothesis and start building. The pre-committed Gate 1 step caught the 4–8 week false start **before** Path D scope was written. Discipline at the routing decision, not just at the verdict decision.
- **Pre-commit on Path D gates was load-bearing.** The Gate 1 mechanism in ADR-0017 §7.4 was not theatre — it actually fired, it actually changed the routing, and it produced a corrigendum that improves future audit methodology. Pre-commitment is only valuable if it sometimes fires; today it fired.

## Bigger picture

Five phases of attempted-or-prevented in-universe work. Four strategy classes empirically tested (MFD, BMR, FCMFD, MacroDonchian8h). One literature foundation empirically verified and found wanting (Fieberg et al. 2023). One corrigendum exposed before-the-fact that would have biased any Path D scope on top of it.

At each decision point, discipline held:

- No bar erosion across five FAILs.
- No parameter farming.
- No retconning of prior phase results.
- No quiet escalation when the cheap-test (Path C) failed and the temptation was to jump to the expensive-test (Path D) on the assumed-correct framing.
- The pre-committed Gate 1 step caught a load-bearing literature misattribution before it shaped 4–8 weeks of strategy work.

The project converged on a **documented negative result with mechanism**, which is more valuable than producing a deployable strategy that wouldn't have worked. Two specific reasons:

1. **The negative result has a receipt** (this ADR + the four predecessor kill ADRs + the Phase 5a audit + Phase 5d Gate 1 report). The receipt names the universe, the strategy classes attempted, the bar, the literature evaluated, the corrigendum, and the routing. A future operator reading this can decide whether to revisit the surface with new evidence rather than re-running the same experiments blind.
2. **The framework artefacts are genuinely rare for retail quant work.** SIA-style pre-hyperopt signal-independence testing is published-ish in academic settings but operationally rare in retail tooling. Cross-machine deterministic Freqtrade pipelines with sha256-pinned data manifests are not free out of the box. Pre-committed audit methodology with mechanical verdict application is essentially absent from the retail-quant literature. The infrastructure has value independent of any specific strategy succeeding on top of it.

## What Phase 5e is

Phase 5e is the **packaging and publication phase**. It is a fundamentally different _kind_ of work than Phases 2–5d, which were strategy attempts. Phase 5e is about shipping the framework artefacts catalogued above as standalone reusable infrastructure — most obviously the SIA harness (publishable per §"What we keep"), and secondarily the deterministic-backtest + look-ahead-safe-alignment + data-manifest tooling as a coherent quant research substrate.

The Phase 5e scope document (boundaries, deliverables, success criteria for the packaging work) is the **next operator conversation**, not part of this ADR. The `phase-5e-path-e-routed` tag at this commit marks the entry; the scope is authored separately.

## References

- Phase 5d Gate 1 verification report: `docs/reports/2026-05-12-phase-5d-gate-1-pf-verification.md` (commit `95bb62c`)
- ADR-0017 (Phase 5b Path C + Path D gates, the pre-commit authority): `docs/decisions/0017-phase-5b-path-c-and-path-d-gates.md`
- ADR-0018 (Phase 5c PATH-C-KILL, immediate predecessor): `docs/decisions/0018-phase-5c-path-c-kill.md`
- ADR-0015 (Phase 4 SIA kill, structural template for this ADR): `docs/decisions/0015-phase-4-sia-kill.md`
- ADR-0014 (**SIA framework — publishable artefact**): `docs/decisions/0014-sia-framework.md`
- ADR-0013 (BMR §14 kill): `docs/decisions/0013-bmr-§14-fail-post-mortem.md`
- ADR-0011 (MFD §14 kill): `docs/decisions/0011-mfd-§14-fail-post-mortem.md`
- Phase 5a literature audit (the corrigendum target): `docs/reports/2026-05-12-pre-phase-5-literature-audit.md` §5.6
- Phase 5 scope (Criterion E branch authority): `docs/phases/phase-5-scope.md` §5.1
- PRD §6 (primary timeframe lock), §14 (the bar), §15 principle 2 (no re-tuning), §15.2 (no bar erosion)
- Fieberg, C., Liedtke, G., Metko, D., & Zaremba, A. (2023). Cryptocurrency factor momentum. _Quantitative Finance_, 23(12), 1853–1869. DOI: [10.1080/14697688.2023.2269999](https://doi.org/10.1080/14697688.2023.2269999). Open-access PDF: https://open.icm.edu.pl/items/d9f44e22-0614-4db8-8585-6dcba8906bb5
- Predecessor tag: `phase-5c-path-c-killed` at `d1bd6c7`
- Successor tags (this ADR): `phase-5d-gate-1-killed` AND `phase-5e-path-e-routed` (two tags, same commit)
