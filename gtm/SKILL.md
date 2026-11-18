---
name: gtm
description: >
  GTM operating system for a B2B company past product-market fit — the full
  domain map (RevOps, ICP/TAM, signals, scoring, data and enrichment,
  outbound, inbound and pipeline, content, ABM and paid ads, partnerships,
  community, AEO, AI agents, reporting). Use when planning or auditing a
  go-to-market motion, deciding what to build next, or when a GTM term comes
  up in planning; each leaf is one procedure to master and later promote
  into its own skill file.
---

# GTM

One-line summary: **GTM is one tree organized by workflow instead of tool — collect signals broadly, score them, act narrowly, and let reporting decide what survives.**

Credit: this comes from [Alex Vacca's post on X](https://x.com/itsalexvacca/status/2122992121036914902).

## The Map

```
📂 GTM
┃
┣ 📂 RevOps
┃ ┣ 📂 1 CRM as the record
┃ ┣ 📂 Signal routing to owners
┃ ┣ 📂 Scheduled enrichment
┃ ┣ 📂 Weekly deal reviews
┃ ┗ 📂 Loss reasons
┃
┣ 📂 ICP and TAM
┃ ┣ 📂 ICP from closed-won deals
┃ ┣ 📂 Segments
┃ ┣ 📂 Personas
┃ ┣ 📂 Lookalikes
┃ ┗ 📂 1 account list
┃
┣ 📂 Signals
┃ ┣ 📂 Hiring
┃ ┣ 📂 Funding
┃ ┣ 📂 New hires and GTM leaders
┃ ┣ 📂 Past champions
┃ ┣ 📂 Tech stack
┃ ┣ 📂 Public records
┃ ┣ 📂 Website visitors
┃ ┣ 📂 Review sites
┃ ┣ 📂 Post engagers
┃ ┣ 📂 Target-account exec posts
┃ ┗ 📂 Brand mentions
┃
┣ 📂 Scoring
┃ ┣ 📂 Fit score
┃ ┣ 📂 Intent score
┃ ┣ 📂 Tiers 1, 2, 3
┃ ┣ 📂 Score decay
┃ ┗ 📂 Hot, warm, cold routing
┃
┣ 📂 Data and enrichment
┃ ┣ 📂 Data sources
┃ ┣ 📂 Email waterfall
┃ ┣ 📂 Email verification
┃ ┗ 📂 Mobile numbers for the top tier
┃
┣ 📂 Outbound
┃ ┣ 📂 Sending infrastructure
┃ ┃ ┣ 📂 Secondary domains
┃ ┃ ┣ 📂 Warmed inboxes
┃ ┃ ┗ 📂 SPF, DKIM, DMARC
┃ ┃
┃ ┣ 📂 Copy
┃ ┃ ┣ 📂 First line per signal
┃ ┃ ┗ 📂 1 test per round
┃ ┃
┃ ┣ 📂 Channels
┃ ┃ ┣ 📂 Email
┃ ┃ ┣ 📂 LinkedIn
┃ ┃ ┗ 📂 Calls for the top tier
┃ ┃
┃ ┗ 📂 Reply routing
┃   ┣ 📂 Reply labels
┃   ┗ 📂 Approval gate
┃
┣ 📂 Inbound and pipeline
┃ ┣ 📂 Inbound lead enrichment
┃ ┣ 📂 Meeting prep and follow-up
┃ ┣ 📂 Product sign-up outreach
┃ ┣ 📂 Webinar and event attendees
┃ ┗ 📂 Closed-lost revival
┃
┣ 📂 Content
┃ ┣ 📂 Founder and team posts
┃ ┣ 📂 Buyer questions from calls
┃ ┣ 📂 Weekly newsletter
┃ ┣ 📂 Live sessions and clips
┃ ┗ 📂 Gated templates
┃
┣ 📂 ABM and paid ads
┃ ┣ 📂 Target-list audiences
┃ ┣ 📂 Promoted team posts
┃ ┣ 📂 1-to-1 ads
┃ ┣ 📂 Intent in the account score
┃ ┣ 📂 Gifting
┃ ┣ 📂 Retargeting
┃ ┗ 📂 Search ads
┃
┣ 📂 Partnerships
┃ ┣ 📂 Warm intros
┃ ┣ 📂 Customer referrals
┃ ┣ 📂 Revenue share
┃ ┣ 📂 Integration listings
┃ ┗ 📂 Shared accounts
┃
┣ 📂 Community
┃ ┣ 📂 Podcasts
┃ ┣ 📂 Dinners
┃ ┣ 📂 Launches
┃ ┣ 📂 Paid community
┃ ┗ 📂 Slack and Discord groups
┃
┣ 📂 AEO
┃ ┣ 📂 Prompt tracking
┃ ┣ 📂 Answer-first pages
┃ ┣ 📂 SEO basics
┃ ┣ 📂 Customer reviews
┃ ┗ 📂 Forum answers
┃
┣ 📂 AI agents
┃ ┣ 📂 Lead scoring
┃ ┣ 📂 Pre-call research
┃ ┣ 📂 Signal to sequence
┃ ┣ 📂 Copy intelligence
┃ ┗ 📂 Meeting action items
┃
┗ 📂 Reporting
  ┣ 📂 Reply rate
  ┣ 📂 Positive reply rate
  ┣ 📂 Show rate
  ┣ 📂 Spam and bounce rate
  ┣ 📂 Meetings booked per signal
  ┗ 📂 Pipeline by motion
```

## How the Tree Is Built

Four conventions carry the value; the specific leaves are examples.

1. **Organized by workflow, not by tool.** No vendor names anywhere. Each node names the job (signal routing, score decay, reply routing), so swapping tools never invalidates the structure.
2. **Numbered "1" entries are single sources of truth.** "1 CRM as the record," "1 account list," "1 test per round." One canonical artifact per concern; everything else references it instead of re-implementing it.
3. **One leaf = one procedure.** Leaves are small and concrete ("first line per signal," "mobile numbers for the top tier") — each is small enough to build, document and measure on its own.
4. **Section order encodes sequence.** ICP and TAM before Signals, Signals before Scoring, Scoring before Outbound, Reporting last. Reading top to bottom is the onboarding path.

Signals is deliberately the largest section: collect inputs broadly, act narrowly.

## How to Work It

- **Pick one motion at a time.** The tree is a map, not a checklist. A company past PMF runs a few motions well; the Reporting section defines the metric for each.
- **Master a leaf before moving on.** A leaf is done when the procedure is repeatable and its metric is measured.
- **Promote leaves into skills.** When a leaf has a proven, repeatable procedure, write it as a companion `.md` file in this directory and link it from the leaf. The tree grows the same way `ruby-on-rails/` grew: entry point first, sub-skills as they earn their place.
- **Leaves already covered elsewhere in this repo:** AEO → `content/aio/`, "SEO basics" → `seo/`, "Search ads" → `content/paid-ads/`. Check those before writing a new companion file.

## Companion Skills

One companion `.md` per section of the tree (AEO is already covered by `content/aio/`). `SKILL.md` is the map; each companion file is the operating playbook for its section:

| File | Covers | One-liner |
|---|---|---|
| `revops.md` | RevOps | One CRM as the record, signal routing, scheduled enrichment, weekly deal reviews, loss reasons |
| `icp-and-tam.md` | ICP and TAM | ICP from closed-won evidence, segments, personas, lookalikes, one account list |
| `signals.md` | Signals | 11 signal types, each with source, filter, and attached action |
| `scoring.md` | Scoring | Fit × intent → tiers, with decay and hot/warm/cold routing |
| `data-and-enrichment.md` | Data and enrichment | Email waterfall, verification, mobile data reserved for the top tier |
| `outbound.md` | Outbound | Sending infrastructure, first line per signal, 1 test per round, reply routing |
| `inbound-and-pipeline.md` | Inbound and pipeline | Inbound enrichment, meeting prep, product signups, event attendees, closed-lost revival |
| `content.md` | Content | Founder posts, buyer questions from calls, newsletter, clips, gated templates |
| `abm-and-paid-ads.md` | ABM and paid ads | Account-list audiences, 1-to-1 ads, retargeting, intent feedback loop |
| `partnerships.md` | Partnerships | Warm intros, referrals, revenue share, marketplaces, shared accounts |
| `community.md` | Community | Podcasts, dinners, launches, paid communities, Slack/Discord |
| `ai-agents.md` | AI agents | The five agents (scoring, pre-call research, signal-to-sequence, copy, action items) with the human-at-conversion rule |
| `reporting.md` | Reporting | The six metrics, their thresholds, and the weekly slot where decisions get made |

Cross-file references use the bare filename convention (see repo `CLAUDE.md`).

## Decision Framework

- **Which motion next?** The one whose reporting metric is currently weakest, upstream of the revenue number you need. Score decay and reply rate fail before pipeline does.
- **Is a motion working?** It has a metric in Reporting that someone reads weekly and a threshold that triggers a change.
- **Is it single-sourced?** For any artifact (account list, CRM, test plan), exactly one canonical copy exists. A second copy is a bug.
- **Tool or workflow first?** Workflow. Name the job, then pick the tool. A tool-shaped org chart breaks on every vendor switch.

## Collaboration With the Other Skills

- `content/aio/` — the AEO section's answer-first pages, prompt tracking and citation tactics, in executable depth.
- `seo/` — the "SEO basics" leaf and the indexing/citation mechanics answer-first pages depend on.
- `content/paid-ads/` — the ABM and paid-ads section's testing cadence and ROI math.
- `software-factory/SKILL.md` — same authoring pattern applied to delivery instead of revenue: map the domain, one procedure per node, let measurement decide.
