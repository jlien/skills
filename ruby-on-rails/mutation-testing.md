---
name: mutation-testing
description: >
  Mutation testing in Ruby/Rails with mutant — configure mutant-rspec,
  subject expressions and the config file, the Rails hooks (eager load +
  per-worker database isolation), incremental CI runs, handling alive
  mutations, and the commercial-license caveat. Use when SimpleCov says
  90%+ but you doubt the tests assert anything real, or after CRAP
  triage flags high-value methods.
---

# Mutation testing with mutant

Coverage says a line **executed**. Mutation testing says the tests would **fail** if the line were wrong. That difference is the whole game: SimpleCov will happily report 90% for a suite that exercises code without asserting anything about it.

**mutant** is mutation testing for Ruby: it rewrites your code (AST mutations), runs the subject's tests per mutation, and reports **alive** mutants — changes the suite failed to catch.

```ruby
# lib/person.rb
def adult?
  @age >= 18
end
```

```ruby
# spec: age 19 → true, age 17 → false. Passes, 100% covered.
```

Mutant flips `>=` to `>` (plus dozens of other operators: arithmetic, logic, statement removal, return-value changes). The suite passes the `>` mutant: age 18 exactly was never tested. That survivor is the bug line coverage cannot see. (Example from mutant's own README.)

Every alive mutant has exactly two resolutions — mutant's framing, and the right one:

1. **Keep the mutation** — the tests already specify correct behavior and the original code was redundant; accept the simplification.
2. **Add the missing specification** — the original behavior is right; write the test that distinguishes it from the mutant.

## The tool, and what it costs

mutant, by Markus Schirp (`mbj/mutant`), is what the Ruby ecosystem actually uses; the older generation (Heckle and similar) has been abandoned for over a decade. Support covers Ruby 3.2–4.0 and Rails 7.2–8.1 at the time of writing — check the repo for the current matrix.

**Licensing:** free for open-source repos (run with `--usage opensource`). **Commercial use requires a paid subscription** — $30/month or $250/year per developer at the time of writing; check [mutant's commercial doc](https://github.com/mbj/mutant/blob/main/docs/commercial.md) for current terms.

Practical consequence for a private Rails shop: apply it to the subjects where a silent bug costs the most (billing, auth, permissions, money math, invariants), not repo-wide. Mutation testing on code that merely persists data buys little for what it costs.

## Install & configure (RSpec)

```ruby
# Gemfile, :test group
gem "mutant-rspec", require: false
```

```sh
bundle install
```

Config file (`.mutant.yml`, `config/mutant.yml`, or `mutant.yml`) — minimal, non-Rails:

```yml
---
requires:
  - ./lib/my_app.rb
integration:
  name: rspec
matcher:
  subjects:
    - MyApp*
  ignore:
    - MyApp::Legacy*
```

`integration: name:` accepts `rspec`, `minitest`, or `test-unit` — each has its own integration gem (`mutant-rspec`, `mutant-minitest`, …) and doc.

```sh
bundle exec mutant run                        # config-file subjects
bundle exec mutant run 'MyApp::Money#add'     # CLI expression REPLACES config subjects
bundle exec mutant run --fail-fast            # stop at the first alive mutant
MUTANT_JOBS=4 bundle exec mutant run          # workers; CLI -j > env > config > CPU count
```

## Subject expressions

| Expression | Selects |
|---|---|
| `MyApp::Invoices` | all subjects on that constant |
| `MyApp::Invoices*` | the constant, recursively |
| `MyApp::Money#add` | one instance method |
| `MyApp::Money.total` | one class method |
| `MyApp::Money#` | all instance methods of `Money` |
| `MyApp::Money.` | all class methods of `Money` |
| `descendants:ApplicationController` | controllers, plus `ApplicationController` itself |
| `source:lib/**/*.rb` | subjects defined under top-level constants in those files |

Also useful: `--ignore-subject MyApp::Legacy*` on the CLI (adds to config ignores). Inline opt-out of a single method — a comment directive with no reason argument:

```ruby
# mutant:disable
def legacy_rate
```

## Rails integration

Rails needs three adjustments: boot in test mode, load all subjects eagerly, and give parallel workers their own databases. From mutant's Rails doc — the recipes are verified in its CI against Rails 7.2/8.0/8.1 on PostgreSQL and SQLite:

```yml
# config/mutant.yml
---
requires:
  - ./config/environment
environment_variables:
  RAILS_ENV: test
integration:
  name: rspec
hooks:
  - config/mutant/hooks.rb
```

`config/mutant/hooks.rb` skeleton — **the eager-load hook is mandatory**: without it, autoloaded classes are invisible to subject discovery and runs silently match nothing.

```ruby
hooks.register(:env_infection_post) do
  Rails.application.eager_load!
end

hooks.register(:setup_integration_post) do
  # disconnect the parent process from the template database (see docs/rails.md)
end

hooks.register(:test_worker_process_start)     { |index:| }  # fires under `mutant test`
hooks.register(:mutation_worker_process_start) { |index:| }  # fires under `mutant run`
```

Database isolation — copy the full recipes from [mutant's rails.md](https://github.com/mbj/mutant/blob/main/docs/rails.md). Mutant's repo keeps those fenced recipes byte-identical to a CI-verified example app, so what you copy is what is tested:

- **PostgreSQL** — each worker gets `CREATE DATABASE … TEMPLATE <test_db>` into `<test_db>_mutant_worker_<index>` via the raw `pg` driver.
- **SQLite** — run `RAILS_ENV=test bin/rails db:test:prepare` first; each worker then gets a file copy under `tmp/mutant/`.
- Register **both** worker hooks if you use both `mutant run` and `mutant test` — they fire under different commands, and dropping one lets that mode's workers trample the shared template database.
- PostgreSQL: skipping the `setup_integration_post` disconnect fails at the first worker with `source database "..." is being accessed by other users`.
- Isolate more than the database, with the same hook events: per-worker ActiveStorage roots, Redis/Memcached namespaces, Sidekiq/GoodJob queue namespaces.

Quick checks when a run behaves oddly:

```sh
bundle exec mutant environment show                    # confirm the loaded configuration
bundle exec mutant environment subject list MyApp*     # confirm subjects are discoverable
bundle exec mutant environment irb                     # IRB with the full mutant environment
```

`subject list` returning nothing for a namespace you know exists = the eager-load hook is missing or not running.

## Sessions

Every run is recorded under `.mutant/results/` (add `.mutant/` to `.gitignore`):

```sh
bundle exec mutant session list                          # past sessions, newest first
bundle exec mutant session show                          # full report of the latest
bundle exec mutant session subject                       # alive/total per subject
bundle exec mutant session subject 'MyApp::Money#add'    # alive mutants for one subject
bundle exec mutant session gc --keep 50                  # prune old session files
```

## Runtime discipline

Cost ≈ (mutants per subject) × (subject test runtime) ÷ jobs. A 40-mutant method with a 3-second spec set is roughly two minutes of work on one core. Squeeze in this order:

1. **Scope subjects.** While developing, run one: `bundle exec mutant run 'MyApp::SomeService#call'`. Repo sweeps are scheduled work, not a coding-loop activity.
2. **Deterministic specs.** Every mutation re-runs the subject's tests; time-dependent or order-dependent specs breed false alive mutants (and false kills through timeouts). Freeze time (`travel_to`), use fixed sequences and factories, keep tests transactional, and remove cross-example coupling.
3. **Bound analysis time.** `mutation: timeout:` (fractional seconds) caps worst-case mutants. Keep `coverage_criteria: timeout: false` (the default) — a hang must not count as a kill.
4. **Start from CRAP-flagged methods.** CRAP (`crap.md`) tells you where tests are thin; mutant tells you whether the thin tests assert. Code that merely persists data rarely justifies the expense.

## CI shape

- **PR gate (incremental — mutant's own recommendation):** `bundle exec mutant run --since origin/main` mutates only subjects touched since the reference (inside, `git diff <ref>` semantics; good references: `HEAD~1` locally, the integration branch on CI). Know the limits: only *direct* source changes select a subject — a changed constant or caller that alters another subject's behavior does not select it.
- **Nightly full pass** — mutant's recommended pattern once full passes outgrow CI patience: incremental on PRs, full `mutant run` on a schedule.
- **Legacy retrofit** — same incremental mode; sweep survivors down namespace by namespace instead of staring at a repo-wide warning wall.
- Gating every PR on mutant in a commercial repo means license seats for everyone whose CI uses it — price the rollout before promising the gate.

## Relationship to the rest of this skill

- CRAP (`crap.md`) picks the first subjects: complex + under-specified → spec them, then mutation-test them.
- The BDD flow (`SKILL.md` §6) writes one failing spec per bug; mutant is the audit layer verifying the specs you have actually *distinguish* behavior — that a mutation of the implementation fails them.
- This is not a default CI gate: runtime plus licensing. Treat it as scheduled or PR-scoped opt-in on flagged subjects.

## Pitfalls

1. **Flaky specs poison everything.** Mutant re-runs the subject's tests dozens of times; one flaky example manufactures noise. Fix determinism before the first run.
2. **Missing eager-load hook** → subjects silently match nothing. Diagnose with `mutant environment subject list`.
3. **Registering one Rails worker hook but not the other** → isolation works under `mutant run` but not `mutant test` (or the reverse). Register both.
4. **CLI expressions replace config subjects** — someone runs `mutant run Foo#bar` "on CI" and the config's other subjects silently don't run. Config subjects for CI; CLI expressions for human-driven narrow runs.
5. **Custom `integration: arguments:` overwrite mutant's rspec defaults** — you must keep `--fail-fast` and point at the specs directory, or runs break in confusing ways.
6. **Every `mutant:disable` needs a reason.** The directive takes none, so the justification lives in the surrounding comment and must survive code review. For whole namespaces, prefer `matcher: ignore:`.
7. **Vacuous assertions.** Specs that pass regardless (`expect(true).to be(true)`, rescue-everything blocks) kill zero mutants and run for every one — pure cost, zero signal. If no spec can distinguish the original from a mutant, declare the mutant a simplification (option 1: keep it) instead of writing theater.
8. **Focusing on the wrong code.** ERB/HAML templates, schemas, migrations, generated files, and Active Record DSL one-liners (`has_many`, trivial `scope`s) produce cost without signal. Prefer models with logic, services and form objects, serializers, and money math.
9. **Coverage theater.** Do not install mutant to raise a mutation score for its own sake. Each alive mutant is a decision — spec or simplification — not a fill-the-bar exercise.

## Cross-references

- `crap.md` — the triage stage that picks subjects
- `debugging.md` — the same pressure on exceptions: reproduce, then assert
- `Code-Review.md` — review eye for assertion quality (mutant finds what review misses)
