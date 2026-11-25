---
name: factory-intake
description: >
  Ticket intake and spec-and-plan for a software factory — self-contained
  tickets with I/O contracts, a gate that bounces vague tickets back to a
  human, testable acceptance criteria, a human-approved spec and build plan,
  and big tickets chunked to one run. Use when writing factory-ready tickets,
  deciding what the factory may touch, or when agents keep guessing instead
  of asking.
---

# Factory Intake & Spec

One-line summary: **the agent has zero tribal knowledge, so the ticket is the entire world it gets — intake quality is the factory's ceiling.**

Credit: checklist from [Mar deHaym's post on X](https://x.com/mardehaym/status/2125319432432157152). This is the detailed layer under parts #1–#2 of the `software-factory/SKILL.md` architecture.

## The Checklist

- self-contained tickets with explicit I/O contracts and edge cases, because the agent has zero tribal knowledge
- a gate that bounces vague tickets back to a human before the agent starts guessing
- testable acceptance criteria on every ticket
- a short list of ticket types the factory is allowed to touch, and a much longer list of the ones it can't
- a written spec before any code gets written, approved by a real person
- a way to route open questions to a human instead of letting the model wing it
- a build plan laying out the architecture, data changes, and contracts upfront
- a sanity check confirming the spec, plan, and task list actually agree with each other
- big tickets broken down into chunks an agent can finish in a single run
- acceptance criteria that stay attached to the ticket all the way through code review
- documented architecture decisions, so the agent stops trying to relitigate them every run

## Conventions That Carry the Value

- **The I/O contract is the ticket.** Inputs, outputs, edge cases — written down, not implied. Anything the agent has to infer, it will infer wrong.
- **The gate runs before the guess.** A vague ticket goes back to a human at intake, not mid-run when the agent has already spent the budget.
- **Scope is a written allowlist.** A short list of allowed ticket types and a much longer forbidden list. The default for anything unlisted is "no".
- **Open questions route to a person.** The model never fills a spec gap with its best guess.
- **Spec → plan → consistency check, in that order.** A person approves the spec, the plan lays out architecture/data/contracts, and a check confirms all three artifacts agree before code starts.
- **One run, one chunk.** A ticket too big for a single run gets split at intake, not discovered mid-run.
- **Acceptance criteria are sticky.** They ride with the ticket through implementation and into code review — that is what the verifier grades against.
- **Architecture decisions are written down** so the agent stops relitigating them on every run.

## Decision Framework

- **Is a ticket factory-ready?** Only if a person could hand it to a new hire with no other context and expect the right output. Otherwise it bounces.
- **Who answers a spec question?** A human, via the routing path — never the model.
- **What size is one ticket?** Whatever one agent run can finish; split the rest.

## Cross-References

- `SKILL.md` — the 10-part architecture this slots into (parts #1 and #2).
- `code-review/SKILL.md` — where the acceptance criteria resurface as review standards.
- `Project-Management.md` — backlog vocabulary for the status transitions.
