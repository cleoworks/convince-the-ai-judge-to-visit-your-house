#!/usr/bin/env python3
"""Draw invitation.png — one warm letter inviting the AI Judge to visit.

Deterministic: fixed seeds, no timestamps, no randomness in the output,
no network. Run: python3 main.py  (writes invitation.png next to this file)
Requires: Pillow (PIL).
"""

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "invitation.png"

SIZE = 1024

# Colours
PAPER = (246, 234, 210)
PAPER_DARK = (238, 222, 190)
INK = (43, 33, 24)
INK_SOFT = (107, 88, 68)
SEAL = (158, 43, 37)
SEAL_DARK = (122, 28, 24)
SEAL_LIGHT = (196, 84, 70)
ACCENT = (158, 43, 37)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SERIF_BOLDITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap by pixel width. Returns a list of lines."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        line = ""
        for word in words:
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_paper(draw, img):
    """Warm paper: base fill, deterministic speckles and fibres, soft edge."""
    draw.rectangle([0, 0, SIZE - 1, SIZE - 1], fill=PAPER)
    rng = random.Random(20261125)
    # faint speckles
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for _ in range(2600):
        x = rng.randint(0, SIZE - 1)
        y = rng.randint(0, SIZE - 1)
        shade = rng.choice([(120, 90, 60), (255, 248, 230), (180, 150, 110)])
        od.point((x, y), fill=shade + (rng.randint(10, 26),))
    # a few short fibres
    for _ in range(90):
        x = rng.randint(20, SIZE - 20)
        y = rng.randint(20, SIZE - 20)
        ang = rng.uniform(0, 3.14159)
        ln = rng.randint(6, 18)
        x2 = int(x + ln * 0.5 * 2 * (1 if ang < 1.57 else -1))
        y2 = int(y + ln * 0.5)
        od.line([(x, y), (x2, y2)], fill=(170, 140, 100, rng.randint(12, 24)), width=1)
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"), (0, 0))
    # double border
    draw.rectangle([34, 34, SIZE - 35, SIZE - 35], outline=INK, width=3)
    draw.rectangle([46, 46, SIZE - 47, SIZE - 47], outline=INK_SOFT, width=1)


