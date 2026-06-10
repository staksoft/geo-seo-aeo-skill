#!/usr/bin/env python3
"""Deterministic SEO/GEO/AEO heuristic checks for a web page.

Stdlib-only (no pip install needed). Fetches a URL or reads a local HTML file,
runs objective/mechanical checks, and prints a JSON report on stdout. The agent
folds this JSON into the qualitative audit (see SKILL.md, Workflow A).

Usage:
    python audit.py https://example.com/page
    python audit.py --file path/to/page.html [--base-url https://example.com]

The JSON is advisory signal, not a verdict. Qualitative scoring stays with the
agent using references/scoring.md.
"""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

HEDGE_WORDS = [
    "might", "could", "may", "maybe", "possibly", "perhaps", "generally",
    "somewhat", "fairly", "quite", "really", "very fast", "blazing fast",
    "scalable", "robust", "seamless", "cutting-edge", "world-class",
    "leading", "best-in-class", "soon", "various", "several",
]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self._in_title = False
        self.meta = {}            # name/property -> content
        self.headings = []        # (level, text)
        self._heading_level = None
        self._heading_buf = []
        self.canonical = None
        self.robots = None
        self.images = 0
        self.images_with_alt = 0
        self.links_internal = 0
        self.links_external = 0
        self.jsonld_blocks = []
        self._in_jsonld = False
        self._jsonld_buf = []
        self.text_parts = []
        self._skip_text = 0       # inside script/style
        self.og_tags = 0
        self.twitter_tags = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key.lower()] = a.get("content", "")
                if key.lower().startswith("og:"):
                    self.og_tags += 1
                if key.lower().startswith("twitter:"):
                    self.twitter_tags += 1
        elif tag == "link" and (a.get("rel", "").lower() == "canonical"):
            self.canonical = a.get("href")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading_level = int(tag[1])
            self._heading_buf = []
        elif tag == "img":
            self.images += 1
            if a.get("alt", "").strip():
                self.images_with_alt += 1
        elif tag == "a" and a.get("href"):
            self._classify_link(a["href"])
        elif tag in ("script", "style"):
            self._skip_text += 1
            if tag == "script" and a.get("type", "").lower() == "application/ld+json":
                self._in_jsonld = True
                self._jsonld_buf = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._heading_level:
            self.headings.append((self._heading_level, " ".join(self._heading_buf).strip()))
            self._heading_level = None
        elif tag in ("script", "style"):
            self._skip_text = max(0, self._skip_text - 1)
            if tag == "script" and self._in_jsonld:
                self.jsonld_blocks.append("".join(self._jsonld_buf).strip())
                self._in_jsonld = False

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data
        if self._heading_level is not None:
            self._heading_buf.append(data)
        if self._in_jsonld:
            self._jsonld_buf.append(data)
        if self._skip_text == 0:
            stripped = data.strip()
            if stripped:
                self.text_parts.append(stripped)

    def _classify_link(self, href):
        if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
            return
        netloc = urlparse(href).netloc
        if netloc:
            self.links_external += 1
        else:
            self.links_internal += 1


def fetch(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (web-optimization-audit)"})
    with urlopen(req, timeout=20) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace"), resp.geturl()


def check_llms_txt(base_url):
    if not base_url:
        return None
    parsed = urlparse(base_url)
    root = f"{parsed.scheme}://{parsed.netloc}/llms.txt"
    try:
        req = Request(root, headers={"User-Agent": "web-optimization-audit"})
        with urlopen(req, timeout=10) as resp:
            return {"url": root, "exists": resp.status == 200}
    except (URLError, HTTPError):
        return {"url": root, "exists": False}


def analyze(html, base_url=None):
    p = PageParser()
    p.feed(html)

    body_text = " ".join(p.text_parts)
    words = re.findall(r"\b\w+\b", body_text.lower())
    word_count = len(words)

    hedges_found = {}
    lower_text = " " + body_text.lower() + " "
    for h in HEDGE_WORDS:
        c = lower_text.count(" " + h + " ") + lower_text.count(" " + h + ".") + lower_text.count(" " + h + ",")
        if c:
            hedges_found[h] = c
    # quantified-claim signal: numbers/units present
    number_mentions = len(re.findall(r"\b\d+(?:[.,]\d+)?\s?(?:%|ms|s|kb|mb|gb|x|k|m|\+|\$)?\b", body_text))

    # heading order sanity
    levels = [lvl for lvl, _ in p.headings]
    h1_count = levels.count(1)
    skipped = False
    prev = 0
    for lvl in levels:
        if prev and lvl > prev + 1:
            skipped = True
        prev = lvl

    valid_jsonld, invalid_jsonld, jsonld_types = [], 0, []
    for block in p.jsonld_blocks:
        try:
            data = json.loads(block)
            valid_jsonld.append(data)
            items = data if isinstance(data, list) else [data]
            for it in items:
                if isinstance(it, dict) and it.get("@type"):
                    t = it["@type"]
                    jsonld_types.extend(t if isinstance(t, list) else [t])
        except json.JSONDecodeError:
            invalid_jsonld += 1

    title = (p.title or "").strip()
    desc = p.meta.get("description", "").strip()

    report = {
        "input": base_url,
        "seo": {
            "title": title or None,
            "title_length": len(title),
            "title_ok": 30 <= len(title) <= 65,
            "meta_description": desc or None,
            "meta_description_length": len(desc),
            "meta_description_ok": 120 <= len(desc) <= 170,
            "canonical": p.canonical,
            "robots_meta": p.meta.get("robots"),
            "h1_count": h1_count,
            "heading_levels_skipped": skipped,
            "images": p.images,
            "images_missing_alt": p.images - p.images_with_alt,
            "internal_links": p.links_internal,
            "external_links": p.links_external,
            "og_tags": p.og_tags,
            "twitter_tags": p.twitter_tags,
        },
        "geo": {
            "word_count": word_count,
            "hedge_words_found": hedges_found,
            "hedge_total": sum(hedges_found.values()),
            "quantified_signal_count": number_mentions,
            "has_tables": "<table" in html.lower(),
            "llms_txt": check_llms_txt(base_url),
        },
        "aeo": {
            "question_headings": [t for lvl, t in p.headings if t.strip().endswith("?")],
            "has_faq_schema": "FAQPage" in jsonld_types,
            "has_howto_schema": "HowTo" in jsonld_types,
        },
        "structured_data": {
            "jsonld_blocks": len(p.jsonld_blocks),
            "jsonld_valid": len(valid_jsonld),
            "jsonld_invalid": invalid_jsonld,
            "jsonld_types": sorted(set(jsonld_types)),
        },
        "headings": [{"level": lvl, "text": t} for lvl, t in p.headings],
    }
    return report


def main():
    ap = argparse.ArgumentParser(description="SEO/GEO/AEO deterministic checks")
    ap.add_argument("url", nargs="?", help="URL to audit")
    ap.add_argument("--file", help="local HTML file to audit instead of a URL")
    ap.add_argument("--base-url", help="base URL (for --file, enables llms.txt check)")
    args = ap.parse_args()

    try:
        if args.file:
            with open(args.file, "r", encoding="utf-8", errors="replace") as f:
                html = f.read()
            base = args.base_url
        elif args.url:
            html, base = fetch(args.url)
        else:
            ap.error("provide a URL or --file")
            return
    except (URLError, HTTPError, OSError) as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

    print(json.dumps(analyze(html, base), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
