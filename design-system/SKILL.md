---
name: design-system
description: >
  Design system foundations — design tokens (color, spacing, type, radius, shadow,
  motion), semantic vs. primitive layering, Tailwind mapping, component API
  conventions (variants, sizes, slots, controlled/uncontrolled), and accessibility
  baselines (WCAG AA contrast, focus visibility, keyboard navigation, reduced motion).
  Framework-agnostic; this skill is the spec, not the implementation. Use when
  defining tokens, naming a component API, deciding semantic vs. primitive colors,
  or setting accessibility floors. Pair with `tailwind/SKILL.md` for implementation
  details. The Rails ViewComponent skill (`ruby-on-rails/view-component.md`) consumes the component contracts defined here.
---

# Design System Skill

A design system is the contract between design intent and shipped UI. It exists so engineers don't have to make taste decisions in the middle of building features, and so the visual language stays consistent as the team grows.

This skill is **framework-agnostic**. It defines tokens, naming, and component conventions. For how to *implement* tokens in CSS, see `tailwind/SKILL.md`. For Rails-specific component implementations, see `ruby-on-rails/view-component.md`, which consumes the contracts defined here.

---

## When to formalize a design system

Formalize when at least two of these are true:

- More than one engineer ships UI regularly.
- The same component (button, modal, form) gets re-implemented inconsistently across the codebase.
- A rebrand or dark-mode rollout is realistic in the next year.
- Accessibility regressions keep surfacing in review or QA.

If none apply, you don't need a design system — you need consistent components. Don't over-build.

---

## Design Tokens

Tokens are the smallest visual decisions, named. Every other UI choice composes them.

### The two-layer model

1. **Primitives** — raw values: `color.blue.500`, `space.4`, `font.size.16`. Stable, neutral names. Should look like a swatch palette, not like product features.
2. **Semantic** — role-based aliases over primitives: `color.surface.default`, `color.accent`, `color.danger`, `space.gutter`, `font.size.body`. Views consume only semantic tokens.

Why two layers: rebrands and theme changes (dark mode) swap semantic → primitive mappings. Views never change.

```
View uses:           bg-surface  text-accent  p-gutter
Semantic resolves:   surface = white  accent = blue.500  gutter = space.4
Primitive defines:   white = #FFFFFF   blue.500 = #0F62FE   space.4 = 1rem
```

### Color

**Primitives:** A scale per hue (50–900), plus utility colors (white, black, neutral grays). Keep counts low — the more hues, the more decisions to argue about.

**Semantic roles** (minimum):
- `surface.default`, `surface.muted`, `surface.raised`
- `text.default`, `text.muted`, `text.inverted`
- `border.default`, `border.strong`
- `accent.default`, `accent.hover`
- `success`, `warning`, `danger`, `info`
- `focus` (ring color)

Naming rule: a role that needs `default` ALSO needs `hover`, `active`, `disabled` for interactive elements. Define them together; don't sprinkle them later.

### Spacing

A geometric scale beats free choice. Default: `0, 1, 2, 4, 8, 12, 16, 24, 32, 48, 64` (px) or the matching `rem` scale. Tailwind's default scale is fine.

Add **semantic** spacing for layout intent: `space.gutter` (between sibling components), `space.section` (between page sections), `space.inline` (within a single component).

### Typography

Per font:
- **Family** (`sans`, `serif`, `mono`).
- **Size + line-height pairs** — never define size without its line-height.
- **Weight** scale (3 weights max for most products: regular / medium / bold).
- **Letter-spacing** for display sizes only.

Semantic roles: `text.body`, `text.caption`, `text.heading.{1..4}`, `text.display`. Bind size + line-height + weight together.

```js
// Tailwind mapping example
fontSize: {
  body:    ["1rem",    { lineHeight: "1.5",  fontWeight: "400" }],
  caption: ["0.875rem",{ lineHeight: "1.4",  fontWeight: "400" }],
  h1:      ["2rem",    { lineHeight: "1.15", fontWeight: "700" }],
  display: ["3.5rem",  { lineHeight: "1",    fontWeight: "700", letterSpacing: "-0.02em" }],
}
```

### Radius, shadow, motion, breakpoints

- **Radius** — 3–4 steps: `none`, `sm`, `md`, `lg`, `full`. Pick once, apply everywhere.
- **Shadow** — `xs`, `sm`, `md`, `lg`. Tie to elevation (`raised`, `overlay`, `modal`).
- **Motion** — duration tokens (`fast: 120ms`, `base: 200ms`, `slow: 320ms`) and easing tokens (`standard`, `entrance`, `exit`). Always honor `prefers-reduced-motion`.
- **Breakpoints** — match Tailwind defaults unless design genuinely needs more. Each breakpoint adds variants to maintain.

### Naming conventions

- Lowercase, dot-separated: `color.surface.default`, `space.gutter`, `text.heading.1`.
- No product names in tokens (`color.cta` not `color.checkout-button`).
- Never bake state into a primitive (`color.blue.500` is fine; `color.blue.hover` is not — `hover` is a semantic concept).

---

## Tailwind Mapping

