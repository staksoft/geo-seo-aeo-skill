# SEO Lens — Traditional Search Ranking

Optimize for Google/Bing crawling, indexing, and ranking. Evaluate each item;
in audits, flag misses with a priority (see `scoring.md`).

## 1. Crawlability & indexing
- `robots.txt` present and not blocking key paths.
- XML sitemap exists, referenced in robots.txt, and lists canonical URLs.
- One canonical URL per page via `<link rel="canonical">`; no duplicate-content forks.
- No accidental `noindex`/`nofollow` on pages that should rank.
- Clean, descriptive, lowercase URLs (words not IDs; hyphens not underscores).

## 2. On-page metadata
- `<title>`: unique, 50–60 chars, primary keyword near the front.
- `<meta name="description">`: 140–160 chars, compelling, includes the query intent.
- Exactly one `<h1>`, matching the page's primary topic.
- Open Graph + Twitter Card tags for social/SERP previews.

## 3. Content & intent
- Page matches **search intent** (informational / commercial / transactional /
  navigational) for its target query.
- Primary keyword + semantic variants/synonyms used naturally (no stuffing).
- Heading hierarchy is logical and sequential (h1 → h2 → h3, no skipped levels).
- Sufficient depth vs. competitors for the query; covers the obvious sub-questions.

## 4. Links
- Descriptive internal links to related pages (spread link equity, aid crawl).
- Anchor text is meaningful (not "click here").
- Outbound links to authoritative sources where it helps the reader.
- No broken links (4xx/5xx) or redirect chains.

## 5. Media & accessibility
- All meaningful images have descriptive `alt` text.
- Images compressed and served in modern formats (WebP/AVIF); explicit width/height.
- Lazy-load below-the-fold media.

## 6. Technical performance (Core Web Vitals)
- **LCP** < 2.5s, **INP** < 200ms, **CLS** < 0.1 (field data where available).
- HTTPS everywhere; HTTP→HTTPS redirects.
- Mobile-responsive; passes mobile usability.
- Reasonable page weight; render-blocking resources minimized.

## 7. Structured data
- Relevant schema.org JSON-LD present and valid (see `references/schema.md`).
- Breadcrumb schema for hierarchical pages.

## Audit output for this lens
For each miss: state the issue, why it costs ranking, and the concrete fix
(exact tag, target value, or file). Group by the section above.
