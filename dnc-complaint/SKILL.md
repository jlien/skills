---
trigger: DNC, Do Not Call, FTC complaint, spam calls, telemarketing complaints, donotcall.gov, robocalls, spam screenshot, unwanted calls
---

# DNC Complaint Filing

File FTC National Do Not Call registry complaints for spam numbers extracted from call-log or voicemail screenshots the user uploads. Drives the public complaint wizard at `donotcall.gov/report.html` with a browser tool. No login, no CAPTCHA (verified 2026-11-03).

## How the Wizard Actually Works

The form looks like a classic ASP.NET postback but is a JS-driven app (`js/report.js`): steps toggle client-side, and each step POSTs JSON to endpoints on `www2.donotcall.gov` (`/complaint-step2`, `/save-complaint`). Three steps:

1. Receiving phone number, call date/time, robocall?, call vs text, subject category
2. Caller number/name, business relationship, optional comment — **the Submit button files immediately, no confirmation screen**
3. Success page with the literal text "Your Complaint Has Been Accepted"

### Field Map (verified against the live form)

Navigate to `https://www.donotcall.gov/report.html`, click `#MainContinueButton`.

**Step 1:**
- `#PhoneTextBox` — the number that RECEIVED the call (the user's own phone, 10 digits). An invalid area code (e.g. 555) fails with "Correct Your Area Code on Line 1" and silently stays on step 1.
- `#DateOfCallTextBox` — MM/DD/YYYY.
- `#TimeOfCallDropDownList` — hour as zero-padded 24h value string ('14' = 2 PM); `#ddlMinutes` — zero-padded ('05', not '5').
- `#PrerecordMessageYESRadioButton` / `#PrerecordMessageNORadioButton` — robocall?
- `#PhoneCallRadioButton` / `#MobileTextMessageRadioButton` — call vs text.
- `#ddlSubjectMatter` — option value ints: 3 debt-reduction, 4 spoofed caller, 5 medical, 6 home security, 7 tech support, 8 debt collection, 9 energy/solar, 10 home improvement, 11 work-from-home, 12 warranties, 13 lottery/prizes, 14 vacation/timeshare, 15 surveys/political, 16 charities, 2 dropped call/no message, 0 unknown, 1 other (+ `#txtSubjectMatter` free text when 1).
- Click `#StepOneContinueButton`.

**Step 2:**
- `#CallerPhoneNumberTextBox` — the spam number. `#chkConsumerPhone` = caller is the same as the receiving number.
- `#CallerNameTextBox` — company name if the screenshot shows one.
- `#HaveBusinessYesRadioButton`/`No`, `#StopCallingYesRadioButton`/`No`.
- Contact info block is voluntary — leave blank.
- `#CommentTextBox` — optional, ≤1000 chars.
- **`#StepTwoSubmitButton` files the complaint immediately** — no preview, no undo. Read back every field value in the same JS call right before clicking.

**Step 3** — verify the literal text "Your Complaint Has Been Accepted" per number. Capture it as proof.

## Screening Rule (title-line rule)

Judge each call/voicemail cell by its **title line** (the bold first line of the cell):

- Title line is a **phone number** → spam. File a complaint — even if a person's name appears only in the transcript (a rep identifying themselves is not a contact).
- Title line is a **name** → contact. **Never file**, even if the transcript sounds like sales/spam. Only the title line counts.
- When unsure (e.g. a business name that might be a saved contact), list the entry and ask before filing.
- Dedupe: one complaint per unique number, using the most recent call's date/time; mention the repeat count in the comment.

## Procedure

1. **Extract.** For exact digits, delegate a vision pass over the screenshot asking for every cell: title line, date, time, transcript, robocall or not. Cross-check against any inline image description the channel gateway provides.
2. **Screen** with the title-line rule. Build a table: spam number | date | time | robocall | subject | skip-reason.
3. **Ask once** for the user's receiving phone number if not known; never guess it (an invalid area code fails silently).
4. **File** each entry per the Field Map. Set values via JS with the native value setter + `input`/`change` events (plain `.value=` assignment doesn't stick).
5. **Verify** "Your Complaint Has Been Accepted" before the next number. One tab, sequential loop, ≥60s between submissions (see Rate Limit).
6. **Report** in chat: filed count, per-number confirmation, skipped contacts with the skip reason.

## Rate Limit (hard blocker)

- `www2.donotcall.gov` returns **HTTP 429 "Too many requests"** after roughly 20 complaints in an hour from one IP.
- The failure is SILENT: the wizard's AJAX `.done()` never fires, the page stays on step 1, and `#ContentPlaceHolder1_ErrorMsgLabel` keeps showing the error from the PREVIOUS attempt — do not trust on-screen errors. Probe directly from a page on the domain:
  `fetch('https://www2.donotcall.gov/complaint-step2', {method:'POST', headers:{'Content-Type':'application/json;charset=utf-8'}, body:JSON.stringify({PhoneNumber:'<receiving_number>', DateOfCall:'11/03/2026'})})`
  A 429 means back off; a `0`/`1`/`2` body means clear.
- On 429: stop filing, save remaining numbers to a JSON file (caller/date/hour/min/comment), retry after a few hours, and pace submissions ≥60s apart once resumed.

## Pitfalls

- The error label shows stale text after a failed AJAX call. `#step1`/`#step2` are NOT element ids (they're only URL hashes) — detect the current step by field presence (`#CallerPhoneNumberTextBox`), and verify success by the literal "Your Complaint Has Been Accepted" text.
- `#StepTwoSubmitButton` submits instantly — a misclick files a complaint that cannot be retracted.
- Setting values without the native setter + dispatched events leaves the form state stale; the wizard stays on step 1 with no visible error. Use the right prototype per tag: `HTMLSelectElement` for selects, `HTMLTextAreaElement` for `#CommentTextBox` (the input-setter throws 'Illegal invocation' on textareas), `HTMLInputElement` for the rest.
- The date field is a jQuery datepicker; set it through `jQuery('#DateOfCallTextBox').datepicker('setDate', ...)` or the native setter — the validator runs `$.datepicker.parseDate('mm/dd/yy', ...)` on the value.
- If the spam number is unknown/blocked, the form still needs a valid receiving number; leave `CallerPhoneNumberTextBox` empty and pick subject 0 (Unknown).
- The complaint form is on www.donotcall.gov — don't confuse it with telemarketing.donotcall.gov (the sellers' portal).

## Verification

- Each filed number shows "Your Complaint Has Been Accepted" in the page text.
- The final report states exactly N filed / N skipped / N failed, matching the extracted table count.
