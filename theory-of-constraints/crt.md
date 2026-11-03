---
name: current-reality-tree
description: >
  Current Reality Tree — Goldratt's sufficiency-logic tool for tracing a set
  of Undesirable Effects down to the few root causes that produce all of them,
  distinguishing core problems from symptoms. Use when many unrelated-seeming
  problems plague a process, fixes keep not working, or the team disagrees
  about what the real problem is.
---

# Current Reality Tree Agent Skill

One-line summary: **symptoms cluster; if five problems collapse into one root cause, fixing the root is the only move worth making — the CRT is how you prove which cause is the root.**

Use *before* proposing any fix when the situation is a fog of complaints. Pairs with `constraint-finder.md`: the CRT names why the system behaves this way; the constraint finder names where the flow binds.

## Core Concepts

- **Undesirable Effect (UDE)** — an observed, factual negative: "deploys take 2 weeks", "senior engineers quit", "customers churn in month 2". Not interpretations ("morale is bad") — checkable statements.
- **Sufficiency logic** — each arrow reads "IF [cause] THEN [effect]". One cause suffices for the effect; that's the test, not correlation.
- **Core driver** — the few causes at the bottom of the tree that all arrows trace back to. Typically 1–3 for a whole mess of UDEs.
- **The ring of causality** — some loops feed themselves (low trust → more review gates → slower work → more blame → lower trust). Ring-fence it; it won't respond to a linear fix.

## Workflow

1. **Harvest UDEs (5+)** — from the people in the process, stated as observable facts. Exit: list of checkable UDEs.
2. **Cluster** — group UDEs that likely share a cause. Exit: 2–4 clusters.
3. **Build downward** — for each cluster, ask "IF that's true, THEN what else must follow?" and "what IF-THEN chain produces this?" Draw entities and arrows. Exit: draft tree where each arrow is one readable sentence.
4. **Test for sufficiency** — read each arrow aloud: "IF {bottom}, THEN {top} — always, even when inconvenient?" Anything that needs "usually" gets an additional condition entity or a different cause. Exit: no arrow survives on "usually".
5. **Verify against reality** — walk the tree bottom-up with a neutral party who lives in the process and ask "does this match what you see?" Exit: their corrections are in the tree.
6. **Find the core driver** — the bottom entity (or loop) with the most arrows leaving it. Exit: one sentence: "the core problem is X because it directly causes {list the UDEs}".
7. **Predict a test** — state one observable consequence of the core driver that hasn't been checked yet, and go check it. Exit: prediction confirmed or tree revised.

## Decision Framework

**Symptom or root?**
- Flip the entity: if removing it would dissolve the UDEs above it, it's a candidate root. If removing it changes nothing downstream, it's a symptom.
- Roots are uncomfortable to say out loud in the room. "The constraint is the process" is a symptom; "the constraint is that the release policy assumes all changes carry equal risk" is closer to a root.

**Several plausible roots?**
- Prefer the one that explains the most UDEs with the fewest entities, and that a cheap probe can falsify fastest.

**The tree keeps growing?**
- Cap it. A CRT with 30 entities nobody will read is a mural, not a tool. 10–20 entities is the working range.

## Example

UDEs: deploys take 2 weeks; hot fixes wait in the same queue; engineers avoid small changes; incidents are large.

Tree: IF every change requires the same heavyweight review (policy) → THEN small and large changes queue together → THEN deploys batch up → THEN each deploy carries many changes at once → THEN incidents, when they happen, are large and hard to attribute.

Core driver: a *policy* — one review depth for all change sizes. Note that no single person or machine is the constraint; the CRT caught a policy constraint that a capacity analysis would have missed.

## Pitfalls

- **Blame entities.** "Dave is slow" is not an entity. "Manual regression testing consumes 60% of review time" is. A tree that names people gets discarded, not acted on.
- **Correlation arrows.** Two things moving together is not IF-THEN. Demand the causal sentence.
- **Fixing mid-tree.** An intervention at a symptom entity buys relief until the core driver re-creates it.

## Collaboration Pattern

### With `evaporating-cloud.md`
The CRT often exposes a *conflict* at the root ("thoroughness vs. speed"). Hand that conflict to the Evaporating Cloud rather than picking a side.

### With `future-reality-tree.md`
Once the core driver is found and a fix is proposed, the FRT verifies the fix dissolves the UDEs the CRT connected.

### With `CTO.md` and `Project-Management.md`
Core drivers that are policies route to the CTO agent for retirement decisions; UDE lists feed the risk register as evidence-backed risks.

## Key Principles

- **The mess is not many problems.** It is few causes wearing many masks.
- **Sufficiency over plausibility.** "Could be" fails; "must follow" passes.
- **Read the arrows, not the boxes.** A tree of nouns proves nothing; the IF-THEN sentences carry the argument.
- **Stay factual.** If an entity can't be checked by an observer, rewrite it.
