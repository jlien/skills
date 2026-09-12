# Debugging Rails exceptions

A stack trace is a spec that has not been written yet. Do not patch the raising line first.

## Reproduce, then fix

1. **Read the trace, not the guess.** Controller, action, template line, params (`id`, nested ids). That is the request the spec must make.
2. **Identify the nil.** `undefined method 'x' for nil` means an optional association, empty collection, or missing nested record. Recreate **that shape** in the spec (teamless `ChannelBinding`, person without `user`, venue without coordinates) — not only the happy path the existing examples cover.
3. **Write the request spec first.** Sign in as the same role, `GET`/`POST` the same path, with that data already in the database. Assert `have_http_status(:ok)` (or the intended status) **and** that the awkward record is visible (a label, an id, a safe fallback).
4. **Run it. It must fail the same way** (`ActionView::Template::Error` / `NoMethodError` wrapping the same method). If it passes, you did not reproduce the bug.
5. **Then change application code.** Prefer a domain label (`binding.label`) or an explicit branch over a silent `&.` that hides a missing type. Scan sibling templates for the same dereference (`grep binding.team.name`).
6. **Re-run the spec, then the full suite.** The new example stays; it is the regression lock.

## What not to do

- Rescue in the view, `try`, or `defined?` to make the 500 go away without a spec.
- Fix only the reported template when grep shows the same call in `/admin` or a partial.
- Use `&.` when the model already knows how to name the record (`ChannelBinding#label` covers team rooms, staff rooms, all-staff, and DMs).

## After a user correction

Add the pattern to the project's `tasks/lessons.md` so the next exception of this class starts at step 1.
