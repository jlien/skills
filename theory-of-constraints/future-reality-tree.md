---
name: future-reality-tree
description: >
  Future Reality Tree — Goldratt's tool for proving a proposed injection
  actually produces the desired effects and dissolves the original undesirable
  effects, plus Negative Branch Reservation: hunting and trimming the new
  problems the fix would create before committing. Use before implementing any
  fix from a CRT, Evaporating Cloud, or Five Focusing Steps cycle.
---

# Future Reality Tree Agent Skill

One-line summary: **before you commit, prove in logic that the injection dissolves the original problems — and reserve negative branches: write down how the fix could backfire, and trim each path before it exists.**

## When to Use

- An injection from `evaporating-cloud.md` or an exploit/elevate move from `five-focusing-steps.md` is about to be committed.
- A past fix worked for a quarter and then created a new problem (that fix skipped its NBR).
- Stakeholders ask "how do we know this won't make things worse?"

## Core Concepts

- **Injection** — the proposed change (policy, practice, resource).
- **Desirable Effects (DEs)** — the positive outcomes the injection should cause, stated as checkably as UDEs were.
- **Sufficiency logic again** — IF injection THEN chain of intermediate effects THEN DE. Every arrow must survive the "always?" test.
- **Negative branch** — an unintended causal path: IF injection THEN {some side condition} THEN {new UDE}. NBR is the discipline of finding these *before* the injection ships.
- **Trimming** — pre-empting a negative branch with a small added injection (a guard, a phase-in, a metric) that cuts the path.

## Workflow

1. **Restate the UDEs** this fix must dissolve (from the CRT or constraint statement). Exit: list on the table.
2. **List the DEs** the fix should produce, one per dissolved UDE. Exit: paired UDE→DE list.
3. **Build the sufficiency tree** from injection to DEs. Exit: causal chain with no "usually" arrows.
4. **Check each UDE is dissolved** — trace the path from injection to the negation of that UDE. If a UDE has no path, the injection doesn't cure it; say so. Exit: every UDE mapped or honestly flagged.
5. **Hunt negative branches.** For each intermediate effect ask: "what ELSE does this cause? Who loses what? What habit, metric, or contract does this break?" Exit: every negative path drawn to a concrete new UDE.
6. **Trim each negative branch** — add the smallest injection that cuts the path, and re-verify it doesn't start a new branch of its own. Exit: no untrimmed path remains.
7. **Set the verification signal.** Define the measurement that will show the DE arrived (and a negative branch didn't) within 2–4 weeks of shipping. Exit: signal named with owner.

## Negative Branch Hunting Prompts

Run these against every intermediate effect in the tree:

- Who becomes worse off because of this? (Their behavior will change.)
- What local metric or incentive does this violate? (People protect their metrics.)
- What does the system do during the transition, before the benefit lands? (The gap is where branches grow.)
- What happens at twice this scale? Ten times?
- What does this make *impossible* that someone legitimately needs?

## Example

Injection: cross-train a second editor (from the five-focusing-steps example).

Positive path: IF second editor trained → THEN publish capacity rises → THEN the pull queue clears weekly → THEN lead time per piece drops (DE).

Negative branch: IF a second editor exists → THEN the release policy "editor signs every piece" hardens into bureaucracy → THEN even trivial copy tweaks queue for two people → THEN lead time *rises*.

Trim: define decision rights first — the original editor keeps the standard, the second editor handles defined categories solo. One small policy injection cuts the branch.

## Pitfalls

- **The cheerleader tree.** Building only the positive path because the injection is popular. The NBR pass is where the tool earns its cost.
- **Trimming with monitoring instead of change.** "We'll watch for it" does not cut a causal path; it documents the damage. Trim with a guard, cap, or decision right.
- **Skipping step 7.** Without a pre-named verification signal, "no complaints" becomes the success criterion.
- **One tree for three injections.** Each injection gets its own tree; bundled injections can't attribute effects.

## Collaboration Pattern

### With `crt.md`
The CRT supplies the UDEs and core driver; the FRT is its mirror image — same logic run toward a future state.

### With `transition-tree.md`
A validated FRT hands its trimmed branches to the transition plan as known obstacles with pre-decided guards.

### With `Project-Management.md`
The verification signal (step 7) becomes a tracked item with an owner; trimmed branches feed the risk register.

## Key Principles

- **The injection that creates no negative branch is the injection nobody thought hard about.**
- **Dissolution, not mitigation.** Each original UDE should be logically *gone*, not reduced.
- **Name the signal before shipping.** Success and failure criteria are decided in logic, not discovered in sentiment.
- **Small trims beat big reworks.** A guard added now is cheaper than a branch lived with later.
