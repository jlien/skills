---
trigger: PageSpeed, PageSpeed Insights, PSI, Lighthouse, Core Web Vitals, CWV, LCP, CLS, INP, page speed, site performance, web vitals, performance audit, speed audit
---

# PageSpeed (Run · Analyze · Prescribe)

Run Google PageSpeed Insights / Lighthouse against a URL, read the results correctly, and turn them into a short, ranked list of changes that will actually move a failing metric — while explicitly filtering out the audits that are noise, third-party, or irrelevant to *this* site. The goal is not a 100 score; it's passing Core Web Vitals in the field with the least work.

**Companion:** `pagespeed/audit-triage.md` — the per-audit catalog (what each Lighthouse audit means, when it's real, when it's noise, and the fix). Consult it in Phase 3.

## Core Responsibilities

- Run PSI for a URL on **both** mobile and desktop, and capture the raw JSON without dumping it into context.
- Read **field data (CrUX) first** — it's the ranking-relevant truth — then use lab data for diagnosis.
- Separate **real, fixable, high-impact** findings from **noise / third-party / irrelevant / variance** ones.
- Prescribe concrete, code-level fixes ranked by (impact on a failing metric ÷ effort).
- Produce a "safe to ignore" list that says *why* each dismissed audit doesn't matter here.
- Verify by re-running after changes ship (field data lags ~28 days; lab confirms immediately).

## Setup (once)

PSI is a REST API. The anonymous quota is effectively **zero** now — you must pass an API key.

- Get a key: Google Cloud Console → enable **PageSpeed Insights API** → create an API key (free, ~25k/day).
- Store it as `PAGESPEED_API_KEY` in the environment (never hardcode it in a committed file).
- No key handy? Fallbacks, in order: (a) run Lighthouse locally — `npx lighthouse <url> --only-categories=performance --form-factor=mobile --screenEmulation.mobile --output=json --output-path=./lh.json --quiet` (no quota, lab-only, **no field data**); (b) query the CrUX API directly for field data (`https://chromeuxreport.googleapis.com/v1/records:queryRecord`); (c) as a last resort, open `https://pagespeed.web.dev/analysis?url=<URL>` for a human to read. Prefer the PSI API — it returns lab **and** field in one call.

## Workflows

### Phase 1 — Run (mobile + desktop)

Request all four categories so one call covers performance, a11y, best-practices, and (shallow) SEO. Save to files; the JSON is ~0.5–1 MB — **never** cat the whole blob into context, always `jq` the parts you need.

```bash
API="https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
Q="url=https://example.com&category=performance&category=accessibility&category=best-practices&category=seo&key=$PAGESPEED_API_KEY"
curl -s "$API?$Q&strategy=mobile"  -o psi-mobile.json
curl -s "$API?$Q&strategy=desktop" -o psi-desktop.json
# Sanity-check the call succeeded (else you'll jq an error object):
jq -e '.lighthouseResult.categories.performance.score' psi-mobile.json >/dev/null || jq '.error' psi-mobile.json
```

PSI lab runs are **noisy** (±5–10 points between runs). If a lab number looks surprising, re-run once before trusting it. Field data does not move between runs — it's a 28-day rolling aggregate.

### Phase 2 — Field data first (the ranking truth)

Google's Page Experience signal uses **CrUX field data**, not the lab score. Read it before anything else.

```bash
# Per-URL field CWV (may be absent on low-traffic pages):
jq '.loadingExperience | {url_overall: .overall_category,
     metrics: (.metrics // {} | to_entries | map({m:.key, p75:.value.percentile, cat:.value.category}))}' psi-mobile.json
# Origin-level fallback (whole site) — present even when the URL has no data:
jq '.originLoadingExperience.overall_category' psi-mobile.json
```

Verdict thresholds (p75, mobile):

| Metric | Good | Needs work | Poor | Notes |
|---|---|---|---|---|
| **LCP** (load) | ≤2.5 s | ≤4 s | >4 s | Biggest lever on most sites |
| **CLS** (stability) | ≤0.1 | ≤0.25 | >0.25 | Unitless |
| **INP** (responsiveness) | ≤200 ms | ≤500 ms | >500 ms | Replaced FID in 2024; from JS work |
| TTFB (server) | ≤0.8 s | ≤1.8 s | — | Diagnostic input to LCP |
| FCP | ≤1.8 s | ≤3 s | — | Diagnostic |

**Rules that make you "smart" here:**
- If field is **Good** but the lab score is low → the lab's throttled mobile emulation is pessimistic; real users are fine. Say so and de-prioritize. Do not chase the lab number.
- If the URL has **no field data** (`.loadingExperience.metrics == {}`) → the page lacks traffic; fall back to origin-level field data + lab. Note the uncertainty; don't present lab as ground truth.
- Passing CWV = **all three** (LCP, CLS, INP) at "Good" on mobile. Desktop is secondary for ranking but worth reporting.

### Phase 3 — Triage lab audits (real vs. noise)

Pull the failing/opportunity audits, then run each through `pagespeed/audit-triage.md`.

