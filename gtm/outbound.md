# Outbound — Get Replies Without Burning the Domain

Outbound is a deliverability business that happens to send messages. Volume is capped by reputation, not by will. This file covers the infrastructure, the copy, the channel mix, and what happens when someone replies.

## Sending infrastructure

Secondary domains and warmed inboxes are insurance: the primary company domain never sends cold.

- Register 1-2 secondary domains (variants of the brand, real-looking — not obvious throwaways), with real sites on them.
- SPF, DKIM, DMARC configured on every sending domain before any send. DNS setup is table stakes, not an optimization.
- Warm new inboxes for 2-4 weeks (low-volume human-like exchange) before campaigns. Warm-up tools help, but the honest version is: send few, reply to everything, wait.
- Volume per inbox: start at 10-20/day, scale to 30-50/day max. Scale by adding inboxes, never by raising per-inbox volume. A burned domain takes 6-8 weeks to recover; a burned primary company domain, much longer.
- Monitor `reporting.md` spam and bounce rates weekly; a spike is a stop signal, not a stat.

## Copy

**First line per signal** — the opening line is built from the trigger that routed the account (`signals.md` defines the signals; each has a first-line template).

- The first line proves the message isn't a blast: name the specific trigger (the roles they're hiring, the funding round, the exec post, the page they visited — topic, not surveillance).
- One idea per email. The email asks one question; the CTA is a question that costs the reader nothing ("worth a look?" not "15 minutes on Tuesday?").
- Write from persona language (`icp-and-tam.md`), not internal jargon. Read every template out loud before it ships — if it sounds like a vendor, rewrite it.
- Keep emails under ~90 words. Short emails don't just read better; they carry fewer spam-trigger patterns.

**1 test per round** — one variable per testing cycle.

- A "round" is 2-4 weeks. Each round changes exactly one thing: the first line, the CTA, or the persona angle — never two, or you can't attribute the delta.
- Sample size discipline: don't call a round after 30 sends. A round needs enough volume per variant that the difference in `reporting.md` positive-reply rate couldn't be noise.
- Losers get archived with their numbers. Winning variants become the new control. The test log is one file; if you can't name last round's winner, the testing program doesn't exist.

## Channels

- **Email:** the workhorse; runs at infrastructure scale, governed by this file.
- **LinkedIn:** for the same contacts, in parallel but not copy-paste — connection request with no pitch, then a shorter version of the email angle. Social touches on exec posts (see `signals.md`) precede DMs.
- **Calls for the top tier:** tier 1 accounts only (`scoring.md`), worked with verified numbers from `data-and-enrichment.md`. Calls convert where email stalls; the cost is the reason they're reserved.

Channel mix per tier: tier 1 gets email + LinkedIn + calls; tier 2 gets email + LinkedIn; tier 3 gets nothing.

## Reply routing

A reply is the conversion moment — handle it like it matters, because it's the entire point.

- **Reply labels:** classify every reply within a day: interested / later (with a date) / not-a-fit / referral / negative. Labels feed `reporting.md` positive-reply rate; unlabeled replies are unmeasured conversions.
- **Approval gate:** before an automated or template response goes to an "interested" reply, a human approves it. Interested replies get a human reply from the sender — not a sequence, not a booking link dump. The approval gate is also the quality check on copy: bad template responses show up here first.

## Decision Framework

- **Scale volume or fix reply rate?** Fix reply rate first (1 test per round) — scaling a below-average reply rate just burns domain faster.
- **A test won on a small sample?** Re-run it. Winner calls on <100 sends per arm are coin flips.
- **Hot reply arrives?** Route per `revops.md` SLA (minutes, not days). Speed-to-reply is the highest-leverage number in outbound.
- **Domain hit a spam/bounce spike?** Stop the campaign, re-verify lists, check infrastructure before restarting. Don't "send through it."

## Collaboration With the Other Skills

- `signals.md` + `scoring.md` — who gets contacted, and the trigger for every first line.
- `data-and-enrichment.md` — verified emails and dialer numbers feed every send.
- `reporting.md` — reply rate, positive reply rate, spam and bounce rate are this file's scoreboard.
- `inbound-and-pipeline.md` — reply routing hands off to meeting booking once interest is confirmed.