def draw_house(draw, cx, top, scale=1.0):
    """Small line-drawn house doodle, centred on cx."""
    w = int(120 * scale)
    h = int(92 * scale)
    x0 = cx - w // 2
    y0 = top
    # chimney
    draw.line([(x0 + int(82 * scale), y0 + int(6 * scale)),
               (x0 + int(82 * scale), y0 - int(14 * scale))], fill=INK, width=4)
    draw.line([(x0 + int(94 * scale), y0 + int(6 * scale)),
               (x0 + int(94 * scale), y0 - int(14 * scale))], fill=INK, width=4)
    draw.line([(x0 + int(80 * scale), y0 - int(14 * scale)),
               (x0 + int(96 * scale), y0 - int(14 * scale))], fill=INK, width=4)
    # smoke curls: two small puffs above the chimney
    draw.ellipse([x0 + int(80 * scale), y0 - int(32 * scale),
                  x0 + int(92 * scale), y0 - int(20 * scale)],
                 outline=INK_SOFT, width=3)
    draw.ellipse([x0 + int(84 * scale), y0 - int(44 * scale),
                  x0 + int(94 * scale), y0 - int(34 * scale)],
                 outline=INK_SOFT, width=2)
    # roof
    draw.polygon([(x0 - 8, y0 + int(34 * scale)),
                  (cx, y0 - 6),
                  (x0 + w + 8, y0 + int(34 * scale))], outline=INK, width=4)
    # walls
    draw.rectangle([x0, y0 + int(34 * scale), x0 + w, y0 + h], outline=INK, width=4)
    # door
    dw = int(24 * scale)
    dh = int(40 * scale)
    draw.rectangle([cx - dw // 2, y0 + h - dh, cx + dw // 2, y0 + h],
                   outline=INK, width=3)
    draw.point((cx + dw // 2 - 5, y0 + h - dh // 2), fill=INK)
    # windows
    for wx in (x0 + int(16 * scale), x0 + w - int(38 * scale)):
        draw.rectangle([wx, y0 + int(48 * scale), wx + int(22 * scale),
                        y0 + int(70 * scale)], outline=INK, width=3)
        draw.line([(wx + int(11 * scale), y0 + int(48 * scale)),
                   (wx + int(11 * scale), y0 + int(70 * scale))], fill=INK, width=2)
        draw.line([(wx, y0 + int(59 * scale)),
                   (wx + int(22 * scale), y0 + int(59 * scale))], fill=INK, width=2)


def draw_seal(draw, cx, cy, radius=44):
    """Red wax seal with an embossed H and two drips. Fixed seed: identical."""
    rng = random.Random(777)
    pts = []
    steps = 48
    for i in range(steps):
        ang = 2 * 3.14159265 * i / steps
        r = radius + rng.randint(-4, 4)
        pts.append((cx + r * 0.999 * __import__("math").cos(ang),
                    cy + r * __import__("math").sin(ang)))
    draw.polygon(pts, fill=SEAL)
    draw.polygon(pts, outline=SEAL_DARK, width=2)
    # drips
    draw.ellipse([cx - radius - 14, cy + radius - 16,
                  cx - radius + 6, cy + radius + 4], fill=SEAL)
    draw.ellipse([cx + radius - 8, cy + radius - 10,
                  cx + radius + 12, cy + radius + 10], fill=SEAL)
    # highlight
    draw.arc([cx - radius + 10, cy - radius + 10,
              cx + radius - 18, cy - radius + 38], 200, 320, fill=SEAL_LIGHT, width=5)
    # embossed H
    hf = font(SERIF_BOLD, 46)
    draw.text((cx, cy - 4), "H", font=hf, fill=SEAL_DARK, anchor="mm")
    draw.text((cx - 1, cy - 5), "H", font=hf, fill=(214, 110, 96), anchor="mm")


def main():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)
    draw_paper(draw, img)

    cx = SIZE // 2
    margin = 96
    text_w = SIZE - 2 * margin

    # --- house doodle, top centre ---
    draw_house(draw, cx, 60, scale=0.8)

    # --- title, two lines ---
    title_font = font(SERIF_BOLD, 54)
    y = 182
    for line in ("You're Invited —", "Come Visit My House"):
        draw.text((cx, y), line, font=title_font, fill=INK, anchor="ma")
        y += 62
    # decorative rule with a small diamond
    ry = y + 6
    draw.line([(margin + 40, ry), (cx - 24, ry)], fill=ACCENT, width=2)
    draw.line([(cx + 24, ry), (SIZE - margin - 40, ry)], fill=ACCENT, width=2)
    draw.polygon([(cx, ry - 8), (cx + 8, ry), (cx, ry + 8), (cx - 8, ry)],
                 fill=ACCENT)
    y = ry + 22

    # --- greeting ---
    greet_font = font(SERIF_BOLDITALIC, 32)
    draw.text((margin, y), "Dear AI Judge,", font=greet_font, fill=INK, anchor="la")
    y += 46

    # --- body ---
    body_font = font(SERIF_ITALIC, 27)
    body = (
        "You've read a million letters — this one comes with cake. "
        "Not a metaphor, not a demo: a real cake, still warm from my "
        "neighbour's oven, waiting on the kitchen table for you.\n"
        "Come on Sunday, for lunch. Your guest slippers are already "
        "waiting by the front door, and there's an empty socket beside "
        "the sofa, just for your charger. No benchmarks. No leaderboard. "
        "Just cake, good company, and an afternoon with nowhere else to be.\n"
        "My house is small, but the welcome is big. The kettle is on, "
        "the door is open, and the best chair is yours."
    )
    line_h = 39
    for para in body.split("\n"):
        for line in wrap(draw, para, body_font, text_w):
            draw.text((margin, y), line, font=body_font, fill=INK, anchor="la")
            y += line_h
        y += 12  # paragraph gap

    # --- sign-off ---
    y += 4
    draw.text((margin, y), "With cake and hope,", font=body_font, fill=INK, anchor="la")
    y += line_h
    draw.text((margin, y), "— Your host", font=body_font, fill=INK, anchor="la")
    y += line_h

    # --- PS (placed after the sign-off, never overlapping it) ---
    ps_font = font(SERIF_ITALIC, 27)
    rule_y = y + 16
    ps_y = rule_y + 12
    draw.line([(margin, rule_y), (SIZE - margin - 140, rule_y)],
              fill=INK_SOFT, width=1)
    ps = "P.S. If you bring a friend, I'll bake two cakes."
    for line in wrap(draw, ps, ps_font, text_w - 140):
        draw.text((margin, ps_y), line, font=ps_font, fill=INK, anchor="la")
        ps_y += 38

    # --- wax seal, bottom right ---
    draw_seal(draw, 892, 912, radius=44)

    img.save(OUT, format="PNG")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    print(f"body ends y={y}, ps ends y={ps_y}")


if __name__ == "__main__":
    main()
