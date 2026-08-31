---
trigger: AIO, AEO, answer engine optimization, AI optimization, LLM SEO, get cited by ChatGPT, Perplexity, Google AI Overviews, llms.txt, AI crawlers, GPTBot, measure AI visibility, LLM rank tracking, AI referral traffic
---

# AIO — AI / Answer-Engine Optimization

Get a site's content surfaced and *cited* by answer engines and assistants — Google AI Overviews, ChatGPT, Perplexity, Claude, Bing Copilot. Classic SEO optimizes for a ranked list of links; AIO optimizes to *be the answer* an AI quotes. Pairs with the `seo` skill (shared markup) and the `content-brief` skill (AEO writing).

## Core Responsibilities

- Make each page answer one question completely, in self-contained, extractable text
- Emit machine-readable Q&A and entity data (`FAQPage`, `Organization`) for lifting
- Publish an LLM-facing site map (`llms.txt` / `llms-full.txt`)
- Set a deliberate AI-crawler policy in `robots.txt` (allow vs. block, per bot)
- Establish entity clarity and freshness signals so AI trusts and attributes the source

## Workflows

### Phase 1: Decide crawler policy (do this first — it's a business decision)

AI crawlers fall into two buckets; you can allow/deny each independently in `robots.txt`:

- **Retrieval/citation bots** (drive visibility *now*): `OAI-SearchBot` (ChatGPT search), `PerplexityBot`, `Google-Extended` (AI Overviews/Gemini grounding), `Bing` (Copilot). Allowing these is how you get cited.
- **Training bots** (feed model training): `GPTBot`, `ClaudeBot`/`anthropic-ai`, `CCBot` (Common Crawl), `Google-Extended` (also gates training).

**Recommendation for marketing/funnel sites: allow both.** Visibility and citations outweigh training-data concerns when the whole point is reach. For paywalled/proprietary content, allow retrieval bots but consider blocking training bots. Make the call explicitly and record it.

```
# robots.txt — allow AI crawlers
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: CCBot
Allow: /

Sitemap: https://example.com/sitemap.xml
```

### Phase 2: Make pages extractable

- **Answer block at the top.** The first thing on the page is a complete, standalone answer to its core question (40-150 words) — phrase, definition, the direct answer — *before* any video, hero, or fluff. AI lifts the first clean, complete answer it finds.
- **One question per page; one H2 per sub-question.** Each section must answer its heading without the reader (or model) needing surrounding context. Mirror real "People Also Ask" phrasing in the headings.
- **Structured facts as text.** Tables, definition lists, and labeled fields (term / reading / meaning / when-to-use) are highly liftable. Don't bury facts in prose or media.
- **Self-contained sections.** No "as mentioned above" — models read sections in isolation.

### Phase 3: Machine-readable layer

- **`FAQPage` JSON-LD** — turn the page's core Q&A into structured data: `Q: How do you say "X" in Japanese? A: <phrase> (<romaji>) — <meaning>`. Answer engines preferentially ingest structured Q&A. (`HowTo` for procedures.)
- **`Organization` + `sameAs`** — define the brand entity once, site-wide, linking every official profile, so assistants resolve and attribute "who said this."
- **Dates** — `datePublished` / `dateModified` (and `uploadDate` for video). AI engines favor fresh, dated, citable sources.

### Phase 4: `llms.txt`

Publish a plain-Markdown file at `/llms.txt` describing the site for LLMs: a one-line site summary, then a curated list of key URLs with one-line descriptions (think "sitemap written for a model"). Optionally `/llms-full.txt` with the full text of priority pages inlined. Generate it from the same data that builds the sitemap.

```
# Kōfuku — Japanese for travelers
> Short bilingual reels teaching the exact phrases tourists need in Japan.

## Phrases
- https://example.com/videos/tourist-konbini: How to order hot food at a convenience store ("kore, kudasai")
- https://example.com/videos/tourist-takkyubin: Forward your luggage hotel-to-hotel ("nimotsu o okuritai desu")
```

### Phase 5: Verify

- Fetch pages as the bots do: `curl -A "PerplexityBot" <url>` and confirm full content renders server-side (no JS gate).
- Confirm `robots.txt` allows the intended agents; check server logs for `GPTBot`/`PerplexityBot`/`OAI-SearchBot` hits over the following weeks.
- Ask the assistants directly ("How do you say X in Japanese?") and watch for your domain appearing as a cited source; iterate on the answer block where it doesn't.

For ongoing measurement — citation-rate tracking, AI referral traffic, crawler coverage, share-of-voice — see the **`measurement.md`** sub-skill. Optimize here; track there.

## Decision Framework

- **Allow or block a given AI bot?** Allow if the goal is reach/citations (marketing, docs, funnels). Block training bots only if the content is a proprietary moat. Retrieval bots should almost always be allowed if you want to appear in AI answers at all.
- **Where does the answer go?** The single most-cited content is a complete answer in the first paragraph. If you must choose one AIO change, make it the top-of-page answer block.
- **Structured data vs. prose?** Both — prose for humans, mirrored `FAQPage` JSON-LD for machines. When they conflict, keep them consistent (engines cross-check).
- **Freshness:** if content changes, bump `dateModified`. Stale-looking pages lose to dated competitors in AI answers.

## Collaboration Patterns

- **`content-brief` skill** — the upstream writing discipline (answer blocks, PAA→H2 mapping, EEAT). AIO turns that copy into the extractable + machine-readable layer and sets crawler policy. They're two halves of the same play.
- **`seo` skill** — shares the JSON-LD and crawl plumbing. SEO targets ranked links + rich results (`VideoObject`, sitemap); AIO targets citations (`FAQPage`, `llms.txt`, crawler allow-list). Implement in one batch — same `<head>` and helper code.
- **`ruby-on-rails` skill** — implements `llms.txt`/`robots.txt` routes, the FAQ schema helper, and answer-block partials from this spec.

## Key Principles

- **Be the answer, not a result.** Structure every page so a model can quote it verbatim and attribute it.
- **Lead with the complete answer.** First paragraph, no preamble — that's what gets lifted.
- **Self-contained sections.** Each heading answers its question alone; models read out of order.
- **Allow the crawlers you want citations from.** You can't be cited by a bot you blocked.
- **Mirror facts in structured data.** `FAQPage` + `Organization` + dates make content liftable and attributable.
- **Freshness and entity clarity build trust.** Dated, well-attributed sources win AI answers.
