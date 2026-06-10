# AEO Lens — Answer Engine Optimization

Optimize to be **the answer** — featured snippets, "People Also Ask", voice
assistants, and direct-answer boxes. AEO overlaps GEO but targets short,
extractable, single-best-answer formats rather than synthesized prose.

## 1. Answer-first writing
- Lead each section with a **direct 40–55 word answer**, then elaborate. This is
  the snippet sweet spot.
- Definitional sentences in "X is a …" form for "what is" queries.
- Numbered steps for "how to" queries; each step a short imperative.
- Tables for comparison/"vs"/spec queries.

## 2. Question targeting
- Mine real questions (PAA, autocomplete, "who/what/when/where/why/how").
- Use the literal question as an `<h2>`/`<h3>`, immediately followed by the
  concise answer.
- Build a dedicated **FAQ section** for the page's cluster of related questions.
- Cover the long-tail follow-ups a voice assistant would chain.

## 3. Snippet-eligible formatting
- Short paragraphs (2–4 sentences); generous use of lists and tables.
- Bold the key term/answer where natural.
- Keep the answer self-contained (no "as mentioned above").
- Logical heading order so engines can map structure to the question hierarchy.

## 4. Structured data for answers
- **FAQPage** schema for Q&A blocks (see `references/schema.md`).
- **HowTo** schema for step-by-step content.
- **Speakable** schema (where relevant) to mark voice-friendly passages.
- Ensure visible on-page content matches the schema (no schema-only answers).

## 5. Voice & conversational fit
- Natural-language phrasing; write the way people speak the query.
- Concise enough to be read aloud in one breath (~30 words for voice answers).
- Local intent: include place / "near me" context and LocalBusiness schema when applicable.

## Audit output for this lens
For each target question on the page: is there a direct, self-contained,
snippet-length answer? Is it backed by FAQ/HowTo schema? Flag questions answered
only in long prose, and supply the tightened answer-first rewrite.
