---
name: ai-animation-factory
description: "End-to-end AI animation pipeline: script, frames, motion, voice, music, publish. Six tools, fully automated after setup. $12K+/month from four content types."
version: 1.0.0
author: Jimmy Lien (adapted from @0x_fokki)
license: MIT
metadata:
  hermes:
    tags: [animation, video, ai-content, youtube, automation, pipeline]
    related_skills: [youtube, youtube-short-form, video-pipeline]
---

# AI Animation Factory

End-to-end pipeline for producing AI-animated content that runs 24/7. Six tools chained together: Claude writes the script, Midjourney generates frames, Runway adds motion, ElevenLabs provides voice, Suno scores it, and Make orchestrates everything.

## Sub-Skills

- `scripting.md` — Claude prompt templates for episode scripts, brand explainers, scene breakdowns, and voiceover lines
- `framing.md` — Midjourney character sheets, environment prompts, and brand explainer visuals
- `motion.md` — Runway animation: action cuts, environmental atmosphere, brand transitions
- `voice.md` — ElevenLabs voice selection by content type, settings, and best practices
- `music.md` — Suno scoring: cinematic orchestral, upbeat corporate, ambient acoustic
- `automation.md` — Make.com orchestration: connecting all six tools end-to-end

## Content Types

Four content types, same pipeline with different parameters:

1. **Animated story series** — 6-10 minute episodes, original characters, AI voice cast, original score. Buyer: YouTube audiences. Revenue: ad share + channel growth.
2. **Brand explainer animations** — 60-90 second product videos sold to SaaS companies and startups. Buyer: direct clients. Revenue: $800-$2,500 per video.
3. **Motion comic series** — Illustrated panels pushed into Runway, narrated, cinematic pacing. Buyer: YouTube audiences. Revenue: ad share.
4. **Children's story channels** — 5-minute bedtime stories, soft animation, calming voice, ambient music. Buyer: YouTube families. Revenue: high RPM ad share.

Together they clear $12,000+/month.

## The Pipeline

```
Claude  -> Midjourney -> Runway -> ElevenLabs -> Suno -> Make
script      frames      motion      voice         music   publish
```

Six tools. Fully automated after setup. Total monthly cost: ~$349.

### Tool Costs

| Tool | Cost |
|------|------|
| Claude Pro | $200/month |
| Midjourney Standard | $30/month |
| Runway Standard | $78/month |
| ElevenLabs Creator | $22/month |
| Suno Pro | $10/month |
| Make Standard | $9/month |
| **Total** | **$349/month** |

## Common Pitfalls

1. **Character consistency** — Midjourney drifts between frames. Fix: always generate a character sheet first, then use `--cref` (character reference) on every subsequent prompt with the same character.
2. **Lip sync** — Runway won't match mouth movement to dialogue. Fix: keep dialogue to 3-4 seconds per shot, add ElevenLabs-generated sound effects to mask gaps.
3. **Pacing** — Long static frames kill retention. Fix: break scenes into 4-8 second chunks with at least one motion element per chunk (camera pan, character movement, environmental change).
4. **Music overpowering voice** — Fix: mix music at -18dB relative to voice, duck during dialogue peaks.
5. **Midjourney aspect ratio** — Use `--ar 16:9` for YouTube, `--ar 9:16` for Shorts/Reels/TikTok. Set this once in your prompt template and don't change it mid-pipeline.
6. **Runway motion too chaotic** — Use "Subtle" motion strength for brand explainers and children's stories. Reserve "Strong" for action sequences in story series.

## Revenue Benchmarks

| Source | Monthly |
|--------|---------|
| YouTube ad revenue (68K subs) | ~$4,200 |
| Licensing deals (5 ongoing) | ~$3,800 |
| Brand explainers (3 deals) | ~$2,800 |
| Content licensing | ~$1,545 |
| **Total** | **~$12,345** |

## Workflow

1. Pick a content type and load the relevant sub-skill
2. Start with `scripting.md` — Claude generates everything from the seed prompt
3. Feed scene descriptions to Midjourney (`framing.md`)
4. Animate frames in Runway (`motion.md`)
5. Generate voiceover in ElevenLabs (`voice.md`)
6. Score in Suno (`music.md`)
7. Assemble and publish via Make (`automation.md`)
8. Upload to YouTube using the `youtube` skill

## When to Use This Skill

- Building AI-animated content at scale
- Creating branded explainer videos without a studio
- Producing YouTube animation channels
- Setting up automated content pipelines
- Any task requiring the Claude → Midjourney → Runway → ElevenLabs → Suno → Make workflow