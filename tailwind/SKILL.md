---
name: tailwind
description: >
  Tailwind CSS configuration, customization, composition patterns, and pitfalls.
  Covers tailwind.config.js shape, theme extension, design tokens via theme.extend,
  responsive and state variants, @apply usage, and common misconfigurations
  (content paths, dynamic class strings). Use when configuring or extending Tailwind
  in a project, debugging missing styles, deciding whether to extract @apply
  components, or wiring design tokens into Tailwind. For token strategy, semantic
  layers, and accessibility baselines, pair with the `design-system/` skill.
---

# Tailwind CSS Skill

Utility-first CSS. The whole stylesheet is composed of single-purpose classes; you compose layouts in markup.

This skill covers Tailwind itself. For token decisions and design-system structure on top of Tailwind, see `design-system/SKILL.md`.

---

## When to reach for Tailwind

- You want to ship UI fast without hand-rolling CSS files per component.
- You want a consistent visual scale enforced at the class level (spacing, type, color).
- The team is comfortable reading utility-dense markup.

When NOT to: a project that already has a mature CSS architecture (BEM, CSS Modules, design-system component library) — adding Tailwind on top usually just creates two ways to do everything.

---

## Configuration

### `tailwind.config.js` shape (v3)

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/views/**/*.{erb,html}",
    "./app/components/**/*.{rb,erb,html}",
    "./app/javascript/**/*.js",
  ],
  theme: {
    extend: {
      colors: { /* see Customization */ },
      spacing: { /* ... */ },
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
  ],
}
```

### `theme.extend` vs. `theme` (override)

- `theme.extend` — adds to Tailwind's defaults. Almost always what you want.
- `theme` (top-level) — replaces Tailwind's defaults for that key. Use only when you genuinely want to forbid the defaults (e.g., locking color to a strict brand palette).

```js
// EXTEND: keeps Tailwind's reds, blues, etc. and adds `brand`
theme: { extend: { colors: { brand: "#0F62FE" } } }

// OVERRIDE: ONLY `brand` is available; no slate, gray, blue, etc.
theme: { colors: { brand: "#0F62FE", white: "#fff", black: "#000" } }
```

### Tailwind v4 note

v4 moved most configuration into CSS via `@theme` directives and removed `tailwind.config.js` for many setups. The shape and semantics of tokens are the same; the file they live in differs. If your project is on v4, add tokens like:

```css
@theme {
  --color-brand: #0F62FE;
  --spacing-gutter: 1.5rem;
}
```

The rest of this guide uses the v3 JS-config form because it's still the most common; translate to `@theme` if you're on v4.

### Content paths

Tailwind only generates classes it sees in the files listed under `content`. Forgetting a path is the #1 cause of "my class isn't working":

- Add ALL paths that produce HTML/markup — Rails views, partials, ViewComponent files (`.rb` AND `.html.erb`), JS that builds class strings.
- Globs must match real extensions. `*.erb` does not match `*.html.erb` unless you write `*.{erb,html.erb}` — when in doubt, use `**/*.{erb,html,rb,js}`.

---

## Customization Patterns

### Semantic vs. primitive colors

Define a **primitive** scale (the raw colors) and **semantic** roles on top. Semantic names are what views should use.

```js
theme: {
  extend: {
    colors: {
      // primitives
      slate: { /* defaults are fine */ },
      brand: { 50: "#EFF5FF", 500: "#0F62FE", 900: "#001D6C" },
      // semantic
      surface: {
        DEFAULT: "var(--surface)",
        muted: "var(--surface-muted)",
      },
      accent: { DEFAULT: "var(--accent)" },
      danger: { DEFAULT: "var(--danger)" },
    },
  },
}
```

```css
:root {
  --surface: theme('colors.white');
  --surface-muted: theme('colors.slate.50');
  --accent: theme('colors.brand.500');
  --danger: theme('colors.red.600');
}
.dark {
  --surface: theme('colors.slate.900');
  --surface-muted: theme('colors.slate.800');
}
```

Views use `bg-surface`, `text-accent`, `bg-danger` — never `bg-blue-500` directly. Dark mode and rebrands then change CSS variables, not every view.

### Spacing & type

Extend, don't replace. Add only what's missing — usually a couple of larger sizes or a few brand-specific font sizes.

```js
extend: {
  spacing: { 18: "4.5rem", 88: "22rem" },
  fontSize: {
    "display": ["3.5rem", { lineHeight: "1", letterSpacing: "-0.02em" }],
  },
}
```

---

## Composition

### `@apply` sparingly

`@apply` lets you bundle utilities into a CSS class. Tempting; usually wrong.

- **Use it** for tightly-coupled, single-purpose components that appear many times and need DRY (e.g., `.prose-card`).
- **Avoid it** as a way to "abstract" utilities into CSS classes. You're recreating BEM with extra steps.
- **Never** use `@apply` to build a whole component library — extract a real component (ViewComponent, Stimulus controller wrapping markup, partial) instead.

```css
/* OK: high-frequency, semantically coherent */
.btn {
  @apply inline-flex items-center px-4 py-2 rounded-md font-medium
         transition focus-visible:outline focus-visible:outline-2;
}
.btn-primary { @apply btn bg-accent text-white hover:bg-brand-700; }
```

### Component classes vs. utility classes

Default to utilities in markup. Extract a class (or a component) only when:

1. The same long utility string appears in 3+ places, AND
2. Changing it should change all of them, AND
3. It has a meaningful name.

If you can't think of a name, you don't need a class.

---

## Responsive & State Variants

### Breakpoints

Default scale: `sm` (640), `md` (768), `lg` (1024), `xl` (1280), `2xl` (1536). Mobile-first — `md:flex` means "flex from md and up".

Avoid adding custom breakpoints unless the design genuinely demands it. Each new breakpoint multiplies markup variants.

### State variants

```html
<button class="bg-accent hover:bg-brand-700 focus-visible:outline focus-visible:outline-2
               disabled:opacity-50 disabled:cursor-not-allowed">
