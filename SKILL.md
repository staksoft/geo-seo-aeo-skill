---
name: web-optimization
description: >-
  Audit or generate web content optimized for traditional search (SEO),
  AI generative answer engines like ChatGPT/Perplexity/Google AI Overviews
  (GEO), and answer engines / featured snippets / voice (AEO). Use when the
  user asks to improve a page's ranking or AI-citability, run an SEO/GEO/AEO
  audit of a URL or file, add JSON-LD schema, create an llms.txt, or write new
  content that is search- and LLM-friendly.
license: MIT
metadata:
  authors: Staksoft (https://www.staksoft.com)
  source: https://www.staksoft.com/insights/seo/beyond-keywords-the-definitive-guide-to-generative-engine-optimization-geo-in-2026
---

# Web Optimization (SEO · GEO · AEO)

This skill treats **SEO**, **GEO**, and **AEO** as three lenses over one shared
body of web-optimization practice. It supports two workflows: **Audit** an
existing page, and **Generate** new optimized content.

## The three lenses (what each optimizes for)

| Lens | Optimizes for | Load file |
|------|---------------|-----------|
| SEO  | Google/Bing ranking (blue links) | `references/seo.md` |
| GEO  | LLM synthesis (ChatGPT, Perplexity, AI Overviews) | `references/geo.md` |
| AEO  | Answer engines, featured snippets, voice | `references/aeo.md` |

Shared support files:
- `references/schema.md` — JSON-LD patterns (load whenever structured data is involved).
- `references/scoring.md` — the rubric and priority weighting used by both workflows.

> **Progressive disclosure:** Do NOT read every reference up front. Read only the
> lens file(s) relevant to the request, plus `scoring.md` for audits and
> `schema.md` when structured data is in play.

## Workflow A — Audit

Use when given a **URL or a local content file** and asked to evaluate/improve it.

1. **Acquire the content.**
   - URL: prefer `python scripts/audit.py <url>` for deterministic, objective
     checks (returns JSON). Also fetch the rendered content to judge quality.
   - Local file (`.html`/`.md`): read it directly; run `audit.py --file <path>`.
2. **Apply the three lenses.** Read `references/seo.md`, `geo.md`, `aeo.md` and
   evaluate the content against each. Fold in the JSON facts from `audit.py`.
3. **Score & prioritize** using `references/scoring.md` (P0 blocking → P3 nice-to-have).
4. **Emit the report** using `assets/audit-report-template.md`: every finding =
   *issue · lens · impact · concrete fix*. Lead with the prioritized action list.

## Workflow B — Generate

Use when given a **topic/brief + target keyword or user intent** and asked to
produce new content.

1. **Clarify intent** — target query, audience, and primary lens emphasis if any
   (default: optimize for all three).
2. **Draft** applying all three lenses: answer-first structure (AEO), keyword/
   intent coverage and clean heading hierarchy (SEO), high information density
   with concrete measurable claims (GEO).
3. **Attach structured data** — pick the right JSON-LD from
   `assets/schema-templates/` per `references/schema.md` (Article + FAQPage are
   the common pair).
4. **Produce an llms.txt entry** from `assets/llms-txt-template.md`.
5. **Output** the content + JSON-LD + llms.txt entry + a short "why this is
   optimized" rationale mapping choices back to the three lenses.

## Quick rules of thumb

- **Information density beats word count.** Replace hedges ("might be fast") with
  measurable claims ("sub-50ms p95 latency"). LLMs cite specifics.
- **Answer the question in the first sentence**, then elaborate — this serves
  snippets, voice, and LLM extraction simultaneously.
- **Structure for two readers**: a human operator and a natural-language parser.
  Tables, lists, and JSON-LD help the parser without hurting the human.
- **Authority is distributed.** Off-domain mentions (GitHub, Reddit, citations)
  matter for GEO trust, not just on-page factors.
