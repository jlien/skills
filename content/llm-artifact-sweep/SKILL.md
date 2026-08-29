# LLM Artifact Sweep

**Generic QA step for any LLM-generated copy destined for a blog, webpage, app screen, email, or social post.** Run it before shipping — as the last step before commit/deploy, and again on the live URL after deploy. It exists because artifacts (stray tokens, instruction leakage, placeholders, language bleed) survive every structural check: a page can return 200 with a perfect `<h1>` and still say "until you cancel)Skip." in the second paragraph.

## Core Responsibilities

1. Treat **rendered output**, not the source file, as the object under test. Fetch the URL (or render the component), strip tags, and read the prose.
2. Run the four passes below **in order**; any hit fails the sweep and blocks shipping until fixed and re-swept.
3. Report pass/fail per pass with the exact offending text and location. Never silently fix and re-render without reporting what was found.

## The Four Passes

### Pass 1 — Regex sweep (mechanical)

Run every pattern below case-insensitively over the final prose. Keep the pattern list in a repo-local reference file and extend it whenever a new artifact class is observed (record the example, derive the pattern).

| Class | Patterns (examples, not exhaustive) |
|---|---|
| Instruction leakage | `)Skip.`, `Certainly!`, `Sure, here`, `Here is the`, `Here's the`, `I've written`, `As an AI`, `I cannot`, `Note: this is`, `Let me know if` |
| Placeholders | `TODO`, `FIXME`, `XXX`, `lorem ipsum`, `[insert`, `[your `, `{var`, `<placeholder`, `TBD`, `example.com` (outside docs about examples) |
| Doubled words | `the the`, `a a`, `is is`, `to to`, `and and` (word-boundary regex; skip legitimate repeats like "had had" in dialogue) |
| Dangling punctuation | unbalanced `(`/`)`/`[`/`]`/`{`/`}`, `""`, `..`, ` ,`, ` .`, ` – ` orphaned mid-sentence |
| Truncation | paragraph not ending in `.!?…:"` + `)`, headline cut mid-phrase |
| Meta-commentary | `as mentioned`, `as requested`, `per your instructions`, `in this document, we will`, `this section discusses` |

Tools: `grep -nE` over the stripped text, or the language's regex facility. One combined pass is fine; log which pattern matched where.

### Pass 2 — Language-bleed check

LLMs writing English routinely bleed the target/foreign language in (or vice versa) — pinyin, simplified-Chinese glyphs in Japanese content, romaji in English segments, untranslated fragments:

- Scan English-facing copy for CJK codepoints that aren't intentional (e.g. pinyin
  tone marks like `nǐ`, or simplified-Chinese hanzi like 鱼/这 in a Japanese-facing
  page — Japanese uses traditional/kanji forms). Use the project's own checker where
  one exists, e.g. Kōfuku's `bin/kofuku-check-chinese`.
- Scan Japanese-facing copy for romaji words that should be kana.
- Confirm any *intentional* foreign terms are marked up consistently (tags, quotes, glosses).

### Pass 3 — Full human read of the rendered page

The pass that catches what regexes can't. Fetch the **rendered** page (curl + strip tags, or headless render for JS-driven pages), then actually read every sentence top to bottom, checking:

- Does each sentence parse? (Artifacts often produce *grammatical* nonsense — "Subscriptions renew automatically until you cancel)Skip." reads fine to a skimming eye.)
- Is every claim true and consistent with the rest of the page (no contradiction between sections, dates sane, names spelled one way)?
- Is the register/voice correct for the audience (no corporate hedging in a casual post, no slang in legal copy)?
- Are links, prices, dates, and numbers plausible and current?

Budget for this: it is a slow read, not a scan. On a 1,000-word page, expect to spend real attention. Skimming defeats the pass.

### Pass 4 — Post-deploy re-sweep

After the change is committed and deployed to production:

1. Fetch the **live URL** (not localhost, not the worktree).
2. Re-run Passes 1–2 verbatim on the fetched body.
3. Spot-read the sections edited in this change (Pass 3 depth).
4. Only then report the task complete, with the live URL.

Catching an artifact at this stage costs one follow-up commit; skipping it costs a customer-facing typo for however long nobody reads carefully. The `/terms` incident (2026-08-28): structural check passed, `)Skip.` shipped, caught by the user.

## Decision Framework

- **Any Pass 1–2 hit** → fix the source, re-render, re-sweep from Pass 1. Do not hand-wave "minor".
- **Pass 3 finds a problem** → fix, then full re-sweep (artifacts cluster — one hit raises the prior for others).
- **Pass 4 finds a problem** → fix + re-deploy + re-verify, then write the pattern into Pass 1's list so it can't recur.
- **Ambiguous hit** (e.g. quoted artifact in an article *about* artifacts) → judge intent; the sweep flags, a human-or-agent read decides.

## Collaboration Patterns

- **Copywriter/content agents**: run the sweep on their output before publishing; feed rejected examples back into the pattern list.
- **Deploy pipeline**: Pass 4 pairs with any health check — a page that fails the sweep is not "deployed OK", whatever the HTTP status says.
- **Project QA gates** (e.g. a glyph gate, a pronunciation gate): this sweep is *additive* — it checks the copy layer, not media or grammar.

## Key Principles

- **Rendered output is the truth.** Source files lie; the browser doesn't.
- **Sweeps are cheap; embarrassment is expensive.** Four passes cost minutes.
- **Every escape improves the net.** An artifact that ships means a missing pattern — add it.
- **Fail closed.** No confirmed artifact = do not ship, regardless of deadline pressure.
- **Keep the pattern list local and living.** The table above is a seed, not a ceiling.
