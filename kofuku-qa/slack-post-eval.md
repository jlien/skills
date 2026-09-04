# Slack-Post Eval — verify rendered videos actually reach Slack

Render is not done until the video is IN Slack for review. A silent
`files_upload_v2` failure (channel_left, rate_limit, token drift) otherwise ends
with a QA-passed video nobody ever sees.

## The contract (produce.md step 1 / bin/kofuku-produce)

`bin/kofuku-produce`'s `slack_post_eval`:

1. Calls `bin/kofuku-slack-video <slug> [caption]` capturing stdout+stderr+status
   (NOT `system(..., out: File::NULL)` — that hid every failure).
2. Success requires BOTH: uploader exit 0 **and** a `permalink:` line parsed from
   its stdout. Exit 0 without a parseable permalink → counted as posted but noted
   `permalink unparsed`.
3. Retries ONCE (3s backoff) on failure — Slack errors are usually transient.
4. On persisted failure the run summary carries the state + error:

```
▶️ Rendered this run: 1
  • <slug> (id 729) → qa_passed (SLACK POST FAILED) — exit 1 — video NOT posted to Slack
```

State strings matter downstream: `kofuku-gate`/`kofuku-status` reading a summary
must treat `SLACK POST FAILED` as "rendered, unreviewable" — the video exists on
disk but was never delivered.

## When posting ad-hoc (agent, not runner)

Always prefer the runner. By hand:

```bash
out=$(bin/kofuku-slack-video <slug> 2>&1); st=$?
echo "$out" | grep -q "permalink:" && [ $st -eq 0 ] && echo "posted: $(echo "$out" | grep -o 'https://[^ ]*')"
```

No grep hit or non-zero exit → repost once, then investigate the token
(`$KOFUKU_SLACK_TOKEN` / `$SLACK_BOT_TOKEN`, channel `C0B9EPEV03Y`).

## Recovery

If the summary shows `SLACK POST FAILED`: the render itself is fine. Re-post with
`bin/kofuku-slack-video <slug> --thread <review thread_ts>` (if delivering into a
known review thread) after fixing the underlying cause — don't re-render.
