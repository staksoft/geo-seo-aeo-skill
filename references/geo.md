# GEO Lens — Generative Engine Optimization

Optimize for how LLMs and RAG systems (ChatGPT, Perplexity, Google AI Overviews,
Claude) ingest, trust, and **cite** content. The shift: from keyword-matching to
*information synthesis* — engines decompose a query into sub-queries and evaluate
passages via vector embeddings. Design for two audiences: human operators **and**
natural-language parsers.

Based on the three frameworks from the Staksoft GEO 2026 guide.

## 1. llms.txt standard
- A `/llms.txt` file exists at the domain root (markdown, like robots.txt for AI).
- It maps the site's key directories/pages with one-line descriptions and links.
- Curated, current, and points to the highest-value canonical content.
- Optionally an expanded `/llms-full.txt` with fuller content.
- See `assets/llms-txt-template.md` to create or audit one.

## 2. Information density (the highest-leverage GEO factor)
LLMs preferentially cite **specific, verifiable, quantified** statements.
- **Flag and replace hedges**: "might", "could", "may", "possibly", "generally",
  "fast", "scalable", "robust", "soon" used without numbers.
- **Reward concrete claims**: replace "very fast" → "sub-50ms p95 latency";
  "widely used" → "12,000+ GitHub stars"; "cheap" → "$0.002 per request".
- One clear claim per sentence; front-load the fact.
- Define entities explicitly (full names, versions, dates) — don't rely on context.
- Use **tables** for comparisons/specs and **JSON-LD** for facts: both are
  high-signal, easily parsed structures.

## 3. Citability & passage structure
- Self-contained passages: each section should make sense if extracted alone
  (RAG chunks lose surrounding context).
- Answer-first paragraphs; a clear topic sentence per chunk.
- Stable, descriptive headings that match likely sub-queries.
- Include data, examples, and named sources LLMs can attribute.
- Freshness signals: visible "last updated" date, current stats.

## 4. Distributed authority
AI systems verify claims **across domains** before trusting them.
- Brand/product mentioned and consistent across third-party sites.
- Presence where models are trained/grounded: GitHub, Reddit, Wikipedia, Q&A
  sites, reputable publications, documentation.
- Open-source citations / references that corroborate on-page claims.
- Consistent entity naming and `sameAs` links (see `schema.md`) to disambiguate
  the brand as a knowledge-graph entity.

## 5. Machine-readability hygiene
- Content available in HTML without requiring JS execution (many crawlers don't
  render JS); critical facts not locked behind client-side rendering.
- Not blocking AI crawlers in robots.txt unless intentional (GPTBot,
  ClaudeBot, PerplexityBot, Google-Extended) — decide deliberately.
- Clean semantic HTML; avoid burying text in images.

## Audit output for this lens
For each miss: issue, why it suppresses AI citation/visibility, concrete fix.
Quote specific hedge sentences found and supply the quantified rewrite.
