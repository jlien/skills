---
trigger: citation hub, statistics page, stats hub, linkable asset, backlink magnet, earn backlinks without outreach, citable content, citation bait, be the source, statistics roundup
---

# Citation Hub — Build the Content Asset Everyone Links To

Earn links passively by publishing the most citable statistics asset in a niche. Instead of begging for links (outreach) or copying competitors (skyscraper), you build the **primary reference writers cite by reflex** — and the links come to you. Distinct from the `skyscraper-approach` skill (outreach to competitor linkers) and complementary to the `aio` skill (extraction layer for the same page).

## Why It Works

Nearly every blog post, journalist, SaaS landing page, and now every AI answer needs a number to back up its claim:

- "The market is worth $$$."
- "Y% of teams already do this."

The person who publishes the first credible, structured, dated source for the number **becomes the claim** — and gets the link. The same asset gets cited inside ChatGPT, Google AI Overviews, and Perplexity, so one page compounds both SEO links and AI mentions.

**Measured results (from the tactic's author, five pages May–Aug 2026):**

- 80+ backlinks across five pages, zero cold outreach
- 10 links from DR 60+ sites; one page earned 20 links on its own
- ~40% of anchor text was the statistic itself ("$10.87B market," "56% wage premium") — people quote the numbers
- Links compounded over time: 23 landed in a single month once the page had traction
- Host-site DR doesn't matter much: one page on a small site still earned 5 links

## The Mechanism

### Step 1: Pick the head term people are forced to cite

Target citation-intent queries, not commercial ones:

- ❌ "Best accounting software" — buyers, not writers
- ✅ "Accounting statistics 2026" — the query a writer types at 11 PM with a deadline tomorrow

Citation-intent queries have **permanent demand** (every new post in the niche needs the same stats) and low competition, because almost nobody builds them. Then keyword-research every section and sub-section until the topic is covered wall to wall — you never know what someone will look for.

### Step 2: Aggregate 50+ statistics from primary sources only

This is where most roundups fail: they copy numbers from other roundups. Trace every stat to the **entity that produced it** — government body, earnings filing, original research study, regulator dataset. Sometimes that means hopping paywalls (library access, archive copies) to reach the primary text.

Verify every URL loads and the number actually appears on that page. Journalists and search engines trace citations to the root before they link; if your chain of provenance is solid, you're the shortcut they were looking for.

### Step 3: Structure the page to be cited, not just read

- **Key Takeaways block up top**: 10–14 one-line, quotable stats — liftable without reading the page
- **Question-style headings** that match the exact sub-questions AI breaks a query into (see the `aio` skill), each answered in the first sentence below the heading
- **Every stat attributed** to its publisher with a date and a link
- **Each number appears exactly once** — no fluff between facts, nothing that muddies extraction

### Step 4: Stamp it fresh and keep it alive

Freshness is both a ranking signal and a citation signal — a "statistics 2026" page beats a stale 2023 one on recency alone. Add the year to the title, show `datePublished`/`dateModified` (see `aio`), and schedule refreshes so the page stays current instead of decaying.

That's the whole play: build the most citable asset in the niche, and the links and AI mentions come to you.

## Workflows

### Phase 1: Vertical & Head Term Selection

1. Choose your vertical or a client's vertical
2. Confirm primary data exists: government datasets, regulator filings, industry associations, vendor reports, earnings filings. (Almost every B2B category has usable primary data. If yours genuinely doesn't, pick a different vertical instead of faking it with secondary sources.)
3. Pick the citation-intent head term: `<topic> statistics <year>`
4. Estimate editorial demand: how many blogs, journalists, and AI answers in this niche need numbers weekly? Highest editorial interest = fastest link velocity.

### Phase 2: Research & Verification

1. Break the head term into every section and sub-section (keyword research wall to wall)
2. For each section, hunt primary sources first; use roundups only as **leads** — never as the cited link
3. For every stat, record: the number, the producing entity, the source URL, the date of the data, and pull quotes/context
4. Open each URL and confirm the page loads and the number is really there (this is the step everyone skips)
5. Target 50+ verified stats per page — dense enough that a writer looking for one number finds twelve more worth citing

### Phase 3: Build the Page

Build per the Step 3 structure (Key Takeaways top block, question-style H2s, one attribution each). Add the machine-readable layer from the `aio` skill — `datePublished`/`dateModified`, `FAQPage`/`Article` JSON-LD, and the structured-facts formatting so both search crawlers and LLMs can lift it cleanly.

### Phase 4: Refresh Loop

1. Schedule quarterly (at minimum) refresh cycles to re-verify sources and add new data
2. Move new findings into the Key Takeaways block; date every change
3. Reissue the asset under the current year and keep a visible revision history — the dated asset wins the citation

## Decision Framework

- **Which head term?** The one writers type at 11 PM when they need a stat, not the one buyers type when shopping. Search results full of roundups full of unattributed numbers = perfect target.
- **Secondary-source roundup as a lead?** Only for discovery. Never re-host a number you haven't traced to its producer.
- **How many stats?** 50+ per hub. Density drives incidental discovery — a writer who finds one number browses and links to more.
- **Anchor text strategy?** None needed. Make every stat self-quoting; the number itself is the hook.
- **Paywalled primary source?** Cite it and link it anyway (provenance matters more than the click), but do the verification hop yourself before publishing.
- **Skyscraper or Citation Hub?** Skyscraper targets an existing ranked page and harvests its linkers by outreach. Citation Hub creates a new asset category and earns links passively. They compose: use citation-intent research when you'd otherwise have no outreach targets.

## Key Principles

- **Be the claim, not the roundup.** The first credible source for a number gets cited everywhere.
- **Primary sources only.** Trust comes from provenance; copied roundups are invisible noise to journalists and LLMs.
- **Structure for lifting, not reading.** Quotable takeaways block, question headings, one stat per line.
- **Every stat is a hook.** ~40% of earned anchors were the statistic itself — a verified number is a pre-written anchor.
- **Freshness compounds.** Dead pages lose citations to current-year ones; keep the asset alive.
- **No begging.** No PBNs, no link farms, no cold email — the structure earns the links.

## Source

- ["Stop Begging for Links. Build the Content Asset everyone links to." — Flavio Amiel, X (Sep 2026)](https://x.com/i/article/2098486326802743298)
- Example hub: [Citation-Led Statistics Hub (SWAT SEO demo)](https://swatseo-stats.vercel.app/)
- Related skills in this repo: `aio` (extraction + structured-data layer for the same page), `seo/link-building-strategy` (outreach-based complement), `content/skyscraper-approach` (competitive alternative)
