---
name: crap
description: >
  CRAP (Change Risk Anti-Patterns) triage for Rails — compute Savoia's
  comp^2 * (1 - cov/100)^3 + comp per method from RuboCop cyclomatic
  complexity and SimpleCov coverage, then act: write the missing specs,
  extract the method, or hand the subject to mutation testing. Use when
  deciding what to test next, prioritizing legacy cleanup, or explaining
  why a fully "covered" method still carries change risk.
---

# CRAP: Change Risk Anti-Patterns

CRAP scores one method at a time on two questions: **how complex is this to change** and **how likely is a change to slip past the tests**. The metric is Alberto Savoia's "Change Risk Anti-Patterns" (2007):

```text
CRAP = comp² · (1 − cov/100)³ + comp
```

- `comp` — the method's cyclomatic complexity
- `cov` — its line coverage, 0–100

**Threshold: a method with CRAP > 30 needs action** (Savoia's original cutoff).

## Why the cube matters

The `(1 − cov/100)³` term punishes uncovered complexity non-linearly:

| cov | (1 − cov/100)³ | dilution vs 0% coverage |
|---|---|---|
| 0%  | 1.000 | 1× |
| 40% | 0.216 | ~4.6× |
| 60% | 0.064 | ~15.6× |
| 80% | 0.008 | ~125× |
| 100%| 0     | penalty gone — `CRAP = comp` |

Worked examples (exact arithmetic):

| comp | cov | CRAP | reading |
|---|---|---|---|
| 2 | 0% | 4 + 2 = **6** | trivial; ignore |
| 10 | 0% | 100 + 10 = **110** | test before you touch |
| 10 | 40% | 21.6 + 10 = **31.6** | borderline — add the missing branches |
| 10 | 60% | 6.4 + 10 = **16.4** | acceptable |
| 30 | 0% | 900 + 30 = **930** | refactor or quarantine |
| 35 | 100% | 0 + 35 = **35** | fully covered, still flagged — the complexity *is* the risk |

Two structural consequences, both intended by the metric:

1. **You cannot cover your way out of comp > 30.** At 100% coverage, CRAP = comp. A method still over 30 with every line tested is telling you to extract methods, not to chase coverage.
2. **Coverage past ~60% has small returns.** Going 40% → 60% cuts the complexity penalty 3.4×; 80% → 100% buys almost nothing beyond zeroing the last term. Spend test effort where the cube still bites.

Realistically, comp ≤ 5 can only crack the threshold at near-zero coverage (`comp = 5`, `cov = 0` scores exactly 30), so actual CRAP offenders are comp ≥ 8 methods.

## Getting the inputs (stack you already have)

### comp — RuboCop (cyclomatic, the real denominator)

```sh
bundle exec rubocop --only Metrics/CyclomaticComplexity,Metrics/PerceivedComplexity app lib
```

Each offense reports actual/allowed — `Cyclomatic complexity for apply_payment is too high. [9/6]` means `comp = 9`. Methods under the cop's Max produce no number; that is fine, because sub-Max methods rarely trip CRAP (see the comp ≤ 5 note above).

`Metrics/PerceivedComplexity` is a gentler variant (boolean operators and `? :` weighted lower). Whichever you quote, say which one you used.

### comp — Flog via RubyCritic (discovery + churn, different denominations)

RuboCop prints only offending methods. For a per-method scan of a directory, Flog does it, and RubyCritic wraps Flog and adds churn:

```ruby
# Gemfile, :test group
gem "rubycritic", require: false
```

```sh
bundle exec rubycritic --no-browser -f json app/models app/services
# or browse tmp/rubycritic/ — per-method complexity plus churn (commit count)
```

**Flog is ABC complexity (Assignments, Branches, Calls) — not cyclomatic.** It counts assignments and calls the CRAP formula ignores, so "Flog 30" is not "CRAP comp 30". Use Flog/RubyCritic to *find* candidates and to see churn; take the `comp` number that feeds the formula from RuboCop.

### cov — SimpleCov

SimpleCov reports per-line (and per-branch once `enable_coverage :branch` is on, which the standard setup in `SKILL.md` enables). There is no per-method rollup — read it: open `coverage/index.html`, go to the flagged file, find the method's line range from the offending method name, and eyeball the share of uncovered lines across the method's executable lines.

Close enough for triage. CRAP is a prioritization signal, not a CI gate — do not build tooling around it until repeated use proves the need.

## The workflow

1. **List candidates** — RuboCop for the offending methods, RubyCritic for a directory-with-churn view.
2. **Score each candidate** — the formula is three operations; do it in your head, or with the table above.
3. **Act per quadrant:**

| Situation | Action |
|---|---|
| comp high, cov low (CRAP ≫ 30) | Write the missing specs first — follow the BDD flow in `SKILL.md` §6: one failing spec per uncovered branch, then fix |
| comp high, cov 100% (CRAP ≈ comp > 30) | Refactor — extract a method, class, or state object. The suite is green and behavior-locked, so extract mechanically |
| comp low, cov low | Ignore unless you are touching that file anyway |
| comp low, cov high | Ignore |

4. **Re-score after the specs land.** Still above 30 at full coverage → the remaining problem is shape, not tests → refactor task, not a test task.
5. **Escalate high-value, hard-to-spec subjects** (money math, auth, permission checks, state machines) to mutation testing (`mutation-testing.md`) once specs exist. CRAP finds thin tests; mutation testing finds specs that never assert anything.

Example pass: `Invoices::ApplyPayment#call` — RuboCop `[9/…]`, SimpleCov ≈ 33% line coverage → CRAP = 81·0.301 + 9 ≈ 33 → flag. Add specs for the failed-payment and boundary branches, coverage → 78% → CRAP = 81·0.011 + 9 ≈ 10 → clear, move on. If instead you hit 100% and CRAP stayed ≈ 9, it was never a CRAP problem.

## Limits

1. **Line coverage ≠ path coverage.** A method can be 100% line-covered with an untested branch combination. `enable_coverage :branch` narrows the gap; mutation testing closes it.
2. **Flog ≠ cyclomatic.** Keep the denominations straight (see above).
3. **Per-method only.** Never average CRAP into file or class scores — the squaring and cubing make it non-additive, and a file-level "CRAP" number is meaningless.
4. **Churn is a separate axis.** CRAP says nothing about how often code changes. RubyCritic's churn × complexity chart covers exactly what CRAP drops: an often-changed comp-8 file can be a worse bet than a frozen comp-20 one.
5. **No maintained Ruby gem prints CRAP.** RubyCritic's core metrics are churn/complexity/cost/rating, and no other well-known Ruby tool computes it. The formula is short enough for mental math during triage — stop hunting for tooling.
6. **Don't game it.** Do not split a method into five shards to move the number; extract along cohesive seams (single responsibility), not arithmetic seams. Do not spec trivial accessors for the score either — the coverage standard in `SKILL.md` already says: find gaps, don't chase percentages.

## Cheat sheet

```sh
# comp (cyclomatic)
bundle exec rubocop --only Metrics/CyclomaticComplexity,Metrics/PerceivedComplexity app lib

# per-method complexity + churn (discovery; ABC proxy)
bundle exec rubycritic --no-browser -f json app/models app/services

# cov per method
open coverage/index.html          # SimpleCov from the last full spec run

# CRAP = comp² · (1 − cov/100)³ + comp     → act when > 30

# thin-but-valuable subjects →
#   see mutation-testing.md
```

## Cross-references

- `mutation-testing.md` — verification that specs actually assert (the next stage after CRAP triage)
- `debugging.md` — reproduce exceptions as specs first when CRAP flags a crash-prone method
- `SKILL.md` §6 (BDD bug fixing) and the Test Coverage section
