---
name: ai-transformation
description: >
  AI-native transformation playbook for PE-backed companies — the order that
  works: people first, then data, then one workflow at a time. Use when a
  portfolio company or team wants to "go AI-native", when evaluating an AI
  adoption plan, when pilots are multiplying without production, or when an
  agent rollout needs governance (gateway, budget, kill switch, golden set).
---

# AI Transformation Playbook

One-line summary: **skip the boring half and you end up with 40 pilots and nothing in production.**

The companies that get AI-native do it in this order: people, data, workflows, guardrails, engineering. The phases are sequenced on purpose — workflows can't move until data agrees with itself, and nothing ships until a person approves it.

## Phase 1 — The People

1. Give everyone a paid AI seat, with a budget per team so the bill doesn't surprise your CFO.
2. Find the 5 people already using it every day. They teach everyone else.
3. Ask every team lead to write down the 10 most boring tasks their team does each week.
4. Sit with your best people and write down how they do the job. If it only lives in their head, an agent can't do it.

## Phase 2 — The Data

1. List every system you run. After a few acquisitions it's usually a zoo, with Excel holding it together.
2. Pick one source of truth for revenue, customers and headcount. Agents can't fix numbers that disagree.
3. Give agents read access first. Write access gets earned, same as a new hire.

## Phase 3 — The Workflows

1. Put a dollar number next to each boring task. Hours saved only count if somebody spends them on something else.
2. Pick one workflow, with one owner and one number you want to move.
3. Put every fixed rule in plain code. The model only handles the judgment calls.
4. Build a golden set: 100 past cases your best people already judged.
5. Run it in shadow mode next to your team for a few weeks and read every disagreement.
6. The agent prepares, a person approves. Anything touching money or customers waits for a human.
7. Ship it in weeks. If it takes a quarter, the scope is wrong.

## Phase 4 — The Guardrails

1. Every model call goes through one gateway, with logs and a budget.
2. Keep a kill switch, and test it.
3. Re-run the golden set every time the model changes.

## Phase 5 — The Engineering Team

1. Small teams ship. Two or three engineers with agents and one tech lead reviewing everything.
2. Every pull request goes through the same checks, whoever or whatever wrote it.
3. Measure AI spend against what shipped to customers.

## The Part Nobody Wants to Hear

1. Never vibe-code your ERP or your billing.
2. Finish one workflow properly before you start the next five.

## Decision Framework

- **Where to start?** Phase 1 step 3 — the boring-task lists. Not the model, not the vendor.
- **Which workflow first?** The one with a dollar number, one owner, and no money-or-customer write access.
- **Is it safe to expand?** Only after the golden set passes on the current model and the kill switch has been tested.
- **Is the program working?** AI spend shipped-to-customers, not pilots started.

## Collaboration With the Other Skills

- `code-review/SKILL.md` — Phase 5's "every PR goes through the same checks" is that skill's process applied to agent-authored code.
- `CTO.md` — the technical-strategy owner for this playbook's build-vs-buy and gateway decisions.
- `theory-of-constraints/SKILL.md` — Phase 3's dollar-per-task sizing is a throughput question: find the constraint before automating around it.
