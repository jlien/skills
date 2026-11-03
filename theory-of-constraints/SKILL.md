---
name: theory-of-constraints
description: >
  Theory of Constraints analysis — a team of specialist agents that find the
  binding constraint in any process, apply the Five Focusing Steps, and reason
  with Goldratt's Thinking Processes (CRT, Evaporating Cloud, FRT with Negative
  Branch Reservation, Transition Tree) plus Throughput Accounting. Use when a
  process is slow, a team or pipeline is underperforming, work piles up at one
  stage, two legitimate goals conflict, or an improvement effort stalled.
---

# Theory of Constraints Agent Skill

One-line summary: **every system's output is set by exactly one constraint at a time — find it, squeeze everything out of it, and stop optimizing everything else.**

This directory is a team of specialist agents, not a single skill. Load the entry point, route to the specialist the engagement stage calls for, and keep the other files unloaded until needed. Each agent is self-contained: one file, one job, its own decision framework.

## The Agent Team

| Agent | File | Job in one line |
|---|---|---|
| Orchestrator | `SKILL.md` (this file) | Route the engagement, keep the Five Focusing Steps moving |
| Constraint Finder | `constraint-finder.md` | Locate the system's binding constraint with evidence, not opinion |
| Five Focusing Steps | `five-focusing-steps.md` | Exploit → Subordinate → Elevate → Repeat around the found constraint |
| Current Reality Tree | `crt.md` | Trace a set of undesirable effects down to the root cause that drives them all |
| Evaporating Cloud | `evaporating-cloud.md` | Resolve a genuine conflict between two legitimate needs |
| Future Reality Tree | `future-reality-tree.md` | Prove a proposed fix produces the desired effects — and trim negative branches before they happen |
| Transition Tree | `transition-tree.md` | Convert an agreed fix into a concrete, obstacle-aware implementation plan |
| Throughput Accounting | `throughput-accounting.md` | Score every decision by Throughput / Inventory / Operating Expense, not cost accounting |

## Engagement Workflow

Run the stages in order; each has an exit criterion. Do not skip to solutions.

1. **Map and measure** — draw the process end to end with real numbers (arrival rates, cycle times, WIP, queue lengths per stage). Exit: you can state where work accumulates.
2. **Find the constraint** — load `constraint-finder.md`. Exit: one stage named as the binding constraint, with evidence that would falsify it.
3. **Decide the focus move** — load `five-focusing-steps.md`. Exit: a chosen step (exploit, subordinate, or elevate) with a specific action.
4. **Surface hidden conflicts** — if the constraint analysis stalls on "we can't do X because Y conflicts with Z", load `evaporating-cloud.md`. Exit: an injection that satisfies both needs.
5. **Validate the future** — load `future-reality-tree.md` before committing to the fix. Exit: each original undesirable effect is logically resolved and negative branches are trimmed.
6. **Plan the transition** — load `transition-tree.md`. Exit: an ordered implementation plan with obstacles and resources named.
7. **Score decisions** — load `throughput-accounting.md` whenever a choice needs justification in money terms. Exit: the decision stated in T/I/OE terms.
8. **Repeat** — after the constraint moves, return to stage 2. The process never ends; the constraint just relocates.

**Stage routing shortcuts:** If symptoms are known but causes are tangled, run `crt.md` before anything else. If the "constraint" turns out to be a policy or a dilemma rather than a resource, the Evaporating Cloud is the right tool even mid-engagement.

## What TOC Is Not

- Not a survey of every inefficiency. Non-constraint improvements produce zero system gain and consume the credibility you need for the real fix.
- Not cost reduction. Cost-world thinking optimizes every part; throughput-world thinking optimizes the whole by serving the constraint.
- Not a one-time project. Step 5 of the Five Focusing Steps warns that the real danger is inertia — yesterday's solution becoming today's policy constraint.

## Collaboration Patterns

### With `Project-Management.md`
A blocker is local and temporary (this task waits on a person); a constraint is systemic and structural (all throughput passes through this point). The Project-Management agent handles blockers; escalate to Constraint Finder when the same class of blocker recurs across tasks. Feed TOC findings into the risk register.

### With `Product-Manager.md` and `CPO.md`
When the constraint is demand rather than capacity — the market won't buy more at current value — the constraint moves to marketing and sales. Product decisions (what to build) are capacity-allocation decisions: sequence the backlog by contribution to Throughput, not by story count.

### With `CTO.md`
Capacity investments (new hires, infra spend) are "elevate the constraint" decisions and must pass the Throughput Accounting test before budget is committed. Architecture choices that slow the constraint stage (e.g., heavyweight review on the deployment pipeline) are policy constraints — the CTO agent should retire them.

### With `ruby-on-rails/SKILL.md` and `code-review/SKILL.md`
Engineering pipelines have constraints too: CI runtime, review turnaround, deploy frequency. Apply the same logic — measure queue depth per stage, exploit the constraint (batch smart, skip stages that add no information), never push more WIP into a saturated stage.

## Key Principles

- **An hour lost at the constraint is an hour lost for the whole system.** An hour lost elsewhere is recoverable.
- **Local optima are the enemy.** Making every stage busy maximizes WIP and queues, not throughput.
- **Evidence over consensus.** Every claim in this process gets a number or a falsifiable statement attached.
- **Focus beats effort.** One change at the constraint outperforms ten changes elsewhere.
- **Assumptions can be evaporated.** Most "impossible" trade-offs rest on an assumption nobody has stated out loud.
