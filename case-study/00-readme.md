# Case Study Reading Guide

This directory contains 11 curated artefacts from Project Aṣe, a quantitative crypto-trading research project that produced a documented negative result with mechanism across four strategy attempts plus a literature audit, all under pre-committed criteria (Sharpe > 1.0 AND profit factor > 1.4). The 11th document is an epilogue: after the decision to stop (Path E), the project ran one owned, pre-committed exception (the Markov-Switched Strategy) under a deliberately revised bar that lowered the Sharpe pass mark to 0.85. It failed too. The narrative writeup of that epilogue is at `../MSS_POST.md`.

The full project repo is private; this curated subset is the evidence chain for the blog post at `../BLOG_POST.md`.

Each document carries a "for external readers" framing block at the top. The 10th document (`10-audit-corrigendum.md`) is the only one written specifically for this case study — the other 9 are lightly-reframed copies of internal ADRs and reports.

## Reading paths

Three suggested orders depending on what you're after.

### A. Chronological (the full trajectory)

Read in numbered order. Mirrors how the project unfolded over time.

1. `01-mfd-kill-adr-0011.md` — Phase 2: trend-following at 4h. §14 FAIL, Sharpe-bound.
2. `02-bmr-kill-adr-0013.md` — Phase 3: mean reversion at 4h. §14 FAIL, Sharpe AND PF bound.
3. `03-sia-framework-adr-0014.md` — The SIA methodology that emerged from the first two kills. Pre-hyperopt screening framework.
4. `04-fcmfd-sia-kill-adr-0015.md` — Phase 4: funding-conditioned MFD. **SIA-killed in ~3 seconds before any hyperopt compute ran.** The strongest worked example of SIA's value.
5. `05-literature-audit.md` — 2-day literature audit asking "is §14 empirically achievable on this surface at all?" Produces Criterion D (mixed evidence).
6. `06-phase-5b-decision-adr-0017.md` — Decision ADR locking Path C (cheap timeframe test) first + the four Path D escalation gates pre-committed.
7. `07-path-c-kill-adr-0018.md` — Phase 5c: 8h MFD diagnostic test. 0/4 windows clear §14. Timeframe shift was not directionally helpful per-window.
8. `08-gate-1-pf-verification.md` — Phase 5d Gate 1: full-text retrieval of the foundational literature paper. PF is never reported in the paper.
9. `09-path-e-routing-adr-0019.md` — Routing decision ADR. Path E (stop in-universe, ship the framework) is selected.
10. `10-audit-corrigendum.md` — The standalone teaching artefact about the AI-assisted literature research failure mode the Gate 1 verification exposed.
11. `11-mss-kill-adr-0027.md` (epilogue): the Markov-Switched Strategy. The one owned exception taken after Path E, under a revised bar (Sharpe pass mark lowered to 0.85). It combined the failed trend and mean-reversion strategies via a regime detector, passed the SIA pre-screen for the first time in the project, then failed out-of-sample anyway (0 of 5 candidates, negative Sharpe). Narrative version: `../MSS_POST.md`.

### B. SIA-methodology focused (you want the tool, not the project history)

Read these in order; skip the rest.

1. `03-sia-framework-adr-0014.md` — The SIA methodology spec. Four screens, design rationale.
2. `04-fcmfd-sia-kill-adr-0015.md` — The strongest worked example. SIA evidence JSON, per-tercile tables, inversion-clause test, verdict routing.
3. `09-path-e-routing-adr-0019.md` §"What we keep — framework artefacts catalogue" — the SIA harness's place among the other reusable infrastructure Project Aṣe produced.

Then go straight to the `../sia/` directory in this repo to see the harness implementation, and `../examples/fcmfd_replay.ipynb` for a runnable demo on synthetic data.

### C. Negative-result-focused (you want the honest disconfirmation story)

Read in this order. Skips the SIA methodology details until the end.

1. `01-mfd-kill-adr-0011.md` — Phase 2 kill.
2. `02-bmr-kill-adr-0013.md` — Phase 3 kill (different failure mode).
3. `05-literature-audit.md` — The literature audit + its findings.
4. `07-path-c-kill-adr-0018.md` — Phase 5c kill (timeframe shift refuted).
5. `08-gate-1-pf-verification.md` + `10-audit-corrigendum.md` — The Path D Gate 1 verdict + the corrigendum (the cleanest teaching artefact).
6. `09-path-e-routing-adr-0019.md` — How Path E was framed and why it's not "project failure."

`04-fcmfd-sia-kill-adr-0015.md` and `03-sia-framework-adr-0014.md` are also worth reading at the end, in either order — they're the methodology that emerged from the failures.

## Reading the negative result honestly

The blog post at `../BLOG_POST.md` argues that **Path E (stop in-universe, ship the framework) is not project failure** — it's a documented disconfirmation of the in-universe hypothesis with mechanism, on a surface where the literature itself does not have positive evidence for retail-realistic strategies meeting the criteria.

The §14 bar (Sharpe > 1.0 AND PF > 1.4) held throughout 19 ADRs. The bar transitions from "contested-theoretical" to "documented-empirical." If anyone wants to deploy capital on BTC/USDT + ETH/USDT 4h spot long-only in the future, this case-study directory is the receipt: this surface doesn't support §14-clearing strategies per documented evidence across 4 attempts + literature audit + Path D Gate 1 verification.

That framing is the bigger picture this case study is meant to support.

## A note on what's NOT in this case study

The strategy implementation code, hyperopt outputs, raw backtest data, ops playbooks, and deployment infrastructure are NOT included. Scope was locked at "SIA harness + curated case-study evidence" in the Phase 5e shipping spec. The 10 documents here are the evidence chain for the narrative; they are not the full project. The full project repo is private.

If you want the SIA harness itself: `../sia/` (this repo) + `../README.md` for install + `../examples/fcmfd_replay.ipynb` for a runnable demo.
