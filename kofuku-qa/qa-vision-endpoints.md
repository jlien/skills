# QA Vision Endpoints — two paths, and how they drift

`bin/kofuku-qa` runs the Gate-2 vision pass one of two ways:

1. **Deterministic** — when the var is on: it `exec`s `bin/kofuku-vision <slug>`,
   which samples frames and asks a local OpenAI-compatible VL server
   (`lib/kofuku/vision.rb`; model from `KOFUKU_VISION_MODEL`, default
   qwen2.5-vl-7b — host:port lives in `KOFUKU_VISION_URL`, it has drifted).
2. **Heavy-agent eyes** — otherwise: the QA prompt tells the running heavy agent
   to execute `docs/playbooks/qa-vision.md` itself. Always-available fallback
   (and what actually passed tourist-tatchi-kessai on 2026-09-03).

## Env-loading asymmetry (the gotcha)

- `bin/kofuku-qa` is bash: its vision-branch test sees only the **exported shell
  env** — a key that lives only in repo `.env` does NOT turn on path 1.
- `bin/kofuku-vision` / `bin/kofuku-produce` are Ruby and DO `Kofuku::Env.load!`
  (repo `.env`, then `~/.hermes/.env`), and descendants inherit their env. So a
  cron that runs `bin/kofuku-produce` gets the deterministic vision judge even
  when nobody exported the var, while a shell-invoked `bin/kofuku-qa` in the
  same hour doesn't. The two runtimes judge with different eyes.
- FIXED (jlien/kofuku PR #287, merged 2026-09-04): `bin/kofuku-qa` sources a
  `bin/lib/env.sh` helper that loads only these two vars from the repo `.env`
  (exported shell values winning) — path selection no longer depends on who
  exported what; a supported workaround survives on older trees
  (`set -a; source .env; set +a` before invoking).

## Pre-flight before trusting either vision key

After changing an `.env` vision key or anything about the GPU server:

    GET ${KOFUKU_VISION_URL}/models

- `KOFUKU_VISION_MODEL` must name an id the server ACTUALLY SERVES
  (`/v1/models` catches renames/re-points — but the list says NOTHING about
  image input; modality is verified end-to-end only, see below). vLLM boxes get
  re-pointed silently (text LLMs and VL servers share hardware) — the served
  list is ground truth for WHICH model, never for WHAT it can see.
- A text-only id means path 1 ships video frames to a model that cannot see
  them: verdicts fail or hallucinate, and the produce loop burns ~4 min per
  rerender before needs_human.
- Verify the server is actually listening (the endpoint in the env may be
  stale — port/host drifts when the GPU box re-arranges). Curl it with a short
  `--connect-timeout`.
- **NEVER infer modality from the model id or the `/v1/models` list** — the
  list proves nothing about image input. Lesson (2026-09-03→04): the listed id
  `glm-5.3-flash` was *assumed* text-only because of the name, a "broken
  vision config" conclusion and an `.env` edit proposal were built on that
  assumption, and a real frame POST then disproved it: `bin/kofuku-vision
  tourist-tatchi-kessai` end-to-end (repo `.env` → base64 reference + 8 frames
  → glm-5.3-flash) returned PASS score 1.0 with substantive judgments. The
  modality test is END-TO-END: run `bin/kofuku-vision <slug>` on a rendered
  video — a real verdict or a hard API error, never an inference from names.
- Consequently the `.env` keys `KOFUKU_VISION_URL` +
  `KOFUKU_VISION_MODEL=glm-5.3-flash` are CORRECT as configured (verified
  2026-09-04). A proposal to comment them out was withdrawn; do not
  re-propose it without NEW evidence of a failed frame POST.
