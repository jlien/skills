---
trigger: measure AI visibility, LLM rank tracking, GEO tracking, AI referral traffic, share of voice, prompt panel, are we cited, Perplexity citations, AI Overview monitoring, AI crawler logs
---

# AIO Measurement — Tracking AI / Answer-Engine Visibility

Companion to the `SKILL.md` in this directory. Optimization gets you cited; this
measures whether it's working. There is no official "LLM ranking" — you triangulate from
four signals, cheapest and highest-signal first.

## Read this first (the honest baseline)

A new or small site is not in a model's training data, so **base (no-web)
ChatGPT/Claude will not cite you — and that is expected**. Every bit of visibility you
can actually measure for a young site comes from **web-retrieval modes** (Perplexity,
ChatGPT Search, Gemini grounding, Bing Copilot, Grok live search) and the **referral
traffic** they send. Measure those. Do not waste a panel prompting base models with the
web off — a zero there means nothing.

## Four methods (triangulate — no single one is truth)

### 1. AI referral traffic — the ground truth (GA4)

Real humans arriving from an AI answer show up as referral traffic. In GA4, build a
segment / exploration on Session source (or Session source / medium) matching these
hosts:

- `chatgpt.com`, `chat.openai.com`
- `perplexity.ai`
- `gemini.google.com`, `bard.google.com`
- `claude.ai`
- `copilot.microsoft.com`, `bing.com` (Copilot)
- also seen: `you.com`, `poe.com`, `grok.com`

This is the number that matters — the *outcome*. Track weekly sessions and conversions
from that segment. For a young site it may be near zero; the point is the trend.

### 2. Prompt-panel harness — the closest thing to "rank tracking"

Define a fixed set of 20–50 real user queries, run them across web-enabled models on a
schedule, and score whether your domain is cited or recommended. Track **citation rate**
and **share-of-voice** (you vs. named competitors) over time.

- **Query set** — mirror what your audience actually asks: informational ("how do I say
  X"), comparison ("best way to learn Y"), use-case ("what should I know before Z").
  **Freeze and version it** — comparability week-over-week beats a bigger one-off panel.
- **Models, best programmatic signal first**: Perplexity API (returns a `citations`
  array — the single best source), then ChatGPT (search on), Gemini (grounded), Grok
  (live search), Claude (web-search tool). Web/search modes only.
- **Score per query**: cited? (your domain in the sources), recommended? (brand named in
  the prose), position among sources, which competitors appear.
- **Metrics**: citation rate (% of queries citing you), share-of-voice (your mentions ÷
  all brand mentions), average source position.
- **Cadence**: weekly. Cheap enough to self-host; alert on a drop.

A minimal Perplexity-first runner is below.

### 3. AI-crawler coverage — server / CDN logs

The precondition for any citation: the retrieval bots must actually fetch you. Grep
access logs for these user-agents and confirm 200s on `/llms.txt` and your money pages:

- Retrieval/citation: `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `Perplexity-User`,
  `Google-Extended` (AI Overviews / Gemini grounding), `Bingbot` (Copilot)
- Training: `GPTBot`, `ClaudeBot`, `anthropic-ai`, `CCBot`, `Applebot-Extended`,
  `meta-externalagent`, `Bytespider`, `Amazonbot`

A retrieval bot that never fetches you = zero chance of a citation → fix the crawler
allow-list (see `SKILL.md` Phase 1) before chasing anything else.

### 4. GSC as a proxy — indirect but free

Google AI Overviews are drawn from pages that already rank. Rising impressions on
informational / question queries with flat or soft clicks is a fingerprint of AI-Overview
inclusion (the answer is shown, the click is absorbed). Watch Search Console query-level
impressions on your target questions.

## Reference: minimal prompt-panel (Perplexity-first)

Freeze the query set; one realistic user query per line:

```
# queries.txt
how do I say I don't eat meat in Japanese for travel
best way to learn essential Japanese phrases for a Japan trip
how do I read a Japanese no-smoking street sign
what should I know before using a Japanese convenience store
```

```bash
#!/usr/bin/env bash
# panel.sh — citation check via Perplexity (its response includes source URLs).
# Needs PERPLEXITY_API_KEY. Emits per-query CITED/-, then the citation rate.
set -uo pipefail
DOMAIN="${DOMAIN:?set DOMAIN, e.g. example.com}"
hits=0 n=0
while IFS= read -r q; do
  [ -z "$q" ] && continue; n=$((n+1))
  payload=$(printf '%s' "$q" | ruby -rjson -e 'puts({model:"sonar",messages:[{role:"user",content:STDIN.read.strip}]}.to_json)')
  resp=$(curl -s https://api.perplexity.ai/chat/completions \
    -H "Authorization: Bearer $PERPLEXITY_API_KEY" -H "Content-Type: application/json" \
    -d "$payload" || true)
  if printf '%s' "$resp" | grep -qi "$DOMAIN"; then hits=$((hits+1)); mark="CITED"; else mark="-    "; fi
  printf '[%s] %s\n' "$mark" "$q"
done < queries.txt
printf 'citation_rate: %d/%d\n' "$hits" "$n"
```

Extend it: add Grok (`api.x.ai`), Claude (web-search tool), and Gemini (grounded
`generateContent`); aggregate **share-of-voice** by also grepping competitor domains;
schedule weekly, store each run, and alert on a drop. This is a natural recurring
agent/cron job — the same shape as any other scheduled report.

## Metrics that matter (track weekly)

- **AI referral sessions + conversions** (GA4) — the outcome
- **Citation rate** (% of panel queries citing you) — the leading indicator
- **Share-of-voice** vs. named competitors
- **Crawler coverage** (retrieval bots fetching key URLs, returning 200)
- **GSC impressions** on target question queries — the proxy

## Decision Framework

- **Base model won't cite you?** Expected for a young site. Ignore base models; measure
  web-retrieval modes + referral traffic.
- **Crawlers absent?** Fix the allow-list first — you cannot be cited by a bot you
  blocked or that never fetched you.
- **Citation rate up but referrals flat?** You're cited without a clickable link, or the
  citation isn't compelling — strengthen the top-of-page answer block and title
  (`SKILL.md` Phase 2).
- **DIY vs. paid?** Self-run the panel with your own API keys. Graduate to a paid
  tracker — Profound, Peec AI, Otterly, Scrunch, Ahrefs Brand Radar — when you want
  multi-model dashboards and history without maintaining the harness.

## Key Principles

- **Measure retrieval modes and referral traffic, not base-model recall.**
- **Freeze the query set.** Comparability over time beats a bigger one-off panel.
- **Citations are the leading indicator; referral sessions are the outcome.** Track both.
- **Crawler access is the precondition.** Verify bots fetch you before chasing citations.
- **Trend beats absolute.** Week-over-week movement on a fixed panel is the real signal.

## Collaboration Patterns

- **`SKILL.md`** (this directory) — the optimization half (get cited). This is the
  measurement half. Run them together: make an AIO change, then watch citation rate move.
- **`seo/` + GSC** — the GSC proxy overlaps SEO reporting; pull them in one pass.
- **`llm-as-a-verifier`** — score panel responses at scale (genuine recommendation vs. a
  passing mention) instead of a brittle keyword grep.
