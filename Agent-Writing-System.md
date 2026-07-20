# Agent Writing System

Stop telling AI tools "no em dashes", "stop saying delve", "don't sound like AI". You never gave it a writing system. Every README, PR description, and landing page ships in the same AI voice, and you ban words one at a time.

George Orwell wrote the fix 80 years ago — six rules from "Politics and the English Language" (1946). Paste them into your global CLAUDE.md / AGENTS.md and every session picks them up.

## The Six Rules

1. **Never use a long word where a short one will do.**
2. **If it is possible to cut a word out, cut it out.**
3. **Never use the passive where you can use the active.**
4. **Never use a metaphor, simile, or other figure of speech which you are used to seeing in print.**
5. **Never use a foreign phrase, a scientific word, or a jargon word if you can think of an everyday English equivalent.**
6. **Break any of these rules sooner than say anything outright barbarous.**

## 6 Code Blocks for AGENTS.md / CLAUDE.md

Copy-paste these blocks into your project's `AGENTS.md` (Hermes) or `CLAUDE.md` (Claude Code) file:

### Block 1: Short Words

```
- Never use a long word where a short one will do.
```

### Block 2: Conciseness

```
- If it is possible to cut a word out, cut it out.
```

### Block 3: Active Voice

```
- Never use the passive where you can use the active.
```

### Block 4: Fresh Language

```
- Never use a metaphor, simile, or other figure of speech which you are used to seeing in print.
```

### Block 5: Plain English

```
- Never use a foreign phrase, a scientific word, or a jargon word if you can think of an everyday English equivalent.
```

### Block 6: The Escape Clause

```
- Break any of these rules sooner than say anything outright barbarous.
```

## Combined Block (single paste)

```markdown
## Writing System

The following rules come from George Orwell's "Politics and the English Language" (1946). Apply them to all written output:

- Never use a long word where a short one will do.
- If it is possible to cut a word out, cut it out.
- Never use the passive where you can use the active.
- Never use a metaphor, simile, or other figure of speech which you are used to seeing in print.
- Never use a foreign phrase, a scientific word, or a jargon word if you can think of an everyday English equivalent.
- Break any of these rules sooner than say anything outright barbarous.
```

## Why This Works

- **Positive instructions** work better than negative bans. "Never use the passive" is a framework the AI can apply, while "don't sound like AI" is a vague prohibition.
- **Anchored in a known authority** — Orwell's essay is a canonical reference the AI can reason about.
- **Self-correcting** — Rule 6 (the escape clause) prevents the system from becoming pedantic or robotic.
- **Concise** — 6 rules fit in a single paragraph, easily loaded into context every session.
- **Proven** — These rules have survived 80 years because they work.

## Integration

Add the **Combined Block** to:
- `CLAUDE.md` (for Claude Code projects)
- `AGENTS.md` (for Hermes Agent projects)
- The global `~/.claude/CLAUDE.md` (for system-wide coverage)

## Source

George Orwell, "Politics and the English Language" (1946). Via [@Voxyz_ai](https://x.com/voxyz_ai/status/2078857039116156978).