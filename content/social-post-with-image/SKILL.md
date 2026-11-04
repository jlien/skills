---
name: social-post-with-image
description: "Thought-leadership social posts (X/LinkedIn) with a matching generated image: fact-check, punchy draft, ComfyUI/Flux image pipeline, verify loop, and standalone HTML preview packaging."
version: 1.0.0
author: Jimmy Lien
license: MIT
metadata:
  hermes:
    tags: [social-media, linkedin, image-generation, comfyui, flux, content]
    related_skills: [ai-animation-factory, llm-artifact-sweep]
---

# Social Post with Image

Turns a raw idea into a punchy, fact-checked post plus a matching square image, and optionally packages it as a standalone HTML preview that looks like a LinkedIn feed card.

## Workflow

### 1. Load the voice

Check the user's saved voice notes and target platform first. If none exist, ask ONCE for a sample account or 2-3 past posts to match, save the voice, then proceed.

### 2. Fact-check first

Before drafting, flag any claim that is wrong, unverifiable, or likely to draw skepticism (for example, big output numbers without context). Suggest the fix in one line. Verify with a web search when you can, and take the user's word on numbers you can't access. Hedged claims ("when RAM prices normalize") read better than confident ones if the search shows ongoing volatility.

### 3. Draft punchy

- Hook in line 1: a short, bold, or counterintuitive claim.
- One idea per line, lots of white space, short sentences.
- Use concrete specifics (numbers, model names, examples) over abstractions.
- Emoji bullets only for a short list of 2 to 4 parallel items.
- End with an aphorism-style closer or one question, not both.
- LinkedIn: slightly more polished than X; no hashtag spam. X: trim to fit, or split into a short thread.

### 4. Make the image (every post gets one)

Generate 1:1 (1024x1024) on a ComfyUI Flux box running `flux1-dev-kontext_fp8_scaled` with `clip_l` + `t5xxl_fp8_e4m3fn_scaled` clips and `ae.safetensors` VAE.

**Setup**: the base URL comes from `IMAGE_GEN_URL`. Check the box is up before any spend: `curl -s -m 8 "$IMAGE_GEN_URL/system_stats"`.

**Text-to-image — the blank-canvas trick**: Kontext always edits a source image. For pure text-to-image, pass `--canvas 1024x1024` to `scripts/flux-batch-edit.py` instead of a source file — it generates a solid dark canvas, uploads it, and proceeds as usual. Describe the full design in the positive text.

**Batch runner** (preferred): `scripts/flux-batch-edit.py <src> graph1.json [graph2.json ...]` — one call does upload → N parallel graph submits → poll → download (stdlib only; fits a 600s foreground window for 2 seeds). Exits 2 if anything is still pending; resume via `GET /history/<id>`, never resubmit. Pass `--canvas WxH` instead of `<src>` for text-to-image.

**Graph template**: `templates/comfyui-kontext-edit.json` — copy it, swap `SRC_UPLOAD_NAME.png`, the positive text, seed, and `filename_prefix`.

**Prompt rules** (each cost a failed render to learn):

- The graph runs at cfg=1.0, so **negative prompts are INERT** — Flux never samples the negative branch. Anything steering the generation goes in the POSITIVE text ("Avoid: …" lists included).
- `ReferenceLatent.conditioning` is a bare link `["pos", 0]` — a nested `[["pos", 0]]` fails validation.
- `VAEEncode`'s vae input key is `vae` (typo `v` → required-input-missing).
- Re-submit freely after fixing validation errors — every job is idempotent until it validates.
- Chaining passes: each pass is a NEW job — upload the previous pass's output and put THAT returned name in LoadImage. A file downloaded to local disk is invisible to LoadImage.
- Output size follows the SOURCE image aspect after `FluxKontextImageScale`.
- Design guidance: one clear visual metaphor for the core idea, dark modern style, at most one headline and a few short labels.

**Iterating** (verified patterns):

- One correction per pass. State the one property that moves and lock the rest.
- Chain from the newest image that has the RIGHT STYLE; chained references anchor the prior edit hard.
- After ~2 failed strikes on the same property, re-chain from the ORIGINAL with one holistic replace instruction and bump guidance to 3.2.
- Two parallel seeds is the cheap way to get a pick-the-better take.
- Do not repeat a prompt recipe more than twice; the second identical failure is a diagnosis signal.

**Punctuation and small glyphs are sampler-stubborn.** Three passes (delta edit at guidance 2.5, delta edit again, holistic replace at 3.2, two seeds) can all fail to turn a comma into a period — and one edit added garbled prefix text while "fixing" it. After 2 strikes on the same glyph, switch to deterministic pixel surgery instead of re-rolling:

1. Get the exact glyph bbox from a vision/OCR verify pass. A period is a dot ON the baseline; a comma descends below it — pixel-level baseline comparison beats OCR confidence.
2. Erase with a per-COLUMN vertical background lerp (sample clean background above and below the glyph). A horizontal lerp can sample a neighboring glyph and leave a bright streak.
3. Stamp a copy of a known-good glyph from elsewhere in the same image (font-matched), scaled and placed on the baseline.
4. Re-verify with a luminance check of the edit zone.

**Vision-verify every pass before delivering.** Verify against the exact property that was wrong before, not a generic check. OCR + glyph-baseline analysis is a reliable fallback when no vision tool is available.

### 5. Deliver

Send the post text and attach the image. Keep commentary to a line or two.

### 6. Iterate

For edits ("punchier", "redo the photo"), change only what was asked and keep the rest.

### 7. Package as HTML preview (optional)

Edit `build.py` (next to this file): fill in `NAME`, `TITLE`, `OUT`, and one `POSTS` entry per post: `"<slug>.html": ("<Title>", "<image path>", "<post text>")`. Run `python3 build.py` (Pillow required). It base64-embeds a 640px JPEG (quality 70) of each image into one self-contained HTML page styled like a LinkedIn feed card, with a Copy-text button — no network calls, works from `file://`. Keep each file under ~100 KB; if it's over, shrink the image further. Uses the exact final post text — don't rewrite it here.
