---
name: gsc-question-farming
description: "Mine GSC for 7+ word conversational queries and turn them into on-page Q&A that AI answers cite."
version: 1.0.0
author: Jimmy Lien
license: MIT
metadata:
  hermes:
    tags: [seo, gsc, aeo, content]
    related_skills: [content-gap-analysis, aio, citation-hub]
---

# GSC Question Farming

Find the queries in your own Search Console data that look like AI prompts —
long, conversational, question-shaped — then answer one of them exactly on the
page Google already ranks for it. This is how a page starts showing up in
ChatGPT and Google AI answers: you meet the phrasing people actually use, on
the URL Google already trusts for it. For pulling GSC data live, see
`content/content-gap-analysis/gsc-ga4-data-access.md`; for making a whole page
machine-extractable, see the `aio` skill.

## Why It Works

Nobody types 7-word queries into a search box by accident — they type the way
they talk to an assistant. Long queries are the closest thing in GSC data to
how people prompt AI, and Google surfacing your page for one is a live signal
that AI engines can too. Answering that exact phrasing in the first sentences
makes the page extractable: the AI lifts the answer instead of paraphrasing
someone else's.

## The Filter

In Google Search Console → Performance → add a filter → Query → switch to
**Custom (regex)** and paste:

```
^(\S+\s){6,}\S+$
```

This matches every query of 7 or more words. Sort the result by impressions.

## Workflow

1. Open GSC Performance, add the regex filter above.
   *Completion:* the query list shows only 7+ word queries.
2. Sort by impressions and pick **one** question that matches something the
   site actually sells. Ignore the rest — one page, one query, measured
   before moving on.
   *Completion:* the chosen query maps to a real product/service.
3. Click the query, open the **Pages** tab, and note which URL Google shows
   for it. That page — not a new one — gets the edit.
   *Completion:* the target URL is recorded.
4. Edit that page: add the exact query verbatim as a heading, and answer it
   in the first two sentences underneath, with one specific number or fact.
   *Completion:* the heading matches the query word-for-word and the answer
   opens with a concrete figure.

## Pitfalls

1. **Picking a query you don't sell.** Impressions without a product behind
   them is traffic, not revenue — filter for commercial relevance first.
2. **Paraphrasing the query in the heading.** The match is the mechanism;
   close-but-not-exact loses the signal.
3. **Burying the number.** A specific fact in the first two sentences is what
   gets lifted; a fact in paragraph five is invisible to extraction.
4. **Doing ten at once.** You can't attribute the effect. Ship one, give GSC
   2–3 days to populate new data and a few weeks for movement, then repeat.
5. **The regex is a proxy, not proof of AI intent.** Some 7-word queries are
   just verbose shoppers; judge each candidate before committing.

## Verification Checklist

- [ ] Regex filter pasted exactly; query list is 7+ words only
- [ ] Chosen query matches a product the site sells
- [ ] Edit went to the URL Google actually shows for the query (Pages tab)
- [ ] Heading is the query verbatim
- [ ] First two sentences under it contain one specific number or fact
- [ ] Change is live on the rendered page, not just in the CMS
