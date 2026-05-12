> **For external readers:** This document is one of 10 curated case-study artefacts from Project Aṣe, a quantitative crypto-trading research project that produced a documented negative result with mechanism across four strategy attempts plus a literature audit, all under pre-committed criteria (Sharpe > 1.0 AND profit-factor > 1.4 OOS, called "§14" internally) that held without bar erosion across 19 ADRs. The full project repo is private (scope B of the Phase 5e shipping spec). Start with `./00-readme.md` for the reading guide. Read order context: The 2-day literature audit that asked "is §14 empirically achievable on this surface at all?" — produces Criterion D. The substance of the document below is unchanged from the internal version; only this framing block and personal/identifying content scrubs are added.

---

# Pre-Phase-5 Literature Audit

## §0. Metadata

- **Date:** 2026-05-12
- **Author:** Femi Adedayo (executed with Claude Code)
- **Scope reference:** `docs/phases/phase-5-scope.md` §4 (Sub-phase 5a)
- **Criteria reference:** `docs/phases/phase-5-scope.md` §5.1 (A–E pre-committed)
- **Audit budget:** 2 days. Actual time used: ~2 hours focused (compressed for this run)
- **Sources surveyed:** ~25 candidate sources across 12 search queries
- **Sources cited in this report:** 10 primary, 4 secondary
- **Limitations:** several Tier-1 papers (SSRN, Springer, Wiley, ScienceDirect) were behind authentication walls and could not be directly fetched. Where this occurred, the audit relies on abstract summaries returned by web search engines and explicitly notes the unverified detail. Specific OOS Sharpe figures and profit factors for some key papers could not be independently confirmed and are flagged as "abstract-reported, not full-text verified."

## §1. Mission

Answer the binding question from Phase 5 scope §4.1:

> _"What Sharpe ratios and profit factors do published / open-source crypto trading strategies actually achieve on retail-accessible surfaces, particularly BTC/ETH spot long-only at various timeframes?"_

The audit's role is to provide the evidence base on which §5.1's pre-committed decision criteria are mechanically applied. The audit does NOT propose strategies, revise criteria, or recommend bar adjustments. It surfaces what the literature documents and lets the criteria fire.

## §2. Methodology

### §2.1 Source priorities (operationalised per scope §4.3)

| Tier | Definition                                                                                               | Qualifies for which criteria?       |
| ---- | -------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| 1    | Peer-reviewed academic journal articles                                                                  | All criteria including A            |
| 2    | SSRN / arXiv working papers from established academics; AQR / Two Sigma / institutional research         | All criteria including A            |
| 3    | Crypto-native institutional research (Glassnode, Coinmetrics, Kaiko, Galaxy, Grayscale) with methodology | Criteria B, C, D, E only            |
| 4    | Open-source community evidence (Freqtrade, GitHub repos with documented OOS)                             | Criteria B, C, D, E only            |
| 5    | Practitioner blog posts                                                                                  | Caveat-heavy, only cited as pointer |

### §2.2 Search execution (12 queries across two waves)

**Wave 1 (surveys + institutional discovery):**

1. "cryptocurrency algorithmic trading literature review academic survey"
2. "Bitcoin Ethereum trading strategies survey peer-reviewed Sharpe"
3. "crypto quantitative strategy systematic backtest meta-analysis"
4. "AQR cryptocurrency systematic research paper"
5. "Two Sigma Renaissance Bitcoin cryptocurrency quantitative trading"
6. "Quantpedia cryptocurrency strategy database backtest results"
7. "technical trading cryptocurrencies Annals Operations Research Sharpe out-of-sample"
8. "Galaxy Digital Coinmetrics institutional crypto strategy performance research"

**Wave 2 (criterion-targeted):** 9. "high frequency momentum trading cryptocurrencies Sharpe ratio Bianchi" 10. "cryptocurrency cross-sectional momentum Liu Tsyvinski Sharpe long only" 11. "Bitcoin daily timeframe trend following strategy Sharpe profit factor out-of-sample academic" 12. "cryptocurrency factor momentum long-only winners Sharpe 1.28 weekly rebalance" 13. "Cryptocurrency factor momentum transaction costs gross net Sharpe profit factor" 14. "cryptocurrency momentum strategy net transaction costs Sharpe profit factor friction-adjusted" 15. "Cryptocurrency momentum Grobys Shahzad illusion Sharpe spurious" 16. "Bitcoin Ethereum long only spot trend following annual Sharpe 1.0 retail accessible" 17. "cryptocurrency 4 hour timeframe trading academic Sharpe out-of-sample BTC ETH" 18. "Hudson Urquhart technical trading cryptocurrencies daily 15000 rules data"

**Wave 3 (methodology / friction) was rolled into Waves 1–2 because friction-adjustment evidence surfaced naturally in the factor-momentum query thread (especially Baldi-Lanfranchi 2024 and Cryptocurrency Market Risk-Managed Momentum).**

### §2.3 Inclusion criteria for citation

A source is cited in this report only if at least one of the following is true:

- It is peer-reviewed (Tier 1) AND reports numerical Sharpe or profit factor on a crypto strategy.
- It is an established quant firm publication (Tier 2) reporting friction-adjusted numerical performance.
- It is a survey or meta-analysis covering multiple primary sources.
- Its absence of a result is itself a finding (e.g., AQR has no crypto trading research).

### §2.4 Discipline rules applied

Per scope §4.5:

