# Data and Enrichment — Get the Contact Data Right

Outbound lives or dies on deliverability and contact quality. This section is deliberately narrow: where data comes from, how to get an email that lands, how to prove it works, and when a phone number is worth the cost.

## Data sources

Use a small, known set of sources — every new source adds a dedupe and quality problem.

- Firmographics + contacts: a primary data provider, supplemented by a secondary for verification (the "waterfall" below).
- Technographics: tech-detection feeds; job postings as the forward-looking source (see `signals.md`).
- Rule: every source gets evaluated on coverage, accuracy, and freshness before adoption, and re-evaluated quarterly against the bounce-rate number in `reporting.md`. A source that quietly rots poisons everything downstream.

## Email waterfall

One provider misses roughly half the time. The waterfall finds the email by trying sources in order, not by buying three subscriptions and hoping.

1. Provider A. If no result →
2. Provider B. If no result →
3. Pattern inference (first.last@domain) → **verify before use** (see below). Guessed patterns never go to a live send unverified.
4. No verified result: the contact is unreachable. Log it and stop — an unverified send is how a domain burns.

Implementation notes: run the waterfall automatically at enrichment time (scheduled, per `revops.md`), not manually at send time. Log which source produced each email so you can cut sources that fail.

## Email verification

Verification runs on every address before first use, and re-runs on any list before a new campaign.

- Verification result classes: valid / invalid / risky (catch-all, disposable, role-based).
- Valid sends. Risky sends in a small batch with a real reply expectation, never in a bulk sequence. Invalid never sends.
- Hard rule tied to `reporting.md`: bounce rate above ~2% means stop sending and re-verify the list before another email goes out. Bounces are the #1 deliverability killer and they compound — each bounce makes the next email less likely to land.

## Mobile numbers for the top tier

Phone is the highest-response, highest-cost channel — reserve it.

- Who: tier 1 accounts only (per `scoring.md`), and only contacts who've been worked and gone quiet, or hot-signal contacts (per routing).
- Where: direct-dial providers; verify with a dialer's validation before loading into the CRM.
- Discipline: numbers without a reason to call rot fast. Don't buy mobile data for the whole database — it costs real money and produces calls nobody should make.

## Decision Framework

- **Buy more contacts or fix conversion first?** Fix conversion. More volume into a broken funnel burns domain and brand simultaneously.
- **A source's data caused bounces?** Re-verify everything that source produced; drop it if the pattern repeats.
- **Guessed email pattern?** Verified or not sent. No exceptions — one bad batch costs weeks of inbox warm-up.

## Collaboration With the Other Skills

- `revops.md` — enrichment scheduling and the CRM-as-record rule apply to all data here.
- `outbound.md` — sending infrastructure depends on the verified-data discipline in this file; bounces here become spam flags there.
- `reporting.md` — bounce rate is this section's primary health metric; watch it weekly.
