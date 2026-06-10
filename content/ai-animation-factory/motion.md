---
name: motion
description: "Runway animation: action cuts, environmental atmosphere, brand transitions"
---

# Runway: Animation

Bring static frames to life.

## Action Cut (Story Series)

For dynamic scenes with character movement:

```
Motion prompt: [Character action: e.g. running through street, turning to face camera]
Motion strength: Strong
Duration: 4-8 seconds
Camera: [movement: pan, zoom, follow, static]
```

Example:
```
Motion prompt: woman detective runs through rain-slicked street, turns sharply to face camera, trench coat flapping
Motion strength: Strong
Duration: 5 seconds
Camera: follow behind, then pan to front
```

## Environmental Atmosphere

For mood-setting shots without characters:

```
Motion prompt: [Environmental movement: rain falling, clouds shifting, lights flickering]
Motion strength: Subtle
Duration: 6-10 seconds
Camera: slow pan or static
```

Example:
```
Motion prompt: rain falling on street, neon signs flickering, distant car lights passing through fog
Motion strength: Subtle
Duration: 8 seconds
Camera: slow pan left
```

## Brand Explainer Transition

For clean, professional motion:

```
Motion prompt: [Element movement: graphic slides in, icon scales up, text fades]
Motion strength: Subtle
Duration: 3-4 seconds
Camera: static
```

Example:
```
Motion prompt: product icon scales up from center, data visualization graphics fade in from left
Motion strength: Subtle
Duration: 4 seconds
Camera: static
```

## Children's Story — Gentle Motion

```
Motion prompt: [Gentle movement: tree swaying, stars twinkling, character slowly waving]
Motion strength: Subtle (use the lowest setting)
Duration: 6-10 seconds
Camera: very slow zoom or static
```

## Motion Strength Guide

| Setting | Use Case |
|---------|----------|
| **Subtle** | Brand explainers, children's stories, environmental shots, text-heavy scenes |
| **Medium** | Default for most scenes, dialogue shots, standard action |
| **Strong** | Action sequences, chase scenes, dramatic reveals, high-energy moments |

## Tips

- Keep motion prompts specific and directional ("wind blows left to right" not "wind blows")
- Shorter clips (4-6 seconds) are more reliable than long ones (10+ seconds)
- For character motion, describe the character's action, not the camera — Runway handles both but conflates them if the prompt is ambiguous
- Generate 2-3 variations per scene and pick the best one
- Runway excels at environmental motion (rain, smoke, water, fire) — lean into it
- For dialogue scenes, keep motion minimal — the audience focuses on the face, not the background

## Common Pitfalls

- **Morphing artifacts** — Runway struggles with complex character motion. Fix: break into shorter clips and cross-dissolve in post.
- **Motion too fast** — "Strong" on everything looks chaotic. Fix: reserve Strong for action beats, use Subtle/Medium for 80% of scenes.
- **Inconsistent lighting between clips** — Fix: generate source frames with matching lighting before animating.
- **Runway ignores the prompt** — Fix: simplify the motion prompt to one sentence describing the primary motion.