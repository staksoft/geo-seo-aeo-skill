# Web Optimization Audit — {{page title or URL}}

**Audited:** {{URL or file path}}
**Date:** {{YYYY-MM-DD}}

## Scores

| Lens | Score | One-line verdict |
|------|-------|------------------|
| Overall | {{0–100}} | {{verdict}} |
| SEO  | {{0–100}} | {{verdict}} |
| GEO  | {{0–100}} | {{verdict}} |
| AEO  | {{0–100}} | {{verdict}} |

## Prioritized actions

| # | Priority | Lens | Action | Effort |
|---|----------|------|--------|--------|
| 1 | P0 | {{SEO/GEO/AEO}} | {{the single concrete fix}} | {{S/M/L}} |
| 2 | P1 | … | … | … |
| 3 | P2 | … | … | … |

> Cheapest high-impact fixes first.

## Detailed findings

### SEO
- **{{Issue}}** — *Impact:* {{why it costs ranking}}. *Fix:* {{exact change}}.

### GEO
- **{{Issue}}** — *Impact:* {{why it suppresses AI citation}}. *Fix:* {{change}}.
  - Hedge found: "{{quoted sentence}}" → Rewrite: "{{quantified version}}".

### AEO
- **{{Question on page}}** — *Impact:* {{not snippet-eligible}}. *Fix:*
  {{answer-first rewrite + schema to add}}.

## What's already good
- {{Reinforce the strengths so they aren't regressed.}}

## Raw deterministic checks (from audit.py)
```json
{{paste the JSON output here}}
```
