# AI Agents — Automate the GTM Loops That Are Actually Loops

AI agents in GTM work when the task is repeatable, the input is structured, and a human checks the output at the moment it matters. They fail when asked to fake judgment or to replace the human at a conversion moment. The section's five agents, in the order to build them:

## Lead scoring

The scoring model in `scoring.md` is the spec; the agent is the machinery.

- Agent job: recompute fit and intent scores on every enrichment run and signal event, apply decay, re-tier, and route tier changes to owners (per `revops.md` SLAs).
- Human stays at: the override (owners can re-tier with a logged reason) and quarterly reweighting of signal weights from measured conversion.
- Watch: score drift. When the tier list stops matching the deal review's gut, recompute the weights from fresh data instead of patching one score.

## Pre-call research

The pre-call brief from `inbound-and-pipeline.md`, written by an agent, checked by a rep in 5 minutes.

- Agent job: pull the account snapshot, signals that fired, site/product activity, CRM history, persona notes — into the template, before the meeting, into the rep's workflow.
- The rep reads it and corrects it. An unchecked brief that reaches the call can confidently state something wrong — the check is the product.
- The 5-minute check is the whole ROI: a rep doing research manually spends 20-30 minutes per call and does it worse.

## Signal to sequence

When a signal fires, the sequence enrolls itself — with the right first line.

- Agent job: signal fires (`signals.md`) → validate the account is on-list and ICP-passed (`icp-and-tam.md`) → enroll in the matching sequence with the signal-specific first line (`outbound.md`) → route to owner.
- The library of first lines per signal is a maintained artifact — the agent picks from it, it doesn't write new copy unsupervised. New first lines enter through the 1-test-per-round loop (`outbound.md`).
- Guardrail: dedupe and rate-limit. One account firing five signals gets one enrollment and one owner note, not five sequences.

## Copy intelligence

Copy is drafted by agents and edited by humans; the 1-test-per-round loop (`outbound.md`) decides what survives.

- Agent job: draft first-line variants from persona language (`icp-and-tam.md`) and past winners; summarize reply themes across the label data (`outbound.md` reply labels) so the next round is informed by what buyers actually said.
- The agent never ships copy directly to a send. Drafts go through the approval gate (`outbound.md`), which is also where bad drafts get caught.
- Feed the agent wins, not just briefs: the winning variants' texts and their label data are the training set.

## Meeting action items

The post-call loop that keeps deals moving: transcript in, structured record out.

- Agent job: from the call recording — summary in the buyer's language, action items with owners and dates, objections and competitor mentions tagged into the CRM, loss/churn-relevant quotes saved (feeds the buyer-questions loop, `content.md`).
- Write into the CRM (the record, `revops.md`), not into a notes tool the deal review never sees.
- Follow-up draft gets generated same-day; the rep edits and sends (the human-at-conversion rule — `outbound.md` reply routing).

## The Human-at-Conversion Rule

Automate everywhere except the moments that decide the deal: the reply to an interested buyer, the live call, the follow-up that lands the next step. Everything upstream of those can run itself; those moments get a person, every time.

## Decision Framework

- **Agent or template?** If a template with merge fields does the job, use the template. An agent is justified when the input varies (research, summaries, signal variety) — not when the output is the same five fields.
- **Where's the check?** Every agent output has a named human checkpoint. No checkpoint, no deployment.
- **Agent output silently wrong twice?** Fix the input data or shrink the agent's scope. Never add a second agent to catch the first one's errors.

## Collaboration With the Other Skills

- `revops.md` — the CRM is the record; agents write there, not around it.
- `signals.md` + `scoring.md` — the signal taxonomy and score spec are what these agents implement.
- `outbound.md` — first-line library, reply labels, approval gate, 1-test-per-round: the human loop this section's agents plug into.
- `content.md` — reply themes and call quotes feed the buyer-questions loop.
