---
name: paid-ads
description: "Framework for running simple, profitable paid ads for SaaS — Google Ads bottom-of-funnel keywords + Facebook Ads creative testing, with ROI tracking via CAC vs LTV."
version: 1.0.0
author: Jimmy Lien
license: MIT
metadata:
  hermes:
    tags: [paid-ads, google-ads, facebook-ads, saas-marketing, cac, ltv, roi]
    related_skills: [content/content-brief, seo]
---

# Paid Ads for SaaS

A minimal, repeatable paid ads framework for SaaS: stop overcomplicating, focus on bottom-of-funnel keywords, test creative volume, and measure ROI by CAC vs customer lifetime value.

Source: https://x.com/jimmylien/status/1934752341234567890

## Core Principles

1. **Bottom of funnel only** — never waste budget on awareness or consideration. Bid on keywords where the searcher already knows what they need.
2. **Creative volume wins** — test 20 pieces of ad creative per week on Facebook, then double down on winners.
3. **ROI is simple** — if $1 in ad spend produces $5 of customer lifetime value, you're good. CAC vs LTV vs payback period is the only math that matters.
4. **Landing page matching** — the keyword you bid on must appear in the H1 and first paragraph of the landing page. The ad creative's hook must match the landing page.

## Google Ads Workflow

### 1. Keyword Strategy

- Find **bottom of funnel keywords** related to the product — terms where the searcher is ready to buy or sign up (e.g., "best [tool] for [use case]", "[product] pricing", "[product] alternative", "[product] review", "[category] software")
- Use **phrase match bidding** on those keywords — broad match wastes budget, exact match is too narrow. Phrase match captures relevant variations without overbroadening.

### 2. Landing Pages

- Every keyword group gets a dedicated landing page
- The keyword (or its core variant) appears in the **H1 title** and **Paragraph 1** — this is non-negotiable for Quality Score
- Page content answers the searcher's intent: compare, demo, pricing, or free trial — whatever matches the keyword's stage

### 3. Conversion Events

- **Signup event** — tracks free trial or account creation. Primary optimization target for top-of-funnel spend.
- **Payment event** — tracks first paid transaction. Secondary optimization target; use this for ROAS reporting and bid adjustments once you have sufficient payment data.

### 4. Account Structure

- One campaign per product or major feature
- Ad group per keyword theme (3-5 closely related keywords per group)
- Landing page per ad group — never send multiple keyword themes to the same page

## Facebook Ads Workflow

### 1. Targeting

- **Target all of Facebook** — no narrow audiences, no lookalikes, no interest targeting. Let the platform's algorithm find the right people. Broad targeting + good creative outperforms narrow targeting every time for SaaS.

### 2. Creative Testing

- Test **20 pieces of ad creative per week** — different hooks, formats, angles. This is the volume that lets you find winners fast.
- Creative types to rotate:
  - Direct benefit headlines ("Cut your [X] by Y%")
  - Problem/solution hooks ("Stop doing [pain point] manually")
  - Social proof ("Join Z companies using [product]")
  - Feature demos (short video or screenshot carousel)
  - Testimonial / case study quotes

### 3. Winner Escalation

- Identify winners by CTR + conversion rate + cost per signup
- Winners get promoted into **their own conversion campaigns with dedicated spend** — separate ad sets with higher budgets, optimized for the conversion event, not further creative testing
- Losers get killed — don't let low-performers burn budget

### 4. Landing Pages

- The hook of the winning creative must be reflected in the H1 of the landing page — continuity from ad to page is critical for conversion rate
- Same conversion events as Google Ads: signup event + payment event

## Measurement & ROI

### Dashboard

- Use **Graphed** or **Looker Studio** (or any dashboard tool that connects ad platform APIs)
- Track at minimum:
  - Spend by channel (Google vs Facebook)
  - CAC (cost per acquisition) by channel and by creative
  - Customer lifetime value (LTV) — use historical data or modeled LTV
  - Payback period — months to recover CAC from LTV

### The Only Metric That Matters

```
ROI = LTV / CAC

If $1 in → $5 of LTV comes out → you're good.
```

- **Threshold**: 5x LTV-to-CAC is healthy for most SaaS
- **Payback period**: ideally under 6 months — if it takes longer than 12 months to recover CAC, the channel or creative mix is wrong
- **Channel comparison**: compare Google Ads vs Facebook Ads side-by-side on the same LTV basis — if one channel is 2x the CAC of the other, shift budget proportionally

### Attribution

- Both channels need signup and payment conversion events fired to the same dashboard
- Use UTMs or integration (Segment, GA4, or ad platform API) to join ad spend to customer value
- Don't optimize for clicks — optimize for signups and payments only

## Decision Framework

**Run Google Ads when:**
- Your product has clear bottom-of-funnel keywords (comparison, pricing, alternative, review terms exist)
- You have dedicated landing pages per keyword theme
- You have signup and payment conversion events firing reliably

**Run Facebook Ads when:**
- You can produce 20+ creative variants per week
- Your ad-to-landing-page continuity is tight (hook in ad → H1 on page)
- You have enough conversion data (50+ signups/month per campaign) for Facebook's algorithm to optimize

**Skip paid ads entirely when:**
- Your product has no bottom-of-funnel keyword volume (too new, too niche)
- You can't maintain creative velocity (less than 10 variants per week)
- You don't have conversion tracking set up — no conversions = no optimization = wasted spend

## Collaboration Patterns

- **Product team**: Defines the signup and payment conversion events; provides LTV data for ROI calculation
- **Growth / Marketing team**: Executes ad campaigns, produces creative, builds landing pages, monitors dashboard
- **Engineering / Data team**: Ensures conversion events fire correctly, sets up dashboard data pipeline (ad platform APIs → dashboard tool)
- **Content team**: Writes landing page copy that matches keywords and ad hooks

## Key Principles

- **Bottom of funnel only** — awareness spend is a luxury most SaaS can't afford. Bid on intent, not interest.
- **Phrase match over broad match** — broad match burns budget on irrelevant queries. Exact match misses volume. Phrase match is the Goldilocks zone.
- **Creative volume is a competitive moat** — most advertisers test 3-5 creatives and pick a winner. Testing 20/week gives you a 4-5x discovery advantage.
- **Winners get dedicated spend** — don't dilute a winning creative by putting it in a shared budget with losers. Promote and scale.
- **Landing page matching is non-negotiable** — keyword in H1+P1 for Google. Hook in H1 for Facebook. Mismatch kills Quality Score and conversion rate.
- **ROI is CAC vs LTV, not ROAS** — return on ad spend (revenue/spend) ignores LTV. A campaign with 3x ROAS but low LTV is worse than 1.5x ROAS with high LTV.
- **One dashboard to rule them all** — don't optimize Google and Facebook in separate silos. Compare side-by-side on the same LTV basis.
- **Payback period under 6 months** — if it takes longer, the channel or creative isn't right.