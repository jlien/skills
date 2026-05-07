---
name: view-component
description: >
  ViewComponent (the gem) usage in Rails — file layout, slot APIs, sidecar assets,
  variants and sizes via constructor arguments, Stimulus integration, preview /
  Lookbook, testing with render_inline, when to use a component vs. a partial.
  This skill is the Rails-specific implementation layer that consumes the design
  contracts defined in `design-system/SKILL.md`. Use when building reusable Rails
  view components (Button, Modal, Card, DataTable), refactoring partials into
  components, deciding component API shape, or wiring a component to Stimulus.
---

# ViewComponent Skill

ViewComponent (the gem: `gem "view_component"`) gives Rails a real component model — a class + template pair you can instantiate, test, and document in isolation. This is the implementation layer for the design system; it is **not** the design contract.

- For *what tokens to use, what variants/sizes/slots a component should expose, and what accessibility floor to meet*, read `design-system/SKILL.md`. That skill is the spec.
- For *Tailwind config, semantic colors, `@apply` rules*, see `tailwind/SKILL.md`.
- For *Stimulus controllers wired to component markup*, see `hotwire.md` (basics) and `stimulus.md` (advanced).

This skill assumes you have those open. It covers the Rails-specific implementation patterns only.

---

## When to use ViewComponent vs. a partial

Default to a partial. Reach for ViewComponent when at least one of these is true:

- The view has non-trivial logic (conditionals, loops, helpers) that wants to live in a class.
- It needs **slots** — multiple distinct content regions a caller fills.
- It is reused across multiple controllers/views and you want to test it in isolation.
- It is part of the design system (Button, Modal, Card, etc.) and benefits from a stable API.

If the partial is a flat template with no logic, leave it as a partial. ViewComponent has overhead; don't pay it without payoff.

---

## File Layout

ViewComponent expects a sidecar pattern under `app/components/`:

```
app/components/
  button_component.rb
  button_component.html.erb
  card_component.rb
  card_component.html.erb
  card_component.css            # optional sidecar CSS (rare with Tailwind)
  card_component.js             # optional sidecar JS (rare with Stimulus)
```

Class name MUST end in `Component` and match the file. Namespacing works:

```
app/components/forms/
  text_field_component.rb       # Forms::TextFieldComponent
  text_field_component.html.erb
```

---

## Component Class Shape

```ruby
# app/components/button_component.rb
class ButtonComponent < ViewComponent::Base
  VARIANTS = %i[primary secondary ghost danger].freeze
  SIZES    = %i[sm md lg].freeze

  def initialize(label: nil, variant: :primary, size: :md, type: "button", **html_options)
    raise ArgumentError, "unknown variant: #{variant}" unless VARIANTS.include?(variant)
    raise ArgumentError, "unknown size: #{size}"       unless SIZES.include?(size)

    @label = label
    @variant = variant
    @size = size
    @type = type
    @html_options = html_options
  end

  private

  def classes
    [base_classes, variant_classes, size_classes, @html_options[:class]].compact.join(" ")
  end

  def base_classes
    "inline-flex items-center justify-center rounded-md font-medium " \
    "transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 " \
    "disabled:opacity-50 disabled:cursor-not-allowed"
  end

  def variant_classes
    {
      primary:   "bg-accent text-white hover:bg-accent-hover",
      secondary: "bg-surface-muted text-text-default hover:bg-surface-raised",
      ghost:     "bg-transparent text-text-default hover:bg-surface-muted",
      danger:    "bg-danger text-white hover:bg-danger-hover",
    }.fetch(@variant)
  end

  def size_classes
    { sm: "h-8 px-3 text-sm", md: "h-10 px-4 text-base", lg: "h-12 px-6 text-lg" }.fetch(@size)
  end
end
```

```erb
<%# app/components/button_component.html.erb %>
<button type="<%= @type %>"
        class="<%= classes %>"
        <%= tag.attributes(@html_options.except(:class)) %>>
  <%= @label || content %>
</button>
```

Two contracts shown above:
1. **Variants and sizes are validated in `initialize`** — fail loudly if a caller passes garbage.
2. **`**html_options` passthrough** — callers add arbitrary attributes (`id`, `data-*`, `aria-*`) without a prop explosion.

---

## Slots

Slots are how ViewComponent expresses **composition**. Use them whenever a component wraps caller-supplied content beyond a single string/block.

### `renders_one` (single named slot)

```ruby
class CardComponent < ViewComponent::Base
  renders_one :header
  renders_one :footer
end
```

```erb
<%# card_component.html.erb %>
<div class="rounded-md bg-surface shadow-raised">
  <% if header? %><div class="border-b p-4"><%= header %></div><% end %>
  <div class="p-4"><%= content %></div>
  <% if footer? %><div class="border-t p-4"><%= footer %></div><% end %>
</div>
```

```erb
<%= render CardComponent.new do |c| %>
  <% c.with_header { "Account settings" } %>
  Body content here…
  <% c.with_footer { link_to "Manage", profile_path } %>
<% end %>
```

### `renders_many` (collection slot)

```ruby
class TabsComponent < ViewComponent::Base
  renders_many :tabs, "TabComponent"
end
```

```erb
<%= render TabsComponent.new do |t| %>
  <% t.with_tab(label: "Overview") { "..." } %>
  <% t.with_tab(label: "Activity") { "..." } %>
<% end %>
```

### Slot rules

- Use slots when a caller would otherwise pass multiple long strings or blocks via separate props.
- The unnamed `content` block is itself a slot — use it for the primary body.
- Don't use slots for trivial single-string fields — that's what kwargs are for.

