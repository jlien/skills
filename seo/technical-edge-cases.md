---
trigger: technical SEO edge cases, parameter handling, JS rendering, infinite scroll, mixed content, tracking parameters, charset issues, crawl waste, URL parameters, rendering audit, indexation audit
---

# Technical SEO Edge Cases

Advanced technical SEO issues that affect 10-40% of sites but rarely show up in standard audits. These are edge cases that, when fixed, can recover +2-3 ranking positions.

## Core Responsibilities

- Audit and fix URL parameter handling to prevent crawl waste and authority dilution
- Diagnose JavaScript rendering mismatches that cause content to go unindexed
- Fix infinite scroll patterns that leave most content unindexed
- Detect and remediate HTTP/HTTPS mixed content after migration
- Block duplicate tracking parameters from diluting rankings
- Verify character encoding so non-English content indexes correctly

## Edge Case Audits & Fixes

### 1. Parameter Handling Confusion (affects ~23% of sites)

**Problem:** URLs with different query parameters are treated as separate pages:
- `example.com/product`
- `example.com/product?ref=email`
- `example.com/product?utm_source=twitter`
- `example.com/product?sort=price`

Each variation gets crawled separately. Internal links split across versions. Ranking authority divides by the number of param variations. Result: a page that should rank #3 instead ranks #8.

**Audit:**
1. Google Search Console → Settings → URL Parameters
2. Review which parameters Google has detected as generating duplicate content
3. Check the Coverage report for pages indexed with query parameters

