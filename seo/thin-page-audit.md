# Thin-Page Audit (why pages get crawled but not indexed)

Sub-skill of `seo`. When a site has a sitemap and pages *still* aren't indexed,
the bottleneck is almost never discovery — it's **selection**. Google crawls the
page, judges it too thin/duplicative to be worth an index slot, and files it under
**"Crawled – currently not indexed"** or **"Discovered – currently not indexed"**
in Search Console. This sub-skill finds those pages before Google drops them and
says exactly how to fix them.

Run it when: a large templated section (catalog, video pages, product pages) has
lots of URLs but low indexed-count, or GSC shows a big "not indexed" bucket.

## Ground truth first: GSC → Pages (Index coverage)

The **Pages report in Search Console is authoritative** — it tells you how many
URLs are indexed and the reason for each excluded one. Always ask for it. The
telltale reasons for thinness:
- **"Crawled – currently not indexed"** — Google saw it, declined it. Classic thin/
  low-value signal.
- **"Discovered – currently not indexed"** — crawl-budget/quality throttling; often
  thin or near-duplicate templated pages.
- **"Duplicate without user-selected canonical" / "Alternate page…"** — near-dup
  templating, not thinness per se (different fix: consolidate/canonicalize).

If you can't get GSC, run the crawl audit below to *predict* which pages are at risk.

## The audit (measure real crawlable content)

Sample live pages by type and measure the **main content** — not the whole HTML
(nav/footer/boilerplate inflate the count and are duplicated across every page, so
they don't help indexing).

1. Pull URLs from the sitemap, grouped by template (e.g. `/videos/*`, `/blog/*`).
2. Sample each group (evenly across the list, ~25–40 for the big one).
3. For each page, extract the **`<main>`** region, strip `<script>/<style>/tags`,
   collapse whitespace, and count words. Also flag the presence of the section's
   unique-text feature (a transcript block, a spec table, a real description).
4. Report per group: min / median / max words, count under thresholds, transcript/
   unique-text coverage, and the thinnest offenders by slug.

A dependency-free sampler (Ruby, stdlib only):
```ruby
require "open-uri"
def words(html)
  main = html[%r{<main[^>]*>(.*?)</main>}m, 1] || html
  main = main.gsub(%r{<script.*?</script>}m," ").gsub(%r{<style.*?</style>}m," ")
  main.gsub(/<[^>]+>/," ").gsub(/&[a-z#0-9]+;/," ").split(/\s+/).size
end
urls  = File.read("sitemap.xml").scan(%r{<loc>([^<]+)</loc>}).flatten
group = urls.select { |u| u.include?("/videos/") }
sample = group.each_slice([group.size/30,1].max).map(&:first)
rows = sample.map { |u| [u, words(URI.open(u,&:read))] rescue nil }.compact
ws = rows.map(&:last).sort
puts "min #{ws.first} / median #{ws[ws.size/2]} / max #{ws.last}; under 250: #{ws.count { |w| w<250 }}/#{ws.size}"
```

## Interpreting the numbers (rough thresholds)

Word count is a proxy, not a ranking factor — but it correlates strongly with
"does Google bother indexing this."
- **< ~150 main-content words** → high risk; frequently not indexed.
- **~150–300** → borderline; indexed inconsistently, especially on low-authority
  or newer sites. This is the danger zone most templated pages live in.
- **300+ of genuinely unique text** → usually indexed if not duplicative.
- Judge **uniqueness**, not just length: 300 words that are 80% shared boilerplate
  across pages is still thin. The question is "how much text here exists *nowhere
  else on the site*."

Blog/article templates usually clear this easily (1000+ words). **Media/catalog
templates are the usual failures** — a video embed, a poster image, or a product
shot with a sentence of copy. That's where the indexed-count leaks.

## Remediation (in priority order)

1. **Add unique text to the thin template — the highest-leverage fix.** Turn each
   thin page into a real one:
   - Media pages → a full **transcript/breakdown** (crawlable text of what's in the
     video), plus a short "how/when to use this" paragraph and a 2–4 item **FAQ**
     (which also earns `FAQPage` rich results). A reel page jumps from ~200 to
     ~450+ unique words.
   - Product/catalog pages → real specs, use-cases, and differentiators, not a
     templated blurb.
   Even ~150–200 words of genuinely unique prose per page moves most out of the
   danger zone.
2. **Fix missing/partial unique content.** If the "unique" feature is often empty
   (e.g. transcripts present on only some pages, or 1–2 lines), backfill it — the
   thinnest offenders are usually the ones where it's missing.
3. **Consolidate near-duplicates.** If many pages are minor variants, merge them or
   canonicalize to one; don't make Google choose between 50 almost-identical URLs.
4. **Strengthen internal links** to the thin pages (hub/index pages, "related",
   breadcrumbs) so crawl depth is shallow and they don't look orphaned/low-value.
5. **Re-check GSC after shipping.** Coverage lags weeks; watch the "not indexed"
   bucket shrink rather than declaring victory on a re-crawl.

Prioritize by **count × traffic potential**: a 200-page template stuck at a ~240-word
median is a far bigger prize than 18 thin pages in a minor section.

## Key Principles

- **Not indexed is usually a *selection* problem, not a discovery one** — more
  pings won't help; better pages will.
- **Measure main content, not the whole HTML** — boilerplate is duplicated and
  doesn't count toward uniqueness.
- **GSC's Pages report is ground truth**; the crawl audit is the predictor when you
  can't see GSC.
- **Fix the template, not the page** — thin templated sections fail together and get
  fixed together.
- **Uniqueness over length** — 300 shared-boilerplate words is still thin.
