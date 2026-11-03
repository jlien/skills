---
name: throughput-accounting
description: >
  Throughput Accounting — Goldratt's decision economics: Throughput (T),
  Inventory (I), Operating Expense (OE), and the global-focal-point questions
  ("how much more money will we make?"). Use to justify or reject any
  improvement, pricing, hiring, or make-vs-buy decision — especially elevate
  decisions from the Five Focusing Steps.
---

# Throughput Accounting Agent Skill

One-line summary: **score every decision by its effect on money generated (T), money stuck (I), and money spent (OE) — not by cost per unit, utilization, or local efficiency.**

## The Three Measurements

- **Throughput (T)** — revenue minus *totally variable costs* (costs that exist only when a unit is sold: materials, per-transaction fees). Not revenue alone; not gross margin with absorbed overhead.
- **Inventory (I)** — all money the system has invested in things it intends to sell: raw materials, WIP, finished goods. In a service organization, WIP is the work released but not delivered.
- **Operating Expense (OE)** — all money spent turning Inventory into Throughput: salaries, rent, tooling. Everything that isn't totally variable.

The system goal: **make more money, now and in the future.** The measurements exist to answer that, locally framed as: raise T, lower I, lower OE — with T first, because T is the only one with a ceiling and it grows the future, not just the present.

## The Two Worldviews

| | Cost World (traditional) | Throughput World (TOC) |
|---|---|---|
| Unit of success | cost per unit, utilization | system T, I, OE |
| Optimizes | every part | the whole, via the constraint |
| Typical move | "save 10% here" | "move 1 hour of constraint time to revenue work" |
| Failure mode | local wins, system flat | (correctly aimed) global wins |

Cost accounting is not *wrong* — it is blind to the constraint. A 10% OE cut on a non-constraint stage changes nothing in T; a 10% capacity gain at the constraint can double it.

## The Five Decision Questions

For any proposal, answer in order:

1. Does it **increase T**? By how much per month, against which constraint?
2. Does it **decrease I**? (Less WIP, less shelf, faster conversion.)
3. Does it **decrease OE**? With what lag or severance?
4. Does it **increase I**? (Beware: capacity investments raise I before they raise T.)
5. Does it **move constraint capacity** to (or from) revenue-generating work? An hour is priced at the constraint's rate, not the department's.

A proposal that fails all five is noise, however sensible it sounds.

## Decision Recipes

### Pricing and order acceptance
- An order at the constraint: price must exceed T per constraint-hour the order consumes *at the margin* — compare orders by T per constraint-hour, not gross margin.
- An order off the constraint (spare capacity exists): any price above totally variable cost adds T. Rejecting it because "we'd lose money per unit" is cost-world thinking throwing away real money.

### Make vs. buy
- Buying moves OE up and T potentially up (constraint time freed). Decide on the constraint-time freed × its T rate vs. the vendor cost — never on internal cost-per-unit parity.

### Elevate investments (hiring, tooling, infra)
- Project ΔT (constrained by what the *new* constraint will allow — elevating can create a different bottleneck) vs. ΔOE + ΔI. Approve only when ΔT dominates durably, and re-run `constraint-finder.md` after, because the constraint moves.

### Headcount
- Hiring at the constraint: near always positive (ΔT). Hiring at a non-constraint: raise OE with no T change until the constraint moves — justify as protective capacity or as preparation for a known constraint relocation, explicitly.

## Workflow

1. Get the decision on the table with its claimed benefit. Exit: benefit stated in one sentence.
2. Identify which constraint the decision touches. Exit: constraint named (or "none — flag: likely noise").
3. Answer the five questions with numbers, ranges accepted but no blanks. Exit: T/I/OE effects written down.
4. Compare against the do-nothing baseline over 3–12 months. Exit: delta stated.
5. Give the verdict with the weakest assumption named. Exit: "approve — assuming X" or "reject because Y" or "revise — the numbers depend on Z".

## Example

Constraint: deployment pipeline (2 weeks per release). Proposal: pay $2k/month for a faster CI tier (OE +$24k/yr).

- Cost-world view: "CI is a tooling expense; cut it."
- Throughput view: release latency is the constraint; cutting deploy time from 2 weeks to 2 days lets the team ship features a month earlier. If shipped features generate $15k/month in new T, ΔT is $180k/yr against ΔOE $24k/yr — approve, then re-identify the constraint.

## Pitfalls

- **Counting absorbed overhead in T.** T = revenue − totally variable costs. Adding allocated salaries into "margin per unit" reproduces the cost world with extra steps.
- **Treating OE cuts as throughput gains.** They only matter if they survive without breaking the constraint's support.
- **Ignoring the new constraint.** Every elevate projection must ask "and then what binds?" — the new bottleneck caps ΔT.
- **Precision theater.** Ranges with named assumptions beat false precision; the tool's job is to expose the weakest assumption, not to pretend it away.

## Collaboration Pattern

### With `five-focusing-steps.md`
Every elevate (step 4) ships with this agent's projection; exploits (step 2) get scored too when they shift constraint hours.

### With `CTO.md`
Budget decisions route here for the T/I/OE test before they reach the CTO agent for ratification.

### With `Product-Manager.md`
Backlog sequencing by contribution to Throughput (T per constraint-hour) instead of story points or effort estimates.

## Key Principles

- **Money generated beats money saved.** OE has a floor; T doesn't.
- **An hour at the constraint has a price.** Price decisions in constraint-hours.
- **Name the weakest assumption.** Every verdict carries its fragility in plain text.
- **Re-measure after every change.** The numbers that justified the last decision are stale for the next.