```bash
# Opportunities, sorted by estimated savings:
jq '[.lighthouseResult.audits|to_entries[]|select(.value.details.type=="opportunity")
     |{id:.key,title:.value.title,ms:(.value.details.overallSavingsMs//0),score:.value.score}]|sort_by(-.ms)' psi-mobile.json
# Everything scored below passing (0.9), with its display value:
jq '[.lighthouseResult.audits|to_entries[]|select(.value.score!=null and .value.score<0.9)
     |{id:.key,title:.value.title,score:.value.score,val:.value.displayValue}]' psi-mobile.json
# What the LCP element actually is (drives the #1 fix):
jq '.lighthouseResult.audits["largest-contentful-paint-element"].details.items' psi-mobile.json
```

Triage every finding into one of three buckets — **this is the core judgment of the skill:**

1. **Fix** — first-party, maps to a *failing field metric*, meaningful savings. → prescribe in Phase 4.
2. **Ignore (noise)** — see `audit-triage.md`. Common cases: savings map to a metric already passing in the field; the culprit bytes are third-party you can't tree-shake (GA/GTM, Meta pixel, YouTube/TikTok/Instagram embeds, chat widgets); estimated savings <100 ms; the audit doesn't apply to this stack (e.g. "preconnect" with no cross-origin requests). **Name each one and say why** — a dismissed audit with a reason is more useful than a silent omission.
3. **Investigate** — plausibly real but needs a look at the source before prescribing (e.g. `unused-javascript` — is the bundle first-party and route-splittable, or a vendor blob?).

**Never** prescribe a fix for an audit whose remedy is "remove a tool the business depends on." Note it as an accepted cost instead.

### Phase 4 — Prescribe (ranked, concrete)

For each **Fix**-bucket item, give the specific change, not the generic audit title. Rank by impact-on-a-failing-metric ÷ effort. Typical highest-ROABs, in order:

1. **LCP** — identify the LCP element (Phase 3). If it's an image: serve WebP/AVIF at the right size, add `fetchpriority="high"`, `preload` it, and make sure it is **not** `loading="lazy"`. If it's text: fix render-blocking CSS/fonts (`font-display: swap` + `size-adjust`, inline critical CSS) and TTFB (cache/CDN).
2. **CLS** — set explicit `width`/`height` (or `aspect-ratio`) on every image, video, iframe, and ad slot; reserve space for late-injected embeds; avoid inserting content above existing content.
3. **INP / TBT** — cut and defer first-party JS (route-level code splitting, `defer`/`async`, `import()` on interaction); break up long tasks; move heavy work off the main thread. TBT (lab) is the actionable proxy for INP.
4. **TTFB** — server/CDN caching, edge, faster backend queries. Upstream of LCP.

Tie each recommendation back to the metric it moves and the field verdict. Skip anything that only improves an already-passing metric.

### Phase 5 — Report & verify

Deliverable (keep it tight):
- **Verdict** — CWV pass/fail per metric, mobile + desktop, field-based. One line each.
- **Do these** — 3–5 ranked fixes, each with the concrete change and the metric it moves.
- **Safe to ignore** — the dismissed audits, each with a one-line reason (third-party / already-passing / negligible / N/A).
- **Watch** — anything borderline that could regress.

After fixes ship: re-run PSI → lab metrics confirm immediately; **field CWV updates over ~28 days**, so set expectations and check CrUX/Search Console later rather than declaring victory on the lab score.

## Decision Framework

- **Field beats lab.** CrUX is what Google ranks on; Lighthouse lab is a diagnostic microscope. When they disagree, trust the field for "is there a problem?" and use the lab for "why?".
- **Passing > perfect.** Ship when all three CWV are Good in the field. A 100 lab score is vanity; the last 10 points are usually third-party you don't own.
- **Third-party is a business decision, not a bug.** Surface its cost; don't prescribe deleting the analytics/pixel/embed unless asked.
- **One bad run ≠ a regression.** Re-run before believing a lab swing; confirm against field.
- **No field data = low confidence.** Say so; lean on origin-level data and lab, and flag the page as under-measured.

## Collaboration Patterns

- **`seo` skill** — owns Core Web Vitals as *one* of its Tier-3 concerns and the JSON-LD/crawl plumbing. This skill is the deep-dive that *measures and prescribes* the CWV fixes the SEO skill lists. Hand off: PageSpeed produces the ranked fix list; SEO/ruby-on-rails implement it. PSI's own SEO audits are shallow — defer real SEO to the `seo` skill.
- **`ruby-on-rails` skill** — implements the fixes (asset pipeline, `image_tag` dimensions, `preload`/`fetchpriority`, HTTP caching headers, Turbo/Stimulus JS budget). PageSpeed supplies the spec; Rails executes with a failing baseline to beat.
- **`tailwind` / `design-system` skills** — CLS fixes live here (explicit sizing, `aspect-ratio`, reserved space, font loading). Coordinate so a redesign doesn't reintroduce layout shift.
- **`content` skills** — heavy hero media and embeds are the usual LCP/CLS culprits; feed image-format/size and lazy-load rules back into how content is produced and embedded.

## Key Principles

- **Read the field first.** The lab score is a means; the CWV field verdict is the end.
- **Prescribe changes, not audit titles.** "Preload the hero WebP and drop its lazy-load" beats "improve LCP."
- **Name what you ignore, and why.** A defensible dismissal is part of the analysis, not an omission.
- **Don't chase 100.** Fix failing metrics; stop when the field passes.
- **Re-run to confirm, and wait for the field.** Lab verifies the change; CrUX verifies the outcome ~28 days later.
