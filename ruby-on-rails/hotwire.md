---
name: hotwire
description: >
  Hotwire (Turbo + Stimulus) development guide — creating Stimulus controllers,
  Turbo Frames, Turbo Streams, project-specific patterns (modals, flash messages,
  dropdowns). Use when building interactive UI with Hotwire, creating Stimulus
  controllers, implementing real-time updates with Turbo Streams, or debugging
  Hotwire-related issues.
---

# Hotwire Development Guide

This project uses Hotwire (Turbo + Stimulus) for interactive UI without heavy JavaScript.

---

## Stimulus Controllers

### Creating a New Controller

1. Create the controller file in `app/javascript/controllers/`:

```javascript
// app/javascript/controllers/example_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "output"]
  static values = { url: String, count: Number }
  static classes = ["active", "hidden"]

  connect() {
    // Called when controller connects to DOM
  }

  disconnect() {
    // Called when controller disconnects from DOM
  }

  // Action methods
  submit(event) {
    event.preventDefault()
    // Handle action
  }
}
```

2. **IMPORTANT: Register the controller in `app/javascript/application.js`:**

```javascript
// Add import with other controllers (keep alphabetical order)
import ExampleController from "./controllers/example_controller"

// Add registration with other controllers (keep alphabetical order)
application.register("example", ExampleController)
```

3. Rebuild JavaScript:

```bash
npm run build
```

### Controller Naming Convention

| File Name | Controller Name | HTML Usage |
|-----------|-----------------|------------|
| `example_controller.js` | `example` | `data-controller="example"` |
| `mobile_menu_controller.js` | `mobile-menu` | `data-controller="mobile-menu"` |
| `inline_edit_controller.js` | `inline-edit` | `data-controller="inline-edit"` |

### Using Controllers in Views

```erb
<div data-controller="example"
     data-example-url-value="<%= some_path %>"
     data-example-count-value="5">

  <input data-example-target="input" type="text">

  <button data-action="click->example#submit">
    Submit
  </button>

  <div data-example-target="output"></div>
</div>
```

### Common Patterns

**Multiple controllers on one element:**
```erb
<div data-controller="dropdown modal">
```

**Multiple actions:**
```erb
<input data-action="input->search#filter keydown.enter->search#submit">
```

**Action with parameters:**
```erb
<button data-action="click->cart#add"
        data-cart-item-id-param="123">
```

---

## Turbo Frames

### Basic Frame

```erb
<%# In your view %>
<%= turbo_frame_tag "user_profile" do %>
  <h2><%= @user.name %></h2>
  <%= link_to "Edit", edit_user_path(@user) %>
<% end %>

<%# In edit view - frame with same ID will swap %>
<%= turbo_frame_tag "user_profile" do %>
  <%= form_with model: @user do |f| %>
    ...
  <% end %>
<% end %>
```

### Lazy Loading Frame

```erb
<%= turbo_frame_tag "comments", src: comments_path, loading: :lazy do %>
  <p>Loading comments...</p>
<% end %>
```

### Breaking Out of Frame

```erb
<%# Link targets the whole page, not just the frame %>
<%= link_to "View All", posts_path, data: { turbo_frame: "_top" } %>
```

---

## Turbo Streams

### From Controller

```ruby
def create
  @comment = Comment.create!(comment_params)

  respond_to do |format|
    format.turbo_stream
    format.html { redirect_to @comment.post }
  end
end
```

### Stream Template

```erb
<%# app/views/comments/create.turbo_stream.erb %>
<%= turbo_stream.append "comments" do %>
  <%= render @comment %>
<% end %>

<%= turbo_stream.update "comment_count", @post.comments.count %>
```

### Stream Actions

| Action | Description |
|--------|-------------|
| `append` | Add to end of target |
| `prepend` | Add to beginning of target |
| `replace` | Replace entire target element |
| `update` | Replace target's innerHTML |
| `remove` | Remove target element |
| `before` | Insert before target |
| `after` | Insert after target |

---

## Project-Specific Patterns

### Modal Pattern

```erb
<%# Link that opens modal %>
<%= link_to "Edit", edit_thing_path(thing),
    data: { turbo_frame: "modal" } %>

<%# Modal content view %>
<%= turbo_frame_tag "modal" do %>
  <div class="modal-content">
    ...
  </div>
<% end %>
```

### Flash Messages

Flash messages use the `dismissable` controller:

```erb
<div data-controller="dismissable">
  <%= flash[:notice] %>
  <button data-action="click->dismissable#dismiss">×</button>
</div>
```

### Dropdown Menus

```erb
<div data-controller="dropdown">
  <button data-action="click->dropdown#toggle">Menu</button>
  <div data-dropdown-target="menu" class="hidden">
    ...
  </div>
</div>
```

---

## Debugging

### Enable Stimulus Debug Mode

In `app/javascript/application.js`:

```javascript
application.debug = true  // Set to true temporarily
```

### Check Controller Connection

In browser console:

```javascript
// List all registered controllers
Stimulus.controllers

// Check if element has controller
document.querySelector('[data-controller="example"]').controller
```

---

## Common Mistakes

1. **Forgetting to register controller** - Controller file exists but not imported/registered in `application.js`

2. **Forgetting to rebuild** - After adding controller, run `npm run build`

3. **Wrong controller name** - `my_thing_controller.js` → `data-controller="my-thing"` (underscores become hyphens)

4. **Target not found** - Ensure target element is inside the controller's element

5. **Turbo cache issues** - Use `data-turbo-permanent` for elements that shouldn't reset on navigation
