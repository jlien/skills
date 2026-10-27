---
name: code-review
description: >
  Agent-era code review process, distilled from the Claude Code team's
  practice (claude.dev, Oct 2026). Layers of checks instead of one human
  gate: verify-before-review, AI review on every PR, blocking security
  review, risk-tiered human approval, and convergence rules that stop
  agent-author/agent-reviewer loops. Use when reviewing agent-written code,
  setting up a review pipeline, writing a REVIEW.md, or deciding which
  changes still need a human.
---

# Code Review (Agent Era)

One-line summary: treat "did a human read the code?" as a proxy for the real question — **what could go wrong with this change, and which check (automated or human) is the right one to catch it?**

Source: [How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/) (Addy Osmani, Morgan Westlee Lunt, Qing Wang; Oct 15, 2026). Their results: merged PRs more than doubled Jun–Sep while the share reverted fell 40%+.

## Code Review's Two Jobs

1. **Find and fix issues before they ship.**
2. **Build shared context across the team.**

Most of job 1 moves to machines. Job 2 is solved differently too: when someone needs to understand a slice of the codebase, have the agent write an explainer for exactly that slice (minutes, reflects today's code) instead of reading trivial diffs. A one-line copy change teaches nothing; an explainer of the module you're about to change teaches a lot.

## Review Continuously, Not as a Gate

Old flow: write code → open PR → wait for a colleague. New flow: review runs while the code is written, like spellcheck. Most changes have been reviewed **and fixed** at least once before a human is asked to look. This catches routine mistakes and saves human attention for higher-level questions.

## The Layered Model (Six Layers + Rollback)

Each layer catches some problems and misses others; few get through all of them.

```
1. Author verification      →  before anyone else looks
2. Required CI              →  lint, types, tests, build
3. AI review                →  every PR, diff vs whole repo + intent
4. Security review          →  separate pass, can block
5. Human approval           →  scaled by risk tier
6. Merge queue + flags      →  re-check vs latest main; gradual release
   └ Fast rollback          →  flags off without deploy; reverts in minutes
```

### Layer 1 — Verify Before Anyone Looks

Give the agent something it can **run** — tests, a build, a screenshot to compare against a design — and require it to **show the output instead of saying it's done**. Boris Cherny: giving Claude a way to verify its work is probably the most important thing for good results; he estimates it makes the result 2–3× better.

- Then a **subagent reviews the diff with fresh context** (no sunk-cost attachment to the code it just wrote).
- Run focused passes before opening the PR: one that hunts for bugs, one that simplifies the diff, one that checks behavior end to end.
- When the reviewer keeps flagging the same thing, **fix it at the source**: in the skill, as a lint rule, or in `CLAUDE.md`/`REVIEW.md` — not by re-explaining in each PR.

### `CLAUDE.md` and `REVIEW.md`

- **`CLAUDE.md`**: what the project is — stack, conventions, goals, non-goals. Keep it short in a large codebase; point to other docs from there. The reviewer flags code that breaks a convention in it *and* changes that make a line in it out of date.
- **`REVIEW.md`** (written by code owners): what matters in this part of the code. Good ones are short:
  - Say what **failure looks like** in this repo (for docs it's "it lies"; for config, "it misroutes").
  - **Cap the nits.** List paths to skip.
  - Demand **file and line as evidence**, not a guess from a name.
  - Summary **starts with a count** and says plainly when there's nothing to fix.

### Layer 3 — AI Review on Every PR

The reviewer reads the diff against the whole repo and the PR's stated intent, and asks: **does the change solve its problem, fit the system, or break something else?** On a bug fix, it hunts for the root cause, not the symptom.

Findings protocol:

- Several agents look for bugs **in parallel**; a separate group **votes** on each finding, and it only gets posted if enough agree it's real. (Cuts false positives hard — internal PRs getting substantive review comments went 16% → 54%.)
- Style-only, diagnostics, or cleanup findings are **dropped**.
- What survives posts as inline comments sorted by severity, each tagged:
  - **Important** — real bug, fix before merge
  - **Nit** — minor; batch or skip
  - **Pre-existing** — not introduced by this PR (so it doesn't read as the author's fault)
- **Every finding must be answered**: fix it, or resolve the thread with a short reason (that's how you clear a false positive).
- Match depth to stakes: Quick / Standard / Deep. Deep is worth it where one missed bug costs more than the extra review time.

### Layer 4 — Security Review That Can Block

A PR **cannot merge** while any bug-review or security-review finding is open. Fix it or close the thread with a written reason. If a later commit fixes the issue, the finding clears on its own.

### Layer 5 — Human Approval, Scaled by Risk

The **change sets the tier, not the author**. A classifier reads the change; some paths always need a person (anything code owners marked sensitive, any CI workflow file).

| Tier | Examples | Human approvals |
|---|---|---|
| Low | Docs, copy, internal-only features, additive changes behind a flag | None — automated review + security green is enough |
| Medium | Ordinary product changes; sensitive areas (caching, auto-updater, prompts) | One person |
| High | Highest-risk code; designated always-two-people paths | Two people |

- Only **trusted authors** get the lighter paths; everyone else needs a second approval.
- **An agent's approval never counts as a person's.** Automated review can clear a low-risk change, but it can't fill a slot that calls for a human.
- On an agent-written PR, the **person directing the agent counts as a required reviewer** — same as if they'd typed the code.
- An approval covers **one specific commit**; new commits the system can't vouch for require re-approval.

### Layers 6–7 — Merge Queue, Flags, Rollback

- Merge queue re-runs checks against latest main, so two PRs that pass separately can't combine into a broken main.
- New behavior ships behind a flag; internal use surfaces regressions before users do. Latest channel first, stable trails.
- Last layer is speed of recovery: flags turn off without a deploy, broken builds get reverted. Incident reviews ask *which layer should have caught it*.

## Convergence Rules (Break the Agent Loop)

An agent author and an agent reviewer can keep each other busy forever — one PR went 50+ rounds overnight. And when they measured, ~59% of what the reviewer kept flagging was code that had been there since the first pass: it was finding *old* bugs, not new ones.

- **Round cap.** After 3 rounds, stop and reconsider the approach — not another pass.
- **Diff-only re-review** after the first few passes.
- **Flag the class of bug**, so the author fixes every instance, not one line.
- **No repeats** of findings already posted.
- Track **rounds-to-pass** alongside recall. Noise costs more when the author is an agent: a person waves off a nit in seconds; an agent fixes it, which means another commit and another round.
- Priority, in writing: **catching real bugs first, cutting review rounds second.**

## Where Humans Stay in the Loop

Pulling a senior engineer out of deep work to catch a routine mistake costs more than the automated review. Humans decide the things machines are bad at:

1. **Should we build this at all?** Direction, taste, scope.
2. **Risky code** — billing, auth, auto-updaters, CI workflows.
3. **Architecture** that sets a pattern others will copy.
4. **Reading the evidence** — test output, what ran and what it returned. If you can't say what the checks would miss, ask for a real review, not a quick approval.
5. **Owning the outcome.** A person is accountable for every change that ships, whoever typed it.

"You land it, you own it": land a change, and when something breaks you fix it — you have the most context. Not blame; incident reviews look at the system. This works because changes are small, everything is reversible, and blast radius sets the bar for how many checks a change gets.

## Make the Reviewer Better Over Time

- **Incidents are the eval.** Collect past PRs that caused incidents/reverts, have experts confirm each bug, and score the reviewer against that set. Every incident adds a case. Rescore whenever prompts, tools, or the model change — keep the change only if the score went up.
- **Measure noise** by what people do with the comments: fixed / said it was wrong / said intentional / didn't matter. Also run the reviewer on known-clean PRs and count harmful-change reports.

## PR Template Fields

Ask on every PR — the agent can fill it in, but the person who asked for the change signs off:

- **Testing** — how the change was tested
- **Risk** — which tier, and why
- **How to revert** — the one-step undo

## Decision Framework

- Routine mistake (style, missing guard, N+1)? → automated layer catches it; don't spend human attention.
- Does the change solve its stated problem? → AI review layer.
- Could it lose money, data, or trust? → security review + human, minimum Medium tier.
- Sets a pattern others will copy? → architecture review by a senior engineer.
- Loop running past 3 rounds? → stop, reconsider approach.

## Collaboration

- `ruby-on-rails/SKILL.md` invokes the Rails-specific checklist in `ruby-on-rails/code-review.md` automatically after implementation — those five skills (smells → performance → security → readability → modularity) are the *content* of a review; this skill is the *process* around it.
- `llm-as-a-verifier` ranks candidate implementations when several fixes compete.

## Key Principles

- Review is a **routing question**, not a reading chore: match each risk to the cheapest check that catches it.
- **Verify with runnable evidence**; never accept "it's done" without output.
- **Findings need evidence** (file:line) and a **response** (fix or reasoned resolve) — nothing open at merge.
- **Converge or stop**: cap rounds, re-review diffs only, fix bug classes.
- **Risk scales review, not seniority or asking.** Change sets the tier.
- Optimize for **minimum human review time that doesn't raise reverts** — measure both.
