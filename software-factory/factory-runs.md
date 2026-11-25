---
name: factory-runs
description: >
  Run mechanics for a software factory — idempotent triggers, webhook
  signature verification with a poller fallback, a repo that builds from a
  fresh checkout, context slicing, disposable sandboxes with seeded test
  data and no credentials, one-branch write access, and hard run budgets
  (retries, CI caps, timeout, spend, kill switch, dry-run). Use when
  building or auditing the orchestrator, sandbox, or run-limits layer.
---

# Factory Runs: Triggers, Sandboxes, Budgets

One-line summary: **a run is disposable by design — fresh sandbox, one branch, a budget it cannot exceed, and a switch that kills it.**

Credit: checklist from [Mar deHaym's post on X](https://x.com/mardehaym/status/2125319432432157152). This is the detailed layer under parts #3–#4 of the `software-factory/SKILL.md` architecture.

## The Checklist

- a trigger that won't kick off the same ticket twice if someone drags it to "AI: Ready" and back
- webhook signature verification, so nobody outside your org can trigger a run on your repo
- a fallback poller for the day the webhook silently drops
- a repo that builds cleanly from a fresh checkout, since the agent doesn't have your laptop's local state
- setup steps an agent can execute without pinging someone on Slack
- a queryable code map, so it actually knows what calls the function it's about to change
- your domain rules written down somewhere the agent can read them
- only the slice of the repo the ticket needs, instead of stuffing the whole codebase into every prompt
- a fresh sandbox for every task that gets nuked the second it finishes
- preloaded dependencies, so runs don't burn ten minutes on npm install every time
- parallel sandboxes that don't trample over a single shared test database
- seeded test data in every sandbox, with zero production data copied over
- zero long-lived credentials sitting inside the sandbox
- an outbound network allowlist, so the agent can't install some random package it read about in a GitHub comment
- write access locked to one working branch, with no way to push to main
- zero merge permissions anywhere in the factory
- a retry cap, so a stuck ticket goes back to the board instead of looping all night
- a cap on CI runs per ticket, because CI minutes aren't free
- a hard timeout for the run that decides your entire billing module needs a rewrite
- hard spend caps per run and per day (the review agent we built for a US healthcare data company cuts off at $20 a day)
- a kill switch that halts every active run immediately
- a dry-run mode that does all the work and posts nothing until you give the green light

## Conventions That Carry the Value

- **Triggers are idempotent and verified.** Status flapping must not double-fire; webhooks must prove their origin; a poller covers the silent-drop day.
- **The agent gets no local state.** If the repo doesn't build from a fresh checkout, every run starts with a broken floor.
- **Context is sliced, not dumped.** Code map first, then only the files the ticket needs.
- **Sandboxes are cattle.** Fresh per task, dependencies preloaded, test data seeded, production data never, credentials never, network egress allowlisted, destroyed on finish.
- **The factory cannot merge.** One working branch, no path to main, zero merge permissions anywhere.
- **Every budget is hard.** Retries, CI runs, wall-clock time, spend per run and per day — when a cap trips, the ticket goes back to the board, not into another loop.
- **Kill switch and dry-run ship on day one.** Halt everything immediately; do all the work, post nothing, until a human green-lights.

## Decision Framework

- **A run is stuck. Now what?** Retry cap trips → back to the board with a report, never an overnight loop.
- **Can the sandbox reach the internet?** Only hosts on the allowlist.
- **Who can merge?** A person. The factory has zero merge permissions.

## Cross-References

- `SKILL.md` — parts #3 (orchestrator) and #4 (sandbox).
- `factory-security.md` — why sandboxes carry no long-lived credentials.
- `factory-observability.md` — the traces and checkpoints that make runs resumable.
