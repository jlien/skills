---
name: framing
description: "Midjourney character sheets, environment prompts, and brand explainer visuals"
---

# Midjourney: Frame Generation

Convert scene descriptions into production-ready frames.

## Character Sheet (Series)

Generate a reference sheet first, then use `--cref` for every subsequent frame.

```
character design sheet, [CHARACTER DESCRIPTION], full body front view, three-quarter view, side view, expression sheet, white background, clean lines, [STYLE: e.g. 2D animated, cel-shaded, watercolor, minimalist], --ar 3:2 --style raw --s 250
```

Example:
```
character design sheet, young female detective, short curly red hair, oversized trench coat, green eyes, confident expression, full body front view, three-quarter view, side view, expression sheet, white background, clean lines, 2D animated style, --ar 3:2 --style raw --s 250
```

## Environment — Night City

```
[SCENE DESCRIPTION], nighttime, cinematic lighting, [MOOD], volumetric fog, neon accents, --ar 16:9 --style raw --s 250
```

Example:
```
rain-slicked city street, nighttime, cinematic lighting, noir atmosphere, volumetric fog, neon accents, shallow depth of field, --ar 16:9 --style raw --s 250
```

## Brand Explainer — Corporate

```
[SCENE: e.g. modern office interior with product visualization], bright, clean, professional, soft shadows, [BRAND COLOR] accents, minimal, --ar 16:9 --style raw --s 150
```

## Character Reference (Consistency)

After generating your character sheet, reference it in every prompt:

```
[SCENE with character], --cref [CHARACTER_SHEET_URL] --cw 100 --ar 16:9 --style raw --s 250
```

- `--cw 100` = maximum character reference strength (appearance, clothes, face)
- `--cw 0` = appearance only, allow different clothes
- Use `--cw 100` for series where character identity matters

## Children's Story — Soft Style

```
[SCENE: e.g. cozy bedroom at bedtime], soft pastel colors, gentle lighting, storybook illustration style, warm, comforting, --ar 16:9 --style raw --s 200
```

## Motion Comic Panels

```
[SCENE DESCRIPTION], comic book panel, dramatic lighting, cinematic composition, [STYLE: manga, western comic, noir], --ar 16:9 --style raw --s 300
```

## Aspect Ratios

| Format | Flag |
|--------|------|
| YouTube (16:9) | `--ar 16:9` |
| Shorts/Reels/TikTok (9:16) | `--ar 9:16` |
| Character sheet (3:2) | `--ar 3:2` |

## Common Pitfalls

- **Character drift** — Always use `--cref` after the reference sheet. Without it, Midjourney will generate similar but inconsistent characters.
- **Too much detail** — Midjourney chokes on overly complex scenes. Strip prompts to essentials: subject, setting, lighting, mood.
- **Text in frames** — Midjourney is unreliable with text. Do not include text in frames — add titles and labels in post-production.
- **Inconsistent style** — Use the same `--style` and `--s` (stylize) value across all frames in a project.
- **Hands and faces** — Midjourney v6 handles these better, but still check every frame. Regenerate with `--vary subtle` if needed.

## Batch Workflow

1. Generate character sheets first (1 prompt per character)
2. Generate environment frames without characters
3. Generate final frames combining characters + environments using `--cref`
4. Vary lighting/time of day for the same scene to get multiple shots
5. Export all frames at max resolution before sending to Runway