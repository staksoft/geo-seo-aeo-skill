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
W, H = 860, 664
MARGIN_X, TOP = 28, 60
LINE_H = 29
FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
FONT_BOLD = r"C:\Windows\Fonts\consolab.ttf"
FS = 18

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

CPF = 4            # characters revealed per frame
PAUSE_FRAMES = 7   # hold length for a PAUSE sentinel
HOLD_END = 30      # frames to hold the finished screen

def draw_frame(revealed, cursor_on=True):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # title bar + traffic lights
    d.rectangle([0, 0, W, 40], fill=BAR)
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([20 + i * 22, 14, 32 + i * 22, 26], fill=col)
    d.text((W // 2 - 150, 11), "Claude Code  —  geo-seo-aeo-skill", font=font, fill=GRAY)

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

def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(here, "assets", "demo.gif")
    frames = build_frames()
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=48) for f in frames]
    pal[0].save(out, save_all=True, append_images=pal[1:], duration=70,
                loop=0, optimize=True, disposal=2)
    kb = os.path.getsize(out) // 1024
    print(f"wrote {out}  ({len(frames)} frames, {kb} KB)")

if __name__ == "__main__":
    main()
