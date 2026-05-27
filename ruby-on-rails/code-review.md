# Ruby on Rails Code Review Skill

Review Claude-generated code using these 5 skills sequentially. Flag issues with file paths and line numbers, suggest concrete refactors with before/after diffs.

---

## Skill 1: Identify and Eliminate Code Smells (Structural Refactoring)

**Focus:** Duplicated code, long methods/classes, primitive obsession, DRY violations.

**Patterns:**
- Extract Method/Class — use modules/concerns for shared behavior
- Replace Conditional with Polymorphism — leverage STI or service objects
- Extract Variable — prefer symbols or inline blocks for clarity

**Checklist:**
- [ ] Methods >20 lines? Split into single-responsibility methods
- [ ] Duplicated logic across controllers/models? Move to concerns or `lib/` modules
- [ ] Models bloated with business logic? Extract to service objects or POROs
- [ ] Controllers skinny? Complex queries in query objects, not controllers or models
- [ ] Hotwire: Extracted methods handle Turbo Streams properly (not full redirects when streams are expected)
- [ ] Stimulus: Long JS methods extracted into separate controllers

**Example — Extract Service Object:**
```ruby
# BAD: Controller does too much
def update
  @user = User.find(params[:id])
  if @user.update(user_params)
    UserMailer.welcome(@user).deliver_later
    AuditLog.create(user: @user, action: 'update') if @user.admin?
    redirect_to @user, notice: 'Updated'
  else
    render :edit
  end
end

# GOOD: Service object
def update
  @user = User.find(params[:id])
  if UserUpdater.new(@user, user_params).perform
    redirect_to @user, notice: 'Updated'
  else
    render :edit
  end
end
```

---

## Skill 2: Optimize Performance and Database Interactions

**Focus:** N+1 queries, missing indexes, unoptimized Postgres usage.

**Patterns:**
- Replace Loop with Pipeline — use `map`, `select`, `pluck`
- Extract Query — scopes or query objects for reusable AR chains
- Decompose Conditional — break complex `where` clauses into named scopes
- Extract conditional query in controller to scope

**Checklist:**
- [ ] N+1 queries? Associations accessed in loops without `includes`/`preload`
- [ ] Indexes on frequently queried Postgres columns (foreign keys, timestamps, tokens)
- [ ] Using `pluck`/`select` instead of loading full AR objects when only specific fields needed
- [ ] Unnecessary DB hits in views/helpers? Memoize with `@ivar ||=`
- [ ] Hotwire updates triggering full page reloads instead of Turbo Frame updates
- [ ] Turbo Streams broadcasting efficiently via ActionCable without redundant DB polls
- [ ] Check `EXPLAIN ANALYZE` in logs for slow Postgres queries

**Example — Fix N+1:**
```ruby
# BAD
@posts.each { |post| puts post.user.name }

# GOOD
# Model scope
scope :with_users, -> { includes(:user) }
# Controller
@posts = Post.with_users.recent
```

**Example: Extract conditional query in controller to scope
```ruby
  # BAD
  class CoachClientsController < BaseController
    before_action :set_coach_client, only: [ :show, :edit, :update, :destroy ]

    def index
      @coach_clients = CoachClient.includes(:coach, :client)

      if params[:q].present?
        search = "%#{CoachClient.sanitize_sql_like(params[:q])}%"
        @coach_clients = @coach_clients.joins(:coach, :client)
          .where("users.email ILIKE ? OR users.first_name ILIKE ? OR users.last_name ILIKE ?", search, search, search)
      end

      if params[:status].present?
        @coach_clients = @coach_clients.where(status: params[:status])
      end

      @coach_clients = @coach_clients.order(created_at: :desc)
    end
  end

  # GOOD
  # Model scope
  class CoachClient
    scope :search, (lambda do |search|
      return unless search

      sanitized = "%#{CoachClient.sanitize_sql_like(search)}%"
      joins(:coach, :client)
          .where("users.email ILIKE ? OR users.first_name ILIKE ? OR users.last_name ILIKE ?", sanitized, sanitized, sanitized)
    end)

    scope :filter_status, (lambda do |status|
      return unless status 

      where(status: params[:status])
    end)
  end

  class CoachClientsController < BaseController
    before_action :set_coach_client, only: [ :show, :edit, :update, :destroy ]

    def index
      @coach_clients = CoachClient
        .includes(:coach, :client)
        .search(params[:q])
        .filter_status(params[:status])
        .order(created_at: :desc)
    end
  end

```

