# RevOps — Run the Operating System Under the Motions

Everything else in the `gtm` tree assumes this section works. RevOps is plumbing: when it breaks, every motion breaks, and nobody blames the plumbing — they blame the motions.

## 1 CRM as the record

One CRM holds the truth. Not the spreadsheet, not the sequencer, not the data tool — the CRM.

- Every account, contact, activity, deal and signal lands there, either natively or via a sync that runs at least hourly.
- If a tool disagrees with the CRM, the CRM wins. Fix the sync, not the record.
- Field hygiene rules: no free-text where a picklist works, no picklist where a boolean works. Every required field has an owner (a person or a job, not "the team").
- Audit monthly: pick 20 random accounts, check that fields a rep would need to work the deal are filled and current. Below 80% correct, fix the inputs — never patch records by hand.

## Signal routing to owners

A signal without an owner is noise. The routing rule has three parts:

1. **Who.** Every account has one named owner. Territory rules decide; when territory is ambiguous, round-robin with an exception list, not a debate.
2. **When.** Routing is automatic and inside a time budget — hot signals inside 5 minutes, warm inside a business day. Speed-to-lead is the one metric where minutes matter.
3. **What happens if nobody moves.** If the owner doesn't touch the signal inside the SLA, it escalates to their manager. Silent reassignment teaches people to ignore signals.

## Scheduled enrichment

Enrichment runs on a schedule, not on demand at the moment someone needs a field.

- Nightly for accounts in active pipeline and tier 1 of the account list; weekly for everything else.
- Job-to-be-done: keep firmographics, headcount, tech stack and funding current. Stale data poisons scoring (see `scoring.md`) more than missing data does.
- Track enrichment coverage as a metric: % of accounts with a last-enriched date inside the freshness window. Coverage under 90% on tier 1 is a fire.

## Weekly deal reviews

One hour, same slot, every week. Pipeline only, no training, no pipeline-that-isn't (deals without a next step and a date).

- Walk tier-1 deals only. Ask three questions per deal: what changed since last week, what is the next step and its date, what would kill this deal.
- Deals that go three reviews without a new next step get marked stalled. Stalled deals either get a revival play (see `inbound-and-pipeline.md` for closed-lost) or leave the forecast.
- Output is written down in the deal record, not in the meeting notes nobody opens.

## Loss reasons

Every closed-lost deal gets a loss reason from a short picklist — 6-10 options max, no "other" dumping ground.

- Reasons must be diagnosable, not descriptive: "lost to incumbent" (fine), "price" (useless — why was the price wrong?).
- Review quarterly: if one reason exceeds 40% of losses, that is a product or motion problem, and it goes to the founder, not to more prospecting.
- Loss reasons feed ICP refinement (see `icp-and-tam.md`) — the deals you lose repeatedly define who you should stop selling to.

## Decision Framework

- **A tool wants to own data?** It syncs into the CRM and defers to it, or it doesn't get adopted.
- **A signal has no owner?** It doesn't get sent until it does.
- **Data looks wrong?** Fix the input and the sync. Never hand-patch a record to hide a broken process.
- **Something failed silently?** That's a RevOps bug. Add the alert, don't just fix the instance.

## Collaboration With the Other Skills

- `scoring.md` — RevOps maintains the fields; scoring consumes them. Garbage fields, garbage tiers.
- `reporting.md` — every metric there depends on this section's data being current.
- `signals.md` — routing rules live here; the signals themselves are defined there.