---

## Mapping the Design System

Each component is a contract from `design-system/SKILL.md` made concrete in Rails. Keep the mapping clean:

| Design system concept | ViewComponent expression |
|---|---|
| Variant (mutually exclusive role) | `variant:` kwarg validated against a constant set |
| Size | `size:` kwarg validated against a constant set |
| Slot | `renders_one` / `renders_many` |
| Controlled vs. uncontrolled | Two distinct components, OR a clear flag (`open:` present → controlled; absent → component manages own state via Stimulus) |
| Token (color, spacing) | Tailwind class keyed to the semantic token (`bg-accent`, `p-gutter`) — never raw values |
| Accessibility floor | Component MUST satisfy WCAG AA contrast, focus visibility, keyboard nav. Tested in component spec. |

If you find yourself adding a 7th boolean prop, the design-system skill says you want a **slot or a child component** instead. Re-read the "Props as configuration vs. composition" section of `design-system/SKILL.md`.

---

## Stimulus Integration

Components frequently wrap a Stimulus controller. Two clean patterns:

### Component owns the controller wiring

```erb
<%# disclosure_component.html.erb %>
<div data-controller="disclosure"
     data-disclosure-open-value="<%= @open %>">
  <button data-action="click->disclosure#toggle"
          data-disclosure-target="trigger">
    <%= trigger %>
  </button>
  <div data-disclosure-target="panel" class="<%= "hidden" unless @open %>">
    <%= content %>
  </div>
</div>
```

```ruby
class DisclosureComponent < ViewComponent::Base
  renders_one :trigger
  def initialize(open: false); @open = open; end
end
```

The component is the only thing that knows how to wire `data-controller` / `data-target` / `data-action`. Callers pass content; controller behavior is encapsulated.

### Sidecar JS (rare)

If a component has truly local JS that nothing else uses, you can ship it as a sidecar:

```
button_component.rb
button_component.html.erb
button_component.js
```

You'll need to import the sidecar in `application.js`. In practice: prefer a regular Stimulus controller in `app/javascript/controllers/` and reference it from the component template. Sidecar JS exists; it's rarely the right call.

For Stimulus patterns (lifecycle, outlets, testing), see `stimulus.md`.

---

## Preview / Lookbook

ViewComponent ships `ViewComponent::Preview`. Lookbook (`gem "lookbook"`) wraps it in a UI for browsing, theming, and trying variants — strongly recommended for any non-trivial component library.

```ruby
# test/components/previews/button_component_preview.rb
class ButtonComponentPreview < ViewComponent::Preview
  def primary
    render(ButtonComponent.new(label: "Save", variant: :primary))
  end

  def all_sizes
    render(ButtonComponent.new(label: "Click me", size: :lg))
  end
end
```

Visit `/rails/view_components` (or `/lookbook`) in development.

Treat previews as **the design system's storefront**. Every component should have a preview covering: each variant, each size, each slot in use, disabled state, loading state.

---

## Testing

```ruby
# test/components/button_component_test.rb (or spec)
require "test_helper"

class ButtonComponentTest < ViewComponent::TestCase
  test "renders primary variant" do
    render_inline(ButtonComponent.new(label: "Save"))
    assert_selector "button.bg-accent", text: "Save"
  end

  test "passes html_options through" do
    render_inline(ButtonComponent.new(label: "Save", id: "save-btn", data: { turbo: false }))
    assert_selector "button#save-btn[data-turbo='false']"
  end

  test "raises on unknown variant" do
    assert_raises(ArgumentError) { ButtonComponent.new(label: "x", variant: :wat) }
  end
end
```

What to test:
- Each variant/size renders the right classes (you don't need every class — pick the discriminating one).
- Argument validation rejects garbage.
- Slots render in the right place.
- Accessibility-critical attributes are present (`aria-label` for icon-only, `type` on buttons, `for` on labels).

What NOT to test:
- The exact Tailwind class string. It will change. Test the discriminating class only.
- Visual output. That's preview/Lookbook's job (and a designer's eyes).

---

## Common Anti-patterns

1. **Reaching for ViewComponent for every partial.** Plain partials are still fine. The bar for a component is logic, slots, reuse, or testability — not "I might want it later".
2. **Stuffing arbitrary HTML into kwargs.** If the caller wants to pass content, give them a slot. Strings via kwargs are for plain text and small flags.
3. **Boolean prop sprawl.** `with_icon: true, with_caret: true, with_badge: true, ...` — extract slots or split the component.
4. **Skipping variant validation.** A `case` over a string from `params` is a runtime bug waiting to ship. Validate against a constant set in `initialize`.
5. **Hardcoding raw Tailwind colors.** `bg-blue-500` couples the component to today's brand. Use `bg-accent` (semantic token from `design-system/SKILL.md`).
6. **Component reaching outside its tree.** A ViewComponent should not call `current_user`, `flash`, `params`, or hit the database. Pass what it needs in. Helpers are a grey area — prefer kwargs.
7. **Preview gaps.** Component without a preview = component nobody can find or audit. Add the preview when you add the component.

---

## Cross-references

- `design-system/SKILL.md` — tokens, component API conventions, accessibility floor. The contract this skill implements.
- `tailwind/SKILL.md` — Tailwind config, `@apply`, content paths, variants. The styling layer.
- `hotwire.md` — Stimulus and Turbo basics for view-level interactivity.
- `stimulus.md` — advanced Stimulus patterns when a component's controller grows beyond toggle/dismiss.
- `code-review.md` — review checklist; ViewComponent-specific concerns appear under modularity and accessibility.
