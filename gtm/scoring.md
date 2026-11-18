# Scoring — Turn Signals into a Queue

Scoring exists for one reason: attention is scarce, and the next action should always go to the account most likely to buy. Keep the model simple enough to explain out loud. A model nobody can explain doesn't get trusted, doesn't get maintained, and quietly stops mattering.

## Fit score

How much the account looks like your ICP (see `icp-and-tam.md`). Static attributes only.

- Formula: point-weighted boolean checks derived from the ICP sentence. E.g. headcount in band (+), industry in segment (+), tech stack match (+), region covered (+).
- Keep it to 5-8 factors. Each factor must be something you'd actually disqualify on. If no one would drop an account for failing a factor, it doesn't belong in the score.
- Refresh on the enrichment schedule (`revops.md`) — fit decays when the data does.

## Intent score

How much the account is behaving like a buyer right now. Behavioral signals only.

- Inputs: each signal type from `signals.md` with a weight roughly proportional to its observed conversion (measured, not guessed — start with your intuition, then reweight quarterly from `reporting.md` data).
- Time-window the inputs: 30-90 days. A website visit from 8 months ago is not intent, it's history.

## Tiers 1, 2, 3

The tiers are the output of fit × intent — the only thing downstream motions see.

- **Tier 1:** high fit, active intent. Gets calls, 1-to-1 outreach, full personalization. Size-capped (see `icp-and-tam.md`).
- **Tier 2:** good fit, dormant or weak intent. Gets sequenced nurture and waits for a trigger to promote.
- **Tier 3:** everything else. Costs nothing and receives nothing.
- Publish the thresholds. When someone asks "why is this account tier 2," the answer is a formula, not a feeling.

## Score decay

Scores fall when signals age, so that a hot account that goes cold actually leaves the queue.

- Intent components decay on a half-life (e.g. each signal loses half its weight every 30 days) or via the simple version: intent resets to zero unless a fresh signal fires inside the window.
- Decay is what makes the tier list a queue instead of a graveyard. Without it, tier 1 fills with accounts that were hot once.

## Hot, warm, cold routing

The tier (plus any live signal) maps to an action with a time budget:

- **Hot** — a live high-intent signal: owner works it in minutes (see `revops.md` routing SLAs). Human touches it, always.
- **Warm** — fit without live intent: enters nurture; automation carries it until a trigger fires.
- **Cold** — nothing now: scheduled re-enrichment, and a re-look when a new signal fires.

The map from score to hot/warm/cold is written down and reviewed quarterly against conversion data.

## Decision Framework

- **Model getting complex?** Cut factors before adding weights. Two factors everyone believes beat eight factors nobody checks.
- **Score vs. judgment conflict?** The owner can hand-promote/demote an account, with a one-line reason in the record. Track override rate: if overrides are frequent, the model is wrong; if never, nobody's looking.
- **New signal type?** Add it to intent only after it's measured (a quarter of data), not when it's shiny.

## Collaboration With the Other Skills

- `icp-and-tam.md` — fit score is the ICP sentence as a formula; tiers drive the account list's tiering.
- `signals.md` — intent inputs are the signals, with measured weights.
- `outbound.md` — hot/warm/cold determines channel and effort: hot gets calls, warm gets sequences.
- `abm-and-paid-ads.md` — intent feeds ad audiences and account selection.
