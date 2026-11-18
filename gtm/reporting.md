# Reporting — Decide What Survives

Reporting's job is not dashboards; it's deciding. Every metric here maps to a motion in the tree, and each one has a threshold that triggers a change. A metric nobody acts on gets cut — measurement theater is worse than no measurement because it feels like progress.

## The six metrics

**Reply rate** — replies / delivered, per campaign and per segment. The health check for targeting and copy combined. Below ~2-3% on cold outbound means the list or the first line is wrong; fix before scaling (see `outbound.md` decision framework).

**Positive reply rate** — interested+later replies / delivered, per campaign. The metric that 1-test-per-round optimizes. It's the honest one: reply rate alone rewards controversy and confusion.

**Show rate** — meetings held / meetings booked, per source. Diagnoses the booking handoff: low show rate with good reply rates means the follow-up loop (`inbound-and-pipeline.md`) is dropping intent between booking and call. Below ~70%, work the reminder/confirm loop before adding volume.

**Spam and bounce rate** — the deliverability pair, watched weekly. Bounce >2% or a spam-complaint spike → stop sending, re-verify, check infrastructure (`data-and-enrichment.md`). These two metrics protect every other number; a burned domain zeroes out reply rate for weeks.

**Meetings booked per signal** — by signal type (`signals.md`). This is what justifies the signal taxonomy: signals that fire often and book nothing get killed; signals that book rarely but well get promoted. This metric is why the tree collects inputs broadly — each input has to pay rent.

**Pipeline by motion** — pipeline $ and meetings, grouped by source motion (outbound, inbound, events, partnerships, revival, product signups). The allocation metric: it tells you where next quarter's attention goes. Run it by segment too (see `icp-and-tam.md`) — a motion that works in one segment and dies in another is a segment decision, not a motion failure.

## How to run it

- **One weekly slot** (with the deal review, `revops.md`): the six metrics, current vs. trend, and one decision per metric that's off threshold. Ten minutes, tops.
- **Source of truth:** metrics computed from the CRM (the record) and the sending tooling — one definition per metric, written down. Two teams computing "reply rate" differently will eventually have an argument that costs a quarter.
- **Trend over snapshot:** a single week's number is noise; the threshold rules fire on 2-3 consecutive periods. This keeps the system from whipsawing on variance.
- **Attribution honesty:** report by motion and by segment, never by individual. People game individual dashboards in ways that quietly break the data.

## Decision Framework

- **Metric off threshold → change what?** Each metric names its own fix: reply rate → list/copy; show rate → follow-up loop; bounce/spam → infrastructure stop; meetings per signal → kill or promote signals; pipeline by motion → reallocate attention.
- **Metric with no threshold?** It's a chart, not a metric. Give it a trigger or drop it.
- **Motion starving for attention?** Pipeline by motion decides — not the loudest internal advocate.
- **New metric proposed?** It must name its decision and its threshold in the same breath it's introduced.

## Collaboration With the Other Skills

- `revops.md` — the CRM supplies every number here; the weekly slot is shared.
- `outbound.md` — reply, positive-reply, spam and bounce live there day to day; the thresholds here are the tripwires.
- `signals.md` — meetings per signal is the scoreboard that prunes the taxonomy.
- `scoring.md` — measured conversion data reweights the intent model quarterly.