```

Prefer `focus-visible:` over `focus:` for accessibility — `focus:` triggers on mouse click, which is visually noisy.

### Dark mode

```js
// tailwind.config.js
darkMode: "class", // toggle via <html class="dark">
```

Then `dark:bg-slate-900` etc. Combine with semantic colors so dark mode is a CSS-variable swap rather than a `dark:` prefix on every element.

### Custom variants

Only when the same selector pattern repeats. Example: a `data-state="open"` variant:

```js
plugins: [
  plugin(({ addVariant }) => {
    addVariant("open", '&[data-state="open"]')
  }),
]
```

---

## Common Pitfalls

1. **Class not applied → check `content` paths.** Run `npx tailwindcss -i ... -o ...` and grep the output. If the class isn't in the build, content paths missed the file.

2. **Dynamic class strings break Tailwind's scanner.**
   ```jsx
   // BROKEN — Tailwind sees `bg-${color}-500`, not the expanded class
   <div className={`bg-${color}-500`}>
   ```
   Either map explicitly:
   ```js
   const colors = { red: "bg-red-500", green: "bg-green-500" }
   <div className={colors[color]}>
   ```
   Or whitelist via `safelist` in config (last resort — defeats tree-shaking).

3. **`@apply` with `dark:` / `hover:` doesn't work in older versions.** Always test the variant after extracting.

4. **Specificity wars with custom CSS.** Tailwind utilities are single-class selectors. Custom CSS with nested selectors will out-specify them. Either keep custom CSS to `@layer base`, or use `!important` utilities (`!bg-red-500`) — sparingly.

5. **JIT mode produces only seen classes.** When debugging "class disappears in production", check that production build sees all source files (content paths) and that no class is constructed at runtime.

6. **Forgetting `prose` plugin for content blocks.** Long-form text from markdown/CMS needs `@tailwindcss/typography` and a `prose` class — don't try to style it with utilities individually.

---

## Cross-references

- `design-system/SKILL.md` — defines what tokens to put in `theme.extend`, semantic naming conventions, accessibility baselines, and component-API patterns. Tailwind is the implementation; the design system is the spec.
- `ruby-on-rails/SKILL.md` — for Rails-specific integration (`rails-tailwindcss` gem, asset pipeline, ViewComponent styling).
