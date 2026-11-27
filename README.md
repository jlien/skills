# Skills Repository

This repository contains specialized agent skills for various roles and workflows.

## Skills

### Core Development

- **Ruby-on-Rails.md** - Rails development with BDD, planning, and automated code review
- **code-review/SKILL.md** - Agent-era review process (from the Claude Code team's practice): layered checks (verify-before-review, AI review, blocking security review, risk-tiered human approval), REVIEW.md guidance, findings protocol (Important/Nit/Pre-existing), convergence rules to break agent author/reviewer loops, and where humans stay in the loop
- **ruby-on-rails/crap.md** - CRAP (Change Risk Anti-Patterns) triage: Savoia's comp² · (1 − cov/100)³ + comp score per method from RuboCop cyclomatic complexity + SimpleCov coverage, act per quadrant (spec missing branches, extract the method), escalate to mutation testing
- **ruby-on-rails/mutation-testing.md** - mutant: Ruby mutation testing — mutant-rspec/rails config, subject expressions, Rails hooks (eager load + per-worker DB isolation), incremental CI discipline, handling alive mutants, commercial-license caveat
- **Project-Management.md** - Blocker tracking, dependency management, and status updates

### Product & Technical Leadership

- **CPO.md** - Chief Product Officer: strategic direction, market analysis, and roadmap
- **CTO.md** - Chief Technology Officer: technical strategy, architecture, and team leadership
- **Product-Manager.md** - Product backlog management, requirements, and execution
- **ai-transformation/** - AI-native transformation playbook for PE-backed companies, in the order that works: paid AI seats with budgets and daily-user champions (people), one source of truth and read-first agent access (data), one workflow with one owner and a dollar number, golden set, shadow mode, human approval on money and customers (workflows), single gateway with logs/budget/kill switch (guardrails), and small shipping teams where every PR gets the same checks (engineering). Skip the boring half and you end up with 40 pilots and nothing in production
- **software-factory/** - The 10 parts of a software factory (Mar deHaym): intake with code-checkable acceptance criteria, human-approved spec, budgeted orchestrator, disposable sandbox, self-hosted model gateway, code-map context, CI-owned gates, git-versioned prompts with evals, session-to-epic measurement, and metadata-only seat tracking. Build the platform (gateway, measurement, gates, evals) before the agent; what stays with people (architecture, greenfield, big refactors, discovery) is named; rent-vs-own test: stop paying the vendor, does it keep running? Companion to `ai-transformation/`

### Frontend & Design

- **design-system/** - Design tokens, component API conventions, accessibility baselines, and Tailwind mapping (framework-agnostic; basis for the Rails ViewComponent skill)
- **hotwire-crud/** - Canonical admin CRUD: table index, row opens Show, Edit/Delete in the last column, Show edits via turbo-frame modal, nested records as tables on the parent
- **tailwind/** - Tailwind CSS configuration, customization, composition patterns, and common pitfalls

### Marketing & Growth

- **seo/** - Technical & on-page SEO: metadata, canonicals, sitemaps/robots, JSON-LD structured data (incl. video), Core Web Vitals, and internal linking
- **content/aio/** - AI / answer-engine optimization: get cited by ChatGPT, Perplexity & Google AI Overviews via extractable answer blocks, `FAQPage` schema, `llms.txt`, and a deliberate AI-crawler policy
- **content/aio/measurement.md** - Measure AI visibility (the tracking counterpart to aio): AI referral traffic in GA4, a prompt-panel harness for citation-rate & share-of-voice across web-enabled models, AI-crawler log coverage, and GSC as a proxy — with a runnable Perplexity-first panel script
- **seo/backlinks.md** - Top 50 high-quality backlink sources organized by tier (editorial/media, Web 2.0, document sharing, image/video, bookmarking, business/directory), with DA scores, dofollow status, and best-use guidance
- **seo/link-building-strategy.md** - Tactical execution playbook: broken link building (Moving Man Method), digital PR with localized data, guest posting for the Citation Core, unlinked brand mentions, outreach templates, and case studies
- **seo/citation-hub.md** - Citation Hub tactic: earn links passively by publishing a primary-sourced statistics hub (50+ verified stats, question-style headings, quotable Key Takeaways block) that writers and AI engines cite by reflex — no outreach
- **seo/indexing-and-freshness.md** - Faster discovery/recrawl: IndexNow (Bing/Yandex — Google isn't a participant), why the sitemap-ping and general Indexing API are dead, honest sitemap `lastmod` (incl. section indexes), and video sitemaps (`<video:video>`)
- **seo/thin-page-audit.md** - Why pages get crawled but not indexed ("Crawled/Discovered – currently not indexed"): sample live pages, measure per-template main-content words + unique-text coverage, and thicken thin templates (transcripts, FAQ, unique prose); GSC Pages report as ground truth
- **seo/search-engine-submission.md** - First-time indexation across engines: which submission channel exists per engine (Google GSC, IndexNow bulk for Bing/Yandex, Brave's submit-url form with its silent per-IP rate limit, Apple's robots-only path) and the bulk-initial-submission playbook — robots/sitemap prep, IndexNow ≤500-URL batches, homepage-seed submission, 3-day-later GSC coverage audit
- **content/paid-ads/** - SaaS paid ads framework: Google Ads bottom-of-funnel keyword + phrase match bidding, Facebook Ads 20-creative/week testing cycle, landing page matching, and ROI measured by CAC vs LTV
- **content/llm-artifact-sweep/** - QA sweep for LLM-generated copy before it ships: regex artifact patterns (instruction leakage, placeholders, doubled words, truncation), language-bleed checks, a full read of the rendered page, and a post-deploy re-sweep of the live URL
- **content/llm-output-deslop/** - Deslop pass for LLM-generated prose: the ten rhetorical tics (negation-first reveal, abstraction agency, straw-man knockdown, fragment cadence, ...) with tells and rewrite rules — the stylistic layer the regex-based `llm-artifact-sweep` can't see
- **content/content-gap-analysis/** - SEO content gap analysis from live GSC/GA4 data (service-account auth, no CSV exports needed): clusters queries into topic groups, then flags missing content, striking-distance (pos 8-20), underperforming CTR vs the site's own position bands, and answer-style/AI-citation opportunities; outputs a prioritized cluster table + top-5 new pages + top-5 quick wins. Companion `gsc-ga4-data-access.md` holds the live-verified pull recipes (JWT auth, search-analytics + runReport endpoints, row caps)
- **gtm/** - GTM operating system for a B2B company past PMF (Alex Vacca): the full domain map — RevOps, ICP/TAM, signals, scoring, data/enrichment, outbound, inbound, content, ABM, partnerships, community, AEO, AI agents, reporting — organized by workflow instead of tool, with numbered "1" entries as single sources of truth and one leaf = one procedure. Ships with 13 companion files (one playbook per section: `revops.md`, `icp-and-tam.md`, `signals.md`, `scoring.md`, `data-and-enrichment.md`, `outbound.md`, `inbound-and-pipeline.md`, `content.md`, `abm-and-paid-ads.md`, `partnerships.md`, `community.md`, `ai-agents.md`, `reporting.md`); the AEO/SEO/paid-ads leaves already live in `content/aio/`, `seo/`, `content/paid-ads/`
- **pagespeed/** - Run PageSpeed Insights / Lighthouse, read field (CrUX) Core Web Vitals before lab scores, and turn the results into a ranked fix list — with a companion `audit-triage.md` catalog that separates real, first-party, metric-moving findings from third-party / already-passing / negligible noise

### Security

- **security/web-pentest/** - Ethical-hacking agent for testing your own web apps: phased methodology (recon → surface mapping → OWASP Top 10 → APT-grade deep pass → report), an exhaustive local toolchain (`toolkit.md`), a concrete OWASP test checklist (`owasp-web-checklist.md`), authenticated-area testing — sessions, IDOR, privilege escalation, auth-flow abuse, CSRF (`authn-authz.md`), an API-layer checklist — BOLA, mass assignment, GraphQL, resource abuse (`api-testing.md`), a source-assisted white-box pass — route/guard maps, config review, secret sweeps, lockfile verification (`white-box.md`), state-actor tradecraft emulation — APT29/APT28/Lazarus patterns: edge-appliance CVE exposure, credential-attack realism, business-logic races, supply chain, exploit chains, detection validation (`apt-ttps.md`), a remediation/retest loop — verified-done criteria, fresh evidence, risk acceptance (`remediation.md`), and an evidence-based findings report (`report-template.md`). Guardrails first: written scope file, authorized targets only, no destructive payloads, rate-limited, verified findings. Complements the `code-review/SKILL.md` blocking security review — that covers code, this covers the running app

### Process & Systems Analysis
- **theory-of-constraints/** - A team of TOC specialist agents: Constraint-Finder locates the binding constraint with falsifiable evidence (capacity vs. policy vs. market); Five Focusing Steps runs Exploit → Subordinate → Elevate → Repeat; the Thinking Processes agents reason with sufficiency logic — Current Reality Tree (many UDEs → one root cause), Evaporating Cloud (dissolve speed/quality-type conflicts, no compromise), Future Reality Tree with Negative Branch Reservation (prove the fix, trim what it breaks first); Transition Tree turns the fix into an obstacle-driven plan; Throughput Accounting scores decisions in T/I/OE. Entry point routes by engagement stage; wired into the CTO/PM org chart.

### Agent Workflow

- **Agent-Writing-System.md** - Orwell's six rules from "Politics and the English Language" (1946): short words, active voice, cut the fluff, fresh language, plain English. Paste into CLAUDE.md / AGENTS.md for instant writing quality.
- **goal/** - Long-horizon goal-mode persistence with `goal.md`, audit discipline, and budget awareness (modeled on Codex CLI's `/goal`)
- **llm-as-a-verifier/** - Verification as a scaling axis: continuous, probabilistic scoring (`select` best-of-N, `compare` pairs, `track` progress) replaces coarse 1-5 judging; used to rank candidate implementations and monitor long refactors (arXiv 2607.05391)
- **launch-qa/** - Launch QA via five simulated first-time users (impatient, skeptic, mobile, non-native English speaker, breaker): five parallel browser subagents walk landing → first success and screenshot every confusion, findings merge ranked by how many users hit each, one-pass fix, rerun to prove it; includes a 25-scenario common-QA checklist (auth, forms, uploads, payments, offline, emails, console leaks) run alongside the personas
- **simulated-customers/** - Pre-test an idea, price, or copy with simulated customer personas instead of market research: role-play one specific person, show the artifact verbatim, collect unfiltered written reactions, convert text to intent in a separate pass (Semantic Similarity Rating, arXiv 2510.08338 — ~90% of real test-retest reliability across 57 surveys / 9,300 human answers). Tests whether a persona would WANT it and at what price; pairs with `launch-qa`, which tests whether the flow works
- **dnc-complaint/** - File FTC Do Not Call registry complaints in bulk from spam-call screenshots: vision extraction of call-log rows, title-line contact screening, the verified donotcall.gov wizard field map (JS-driven AJAX, instant-submit step 2), and the silent-429 rate-limit trap with pacing and resume-from-JSON

### 3D Printing

- **3d-printing/** - Programmatic mesh CAD without CAD software: parse STL/3MF, measure real geometry in a derived design frame, build mating parts (flanges, enclosures, bolt bosses) with trimesh + manifold3d booleans, verify by numeric clash checks before handoff. Includes `case-study-rack-enclosure.md` (3-iteration bolt-down tub build with iteration log) and `destaco-rack-reference.md` (measured geometry of the rack the case study used, for future lid/panel work).

## Usage

These skills are designed to be read by AI agents to understand role-specific responsibilities, workflows, and best practices. Each skill provides:

- Core responsibilities and accountabilities
- Decision-making frameworks
- Collaboration patterns with other roles
- Key principles and best practices
- Integration points with tools and processes

## Contributing

When creating new skills or updating existing ones, follow the established pattern:

1. Clear title and one-line summary
2. Core responsibilities section
3. Detailed workflows and processes
4. Decision frameworks
5. Collaboration patterns
6. Key principles

## Related

- [OpenClaw](https://github.com/openclaw/openclaw)
- [Agent Skills](https://clawhub.ai)