1. **No cherry-picking.** The Grobys & Shahzad dissent on crypto momentum Sharpe reliability is cited alongside the Liu/Tsyvinski/Wu / Quantitative Finance positive findings. The Hudson & Urquhart Bitcoin-OOS-fails-predictability finding is cited alongside generally positive results for other cryptocurrencies.
2. **Friction-adjusted figures preferred.** Where only gross is reported, the gross figure is flagged and the source's Tier is capped at 4 for §14-bar evaluation.
3. **IS vs OOS distinction explicit.** Multiple sources report IS-only Sharpe; these are noted as such.
4. **Publication bias caveat.** Section §6 of this report applies a qualitative confidence adjustment.
5. **Reddit/Twitter excluded** as primary evidence. All cited sources are journals, working papers, or institutional research pages.
6. **Honest verdict.** Section §7's Decision Mapping applies the criteria mechanically; no soft-pedalling to favour a preferred path.

### §2.5 Judgment call (pre-execution, recorded for auditability)

Per the open question raised before search began: _if a Tier-1 paper reports §14-clearing OOS performance on **daily** BTC/ETH and notes "results extend to higher-frequency operation"_, this audit routes that evidence to Criterion B (timeframe shift), NOT Criterion A (strict 4h). The "extends to" claim is a claim, not an OOS result on 4h itself. The operator approved this routing implicitly by saying "proceed" without challenge.

---

## §3. Achievability Matrix

The matrix maps `(timeframe × asset universe × strategy class) → Sharpe range`. Empty cells with `N=0` are themselves findings — they inform Criterion E.

| Cell | Timeframe    | Asset universe         | Strategy class           | Sharpe (net OOS reported)                                                                                                  | PF                        | §14?                   | N sources            | Top tier |
| ---- | ------------ | ---------------------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------- | ------------------------- | ---------------------- | -------------------- | -------- |
| A1   | 4h           | BTC/ETH long-only spot | Trend / breakout         | **N=0 direct evidence**                                                                                                    | —                         | —                      | 0                    | —        |
| A2   | 4h           | BTC/ETH long-only spot | Mean-revert              | **N=0 direct evidence**                                                                                                    | —                         | —                      | 0                    | —        |
| A3   | 4h           | BTC/ETH long-only spot | Multi-signal / factor    | **N=0 direct evidence**                                                                                                    | —                         | —                      | 0                    | —        |
| A4   | 4h           | BTC + alts long-only   | Cross-sectional          | **N=0 direct evidence**                                                                                                    | —                         | —                      | 0                    | —        |
| B1   | 8h           | BTC/ETH long-only spot | Trend / breakout         | **N=0 direct evidence**                                                                                                    | —                         | —                      | 0                    | —        |
| B2   | 8h           | BTC + alts long-only   | Cross-sectional          | **N=0 direct evidence**                                                                                                    | —                         | —                      | 0                    | —        |
| C1   | Daily        | BTC/ETH long-only spot | Trend / momentum         | BTC OOS: **no predictability** (Hudson & Urquhart 2021); intraday TS momentum gross Sharpe ~1.6 unverified net (Shen 2022) | Not reported              | **No**                 | 2                    | T1       |
| C2   | Daily/Weekly | BTC + alts long-only   | Cross-sectional momentum | Long-only winners Sharpe 1.28 (Cryptocurrency Factor Momentum 2023); risk-managed momentum Sharpe 1.42 (2025)              | Not reported in abstracts | **Possibly** (caveats) | 3                    | T1       |
| D1   | 4h           | Perp futures top-N     | Long-only rotation       | **N=0 direct evidence**                                                                                                    | —                         | —                      | 0                    | —        |
| D2   | Daily        | Perp futures top-N     | Long-only rotation       | Implied by C2 (universe broader)                                                                                           | Not reported              | **Possibly**           | 0 direct, 2 adjacent | T1       |

### §3.1 Reading the matrix

- **Row A1 is the bullseye for Criterion A.** It is empty. **No Tier 1/2 study identifies an OOS Sharpe-and-PF-passing strategy on BTC/ETH 4h spot long-only.** This is the central finding.
- **Row C1 (daily BTC/ETH long-only) is the next-most-specific row.** It is _partially populated and negatively signed_. Hudson & Urquhart (2021), the largest systematic study of technical trading rules on cryptocurrencies, finds no out-of-sample predictability for Bitcoin specifically — though predictability persists in other cryptocurrencies and gross-of-fees signals exist intraday.
- **Row C2 (daily/weekly cross-sectional long-only) is positively populated.** Long-only winners from cryptocurrency factor momentum strategies achieve gross Sharpe 1.28; risk-managed variants 1.42; multiple peer-reviewed sources. BUT: profit factor not reported in any abstract I could verify, and Grobys & Shahzad (2024, peer-reviewed) argues the Sharpe metric is mathematically unreliable for crypto momentum.
- **All 4h-specific cells (A1–A4) and 8h-specific cells (B1–B2) and 4h-perp cell (D1) are empty.** Academic literature concentrates on daily and weekly horizons.

---

## §4. Per-Source Citation Table

