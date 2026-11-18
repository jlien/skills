# Signals — The Inputs That Tell You When to Act

The largest section of the `gtm` tree on purpose: collect inputs broadly, act narrowly. A signal is only real if it has three things — a source that catches it, an ICP filter that says it's relevant, and an action attached when it fires (routing per `revops.md`). A signal with no attached action is trivia.

## Hiring

What: the account is growing in roles that map to your product's job (e.g. you sell to sales teams → AE/SDR openings).

- Source: job boards, career pages, job-posting data feeds.
- Filter: openings count within a window (≥2 relevant postings in 30 days is a decent threshold; tune per segment).
- Action: route to owner with the specific roles named in the outreach first line — copy references the actual openings, not "I saw you're hiring."

## Funding

What: new capital means budget and a mandate to grow.

- Source: funding databases, press releases, regulatory filings (public records below).
- Window matters: funding older than ~6 months has usually been allocated. Route within days of announcement.
- Action: tier bump on the account list, first line references what they said they'd invest in.

## New hires and GTM leaders

What: a new VP/C-level in a role your product serves is the highest-intent signal there is. New leaders buy tools in their first 90 days; that is their one window of mandate.

- Source: LinkedIn job-change feeds, press announcements.
- Action: contact the new leader directly within the first 2 weeks. First line: what you know about their mandate, not a feature list. If they were hired into an adjacent team (not your buyer), route as warm context, not as the pitch.

## Past champions

What: a person who bought from you (or evaluated and lost) just moved to a new company.

- Source: CRM contacts matched against job-change feeds, run weekly.
- Action: reach out personally — warm, no pitch, "congrats, saw the move." Champions who moved are the cheapest pipeline that exists. Route into the new company's account entry.

## Tech stack

What: the account runs a technology that implies your product fits (integrates, replaces, complements).

- Source: tech-detection feeds, job postings that mention the tool (a company hiring for X is about to run X).
- Action: pair with the integration story. "Replaces X" and "works with X" are different pitches — tag which one applies.

## Public records

What: filings, regulatory registrations, procurement notices, lawsuits. Slow, boring, and nobody else reads them.

- Source: SEC/Companies House filings, court records, government procurement portals — depends on segment.
- Action: long-horizon plays. A permit filing today is a budget line 12 months out. Route to tier 2 with a dated follow-up.

## Website visitors

What: de-anonymized visitor data showing which target accounts are on your site, and which pages.

- Source: IP-matching visitor tool.
- Filter: ICP accounts only; ignore everyone else or the signal drowns.
- Action: route within 24h. The visited page is the copy: pricing page visitors get a pricing conversation, docs visitors get a technical one. Do not email "I saw you visited our website" — reference the topic, not the surveillance.

## Review sites

What: accounts actively comparing categories on G2/Capterra-type sites, and reviews of you and competitors.

- Source: review-site buyer-intent feeds, plus your own review pages.
- Action: intent-flagged accounts go straight to tier 1 — these people are mid-decision. Reviews of competitors on target accounts are first-line material: "saw you evaluated X."

## Post engagers

What: someone from a target account engaged with your (or a founder's) content.

- Source: LinkedIn engagement on company/founder posts, newsletter clicks, webinar attendance.
- Action: warm follow-up referencing the actual topic they engaged with. Engagement is permission to talk about that topic only.

## Target-account exec posts

What: an exec at a tier-1 account posts about a problem you solve.

- Source: LinkedIn feed filtered to the account list.
- Action: reply substantively within hours (not "great post!"), then optionally a DM that continues the thread. The reply is public proof you think; the DM is where the meeting happens. Never pitch in the reply.

## Brand mentions

What: your brand, competitors, or category terms mentioned in public — forums, communities, news.

- Source: alerts on brand and competitor names, community monitoring.
- Action: for brand mentions, thank and engage; for competitor mentions in "who should I use" threads, answer helpfully per community rules (see `community.md`), disclose affiliation. For category terms, answer the underlying question and link only where the forum allows.

## Making the system work

- **Each signal gets an owner, a time budget, and an attached play** — same routing rules as `revops.md` (signal routing to owners). Hot signals (new GTM leader, review-site intent, website visitor) move in minutes; slow ones (public records, hiring) move in days.
- **Deduplicate at the routing layer.** One account firing five signals in a day is one priority account, not five tasks. Aggregate to the owner.
- **Measure which signals actually convert**: `reporting.md` tracks "meetings booked per signal" by signal type. Kill signals that fire often and convert never — they cost attention, which is the scarce resource.

## Decision Framework

- **Is it a signal or just news?** If nothing in your motion changes when it fires, it's news. Don't collect it.
- **Which signal first?** Start with 3-4: new GTM leaders, hiring, funding, website visitors. Add more only when those are routed and measured end to end.
- **Signal fired for a non-ICP account?** Drop it. The ICP filter (`icp-and-tam.md`) runs before routing, not after.

## Collaboration With the Other Skills

- `revops.md` — routing, ownership, SLAs live there.
- `icp-and-tam.md` — the one account list defines which signals are even worth catching.
- `scoring.md` — each signal type contributes to the intent score.
- `outbound.md` — "first line per signal" is written against the signals defined here.
