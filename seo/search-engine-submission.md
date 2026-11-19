---
trigger: search engine submission, submit site to search engines, submit URL, first-time indexation, new site launch SEO, IndexNow bulk submit, Brave submit URL, Bing Webmaster Tools, engine coverage
---

# Search Engine Submission (channel map + first-time bulk indexation)

Sub-skill of `seo`. Covers the **one-time act of getting a site into each major
engine's index** — which submission channel exists per engine, which don't exist,
and the bulk-initial-submission playbook for a new or recently expanded site.
For **ongoing freshness** (pinging engines when individual pages publish), see
the `indexing-and-freshness` sub-skill — this one is the launch-day inventory;
that one is the steady-state pipeline.

## The channel map (what exists per engine, verified)

Lead with the truth — most "submit your site" advice is stale:

- **Google** — no general submission endpoint. Get indexed via: `robots.txt`
  (allow + sitemap reference), a sitemap index submitted in Search Console
  (verify the property first, Domain property via DNS TXT), internal links from
  already-indexed pages, and — for one urgent URL — "Request indexing" in the
  GSC URL Inspection tool (manual, ~10–20/day, not automatable). Bulk index
  status is auditable via the URL Inspection API (one URL per call, ~0.2s
  spacing, 2–3 day data lag after fixes).
- **Bing / Yahoo / DuckDuckGo** — Bing Webmaster Tools (import the GSC property
  to skip re-verification) gives crawl diagnostics for the Bing index, which
  powers Yahoo and DuckDuckGo. Fast lane is IndexNow (see below).
- **Yandex / Seznam / Naver** — IndexNow participants; each also has its own
  webmaster portal if you want diagnostics. Usually IndexNow alone is enough.
- **Brave** — no webmaster console. The only channel is the public form at
  `search.brave.com/submit-url`: enter a URL, pass a human-verification check,
  done. There is no API and no account.
- **Apple (Siri/Spotlight)** — no submission portal at all. The only lever is
  robots.txt policy: explicitly `Allow` `Applebot` / `Applebot-Extended` and
  let the sitemap do the rest.
- **AI answer engines (Perplexity, ChatGPT, Claude)** — no submission channel;
  coverage follows their crawlers. Expressly welcome the crawler user-agents in
  robots.txt (see the `aio` skill for the AI-crawler policy surface).

## Brave submit-url: operational notes

The form is finicky in ways the docs don't say:

- It is **one URL per IP per session**. The first submission passes human
  verification and confirms "Success". Immediate follow-up submissions are
  **silently refused** — no error, the form just resets without a verification
  flow. Don't loop retries against it.
- Submit the **homepage** — it's the seed Brave crawls from to find everything
  else. Per-hub submissions are a nice-to-have, not a requirement.
- If more URLs matter, wait (the limit appears to reset daily) and submit one
  more per session from a fresh browser context.

## First-time bulk submission playbook

For a new site, or an existing one that grew a large new section:

1. **Robots.txt** — `User-agent: *` allows the content paths, disallows
   admin/API, and references the sitemap URL.
2. **Sitemap index** — `/sitemap.xml` pointing at per-class files
   (main hubs, videos, blog, posters, quizzes …) with honest `lastmod` dates.
   Per-class files get their own fetch cadence per engine.
3. **Verify the IndexNow key file is live** before submitting anything:
   `https://<host>/<key>.txt` must return 200 with the bare key as the body.
4. **Bulk-submit all sitemap URLs to IndexNow** in **≤500-URL batches** —
   the protocol accepts large `urlList`s but batches of 500 through
   `api.indexnow.org` are reliably accepted. Either POST direct with
   `{ host, key, keyLocation, urlList }`, or wrap a token-authed endpoint on
   your own app so CI/pipelines can call it without handling the key.
   This is the one-time exception to "don't blast the whole sitemap" —
   on first submission there is no such thing as "what changed" yet.
5. **Submit the homepage to Brave** via the form (one URL, see above).
6. **Google**: submit the sitemap index in GSC, then wait. Audit ~3 days
   later with the URL Inspection API and bucket coverage
   (`Submitted and indexed` / `Discovered - currently not indexed` /
   `URL is unknown to Google`) — see `thin-page-audit` for the
   crawled-but-not-indexed diagnosis.
7. **Optional**: import the GSC property into Bing Webmaster Tools for
   Bing-side crawl diagnostics.

## Decision framework

"I want engine X to index my site" →

- **Google** → sitemap in GSC + internal links; URL Inspection API to audit.
- **Bing/Yahoo/DuckDuckGo** → IndexNow bulk push (one-time) + publish-event
  pings (steady state, see `indexing-and-freshness`).
- **Yandex/Seznam/Naver** → same IndexNow push covers them.
- **Brave** → homepage through the submit-url form, once, then let it crawl.
- **Apple** → robots.txt welcome + sitemap; no other lever exists.
- **Any engine, page still missing after weeks** → check the crawl-hub chain
  first (is the page linked from an *indexed* page?), before assuming a
  submission problem. Orphan pages stay unindexed no matter what you submit.

## Key Principles

- **No engine except IndexNow participants offers a programmatic "index me
  now"** — for Google, submission means making discovery easy and auditing
  coverage, not pushing URLs.
- **The homepage is the seed.** Every engine's crawler expands from pages it
  already has; submitting the homepage of an uncrawled site is worth more
  than twenty deep URLs.
- **Verify the key file before submitting through IndexNow** — a 404 on
  `<key>.txt` means every URL in the payload is silently discarded.
- **Rate limits are silent.** Brave's form and several portals fail with no
  error state; a missing success message after a submit is a failure, not a
  pending state.
