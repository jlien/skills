---
name: factory-evals
description: >
  Evals and prompt management for a software factory — prompts stored in git,
  a golden set of tickets rerun on every model/prompt/tool change, an eval
  suite that blocks the change on any failure, and ugly-case coverage (data
  in logs, .env commits, delete-only diffs, injections). Use when changing a
  model, prompt, or tool, or when eval scores tank after a provider update.
---

# Factory Evals & Prompts

One-line summary: **a prompt change ships like a code change: reviewed in git, graded against a golden set, and blocked if even one case fails.**

Credit: checklist from [Mar deHaym's post on X](https://x.com/mardehaym/status/2125319432432157152). This is the detailed layer under part #8 of the `software-factory/SKILL.md` architecture.

## The Checklist

- prompts stored in git and reviewed like production code
- a golden set of tickets with known answers, rerun whenever you tweak a model, prompt, or tool
- an eval suite that blocks the change if even one case fails
- evals specifically testing the ugly stuff: patient data in logs, committed .env files, delete-only diffs, prompt injections
- evals written by your own engineers, rather than a vendor's cherry-picked demo set
- a prompt version stamped on every run, so you can trace which one opened the bad PR
- a playbook for the Thursday your model provider ships a silent update and your eval scores tank

## Conventions That Carry the Value

- **Prompts are production code.** Stored in git, reviewed like anything else, rollback as fast as code.
- **Any tweak reruns the golden set.** Model, prompt, or tool — no exceptions, no "it's just a small change".
- **One failure blocks the ship.** Not a warning; a block.
- **Test the ugly stuff on purpose.** Patient data in logs, committed .env files, delete-only diffs, prompt injections — the failures nobody demos.
- **Your engineers write the evals.** A vendor's demo set measures the vendor.
- **Every run is stamped with its prompt version.** The bad PR traces back to the exact prompt that opened it.
- **The silent-update playbook exists in advance.** Provider ships a change, scores tank, you notice because evals run — then you follow the playbook instead of improvising.

## Decision Framework

- **Did the model/prompt/tool change?** Then the golden set reruns before anything ships.
- **Where did the bad PR come from?** The prompt version stamped on the run.
- **Scores dropped with no deploy?** Assume a provider-side update; run the playbook.

## Cross-References

- `SKILL.md` — part #8 (evals).
- `factory-verification.md` — CI as judge; evals are the same principle applied to prompts.
- `factory-observability.md` — traces and run history that make the prompt-version stamp queryable.
