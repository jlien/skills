---
name: software-factory
description: >
  Software factory architecture — the 10 parts that take a ticket from intake
  to a reviewed merge with agents in the loop: intake, spec-and-plan,
  orchestrator, sandbox, gateway, context, gates, evals, measurement, seats.
  Use when designing or auditing an AI-driven delivery pipeline, when "software
  factory" comes up in planning, or when deciding what to build around the
  agent (the platform underneath it is most of the work).
---

# Software Factory

One-line summary: **most of a software factory is the platform underneath the agent — a gateway, measurement, gates and evals. Build those first, on the stack you already own. Adding the agent is the easiest part.**

Credit: this comes from [Mar deHaym's post on X](https://x.com/mardehaym/status/2122415554736570852).

A software factory takes a ticket in and returns a reviewed pull request. The work is split three ways: code handles every step it can check, agents handle the few steps that need judgment, and people own the spec, the hard decisions and the merge.

The rule is simple: if code can check it, code does it. An agent saying "the tests pass" doesn't count. CI decides.

## The 10 Parts

1. **Intake.** A status in your tracker starts the run. If the ticket doesn't have acceptance criteria that code can check, it goes back instead of getting built.
2. **Spec and plan.** Before writing any code, the run lays out what it will build and how. A person approves that plan in the ticket, while a misunderstanding still takes minutes to fix.
3. **The orchestrator.** Every ticket goes through the same fixed steps, within a budget for CI runs, attempts, time and money. In the reference design, a run gets two CI runs. If the second is still red, it stops and leaves a report in the ticket.
4. **The sandbox.** Every task gets a fresh sandbox, with no credentials inside and an allowlist for outbound connections. When the task ends, the sandbox gets thrown away.
5. **The gateway.** Every model call in the company goes through one gateway you host. Each team and service gets its own key and spend cap. Switching models becomes a config change.
6. **Context.** The agent uses a map of the code to see what depends on what, then pulls only what it needs. A huge legacy repo becomes a handful of relevant files.
7. **The gates.** CI decides whether the work passes. Deleting a test sends it back. The agent can't change its own rules, a review agent has to quote the code it flags, and a person merges every pull request.
8. **Evals.** Prompts live in git. A prompt change only ships after it passes test cases built from real past pull requests.
9. **Measurement.** Every change connects the session, commit, pull request, ticket and epic, so you can see what a feature cost and how long it took. Report this by team, never as a ranking of individual developers.
10. **The seats.** Engineers' own AI tools connect directly to their vendors. Track that usage through metadata only: who uses what and what it costs. No prompts or code.

## What Doesn't Qualify

- Giving every engineer an AI coding tool is useful, but that alone won't take a ticket from intake to merge.
- One agent with access to your repo gives you the loop, without the factory around it.
- A swarm sharing one long conversation spends tokens on every agent rereading everything.
- If the whole thing only works while your code and staging data sit on a vendor's servers, you have a production line you can't move.

## What Stays With People

Architecture, new domains, greenfield, big refactors, performance work and product discovery stay with people. The factory handles work that's well specified and checkable, giving your seniors more time for the rest.

## Where It Breaks

The slowest part is #1, intake. Most backlogs don't have acceptance criteria that code can check. Rewriting those tickets takes time, and nobody volunteers for it.

## The Rent-vs-Own Test

If you stop paying the vendor tomorrow, does the factory keep running? If it doesn't, you're renting the production line.

## Decision Framework

- **Build order:** gateway, measurement, gates and evals first — the platform, on the stack you already own. The agent comes last and is the easiest part.
- **Is a ticket factory-ready?** Only if it has acceptance criteria that code can check. Otherwise it goes back to a person.
- **Who decides quality?** CI — never the agent's self-report. A person merges every PR.
- **Is it a factory or a pilot?** One ticket in, one reviewed PR out, through the same fixed steps, inside budget.

## Collaboration With the Other Skills

- `ai-transformation/SKILL.md` — the transformation playbook this factory slots into: the factory is the destination of its Phase 3 (workflows) and the #5 gateway reappears as its Phase 4 guardrail.
- `code-review/SKILL.md` — part #7's gates: CI decides, review agents quote the code they flag, a person merges.
- `CTO.md` — the technical-strategy owner for the build-vs-own and gateway decisions.
