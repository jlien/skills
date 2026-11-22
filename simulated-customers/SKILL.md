---
name: simulated-customers
description: >
  Pre-test a product idea, price, or piece of copy with simulated customer
  personas before spending anything on market research. Role-play ONE specific
  person (age, income, context), show them the artifact verbatim, and collect
  their unfiltered written reaction — never ask the model to "rate this 1-5",
  which returns a useless lukewarm middle. Convert the written reaction to
  intent in a separate pass (Semantic Similarity Rating). Validated against 57
  real surveys and 9,300 human responses (arXiv 2510.08338): virtual customers
  reached ~90% of real test-retest reliability and reproduced price sensitivity
  by age and income. Use when you need to know whether a persona would buy,
  what would stop them, and what price they'd accept — overnight, for free.
---

# Simulated Customers

One-line summary: **ask the model to BE the customer and write unfiltered; never ask it to grade itself.** The written reaction carries the signal; a second pass converts it to intent.

Source: [Paul Young's post on X](https://x.com/PaulYoungX/status/2124424175980810549) summarizing the Semantic Similarity Rating (SSR) paper, [arXiv 2510.08338](https://arxiv.org/pdf/2510.08338).

## Why a 1-5 rating fails

Ask a model "rate this product 1 to 5" and it returns a lukewarm middle every time — the answer predicts nothing. The paper's fix: don't request a number from the persona at all. Give it a persona, show the product idea, and ask what it honestly thinks. Then a separate tool pass converts the written opinion into a rating. Generation and scoring stay decoupled.

## Core Responsibilities

- Write **one person, not a segment**: age, income, context (what they use today, who they buy for), and one live constraint (time, budget, skill, skepticism). "41, $85k household, buys for a 12-year-old's club team, works full time" beats "parents aged 35-50".
- Show the **artifact verbatim** — the real copy, real price, real screen text. A persona fed a summary will react to the summary, not the product.
- Ask for the **unfiltered written reaction in first person**. No rating scale in the prompt. Good asks: "What would stop you from doing this?" "Read this out loud to your spouse." "What question would you type before clicking?"
- **Convert, don't grade**: a separate pass maps the written reaction to intent (would do it now / would ask a question first / would not) or compares it to anchored statements. The persona never scores itself.
- Run **3-10 personas across deliberate age and income bands** — the paper reproduced real price sensitivity along exactly those axes.
- Aggregate **blockers, not scores**: count distinct objections and how many personas hit each. One objection every persona raises beats ten lukewarm ratings.

## Validation (why this replaces the first survey round)

Compared against 57 real product surveys with 9,300 human answers:

- Virtual customers reached **~90% of real test-retest reliability** (humans don't even agree with themselves 100% when asked twice).
- They reproduced **price reaction by age and income**.
- Their written feedback was **more detailed and more critical** than real humans'.

That last point cuts both ways — see caveats.

## Caveats

- Virtual customers skew **harsher and wordier** than real ones. Treat output as a stress test for objections, not a demand forecast. Never quote a "72% would buy" number from a simulation.
- A persona only knows what you tell it. Feed real copy and real numbers, or it invents plausible ones and reacts to your fiction.
- Simulation replaces the **first** research round, not the customer. When an objection would change what you build, confirm it with one real conversation before big spend.

## Decision framework

| Situation | Use |
|---|---|
| Rank landing-page pitches, prices, or onboarding copy before shipping | Simulated customers — 3-10 personas, one night, free |
| Find every objection a persona class could raise | Simulated customers with the artifact verbatim |
| Does the flow *work* (can they finish it)? | `launch-qa` — simulated first-time users in a real browser |
| The objection would change what gets built and being wrong is expensive | One real customer conversation after simulating |
| Convert written reactions to a ranked score at scale | `llm-as-a-verifier` — same move: continuous signal from text, not self-reported integers |

## Workflow

1. Draft the persona file (age, income, context, constraint) and the artifact (copy, price, screen text) verbatim.
2. One agent per persona, in character, produces the unfiltered written reaction. Parallelize.
3. A second pass (different context, no persona) converts each reaction to intent and extracts the objection list.
4. Merge: objections ranked by how many personas hit each. Fix copy in one pass.
5. Rerun the personas that hit the top objection to confirm it's gone.

## Relationship to other skills

- `launch-qa` tests whether the flow **works**; this tests whether the persona would **want it** and at what price. Run both before a launch: launch-qa finds where they get stuck, simulated customers find why they'd leave even if nothing is broken.
- `llm-as-a-verifier` is the scoring pattern this relies on: derive the signal from the text, never from the generator's self-assessment.
