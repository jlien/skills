# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repo is a collection of Markdown "agent skills" — prompt-style specifications meant to be loaded by AI agents (not executed). There is no build system, test suite, package manager, or runtime. Edits are documentation edits.

## Skill File Conventions

Skills come in two shapes:

- **Single-file skill** — a `*.md` file at the repo root (e.g. `CPO.md`, `CTO.md`, `Product-Manager.md`, `Project-Management.md`).
- **Multi-file skill** — a directory whose entry point is `SKILL.md`, with sub-skill `*.md` files alongside it (e.g. `ruby-on-rails/SKILL.md` + `ruby-on-rails/hotwire.md`). Use this shape when the role needs technology-specific companion guides. Sub-skills are referenced by relative filename from `SKILL.md`.

New skills must follow the established structure (see `README.md`):

1. Title + one-line summary
2. Core Responsibilities
3. Detailed workflows / processes
4. Decision framework
5. Collaboration patterns (how this role interacts with the others in the repo)
6. Key Principles

Keep skills self-contained. Cross-skill references use the bare filename (e.g. `` `Notion.md` skill ``, `` `Code-Review.md` skill ``). Some referenced sub-skills (Notion, Code-Review) are mentioned by `ruby-on-rails/SKILL.md` but do not exist in this repo yet — only `hotwire.md` has been added so far.

## Skill Relationships

The skills form an implicit org chart that future edits should preserve:

- **CPO.md** sets strategy → **Product-Manager.md** translates into backlog → **CTO.md** ensures technical fit → **ruby-on-rails/SKILL.md** executes → **Project-Management.md** tracks blockers and status across all of it.
- The "Collaboration Pattern" section in each leadership skill explicitly names the others. When changing a responsibility in one file, check the matching subsection in the related files so the handoffs stay consistent.

## Notion as External Source of Truth

Multiple skills (`Ruby-on-Rails.md`, `Project-Management.md`) treat Notion as the canonical Product Backlog and reference status transitions: `Not started` → `Approved to Begin` → `In progress` → `Done`. Keep this vocabulary identical across skills — divergence between files will confuse the agents that load them.

## Rails Skill Particulars

`ruby-on-rails/SKILL.md` encodes opinionated workflow rules that go beyond generic Rails guidance and should be preserved when editing:

- Plan mode is the default for any non-trivial task; re-plan on the first sign of trouble rather than pushing through.
- Bug fixes start with a failing test (BDD), then subagents make it pass.
- After implementation, the Code-Review skill must run **automatically** — not on user request.
- Corrections from the user must be captured in `tasks/lessons.md` (in the consuming Rails project, not this repo).
- Tech stack assumed by the skill: Rails 8+, Hotwire (Turbo + Stimulus), Tailwind v4, PostgreSQL, RSpec, Rubocop.
