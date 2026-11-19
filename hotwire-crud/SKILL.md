---
name: hotwire-crud
description: >
  Canonical admin CRUD UI for Hotwire apps: index is a table, the row opens
  Show, Edit and Delete sit in the last column, Show edits through a turbo-frame
  modal, forms submit over Turbo, nested records are tables on the parent.
  Use when building or changing admin/index/show/edit screens, resource tables,
  nested associations on a parent, or when the user mentions CRUD, Super Admin,
  club admin, or clickable rows. Slash: /hotwire-crud
---

# Hotwire CRUD

This is the CRUD shape. Do not invent a different one (cards-as-index, edit-as-a-full-page, delete only on Show, nested records as a `<ul>`).

## Index

1. One table. Same column rhythm on every admin index.
2. The **row** is the Show control. Click/tap anywhere on the row except the actions column visits Show (`Turbo.visit`). Cursor pointer. Keyboard: Enter on the focused row.
3. **Last column** is actions only, right-aligned: **Edit** then **Delete**. Not in the header. Not on a hover menu. Not only on Show.
4. Edit is a link with `data-turbo-frame="modal"`. Delete is `button_to` DELETE with `turbo_confirm`. Both stop row navigation.
5. **Add** above the table opens New in the same modal frame (`data-turbo-frame="modal"`).
6. Empty state: one sentence plus Add. Still no card-grid of records.

## Show

1. Identity (title + key facts) then nested tables, never a unique snowflake layout per resource.
2. **Edit** on the show page opens the modal. Do not push a full-page edit.
3. Nested associations belong **on this page** as tables that follow Index rules. Example: Venue show lists Fields. Add/Edit field is a modal; Delete is in the field row.
4. Nested row click: child Show if that resource has one; otherwise the Edit modal.
5. Destroy on Show is allowed in addition to the index column, same confirm.

## Modal + Hotwire

1. Layout has exactly one `turbo_frame_tag "modal"`.
2. `new` and `edit` templates render **only** that frame (title, form, cancel). No site chrome inside the frame.
3. Form lives in the modal frame. Validation failure re-renders the frame (422).
4. Success **redirects** (303) so Turbo breaks out of the frame and refreshes the page. Do not `redirect_to` the modal template.
5. Cancel is a link that targets `modal` and renders an empty frame (or a button that sets the frame to empty).
6. No parallel non-Hotwire HTML-only edit path.

## Nested writes

Parent controller does not mass-assign children. Nested resource routes:

```
resources :venues do
  resources :fields, only: %i[new create edit update destroy], shallow: true
end
```

`new`/`edit` of the child use the same `modal` frame. After save, redirect to the **parent Show**.

## Do not

- Put Edit in the name cell and call that a row click.
- Open Edit as `/resources/:id/edit` as a full page.
- Skip Delete on the index because it also exists on Show.
- Use a definition list or card stack for a collection that has more than one record.
- Geocode, sync, or do other GET side-effects from Show. Show reads.

## Checklist before merging an admin screen

- [ ] Index is a `<table>`
- [ ] Row click/tap → Show (or Edit modal if there is no Show)
- [ ] Last column: Edit (modal) + Delete (confirm)
- [ ] Show Edit is a modal; form is Turbo
- [ ] Nested collections are tables on the parent, same actions column