**Fix options (in order of preference):**
1. **Google Search Console URL Parameters** — Mark parameters as "doesn't change page content" (UTM parameters → mark as UTM type). This tells Google to ignore them for indexing.
2. **Canonical tags** — Add `<link rel="canonical" href="https://example.com/product">` on every variant page. More portable (works for all search engines), but relies on proper implementation everywhere.
3. **robots.txt** — Block tracking/parameter URLs from crawling (see Edge Case #5 below).

### 2. JavaScript Rendering Mismatch (affects ~31% of sites)

**Problem:** Googlebot crawls a JS-heavy page. The initial HTML has minimal content. JavaScript renders the full content, but crawling and indexing are separate passes — Google might index the empty version, not the rendered one. The page has content users can see but Google doesn't index it.

**Audit:**
1. Google Search Console → URL Inspection → paste any JS-heavy URL
2. Compare two views:
   - **Original HTML** (what the crawler first sees)
   - **Rendered HTML** (what a browser sees after JS executes)
3. If the two differ significantly in meaningful content → you have a rendering problem

**Fixes:**
1. **Server-side rendering (SSR)** — Use Next.js, Nuxt.js, or any framework that renders HTML on the server so the crawler gets the final content immediately.
2. **Pre-rendering** — Serve pre-rendered HTML snapshots to crawlers (works for static sites).
3. **JSON-LD schema markup on server** — Add structured data that doesn't depend on JS execution. Even if the visual content fails to render, the structured data is indexed.
4. **Ensure fast client-side rendering** — If SSR isn't possible, make JS bundles small enough that Googlebot's 2-pass rendering completes within its time budget.

### 3. Infinite Scroll Breaking Indexation (affects ~18% of sites)

**Problem:** A page loads 10 products initially. Scrolling triggers dynamic loading of more content. Google crawls the initial load, indexes only those 10 products, and never discovers the dynamically-loaded content below. Example: an e-commerce site with 10K products only gets 1,500 indexed (15%).

**Audit:**
1. Google Search Console → Coverage report → count indexed pages vs. actual product/detail pages
2. Check if dynamically-loaded pages appear in the sitemap or are reachable via paginated links
3. Test: disable JavaScript and see if all products are still accessible via links

**Fixes:**
1. **Paginated HTML links** — Add standard `<a href="/products?page=2">Next Page</a>` and `<a href="/products?page=3">Page 3</a>` links. Googlebot follows these.
2. **`rel="next"` / `rel="prev"`** — Indicate pagination sequence (note: Google has stated this is deprecated, but still used by Bing; prefer paginated links + canonical).
3. **Complete sitemap** — List every product URL in `sitemap.xml` so Google discovers them regardless of site navigation.

### 4. HTTP/HTTPS Mixed Content (affects ~12% of sites)

**Problem:** Site migrated from HTTP to HTTPS but old content still loads images, scripts, or stylesheets via HTTP URLs. Browsers block mixed content (active and passive). Pages display broken (images missing, scripts failing). Google sees broken pages → poor UX → ranking penalty.

**Audit:**
1. Open a representative page in Chrome
2. DevTools → Security tab → view "Mixed content" warnings
3. Look for: images loaded via `http://`, scripts/stylesheets via `http://`, iframes via `http://`
4. Check Core Web Vitals — mixed content often causes LSP failures

**Fixes:**
1. **Replace hardcoded HTTP URLs** — Search database/content for all `http://` URLs in images, scripts, stylesheets. Replace with `https://`.
2. **Protocol-relative URLs** — Change `http://example.com/image.jpg` to `//example.com/image.jpg`. The browser picks the correct protocol automatically. This is a good short-term fix but less explicit than full HTTPS URLs.
3. **Content Security Policy (CSP)** — Use `upgrade-insecure-requests` directive to auto-upgrade HTTP to HTTPS.
4. **Verify** — Re-test in Chrome DevTools Security tab → confirm zero mixed content warnings.

### 5. Duplicate Tracking Parameters (affects ~27% of sites)

**Problem:** Tracking code adds parameters to internal links: `/page?utm_source=email&utm_medium=email`. Google crawls the parameter version and indexes it as a separate page from the canonical URL. This wastes crawl budget and dilutes ranking authority.

**Audit:**
1. Search Console → URL Parameters → check if tracking parameters are creating indexed variants
2. Site search in Google: `site:example.com utm_source` — see how many parameter-version pages are indexed
3. Check Coverage report for "URLs with parameters" or "duplicate without user-selected canonical"

**Fixes:**
1. **`robots.txt` blocking** — Block tracking parameters from crawling:
   ```
   Disallow: /*?utm_source=
   Disallow: /*?utm_medium=
   Disallow: /*?fbclid=
   Disallow: /*?gclid=
   Disallow: /*?ref=
   ```
   This is the most reliable fix — prevents crawling entirely.
2. **Canonical tags** — Add `<link rel="canonical" href="/page">` on pages loaded with tracking params. Works but depends on proper implementation.
3. **Self-canonicalization** — In your app, when rendering a page with tracking parameters, always self-referencing canonical to the clean URL.

### 6. Charset Issues (affects ~8% of sites, critical for i18n)

**Problem:** Meta charset declares `UTF-8` but actual encoding is `ISO-8859-1` or another encoding. Non-English characters display as gibberish. Google can't understand the content → can't rank for non-English keywords. Common on international sites with European languages, Asian characters.

**Audit:**
1. Open a page in browser → view page info → check reported character encoding
2. Look for garbled characters: `ä` showing as `Ã¤`, `ñ` as `Ã±`, CJK characters as `???`
3. Check `Content-Type` header vs. `<meta charset>` — they should match
4. Verify database encoding matches the declared encoding

**Fixes:**
1. **Ensure `<meta charset>` matches actual encoding** — Set to `UTF-8` and ensure all layers (database, application, template) use UTF-8:
   ```html
   <meta charset="UTF-8">
   ```
2. **Database encoding** — Verify tables use `utf8mb4` (MySQL) or `UNICODE` (PostgreSQL) — not `latin1` or `utf8mb3` which can't store 4-byte characters.
3. **Content-Length/Content-Type headers** — Ensure server sends `Content-Type: text/html; charset=utf-8`.
4. **Verify** — Use browser's character encoding detection: look for the encoding indicator in the URL bar or page info.

## Decision Framework

**Which edge case to prioritize?** Rank by prevalence × impact:

| Edge Case | Prevalence | Impact (lost rankings) | Priority |
|---|---|---|---|
| JS rendering mismatch | 31% | Content unindexable | 🔴 Critical |
| Duplicate tracking params | 27% | Authority dilution | 🔴 Critical |
| Parameter handling | 23% | Authority dilution + crawl waste | 🔴 Critical |
| Infinite scroll | 18% | ~85% of content unindexed | 🟡 High |
| Mixed content | 12% | Broken pages + ranking penalty | 🟡 High |
| Charset issues | 8% | Non-English content unreadable | 🟢 Medium |

**Audit cadence (weekly rotation):**
- Week 1: Parameter handling audit (GSC URL Parameters)
- Week 2: Rendering audit (GSC URL Inspection → Fetch and Render)
- Week 3: Indexation audit (GSC Coverage report)
- Week 4: Mixed content check (Chrome DevTools → Security tab)
- Week 5: Charset verification (browser encoding detection)

## Collaboration Patterns

- **`SEO` skill** — This is a companion to the main Technical SEO skill. The main skill covers standard infrastructure (canonical, sitemaps, structured data, CWV). This sub-skill covers edge cases that the standard audit misses. Run this audit after the standard SEO audit, or when rankings don't respond to standard fixes.
- **`ruby-on-rails` skill** — Implements the fixes: canonical tags, protocol-relative URLs, sitemap updates, robots.txt edits, database encoding migration. Hand off: "Add self-referencing canonical on pages with tracking params" or "Change image URLs from http to https in the database."
- **`aio` skill** — Shares interest in rendering fixes — AIO benefits from server-rendered content for LLM crawling.

## Key Principles

- **Edge cases hide where standard audits don't look.** GSC URL Parameters and the Security tab are blind spots for most technical SEO checklists.
- **Parameter handling is the cheapest fix.** Setting URL parameters in GSC takes 2 minutes and recovers crawl budget + ranking authority immediately.
- **Rendering problems are invisible without URL Inspection.** The page looks fine to users but Google sees empty HTML. Always compare Original vs. Rendered HTML.
- **Infinite scroll needs a crawl-friendly fallback.** Paginated links or a complete sitemap — not just dynamic loading.
- **Mixed content is a CWV killer.** One HTTP image can fail LCP. Audit after any HTTPS migration.
- **Charset issues make i18n SEO impossible.** Fix the encoding pipeline end-to-end — database, app, template, response header — not just the meta tag.
- **robots.txt blocking is more reliable than canonical for tracking params.** It prevents crawling entirely; canonical still wastes crawl budget.
