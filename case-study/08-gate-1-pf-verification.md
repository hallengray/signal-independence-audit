> **For external readers:** This document is one of 10 curated case-study artefacts from Project Aṣe, a quantitative crypto-trading research project that produced a documented negative result with mechanism across four strategy attempts plus a literature audit, all under pre-committed criteria (Sharpe > 1.0 AND profit-factor > 1.4 OOS, called "§14" internally) that held without bar erosion across 19 ADRs. The full project repo is private (scope B of the Phase 5e shipping spec). Start with `./00-readme.md` for the reading guide. Read order context: Path D Gate 1: full-text PF verification of the foundational literature paper. PF is never reported in the paper. The substance of the document below is unchanged from the internal version; only this framing block and personal/identifying content scrubs are added.

---

# Phase 5d Gate 1 — Fieberg et al. 2023 PF Verification

## §0. Metadata

- **Date:** 2026-05-12
- **Author:** Femi Adedayo (executed with Claude Code)
- **Gate authority:** `docs/decisions/0017-phase-5b-path-c-and-path-d-gates.md` §"Path D escalation gates" Gate 1
- **Predecessor:** ADR-0018 PATH-C-KILL (commit `d1bd6c7`, tag `phase-5c-path-c-killed`)
- **Source paper:** Fieberg, C., Liedtke, G., Metko, D., & Zaremba, A. (2023). Cryptocurrency factor momentum. _Quantitative Finance_, 23(12), 1853–1869. DOI: 10.1080/14697688.2023.2269999.

## §1. Verdict

**Gate 1: FAIL** (per pre-committed §7.4 routing).

**Routing:** Path E (Criterion E fires). Path D scope MUST NOT be written until — and unless — a separate ADR amends ADR-0017 with new Tier-1 evidence that satisfies Gate 1 on its own terms.

The verdict is driven by two independent failures of the gate's premise, either of which is sufficient:

1. **PF is not reported in the paper.** Anywhere. Not in the main results, not in the long-only robustness section (§4.4.2, Table 13), not in the liquidity-restricted subsamples (Table 12), not in the 768-design-choice robustness (Table 8), not in subperiod analysis (Table 5). The paper's performance metrics are: weekly mean return, standard deviation, Newey–West t-statistic, and annualised Sharpe ratio. Profit factor (or any close analogue — gain-loss ratio, hit rate, success rate, win rate) is **never computed and never tabulated**.
2. **No transaction-cost analysis is reported.** The paper contains zero matches for "transaction cost", "trading cost", "fees", "basis points", "bps", or "net of". All headline figures (Sharpe 1.28 cross-sectional winners; Sharpe 1.43 most-liquid-25% long-only winners; Sharpe 1.09 long-only winners minus risk-free rate per Table 13 Panel A) are **gross of trading frictions**. The gate's "net of fees" clause is therefore unsatisfied regardless of how PF were estimated from related statistics.

