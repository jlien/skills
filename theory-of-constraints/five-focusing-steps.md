---
name: five-focusing-steps
description: >
  The Five Focusing Steps — Goldratt's operational loop for any known
  constraint: Identify, Exploit, Subordinate, Elevate, Repeat. Decides whether
  a constraint fix needs zero or full capital, keeps non-constraint stages
  serving the constraint, and guards against inertia. Use after the constraint
  is identified and evidence-backed.
---

# Five Focusing Steps Agent Skill

One-line summary: **exploit the constraint with what you already have before spending a dime; everything else in the system must subordinate to that decision.**

Prerequisite: a falsifiable constraint statement from `constraint-finder.md`. If the constraint is only guessed at, stop and go back.

## The Five Steps

### 1. Identify
Already done by `constraint-finder.md`. Your job here is to keep it current — the constraint moves after any improvement.

### 2. Exploit (get more from the constraint with existing resources)
- Remove wasted constraint minutes: work that arrives broken and bounces back, context switching, waiting on a decision, rework.
- Ensure the constraint only does what only it can do — offload everything else, even if offloading is "inefficient" for the receiving resource.
- Use constraint off-time: schedule breaks, maintenance, and variability absorption *outside* the constraint's working time.
- **Exploit costs nothing.** If your proposed exploit needs a purchase, it is an elevate step wearing a cheaper hat.

### 3. Subordinate (make everything else serve the constraint)
- Non-constraint stages must throttle to the constraint's pace: releasing more work just builds queues (WIP) without adding throughput.
- Kill local-efficiency metrics that push non-constraint stages to "stay busy" — busyness there is inventory, not progress.
- Protective capacity: non-constraints need *some* slack so the constraint never waits for them. Subordination is not starving them; it is pacing them.
- This step is usually the hardest and most resisted, because it makes good resources look idle. Pre-decide the metric that replaces "busy": constraint output.

### 4. Elevate (invest in more constraint capacity)
- Only after exploit and subordination have been squeezed. Sequence matters: elevating first wastes capital on capacity the system can't feed or use.
- Every elevation passes the `throughput-accounting.md` test: does projected Throughput gain exceed Operating Expense change?
- Cheapest elevations first: a second shift, cross-training one person, automating one manual step — before re-platforming anything.

### 5. Repeat (and guard against inertia)
- After every change, re-run `constraint-finder.md`. The constraint *will* move.
- **Inertia warning:** the policy, batch size, or buffer that fixed constraint #1 becomes the policy constraint for #2. In the repeat step, explicitly list what should now be *undone*.

## Workflow

1. Read the constraint statement. Exit: type and evidence understood.
2. Brainstorm exploit actions; sort by constraint-minutes recovered. Exit: top 3 exploits with estimates.
3. Implement the top exploit. Exit: measured constraint output change.
4. Define subordination rules (release pacing, WIP caps, priority). Exit: rules written and followed for 2 weeks.
5. Only if constraint still binds: elevate, cheapest first, with T/I/OE projection. Exit: accounting test passed.
6. Re-identify the constraint. Exit: new falsifiable statement or confirmation the old one still holds.
7. Record what to undo from the previous cycle. Exit: undo list created.

## Example

System: content team. Constraint: the editor (only person who can publish).

- **Exploit:** writers deliver drafts against the style guide so the editor stops rewriting from scratch — editor handles 8 → 12 pieces/week with the same hours.
- **Subordinate:** release work in a pull queue capped at the editor's new capacity; writers stop "keeping busy" by stockpiling drafts the editor can never clear.
- **Elevate:** only after exploit plateaus — train a second editor part-time, justified by projected Throughput gain, not "the team is busy".
- **Repeat:** re-measure. The constraint moves to the writers' research step — and the old rule "every piece must pass through the editor's morning slot" is now a policy constraint to retire.

## Collaboration Pattern

### With `Project-Management.md`
Subordination rules change what tasks get released and when — coordinate so the backlog sequence reflects constraint pacing, not story ordering habits.

### With `Product-Manager.md`
When the constraint is the market, exploit means better targeting and offers, not more pipeline features.

### With `throughput-accounting.md`
Every elevate decision ships with its T/I/OE projection. No projection, no elevation.

## Key Principles

- **Exploit before elevate.** Free capacity first; bought capacity second.
- **Subordination is where the gain actually lands.** An exploited constraint fed by a non-subordinated system just grows queues.
- **Don't fear idle non-constraints.** Idle capacity elsewhere is the price of a constraint that never waits.
- **Inertia is step 5's real content.** The most dangerous constraint is last quarter's fix.