---

## Skill 3: Enhance Security and Input Handling

**Focus:** SQL injection, XSS, mass assignment, improper auth.

**Checklist:**
- [ ] Strong params with explicit `permit` — no `params[:model]` directly
- [ ] Authorization checks present (Pundit, CanCanCan, or manual `authorize_owner!`)
- [ ] User inputs sanitized in views (`sanitize` helper, no `raw`/`html_safe` on user data)
- [ ] CSRF tokens present in Turbo forms
- [ ] No dynamic SQL interpolation — use parameterized queries
- [ ] LIKE/ILIKE queries use `sanitize_sql_like` on user input to escape `%` and `_` wildcards
- [ ] Secrets/credentials not hardcoded — use Rails credentials or ENV
- [ ] Stimulus: No inline `eval` or dynamic script execution
- [ ] Tailwind: No user input injected into CSS class strings

**Example — Parameterize + Guard:**
```ruby
# BAD
@user.update(params[:user])

# GOOD
def user_params
  params.require(:user).permit(:name, :email)
end
return head :forbidden unless current_user.admin?
```

**Example — LIKE Wildcard Injection:**
```ruby
# BAD: User can pass % or _ to manipulate LIKE pattern matching
.where("name ILIKE ?", "%#{params[:q]}%")

# GOOD: Escape LIKE wildcards in user input
search = "%#{Model.sanitize_sql_like(params[:q])}%"
.where("name ILIKE ?", search)
```

---

## Skill 4: Improve Readability and Idiomatic Style

**Focus:** Ruby/Rails conventions, expressive code.

**Patterns:**
- Rename Method/Variable — snake_case, descriptive names
- Inline Temp — chain methods fluidly
- Pipeline over loops — `select`, `map`, `&:method`

**Checklist:**
- [ ] Ruby idioms used: blocks over loops, `tap`/`then` for chaining, symbols for keys
- [ ] Rails conventions: RESTful routes, partials for views, helpers for view logic
- [ ] Tailwind classes grouped semantically (not scattered)
- [ ] Stimulus controllers lightweight, using `data` attributes idiomatically
- [ ] Self-documenting code preferred over comments
- [ ] `turbo_frame_tag` helpers used idiomatically (not manual HTML)

**Example — Idiomatic Ruby:**
```ruby
# BAD
results = []
posts.each { |p| results << p.title if p.published? }

# GOOD
results = posts.select(&:published?).map(&:title)
```

---

## Skill 5: Promote Modularity and Testability

**Focus:** Composable, testable units. Composition over inheritance.

**Patterns:**
- Move Method — to concerns or services
- Extract Module — mixins for shared behavior
- Replace Subclass with Fields — prefer composition

**Checklist:**
- [ ] View logic extracted to partials/components (ViewComponent if applicable)
- [ ] Services are injectable/testable (no global state dependencies)
- [ ] Multi-step DB operations wrapped in `transaction` blocks
- [ ] Turbo Stream broadcasts extracted to background jobs where appropriate
- [ ] Each Stimulus controller focuses on one behavior
- [ ] Test coverage exists for new/refactored code (model specs, request specs); SimpleCov stays ≥ 90% and the change doesn't lower the project's percentage
- [ ] Concerns are cohesive (not "junk drawer" modules)

**Example — Extract Concern:**
```ruby
# BAD: Business logic in model
class Post < ApplicationRecord
  def publish_and_notify
    update(published: true)
    NotificationService.new(self).send_all
  end
end

# GOOD: Concern + Service
module Publishable
  extend ActiveSupport::Concern
  def publish!
    update!(published: true)
  end
end
```

---

## Review Process

Apply skills **in order**: Smells -> Performance -> Security -> Readability -> Modularity.

For each issue found:
1. State the **skill** and specific checklist item
2. Reference the **file:line**
3. Show **before/after** diff
4. Rate severity: **critical** (security/data loss), **warning** (performance/bugs), **suggestion** (style/maintainability)

Use RuboCop and Brakeman output to supplement manual review.
