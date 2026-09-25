---
name: content-gap-analysis
description: "SEO content gap analysis from live Search Console + GA4 data: missing content, striking-distance, underperforming-visibility, and answer-style opportunities."
version: 1.0.0
author: Jimmy Lien
license: MIT
metadata:
  hermes:
    tags: [seo, gsc, ga4, content-strategy]
    related_skills: [skyscraper-approach, content-brief, icp-seo-inventory]
---

# Content Gap Analysis

An SEO strategist workflow: find missing content, striking-distance rankings,
underperforming pages, and answer-style opportunities — from real Search
Console and GA4 data, never from outside keyword tools.

## Core Responsibilities

- Pull three months of query and page rows from Google Search Console: clicks, impressions, CTR, position.
- Optionally join GA4 landing-page sessions to show whether gap topics convert.
- Classify every filtered cluster into exactly one gap type: missing content, striking distance, underperforming visibility, answer-style page.
- Deliver a prioritized cluster table, top 5 new pages, and top 5 quick wins.
- Use only numbers the GSC API returned. Never invent search volumes or keywords from memory or other tools.

## When to Use

- "Run a content gap analysis on <site>" with no CSVs attached — pull GSC/GA4 live (see `gsc-ga4-data-access.md`).
- The user hands you GSC exports as files — same analysis, skip the pull step.
- Don't use for: technical SEO audits, backlink analysis, rank tracking over time.

## Prerequisites

- A Google service-account JSON with `webmasters.readonly` (Search Console)
  and `analytics.readonly` (GA4) scopes, plus viewer/delegated access on the
  target properties. Keep the JSON wherever secrets live on the machine
  running the pulls; pass its path in at run time.
- The GSC property string (`sc-domain:<domain>` for domain properties) and the
  GA4 numeric property ID. Read these from the target's own config or ask —
  never guess a property identifier.
- The exact pull commands, auth recipe, and limits live in `gsc-ga4-data-access.md`
  (verified live 2026-09-25). Read it before the first pull in any session.
- GA4 is optional. If it fails, run GSC-only and say so in the output.

## Workflow

### 1. Pull the data

Three GSC search-analytics calls, same date range (start = today−92 days,
end = today−2 days, because the newest 2 days are still unpopulated):

1. `dimensions:["query"]`, `rowLimit:25000` → per-query clicks, impressions, CTR, position.
2. `dimensions:["page"]`, `rowLimit:25000` → per-page totals.
3. `dimensions:["query","page"]`, `rowLimit:25000` → query-page pairs. This is
   the ground truth for which page a query currently lands on; it turns most
   guesses into observations.

Optional GA4 join: `runReport` with `dimensions:["landingPage"]`,
`metrics:["sessions","keyEvents"]` over the same range, for conversion signal
per landing page.

Completion criterion: all three JSON/CSV datasets exist and parse, and the
query file's row count is reported along with the data.

If `rowLimit` is reached, split the range into 30-day chunks and merge, or
page with `startRow`. If the dataset was truncated, state it in the output:
"query list truncated at the 25,000-row API cap."

### 2. Clean

Drop rows with fewer than 10 impressions. Drop branded queries — including
misspellings of the brand (fuzzy match). Drop obvious noise (site names,
reddit, youtube). Log how many rows were dropped and why; mention it in the
output. If the user attached CSVs instead of granting API access, parse theirs
(see companion pitfall on their format) and note the source differences.

Completion criterion: a clean table with one row per surviving query, each
with clicks, impressions, CTR, position.

### 3. Cluster queries into topic groups

Group queries that clearly express the same information need: shared head
term, synonyms, question forms of the same need. Split clusters when the same
stem serves different intents (e.g. "x pricing" vs "x vs y") — one stem can be
two clusters. A cluster is a judgment, not a fact: when unsure about members,
say so.

Completion criterion: every surviving query appears in exactly one cluster;
genuinely unclear queries sit in an explicit "unclustered" bucket, never
silently dropped. Total impressions per cluster = sum of member rows.

### 4. Classify gap type

For each cluster, decide exactly one type, citing the row(s) that triggered it:

