# Skills Repository

This repository contains specialized agent skills for various roles and workflows.

## Skills

### Core Development

- **Ruby-on-Rails.md** - Rails development with BDD, planning, and automated code review
- **Project-Management.md** - Blocker tracking, dependency management, and status updates

### Product & Technical Leadership

- **CPO.md** - Chief Product Officer: strategic direction, market analysis, and roadmap
- **CTO.md** - Chief Technology Officer: technical strategy, architecture, and team leadership
- **Product-Manager.md** - Product backlog management, requirements, and execution

### Frontend & Design

- **design-system/** - Design tokens, component API conventions, accessibility baselines, and Tailwind mapping (framework-agnostic; basis for the Rails ViewComponent skill)
- **tailwind/** - Tailwind CSS configuration, customization, composition patterns, and common pitfalls

### Marketing & Growth

- **seo/** - Technical & on-page SEO: metadata, canonicals, sitemaps/robots, JSON-LD structured data (incl. video), Core Web Vitals, and internal linking
- **aio/** - AI / answer-engine optimization: get cited by ChatGPT, Perplexity & Google AI Overviews via extractable answer blocks, `FAQPage` schema, `llms.txt`, and a deliberate AI-crawler policy
- **seo/backlinks.md** - Top 50 high-quality backlink sources organized by tier (editorial/media, Web 2.0, document sharing, image/video, bookmarking, business/directory), with DA scores, dofollow status, and best-use guidance
- **seo/link-building-strategy.md** - Tactical execution playbook: broken link building (Moving Man Method), digital PR with localized data, guest posting for the Citation Core, unlinked brand mentions, outreach templates, and case studies
- **content/llm-artifact-sweep/** - QA sweep for LLM-generated copy before it ships: regex artifact patterns (instruction leakage, placeholders, doubled words, truncation), language-bleed checks, a full read of the rendered page, and a post-deploy re-sweep of the live URL

### Agent Workflow

- **goal/** - Long-horizon goal-mode persistence with `goal.md`, audit discipline, and budget awareness (modeled on Codex CLI's `/goal`)

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
