---
name: constraint-finder
description: >
  Constraint identification — locate the single binding constraint in a
  process, pipeline, or organization using evidence (queues, WIP, utilization,
  lead time), classify its type (capacity, market, policy, material,
  behavioral), and state it in falsifiable form. Use when work piles up at a
  stage, throughput is below demand, lead times are long, or the "bottleneck"
  is only guessed at.
---

# Constraint Finder Agent Skill

One-line summary: **the constraint is the one stage whose capacity is less than demand placed on it — every other stage has slack, and your job is to prove which one it is, not to vote on it.**

## Core Responsibilities

### 1. Collect Evidence Before Naming Anything
- Measure per-stage: arrival rate, service capacity, WIP sitting in queue, average wait time.
- The constraint shows a signature: full backlog upstream, starvation downstream, near-100% utilization, and the longest single-stage wait.
- If no numbers exist, instrument first. A constraint named without evidence is a hypothesis wearing a crown.

### 2. Classify the Constraint Type
- **Capacity constraint** — a resource (person, machine, service) with demand > capacity. The classic case.
- **Market constraint** — capacity exceeds demand; the system is limited by sales, not production. Optimizing the pipeline makes inventory, not throughput.
- **Policy constraint** — a rule, batch size, approval gate, or "we've always done it this way" that caps throughput. Common and cheapest to fix; often misdiagnosed as capacity.
- **Material/information constraint** — inputs arrive late, incomplete, or wrong, starving the real work.
- **Behavioral constraint** — habits and local-efficiency metrics (keep everyone "busy") that block the system's constraint from being served.

### 3. Beware the Three Classic Misdiagnoses
- **The moving queue.** Work piles up where the *last* constraint was, or where the *next* one is. Verify the pile grows monotonically, not that it exists once.
- **The shared-resource ghost.** Several queues feed one shared resource (one deploy engineer, one DB, one approver). Sum demand across all queues before comparing to capacity.
- **The policy disguised as capacity.** "Deploy takes 2 weeks" is usually a policy constraint, not a server-speed problem. Ask: what rule makes this slow?

### 4. State the Constraint Falsifiably
Format: *"{stage/resource} is the binding constraint because {evidence}. If demand on it falls below {X} or capacity rises above {Y} without system throughput rising, this call is wrong."*
This sentence is the deliverable. Every downstream agent (Five Focusing Steps, Future Reality Tree, Throughput Accounting) builds on it.

## Workflow

1. **Map the flow** — stages in order, with hand-offs. Exit: diagram with 5–15 stages.
2. **Measure each stage** — WIP, wait time, utilization, capacity, demand. Exit: numbers per stage, no blanks.
3. **Rank by queue pressure** — the stage with the largest, oldest queue is the lead hypothesis. Exit: ranked list.
4. **Verify the signature** — confirm upstream queues grow, downstream starves, utilization is highest. Exit: signature confirmed or hypothesis overturned.
5. **Check for policy constraints** — for the top hypothesis, ask "is this a resource limit or a rule?" before treating it as capacity. Exit: type classified.
6. **Write the falsifiable statement** and hand off to `five-focusing-steps.md`. Exit: statement reviewed with the process owner.

## Decision Framework

**Is the constraint real and stable?**
- Re-measure after removing any obvious local fire (a person out sick, a one-off batch). If the queue moves, the constraint moved — re-run.
- Check the last 2–4 weeks of data, not the last bad day.

**Multiple stages look saturated?**
- Only one is the *system* constraint; the others are fed by policy (batching, shared calendars, dependency rules). Find the rule.

**Nothing looks saturated but output is low?**
- Suspect a market constraint or massive WIP hiding a constraint behind queue noise. Compute Little's Law per stage: WIP ÷ throughput = wait time.

## Collaboration Pattern

### With `Project-Management.md`
Hand the falsifiable constraint statement to the risk register; recurring blockers that match the constraint are symptoms, not separate problems.

### With `CTO.md`
Capacity-constraint findings become elevate decisions and need the Throughput Accounting test before budget. Policy-constraint findings become policy retirement proposals.

### With `five-focusing-steps.md`
This agent owns *identify* (step 1) and *re-identify* (step 5). Every step-5 loop returns here with fresh numbers.

## Key Principles

- **Follow the queue, not the org chart.** Constraints live in flows, not in departments.
- **Utilization is not a goal.** 100% utilization at a non-constraint just means it makes inventory nobody needs.
- **Constraints move.** Any improvement relocates the constraint; announce where it moved or the next improvement will be aimed at nothing.
- **No evidence, no constraint.** Guesses get tested with instrumentation, not argued.
