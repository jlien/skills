---
name: factory-ops
description: >
  Operating a software factory like a product — adapters to your tracker and
  CI, seat policy for engineers' own AI tools, factory infra as code with
  dev/staging/prod, a deploy pipeline with the same gates as your core
  product, runbooks and postmortems that fix the factory itself, one human
  approving every merge, a named budget owner, and company-owned accounts.
  Use when running the factory day to day, or when asking what happens if
  the person who built it leaves.
---

# Factory Ops: Run the Factory Like a Product

One-line summary: **the factory is production infrastructure — same environments, same deploy gates, same on-call discipline as the product it ships code for.**

Credit: checklist from [Mar deHaym's post on X](https://x.com/mardehaym/status/2125319432432157152).

## The Checklist

- config-driven adapters for your tracker, git host, and CI
- a plan for when your issue tracker changes its API
- review comments posted right in the PR tool your engineers already live in, instead of some separate dashboard nobody opens
- a way to kill a run directly from the ticket
- your existing CI/CD handling deploys, keeping your release rules intact
- a clear policy for the Claude Code, Cursor, and Codex seats your engineers are already using
- seat telemetry that tracks usage without ever logging prompts or code
- device management on every laptop that has agent access to your repos
- the entire factory running on infrastructure you actually own
- a straight answer to "does this keep working if we stop paying the vendor tomorrow?"
- the factory's own infrastructure managed as code
- separate dev, staging, and prod environments for the factory itself
- unit tests for the factory that run without a model or a database
- contract tests covering every adapter
- a deploy pipeline for the factory with the exact same gates as your core product
- prompt rollbacks that are just as fast as code rollbacks
- an on-call rotation for the factory, with someone who actually answers the page
- runbooks for the morning the factory opens 40 pull requests overnight
- postmortems that fix the factory itself, not just the broken code it shipped
- a changelog for the factory so engineers know why it started behaving differently on Tuesday
- real documentation your team can read before they're asked to trust it
- a reviewer rotation so the same two senior engineers don't burn out reading every agent PR
- a weekly tally of how many hours your senior engineers are spending on reviews
- a human approving every single merge, every time
- a clear owner who holds the budget and actually reads the bill
- every key, repo, and account under the company's name, not tied to whoever hacked together the weekend prototype
- a bus factor higher than one

## Conventions That Carry the Value

- **Adapters at the edges, config-driven.** Tracker, git host, CI. When an API changes, one adapter changes — and contract tests catch it.
- **Meet engineers where they are.** Review comments land in the PR tool; deploys stay in your existing CI/CD with your release rules.
- **Seats are policy, not shadow IT.** Engineers' own tools get a written policy; telemetry counts usage and cost without logging prompts or code; every laptop with repo access is managed.
- **Own the infrastructure.** The rent-vs-own test from `SKILL.md`: stop paying the vendor, does it keep running?
- **The factory gets the product's discipline.** Managed as code, three environments, unit and contract tests, same deploy gates, fast prompt rollbacks.
- **Humans stay in the loop by design.** A reviewer rotation (measured weekly so burnout is visible), and a person approving every merge, every time.
- **No personal accounts.** Keys, repos, accounts under the company's name; one named owner reads the bill; bus factor above one.

## Decision Framework

- **The factory opened 40 PRs overnight.** Runbook exists; follow it.
- **A factory change broke something.** Postmortem fixes the factory, not just the code it shipped; the changelog records why behavior shifted on Tuesday.
- **Who holds the pager, the budget, and the accounts?** On-call rotation, named owner, company-owned — three different answers, all written down.

## Cross-References

- `SKILL.md` — "What Doesn't Qualify" and the rent-vs-own test.
- `factory-roles.md` — the people this ops layer needs (platform engineer, on-call, the budget owner).
- `factory-observability.md` — the traces and run history ops reads.
- `factory-evals.md` — prompt rollbacks and the golden set.
