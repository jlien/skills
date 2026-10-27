---
name: launch-qa
description: >
  Launch QA via five simulated first-time users. Before shipping, spin up
  five persona subagents (impatient, skeptic, mobile, non-native English
  speaker, breaker) that each walk the app in a real browser from landing
  page to first success, screenshotting every moment they get confused,
  stuck, or annoyed. Merge their findings ranked by how many users hit
  each one, fix everything in one pass, and rerun all five to prove the
  fix. Use when a product, flow, or signup is about to ship and you need
  the reasons first users would leave — before they leave.
---

# Launch QA (Five First Users)

One-line summary: **your first 100 real users won't tell you why they left; these five will.** Five simulated first-time users, each a different failure mode, run in a real browser before launch. Their confusion is cheaper than churn.

Source: the "five first users" launch-QA pattern (works best with a browser MCP connected, Playwright, or Chrome DevTools — anything that lets a subagent open a real page, click, and screenshot).

## Core Responsibilities

- Run **five persona subagents in parallel**, each walking the app from landing page to **first success** (the first moment the product delivers its core value — signup complete, first item created, first result seen).
- Each persona acts strictly in character and **screenshots every moment they get confused, stuck, or annoyed**, with a one-line note of what the screen showed vs. what they expected.
- Merge all five reports into **one list ranked by how many users hit each issue**.
- Fix everything in **one pass** — not drip-fed — then **rerun all five** to prove the fix.
- This is QA of the existing flow only. Do not add features, redesign, or reposition. Findings are about what blocks or confuses first use.

## The Five Personas

| # | Persona | Script (give verbatim to the subagent) | What it catches |
|---|---|---|---|
| 1 | **The impatient one** | Skim, don't read. Click the first button that looks right. The moment you hit an error, quit and record it. | Broken primary CTA, slow first paint, dead-end error states, anything where the obvious path is the wrong one |
| 2 | **The skeptic** | Read the pricing page, the terms, and the privacy policy before signing up. Question every charge and every data request. | Vague pricing, missing/unreachable legal pages, trust gaps, permission requests with no justification |
| 3 | **The mobile user** | Do the whole flow on a 375px viewport throttled to slow 3G. | Horizontal overflow, unreachable tap targets, unresponsive on throttled networks, un-sized media, no loading states |
| 4 | **The non-native English speaker** | Follow only what the UI literally says. Idioms, metaphors, and implied steps do not exist for you. | Idiomatic or jargon copy, ambiguous labels, flows that assume cultural knowledge, instructions that only work if you already know the product |
| 5 | **The breaker** | Paste junk into every form (emoji, 10k characters, scripts, pasted multi-line garbage). Hit back mid-flow. Double-click every button. | Missing validation, duplicate submissions, corrupt state after back-navigation, unhandled server errors |

Persona 1 defines the **floor**: anything that stops the impatient user is a launch blocker by definition — the largest cohort of real users behaves exactly like them.

## Workflow

### Phase 1 — Set up the run

- You need one real browser session per persona: a browser MCP, Playwright, or Chrome DevTools-driven subagent. Five subagents, five isolated sessions, one app URL.
- Give every agent the same report format so merging is mechanical:

```
persona: <name>
step: <landing → … → first success>
status: completed | quit at <step>
finding: <one line>
evidence: <screenshot path>
ui said: "<exact copy on screen>" / expected: <what they needed>
```

### Phase 2 — Run the five in parallel

Dispatch all five at once; they don't share state and shouldn't see each other's reports. Each opens the app in its browser and walks landing → first success, in character, screenshotting as specified. An agent that cannot complete the flow has still produced the most important finding — record where and why it quit.

### Phase 3 — Merge and rank

- Deduplicate findings across personas (same root cause counts once, but **credit every persona that hit it**).
- Rank by reach: a bug all five hit outranks a bug one hit. Reach, not severity theater, decides the order.
- Keep the screenshots. "It felt broken" is not a finding; a screenshot of the broken state is.

### Phase 4 — Fix in one pass

Work the ranked list top to bottom in a single batch. Resist fixing only the top item and re-running — partial passes waste the rerun, which is the expensive step.

### Phase 5 — Rerun to prove it

Rerun all five personas against the fixed build, same scripts. A fix is done when the persona that found it completes its flow cleanly — not when the code is deployed. Anything new the rerun surfaces re-enters the ranked list.

## Decision Framework

- **Reach wins.** Rank by how many personas hit it. A 5/5 papercut beats a 1/5 catastrophe for launch order.
- **Persona 1 sets the bar.** If the impatient user quits, ship-no is the default regardless of what the others found.
- **Screenshots over adjectives.** No evidence, no finding.
- **One pass, then re-prove.** Never ship between single fixes; the rerun is the proof.
- **QA, not consulting.** Findings describe what blocked first use — not opinions on the business model, copy tone, or feature set.

## Collaboration Patterns

- **`code-review` skill** — after the rerun passes, the fix batch goes through normal agent-era code review. Launch QA finds what to fix; code review governs how the fix lands.
- **`content/llm-artifact-sweep` skill** — persona 4 (non-native speaker) surfaces copy-level failures; the artifact sweep is the copy-layer check that runs on the same screens before launch.
- **`pagespeed` skill** — persona 3's slow-3G findings get their deep-dive there: field CrUX data, ranked fix list, and the real-vs-noise triage this skill doesn't attempt.
- **`ruby-on-rails` skill** — implements the fix batch in the app's stack, with the failing persona walkthrough as the reproduction.

## Key Principles

- **Real browser, real throttle, real clicks.** Code review of the flow is not a substitute for walking it.
- **Five failure modes cover most churn.** Impatience, distrust, hostile devices, plain language, and hostile input are why first users leave.
- **The quit is the finding.** Where the impatient user gave up is the single most valuable screenshot in the run.
- **Rank by reach, fix in one pass, re-prove with a rerun.** Anything less is theater.
