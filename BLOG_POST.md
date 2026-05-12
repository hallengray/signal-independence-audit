> **Note:** This is the canonical Markdown source. The published version at <HOSTING_PLATFORM_URL — to be filled at launch in Task 15> has links rewritten to absolute GitHub URLs.

# Four crypto strategy failures, and the tool that caught one in 3 seconds

> _Or: what happens when you bring software-engineering ADR discipline to retail quant research, then watch it produce an honest negative result._

## Hook

Most retail quant content reads "I found a strategy that backtests well." This post is the inverse.

Over four phases of work on BTC/USDT and ETH/USDT spot at the 4-hour timeframe, four different strategies were tested against pre-committed criteria: Sharpe > 1.0 AND profit factor > 1.4 out-of-sample. All four failed. The bar was never lowered. Across nineteen architecture-decision records the project never said "the threshold was too strict" — it documented why each strategy fell short and moved to the next question.

One of those four — a funding-rate-conditioned variant of a Donchian breakout — was killed in **~3 seconds of pure-Python testing**, before any of the planned 1000-epoch × 2-seed × 3-window hyperopt compute ran. The tool that produced that 3-second verdict is what this post ships. It's a four-screen pre-hyperopt audit called Signal Independence Audit (SIA), published as a standalone repo under Apache 2.0. The methodology applies to any candidate signal on any asset class; crypto was the surface where it was developed and stress-tested.

The rest of this post walks through each of the four failures in turn, then the literature audit that produced an unexpected corrigendum about how AI-assisted research goes wrong, then what survives the kills as reusable methodology. It ends on what a documented negative result actually is, and what it isn't.

