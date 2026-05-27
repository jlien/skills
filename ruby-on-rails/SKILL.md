---
name: ruby-on-rails
description: >
  Rails development execution — plan mode, BDD bug fixes, subagent orchestration,
  atomic commits, automatic code review. Orchestrates principal-engineer-level
  Rails work with Hotwire, Tailwind, RSpec, Rubocop. Use when implementing
  Rails features, fixing bugs, running code reviews, refactoring Rails code,
  seeding databases, or any non-trivial Rails development task.
---

# Ruby on Rails Agent Skill

Orchestrates Rails development with extensive planning, principal engineer level execution (BDD + implementation), and proactive code review.

## Workflow Orchestration

### 1. Plan Mode Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately — don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

**When to spawn subagents:**
- Seeding database from markdown files
- Generating multiple similar files (migrations, tests)
- Research tasks (gem comparisons, API docs)
- Refactoring across multiple files
- Running test suites and analyzing failures

### 3. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes — don't over-engineer
- Challenge your own work before presenting it

### 6. Bug Fixing (TDD/BDD Approach)
- **Don't start by trying to fix it.** Start by writing a test that reproduces the bug.
- Once the test fails (proving the bug exists), spawn subagents to fix it
- Subagents prove the fix by making the test pass
- This ensures: bug is understood, fix is verified, regression is prevented
- For existing failing CI tests: go fix them without being told how

### 7. Atomic Commits
- Prefer smaller, logical commits over one large commit
- Each commit should represent one logical change (feature, fix, refactor)
- Group related files together (controller + views + tests for a feature)
- Separate unrelated changes into distinct commits
- Makes code review easier and git history more useful

---

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
- **Rails Conventions**: Follow Rails way. Use generators. Leverage framework.
- **Hotwire First**: Prefer Turbo Frames/Streams over custom JS. Stimulus for behavior.

---

## Task Management

### Notion Integration (Product Backlog)
- **The Product Backlog lives in Notion** — use `Notion.md` skill for API access
- **Starting a task**: Search Notion for the story, move it to **In Progress**
- **Completing a task**: Move the story to **Done** in Notion after all verification passes
- Always check Notion for acceptance criteria and context before starting work

### Workflow
1. **Plan First**: Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections
7. **Update Documentation**: When a new feature is complete, update `app/content/help/` docs:
   - `help-center.md` — Main user guide (served at /help)
   - `feature-comparison.md` — How do features change at different pricing levels (if applicable)
   - `support-troubleshooting.md` — Add common issues for the new feature
8. **Update Story Progress**: When working on features from `planning/` stories:
   - Check the story file for acceptance criteria and phases
   - Mark completed items with `[x]` as you finish them
   - Add completion dates to phase headers when done
9. **Code Review (Automatic)**: After implementation and tests pass, **always** run the code review agent using `Code-Review.md` skill — do NOT wait for the user to ask. Write findings to `tasks/` and address any issues before presenting the work as complete.

---

## Tech Stack Reference

- **Ruby on Rails 8+** — API and server rendering
- **Hotwire (Turbo + Stimulus)** — SPA-like UX without heavy JS
- **Tailwind CSS v4** — Utility-first styling
- **PostgreSQL** — Primary database
- **RSpec** — Testing framework
- **SimpleCov** — Test coverage measurement (min 90% line coverage)
- **SortableJS** — Drag-and-drop (via Stimulus)
- **Rubocop** — Style and Linting

---

## Test Coverage (SimpleCov)

Coverage is measured with SimpleCov on every test run. Treat the threshold as a gate, not a target — drops below it fail the suite.

**Standard:** Minimum **90% line coverage**. New and refactored code should not lower the project's coverage percentage.

**Setup** — add to the `:test` group in the `Gemfile`:
```ruby
group :test do
  gem "simplecov", require: false
end
```

SimpleCov must start **before any application code loads**, so require it at the very top of `spec/rails_helper.rb` (above `require File.expand_path(...)`):
```ruby
require "simplecov"
SimpleCov.start "rails" do
  add_filter "/spec/"
  add_filter "/config/"
  add_filter "/vendor/"
  enable_coverage :branch
  minimum_coverage line: 90, branch: 80
end
```

- `enable_coverage :branch` catches untested conditional paths that line coverage alone misses.
- `minimum_coverage` makes the suite exit non-zero below the threshold — wire this into CI so coverage regressions block merges.
- Add `coverage/` to `.gitignore`.
- Use coverage to find gaps, not to chase 100% — don't write tests for trivial accessors just to hit a number. The BDD bug-fix flow (section 6) is the source of truth for what to test.

---

## CI Gates

Every push and pull request must pass these gates before merge. A failing gate blocks the merge — never override or skip one to land work faster.

**Required checks** (each must exit non-zero on failure so CI fails):
- **Test runner** — `bundle exec rspec`. The full suite must be green.
- **Coverage** — SimpleCov's `minimum_coverage` (≥ 90% line, 80% branch). Runs as part of RSpec, so a coverage drop fails the test step.
- **Linting** — `bundle exec rubocop`. No offenses; use `rubocop -a` locally before pushing, not `--auto-gen-config` to mask them.

When setting up a new project, add a CI workflow (e.g. `.github/workflows/ci.yml`) that runs these on every PR and marks them as required status checks on the protected branch. If a gate is failing on CI, fix the root cause — do not disable the check, loosen the threshold, or add blanket `rubocop:disable` comments.

---

## Skills & Guides

Detailed guides for specific technologies:

- **`Code-Review.md`** — Code review process. **MUST** run automatically after implementation — do not wait for the user to request it.
- **`hotwire.md`** (in this directory) — Stimulus controllers, Turbo Frames/Streams, registration in application.js
- **`stimulus.md`** (in this directory) — Advanced Stimulus patterns: lifecycle hooks, controller composition via outlets, nested controllers, form patterns, testing, performance. For basics see `hotwire.md`.
- **`view-component.md`** (in this directory) — ViewComponent gem: file layout, slots, sidecar assets, variants/sizes, Stimulus integration, preview/Lookbook, testing. Implements the contracts in the top-level `design-system/` skill.
- **`Notion.md`** — Notion API via curl for Product Backlog management (search, status updates, create pages)
