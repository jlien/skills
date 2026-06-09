---
name: automation
description: "Make.com orchestration: connecting all six tools end-to-end"
---

# Make: Pipeline Orchestration

Connect Claude, Midjourney, Runway, ElevenLabs, and Suno into an automated pipeline.

## Make Scenario Structure

```
Trigger: New script in Google Sheets / Notion database
  ↓
Module 1: Claude API — Generate scene breakdowns from script
  ↓
Module 2: Midjourney (via Discord webhook) — Generate frames for each scene
  ↓
Module 3: Runway API — Animate frames
  ↓
Module 4: ElevenLabs API — Generate voiceover from script
  ↓
Module 5: Suno API — Generate score
  ↓
Module 6: Google Drive — Upload all assets organized by episode
  ↓
Module 7: Slack notification — "Episode ready for assembly"
```

## API Endpoints

| Tool | Integration |
|------|-------------|
| Claude | Anthropic API (Make module available) |
| Midjourney | Via Discord webhook (no direct API) — use Make's Discord module |
| Runway | Runway API (REST) — Make HTTP module |
| ElevenLabs | ElevenLabs API (REST) — Make HTTP module |
| Suno | Suno API (REST) — Make HTTP module |

## Trigger Options

- **Google Sheets row** — Add a new row with script text, trigger the pipeline
- **Notion database** — New entry in a "Scripts" database
- **Slack message** — Send a script to a dedicated channel
- **Webhook** — Push a script from any external tool

## Automation Tips

- Start with semi-automation: Claude generates the script, you review, then the pipeline runs
- Add quality gates: after each step, store the output to Google Drive for manual review before continuing
- Use Make's error handling: if a step fails, send a Slack alert rather than silently dropping the episode
- Rate limit awareness: Midjourney via Discord is the bottleneck — add delays between frame generation calls

## Assembly

After all assets are generated, assembly happens outside the pipeline:
1. Download assets from Google Drive
2. Assemble in DaVinci Resolve (free) or Premiere Pro
3. Sync voiceover to animated clips
4. Add music and sound effects
5. Export and upload to YouTube (use the `youtube` skill)

## Common Pitfalls

- **Midjourney Discord integration unreliable** — Discord webhooks can fail. Add retry logic with exponential backoff.
- **Make runs too fast** — Some APIs have rate limits. Add delay modules between API calls (2-5 seconds).
- **File naming gets messy** — Use consistent naming: `episode_01_scene_03_frame.jpg`, `episode_01_voiceover.wav`, `episode_01_score.mp3`
- **Make scenario times out** — For long pipelines, split into multiple scenarios triggered sequentially rather than one massive scenario