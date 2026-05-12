> **For external readers:** This document is one of 10 curated case-study artefacts from Project Aṣe. Start with `./00-readme.md` for the reading guide. Read order context: this is the standalone teaching artefact about the AI-assisted literature research failure mode exposed during Project Aṣe's Phase 5d Gate 1. Original document context: this is a NEW document for the case study (not a direct copy of an internal ADR or report); it distils the corrigendum content from ADR-0019 §"Phase 5a audit corrigendum" + the Phase 5d Gate 1 verification report into a self-contained teaching artefact retrievable on its own.

---

# Audit corrigendum — paywall reliance + abstract summarisation = attribution errors

## What happened

During Project Aṣe's Phase 5a literature audit (a 2-day survey of published cryptocurrency-trading research aimed at answering "is the §14 bar empirically achievable on this surface?"), one of the Tier-1 sources cited was:

> Fieberg, C., Liedtke, G., Metko, D., & Zaremba, A. (2023). Cryptocurrency factor momentum. _Quantitative Finance_, 23(12).

The audit, working under time pressure and paywall constraints, summarised the paper at the abstract level. In doing so, it attributed two specific claims to the paper:

> "incurs substantial trading costs"

> "extracts alphas largely from short positions"

These claims appeared in the audit's §5.6 verification update as caveats on the paper's headline Sharpe figures, framing them as evidence that the paper itself flagged friction degradation.

**Neither of those phrases — nor their substantive content — appears anywhere in the paper.**

## How it was caught

The audit's findings flowed downstream into ADR-0017's Path D escalation gates. Specifically, Gate 1 required full-text retrieval of the Fieberg et al paper to verify its profit-factor numbers. The gate was pre-committed in ADR-0017 before this specific error was known to exist — its purpose was to prevent the project from building 4-8 weeks of Path D infrastructure on top of unverified literature claims.

When Phase 5d executed Gate 1, the full text was retrieved (via the CC-BY 4.0 published version on `open.icm.edu.pl`, after a header-tweaked HTTP request bypassed the JavaScript CAPTCHA — recorded for reproducibility in the Gate 1 verification report).

The full text revealed:

- **Profit factor is never reported anywhere in the paper.** Zero matches across all tables and sections. Only Mean (% per week), SD, Newey-West t-stat, and annualised Sharpe.
- **No transaction-cost analysis exists.** Zero matches for "transaction cost", "trading cost", "fees", "basis points", "bps", "net of". All performance figures are gross.
- The phrases "incurs substantial trading costs" and "extracts alphas largely from short positions" simply aren't in the paper.

The attribution error was caught by construction: the pre-committed gate required full-text verification, and full-text verification surfaced the misattribution.

## The likely true source of the attributed claims

The phrases the audit attributed to Fieberg et al most likely came from:

- **Liu, Tsyvinski, & Wu (2022).** _Common Risk Factors in Cryptocurrency_. This paper does discuss volume-dependent momentum decay and short-leg-driven returns at the cross-section level.
- **Other Zaremba papers.** Adam Zaremba (one of the Fieberg et al co-authors) has published multiple cross-sectional crypto papers; phrasing about trading-cost robustness appears in some of them but not in the specific Fieberg/Liedtke/Metko/Zaremba 2023 paper that was being cited.

The audit's compressed-time retrieval almost certainly co-mingled snippets across these sources, attributing to one paper what another said.

## The systemic lesson

The failure mode is: **paywall reliance + abstract-only summarisation produces attribution errors that survive review.**

- The paywall prevents full-text verification at audit time.
- Search-result snippets and abstracts get summarised into the audit's narrative.
- The narrative looks coherent; nothing in the audit's own evidence chain catches the misattribution.
- The error propagates to downstream artefacts (in this project's case, the audit's §5.6 update + ADR-0017's framing of Criterion C's evidence weight).
- Only forcing full-text retrieval — for any load-bearing claim — catches it.

The defence is: **for any load-bearing claim, require full-text verification before that claim drives a decision.** Codify this as a pre-committed gate, not as a soft norm.

In Project Aṣe's case, this defence was already in place — ADR-0017's Gate 1 was written into the Path D escalation pipeline specifically to require full-text PF verification before Path D scope was authorised. The pre-committed gate was put there for general epistemic-hygiene reasons (literature claims should be verified before they fund infrastructure builds), not because this specific error was anticipated. The gate caught the error by construction.

This is also a comment on AI-assisted research workflows specifically. The audit was executed with LLM assistance in the search + summarisation loop; the LLM did what LLMs do — produce fluent summaries that integrate sources without preserving the granular "this phrase came from THIS source" attribution. Without an explicit "verify the load-bearing phrase against the full text" gate, the failure mode is hard to catch.

## What changes downstream

The corrigendum **strengthens** the Path E routing decision, not weakens it. The original audit reading was:

> Fieberg et al claims Sharpe 1.28 but acknowledges substantial trading costs and short-side alpha capture.

The corrected reading is:

> Fieberg et al claims gross Sharpe 1.28 (with 1.09 long-only, 1.43 most-liquid-25%-best-variant) but **doesn't address trading costs at all** and **doesn't report profit factor.**

The corrected reading makes the paper an even thinner foundation for the original Path D scope. The literature's PF claim — the AND-clause of §14 — was never verified because the literature never reported it.

## References

- ADR-0019 §"Phase 5a audit corrigendum" (the routing ADR that promotes this corrigendum to a primary finding).
- `./08-gate-1-pf-verification.md` (the Gate 1 verdict report; full retrieval trail + extracted figures).
- The Fieberg et al paper itself: https://www.tandfonline.com/doi/abs/10.1080/14697688.2023.2269999 (paywall) + https://open.icm.edu.pl/ for the OA copy.

_End of audit corrigendum._
