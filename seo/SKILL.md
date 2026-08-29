---
trigger: SEO, technical SEO, on-page SEO, structured data, JSON-LD, sitemap, meta tags, Open Graph, video SEO, rich results, search ranking
---

# SEO (Technical & On-Page)

Make a site's pages discoverable, crawlable, and rich-result-eligible in classic search engines (Google, Bing). This skill covers the *engineering* of SEO — markup, structured data, crawl infrastructure, performance — not content writing (see the `content-brief` skill for AEO content).

## Core Responsibilities

- Ensure every indexable page has a unique title, meta description, and canonical URL
- Emit valid structured data (JSON-LD) so pages qualify for rich results
- Provide crawl infrastructure: `sitemap.xml`, `robots.txt`, clean stable URLs
- Surface page content as crawlable text (transcripts, captions, descriptions)
- Protect Core Web Vitals (LCP, CLS, INP) and mobile usability
- Build internal linking so crawl depth stays shallow and equity flows
- Support off-page authority via link building (see `backlinks` and `link-building-strategy` sub-skills)


## Workflows

### Phase 1: Audit (always start here)

Inventory what exists before adding anything:

- `<head>`: is there a per-page `<title>` and `<meta name="description">`? A `<link rel="canonical">`?
- Social: Open Graph (`og:*`) and Twitter card tags?
- Structured data: any `<script type="application/ld+json">`? Validate with Google's Rich Results Test.
- Crawl: does `robots.txt` exist and reference a sitemap? Does `sitemap.xml` exist and list real URLs?
- Indexability: are important pages returning 200, canonical to themselves, not `noindex`?
- Content depth: is the page's substance locked in images/video/JS, invisible to crawlers?

Output a gap list ranked by impact.

**Also check edge cases** — if rankings are flat despite standard SEO fixes, run the `technical-edge-cases` sub-skill audit: GSC URL Parameters, URL Inspection (compare Original vs. Rendered HTML), Coverage report for indexation gaps, Chrome DevTools Security tab for mixed content, and charset verification.

### Phase 2: Foundational fixes (Tier 1 — highest ROI)

1. **Per-page metadata** — unique `<title>` (~50-60 chars) and `<meta name="description">` (~140-160 chars) derived from the page's primary entity. Provide a layout slot (e.g. `content_for :description`) with a sensible sitewide default.
2. **Canonical + host normalization** — self-referencing `<link rel="canonical">`; 301 non-canonical hosts (www↔apex, trailing slashes) to one form.
3. **Sitemap + robots** — a dynamic `sitemap.xml` listing every indexable URL with `lastmod`; reference it from `robots.txt`. Submit to Google Search Console + Bing Webmaster Tools.
4. **Primary structured data** — add the JSON-LD type that matches the page's main entity (see Decision Framework). This is what unlocks rich results.

### Phase 3: Content depth & entity graph (Tier 2 — biggest long-term lever)

- **Make content crawlable text.** If the value is inside a video/image/app, render the transcript, caption, or structured breakdown as visible on-page HTML. A page of 20 words can't rank; the same lesson as 300 words of marked-up text can.
- **Hub pages** — an index/glossary page that tables every item and links to each detail page. Earns rankings for the head term and shortens crawl depth.
- **Site-wide entity schema** — `Organization` + `WebSite` JSON-LD with `sameAs` pointing at every official social profile, so engines resolve the brand as one entity. Add `BreadcrumbList` and `ItemList`/`CollectionPage` on listings.

### Phase 4: Performance & polish (Tier 3)

- Open Graph + Twitter `player`/`summary_large_image` cards (shared links render a thumbnail/preview).
- Core Web Vitals: lazy-load below-the-fold media (`loading="lazy"`), avoid many heavy third-party iframes on listing pages (use poster tiles linking to detail pages), set explicit image/media dimensions to prevent CLS.
- `alt` text on meaningful images; one `<h1>` per page; semantic headings.
- `inLanguage`/`hreflang` for multilingual content; pagination strategy (`rel=next/prev` is deprecated, but keep crawlable paginated links) as catalogs grow.

