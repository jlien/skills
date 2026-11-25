---
name: factory-security
description: >
  Security and compliance for a software factory — customer data stripped
  from tickets, secrets blocked at the code level, prompt-injection defenses,
  supply-chain checks, tenant isolation, audit trails, and an incident plan.
  Use when onboarding a factory to customer contracts, answering security
  questionnaires, or auditing what the agent can reach.
---

# Factory Security & Compliance

One-line summary: **treat every ticket, comment, and README as untrusted input, and assume an auditor will one day ask exactly what the agent could touch.**

Credit: checklist from [Mar deHaym's post on X](https://x.com/mardehaym/status/2125319432432157152).

## The Checklist

- customer and patient data stripped out of any ticket or comment the agent reads
- a signed BAA with your model provider before any ticket touching patient data goes near it
- code and data staying inside your own cloud if your customer contracts require it
- secrets scrubbed from prompts, traces, and PR comments
- code-level blocks preventing the agent from even opening secret files
- a secrets scan running on every single diff
- prompt injection defenses on every ticket, comment, and README, so a malicious README can't tell the agent to drop a table
- a check verifying that every new package actually exists and isn't a typosquat
- dependency scanning on every pull request
- a guard against deleted tests, because an agent that can't fix a failing test will sometimes just delete it
- protected files that require human sign-off: CI config, auth, migrations, and the factory's own settings
- least-privilege tokens for your issue tracker, repo, and CI
- strict tenant isolation, so one client's code never leaks into another client's context
- a full audit trail of what the agent read, what it changed, and who signed off
- a real answer for customer security questionnaires asking exactly what the AI can access
- an incident plan for the day a tracker token leaks

## Conventions That Carry the Value

- **Data hygiene precedes access.** Strip customer and patient data at the source; a BAA comes before the first ticket, not after the first leak.
- **Secrets are blocked, not asked for.** Code-level blocks on opening secret files, plus a scan on every diff — defense in depth, not policy memos.
- **Every text surface is an injection surface.** Tickets, comments, READMEs — defend each one.
- **Supply chain is checked per package and per PR.** Existence check (typosquat guard) on new packages; dependency scanning on every PR.
- **Deletion is a signal.** An agent that can't fix a test will delete it; the guard sends that back.
- **Four file classes need a human signature:** CI config, auth, migrations, the factory's own settings.
- **Tokens are least-privilege and tenant-walled.** One client's context never reaches another client.
- **The audit trail is the product.** What the agent read, changed, and who signed off — written down so the questionnaire answer is a query, not a scramble. The incident plan for a leaked tracker token exists before the leak.

## Decision Framework

- **Does this ticket touch patient data?** BAA signed first, or the ticket waits.
- **A customer asks what the AI can access.** Answer from the audit trail and the written access map — precisely, same day.
- **Agent deletes a failing test.** Blocked and returned; deletion is never a fix.

## Cross-References

- `factory-runs.md` — sandbox isolation and network allowlists.
- `factory-verification.md` — the deleted-test guard's place in the gates.
- `code-review/SKILL.md` — blocking security review on every PR.
