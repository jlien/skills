# Kōfuku Pipeline QA Evals

Structured, versioned mirror of the **operational QA evals** for the Kōfuku
Japanese-learning video pipeline (`~/Eng/japanese`). The canonical operational
skill lives in `~/.hermes/skills/` (`kofuku` umbrella + `kofuku-video-qa-review`
familia); this repo carries the eval patterns that should survive tooling moves.

## Sub-skills

- **`slack-post-eval.md`** — a render is not done until the video is IN Slack:
  capture exit status + permalink from `bin/kofuku-slack-video`, retry once,
  surface `SLACK POST FAILED` loudly in the run summary (PR #285 in
  jlien/japanese). Treating a silent upload failure as success is how a
  QA-passed video ends up never reviewed.
- **`qa-vision-endpoints.md`** — Gate-2 QA vision runs two ways (deterministic
  `bin/kofuku-vision` via `KOFUKU_VISION_URL`, or heavy-agent eyes), the
  bash-vs-Ruby `.env` loading asymmetry that decides which judge runs, and the
  golden rule learned 2026-09-04: **NEVER infer a model's modality from its
  id or the `/v1/models` list** — glm-5.3-flash was assumed text-only from its
  name, and a real frame POST proved it image-capable. Verify end-to-end.

## Formatting conventions

Same shape as the rest of this repo: entry point + self-contained sub-skill
files. Cross-references use bare filenames. When the hermes-side source files
change, re-mirror here (both sides stay in sync on the human's say-so).