If you only read one section, read the [Phase 4 SIA-kill section](#phase-4--fcmfd-funding-rate-conditioned-mfd--sia-killed-pre-hyperopt-in-3-seconds-the-lead-worked-example) — that's where the methodology earns its keep.

## Phase 2 — MFD (price-only trend-following) → §14 FAIL, Sharpe-bound

The first attempt was a Macro-Filtered Donchian Breakout — MFD. Entries fire when the 4-hour close breaks above an N-period Donchian high, gated by a daily-timeframe filter (daily close above a slow EMA, so trend-following only fires during macro uptrends). Exits are symmetric: a Donchian-low cross. Stops are ATR-scaled. Two seeds, 1000 hyperopt epochs each, top-5 candidates per seed evaluated out-of-sample across four calendar walk-forward windows.

The headline result: best out-of-sample Sharpe **0.314**, against a threshold of > 1.0. That's roughly 3× below the bar. The best per-window Sharpe across the four walk-forward windows was 0.553 (W3, Jan–Jun 2024) — still well short. Profit factor was not the problem: PF cleared 1.4 on multiple candidates, ranging 1.6–2.5 across the windows. The binding constraint was Sharpe.

The failure mode is informative: returns per unit volatility were too low, but the strategy was profitable on average. Stoploss-firing breakdowns showed ~100% of exits firing as `exit_signal` (the Donchian-low cross) with near-zero `stop_loss` and zero `roi` exits — meaning the per-trade edge depends on exit-signal timing, not on stoploss tightness, and that the edge is real but structurally too small relative to trade-noise variance. Wider ATR stops would not have closed the 3× Sharpe gap; the modal expected outcome had already been flagged before the hyperopt ran ([details](./case-study/01-mfd-kill-adr-0011.md)).

Phase 2's discipline holds: 0 of 4 walk-forward windows pass, the bar wasn't softened, and the ADR records exactly what the failure shape was — not "this strategy needs more tuning" but "this strategy class produces edge below threshold on this universe at this timeframe."

## Phase 3 — BMR (mean reversion) → §14 FAIL, Sharpe AND PF bound

If trend-following's per-trade edge was too small, mean reversion was the next obvious thing to try. Phase 3's strategy was BMR — Bollinger Mean Revert — entries when the 4-hour close drops below a lower Bollinger band, exits when it returns to the middle band, gated by the same daily-EMA macro filter as MFD (to avoid catching falling knives during macro downtrends).

Three seeds, top-5 hyperopt candidates per seed, 15 candidates evaluated out-of-sample total. Plan Option B was invoked to skip walk-forward — the trigger conditions for that option are conservative (all OOS candidates fail decisively AND multiple §14 criteria bind AND walk-forward would only confirm), and BMR cleared all three triggers.

Headline: **all 15 out-of-sample candidates were unprofitable**. Best OOS Sharpe -0.083 (seed=42 epoch=51). Worst -0.361. Mean across the 15: -0.180. Mean PF: 0.59 (best 0.85, worst 0.31). Every candidate was both unprofitable AND low-conviction ([details](./case-study/02-bmr-kill-adr-0013.md)).

This is a structurally worse failure than MFD's. MFD was profitable-but-inconsistent — its OOS Sharpe was below threshold but its PF cleared on multiple candidates. BMR was unprofitable-AND-inconsistent: all three seeds independently produced negative best in-sample Sharpe (−0.066 to −0.111), and the hyperopt landscape showed degenerate plateaus (638 out of 1000 epochs tied on one seed), which itself suggested the macro filter was dominating entries.

Two consecutive strategies failed §14 in two different ways. The pattern raised a hypothesis explicitly: maybe the universe + timeframe combination (BTC/ETH spot, 4-hour primary) is too narrow to support strategies with both high enough Sharpe AND high enough profitability to clear the bar. Phase 4 was scoped with that hypothesis on the table.

## Phase 4 — FCMFD (funding-rate-conditioned MFD) → SIA-killed pre-hyperopt in 3 seconds (the lead worked example)

By the start of Phase 4 there were two compute-expensive kills in the rearview. Each had cost roughly an hour of cloud hyperopt to produce a verdict that, in retrospect, was visible in the strategy's design before any hyperopt ran. MFD's per-trade edge was structurally too small. BMR's macro filter dominated entries. Both shapes — "candidate signal weaker than expected after accounting for what's already captured" — should have been catchable cheaply, but the pipeline didn't have a cheap mechanism for catching them.

So before spending another hyperopt budget on the natural Phase 4 candidate, I built one.

The Phase 4 candidate was FCMFD: MFD plus a funding-rate gate. The thesis was direct — when perpetual funding rates are low (longs are not crowded), forward breakouts have more room to run; when funding is high (longs are crowded), breakouts mean-revert. Funding rates are public on-chain data, free, and intuitive. The natural plan was: add a "funding < 60th-percentile of trailing 90-day window" gate to MFD's entry condition, hyperopt the rolling-window and threshold parameters, evaluate out-of-sample.

Before any of that, I built the Signal Independence Audit (SIA) — four mechanical screens that test whether a candidate signal adds information over a price-only baseline ([details](./case-study/03-sia-framework-adr-0014.md)). Screen 1: coverage (does the gate change trade frequency? Does it preserve enough trades for evaluation?). Screen 2: lift (do funding-gated entries' forward returns exceed price-only-gated entries by ≥ 0.5σ on ≥ 2 of 3 horizons?). Screen 3: Jaccard overlap on a small hyperparameter grid (does the gate's trade-set stay stable under perturbation?). Screen 4: information-split control (does the candidate signal explain more of the forward-return variance than realised volatility — the obvious confounder — explains?). The four screens run on the training window only, against a frozen rule set, and produce a JSON verdict. They take about 3 seconds.

The Phase 4 SIA ran and returned exit code 1 ([details](./case-study/04-fcmfd-sia-kill-adr-0015.md)):

| Horizon | Treatment mean | Control mean | Gap σ | Threshold | Verdict |
| ------- | -------------: | -----------: | ----: | --------: | :------ |
| 5d      |          0.85% |        0.25% | 0.147 |     0.500 | FAIL    |
| 10d     |          1.83% |        1.20% | 0.098 |     0.500 | FAIL    |
| 20d     |          3.78% |        3.69% | 0.016 |     0.500 | FAIL    |

The locked direction was qualitatively right — funding-gated entries outperformed price-only entries on all three horizons. The problem was magnitude: the gap σ values (0.147 / 0.098 / 0.016) sat well below the 0.5σ-pooled-stddev bar. By the 20-day horizon the gap was effectively zero. Screen 4 reinforced the verdict: vol-tercile separation on the 10-day horizon was 6.93 percentage points (low vol 5.14%, mid -1.79%, high 3.95%); funding-tercile separation was 2.45pp (low 3.50%, mid 2.77%, high 1.05%). Vol explained more of the forward returns than funding added.

The inversion check made the kill cleaner. ADR-0014 reserves a "Phase 4-prime" branch for the case where the _inverted_ signal direction shows ≥ 1.0σ separation — i.e., maybe the right interpretation is the opposite of what was hypothesised. The inversion cohort (funding > 40th percentile) underperformed control on **all three** horizons with **negative** gap σ. The thesis wasn't wrong about direction; it was right about direction and quantitatively too weak.

Here's where SIA earns the post's title. The Phase 4b 6-month smoke (Jan–Jun 2024) had looked _materially better_ than anything Phase 2 or 3 ever produced: +16.84% return, Sortino 2.04, daily wallet Sharpe 1.98. Without SIA, that smoke would have justified the full 1000-epoch × 2-seed × 3-window hyperopt run. SIA put the smoke in context: 18 trades over 6 months in a +46% market-change window, with a single March 2024 winner (+174 USDT) driving most of the PnL. Across the full 3.5-year training window — 313 conjunction trades, multiple regimes — the gate doesn't carry a tradeable lift. The smoke wasn't fraudulent; it was a small-sample regime-favourable artefact, and SIA was the mechanism that converted it from "promising signal" to "don't spend the compute" in 3 seconds.

Phase 2 burned roughly a Hetzner-hour × 4 windows to learn its shape of fact. Phase 3 burned a Hetzner-hour × 2 seeds. Phase 4 burned 3 seconds laptop time. That is the entire value proposition of pre-hyperopt screening.

## Phase 5 — literature audit, pre-committed gates, and the routing verdict

After three failures with three different failure modes (Phase 2 Sharpe-bound profitable; Phase 3 unprofitable on both criteria; Phase 4 candidate signal too weak vs vol), the productive next question wasn't "what strategy class do we try fourth?" It was: **is §14 empirically achievable on this surface at all?**

That's an evidence question, not a strategy-building question. So Phase 5 started with a two-day literature audit of published academic cryptocurrency-trading research, looking for a Tier-1 source reporting Sharpe > 1.0 AND PF > 1.4 OOS on a retail-realistic universe ([details](./case-study/05-literature-audit.md)). The audit produced a Criterion D verdict — mixed/inconclusive evidence — which routed to a structured next move: test the timeframe hypothesis cheaply (Path C), and gate any expensive follow-up (Path D) on four pre-committed verifications ([details](./case-study/06-phase-5b-decision-adr-0017.md)).

Path C: take Phase 2's locked MacroDonchian default parameters (no hyperopt, no signal-class change) and re-run them at 8-hour primary timeframe across the same four walk-forward windows. The narrow question: was 4h the binding constraint? Result ([details](./case-study/07-path-c-kill-adr-0018.md)) — 0 of 4 windows clear §14 at 8h. Per-window Sharpe means: **4h 0.425 vs 8h 0.415** (a 2% degradation, not an improvement). PF passed comfortably in all four 8h windows (1.45–2.07 range), so the binding constraint stayed exactly where it was at 4h: returns per unit volatility too low for this universe at this strategy class, regardless of candle cadence.

Path D Gate 1 was the next pre-committed verification: retrieve the full text of Fieberg/Liedtke/Metko/Zaremba 2023 (_Quantitative Finance_) — the closest paper in the audit's Criterion C set — and extract its profit factor figure for the long-only winner portfolio. If PF < 1.4 net of fees, Criterion C strictly fails on §14's AND-clause and the path forward routes to Path E (stop in-universe; ship the framework).

The full text was retrieved (via the CC-BY 4.0 published version on `open.icm.edu.pl`, after a header-tweaked HTTP request bypassed the JavaScript CAPTCHA — recorded for reproducibility). Findings ([details](./case-study/08-gate-1-pf-verification.md)):

- **Profit factor is never reported in the paper.** Anywhere. Zero matches across main results, the long-only robustness section (§4.4.2, Table 13), the liquidity-restricted subsamples (Table 12), the 768-design-choice robustness (Table 8), or the subperiod analysis (Table 5). The paper reports weekly mean return, standard deviation, Newey–West t-statistic, and annualised Sharpe. PF (or any close analogue) is **never computed and never tabulated**.
- **No transaction-cost analysis exists.** Zero matches for "transaction cost", "trading cost", "fees", "basis points", "bps", or "net of". All performance figures (Sharpe 1.28 for cross-sectional winners; Sharpe 1.09 for long-only winners minus risk-free; Sharpe 1.43 for the most-liquid-25% best variant) are **gross**.

This is strictly stronger than the gate's pre-committed FAIL condition. The metric required to evaluate the AND-clause doesn't exist in the source; the net-of-fees clause is unsatisfiable because no friction analysis is reported. Criterion E fires. Path D is foreclosed. Path E is routed: stop in-universe; ship the framework artefacts ([details](./case-study/09-path-e-routing-adr-0019.md)).

The routing isn't a soft conclusion. The gates were written into ADR-0017 _before_ Path C ran, specifically to prevent the failure mode of "Path C fails → grind on without sharper criteria." The pre-commit caught a 4–8 week false start (Path D infrastructure build) before it happened. That's the demonstrable value.

## The audit corrigendum — what AI-assisted literature research got wrong, and how it was caught

The Path D Gate 1 retrieval surfaced something the audit hadn't anticipated. The Phase 5a literature audit, working under paywall constraints and time pressure, had attributed two specific phrases to Fieberg et al 2023:

> "incurs substantial trading costs"

> "extracts alphas largely from short positions"

These phrases appeared in the audit's §5.6 verification update as caveats on the paper's headline Sharpe figures — framing them as evidence that the paper itself flagged friction degradation and short-side alpha capture.

**Neither phrase — nor its substantive content — appears anywhere in the paper.**

The misattribution survived the 2-hour focused audit because the original retrieval relied on search-result snippets and abstracts. The paywall prevented full-text verification at audit time. The narrative looked coherent — search snippets about cross-sectional momentum often _do_ discuss trading costs and short-side dynamics, and there's a Liu/Tsyvinski/Wu 2022 paper that addresses exactly those topics for cryptocurrency. It's the most likely actual source of the attributed phrasing. The audit's compressed-time retrieval co-mingled snippets across sources and attributed to one paper what another said.

The error was caught by construction. ADR-0017's Gate 1 was written into the Path D escalation pipeline for general epistemic-hygiene reasons — literature claims should be verified against full text before they fund infrastructure builds — not because this specific error was anticipated. When Phase 5d executed the gate, the full text didn't contain the attributed phrases. The pre-committed gate caught the error because the gate _was_ the verification mechanism ([standalone teaching artefact](./case-study/10-audit-corrigendum.md)).

The systemic lesson is what makes this section load-bearing for the rest of the post:

> **Paywall reliance + abstract-only summarisation produces attribution errors that survive review.**

The mechanism:

1. The paywall prevents full-text access at the moment of summarisation.
2. Search snippets and abstracts get integrated into the audit's narrative.
3. The narrative reads coherently — fluent summaries that _sound_ like the source.
4. Nothing in the audit's own evidence chain catches the misattribution.
5. The error propagates downstream into the artefacts the audit feeds (here: ADR-0017's framing of Criterion C's evidence weight; the §5.6 update).
6. Only forcing full-text retrieval for any load-bearing claim catches it.

This is sharpest when AI-assisted research is in the loop. LLMs do exactly what LLMs do — they produce fluent summaries that integrate sources without preserving granular "this exact phrase came from THIS source" attribution. Without an explicit "verify the load-bearing phrase against the full text" gate, the failure mode is structurally hard to catch. Reading the LLM's summary feels like reading the source; the prose discipline is indistinguishable. Only the bibliographic discipline is missing, and it's invisible inside the summary.

The defence is concrete: **for any load-bearing claim, require full-text verification before that claim drives a decision. Codify this as a pre-committed gate, not a soft norm.** Soft norms aren't enforced under time pressure. Gates are.

The corrigendum strengthens the Path E routing decision rather than weakening it. The original audit reading was "Fieberg et al claims Sharpe 1.28 but acknowledges substantial trading costs and short-side alpha capture." The corrected reading is "Fieberg et al claims gross Sharpe 1.28 (with 1.09 long-only, 1.43 most-liquid-25%-best-variant) but doesn't address trading costs at all and doesn't report profit factor." The corrected reading makes the paper an even thinner foundation for the original Path D scope. The literature's PF claim — the AND-clause of §14 — was never verified because the literature never reported it.

## What survives — the SIA harness and the framework artefacts

Five attempted-or-prevented in-universe phases, four strategy classes empirically tested, one literature foundation empirically verified and found wanting, one corrigendum. The strategy attempts terminate. The methodology survives.

**The SIA harness** ([source](./sia/), Apache 2.0) is the publishable artefact. Four mechanical screens that test whether a candidate signal adds information over a baseline, runnable on a laptop in seconds, with explicit pre-committed bar thresholds. Pre-hyperopt screening like this is published-ish in academic settings but operationally rare in retail tooling — most retail backtests either skip the question or answer it implicitly through hyperopt-then-OOS, which costs hours per signal hypothesis. SIA answers it in seconds, before hyperopt. The Phase 4 FCMFD case is the worked example of why that matters; the 16 unit tests + `mypy --strict` cleanliness are the polish that lets the harness ship as installable Python.

Installable via:

```bash
pip install -e git+https://github.com/hallengray/signal-independence-audit
```

The methodology generalises beyond crypto. The four screens are signal-agnostic: any candidate signal-vs-baseline comparison fits the shape, on any asset class with a forward-return horizon and a confounder available for the information-split control.

**Other framework artefacts** are catalogued in ADR-0019's "what we keep" section ([details](./case-study/09-path-e-routing-adr-0019.md)) but not extracted as separate standalone packages in this Phase 5e (could be later phases):

- **Deterministic backtest pipeline**: image-pinned Docker + sha256 data-manifest + cross-machine determinism check (laptop = cloud byte-for-byte). Applies to any Freqtrade-class strategy on any data.
- **Look-ahead-safe alignment patterns**: `merge_informative_pair(ffill=True)` discipline (for OHLCV joins across timeframes) + a custom non-OHLCV joiner with `merge_asof(allow_exact_matches=False)` for cadence-mixing signals like funding rates. Applies to any cadence-mixing problem.
- **Data manifest tooling**: schema-validated JSON manifests with sha256 verification + cross-platform LF parity handling.
- **Pre-committed audit methodology**: literature audit before strategy attempts, mechanical decision criteria pre-committed in scope docs, audit findings mapped to criteria mechanically rather than via judgment. The Path D escalation gates in ADR-0017 caught a 4–8 week false start — that's the demonstrable value of the methodology over soft norms.
- **ADR + post-mortem discipline**: numbered ADRs, post-mortem-on-kill pattern, cross-strategy comparison tables, references back to predecessor ADRs.

The case-study directory ([reading guide](./case-study/00-readme.md)) is the receipt — ten curated documents covering every kill, the methodology, the audit, the corrigendum, and the routing. Three reading paths: chronological for the full trajectory, SIA-methodology-focused for readers who want the tool, negative-result-focused for readers who want the disconfirmation story.

## What this isn't

Path E is not "the project failed." It is "the project produced a documented disconfirmation of the in-universe hypothesis, with mechanism, on a surface where the literature itself does not have positive evidence for retail-realistic strategies meeting the criteria." Those are different statements with different implications.

The §14 bar (Sharpe > 1.0 AND PF > 1.4) held throughout nineteen ADRs. It wasn't relaxed when Phase 2 fell short, when Phase 3 fell shorter, when Phase 4 was SIA-killed, when Path C's timeframe shift turned out flat, or when Path D Gate 1 found the foundational paper didn't even report the metric. The bar transitions from "contested-theoretical" (a bar someone _might_ clear if conditions are right) to "documented-empirical" (a bar that wasn't cleared on this surface across documented attempts under documented discipline). That's a strictly more useful state for the bar to be in than "contested-theoretical."

