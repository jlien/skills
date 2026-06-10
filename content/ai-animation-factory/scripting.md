---
name: scripting
description: "Claude prompt templates for episode scripts, brand explainers, scene breakdowns, and voiceover lines"
---

# Claude: Script Generation

Everything starts here. Claude generates the episode script, visual scene breakdowns for Midjourney, voiceover lines for ElevenLabs, and the brief for Suno.

## Episode Script Prompt

```
Write a 6-10 minute animated story script. Include:

1. Episode title and logline (1 sentence)
2. Scene-by-scene breakdown with visual descriptions (for Midjourney)
3. Character dialogue and voiceover narration (for ElevenLabs)
4. Emotional beats and pacing notes (for Runway motion timing)
5. Music cues (for Suno brief)

Character guidelines:
- Give each character a distinct visual identity (color, shape, style)
- Keep dialogue natural and conversational
- No line should exceed 4 seconds of speaking time
- Narration can be longer but break at punctuation

Output format:
SCENE 1: [location] - [time of day]
VISUAL: [detailed description for Midjourney prompt]
CAMERA: [movement: static, pan, zoom, follow]
DIALOGUE (CHARACTER): "..."
NARRATION: "..."
MUSIC: [mood cue for Suno]
```

## Brand Explainer Prompt

```
Write a 60-90 second brand explainer script for [COMPANY]. Include:

1. Hook (0-5 seconds) — start with a pain point or surprising stat
2. Problem (5-20 seconds) — why the current solution fails
3. Solution (20-45 seconds) — how the product works, 2-3 key features
4. Social proof (45-60 seconds) — results, testimonials, or stats
5. CTA (60-90 seconds) — clear next step

Style: Professional but not corporate. Conversational tone.
Visual style: Clean, minimal, motion-friendly (avoid cluttered scenes).

Output format:
[0:00-0:05] HOOK
VISUAL: [scene description]
VOICEOVER: "..."
```

## Scene Breakdown Format

For each scene, Claude outputs:

```
SCENE 3: [location] - [time of day]
DURATION: ~8 seconds
VISUAL PROMPT: [Midjourney-ready prompt with style, lighting, composition]
CHARACTER REF: [which character, reference sheet name]
CAMERA: [pan left, static, slow zoom in, etc.]
DIALOGUE (NAME): "line"
NARRATION: "line"
MUSIC MOOD: [tense, warm, triumphant, ambient, etc.]
NEXT: [transition to next scene: cut, dissolve, match cut]
```

## Tips

- Ask Claude to generate scene prompts optimized for Midjourney (include style tags, lighting, aspect ratio)
- Request ElevenLabs-ready formatting: separate dialogue blocks by character, mark emotional tone
- Ask for Suno brief: genre, BPM, instruments, mood progression across the episode
- Generate a character sheet prompt separately — this becomes the anchor for all Midjourney character consistency