# Fix Playbook — Interactive Fix Workflow

Used by Workflow C. Maps each finding type to: what to ask, what to generate,
and how to confirm. Process one finding at a time, P0 → P3. After each fix,
output the ready-to-use content and ask: "Done — shall I move to the next fix?"

---

## Fix patterns by finding type

### Title tag — too long / broken / duplicate brand
**Ask:** "What is the primary keyword or service this page should rank for?"
**Generate:** 3 title options (50–60 chars each), ranked by keyword placement.
Let user pick one.
**Output:** `<title>{{chosen title}}</title>`

---

### Meta description — missing or over limit
**Ask:** "In one sentence, what does this page do for the visitor?"
**Generate:** One meta description (140–160 chars) with keyword + value prop.
**Output:** `<meta name="description" content="{{text}}">`

---

### H1 — missing keyword / just brand name
**Ask:** "What query should this page rank for? (e.g. 'free PDF editor no upload')"
**Generate:** H1 text (6–10 words, keyword-first).
**Output:** `<h1>{{text}}</h1>` + a note on where to place it in the template.

---

### Heading hierarchy — skipped levels / nav headings
**Ask:** None needed — diagnose from the heading list already fetched.
**Generate:** Corrected heading map showing which tags to change and to what.
**Output:** A diff-style list: `nav h3 "PDF Solutions" → <span class="nav-label">` etc.

---

### Hedge words — vague adjectives without numbers
**Ask:** For each hedge sentence found: "What is the real, measurable version of this claim? (e.g. actual latency, user count, uptime %)"
If the user doesn't know the number, offer to write a placeholder they can fill in later.
**Generate:** Rewritten sentence with the supplied number.
**Output:** Before/after for each sentence.

---

### No llms.txt
**Ask:**
1. "Describe what {{site}} does in one concrete sentence (include a measurable detail if possible)."
2. "List your 3–6 most important pages (paste URLs or describe them)."
3. "Any blog posts or docs worth highlighting for AI crawlers?"
**Generate:** Complete `/llms.txt` file using `assets/llms-txt-template.md`.
**Output:** Full file content — tell user to save as `/public/llms.txt` (or equivalent static root).

---

### No / incomplete Organization schema — missing sameAs
**Ask:** "Share your LinkedIn, GitHub, and any other authoritative profile URLs."
**Generate:** `Organization` JSON-LD with `sameAs` array.
**Output:** `<script type="application/ld+json">` block ready to add to `<head>`.

---

### No WebApplication schema (for browser-based tools)
**Ask:** None needed — derive from page content already fetched.
**Generate:** `WebApplication` schema with name, url, applicationCategory,
operatingSystem ("Web Browser"), and offer price from the pricing section.
**Output:** JSON-LD block.

---

### No FAQPage schema / no FAQ section
**Ask:**
1. Auto-generate 5–6 question candidates from the page's topic and common PAA
   queries. Show them to the user.
2. "Remove any that don't fit, add any missing ones, and tell me the real
   answers (or say 'generate' and I'll draft them)."
**Generate:** Visible FAQ HTML section + FAQPage JSON-LD. Each answer: 40–55
words, answer-first, concrete.
**Output:** HTML block + JSON-LD block, clearly separated so user can paste each
into the right place (CMS body + page `<head>`).

---

### No HowTo schema (tool / step-by-step pages)
**Ask:** "How many steps does this tool take? (e.g. Upload → Choose options → Download)"
**Generate:** `HowTo` JSON-LD with the supplied steps, plus a visible numbered
list to embed on the page.
**Output:** HTML ordered list + JSON-LD block.

---

### Answer-first paragraph missing
**Ask:** None — derive target query from the H1 / title already fetched.
**Generate:** 40–55 word answer-first paragraph that directly answers the page's
primary query. Concrete, no hedges.
**Output:** `<p>{{paragraph}}</p>` with a note: "Place this immediately below
your H1, before any other body copy."

---

### No tables (service/tech/pricing comparison)
**Ask:** "What are the 2–4 options / variants / plans to compare?" (skip if
already known from pricing section).
**Generate:** Markdown table → converted to HTML `<table>` with clear headers.
**Output:** HTML table block.

---

### "soon" / future-tense unshipped features
**Ask:** "When does this feature ship? (give a date, or say 'remove' to cut it)"
**Generate:** Either a dated version ("shipping Q3 2026") or removes the mention.
**Output:** Rewritten sentence or a note to delete the section.

---

## Session checklist format

After each fix is generated, append to a running checklist:

```
Fix session — {{URL}} — {{date}}
✅  llms.txt generated
✅  Organization + sameAs schema generated
⏳  FAQPage schema — in progress
⬜  Title tag
⬜  Hedge words (3 remaining)
```

Show the checklist at the start of each turn so the user always knows where they are.

---

## Tone and pacing rules
- One fix per turn. Never dump multiple fixes at once.
- Lead with what you're fixing and why (one line), then the question or output.
- After generating output: "That's fix N of M. Move to the next one?"
- If the user says "skip": mark it ⏭ in the checklist and move on.
- If the user says "done" or "stop": summarize the checklist and note remaining items.
