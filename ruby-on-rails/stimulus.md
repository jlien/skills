---
name: stimulus
description: >
  Advanced Stimulus controller patterns — lifecycle hooks, controller composition
  via outlets, nested controllers, form patterns, testing, performance, and
  anti-patterns. Use when building non-trivial Stimulus controllers, refactoring
  existing controllers for reuse, debugging lifecycle bugs (Turbo cache, double-fires),
  or wiring controllers together. For controller basics (creating, registering,
  targets, values, parameters), see `hotwire.md`.
---

# Advanced Stimulus Patterns

This guide assumes you already know the basics from `hotwire.md`: how to create a controller, register it in `application.js`, and use targets, values, and parameters from views.

If anything below references a basic concept you haven't seen, stop and read `hotwire.md` first.

---

## Lifecycle Hooks

Stimulus controllers fire callbacks at specific moments. Use the right one — don't put `connect` work in `initialize`.

| Hook | When it fires | Use for |
|---|---|---|
| `initialize()` | Once, when the controller instance is constructed | One-time setup that doesn't touch the DOM (e.g., binding methods, building internal state) |
| `connect()` | Every time the controller's element enters the DOM | DOM setup, event listeners on `window`/`document`, starting timers |
| `disconnect()` | Every time the controller's element leaves the DOM | Cleanup: remove listeners, clear timers, abort fetches |
| `<name>TargetConnected(el)` | When a matching target appears in the DOM | React to dynamically-added targets |
| `<name>TargetDisconnected(el)` | When a matching target leaves the DOM | Tear down per-target state |
| `<name>ValueChanged(current, previous)` | When a value attribute changes (also fires once on connect) | Re-render, re-fetch, reconcile UI to new value |

### Turbo cache gotcha

Turbo Drive caches the previous page when navigating. A controller can therefore `connect` twice for what looks like the same element: once for the cached preview, once for the real page. Symptoms: doubled event listeners, doubled API calls.

Two defenses:

```javascript
connect() {
  if (this.element.hasAttribute("data-turbo-preview")) return
  // ...real setup
}
```

Or mark the element so Turbo skips it on cache:

```erb
<div data-controller="metrics" data-turbo-permanent>...</div>
```

### Always pair `connect` with `disconnect`

Every listener, timer, observer, or fetch started in `connect` MUST be torn down in `disconnect`. Otherwise navigating between pages leaks them.

```javascript
connect() {
  this.boundHandler = this.handle.bind(this)
  document.addEventListener("keydown", this.boundHandler)
  this.timer = setInterval(() => this.tick(), 1000)
  this.abortController = new AbortController()
}

disconnect() {
  document.removeEventListener("keydown", this.boundHandler)
  clearInterval(this.timer)
  this.abortController.abort()
}
```

---

## Controller Composition

Don't build a 300-line "god controller". Compose smaller controllers.

### Outlets (Stimulus 3.2+)

Outlets let one controller talk to another by CSS selector — the right tool for sibling/cousin controllers.

```javascript
// app/javascript/controllers/cart_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static outlets = ["badge"]
  static values = { count: Number }

  countValueChanged(value) {
    if (this.hasBadgeOutlet) this.badgeOutlet.update(value)
  }
}
```

```javascript
// app/javascript/controllers/badge_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  update(count) {
    this.element.textContent = count
  }
}
```

```erb
<div data-controller="cart" data-cart-badge-outlet=".cart-badge">
  ...
</div>
<span class="cart-badge" data-controller="badge"></span>
```

Outlet callbacks `<name>OutletConnected` / `<name>OutletDisconnected` fire when matching elements appear/disappear — useful when outlets are inside Turbo Frames.

### Base controllers (extend)

When two controllers share concrete behavior, extract a base class.

```javascript
// app/javascript/controllers/base/dismissable_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  dismiss() {
    this.element.remove()
  }
}
```

```javascript
// app/javascript/controllers/flash_controller.js
import DismissableController from "./base/dismissable_controller"

export default class extends DismissableController {
  connect() {
    setTimeout(() => this.dismiss(), 5000)
  }
}
```

Use extension only when the relationship is genuinely "is-a". Otherwise prefer outlets (composition) or shared utilities.

### Shared utilities (functions, not classes)

For pure logic — formatting, parsing, debouncing — export plain functions from `app/javascript/utils/` and import them. Don't dress them up as controllers.

### Extend vs. compose decision

- **Extend** when behavior is truly identical and the parent class is meaningful on its own.
- **Compose with outlets** when controllers cooperate but live independently.
- **Use utilities** when the logic isn't tied to the DOM at all.