If anyone wants to deploy capital on BTC/USDT + ETH/USDT 4-hour spot long-only in the future, the case-study directory is the receipt. It names the universe, the strategy classes attempted (price-only trend-following, mean reversion, funding-conditioned trend-following, timeframe-shifted trend-following), the bar, the literature evaluated, the corrigendum, and the routing. A future operator can decide whether to revisit the surface _with new evidence_ rather than re-running the same experiments blind.

What this also isn't: a claim that crypto is unsuitable for systematic trading in general, or that the §14 bar is the right bar for every operator, or that funding-rate signals are categorically uninformative. The negative result is scoped narrowly to a documented universe, a documented bar, and four documented strategy attempts. Outside that scope, the artefact this post ships — the SIA harness — is precisely the tool you'd want to apply to whatever signal hypothesis is in scope for you.

## Footnotes / references

- **The case study**: [`./case-study/00-readme.md`](./case-study/00-readme.md) — reading guide for the ten curated documents. The audit corrigendum is at [`./case-study/10-audit-corrigendum.md`](./case-study/10-audit-corrigendum.md) as a self-contained teaching artefact about AI-assisted research failure modes.
- **The SIA harness**: this repo's [`./sia/`](./sia/) directory. Apache 2.0. Python 3.11+. Pandas + numpy hard deps; pytest + mypy as test extras; jupyter + matplotlib as notebook extras. Install: `pip install -e git+https://github.com/hallengray/signal-independence-audit`.
- **The source project's repo**: private. Scope B of the Phase 5e shipping decision intentionally excludes the strategy implementation code, hyperopt outputs, raw backtest data, and ops playbooks from the public artefact. The case-study directory is the curated evidence chain for the narrative above; the full source project is not part of what's published.
- **Maintenance posture**: this repository is published as a finished research project, not an actively-maintained tool. Issues are welcome and may be responded to selectively; there is no response time commitment. PRs may not be reviewed. Forks are welcome.
- **Author**: Femi Adedayo — hallengray@gmail.com.

_End of post._
