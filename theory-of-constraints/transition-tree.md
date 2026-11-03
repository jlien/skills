---
name: transition-tree
description: >
  Transition Tree — Goldratt's implementation-logic tool: convert an agreed
  injection into an ordered plan by starting from the desired near-term effect
  and asking what blocks it, what action clears the block, and what that
  action needs. Use when a validated fix exists but the plan is vague, when
  execution stalls on unnamed obstacles, or when a big change needs staging.
---

# Transition Tree Agent Skill

One-line summary: **plan backwards from the first concrete effect you want, forward through each obstacle — a transition plan with no named obstacles is a wish with a date.**

## When to Use

- The injection is agreed (survived `future-reality-tree.md`) and now needs an executable sequence.
- An implementation keeps stalling; the plan exists but nobody can say which obstacle is blocking.
- A change must be staged (trial group, shadow mode, phase-in) rather than switched on.

## Core Concepts

- **The near-term goal** — the first *effect* you want in reality, not the action. "Deploys run weekly" not "set up CI". Keep the first tree small: one goal the tree can fully cover.
- **Obstacle** — a specific, current, real reason the goal is not already true. Not risks, not fears — facts about today that stand in the way.
- **Action** — what clears a specific obstacle. Every action maps to ≥1 obstacle, or it's decoration.
- **Intermediate goal** — an effect an action needs but that isn't yet true; it becomes the next tree's goal. This is how the tree chains from here to the full injection.

## Workflow

1. **State the near-term goal as an effect.** Exit: one checkable sentence, 2–6 weeks out.
2. **List obstacles.** For each, ask "why isn't this already true?" until the answer is a fact, not a reason. Exit: 3–7 obstacles, each specific.
3. **Attach an action to each obstacle.** An action that clears no listed obstacle gets deleted. Exit: obstacle→action map.
4. **Check actions against reality.** Does the actor have authority, resources, time? Mark what's missing. Exit: each action marked ready / needs-resource / needs-decision.
5. **Sequence by dependency, not preference.** Which action's output another action's input. Exit: ordered plan where no step waits on an unlisted predecessor.
6. **Extract intermediate goals.** Every "needs-resource" or "needs-decision" action becomes the next tree's goal with its own obstacle list. Exit: chain of trees from here to the injection, each tree small and executable.
7. **Set checkpoints.** Each tree gets its verification signal and date. Exit: the plan reads as: goal → obstacles → actions → next goal.

## Decision Framework

**Action has no obstacle?** Delete it. The strongest sign of a bad plan is a step nobody can tie to a blocker.

**Obstacle is actually a person?** Rewrite as the fact blocking them: "the compliance team requires X form" not "compliance is stubborn". Facts get worked; labels get resented.

**Too many obstacles for one tree?** The near-term goal is too far out. Halve the horizon and re-run — the tree works in 2–6 week spans.

**Staging decision:** trial first when the negative branch from `future-reality-tree.md` involves people who could be harmed by a full switch; the trial is itself a trim.

## Example

Injection: move manual regression testing into CI.

- **Goal (tree 1):** the top 20 regression paths run automatically on every PR.
- **Obstacles:** no one owns the suite; top paths aren't written down; CI time budget unknown; flaky tests would block merges.
- **Actions:** appoint suite owner (clears #1); record the 20 paths from the manual checklist (clears #2); measure current CI cycle time and set the budget (clears #3); quarantine flag for flaky tests pending fix (clears #4).
- **Intermediate goal from #1:** "owner role exists with time allocated" → becomes tree 2's goal: obstacles — manager hasn't approved capacity; no job description update.
- **Checkpoints:** PR suite green on all 20 paths by date X; zero flaky-blocked merges in first two weeks.

## Pitfalls

- **Planning the action instead of the effect.** "Hold a workshop" is an action; "suite ownership decided" is the goal. State goals as states of the world.
- **Vague obstacles.** "Resistance to change" is not an obstacle until it names whose, to what, because of what.
- **The invisible dependency.** Two actions share an unspoken prerequisite (a decision, a credential, a maintenance window). Step 5's dependency check exists for exactly this.
- **Never chaining to the next tree.** A transition plan that ends at "needs decision" with no tree 2 is a dead end, not a plan.

## Collaboration Pattern

### With `five-focusing-steps.md`
Elevate decisions become transition trees: the investment is the goal, approvals and hiring steps are obstacles with actions.

### With `Project-Management.md`
The obstacle→action maps slot directly into the backlog as tasks with checkable exits; the tree chain becomes the milestone sequence.

### With `CTO.md`
"Needs-decision" intermediate goals route to the CTO agent with the FRT evidence attached — decisions arrive with logic, not just asks.

## Key Principles

- **No named obstacle, no action.** Activity without a blocker is motion, not progress.
- **Small trees chain far.** A 2-week tree you finish beats a quarter-long tree you polish.
- **Sequence by dependency.** Dates follow the causal order; the causal order does not follow dates.
