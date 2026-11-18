# ICP and TAM — Decide Who You Sell To Before Deciding How

The ideal customer profile is the highest-leverage decision in GTM: every motion downstream inherits it. Get it wrong and execution quality cannot save you. Derive the ICP from evidence, keep it in exactly one artifact, and re-derive it when the evidence changes.

## ICP from closed-won deals

Build the profile from your own wins, not from a template.

1. Pull every closed-won deal from the last 12-24 months from the CRM (see `revops.md`).
2. For each, capture: industry, company size, role of buyer, trigger that started the deal, deal cycle length, and ACV.
3. Cluster wins. The ICP is the cluster with the best combination of **win rate, deal size, and cycle speed** — not the biggest cluster.
4. Do the same for closed-lost. The negative ICP (who you lose to repeatedly, or who churns) matters as much: "loss reasons" in `revops.md` feeds this directly.
5. Write the ICP as one testable sentence: companies of X in Y with Z, buying because of W. If you can't write the sentence, you don't have an ICP.

Re-derive every six months, or whenever a new segment starts winning disproportionately.

## Segments

Split the ICP into 2-4 operating segments — segments you will actually treat differently, not a taxonomy.

- Segment on the variable that changes your motion: buyer role, company size band, or use case. If your process is identical for two segments, they are one segment.
- Each segment gets its own account-list filter, first-line copy variants (see `outbound.md`), and its own line in `reporting.md` ("pipeline by motion" only means something if motions differ).
- One segment should be the current focus. Running all segments equally means running none well.

## Personas

For each segment, document the 2-3 humans who appear in the deal: the economic buyer, the champion, the blocker.

- Per persona: what they're measured on, what they're afraid of, the words they use for the problem, and the one proof they need to believe you.
- Personas come from real calls — quote actual phrases, don't invent. Ten minutes of recorded calls per persona beats any framework.
- Copy, decks, and first lines reference persona language, never internal jargon.

## Lookalikes

Expand the account list from the pattern of your best customers, not from a bought list of "companies like you."

- Take the top 10-20% of customers (by revenue or retention — pick one and say which) and extract their observable attributes.
- Build the lookalike filter on attributes you can actually query in a data source: headcount band, industry, tech stack, hiring velocity, funding stage.
- Cap the output: a lookalike list is an input to the account list (see below), not a list in its own right. Two lists that both claim to be the target list is how targeting rots.

## 1 account list

Exactly one list defines who you are pursuing right now.

- It lives in one place (a CRM view or a single sheet synced to the CRM — per `revops.md`, the CRM is the record).
- Tiered: tier 1 (active pursuit, fully enriched), tier 2 (qualified, queued), tier 3 (future). Tiers map to the scoring system in `scoring.md`.
- Every other motion — outbound, ads, content targeting — reads from this list. If a motion has its own target list, that's a bug: reconcile it into the one list.
- The list has a size budget. If everyone is the target, no one is; tier 1 stays small enough that each account gets real attention.

## Decision Framework

- **Evidence or opinion?** An ICP claim without closed-won data behind it is a hypothesis — label it as one and go validate.
- **New segment or deeper on the current one?** Default to deeper, until the current segment is genuinely saturated (tier-1 account list worked through, reply rates healthy).
- **Should this company be on the list?** Does it pass the ICP sentence, and does it have a reachable trigger (see `signals.md`)? Both, or it's tier 3.
- **Two sources disagree about the target list?** The one list wins; merge or delete the other.

## Collaboration With the Other Skills

- `revops.md` — the CRM supplies the closed-won evidence and stores the account list.
- `signals.md` — triggers are how accounts earn tier-1 attention; the ICP says who, triggers say when.
- `scoring.md` — fit score is the ICP sentence turned into a formula.
- `content.md` — persona language drives founder posts and copy.
