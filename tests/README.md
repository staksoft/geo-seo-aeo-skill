# Golden test pages

Regression fixtures for `scripts/audit.py`. Run from the skill root.

## weak-page.html — should FAIL most checks
```
python scripts/audit.py --file tests/weak-page.html
```
Expected signals:
- `seo.title_ok: false` (5 chars), `meta_description_ok: false` (missing)
- `seo.canonical: null`, `heading_levels_skipped: true`, `images_missing_alt: 1`
- `geo.hedge_total: 11`, `geo.quantified_signal_count: 0`
- `aeo.has_faq_schema: false` with one unanswered question heading
- `structured_data.jsonld_valid: 0`

## strong-page.html — should PASS most checks
```
python scripts/audit.py --file tests/strong-page.html
```
Expected signals:
- `seo.title_ok: true`, `meta_description_ok: true`, `canonical` present
- `images_missing_alt: 0`
- `geo.hedge_total: 0`, `geo.quantified_signal_count: ~13`, `has_tables: true`
- `aeo.has_faq_schema: true`, two question headings
- `structured_data.jsonld_valid: 1` (`FAQPage`)

If a code change shifts these numbers, confirm it is intended before shipping.
