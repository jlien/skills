# PageSpeed Audit Triage

A lookup table for the common Lighthouse audits, keyed by audit `id`. For each: what it measures, **when it's a real problem worth fixing**, **when it's noise / irrelevant / can't-fix**, and the concrete remedy. Use it in Phase 3 of `SKILL.md` to sort each finding into Fix / Ignore / Investigate.

The guiding rule: an audit only matters if fixing it moves a Core Web Vital that is **failing in the field**. Lab-only wins on an already-passing metric are vanity.

## Metric → which audits move it

- **LCP** ← `server-response-time`, `render-blocking-resources`, `prioritize-lcp-image` / `preload-lcp-image` / `largest-contentful-paint-element`, `modern-image-formats`, `uses-responsive-images`, `offscreen-images` (only if the LCP image was wrongly lazy-loaded), `redirects`, `uses-text-compression`, `critical-request-chains`, font loading.
- **CLS** ← `layout-shift-elements` / `cls-culprits-insight`, `unsized-images`, `font-display`, late-injected embeds/ads.
- **INP / TBT** ← `total-blocking-time`, `bootup-time`, `mainthread-work-breakdown`, `unused-javascript`, `legacy-javascript`, `duplicated-javascript`, `third-party-summary`, `dom-size`.

## LCP-related

| Audit id | Real when… | Noise / irrelevant when… | Fix |
|---|---|---|---|
| `server-response-time` (TTFB) | >0.8 s and LCP is failing | Already <0.6 s; or the URL is a cold cache-miss one-off | Cache/CDN, edge, faster backend queries, HTTP caching headers |
| `render-blocking-resources` | Blocking CSS/JS in `<head>` delays first paint | Savings <150 ms; already deferred | Inline critical CSS, `defer` scripts, `media`-scope non-critical CSS, self-host + preload fonts |
| `largest-contentful-paint-element` | Always read it — tells you *what* to optimize | — (informational, never "fails") | Identify element → apply the matching image/text LCP fix |
| `prioritize-lcp-image` / `preload-lcp-image` | LCP is an image and isn't prioritized | LCP is text (no image to preload) | `fetchpriority="high"` + `<link rel="preload" as="image">`; ensure it's **not** `loading="lazy"` |
| `modern-image-formats` | Large JP/PNG heroes; site is image-heavy | Savings tiny; images already WebP/AVIF; SVG/icon fonts | Serve WebP/AVIF with fallback; automate in the asset/build step |
| `uses-responsive-images` | Serving 2000px into a 400px slot | Correctly-sized already; savings negligible | `srcset`/`sizes`; generate width variants |
| `offscreen-images` (lazy-load) | Many below-fold images loading eagerly | **Trap:** never lazy-load the LCP/above-fold image | `loading="lazy"` on below-fold only |
| `uses-text-compression` | Text assets served uncompressed | CDN already gzips/brotlis (common) — verify before prescribing | Enable brotli/gzip at server/CDN |
| `redirects` | Chained redirects on the landing URL | Single expected canonical redirect | Point links at the final URL; collapse chains |
| `uses-optimized-images` | Unoptimized encode, real bytes | Marginal | Recompress; strip metadata |

## CLS-related

| Audit id | Real when… | Noise / irrelevant when… | Fix |
|---|---|---|---|
| `layout-shift-elements` / `cls-culprits-insight` | Field CLS >0.1; lists shifting nodes | Field CLS already ≤0.1 (lab CLS can differ from field — trust field) | Fix the listed nodes: sizing, reserved space |
| `unsized-images` | Images/iframes without width/height | Element is CSS-sized with `aspect-ratio` already | Add explicit `width`/`height` or `aspect-ratio` |
| `font-display` | FOIT causing text shift | Fonts already `swap` with `size-adjust`; system fonts | `font-display: swap` + `size-adjust`/`ascent-override`; preload the font |
| (late embeds/ads) | Content injected above existing content | Reserved container already sized | Reserve fixed space for ad/embed slots before they load |

## INP / TBT / main-thread

| Audit id | Real when… | Noise / irrelevant when… | Fix |
|---|---|---|---|
| `total-blocking-time` | High TBT and INP failing in field | INP already Good in field | Reduce/defer JS; split long tasks |
| `bootup-time` / `mainthread-work-breakdown` | First-party JS dominates execution | The time is third-party (see `third-party-summary`) — you can't tree-shake it | Code-split, `defer`, `import()` on interaction, remove dead deps |
| `unused-javascript` | Large **first-party** bundle, route-splittable | **Culprit is third-party** (GA/GTM, pixel, YouTube/TikTok/IG embed, chat, A/B tool) → can't fix without removing the tool | Route-level splitting; tree-shake; drop unused libs. If third-party: accept or lazy-load the widget on interaction |
| `legacy-javascript` / `duplicated-javascript` | Your build ships transpiled/duplicated code | Injected by a third-party script | Modern build target; dedupe shared chunks |
| `unminified-css` / `unminified-javascript` | First-party assets unminified | Third-party serves them unminified (common) | Enable minification in the build |
| `third-party-summary` | Third-parties block the main thread heavily | Informational — you rarely control them | Lazy-load non-critical widgets; `facade` pattern for embeds; question whether each tag earns its cost |
| `dom-size` | >~1,500 nodes and INP suffers | Moderate DOM on a content page | Virtualize/paginate long lists; simplify markup |
| `uses-passive-event-listeners` / `no-document-write` | Genuinely present | Absent | Passive listeners; remove `document.write` |

## Network / caching

| Audit id | Real when… | Noise / irrelevant when… | Fix |
|---|---|---|---|
| `uses-long-cache-ttl` | **First-party** static assets have short TTL | Flags **third-party** (analytics/pixel) assets — you don't set their headers → **usually ignore** | Long `Cache-Control: immutable` + fingerprinted filenames for your assets |
| `uses-rel-preconnect` | Real cross-origin critical requests exist | No cross-origin critical fetches → N/A | `preconnect` to the critical origin(s) only (don't over-preconnect) |
| `critical-request-chains` | Deep dependency chain delays LCP | Shallow chain | Flatten: preload key resources, inline critical CSS |
| `total-byte-weight` | Page is multi-MB and metrics fail | Under budget | Compress images/JS; the specific audits above are the levers |
| `efficient-animated-content` | Large animated GIFs | No GIFs | Replace GIF with `<video>` (mp4/webm) |

## Non-performance categories (report, don't over-prescribe)

- **Accessibility** — real user + legal value; fix contrast, labels, `alt`, focus order. Worth surfacing, but it's a separate discipline from CWV.
- **Best Practices** — `errors-in-console`, `deprecations`, `csp-xss`, mixed content. Fix functional/security ones; console-noise from third-parties is low priority.
- **SEO** — PSI's SEO checks are shallow (`is-crawlable`, `document-title`, `meta-description`, `hreflang`, `robots-txt`, tap targets). Confirm the basics, then defer real SEO work to the **`seo` skill** rather than treating PSI as an SEO audit.

## Standing "usually ignore" list

Dismiss these by default unless first-party evidence says otherwise — but always **name each one with its reason** in the report:

- Any audit whose savings map to a metric already **Good in the field**.
- `unused-javascript` / `unused-css-rules` / `legacy-javascript` / `uses-long-cache-ttl` traced to **third-party** tags.
- Opportunities with **<100 ms** estimated savings.
- Audits that don't apply to the stack (`preconnect` with no cross-origin, `efficient-animated-content` with no GIFs, `modern-image-formats` on an all-SVG page).
- A single anomalous **lab** swing not corroborated by a re-run or by field data.
