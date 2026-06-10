---
name: music
description: "Suno scoring: cinematic orchestral, upbeat corporate, ambient acoustic"
---

# Suno: Original Scoring

Generate custom music that matches each content type.

## Score by Content Type

| Content Type | Style | Suno Prompt |
|--------------|-------|-------------|
| Animated story series | Cinematic orchestral | `Cinematic orchestral score, dramatic, emotional, building intensity, strings and brass, Hans Zimmer inspired, no vocals` |
| Brand explainer | Upbeat corporate | `Upbeat corporate background music, modern, clean, electronic with acoustic elements, positive, professional, no vocals` |
| Motion comic | Tense atmospheric | `Tense atmospheric score, dark ambient, subtle percussion, building tension, noir, no vocals` |
| Children's stories | Ambient acoustic | `Gentle ambient acoustic, soft piano and strings, warm, calming, bedtime story atmosphere, no vocals` |

## Episode Scoring Workflow

1. Get music cues from Claude's script (each scene has a mood cue)
2. Generate 3-5 minute tracks per episode, matching the mood progression
3. Generate a "theme" track for recurring series (use the same prompt each time for consistency)
4. Trim and cross-fade tracks to match scene changes in post

## Tips

- Generate longer tracks (3-5 minutes) — easier to trim than to extend
- Add `[intro]`, `[build]`, `[climax]`, `[outro]` markers in Suno prompts for structured scoring
- For series consistency, use the same Suno prompt seed across episodes
- Generate music BEFORE voiceover — this helps you time voice delivery to musical beats
- Mix music at -18dB relative to voice, duck during dialogue peaks

## Suno Prompt Structure

```
[Genre], [mood], [instruments], [tempo], [reference artist if helpful], no vocals
```

Example:
```
Cinematic orchestral score, emotional and building, strings with brass accents, moderate tempo starting slow then building, Hans Zimmer inspired, no vocals
```

## Common Pitfalls

- **Music too loud** — Fix: mix at -18dB relative to voiceover. Use a limiter to prevent peaks.
- **Music doesn't match scene** — Fix: generate multiple variations and match them to scenes manually, or use Suno's extended generation to create mood transitions
- **Vocals in the music** — Always include "no vocals" in the prompt unless you specifically want singing
- **Inconsistent style across scenes** — Fix: use the same prompt template with only the mood word changing (e.g. "cinematic orchestral, [tense/warm/triumphant], no vocals")