---

## Nested Controllers

Two controllers on the same element work fine: `data-controller="dropdown modal"`.

For parent/child controllers in nested elements, prefer:

1. **Custom DOM events via `dispatch`** — loose coupling, works across Turbo Frames.

```javascript
// child controller
this.dispatch("selected", { detail: { id: this.idValue } })
```

```erb
<div data-controller="parent"
     data-action="child:selected->parent#handleSelection">
  <div data-controller="child" data-child-id-value="42">...</div>
</div>
```

2. **Outlets** when the parent must call methods on the child (not just react to events).

3. **Avoid** reaching across the DOM with `document.querySelector` from inside a controller. That's a smell — use outlets or events instead.

---

## Form Patterns

### Debounced input

```javascript
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input"]
  static values = { delay: { type: Number, default: 300 } }

  initialize() {
    this.search = this.debounce(this.search.bind(this), this.delayValue)
  }

  search() {
    this.element.requestSubmit()
  }

  debounce(fn, wait) {
    let timer
    return (...args) => {
      clearTimeout(timer)
      timer = setTimeout(() => fn(...args), wait)
    }
  }
}
```

```erb
<%= form_with url: search_path, method: :get,
              data: { controller: "search", turbo_frame: "results" } do |f| %>
  <%= f.text_field :q, data: { search_target: "input", action: "input->search#search" } %>
<% end %>
```

### Optimistic UI

Toggle the desired state immediately, let the server confirm via Turbo Stream.

```javascript
toggle(event) {
  this.element.classList.toggle("active")  // optimistic
  // form submission proceeds; server returns turbo_stream that reconciles
}
```

If the server rejects, return a Turbo Stream that re-renders the element to its true state.

### `requestSubmit` over `submit`

Always use `form.requestSubmit()` (not `form.submit()`) so Turbo intercepts and validation events fire.

---

## Testing

### System tests (Capybara)

Drive the controller through the UI it produces. Don't try to instantiate the controller directly.

```ruby
# spec/system/dismissable_flash_spec.rb
require "rails_helper"

RSpec.describe "Dismissable flash", type: :system, js: true do
  it "removes itself after click" do
    visit root_path
    expect(page).to have_css(".flash")
    find(".flash button").click
    expect(page).to have_no_css(".flash")
  end
end
```

### Asserting on behavior, not data attributes

Assert the user-visible outcome ("flash gone", "modal opens"), not the internal `data-*` state. Internal attributes are implementation detail; behavior is the contract.

### Isolating a controller

If you must unit-test a controller, mount it in JSDOM with the Stimulus `Application` and a minimal HTML fixture. This is rarely worth the effort — system tests cover more for less code.

---

## Performance

### Lazy-load heavy controllers

Stimulus loads everything registered in `application.js`. For a large controller used on one page, lazy-load it:

```javascript
// app/javascript/application.js
import { Application } from "@hotwired/stimulus"
const application = Application.start()

application.register("editor", () => import("./controllers/editor_controller").then(m => m.default))
```

### Avoid observer leaks

`MutationObserver`, `IntersectionObserver`, `ResizeObserver` instances created in `connect` MUST be `.disconnect()`-ed in the controller's `disconnect`. They're a top source of memory leaks across navigations.

### Don't re-query the DOM

Use targets. `this.inputTarget` is cached and fast. `this.element.querySelector("input")` is not, and breaks if the markup changes.

---

## Anti-patterns

1. **DOM-querying outside the controller's element.** If you need data from elsewhere on the page, use outlets or events. `document.querySelector` from a controller is almost always wrong.
2. **Business logic inside controllers.** Controllers are glue between markup and behavior. Validation rules, pricing math, and domain logic belong on the server (or in a plain JS module the controller calls).
3. **Controller-to-controller coupling without outlets.** Reading another controller's DOM, hard-coding selectors, or assuming sibling order — all brittle. Use outlets or dispatched events.
4. **Editing `data-*` attributes to drive state.** Use values (`this.fooValue = ...`) — they trigger `*ValueChanged` callbacks and stay in sync.
5. **Forgetting `disconnect`.** Every `addEventListener`, `setInterval`, `setTimeout`, observer, or `fetch` started in `connect` needs a teardown in `disconnect`.
6. **One mega-controller.** If a controller has more than ~150 lines or handles unrelated concerns, split it.
7. **Mixing Stimulus and inline `onclick`.** Pick one. Stimulus for any non-trivial behavior; nothing inline.
