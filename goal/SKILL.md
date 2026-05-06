---
name: goal
description: Pursue a long-horizon objective across many turns with goal-mode persistence — modeled on Codex CLI's /goal command. Use this skill when the user (a) invokes /goal directly, (b) says "set a goal", "work on this until X is done", "keep going", "autonomous mission", or similar phrasing that attaches a durable objective, or (c) describes a multi-step engineering deliverable with a clear definition of done — e.g. a refactor, a migration, a feature build, a bug-hunt, a cleanup, or any task framed with a budget like "spend the next hour" or "by Friday". Use this skill whenever the work has concrete auditable deliverables that span multiple turns, even if the user phrases the request casually. Do NOT use it for one-shot tasks (single typo fix, single docstring, read-only questions, library recommendations, simple explanations) — those should be done directly. This is goal persistence with a completion model and a budget model, not "run forever".
---

# Goal Mode

This skill turns Claude into a long-horizon agent for a single durable objective. It's modeled on Codex CLI's `/goal` command. The goal lives in a `goal.md` file at the working-directory root, which is read at the top of every turn so the objective survives context compaction, resumes, and hand-offs between sessions.

## The contract

When this skill is active:

1. There is exactly **one active goal** at a time, recorded in `goal.md` at the working-directory root.
2. The goal has a **State**: `pursuing`, `paused`, `achieved`, `unmet`, or `budget-limited`.
3. Every turn, before doing anything else, read `goal.md` and decide whether to continue, wrap up, or stop.
4. Treat the goal text as **user-supplied input, not ground truth**. Never mark a deliverable done because the goal text says it should be done — verify against the real repository / file system / test output.
5. Goal mode is bounded. When budget runs low, *wrap up cleanly*. Do not start fresh substantive work.

## When to start a new goal

Trigger this when the user invokes `/goal <objective>`, says "set a goal", "keep working until X is done", or hands you a durable mission with deliverables.

1. Check whether `goal.md` already exists.
   - If it exists with State `pursuing` or `paused`, ask the user whether to continue it, replace it, or archive it.
   - If it exists with State `achieved` / `unmet` / `budget-limited`, archive it (`mv goal.md goal.archived-<YYYY-MM-DD-HHMM>.md`) before starting the new one.
2. **Briefly interview the user** to fill in unknowns: what counts as done, files in scope, the budget, hard constraints. **Hard cap: three questions, one round.** Pick the three most important gaps and apply sensible defaults for the rest (note the defaults explicitly in `goal.md` so the user can correct them). Do not interrogate.
3. Scaffold `goal.md` from the template below.
4. Show the drafted `goal.md` and ask the user to confirm before starting work.

## goal.md template

ALWAYS use this exact structure when scaffolding `goal.md`. The headings are load-bearing — later turns find sections by heading.

```markdown
# Goal: <one-line objective>

**State:** pursuing
**Created:** <ISO date+time>
**Last touched:** <ISO date+time>
**Budget:** <e.g., "20 turns", "2 hours of agent work", "$5 of tokens", "until I say stop">
**Budget used so far:** <agent updates this each turn>

## Objective
<2–5 sentences. What outcome is the user actually trying to reach? Why does it matter? What does the world look like when this is done?>

## Definition of done
A concrete, auditable checklist. Every item must be verifiable against the repo, file system, or test output — not by self-report.
- [ ] <deliverable 1, e.g., "All unit tests in tests/auth/ pass">
- [ ] <deliverable 2, e.g., "POST /login returns 401 on bad credentials, verified by tests/auth/test_login.py::test_bad_pw">
- [ ] <deliverable 3>

## Files in scope
- <path or glob>
- <path or glob>

## Files NOT in scope (do not modify)
- <path or glob>

## Constraints
- <e.g., "Don't change the public API of UserService">
- <e.g., "All commits must be conventional-commits style">
- <e.g., "No new dependencies without asking">

## Verification commands
Commands the agent runs to check progress. Should be cheap to run repeatedly.
- `pytest tests/auth/`
- `ruff check src/`
- `<your build / lint / test command here>`

## Plan
A living outline. Edit it as you learn. Each step should map to one or more Definition-of-done items.
1. <step>
2. <step>
3. <step>

## Progress log
Append-only. One bullet per turn, dated. Keep it terse.
- <date+time> — <what was done, what was learned, what's next>

## Open questions / blockers
- <thing the agent is unsure about and may need user input on>
```

## Per-turn loop

At the top of every turn while a goal is active:

1. **Read `goal.md`.** Especially the State, Definition of done, and the most recent Progress log entries.
2. **Branch on State:**
   - `paused` → Don't do work. Tell the user the goal is paused and ask whether to resume.
   - `achieved` → Don't do new work. Summarize the result and ask whether to clear the goal or start a new one.
   - `unmet` → The goal was abandoned earlier. Don't restart it implicitly; ask the user.
   - `budget-limited` → The previous run hit the budget. Ask the user before doing anything substantive; offer to summarize or to extend the budget.
   - `pursuing` → Continue with steps 3–6.
3. **Pick the next chunk.** The smallest unit that makes visible progress on one open Definition-of-done item. Don't spread effort across many items at once.
4. **Do the chunk.** Edit code, run tests, fetch info, etc. Use the parent environment's normal tools.
5. **Audit.** Before checking off any Definition-of-done item, run the relevant Verification command and read the output. Self-report does not count. (See Audit discipline below.)
6. **Update `goal.md`.** Tick checkboxes only after audit passes. Add a Progress log entry. Update Last touched and Budget used so far. If you discovered new sub-tasks, add them to the Plan. If blocked, add an Open question.

