---
name: voice
description: "ElevenLabs voice selection by content type, settings, and best practices"
---

# ElevenLabs: Voice Generation

Professional AI voiceover for every content type.

## Voice Selection by Content Type

| Content Type | Recommended Voice Style | Example |
|--------------|------------------------|---------|
| Animated story series | Dramatic, expressive, character-driven | Deep narrator for male lead, warm contralto for female lead |
| Brand explainer | Professional, confident, approachable | "Rachel" or "Adam" — clear, not monotone |
| Motion comic | Cinematic, atmospheric, slightly gravelly | "Antoni" or deep custom voice |
| Children's stories | Warm, gentle, slower pace, higher pitch | "Bella" or custom soft female voice |

## Settings

```
Stability: 50% (balance between consistency and expressiveness)
Similarity enhancement: 75% (keeps voice recognizable across clips)
Style exaggeration: 25% (adds character without overdoing it)
```

Adjust per content type:
- **Brand explainer**: Stability 65%, Similarity 80%, Style 15% (consistency over flair)
- **Story series**: Stability 45%, Similarity 70%, Style 35% (more character range)
- **Children's stories**: Stability 55%, Similarity 75%, Style 20% (warm, consistent)

## Dialogue Generation

Generate each line separately for maximum control:

1. Copy the dialogue line from Claude's script
2. Select the appropriate voice for the character
3. Generate, listen, adjust stability if too flat or too erratic
4. Export as WAV for best quality

For narration:
- Generate in larger chunks (full paragraphs) for natural flow
- Use a different voice from character voices for clear separation

## Tips

- Use ElevenLabs' "Projects" feature for multi-voice episodes — it handles cross-fades between voices automatically
- Generate dialogue BEFORE final animation — this lets you time Runway clips to match speech
- Create custom voices for recurring characters using ElevenLabs' voice cloning (requires a reference audio sample)
- Add a 0.5-second silence between dialogue lines for natural pacing
- For children's stories, lower the speech rate slightly for a calming effect

## Common Pitfalls

- **Voice too monotone** — Fix: increase Style Exaggeration, or break long passages into shorter emotional beats
- **Inconsistent voice between clips** — Fix: increase Stability, or use Projects mode instead of individual generations
- **Emotion doesn't match scene** — Fix: add emotional direction in the prompt: "says angrily", "whispers softly", "narrates with wonder"
- **ElevenLabs adds unwanted pauses** — Fix: use SSML tags to control pacing: `<break time="200ms"/>` between phrases