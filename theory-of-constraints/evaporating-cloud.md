---
name: evaporating-cloud
description: >
  Evaporating Cloud (conflict cloud) — Goldratt's win-win tool for dissolving
  a conflict between two legitimate needs instead of compromising between
  them. Surfaces the hidden assumption that makes the conflict seem
  unavoidable and finds an injection that satisfies both sides. Use when the
  team is stuck between two good goals — speed vs. quality, autonomy vs.
  alignment, cost vs. capability.
---

# Evaporating Cloud Agent Skill

One-line summary: **a dilemma is an assumption in disguise — state the conflict precisely, attack the assumption nobody wrote down, and the cloud evaporates.**

## When to Use

- Two requirements, stakeholders, or values genuinely conflict and compromise would damage both.
- A CRT traced the core problem to a conflict loop (e.g., "thoroughness vs. speed").
- Debate keeps cycling: both sides restate their case louder, no new information enters.

## The Cloud's Structure

```
            A (shared objective)
           /                    \
    B (requirement)        C (requirement)
          |                       |
    D (prerequisite)        D' (prerequisite)
```

- **A** — the objective both sides share. If you cannot state one, you have two separate problems, not a conflict.
- **B and C** — the two requirements each side needs to meet A. *Both are legitimate.* This is the tool's stance: no villains.
- **D and D'** — the prerequisites that make B and C mutually exclusive *as currently practiced*. D and D' are the only things in conflict.
- The verbal trap: "I can't do D because that would prevent D'." Precisely — and the assumption inside that sentence is the target.

## Workflow

1. **State the conflict in one breath.** "We need D *in order to* B, and D' *in order to* C, both *in order to* A." Exit: the sentence, with both sides agreeing it's fair.
2. **Name A, B, C explicitly.** If B or C is stated as an attack on the other side, rewrite it as a need. Exit: B and C are need-statements, not positions.
3. **Surface D and D'.** Get concrete — D is a specific practice, not a value. Exit: D and D' written as checkable statements.
4. **Attack D's assumptions.** For each assumption behind D ("D is required for B because…"), ask: is it always true? Under what conditions was it true when adopted? What changed? Exit: at least one assumption marked as breakable.
5. **Find the injection.** A change that breaks the assumption so both B *and* C are satisfied — no trade-off. Exit: one or more injections.
6. **Verify the injection.** Does it satisfy B? Does it satisfy C? What new assumptions does it need, and are they real? Exit: injection survives both checks or returns to step 5.
7. **Hand off** — `future-reality-tree.md` to verify the fix system-wide, `transition-tree.md` to plan it.

## Example

- **A:** Ship reliable software that customers trust.
- **B:** Every change is verified before release *(requires D)*
- **C:** Changes reach production quickly *(requires D')*
- **D:** Full manual regression suite before every deploy.
- **D':** Deploy without waiting on the manual suite.

Assumption inside D: "only humans clicking through the app can verify release-readiness." Break it: automated coverage of the regression suite's highest-value paths moves verification *into* CI — B is satisfied continuously, C is unblocked. D and D' no longer conflict because D was a *practice*, not the need.

## Pitfalls

- **Compromising.** "Deploy with half the regression suite" is a lose-lose split, not an evaporation. If the injection satisfies only part of B or C, it's not the injection.
- **Attacking C to defend D.** The moment one side argues the other's requirement is optional, the cloud is a political fight, not a logic tool. Stop and re-run step 2.
- **Vague D.** "Better process" as D means no assumption can be attacked. Force the concrete practice.
- **Treating the cloud as done when agreed.** An agreed injection is an opinion until the FRT checks it against the whole system.

## Collaboration Pattern

### With `crt.md`
The CRT finds the conflict; the cloud dissolves it. Run the CRT first when the conflict emerged from a wider mess.

### With `Product-Manager.md`
Product trade-off debates (scope vs. date, quality vs. speed) are evaporating clouds in the wild — the injections usually become roadmap decisions the PM agent owns.

### With `CTO.md`
Engineering policy conflicts (governance vs. velocity) dissolve into specific policy changes the CTO agent can ratify.

## Key Principles

- **Both needs are legitimate.** The conflict lives between the *practices* (D, D'), never between the needs (B, C).
- **No compromise is the success test.** If B and C aren't both fully satisfied, keep digging for assumptions.
- **Write everything down.** The unstated assumption is always the load-bearing one.
