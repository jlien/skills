---
trigger: deslop, AI slop, slop, LLM prose tics, writing tics, AI-generated prose, rhetorical tics, prose cleanup, AI writing style
---

# LLM Output Deslop

Strip the recognizable rhetorical tics of LLM-generated prose — the "slop" tells — from copy before it ships. Companion to the `llm-artifact-sweep` skill: that one catches *mechanical* artifacts (placeholders, instruction leakage, truncation) that a regex finds; this one catches the *stylistic* tells that survive every regex and make prose read machine-generated. Run the artifact sweep first (mechanical, cheap), then this pass.

## Core Responsibilities

1. Treat the ten tics below as a detection checklist: hunt for each pattern in the draft, in order, and log every hit with its location — never silently fix and move on.
2. Rewrite each hit by restating the plain content the tic was hiding. A deslop edit may not change the claim, only remove the costume.
3. Preserve deliberate voice. Sarcasm, humor, and earned rhythm stay; the *reflexive* use of these patterns goes.

## The Ten Tics

### 1. Negation-first reveal

Example: *It is not a wrong answer. It is a non-answer.*

Tell: two sentences where the first denies a rival reading and the second asserts the right one — used reflexively, though nobody actually holds the rival view.

Fix: say what it is ("This is a non-answer"). Deny a reading only when someone really holds it.

### 2. Significance designation

Example: *It is the leg that answers the actual question.*

Tell: the writer declares which item is the important one ("the actual", "the real", "the one that matters") instead of demonstrating it.

Fix: show the consequence that makes it matter, or cut the designation and let the evidence carry it.

### 3. Abstraction agency

Example: *Median hides it. The table shows it.*

Tell: abstract objects act as subjects — a median "hides", a table "shows", a number "tells". Nobody did anything.

Fix: name the actor or the mechanism ("The median hides it because two outliers pull the mean"). One instance is fine; the tic is when every sentence works this way.

### 4. Deferred noun

Example: *Five of those six rows are one cluster. The sixth is not.*

Tell: the concrete noun naming the thing is withheld to the last sentence for suspense.

Fix: name the thing first: "One of the six rows is off-distribution — the sixth."

### 5. Coy or thesis-shaped header

Examples: *What "exhausted" means* / *The one gap that does clear the bar*

Tell: headers tease or announce a thesis instead of describing content; the reader must read the section to learn what it covers.

Fix: the header states the content: "Why the exhaustion rate is inflated", "Gap: no retry path".

### 6. Aphoristic closer

Example: *It is the kind of number that looks like evidence and is not.*

Tell: the section ends on a general aphorism that sounds profound and adds no information — a sentence that would work as an epigraph on any topic.

Fix: end on the specific finding or the action.

### 7. Straw-man knockdown

Example: *"It thinks twice as long" is the obvious reading, and it is wrong.*

Tell: the writer invents a naive reading ("the obvious interpretation", "you might think") and defeats it, to look rigorous.

Fix: address real, documented misreadings only. If nobody would read it that way, cut.

### 8. Fragment cadence

Example: *Six legs. One GPU, one server build, one sampler, one question set.*

Tell: staccato fragments used as rhythm rather than for genuine punch — often several in a row.

Fix: one fragment per beat, only where real emphasis is wanted; otherwise a normal sentence.

### 9. Dressed metaphor

Example: *That is information loss wearing the costume of a style fix.*

Tell: a metaphor does the explanatory work: "wearing the costume of", "dressed up as", "laundered into".

Fix: state the relation plainly: "Calling it a style fix hides that information is lost."

### 10. Label-first framing

Example: *The fucking left column of this table.*

Tell: the writer labels a pattern instead of showing it — the label replaces the content. (The example is self-referential on purpose: it names the pattern instead of demonstrating anything.)

Fix: show the thing first; label afterwards if the name helps.

## How to Run the Pass

1. Read the draft once end to end without editing. Note where the prose "performs" rather than informs.
2. Second pass: hunt each of the ten tics explicitly. Log hit, location, and which tic.
3. Rewrite each hit using the fix above. If the rewrite loses information, the tic was carrying content — keep it and note why.
4. Re-read aloud. Anything you'd be embarrassed to hear in a human colleague's mouth goes another round.

## Decision Framework

- **Deslop**: anything shipping — blog posts, docs, emails, app copy, PR descriptions, commit messages.
- **Keep the tic**: deliberate humor, one fragment used for genuine punch, and direct quotes of the tics themselves (as this skill does).
- **Frequency test**: one instance in a long document is style; three or more of the same tic in a page is a tell. The tics cluster — finding one means look for the others.

## Collaboration Patterns

- `llm-artifact-sweep` — run it first. Mechanical artifacts before stylistic tics; a regex hit and a tic can hide in the same sentence.
- `content-brief` — that skill drafts to brief; this is the cleanup pass before ship.
- `code-review` — the same author/reviewer loop applies here: report findings with exact text and location, never fix silently.

## Key Principles

- A deslop edit must not change the claim, only remove the costume.
- The tics are tells because they *cluster*; one usually means more.
- When in doubt, prefer the plain sentence.
