# Structured Data (JSON-LD) Reference

JSON-LD is shared infrastructure for all three lenses: it helps Google render
rich results (SEO), gives LLMs clean machine-readable facts (GEO), and powers
answer boxes / FAQ snippets (AEO). Always emit JSON-LD in a
`<script type="application/ld+json">` block. Ready-to-fill snippets live in
`assets/schema-templates/`.

## Choosing the right type

| Content type | Primary schema | Lens benefit |
|--------------|----------------|--------------|
| Blog post / guide / news | `Article` / `BlogPosting` | SEO rich result, GEO authorship signal |
| Q&A block | `FAQPage` | AEO snippet eligibility |
| Step-by-step | `HowTo` | AEO / voice |
| Product page | `Product` + `Offer` + `AggregateRating` | SEO rich result |
| Company/brand | `Organization` (with `sameAs`) | GEO entity disambiguation |
| Person / author | `Person` | E-E-A-T, authorship |
| Site hierarchy | `BreadcrumbList` | SEO navigation |
| Reviews | `Review` / `AggregateRating` | SEO stars |
| Local business | `LocalBusiness` | local SEO + voice |

Often combine: `Article` + `FAQPage`, or `Organization` + `WebSite`.

## Rules
- **Match visible content.** Schema must reflect what's on the page — mismatches
  risk manual penalties and are useless to LLMs.
- Use absolute URLs, ISO 8601 dates, and real values (no placeholders shipped).
- `Organization.sameAs` should list authoritative profiles (LinkedIn, GitHub,
  Wikipedia, Crunchbase) — this is a key GEO distributed-authority signal.
- One graph per page is fine; use `@graph` to bundle multiple entities.
- Validate every block (see Verification in SKILL workflow / scoring.md).

## Minimal Organization + sameAs example
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Staksoft",
  "url": "https://www.staksoft.com",
  "logo": "https://www.staksoft.com/logo.png",
  "sameAs": [
    "https://www.linkedin.com/company/staksoft",
    "https://github.com/staksoft"
  ]
}
```

See `assets/schema-templates/` for Article, FAQPage, HowTo, and Product files.