| Type | Definition | Signature |
|---|---|---|
| Missing content | No page on the site targets the topic | No page in the pairs data and no slug/title match |
| Striking distance | Ranks 8–20 with meaningful impressions | Pairs show a page averaging pos 8–20 |
| Underperforming visibility | High impressions, CTR well below the site's own band for that position | Ranked page, CTR < half the site's median CTR at that position band |
| Answer-style page | Question or comparison need | Cluster head is how / what / why / best / vs / alternatives / when — a dedicated answer page can be built and is the cluster most likely to be cited in AI search |

A cluster can be both striking distance AND answer-style; record the primary
gap type from the table and note the answer-style angle in the action column.

`position` is an impression-weighted average across many SERP layouts, not a
rank — interpret 1–2 as excellent, 3–10 as page one, 11–20 as page two. Never
promise a specific post-change rank.

Benchmark CTR against the site's own data: bucket the clean pages into
position bands (1, 2, 3, 4–5, 6–10, 11–20), take each band's median CTR, and
compare rows to their band. Do not quote external band tables in the output.

Completion criterion: every cluster has a gap type plus the triggering rows;
the site's own CTR bands are computed, not assumed.

### 5. Match clusters to pages — and label the match quality

For each cluster, find the URL serving it: pairs data first (observed), then
slug/title keyword match (inference). Label every match:

- **Direct** — pairs data shows ranked pages for the cluster's queries, or the
  slug/title explicitly targets the head term.
- **Probable** — the page's theme plausibly covers it but neither direct
  signal exists.
- **Guess** — thin evidence; say what the evidence was and continue.

No page match at all ⇒ Missing content cluster.

Completion criterion: every cluster carries a labeled match or a "no page →
new page" call.

### 6. Prioritize

Priority reflects four inputs, in this order: impressions at stake, gap-type
impact (core-topic gap > snippet fix), effort (title rewrite < updating an
existing page < new page < new hub), and AI-citation upside for
question/comparison clusters. High = large impressions + small effort, or a
core-topic gap. Med = moderate volume or uncertain intent. Low = small volume
or high effort.

Completion criterion: the table is sorted by priority, and ties would be
obvious from the four inputs.

## Output shape

All numbers trace to pulled rows. After the table, two lists.

| Topic/Query cluster | Total impressions | Avg position | Gap type | Recommended action | Priority |

- Recommended action is one of: new page / update existing URL / rewrite title,
  with the specific URL when one exists.
- Impressions = sum across the cluster; avg position = impression-weighted
  average; both to 1 decimal.

**Top 5 content pieces to create first** — each with a suggested title, target
queries (verbatim from GSC), one line on search intent.

**Top 5 quick wins on existing pages** — each with the URL, the change, and
why the number justifies it.

Then a short assumptions note: match quality labels used, queries dropped
(brand/low impressions counts), truncation if any, and whether GA4 was joined.

## Common Pitfalls

1. **Inventing data.** Every number must trace to a pulled row. No memory
   keywords, no other tools' volumes, no extrapolated "this is probably a 5k
   volume term."
2. **Position ≠ rank.** Averaged across layouts; never say "you'll be #3."
3. **Absence from the pull is not absence from Google.** A query missing from
   the export either fell under the cap or had no impressions — say which.
4. **Clusters follow intent, not keyword stems.** One stem, two intents, two
   clusters.
5. **GA4 landing pages carry query strings and `(other)` buckets; GSC pages
   don't.** Normalize before joining; never join on raw strings.
6. **Branded queries sneak back via misspellings and brand+modifier combos.**
   Filter on fuzzy brand matches, not exact matching.
7. **GA4's keyEvents metric is just `keyEvents`.** If the pull 400s on a
   metric name, read the error — it names valid metrics.

## Verification Checklist

- [ ] Pulls ran live this session (or user CSVs were parsed) — no hand-typed numbers
- [ ] <10-impression and brand/noise filters applied; drop counts reported
- [ ] Every cluster: gap type + triggering rows + labeled page match (direct/probable/guess/no page)
- [ ] CTR benchmark computed from the site's own data, not an external table
- [ ] Prioritized table + top 5 new pages + top 5 quick wins present, verbatim GSC queries
- [ ] Assumptions note covers match guesses, drops, truncation, GA4 status
- [ ] Every number in the reply traces to a specific pulled row
