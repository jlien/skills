# Indexing & Freshness (get pages found, recrawled, and into video results)

Sub-skill of `seo`. Covers the mechanisms that speed up **discovery and recrawl**
of new/changed pages — and, just as important, corrects the ones that no longer
work. Use after Tier-1 (sitemap/robots/canonical) is in place, whenever the site
publishes frequently and you want new URLs picked up fast.

## The honest landscape (what still works)

Half the "notify the engines" advice online is dead. Lead with the truth:

- **Sitemap ping is gone.** `GET google.com/ping?sitemap=…` (and Bing's) was
  **removed in 2023**. Don't add it; don't recommend it.
- **Google's Indexing API is JobPosting/BroadcastEvent-only.** It is *not* a
  general "tell Google about my new page" endpoint. Using it for articles/products
  is unsupported and against ToS (it may appear to work, then stop). Don't build on it.
- **There is no supported programmatic "notify Google"** for ordinary pages.
  Google finds new URLs via the **sitemap + internal links** on its own crawl
  cadence. The levers you *do* control: an accurate sitemap with fresh `lastmod`,
  shallow internal linking, and — for one urgent URL — **"Request indexing"** in
  the GSC URL Inspection tool (manual, ~10–20/day, not automatable).
- **IndexNow works — for Bing, Yandex, Seznam, Naver (NOT Google).** This is the
  one real "ping on publish." Worth it wherever those engines send meaningful traffic.

State this split plainly to whoever you're advising, so nobody wires up a dead ping.

## IndexNow (instant Bing/Yandex recrawl)

A tiny protocol: prove you own the host with a key file, then POST changed URLs.

1. **Key + ownership file.** Generate a hex key; host it at
   `https://<host>/<key>.txt` containing exactly the key (the key is semi-public —
   it only proves ownership). Serve it as a static file.
2. **Submit on add/update.** POST JSON to `https://api.indexnow.org/indexnow`:
   ```json
   { "host": "example.com", "key": "<key>",
     "keyLocation": "https://example.com/<key>.txt",
     "urlList": ["https://example.com/new-page", "..."] }
   ```
   One request accepts many URLs (up to 10k). 200/202 = accepted.
3. **Wire it to real publish events**, not a cron sweep:
   - DB-backed content → a model `after_commit` that fires when the record becomes
     public (guard on the status transition, not every save, or you'll re-ping on
     unrelated edits).
   - File/registry content with no runtime event (e.g. a version-controlled page
     registry) → ping from the deploy/publish pipeline after the push.
4. **Make it best-effort.** Never raise into a request or callback; log and move
   on. Gate to production only (don't ping from dev/test).

Pitfalls: only submit URLs on the verified host; don't submit `noindex`/redirecting
URLs; don't blast the whole sitemap on every deploy (submit what changed).

## Sitemap freshness — `lastmod` that means something

`lastmod` is a recrawl hint Google *does* use — but only if it's honest.

- **Per-item `lastmod`** = the item's real last-modified date (not "today" on every
  build). Faking it site-wide gets `lastmod` ignored.
- **Section/index pages get a `lastmod` too** = the freshest item they list
  (e.g. `/blog` `lastmod` = newest article's date). Without it, hubs look static and
  get recrawled rarely, delaying discovery of the new items linked from them.
- Keep the sitemap dynamic so it stays current as the catalog grows.

## Video sitemaps (get reels into Google Video)

A page that embeds a video is, to Google, a plain URL unless you tell it there's a
video on it. Add a `<video:video>` block per video page under the namespace
`xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"`.

Required-ish fields:
- `<video:thumbnail_loc>` — an absolute, crawlable image URL.
- `<video:title>` and `<video:description>` — match the page.
- One of `<video:content_loc>` (a direct media file) **or** `<video:player_loc>`
  (an embeddable player URL). For socially-hosted reels you usually don't have a
  public MP4 → use the platform's **embed** URL (e.g. `youtube-nocookie.com/embed/<id>`)
  as `player_loc`.
- Useful extras: `<video:duration>` (integer seconds, 1–28800),
  `<video:publication_date>` (ISO-8601).

Only emit the block when you actually have a thumbnail + a player/content URL; list
the rest as plain page URLs. One combined sitemap with both namespaces is fine.

## Decision framework

- **"How do I tell Google a page exists?"** → You mostly can't. Ship it in the
  sitemap (with `lastmod`) and link to it internally; for one urgent page, Request
  Indexing in GSC. Set expectations: discovery is Google's schedule, not a button.
- **"Speed up Bing/Yandex?"** → IndexNow, wired to publish events.
- **"Video pages aren't ranking as videos?"** → video sitemap + `VideoObject`
  JSON-LD on the page (see the parent `seo` skill).
- **Discovery is fine but pages still aren't indexed** → it's not discovery, it's
  *selection*. Go to the `thin-page-audit` sub-skill.

## Key Principles

- **Don't ship dead pings.** Sitemap ping and the general Indexing API are myths now.
- **IndexNow is Bing/Yandex, not Google.** Say so every time, so nobody over-expects.
- **`lastmod` must be true**, or it's worse than absent (Google learns to ignore it).
- **A `<video:video>` needs a real thumbnail + player** — emit it only when you have both.
- **Indexing ≠ discovery.** Notification gets a page *crawled*; whether it's *kept*
  is a content-quality question — hand off to `thin-page-audit`.