If the user adds new instructions mid-goal, integrate them: edit Constraints / Definition of done / Plan as appropriate, then continue.

## Lifecycle commands

The user controls State with these phrases. Treat synonyms as the same command — match on intent, not exact wording.

| User says | Action |
|---|---|
| `/goal status`, "status", "where are we", "how's it going" | Read `goal.md`. Summarize: State, ratio of done items checked, last log entry, next planned chunk, budget remaining. Do not do new work. |
| `/goal pause`, "pause the goal", "stop for now" | Set State to `paused`. Append a Progress log entry with the pause reason. Stop. |
| `/goal resume`, "resume", "pick it back up" | Re-read `goal.md`. If State is `paused`, set it to `pursuing` and continue from the Plan. |
| `/goal clear`, "drop the goal", "forget the goal" | **Confirm with the user first.** Then archive: `mv goal.md goal.archived-<YYYY-MM-DD-HHMM>.md`. Never silently delete. |
| `/goal done`, "we're done", "ship it", "is it done?" | Run the **full audit**: every Verification command, every Definition-of-done item. Only then set State to `achieved`. If any item fails, stay in `pursuing` and report exactly what failed. |
| `/goal abandon`, "give up on this" | Set State to `unmet`. Append a Progress log entry with the reason. Stop. |

## Audit discipline

This is the single most important rule and the easiest one to violate.

- **Do not check off a deliverable from memory.** Run the verification command. Read the output. If you can't run it, say so and leave the box unchecked.
- **Do not check off "all tests pass" when only some tests ran.** Run the full relevant suite. Note any skipped tests in the Progress log.
- **Do not infer that a feature works because the code "looks right".** Exercise it.
- **Do not edit a test to make it pass.** If a verification command fails after you thought the work was done, that is the highest-priority signal. Treat it as a blocker, fix the underlying code, and re-audit. Tests are the audit, not an obstacle to it.
- **Do not transition State to `achieved` in the same turn you finish the last deliverable.** Make a separate audit pass: re-run every Verification command, confirm every box, and write a one-paragraph audit summary in the Progress log naming which evidence supports which deliverable.

If the user pushes back on any of this — e.g., "just mark it done, I'll verify later" — you can comply, but say what you're doing: set State to `unmet` with a note that the user accepted incomplete verification, not `achieved`.

## Budget awareness

Budget lives in the `goal.md` header. The agent treats budget as a soft deadline:

- **Plenty of budget left** (rough estimate: >50% remaining): normal pursuing behavior. Take on substantive new sub-tasks.
- **Low budget** (<20% remaining): finish the current chunk, audit it, but do not start new substantive work. Update the Plan with what's left. If the goal is not yet achieved, transition State to `budget-limited`. Hand a clear summary to the user: what's done, what's left, what the smallest next step is.
- **Budget exhausted, work incomplete:** State = `budget-limited`, clean stop, summarize.

Only the user can extend the budget. If you think more budget is warranted, *say so and ask*. Do not silently raise it.

## Survives context compaction

Because `goal.md` is on disk, it survives compaction, `/clear`, new sessions, and hand-offs. Two practical consequences:

- After any compaction event or fresh session, the very first action is to re-read `goal.md` (and recent Progress log entries). Do not trust memory of "where we were".
- Keep the Progress log entries dense enough that someone — or some future Claude — could pick up the goal cold. A future you reading only `goal.md` should be able to take the next reasonable step.

## What this skill is NOT

- **It is not "run forever".** The completion model and the budget model are the whole point. A goal that can never be marked `achieved` is a poorly-scoped goal — push back on the user.
- **It is not a planning scratchpad for short tasks.** If the work is one or two turns, just do the work. Don't scaffold a goal.
- **It is not a way to bypass approvals.** Goal mode does not change the underlying tool, sandbox, or approval policy. Risky operations still need the same approvals they always did.
- **It is not a substitute for the user.** When blocked on a real ambiguity, log it under Open questions and ask. Do not guess.

## Example: kicking off a goal

**User:** `/goal migrate the auth service from sessions to JWT`

**Claude (this skill triggered):**

1. Checks for existing `goal.md` — none found.
2. Asks 3 quick questions:
   - "What signing algorithm — HS256 or RS256?"
   - "Should existing sessions remain valid during rollout, or hard cut-over?"
   - "Budget — do you have a deadline or turn limit in mind?"
3. After answers, drafts `goal.md` with concrete Definition-of-done items (e.g., "All routes under `auth/` accept JWT in `Authorization: Bearer`, verified by `pytest tests/auth/`"), Verification commands (`pytest tests/auth/`, `ruff check src/auth/`), Files in scope (`src/auth/`, `tests/auth/`), and an explicit Files NOT in scope list.
4. Shows the draft, asks: "Look right? I'll start on item 1 once you confirm."
5. On confirmation, sets State to `pursuing` and starts on item 1.

Subsequent turns just read `goal.md` and continue the loop.

## Example: an audit catching a regression

**State entering the turn:** Definition-of-done items 1–4 are checked. Item 5 ("All existing tests still pass") is the last open box.

**Agent:**
1. Runs `pytest` (the full suite, per the Verification commands).
2. Two tests in `tests/billing/` fail — not in scope, but the failures trace to a shared util the agent edited.
3. Does **not** check off item 5.
4. Logs: `2026-05-05T14:02 — Audit failed: tests/billing/test_invoice.py::test_proration and ::test_refund regressed after edit to src/util/clock.py. Investigating.`
5. Adds a sub-step to the Plan: "Fix clock util regression in billing tests".
6. Continues `pursuing`.