Tokens land in Tailwind via `theme.extend`. Keep primitives and semantics separate; map semantics to CSS variables so theming is a variable swap.

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        // primitives
        brand: { 50: "#EFF5FF", 500: "#0F62FE", 900: "#001D6C" },
        // semantic — point to CSS vars
        surface: {
          DEFAULT: "var(--surface-default)",
          muted:   "var(--surface-muted)",
        },
        accent: {
          DEFAULT: "var(--accent-default)",
          hover:   "var(--accent-hover)",
        },
        danger: { DEFAULT: "var(--danger)" },
      },
      spacing: { gutter: "1.5rem", section: "4rem" },
      borderRadius: { sm: "4px", md: "8px", lg: "12px" },
      boxShadow: {
        raised:  "0 1px 2px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.10)",
        overlay: "0 8px 24px rgba(0,0,0,0.16)",
      },
    },
  },
}
```

```css
/* app/assets/stylesheets/tokens.css */
:root {
  --surface-default: theme('colors.white');
  --surface-muted:   theme('colors.slate.50');
  --accent-default:  theme('colors.brand.500');
  --accent-hover:    theme('colors.brand.700');
  --danger:          theme('colors.red.600');
}
.dark {
  --surface-default: theme('colors.slate.900');
  --surface-muted:   theme('colors.slate.800');
}
```

For deeper Tailwind mechanics (config shape, content paths, `@apply`, variants), see `tailwind/SKILL.md`.

---

## Component API Conventions

A component's API IS its design contract. Bad APIs metastasize; good ones constrain choices.

### Variants

Variants are **mutually exclusive states** of the same component. `<Button variant="primary | secondary | ghost | danger" />`. Reach for variants when the component plays a different *role*, not when it has a different *size*.

Don't pile variants past ~5. If you need more, you have multiple components masquerading as one.

### Sizes

Orthogonal to variants. `size="sm | md | lg"`. Tie sizes to spacing/type tokens, not to raw px.

### Slots

When a component wraps user-provided content, expose **named slots** rather than a wall of props.

```erb
<%= render Card.new do |c| %>
  <% c.with_header { "Account" } %>
  <% c.with_body do %>
    ...arbitrary content...
  <% end %>
  <% c.with_footer { link_to "Manage", profile_path } %>
<% end %>
```

Slots beat config-prop sprawl: they let consumers compose without the component knowing every layout case.

### Controlled vs. uncontrolled

- **Uncontrolled** — component manages its own state (e.g., a Disclosure that opens/closes itself). Default for self-contained UI.
- **Controlled** — caller owns the state, component is a pure render of that state. Required when state must sync with URL, server, or other components.

Never mix. A component is one or the other; if it must support both, expose two clear modes (`<Modal open>` controlled vs. `<Modal>` uncontrolled with a trigger).

### Naming

- Component names: `PascalCase`, singular noun (`Button`, `Modal`, `DataTable`).
- Compound components: dot-namespace (`Tabs.List`, `Tabs.Tab`, `Tabs.Panel`).
- Boolean props: positive form (`disabled`, `loading`), not negative (`notDisabled`).
- Event props: `on<Verb>` (`onClick`, `onClose`).
- Avoid product names in component names (`UserCard`, not `CheckoutUserCard`).

### Props as configuration vs. composition

**Configuration** — small, finite props that select a variant. Good for: visual style, size, alignment.

**Composition** — children/slots that allow arbitrary structure. Good for: content, custom internals, escape hatches.

Rule of thumb: if you find yourself adding a 7th boolean prop to handle a one-off case, that case wants composition (a slot or a child component) instead.

---

## Accessibility Baseline

Non-negotiable floor for every component:

- **Color contrast** — WCAG AA: 4.5:1 for body text, 3:1 for large text (≥18px or 14px bold) and UI components / graphical objects. Use a contrast checker on every semantic-color pair.
- **Focus visibility** — every interactive element shows a visible focus indicator. Default to `:focus-visible` (keyboard-only); never `outline: none` without a replacement.
- **Keyboard navigation** — all interactive elements reachable and operable with keyboard alone. Test every component with Tab / Shift-Tab / Enter / Space / Esc / arrow keys.
- **Semantic HTML** — buttons are `<button>`, links are `<a>`, headings are `<h1..h6>`. ARIA is for filling gaps, not replacing semantics.
- **Reduced motion** — wrap non-essential animation in `@media (prefers-reduced-motion: reduce)` and disable or shorten.
- **Screen reader labels** — icon-only buttons get `aria-label`. Form controls get `<label>` (visible or `sr-only`). Decorative images get `alt=""`.
- **Color isn't the only signal** — don't convey errors / required state with color alone; pair with text or icon.

Adding a new component? Run through this list before merging. Skip none.

---

## Governance

A design system rots without rules for change.

- **Token changes** — primitives are append-only by default; renaming a primitive cascades everywhere. Semantic remappings are cheap because views use the role, not the value.
- **Component API changes** — additive props are fine; removing or renaming a prop is a breaking change. Deprecate in two steps: (1) keep old prop working, log a console warning, (2) remove in next major.
- **Review** — design system PRs need a designer + an engineer review. Both check: does this break the model? Does the name describe the role, not the implementation?
- **Documentation** — every new token or component lands with: name, purpose, example, accessibility notes. Out-of-date docs are worse than missing docs.

---

## What this skill does NOT cover

- **Framework-specific component implementations.** Rails consumers should use `ruby-on-rails/view-component.md`, which references this skill for contracts. Other frameworks (React, Vue) would have their own implementation skills.
- **Brand identity / visual design.** This is engineering-side: how a design system is structured and consumed in code, not how to design it visually.
- **Content style / copywriting.** Voice and tone are a separate system.

---

## Cross-references

- `tailwind/SKILL.md` — Tailwind configuration mechanics, content paths, `@apply`, variants, common pitfalls. The implementation layer beneath the tokens defined here.
- `ruby-on-rails/SKILL.md` — for the Rails projects that consume this design system.
- `ruby-on-rails/view-component.md` — the Rails ViewComponent implementation layer that consumes the component API conventions defined here.
