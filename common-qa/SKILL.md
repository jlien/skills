# Common QA (25 Scenarios That Break Real Sites)

One-line summary: **a standing checklist of the 25 ways everyday apps silently break — run it against any web app at any stage, not just before launch.** Every scenario here is a case real users eventually find and that nothing else in the QA stack catches by default.

Source: the "ask Claude to break your site" 25-scenario QA checklist (https://x.com/acecreamu/status/2126285852590383160).

## Core Responsibilities

- Run every scenario below against the app in a real browser and record what happens. Scenarios are stage-agnostic: run the full list before a launch, and re-run after any auth, form, upload, payment, or infrastructure change.
- Document every failure and rank it by severity. Fix nothing until the fix plan is approved — QA reports; the fix loop is a separate decision.
- If a scenario cannot be run directly, provide exact test instructions instead of claiming it passed. A test that was never run is not a pass.
- Give the QA agent access to the repository and an isolated staging environment with test accounts — never production data or real credentials.

## The 25 Scenarios

### Auth

- Sign up with an email that is already registered
- Enter an incorrect password multiple times
- Ask for several password-reset links
- Open an expired reset link
- Access protected pages while signed out
- Log out, then return using the back button
- Confirm access is revoked after logout or account deletion

### Forms and inputs

- Submit every form without filling it in
- Paste unusually long text into every field
- Upload the wrong file type
- Upload a file larger than the permitted limit

### Payments and transactions

- Click payment and submit buttons twice
- Refresh the page during a transaction

### Network and resilience

- Use the website on a slow connection
- Disconnect halfway through an action

### Devices, browsers, and accessibility

- Open every page on a small phone
- Navigate using only a keyboard
- Disable images and check what remains understandable
- Test the website across different browsers

### Errors and edge states

- Visit missing or invalid URLs
- Test every empty state
- Check signup, payment and password-reset emails
- Confirm errors are recorded correctly

### Security and recovery

- Check that private data never appears in the browser console
- Verify that a backup can be restored in an isolated staging environment

## Workflow

1. Provision an isolated staging environment with test accounts, seeded so each scenario has something to act on (an existing registered email, files of every wrong type, a transaction in flight).
2. Work the scenarios top to bottom. Record for each: the scenario, what was expected, what actually happened, and evidence (screenshot, console output, email content). A scenario that passes silently gets a one-line "passed" so the run is auditable.
3. Rank every failure by severity and write the fix plan. Stop there — nothing gets fixed until the plan is approved.
4. After fixes land, re-run the failed scenarios (not the whole list) to prove each one.

## Decision Framework

- **Cannot run it? Write it.** If the environment blocks a test (email delivery, cross-browser matrix, backup restore), the deliverable is precise manual instructions — never a claimed pass.
- **Evidence or it didn't happen.** Screenshots, console logs, and email bodies are the record; adjectives are not.
- **Re-run after change, not just at launch.** Any change touching auth, forms, uploads, payments, emails, or infrastructure re-triggers the affected sections at minimum.
- **Report, then wait.** Severity-ranked findings with an approved plan keep QA and fixes accountable to each other.

## Collaboration Patterns

- **`launch-qa` skill** — at launch time, run the five personas (impatient, skeptic, mobile, non-native speaker, breaker) to catch what confuses first-time users, then run this checklist to catch what silently breaks. The two overlap deliberately; together they are the pre-ship gate.
- **`code-review` skill** — the approved fix batch lands through normal code review.