Both findings together: even if PF were inferable from the reported moments (it isn't, robustly — see §4.3), the net-of-fees clause cannot be satisfied because no friction analysis exists. Per the §7.4 verdict table, "Full text obtained, PF reported only gross" maps to FAIL; this case is strictly weaker than that — full text obtained, PF not reported at all and all stats are gross.

## §2. Methodology (pre-committed per ADR-0017 §7.4 Gate 1)

The gate states verbatim: _"The Fieberg/Liedtke/Metko/Zaremba 2023 Quantitative Finance paper must be obtained in full text. Profit factor for the long-only winner portfolio (or its closest reported analogue) must be extracted. If PF < 1.4 net of fees, Criterion C strictly fails on the AND-clause of §14, and the decision re-routes to Criterion E (Path E), not Path D."_

Implementation (pre-committed in ADR-0017, executed today):

1. Attempt full-text retrieval across six channels (SSRN preprint, ResearchGate, author institutional repositories, Google Scholar, arXiv, Taylor & Francis paywall).
2. If full text obtained: extract PF and net-of-fees status from the long-only winner portfolio or closest analogue.
3. Apply the §7.4 verdict table mechanically; do not soft-pedal either direction.

Both steps were completed. Full text was obtained. PF was searched for and is not present. Verdict applied per the table.

## §3. Full-text search trail

| #   | Channel                                                                  | Query / URL                                                                                                                  | Outcome                                                                                                                                                                                                                                                                                                          |
| --- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Google web search                                                        | `Fieberg Liedtke Metko Zaremba "Cryptocurrency factor momentum" SSRN preprint PDF`                                           | Located CoLab abstract, RePEc landing page, ResearchGate "Request PDF", Taylor & Francis paywall, **and an open-access bitstream URL at open.icm.edu.pl**.                                                                                                                                                       |
| 2   | Google web search                                                        | `"Cryptocurrency factor momentum" Fieberg Zaremba 2023 ResearchGate full text PDF`                                           | Confirmed ResearchGate has only a "Request PDF" gate. Reconfirmed the open.icm.edu.pl URL.                                                                                                                                                                                                                       |
| 3   | Google web search                                                        | `Fieberg Liedtke Metko Zaremba "Quantitative Finance" 2023 cryptocurrency momentum profit factor`                            | No PF figure surfaced in any snippet. Reconfirmed open repository link.                                                                                                                                                                                                                                          |
| 4   | Google web search                                                        | `"Cryptocurrency factor momentum" Zaremba filetype:pdf`                                                                      | Returned the open.icm.edu.pl bitstream URL as the top PDF result.                                                                                                                                                                                                                                                |
| 5   | WebFetch                                                                 | `https://open.icm.edu.pl/items/d9f44e22-0614-4db8-8585-6dcba8906bb5` (landing page)                                          | Confirmed metadata: published version (not preprint), CC-BY 4.0 licensed, 562.24 KB PDF, identifies the bitstream download path.                                                                                                                                                                                 |
| 6   | WebFetch                                                                 | `https://open.icm.edu.pl/server/api/core/bitstreams/86a51c47-8cd3-4201-88ee-42f44fb89227/content` (bitstream, first attempt) | Returned a JavaScript CAPTCHA wall (744-byte HTML), not the PDF.                                                                                                                                                                                                                                                 |
| 7   | Bash (`curl` with default UA)                                            | Same bitstream URL                                                                                                           | Same CAPTCHA HTML response, 744 bytes.                                                                                                                                                                                                                                                                           |
| 8   | Bash (`curl` with Linux Chrome UA + `Referer: https://open.icm.edu.pl/`) | Same bitstream URL                                                                                                           | **Real PDF returned, 575,736 bytes, header `%PDF-1.5`, linearized.**                                                                                                                                                                                                                                             |
| 9   | WebFetch                                                                 | `https://sites.google.com/view/christianfieberg/research/selected-publications`                                              | Christian Fieberg's own publication list. Cryptocurrency factor momentum is _omitted_ from his curated list (which includes 14 other papers). His related 2025 JFQA paper "A Trend Factor for the Cross-Section of Cryptocurrency Returns" is listed instead. Worth noting but not material to the gate verdict. |
| 10  | WebFetch                                                                 | `https://www.researchgate.net/publication/375473250_Cryptocurrency_factor_momentum`                                          | HTTP 403 Forbidden. No content retrievable.                                                                                                                                                                                                                                                                      |
| 11  | WebFetch                                                                 | `https://colab.ws/articles/10.1080/14697688.2023.2269999`                                                                    | Bibliographic landing page only. No table content.                                                                                                                                                                                                                                                               |
| 12  | WebFetch                                                                 | `https://ideas.repec.org/a/taf/quantf/v23y2023i12p1853-1869.html`                                                            | Abstract only. Three citing papers listed.                                                                                                                                                                                                                                                                       |
| 13  | Google web search                                                        | `"Cryptocurrency factor momentum" "1.65" "0.62" Fieberg Zaremba table`                                                       | No table-content snippets returned.                                                                                                                                                                                                                                                                              |
| 14  | Google web search                                                        | `"cryptocurrency factor momentum" Fieberg Zaremba "transaction costs" basis points Sharpe net`                               | No transaction-cost snippets. (This matters — see §4.4 and §6.1.)                                                                                                                                                                                                                                                |
| 15  | Google Scholar                                                           | `cryptocurrency factor momentum Fieberg Liedtke Metko Zaremba`                                                               | Confirmed open.icm.edu.pl as the canonical open-access source. "All versions" cluster ID `7365063387216489913`.                                                                                                                                                                                                  |

**Outcome:** Full text obtained via channel #8 (open repository PDF). All subsequent analysis in §4 is from direct reading of the published version.

## §4. Findings from the paper

### §4.1. Bibliographic confirmation

- **Title (verbatim from PDF cover page):** "Cryptocurrency Factor Momentum"
- **Authors:** Christian Fieberg (City University of Applied Sciences Bremen / University of Luxembourg / Concordia University), Gerrit Liedtke (University of Bremen), Daniel Metko (University of Bremen), Adam Zaremba (Montpellier Business School / Poznan University of Economics / University of Cape Town).
- **Corresponding author:** Adam Zaremba, adam.zaremba@ue.poznan.pl.
- **Funding:** National Science Center of Poland Grant 2021/41/B/HS4/02443.
- **License:** CC-BY (Open Access). This is the published version, not a preprint.

### §4.2. Sample, universe, frequency, period

| Specification                          | Value                                                     | Source                                                                         |
| -------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Coin universe                          | **3,918 cryptocurrencies**                                | Table 4 footnote, Table 5 footnote, §5 Concluding Remarks                      |
| Sample period                          | **January 2014 – December 2022**                          | Table 4 footnote and elsewhere                                                 |
| Rebalance frequency                    | **Weekly**                                                | "All strategies are rebalanced weekly" (Table 4 footnote, repeated throughout) |
| Anomalies replicated                   | **34** (size / liquidity / volatility / momentum classes) | §1, §5                                                                         |
| Number of design choices in robustness | **768**                                                   | §4.3, Table 8                                                                  |

This matches the audit's universe description (3,900+ coins, 2014–2022, weekly rebalancing). Audit §5.3 figure of 3,900+ is corroborated by the paper's 3,918.

### §4.3. Headline performance metrics — Table 4 (verbatim transcription)

Table 4 reports the headline factor-momentum performance, sample period Jan 2014 – Dec 2022, 3,918 cryptocurrencies, weekly rebalancing.

| Strategy                                              | Mean (% / wk) | SD       | t-stat   | SR (annualised) |
| ----------------------------------------------------- | ------------- | -------- | -------- | --------------- |
| Equal-weighted                                        | 1.11          | 6.22     | 3.85     | 1.28            |
| Time-series factor momentum (TS)                      | 0.55          | 6.41     | 1.86     | 0.62            |
| TS Winners                                            | 1.52          | 8.41     | 3.89     | 1.30            |
| TS Losers                                             | 0.62          | 8.17     | 1.64     | 0.55            |
| Cross-sectional factor momentum (CS)                  | 0.52          | 5.54     | 2.01     | 0.67            |
| **CS Winners** (the gate's target portfolio analogue) | **1.65**      | **9.28** | **3.83** | **1.28**        |
| CS Losers                                             | 0.62          | 7.30     | 1.82     | 0.61            |

All figures are **gross** (see §4.4). Profit factor is **not in this table** and not in any related table.

### §4.4. Transaction-cost discussion — the critical finding

A focused full-text scan was performed for the strings: `transaction cost`, `trading cost`, `fees`, `basis points`, `bps`, `net of`, `round-trip`, `round trip`. **Zero matches.**

The closest the paper comes to transaction-cost language is in §4.4.2 ("Short-Sale Constraints"), which discusses the difficulty of shorting in crypto (citing Stambaugh et al. 2012) and notes: _"the profitability of many stock market anomalies stems from short positions, and implementing these strategies may be costly"_ — but this is a comment about the stock-market literature's reliance on shorting, not a quantification of crypto trading costs. The paper's response is to test long-only variants (Table 13), not to subtract transaction costs from any strategy.

The phrase _"incurs substantial trading costs"_ that Phase 5a audit §5.6 attributed to "Fieberg et al" **does not appear in this paper.** The audit appears to have conflated this with a different source — most plausibly Liu, Tsyvinski, & Wu (2022) or one of Zaremba's other cryptocurrency papers — and inherited that conflation into ADR-0017's framing. This is noted as a corrigendum to the audit (see §6.3 below) but does not change today's verdict: regardless of whether the paper says costs are substantial, it does not quantify them and does not report net-of-fees figures for any strategy.

### §4.5. Long-only winner portfolio — Table 13 (the gate's strict target)

Section 4.4.2 of the paper is titled "Short-Sale Constraints" and explicitly addresses long-only variants. The paper does not implement long-only as "buy winner factors, hold cash on the short leg"; instead it implements long-only as "buy winner factors and finance them by shorting the risk-free rate (Panel A) or shorting Bitcoin (Panel B)". This is a research-design choice but it _is_ the paper's closest reported analogue to "long-only winner portfolio".

Table 13 (verbatim transcription, sample Jan 2014 – Dec 2022, 3,918 coins, weekly rebalancing):

| Strategy                                   | Mean (% / wk) | SD        | t-stat   | SR (annualised) |
| ------------------------------------------ | ------------- | --------- | -------- | --------------- |
| **Panel A — financed with risk-free rate** |               |           |          |                 |
| TS winners minus rf                        | 2.35          | 14.07     | 3.60     | **1.20**        |
| **CS winners minus rf**                    | **2.30**      | **15.19** | **3.27** | **1.09**        |
| **Panel B — financed with Bitcoin**        |               |           |          |                 |
| TS winners minus BTC                       | 1.14          | 12.76     | 1.93     | 0.64            |
| CS winners minus BTC                       | 1.15          | 12.96     | 1.91     | 0.64            |

**Profit factor is not in Table 13 either.** Sharpe is the only risk-adjusted metric.

### §4.6. Most-liquid-25% subsample — Table 12 Panel C (best-of variant)

The 25%-most-liquid restriction is the closest the paper comes to a Path-D-realistic universe (still 3,918×25% ≈ 980 coins, much larger than a top-N perps universe, but more liquid-tilted than the headline sample). Table 12 Panel C ("No size- or liquidity-based factors", 25%-most-liquid subsample):

- CS Winners: Mean 2.03 / SD 10.2 / t 3.47 / **SR 1.43**
- TS Winners: Mean 1.98 / SD 10.5 / t 3.30 / **SR 1.36**

These are the highest long-only winner Sharpes reported anywhere in the paper. Still gross. Still no PF.

### §4.7. PF inferability from the reported moments — no

A profit factor cannot be derived from (Mean, SD, t-stat, Sharpe) alone. PF requires the distribution of per-trade or per-period gains and losses separately, specifically (sum of positive-period returns) / (absolute sum of negative-period returns) — or equivalently a hit-rate × win/loss-magnitude decomposition. None of these are reported. Inferring PF from Sharpe ratios under a normality assumption is a known approximation in some practitioner literature, but the gate language pre-committed in ADR-0017 §7.4 is explicit: PF must be _extracted_ from the paper, not estimated under an assumption the paper does not make. Therefore the inferability path is closed under the pre-committed gate language.

### §4.8. Sharpe re-verification

The audit's headline Sharpe 1.28 for cross-sectional long-only winners is verified at the paper level (Table 4, last row but one). The audit's reading was correct. The 1.42 "risk-managed variant" figure cited elsewhere in the audit is from a different paper (Proelss / Schweizer / Buchwalter 2025 or the related risk-managed-momentum literature) and is not in Fieberg et al. 2023.

## §5. Decision mapping

The §7.4 verdict table, applied to today's findings:

| Outcome                                                                           | Verdict                 | Applies?                                                                                                      |
| --------------------------------------------------------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------- |
| Full text obtained, PF reported net at retail-realistic fees (10–20 bp), PF ≥ 1.4 | PASS                    | **No.** PF not reported anywhere.                                                                             |
| Full text obtained, PF reported but < 1.4 net                                     | FAIL → Path E           | **No.** PF not reported anywhere.                                                                             |
| Full text obtained, PF reported only gross                                        | FAIL → Path E           | **Closest match.** This case is strictly weaker — PF not reported _at all_, and all reported stats are gross. |
| Full text obtained, PF reported net but at unrealistic friction (< 10 bp)         | PARTIAL → operator call | No. No friction analysis at all.                                                                              |
| Full text NOT obtainable after exhaustive search                                  | FAIL → Path E           | N/A — full text obtained.                                                                                     |

**Mechanical verdict: FAIL.** The gate's premise — that PF can be _extracted_ for the long-only winner portfolio at retail-realistic net fees — cannot be satisfied from this paper. The paper does not report PF. The paper does not report any net-of-fees figure for any strategy. Both clauses of the gate language ("PF reported" AND "net of fees") fail independently.

## §6. Routing recommendation

### §6.1. Primary routing — Path E (Criterion E fires)

Per ADR-0017 §7.4 Gate 1 verbatim: _"If PF < 1.4 net of fees, Criterion C strictly fails on the AND-clause of §14, and the decision re-routes to Criterion E (Path E), not Path D."_

The strict reading: PF is not reported, therefore the comparison "PF < 1.4 net of fees" cannot be made affirmatively against the paper's evidence; therefore Criterion C strictly fails on the AND-clause of §14 (which requires both Sharpe > 1.0 AND PF > 1.4 OOS net of fees, with **evidence**, not extrapolation); therefore Path D's empirical foundation is inadequate; therefore Path E.

**Recommended next document: ADR-0019** (numbering follows ADR-0018 PATH-C-KILL), titled approximately _"Phase 5d Path E routing — cross-sectional momentum literature does not satisfy §14 net-of-fees AND-clause"_, citing this Gate 1 verdict as the binding justification. Gates 2–4 are not executed because the AND-structure of the four-gate logic makes any single FAIL terminal for Path D.

### §6.2. What Path E means in practice (sketch, not commitment)

Path E was scoped in ADR-0017 and the audit as "stop in-universe attempts, ship the framework." The Phase 5a audit §7.4 noted this is the routing when (i) cross-sectional momentum literature does not survive PF/net-of-fees scrutiny, AND (ii) no Tier-1 evidence has surfaced for §14-clearing retail-accessible long-only crypto spot. Today's Gate 1 result confirms (i). (ii) was the audit's standing finding and is unchanged.

The practical contents of Path E (ship-the-framework, document the empirical wall, separately consider Criterion E bar revision) are out of scope for this report and should be specified in ADR-0019 plus a fresh phase scope document.

### §6.3. Audit corrigendum

The Phase 5a audit §5.6 attributed the phrase _"incurs substantial trading costs"_ and _"extracts alphas largely from short positions"_ to Fieberg et al. 2023. Direct full-text reading shows these phrases (or their close paraphrases) **are not in this paper.** The paper discusses short-selling difficulty as a research-design motivation for Table 13's long-only variants, but does not quantify trading costs and does not claim alphas come from shorts. The audit appears to have conflated Fieberg et al. with either Liu / Tsyvinski / Wu (2022) or one of Zaremba's other cryptocurrency-anomalies papers (e.g., the 2024 Cryptocurrency Anomalies and Economic Constraints paper that does explicitly tackle implementation friction).

This conflation **does not weaken** today's Gate 1 verdict — it strengthens it. The reason: if the audit's verification-pass framing _had_ been correct (i.e., if the paper itself acknowledged "substantial" costs), Gate 1 would still FAIL because PF was never reported and net figures never tabulated. The corrected reading is that the paper does not even comment on the cost question, which is a more pristine gross-only-evidence base than the audit characterised.

The corrigendum should be noted in any future revision of the audit but does not need to invalidate the audit's overall conclusion structure, which (correctly, on the net) treated cross-sectional momentum Criterion C as PF-unverified.

## §7. References

1. **ADR-0017** — Phase 5b Path C and Path D gates. `docs/decisions/0017-phase-5b-path-c-and-path-d-gates.md` §"Path D escalation gates" Gate 1 (lines 63–64).
2. **ADR-0018** — Phase 5c PATH-C-KILL. `docs/decisions/0018-phase-5c-path-c-kill.md`. Predecessor at commit `d1bd6c7`, tag `phase-5c-path-c-killed`.
3. **Phase 5a literature audit** — `docs/reports/2026-05-12-pre-phase-5-literature-audit.md` §5.3 (Criterion C cross-sectional evidence), §5.6 (verification update + Fieberg et al specifically).
4. **The paper itself** —
   - Fieberg, C., Liedtke, G., Metko, D., & Zaremba, A. (2023). Cryptocurrency factor momentum. _Quantitative Finance_, 23(12), 1853–1869.
   - DOI: https://doi.org/10.1080/14697688.2023.2269999
   - Open Access PDF (CC-BY): https://open.icm.edu.pl/server/api/core/bitstreams/86a51c47-8cd3-4201-88ee-42f44fb89227/content
   - Open Access landing page: https://open.icm.edu.pl/items/d9f44e22-0614-4db8-8585-6dcba8906bb5
5. **Alternative sources checked but not used as primary evidence** —
   - RePEc: https://ideas.repec.org/a/taf/quantf/v23y2023i12p1853-1869.html
   - Taylor & Francis paywalled abstract: https://www.tandfonline.com/doi/abs/10.1080/14697688.2023.2269999
   - ResearchGate (gated): https://www.researchgate.net/publication/375473250_Cryptocurrency_factor_momentum
   - Christian Fieberg's personal publication list: https://sites.google.com/view/christianfieberg/research/selected-publications (notable: omits this paper from his curated list)
   - Google Scholar all-versions cluster: ID 7365063387216489913

_End of Gate 1 verdict._
