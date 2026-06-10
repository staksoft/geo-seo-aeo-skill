# Scoring & Prioritization Rubric

Used by the Audit workflow to turn findings into a ranked action list, and by
Generate as a pre-ship checklist.

## Priority levels

| Priority | Meaning | Examples |
|----------|---------|----------|
| **P0 — Blocking** | Prevents indexing/citation; fix first | `noindex` on a key page, blocked in robots.txt, no HTTPS, content JS-only & unrendered, no `<title>` |
| **P1 — High** | Major visibility/trust loss | missing canonical, no structured data, hedge-heavy low-density copy, no answer-first structure, failing Core Web Vitals |
| **P2 — Medium** | Meaningful but not critical | thin meta description, weak internal linking, missing FAQ schema, no llms.txt, missing alt text |
| **P3 — Low** | Polish / incremental | OG tags, breadcrumb schema, image format upgrades, minor heading tweaks |

## Per-lens scoring (0–100)

Score each lens, then report all three plus an overall. Suggested weighting of
the sub-areas:

**SEO** = crawlability/indexing (25) + metadata (15) + content/intent (25) +
links (15) + performance/CWV (15) + structured data (5).

**GEO** = information density (35) + citability/passage structure (25) +
distributed authority (20) + llms.txt (10) + machine-readability (10).

**AEO** = answer-first writing (30) + question targeting (25) + snippet
formatting (20) + answer schema (FAQ/HowTo) (20) + voice/local fit (5).

Deduct by severity of each miss (P0 ≈ −20+, P1 ≈ −10, P2 ≈ −5, P3 ≈ −2),
floored at 0. These are judgment aids, not exact math — keep scores defensible
and tie every deduction to a specific finding.

## Report ordering
1. **Overall + three lens scores** (one line each).
2. **Prioritized action list** — P0 → P3, most impactful first.
3. **Detailed findings by lens** (issue · lens · impact · concrete fix).

Always make the *cheapest high-impact* fixes obvious at the top.
