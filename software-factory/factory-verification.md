---
name: factory-verification
description: >
  Verification and review gates for a software factory — lint/type/test as
  plain code before any model reviews, CI as the judge, tests written from
  acceptance criteria rather than the agent's own code, a review agent that
  must quote the line it flags, and autonomy earned per repo by metrics.
  Use when setting up review gates for agent-written PRs or deciding how
  much autonomy the factory has earned.
---

# Factory Verification & Review

One-line summary: **CI is the judge — the agent's claim that "all tests pass" is not evidence of anything.**

Credit: checklist from [Mar deHaym's post on X](https://x.com/mardehaym/status/2125319432432157152). This is the detailed layer under part #7 of the `software-factory/SKILL.md` architecture.

## The Checklist

- linting, type-checking, and tests running as plain code before any model reviews a line
- CI acting as the judge, never trusting the agent's own claim that "all tests pass"
- tests written from the acceptance criteria, not generated from the agent's own code, so it isn't grading its own homework
- a review agent forced to quote the exact line it's flagging, or the comment gets dropped
- deterministic rules around the model written as unit-testable code
- a cap of five review comments, security first and style last, because nobody is reading forty
- memory of past dismissals, so a finding an engineer already rejected doesn't pop right back up on the next PR
- pull requests small enough for a human to review before lunch
- draft pull requests by default
- autonomy earned repo by repo based on your own metrics, where a single revert knocks it back down a tier
- first-pass CI rate, merged-unchanged rate, and revert rate tracked for every repo

## Conventions That Carry the Value

- **Deterministic first, model second.** Lint, types, and tests run as plain code; the model only sees what survived them.
- **Tests come from the ticket, not the diff.** Generated-from-your-own-code tests are the agent grading its own homework.
- **Every review finding quotes a line.** No quote, no comment. Findings are capped at five, security first, style last.
- **Dismissals are remembered.** A rejected finding does not return on the next PR — otherwise reviewers stop trusting the stream.
- **PRs are small and draft by default.** Reviewable before lunch; promoted only when ready.
- **Autonomy is earned per repo and reversible.** Metrics (first-pass CI, merged-unchanged, revert rate) set the tier; one revert knocks it back down.

## Decision Framework

- **Who decides the work passed?** CI. The agent's self-report carries no weight.
- **How much autonomy?** Whatever the repo's own metrics have earned — and a revert resets it.
- **A review agent finds something.** It must quote the exact line, or the finding is dropped.

## Cross-References

- `SKILL.md` — part #7 (gates).
- `code-review/SKILL.md` — the layered review process this plugs into.
- `factory-intake.md` — the acceptance criteria the tests are written from.
- `factory-security.md` — the deleted-test guard and protected files.
