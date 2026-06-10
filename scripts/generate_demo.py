#!/usr/bin/env python3
"""Generate assets/demo.gif — an animated terminal demo for the README.

Renders a fake Claude Code session (install the skill, then run an audit) with a
typewriter effect. Reproducible: re-run to regenerate after editing the script.

    python scripts/generate_demo.py

Requires Pillow. Uses Consolas (Windows). Adjust FONT_PATH for other OSes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

# ---- layout / theme ---------------------------------------------------------
W, H = 760, 600
MARGIN_X, TOP = 24, 56
LINE_H = 26
FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
FONT_BOLD = r"C:\Windows\Fonts\consolab.ttf"
FS = 16
BRAND = (45, 212, 191)     # Staksoft accent (teal)

BG = (13, 17, 23)          # #0d1117
BAR = (22, 27, 34)         # #161b22
WHITE = (201, 209, 217)    # #c9d1d9
GREEN = (126, 231, 135)    # prompt $
BLUE = (88, 166, 255)      # user prompt
PURPLE = (210, 168, 255)   # skill activation
GRAY = (139, 148, 158)     # comments
RED = (255, 123, 114)      # P0
ORANGE = (255, 166, 87)    # P1
YELLOW = (227, 179, 65)    # P2
SEO_C, GEO_C, AEO_C = (88, 166, 255), (210, 168, 255), (126, 231, 135)

font = ImageFont.truetype(FONT_PATH, FS)
bfont = ImageFont.truetype(FONT_BOLD, FS)

# ---- script: each line is a list of (text, color, bold) spans ---------------
P = ("PAUSE", None, False)   # sentinel: hold a beat
B = []                       # blank line (no spans)

def line(*spans):
    return [(t, c, b) for (t, c, b) in spans]

def s(t, c, bold=False):
    return (t, c, bold)

SCRIPT = [
    line(s("# 1. Add the skill to your project", GRAY)),
    line(s("$ ", GREEN, True), s("git clone https://github.com/staksoft/geo-seo-aeo-skill \\", WHITE)),
    line(s("      .claude/skills/web-optimization", WHITE)),
    line(s("Cloning into 'web-optimization'... done.", GRAY)),
    [P],
    B,
    line(s("# 2. Ask Claude Code to audit a page", GRAY)),
    line(s("> ", BLUE, True), s("audit https://acme.com for SEO, GEO and AEO", WHITE)),
    [P],
    B,
    line(s("  Using skill: ", PURPLE), s("web-optimization", PURPLE, True)),
    line(s("  $ python scripts/audit.py https://acme.com", GRAY)),
    [P],
    B,
    line(s("  SEO ", SEO_C, True), s("72   ", WHITE), s("GEO ", GEO_C, True),
         s("41   ", WHITE), s("AEO ", AEO_C, True), s("38", WHITE),
         s("    overall 50", GRAY)),
    B,
    line(s("  Prioritized fixes", WHITE, True)),
    line(s("   P0 ", RED, True), s("GEO  add /llms.txt", WHITE), s("            template ready", GRAY)),
    line(s("   P1 ", ORANGE, True), s("GEO  fix 11 hedge words", WHITE), s("     -> \"sub-50ms p95\"", GRAY)),
    line(s("   P1 ", ORANGE, True), s("AEO  add FAQPage schema", WHITE), s("     1 question found", GRAY)),
    line(s("   P2 ", YELLOW, True), s("SEO  title 81 chars", WHITE), s("         trim to <= 60", GRAY)),
    [P],
    B,
    line(s("  Report ready. ", GREEN), s("Ship it.", GREEN, True)),
]

# flatten to know typing budget (PAUSE/blank cost a few frames but no chars)
def total_typable():
    n = 0
    for ln in SCRIPT:
        if ln and ln[0][0] == "PAUSE":
            continue
        for (t, _c, _b) in ln:
            n += len(t)
    return n

CPF = 5            # characters revealed per frame
PAUSE_FRAMES = 6   # hold length for a PAUSE sentinel
HOLD_END = 24      # frames to hold the finished screen

def draw_frame(revealed, cursor_on=True):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # title bar + traffic lights
    d.rectangle([0, 0, W, 40], fill=BAR)
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([18 + i * 20, 13, 29 + i * 20, 24], fill=col)
    brand, rest = "Staksoft", "  ·  geo-seo-aeo-skill"
    tw = d.textlength(brand, font=bfont) + d.textlength(rest, font=font)
    bx = (W - tw) // 2
    d.text((bx, 9), brand, font=bfont, fill=BRAND)
    d.text((bx + d.textlength(brand, font=bfont), 9), rest, font=font, fill=GRAY)

    budget = revealed
    y = TOP
    cursor_drawn = False
    for ln in SCRIPT:
        if ln and ln[0][0] == "PAUSE":
            continue
        x = MARGIN_X
        for (t, c, bold) in ln:
            fnt = bfont if bold else font
            if budget >= len(t):
                d.text((x, y), t, font=fnt, fill=c or WHITE)
                x += int(d.textlength(t, font=fnt))
                budget -= len(t)
            else:
                shown = t[:max(0, budget)]
                d.text((x, y), shown, font=fnt, fill=c or WHITE)
                x += int(d.textlength(shown, font=fnt))
                budget = 0
                if cursor_on and not cursor_drawn:
                    d.rectangle([x + 1, y + 3, x + 11, y + FS + 2], fill=WHITE)
                    cursor_drawn = True
                break
        y += LINE_H
        if budget <= 0 and revealed < TYPABLE:
            break
    # trailing cursor once everything is typed
    if cursor_on and revealed >= TYPABLE and not cursor_drawn:
        d.rectangle([x + 6, y - LINE_H + 3, x + 16, y - LINE_H + FS + 2], fill=WHITE)
    return img

TYPABLE = total_typable()

def build_frames():
    frames = []
    revealed = 0
    # walk the script accumulating typed chars, inserting pauses
    consumed = 0
    idx = 0
    # We render progressively: every CPF chars => one frame; PAUSE => hold frames.
    # Simpler: pre-compute char count BEFORE each PAUSE to time the holds.
    char_at_pause = []
    running = 0
    for ln in SCRIPT:
        if ln and ln[0][0] == "PAUSE":
            char_at_pause.append(running)
            continue
        for (t, _c, _b) in ln:
            running += len(t)

    pauses_done = 0
    while revealed < TYPABLE:
        revealed = min(TYPABLE, revealed + CPF)
        frames.append(draw_frame(revealed, cursor_on=True))
        # fire any pause whose threshold we just crossed
        while pauses_done < len(char_at_pause) and revealed >= char_at_pause[pauses_done]:
            for _ in range(PAUSE_FRAMES):
                frames.append(draw_frame(revealed, cursor_on=True))
            pauses_done += 1
    # end hold with blinking cursor
    for k in range(HOLD_END):
        frames.append(draw_frame(TYPABLE, cursor_on=(k // 6) % 2 == 0))
    return frames

def render_social_card(out_path):
    """Static 1280x640 PNG for GitHub Settings -> Social preview."""
    cw, ch = 1280, 640
    img = Image.new("RGB", (cw, ch), BG)
    d = ImageDraw.Draw(img)
    # subtle top accent bar
    d.rectangle([0, 0, cw, 8], fill=BRAND)
    f_brand = ImageFont.truetype(FONT_BOLD, 30)
    f_title = ImageFont.truetype(FONT_BOLD, 70)
    f_sub = ImageFont.truetype(FONT_PATH, 28)
    f_tag = ImageFont.truetype(FONT_BOLD, 34)
    d.text((80, 90), "STAKSOFT", font=f_brand, fill=BRAND)
    d.text((80, 150), "SEO · GEO · AEO", font=f_title, fill=WHITE)
    d.text((80, 232), "Skill for AI Agents", font=f_title, fill=WHITE)
    d.text((80, 340),
           "Audit & generate web content optimized for Google,",
           font=f_sub, fill=GRAY)
    d.text((80, 378),
           "ChatGPT, Perplexity, AI Overviews, and answer engines.",
           font=f_sub, fill=GRAY)
    # three lens chips
    chips = [("SEO", SEO_C), ("GEO", GEO_C), ("AEO", AEO_C)]
    x = 80
    for label, col in chips:
        w = d.textlength(label, font=f_tag) + 48
        d.rounded_rectangle([x, 470, x + w, 530], radius=14, outline=col, width=3)
        d.text((x + 24, 482), label, font=f_tag, fill=col)
        x += w + 24
    d.text((80, 575), "github.com/staksoft/geo-seo-aeo-skill  ·  MIT",
           font=f_sub, fill=GRAY)
    img.save(out_path)
    return out_path


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(here, "assets")
    out = os.path.join(assets, "demo.gif")
    frames = build_frames()
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=40) for f in frames]
    pal[0].save(out, save_all=True, append_images=pal[1:], duration=72,
                loop=0, optimize=True, disposal=2)
    kb = os.path.getsize(out) // 1024
    print(f"wrote {out}  ({len(frames)} frames, {kb} KB)")

    social = render_social_card(os.path.join(assets, "social-preview.png"))
    print(f"wrote {social}  ({os.path.getsize(social) // 1024} KB)")

if __name__ == "__main__":
    main()
