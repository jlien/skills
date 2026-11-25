---
name: factory-gateway
description: >
  Model gateway and cost control for a software factory — one self-hosted
  gateway for every model call, keys per team/service/agent with budgets,
  config-driven model names, provider fallback, and cost tracked per merged
  PR. Use when designing model-call infrastructure, when the token bill
  surprises someone, or when a provider goes down.
---

# Factory Gateway & Cost

One-line summary: **every model call goes through one gateway you host — a direct vendor call is a bug, not an optimization.**

Credit: checklist from [Mar deHaym's post on X](https://x.com/mardehaym/status/2125319432432157152). This is the detailed layer under part #5 of the `software-factory/SKILL.md` architecture.

## The Checklist

- a single gateway for all model calls, treating any direct vendor call as a bug
- provider API keys that never leave that gateway
- separate keys per team, service, and agent, each with its own budget
- rate limits so one noisy repo doesn't starve everyone else
- model names living in config, so swapping models doesn't require a code deploy
- a fallback provider for the afternoon your primary one goes down
- a migration plan for when your model gets deprecated
- spend alerts that fire the same day, well before the monthly invoice lands
- cost tracked per merged PR, not just raw token counts

## Conventions That Carry the Value

- **One door.** Keys live in the gateway and nowhere else. Code that calls a vendor directly gets treated like a leaked secret.
- **Keys are scoped and budgeted.** Per team, per service, per agent — so a bill answers "who", not just "how much".
- **Model identity is config, not code.** Swapping providers is a config change plus an eval rerun, not a deploy.
- **Cost is a product metric.** Track it per merged PR. Raw token counts answer nothing anyone asks.
- **Plan for provider death twice.** A fallback for today's outage; a migration plan for the eventual deprecation.

## Decision Framework

- **A team's bill spikes.** Their key's budget and rate limit make it visible the same day, in isolation.
- **Primary provider is down.** Fallback provider takes the traffic; no code change.
- **Model gets deprecated.** Migration plan runs: swap config, rerun the eval suite (see `factory-evals.md`), then ship.

## Cross-References

- `SKILL.md` — part #5 (gateway) and the build-order rule: gateway first, agent last.
- `ai-transformation/SKILL.md` — the Phase 4 guardrail this implements.
- `factory-observability.md` — traces carry prompt, tokens, latency, and cost per call.
