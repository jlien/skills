---
name: factory-observability
description: >
  Observability and traceability for a software factory — full traces of
  every model call, self-hosted because prompts contain your source, one
  unbroken session-to-epic chain, run history in a real database, checkpoints,
  cycle-time metrics with no developer leaderboards. Use when wiring up
  measurement, when a bad PR needs tracing to its cause, or when a crashed
  run has to resume.
---

# Factory Observability & Traceability

One-line summary: **one unbroken chain — session, branch, commit, PR, ticket, epic — stored on your own infrastructure, because the traces contain your source code.**

Credit: checklist from [Mar deHaym's post on X](https://x.com/mardehaym/status/2125319432432157152). This is the detailed layer under part #9 of the `software-factory/SKILL.md` architecture.

## The Checklist

- full traces of every model call: prompt, output, tokens, latency, and cost
- self-hosted traces, because those prompts contain your source code
- one unbroken chain linking session, branch, commit, PR, ticket, and epic
- logs that never capture secrets, tokens, or patient data
- run history stored in a real database, not inside an agent's memory
- checkpoints so a crashed run picks up where it left off instead of starting over and billing you twice
- alerts when the queue backs up, before product asks why nothing shipped
- cycle time pulled straight from that chain, not from developer surveys
- reporting rolled up by team and feature, with zero individual developer leaderboards

## Conventions That Carry the Value

- **Trace everything, host it yourself.** Prompt, output, tokens, latency, cost per call — on infrastructure you own, because the payloads are your source.
- **The chain is the spine.** Session → branch → commit → PR → ticket → epic, linked. Cycle time and cost per feature come from the chain, not surveys.
- **Run state lives in a database.** An agent's memory is not storage; checkpoints let a crashed run resume instead of re-billing.
- **Logs are scrubbed by design.** Never secrets, tokens, or patient data — matching `factory-security.md`.
- **Alerts precede awkward questions.** Queue backlog fires before product asks why nothing shipped.
- **Report by team and feature.** Never rank individual developers.

## Decision Framework

- **Why did this PR open, and what did it cost?** Follow the chain; the answer is a query.
- **A run crashed mid-task.** Resume from its checkpoint, don't restart and double-bill.
- **Who is the slowest developer?** Not a metric that exists. Team and feature rollups only.

## Cross-References

- `SKILL.md` — part #9 (measurement) and the build-order rule (measurement before agent).
- `factory-gateway.md` — where per-call token and cost data originates.
- `factory-runs.md` — checkpoints and run budgets.