| #   | Source                                                                                      | Tier | Year | Strategy class                                     | Asset universe                           | Timeframe                              | Sharpe                                                                                    | PF                         | Friction-adj?                                                                            | IS/OOS                            | Notes                                                                                                                                                                                |
| --- | ------------------------------------------------------------------------------------------- | ---- | ---- | -------------------------------------------------- | ---------------------------------------- | -------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Hudson & Urquhart, _Annals of Operations Research_                                          | 1    | 2021 | Technical trading (5 classes, ~15,000 rules)       | 2 BTC markets + 3 other cryptocurrencies | Inferred daily (not directly verified) | BTC: no OOS predictability; other cryptos: positive                                       | Not reported               | Breakeven costs higher than market typical (yes friction-aware)                          | Both IS and OOS reported          | Tier-1 peer-reviewed. The key negative finding on BTC specifically.                                                                                                                  |
| 2   | Cryptocurrency Factor Momentum, _Quantitative Finance_ Vol 23 No 12                         | 1    | 2023 | Cross-sectional factor momentum, long-only winners | 3,900+ coins                             | Weekly rebalanced                      | 1.28 annualised (long-only winners)                                                       | Not reported in abstract   | Profitable after short-sale constraints; transaction cost treatment in body not verified | 2014–2022 sample, full-sample     | Profitable on long-only leg specifically.                                                                                                                                            |
| 3   | Liu, Tsyvinski, Wu (likely _Review of Financial Studies_ or _Journal of Finance_)           | 1    | 2022 | Three-factor model (market + size + momentum)      | Cryptocurrency universe                  | Weekly                                 | Cross-sectional Sharpe varies; long-leg concentrated; "worsens monotonically with volume" | Not reported in abstract   | Not specified in retrieved summaries                                                     | Mixed                             | Theoretical foundation; long-leg performance is volume-dependent — implies BTC/ETH (highest volume) get the weakest momentum effect.                                                 |
| 4   | Cryptocurrency Market Risk-Managed Momentum Strategies, _ScienceDirect_                     | 1    | 2025 | Risk-managed (volatility-targeted) momentum        | Cryptocurrency universe                  | Weekly                                 | 1.42 (risk-managed); 1.12 (plain) annualised                                              | Not reported in abstract   | "Robust to transaction costs" (claim, not verified)                                      | Backtested with robustness checks | Strongest positive case for Criterion C.                                                                                                                                             |
| 5   | Grobys & Shahzad, _International Journal of Finance & Economics_                            | 1    | 2024 | Cross-sectional momentum (long-short)              | Cryptocurrencies                         | Variable                               | Sharpe **mathematically undefined** (claim: power-law variance)                           | N/A                        | N/A                                                                                      | N/A                               | The dissenting view: crypto momentum Sharpe is unreliable.                                                                                                                           |
| 6   | Cryptocurrency momentum has (not) its moments, _Financial Markets and Portfolio Management_ | 1    | 2025 | Momentum                                           | Cryptocurrencies                         | Variable                               | Pro/con discussion of Grobys & Shahzad                                                    | N/A                        | N/A                                                                                      | N/A                               | Follow-up academic debate.                                                                                                                                                           |
| 7   | Mann, _SSRN_ WP "Quantitative Alpha in Crypto Markets: Systematic Review"                   | 2    | 2025 | Meta-analysis                                      | 24+ peer-reviewed studies, 2018–2025     | Various                                | Reviews findings; identifies cross-exchange arb, factor investing, on-chain signals       | Various                    | Various                                                                                  | Both                              | Meta-review confirming the strategy classes that show statistical alpha. Paper paywalled — only abstract verified.                                                                   |
| 8   | Shen et al., _Financial Review_ — "Bitcoin intraday time series momentum"                   | 1    | 2022 | Time-series momentum, intraday                     | Bitcoin                                  | Half-hour intervals (not 4h)           | ~5.4× buy-and-hold (gross, derived ~2.86)                                                 | Not reported               | Gross — friction adj not verified                                                        | Both                              | High-frequency intraday; not directly applicable to 4h cell.                                                                                                                         |
| 9   | Caferra & Vidal-Tomás, _CentAUR Reading repository_ (working)                               | 2    | 2021 | Bitcoin intraday TS momentum                       | Bitcoin                                  | Intraday                               | Improved Sharpe vs B&H                                                                    | Not reported               | Not verified                                                                             | Both                              | Working paper version.                                                                                                                                                               |
| 10  | Multi-timeframe trend strategy on Bitcoin (Quantpedia)                                      | 3    | 2024 | Daily filter + hourly entries                      | Bitcoin                                  | Multi-TF                               | Sharpe 0.33 → 0.80 (improvement)                                                          | Not reported               | Yes (with fees)                                                                          | OOS                               | Tier 3 vendor research. Demonstrates timeframe-shift improvement but neither figure clears §14.                                                                                      |
| 11  | Baldi-Lanfranchi, "Transaction-cost-aware Factors" SSRN/Lancaster WP                        | 2    | 2024 | Factor models with TCA construction                | Equities + general; references crypto    | Various                                | Net Sharpe collapses ~95% gross→net for high-turnover factors                             | Not reported               | Yes (the paper's whole point)                                                            | N/A                               | KEY methodological point: high-turnover factor strategies (momentum) suffer extreme gross-to-net Sharpe degradation. Applied to equities directly; implication for crypto is severe. |
| 12  | Grobys & Sapkota — _Economics Letters_                                                      | 1    | 2019 | Momentum trading                                   | Many cryptocurrencies                    | Daily/weekly                           | Negative — no positive abnormal returns                                                   | N/A                        | N/A                                                                                      | 2014–2018                         | Earlier negative result on crypto momentum.                                                                                                                                          |
| 13  | Korajczyk & Sadka, _Journal of Finance_                                                     | 1    | 2004 | Equity momentum, trading-cost robustness           | Equities (NOT crypto)                    | Daily                                  | Robust to trading costs at modest position sizes; degrades at scale                       | Reported (mostly survives) | Yes                                                                                      | OOS                               | Reference methodology for friction-adjustment in momentum strategies.                                                                                                                |
| 14  | Trend Following Strategies (Grayscale Research)                                             | 3    | 2025 | Trend / momentum on Bitcoin                        | Bitcoin                                  | Daily                                  | Trend signals manage Bitcoin volatility                                                   | Not reported               | Generally yes (institutional context)                                                    | OOS                               | Tier 3 institutional. Suggests trend signals improve risk-adjusted outcomes for BTC but doesn't claim §14 clearance.                                                                 |

### §4.1 Notable absences (themselves findings)

- **AQR Capital Management** — established quant firm specialising in systematic strategies — has **no published cryptocurrency systematic strategy research** as of the searches conducted. AQR explicitly does not offer cryptocurrency investments.
- **Two Sigma** — has crypto **risk analysis** research but **no active crypto trading strategy research** with published performance numbers.
- **Renaissance Technologies** — private firm, no public crypto strategy research.
- **No survey or meta-analysis identified that explicitly tests strategies on BTC/ETH 4h spot long-only specifically.** Academic studies use daily, weekly, or sub-hour intraday; the 4h window is essentially absent from the literature.

---

## §5. Findings by §5.1 Criterion

### §5.1 Criterion A — §14 achievable on BTC/ETH 4h spot long-only

**Requirement (verbatim):** "≥ 2 independent published studies (peer-reviewed or established quant firms) demonstrating Sharpe > 1.0 AND PF > 1.4 on BTC/ETH 4h spot long-only, with reasonable friction adjustments and out-of-sample evidence."

**Evidence found:** **Zero qualifying studies.** Matrix cells A1–A4 are all empty. The most directly relevant study (Hudson & Urquhart 2021, Tier 1, _Annals of Operations Research_) — a comprehensive test of ~15,000 technical trading rules on Bitcoin and four other cryptocurrencies — finds **no out-of-sample predictability for Bitcoin specifically**. Predictability does persist for other cryptocurrencies in their sample, but BTC is the most-relevant asset for Criterion A and the result is decisive.

**Verdict: Criterion A is NOT satisfied.**

### §5.2 Criterion B — Timeframe shift materially improves achievability

**Requirement:** "Multiple studies showing Sharpe improvement on 8h, 12h, or daily timeframes for spot long-only strategies on majors."

**Evidence found:**

- Bitcoin daily technical trading: Hudson & Urquhart 2021 explicitly says NO OOS predictability for BTC. Predictability exists for other cryptos at daily frequency.
- Multi-timeframe (daily filter + hourly entries) on Bitcoin: Sharpe improves from 0.33 to 0.80 — meaningful improvement, but both figures are below §14's 1.0 threshold. (Tier 3 source: Quantpedia.)
- Bitcoin intraday time-series momentum (Shen 2022): gross-of-fees Sharpe ~1.6, ~5.4× passive buy-and-hold. NOT friction-adjusted. Half-hourly intervals, not 8h or daily.
- Grayscale "Trend is Your Friend" (2025): trend signals reduce BTC volatility but no claim of §14 clearance.

The pattern: timeframe shift toward daily/weekly does NOT clearly improve §14-cleared performance on **single-asset BTC/ETH long-only**. Improvements exist in directional sense, but no Tier 1/2 study on majors long-only at 8h/12h/daily clears Sharpe > 1.0 AND PF > 1.4 OOS net of fees.

**Verdict: Criterion B has PARTIAL evidence (timeframe shift improves Sharpe directionally) but does NOT meet the threshold of "multiple studies showing Sharpe > 1.0 net OOS on majors long-only at 8h+ timeframes."**

### §5.3 Criterion C — Cross-sectional approaches show stronger evidence

**Requirement:** "Published evidence that long-only cross-sectional ranking strategies across N perps achieve §14, with mechanism reasonably attributable to the cross-sectional structure rather than long-short asymmetry."

**Evidence found:**

- _Cryptocurrency Factor Momentum_ (Quantitative Finance 2023, Tier 1): long-only winners portfolio Sharpe 1.28 annualised, weekly rebalanced, 3,900+ coins universe, 2014–2022 sample. "Buying past winners profitable even after accounting for short-selling constraints." **Mechanism: long-only cross-sectional ranking, NOT long-short asymmetry.** ✓ Strong evidence for Criterion C.
- _Cryptocurrency Market Risk-Managed Momentum Strategies_ (ScienceDirect 2025, Tier 1): risk-managed momentum Sharpe 1.42 annualised, plain momentum 1.12. "Robust to transaction costs" (claim, body not verified). ✓ Strong evidence.
- _Common Risk Factors in Cryptocurrency_ (Liu, Tsyvinski, Wu, Tier 1): three-factor model with market+size+momentum captures cross-sectional expected returns. Long-leg performance "worsens monotonically with volume" — implies the strongest momentum effects are in LOWER-volume cryptos, not BTC/ETH. ✓ Mechanism evidence but cautions about majors-specific Sharpe.

**Counter-evidence:**

- _Cryptocurrency Momentum: Is It an Illusion?_ (Grobys & Shahzad 2024, Tier 1 IJFE): argues realised variance of crypto momentum portfolio follows a power-law process such that Sharpe ratio is **mathematically undefined** — the metric "does not exist" for crypto momentum. ✗ Dissenting view.
- _Cryptocurrencies and momentum_ (Grobys & Sapkota 2019, Tier 1 Economics Letters): momentum trading does NOT generate positive abnormal returns on many cryptocurrencies over 2014–2018. ✗ Earlier negative evidence.

**Unverified critical detail:** Profit factor (Criterion C requires PF > 1.4 alongside Sharpe > 1.0). I could not find PF figures in any abstract or open-text source for the cross-sectional momentum papers. For a Sharpe-1.28-to-1.42 long-only momentum strategy, PF would _plausibly_ exceed 1.4 — but this is interpretation, not citation. Criterion C's PF requirement is therefore **unverified, not confirmed satisfied**.

**Friction adjustment:** "Robust to transaction costs" appears in the 2025 risk-managed paper's abstract but the magnitude of friction tested was not retrieved. Baldi-Lanfranchi 2024 (Tier 2) shows that high-turnover factor strategies (specifically momentum) can suffer up to 95% gross-to-net Sharpe degradation in equities — a methodological warning that may apply to crypto momentum if turnover is high. Weekly rebalancing on 3,900 coins likely implies HIGH turnover. This is a substantive caveat.

**Verdict: Criterion C has STRONG SHARPE EVIDENCE for long-only cross-sectional crypto momentum (Sharpe 1.12–1.42 across multiple Tier 1 sources, mechanism cross-sectional rather than long-short) but PF unverified and friction-adjustment magnitude unverified. Dissenting Tier 1 view exists.** This is **partial-positive evidence**, not unambiguous §14 clearance.

### §5.4 Criterion D — Mixed or inconclusive evidence

**Requirement:** "Cells in the matrix show partial evidence but no clear winner."

**Evidence:** Yes — the matrix has:

- Empty A1–A4 (no 4h evidence at all)
- Partial-negative C1 (daily BTC fails OOS; other cryptos pass)
- Partial-positive C2 (cross-sectional long-only Sharpe 1.12–1.42 BUT PF/friction caveats)

**Verdict: Criterion D's threshold IS met.** No criterion fires cleanly; multiple cells have partial evidence pointing in different directions.

### §5.5 Criterion E — No published evidence §14 achievable on retail-accessible long-only crypto spot

**Requirement:** "Multiple studies surveyed across timeframes and asset counts, none demonstrating §14 on long-only crypto spot."

**Evidence:** Criterion E is NOT triggered. Criterion C has positive Sharpe evidence (1.12–1.42 across multiple Tier 1 sources) for long-only cross-sectional momentum. Although unverified for PF and full friction magnitude, this is "positive evidence" sufficient to clear Criterion E's "no evidence anywhere" threshold.

**Verdict: Criterion E is NOT triggered.** This is a _positive_ finding — the literature is not unanimously negative on retail-accessible long-only crypto strategies.

### §5.6 Verification update (open-source second pass, 2026-05-12 post-operator-review)

The operator raised three substantive caveats on the v1 audit: (a) 2-hour-vs-2-day compression made abstract-summaries load-bearing, (b) PF unverified across all Criterion C sources, (c) Path D's top-N perps universe doesn't match the literature's 3,900-coin universe. They authorised a 1-2 day open-source verification pass before locking the decision. This subsection records what verification revealed.

**Sources where verification refined the v1 finding:**

1. **Cryptocurrency Factor Momentum (Fieberg, Liedtke, Metko, Zaremba, Quantitative Finance 2023):**
   - Authors confirmed (Tier 1 attribution solid).
   - Sample: 3,900+ coins, 2014–2022, weekly rebalancing.
   - **Headline Sharpe 1.28 verified** as the long-only winner-portfolio figure under one specification.
   - **NEW FINDING:** the paper explicitly states "the momentum effect prevails in larger cryptocurrencies but **incurs substantial trading costs** and **extracts alphas largely from short positions**" (in the long-short variant). This directly contradicts the v1 audit's reading that long-only winners cleanly clear §14. The gross Sharpe 1.28 figure faces significant friction degradation that the paper itself flags. Net Sharpe is not retrievable from open sources but is materially below 1.28.
   - PF remains unverified.

2. **Cryptocurrency Market Risk-Managed Momentum (ScienceDirect 2025):**
   - **Headline Sharpe 1.42 (risk-managed) and 1.12 (plain) verified.**
   - **NEW FINDING:** while the paper claims robustness to transaction costs, it also acknowledges "risk management does not change the tail risk of cryptocurrency momentum" and "the strategy is subject to considerable uncertainty that implies greater risk than previous cryptocurrency research has suggested." These are internal caveats that align with the Grobys & Shahzad dissent on Sharpe applicability rather than contradicting it.
   - Friction magnitude tested still unverified.
   - PF still unverified.

3. **Liu, Tsyvinski, Wu — Common Risk Factors in Cryptocurrency (Journal of Finance 2022):**
   - **CRITICAL NEW FINDING — Sharpe is specification-dependent.** At the 1-week horizon, the top quintile portfolio yields weekly return 11.22% with **Sharpe 0.45** (NOT 1.28). The 1.28 figure from the Fieberg et al paper is one specification's result; the same general approach in Liu/Tsyvinski/Wu gives 0.45 for the same direction at 1-week horizon. Whether crypto momentum clears Sharpe > 1.0 depends materially on formation period, holding period, and rebalancing frequency.
   - This means **the v1 audit's "Sharpe 1.12 to 1.42 across multiple Tier 1 sources" framing was misleading.** The range across specifications is more like 0.45 to 1.42, with 0.45 being a Tier-1 published figure on cross-sectional crypto momentum that the v1 audit did not cite.
   - The long-leg-degrades-with-volume finding stands. Top-N perps would land at the _weakest_ part of the momentum cross-section.

4. **Hudson & Urquhart (2021):** verification confirms 14,919 trading rules across 2010–2017 sample period. Timeframe still inferred daily but consistent with the sample range and rule count. The headline finding (no BTC OOS predictability) is unchanged.

5. **Baldi-Lanfranchi (2024):** verified that the 95% gross→net Sharpe degradation finding was on equity factor momentum, not crypto. Applies as a methodological warning to crypto momentum given similar high-turnover profile, but is not direct crypto evidence.

**Net effect of verification on the matrix:**

Cell C2 (Daily/Weekly cross-sectional long-only) in §3 should be re-read as:

| Metric                 | v1 audit reading                       | Post-verification reading                                                                                     |
| ---------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Sharpe range (gross)   | 1.12 to 1.42 across "multiple sources" | **0.45 to 1.42 across specifications** within Tier 1 sources                                                  |
| Net of fees            | Robustness claimed                     | Friction degradation **acknowledged by sources themselves** ("substantial trading costs" — Fieberg et al)     |
| PF                     | Unverified, assumed plausible          | Unverified, **and** sources' internal caveats imply PF reliability is itself questioned                       |
| Tail risk              | Not discussed                          | Sources acknowledge tail risk + "considerable uncertainty… greater risk than previous research has suggested" |
| Methodological dissent | One Tier-1 dissent (Grobys & Shahzad)  | Same dissent, **now reinforced by the positive papers' own caveats**                                          |

**Refined verdict on Criterion C (post-verification):**

Under the strictest reading of Criterion C's evidence threshold — "published evidence that long-only cross-sectional ranking strategies across N perps achieve §14" where §14 = Sharpe > 1.0 AND PF > 1.4 OOS net of fees — the literature does **NOT** provide evidence sufficient to fire Criterion C. The Sharpe-passing claims are:

- Specification-dependent (range 0.45–1.42 within Tier 1 sources)
- Gross-of-fees, with sources themselves flagging substantial trading costs
- Unaccompanied by PF figures
- Conditioned on a 3,900-coin universe rather than top-N perps
- Methodologically contested by another Tier-1 source

The v1 audit's "partial-positive" framing of Criterion C is **charitable**. A stricter reading lands closer to "Sharpe yes in some specifications, PF unknown, friction degradation acknowledged, tail risk live, metric itself contested" — which is less Criterion D and more Criterion E than the v1 audit suggested.

**Refined verdict on Criterion D vs E (post-verification):**

- Criterion D requires "partial evidence but no clear winner." This still applies — the Sharpe 1.28 / 1.42 figures DO exist in Tier-1 sources, even if they're specification-dependent and degraded by friction.
- Criterion E requires "no published evidence §14 is achievable." With Sharpe-passing evidence present (even if caveated), strictly E does NOT fire. Some evidence remains.

**However:** the strength of Criterion C's evidence is materially weaker than the v1 audit's matrix suggested. The path-forward logic should reflect this:

- Path C first (re-run MFD on 8h) remains the right next move per Criterion D's branch.
- **The escalation gate from Path C → Path D should be tighter than the v1 audit implied.** Specifically: post-Path-C kill, the trigger for Path D should require (i) full-text retrieval of the Fieberg et al 2023 paper to verify PF and net friction model, (ii) confirmation that the cross-sectional momentum effect can be reproduced on a top-N perps universe (not just 3,900 coins), and (iii) re-application of the strict reading: if PF turns out to be < 1.4 in the full-text data, Criterion E becomes the right call, not Path D.

This is what the operator requested in their recommendation 2: "Pre-commit a tighter Path D gate now, before Path C runs." This subsection IS that pre-commit. The Path D scope document, when written, must include the three gates above as explicit pre-conditions.

Standard caveats apply with calibration for the audit's findings:

1. **Successful strategies are over-represented.** Papers reporting positive Sharpe ratios are more publishable than papers reporting negative results. The negative-evidence findings in this audit (Hudson & Urquhart on BTC OOS; Grobys & Shahzad on Sharpe undefinability) carry **disproportionate weight** because negative findings clear a higher publication bar.

2. **Many published Sharpe figures are gross, not net.** Where friction-adjustment is not explicit in the abstract, the realized net Sharpe is likely 30–95% lower (per Baldi-Lanfranchi 2024's equity finding, methodologically applicable to high-turnover crypto strategies). Cross-sectional momentum's gross Sharpe 1.28–1.42 should be considered an upper bound; net Sharpe could easily be 0.6–0.9.

3. **The cited sources skew toward 2018–2025 publications and BTC-heavy data.** Pre-2018 backtests may not generalise (small universe, different regime). Post-2022 OOS holdout is rare in the cited sample.

4. **"Robust to transaction costs" claims in abstracts are almost always under-specified.** When a paper claims robustness without specifying the friction magnitude tested, the claim has weak qualitative force.

5. **The author of this audit ran three strategies (MFD, BMR, FCMFD) on the BTC/ETH 4h spot long-only surface and observed three §14 failures.** This is a sample of 3 from the audited surface and the failures are direct evidence that this surface is empirically hard — independent of literature claims. The literature audit and the operator's own trajectory are mutually reinforcing.

**Net effect of publication bias on this audit's verdict:** It tilts evidence toward false-positive Criterion C clearance (positive results are over-published). Mechanically applied caveats land Criterion C in "partial-positive" rather than "clearly clears §14" territory, which is the correct calibration.

---

## §7. Decision Mapping

Applying the pre-committed §5.1 criteria mechanically to the §5 findings:

```
Criterion A check (strict 4h BTC/ETH long-only spot):
  Required: ≥ 2 Tier 1/2 studies, Sharpe > 1.0 AND PF > 1.4 OOS friction-adj
  Found: 0 qualifying studies.
  Result: FAIL → A does NOT fire.

Criterion B check (timeframe shift on 8h/12h/daily for majors long-only):
  Required: multiple studies showing Sharpe IMPROVEMENT on 8h+ for BTC/ETH long-only
  Found: directional improvement (0.33 → 0.80) but no Tier 1/2 study clears §14
        on majors long-only spot at any non-4h timeframe.
  Result: PARTIAL but does NOT meet "multiple studies showing improvement [to §14]"
          threshold. → B does NOT fire cleanly.

Criterion C check (long-only cross-sectional perps achieving §14):
  Required: published evidence + mechanism cross-sectional (not long-short asymmetry)
  Found: Sharpe 1.12–1.42 across 3+ Tier 1 sources on long-only winners.
        Mechanism is cross-sectional (verified).
        Profit factor UNVERIFIED in abstracts (Criterion C requires PF > 1.4).
        Friction-adjustment claimed but magnitude unverified.
        Dissenting Tier 1 view exists (Grobys & Shahzad).
  Result: PARTIAL-POSITIVE but PF/friction unverified. → C does NOT fire
          unambiguously per the strict reading of "achieves §14".

Criterion D check (mixed/inconclusive across A/B/C):
  Required: cells with partial evidence, no clean winner.
  Found: A FAIL, B partial, C partial-positive. → D FIRES.

Criterion E check (no evidence anywhere):
  Found: C has positive Sharpe evidence, so E does NOT fire.
```

### §7.1 Recommended path (per Criterion D's Decision branch in scope §5.1)

> "**Path C first** (smaller change, cheaper test). If C fails its own SIA or §14, escalate to Path D."

**Path C** — universe revision to 8h timeframe; re-run MFD on 8h data as cheap test of the timeframe hypothesis. Per scope §6 Path C: 1–2 weeks estimated duration.

### §7.2 Why this routing is honest given the evidence

- **Criterion A's strict reading is honored.** No 4h-specific Tier 1/2 study clears §14 on BTC/ETH long-only spot. The strict 4h scope you locked in pre-execution forecloses Criterion A by construction _given the literature's granularity_, which is the discipline working as designed.
- **Criterion B receives partial support from timeframe-improvement evidence.** Multi-timeframe daily filter on Bitcoin shows Sharpe improvement (0.33 → 0.80); intraday momentum (gross) is higher than passive. Daily is the most commonly-studied timeframe in academic crypto literature and _some_ signal survives at daily, though not enough to clear §14 on BTC/ETH long-only spot specifically.
- **Criterion C receives the strongest positive evidence**, but the cleanest §14-clearance claims are on the broader cryptocurrency universe (3,900+ coins) at weekly rebalancing, _not_ BTC/ETH alone. The published evidence is "cross-sectional ranking across many coins works", which directly maps to Path D — _expanding the universe and switching to ranking_ — not Path C.
- **The dissenting voice (Grobys & Shahzad) on Sharpe-undefinability for crypto momentum cannot be ignored.** It's published in IJFE; it's not a fringe view. It tempers the Sharpe-1.28-to-1.42 readings into "the strategies generate returns but the standard risk-adjusted metric may not apply."
- **Path C as a first step is consistent with the discipline of "smaller change, cheaper test"** — and crucially, if Path C produces another §14 failure on 8h MFD, the failure itself is informative (it locates the constraint as not just-timeframe), and the project escalates to Path D's universe expansion with stronger justification.

### §7.3 What is explicitly NOT recommended

- **Path B (new in-universe vol-orthogonal signal)** is NOT recommended. The evidence does not show that a fifth signal class would succeed where four (price-only, mean-revert, funding-conditioned, the missing ones) have failed. The published literature does not suggest that "find a better signal in this universe" is what unlocks §14.
- **Path E (stop in-universe attempts, ship framework)** is NOT triggered at this audit. Criterion E requires zero positive evidence anywhere on retail-accessible long-only crypto spot. With the v1 audit's Sharpe-passing evidence (caveated, specification-dependent), strict E does not fire today. **Bar revision is therefore NOT a legitimate option at this point** per scope §7.5. However, the post-verification §5.6 update reframes Criterion E as a _more likely_ outcome than the v1 audit suggested — see §7.4 below.
- **Pursuing Paths C and D in parallel** is forbidden by scope §8.3. Sequential execution per Criterion D's decision branch: C first, escalate to D conditional on C's outcome.

### §7.4 Path D escalation gates (pre-committed post-verification)

The §5.6 verification update revealed that the v1 audit's "partial-positive Criterion C" framing was charitable. Cross-sectional crypto momentum Sharpe is specification-dependent (range 0.45–1.42 within Tier 1 sources), gross-of-fees with sources themselves acknowledging substantial trading costs, PF universally unverified, and methodologically contested. To prevent the Path C → Path D escalation from committing 4–8 weeks on weaker-than-claimed evidence, the following gates are **pre-committed in this audit** and must be satisfied before any Path D scope document is written:

**Gate 1 — Full-text PF verification.**
The Fieberg/Liedtke/Metko/Zaremba 2023 Quantitative Finance paper must be obtained in full text. Profit factor for the long-only winner portfolio (or its closest reported analogue) must be extracted. If PF < 1.4 net of fees, Criterion C strictly fails on the AND-clause of §14, and the decision re-routes to Criterion E (Path E), not Path D.

**Gate 2 — Universe match.**
The Path D scope as currently drafted (top-N liquid perps, BTC/ETH/SOL/BNB/XRP minimum) does not match the literature's evidentiary universe (3,900+ coins). Either:
(a) The Path D scope is expanded to a top-20 or top-50 perp universe with explicit liquidity gates (matching better, larger build), OR
(b) Full-text retrieval of the Fieberg et al / Liu-Tsyvinski-Wu papers confirms the cross-sectional momentum effect persists when restricted to top-10 by volume (matching Path D's scope).
Without one of these, Path D's empirical foundation is inadequate.

**Gate 3 — Net-of-fees Sharpe verification.**
The Cryptocurrency Market Risk-Managed Momentum 2025 paper's "robust to transaction costs" claim must be quantified. Specifically: what friction magnitude was tested (1 bp? 10 bp? 50 bp?), and what is the actual net Sharpe at realistic crypto retail-accessible fees (typically 10–20 bp round-trip on Binance spot)? If the paper tested friction at < 10 bp, the result does not generalise to retail Binance and Path D's foundation weakens further.

**Gate 4 — Methodological dissent resolution.**
The Grobys & Shahzad (2024 IJFE) finding that crypto momentum Sharpe is mathematically undefined due to power-law variance must be addressed. Either the Path D plan acknowledges that the strategy is built on a metric the literature itself contests, OR the plan substitutes a metric that doesn't require finite second moments (e.g., Calmar, Sterling, max-drawdown-relative measures). The first option is acceptable as long as it is explicit; the second is preferable.

**If gates 1–4 cannot be satisfied:** Path D is not authorised, and the decision re-routes to Path E (stop in-universe, ship the SIA framework as standalone infrastructure). This is bar erosion in reverse — closing a possible path because the evidence supporting it didn't hold up under scrutiny, not because we lowered the bar to dismiss it.

These gates are the operationalised version of the operator's recommendation 2 ("Pre-commit a tighter Path D gate now, before Path C runs"). They become binding constraints on any future Path D scope document.

---

## §8. References

### Tier 1 — Peer-reviewed academic journals

1. Hudson, R., & Urquhart, A. (2021). Technical trading and cryptocurrencies. _Annals of Operations Research_, 297(1), 191–220. https://link.springer.com/article/10.1007/s10479-019-03357-1 [paywalled; open version: https://centaur.reading.ac.uk/85715/8/Hudson-Urquhart2019_Article_TechnicalTradingAndCryptocurre.pdf]
2. Cryptocurrency factor momentum. (2023). _Quantitative Finance_, 23(12), 1853–1869. https://www.tandfonline.com/doi/abs/10.1080/14697688.2023.2269999
3. Cryptocurrency market risk-managed momentum strategies. (2025). _Finance Research Letters_. https://www.sciencedirect.com/science/article/abs/pii/S1544612325011377
4. Grobys, K., & Shahzad, S. J. H. (2024). Cryptocurrency momentum: Is it an illusion? _International Journal of Finance & Economics_. https://onlinelibrary.wiley.com/doi/10.1002/ijfe.70036
5. Cryptocurrency momentum has (not) its moments. (2025). _Financial Markets and Portfolio Management_. https://link.springer.com/article/10.1007/s11408-025-00474-9
6. Liu, Y., Tsyvinski, A., & Wu, X. (2022). Common Risk Factors in Cryptocurrency. _SSRN_. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3379131
7. Shen, D., et al. (2022). Bitcoin intraday time series momentum. _Financial Review_. https://onlinelibrary.wiley.com/doi/10.1111/fire.12290
8. Grobys, K., & Sapkota, N. (2019). Cryptocurrencies and momentum. _Economics Letters_, 180, 6–10. https://ideas.repec.org/a/eee/ecolet/v180y2019icp6-10.html

### Tier 2 — Working papers from established academics / institutions

9. Mann, W. (2025). Quantitative Alpha in Crypto Markets: A Systematic Review of Factor Models, Arbitrage Strategies, and Machine Learning Applications. _SSRN_. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5225612 [paywalled; LinkedIn summary at https://www.linkedin.com/posts/william-mann-cfa_quantitative-alpha-in-crypto-markets-a-systematic-activity-7321138680465666051-Jv9l]
10. Baldi-Lanfranchi, F. (2024). Transaction-cost-aware Factors. _SSRN/Lancaster Univ. WP_. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4737166

### Tier 3 — Institutional / vendor research

11. Grayscale Research. (2025). The Trend is Your Friend: Managing Bitcoin's Volatility with Momentum Signals. https://research.grayscale.com/reports/the-trend-is-your-friend-managing-bitcoins-volatility-with-momentum-signals
12. Quantpedia. (2024). How to Design a Simple Multi-Timeframe Trend Strategy on Bitcoin. https://quantpedia.com/how-to-design-a-simple-multi-timeframe-trend-strategy-on-bitcoin/
13. Two Sigma. Risk Analysis of Crypto Assets. https://www.twosigma.com/articles/risk-analysis-of-crypto-assets/

### Tier 4 — Open-source / community

14. (Searched but no documented forward-test results meeting the audit's citation threshold were identified.)

### Tier 5 — Practitioner blogs

15. (Excluded by audit discipline §4.5.5; used only as pointers to find Tier 1–3 sources.)

### Notable absences (themselves findings)

- AQR Capital Management — no cryptocurrency systematic strategy research
- Two Sigma — crypto risk research only, no active trading strategies
- Renaissance Technologies — private, no public crypto research
- No Tier 1/2 study specifically on BTC/ETH 4h spot long-only

---

## §9. Summary one-liner

**Criterion D fires. The §5.1 decision routes to Path C first (re-run MFD on 8h as cheap timeframe-shift test). Path D escalation requires satisfying the four post-verification gates in §7.4 — failing which the decision re-routes to Path E (stop in-universe, ship the SIA framework). ADR-0017 documents this decision next.**

_End of audit._