### Phase 5: Verify

- Google Rich Results Test + Schema.org validator on representative pages.
- `curl` each new route: confirm 200, canonical, title/description, JSON-LD present.
- Search Console: submit sitemap, watch Coverage + Enhancements for the schema types you added.

## Decision Framework

**Which JSON-LD type?** Match the page's dominant entity:

- Short-form / vertical video → `VideoObject` (name, description, thumbnailUrl, uploadDate, embedUrl/contentUrl, duration, inLanguage). The single highest-value type for a video site.
- Article / blog post → `Article` / `BlogPosting`.
- Product → `Product` + `Offer` + `AggregateRating`.
- How-to steps → `HowTo`; recurring Q&A → `FAQPage` (also a big AEO win — see `aio` skill).
- Course / lesson → `Course` / `LearningResource`.
- Any listing page → `ItemList` / `CollectionPage`; any nested page → `BreadcrumbList`.
- The whole site → `Organization` + `WebSite` (once, in the layout).

**Build vs. defer:** Do Tier 1 before any content work — it's shared plumbing (a head-meta block + a JSON-LD helper + sitemap/robots) that everything else builds on. Defer Tier 3 polish until Tier 1+2 are shipped and indexed.

**Render-blocking trade-off:** Prefer server-rendered HTML for anything you want indexed. If content is client-rendered, confirm Googlebot sees it (URL Inspection → rendered HTML) or pre-render it.

## Collaboration Patterns

- **`content-brief` skill** — owns the *words* (answer blocks, PAA-mapped H2s, EEAT). This skill owns the *markup and infrastructure* that make those words eligible for rich results. Hand off: content-brief produces the copy; SEO wraps it in title/description/schema.
- **`aio` skill** — shares the JSON-LD plumbing. SEO adds `VideoObject`/`Article`; AIO adds `FAQPage`/`llms.txt`/crawler policy on top. Do them in one batch when possible.
- **`backlinks` skill** — supplies the off-page half of SEO. This technical SEO skill makes pages linkable; the backlinks skill supplies the source database and outreach playbook to acquire those links.
- **`link-building-strategy` skill** — execution arm for link acquisition. SEO ensures the landing page is technically flawless; the strategy skill provides the outreach scripts and campaign frameworks.
- **`ruby-on-rails` skill** — implements the routes, helpers, and views; SEO supplies the spec (which tags, which schema, which routes need a sitemap entry).
- **`technical-edge-cases` sub-skill** — companion for edge case audits. Run after the standard SEO audit if rankings are flat. Covers parameter handling, JS rendering, infinite scroll, mixed content, tracking params, and charset issues.
- **`indexing-and-freshness` sub-skill** — after Tier-1 crawl infra, to speed up discovery/recrawl: IndexNow (Bing/Yandex; Google isn't a participant), the dead sitemap-ping / Indexing-API myths, honest `lastmod`, and video sitemaps (`<video:video>`). Run when the site publishes frequently.
- **`thin-page-audit` sub-skill** — when pages are crawled but **not indexed** ("Crawled/Discovered – currently not indexed"). Measure per-template main-content words + unique-text coverage, then thicken the thin templates (transcripts, FAQ, unique prose). Run when a large templated section has a low indexed-count.

## Key Principles

- **Crawlable text beats clever markup.** Schema amplifies content; it can't substitute for it.
- **One canonical URL per piece of content.** Duplicates split ranking signals.
- **Unique title + description per page.** Templated duplicates waste the strongest on-page signals.
- **Validate everything.** Invalid JSON-LD silently disqualifies rich results — always run the Rich Results Test.
- **Ship Tier 1 first.** Metadata + canonical + sitemap + primary schema is ~80% of the gain for ~20% of the work.
- **Measure in Search Console.** Indexing and enhancement reports are ground truth, not local guesses.
