---
name: factory-roles
description: >
  The people a software factory still needs — product owner writing the
  spec, senior engineers signing the plan and reading every PR, tech lead
  deciding forbidden tickets, architect, QA, platform engineer, AI engineer,
  security/compliance, engineering manager, on-call. Use when staffing a
  factory, when someone claims agents replace developers, or when assigning
  ownership of the factory's failure modes.
---

# Factory Roles: Who You Still Need

One-line summary: **the factory doesn't remove a single role — it moves every one of them up a level, from writing code to owning what the agent builds from.**

Credit: checklist from [Mar deHaym's post on X](https://x.com/mardehaym/status/2125319432432157152). Pairs with "What Stays With People" in `SKILL.md`.

## The Checklist

- writing the spec the agent builds from (a product owner who knows the domain)
- signing off on the plan before a line of code exists (a senior engineer)
- reading every pull request before it merges (a senior engineer, again)
- deciding which tickets the factory is never allowed to touch (a tech lead)
- keeping the architecture from turning into spaghetti while agents keep adding to it (an architect)
- writing the test cases the factory gets graded on (QA)
- running the gateway, sandboxes, and cloud bill (a platform engineer)
- rerunning evals every time a model changes (an AI engineer)
- walking an auditor through what the agent read and what it changed (security and compliance)
- explaining to the CFO why the token bill doubled in March (an engineering manager)
- answering the 3 a.m. page when an agent-written change breaks checkout (whoever's on call)
- debugging the code when the agent that wrote it gets stuck (a senior engineer)
- remembering why the factory was built this way a year from now (someone who was actually there)

## Conventions That Carry the Value

- **Each failure mode has a named owner.** Spec quality → product owner. Plan and PR sign-off → senior engineer. Scope limits → tech lead. Architecture → architect. Grading → QA. Infrastructure → platform engineer. Model changes → AI engineer. Audit → security/compliance. Bill → engineering manager. Pages → on-call.
- **The agent never owns a judgment call.** Every item above is a decision, and every decision has a person.
- **Institutional memory is a role, not a side effect.** Someone who was actually there has to remember why it was built this way.
- **Seniors debug what agents get stuck on.** The skill that writes the code also fixes it — just less often.

## Decision Framework

- **Who approves what?** Spec = product owner. Plan = senior engineer (before code). Merge = a person, every time. Forbidden-ticket list = tech lead.
- **Does the factory reduce headcount?** It shifts everyone up a level; if no one owns the failure modes, the factory isn't staffed.

## Cross-References

- `SKILL.md` — "What Stays With People" and the 10 parts each role runs.
- `factory-ops.md` — on-call, runbooks, and the budget owner in practice.
- `factory-intake.md` — the spec and plan the product owner and senior engineer sign.
- `CTO.md` and `Product-Manager.md` — the leadership owners of the technical and product decisions.
