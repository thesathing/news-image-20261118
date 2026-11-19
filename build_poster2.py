#!/usr/bin/env python3
"""Build entry.png v2 — 'Wednesday 18 November 2026' front page, revision.

Own design, own code, own flat drawings. V2 answers the top 10: a navy
masthead with a calendar block, a colour-coded region bar (counts sum to
45), a day-in-numbers strip, four leads that are genuinely 18 November
news, ten illustrated cards, a larger world map with numbered pins, a
two-column also-list at 12px, and an explicit DATE CHECK box naming the
17 November stories that are NOT on this page (Kerch Bridge collapse,
Nvidia's results, the Knesset speaker vote, Mongolia's president quitting).
45 stories in all, every one a real event reported on 18 November 2026,
with contested claims attributed. The world outline is Natural Earth 110m
land data (public domain) in map_data.py. Drawn with Pillow, no network.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image, ImageDraw, ImageFont
from map_data import LAND_POLYS

W, H = 1024, 1024
BG = (250, 246, 236)
INK = (24, 24, 24)
NAVY = (22, 32, 63)
RED = (178, 34, 34)
BLUE = (30, 80, 140)
TEAL = (0, 120, 110)
PURPLE = (90, 60, 140)
ORANGE = (214, 110, 20)
GREEN = (34, 130, 70)
GOLD = (217, 164, 65)
GOLDD = (170, 120, 25)
SKY = (190, 215, 235)
SEA = (150, 190, 215)
SAND = (238, 222, 180)
LAND = (232, 214, 170)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, max_w, fill=INK, leading=None, max_lines=None,
         what="text"):
    lh = leading or int(font.size * 1.18)
    lines = wrap(d, text, font, max_w)
    if max_lines is not None and len(lines) > max_lines:
        raise ValueError(f"OVERFLOW in {what}: {lines!r} "
                         f"({len(lines)} lines, max {max_lines})")
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def one_line(d, text, font, max_w, what="text"):
    orig = text
    while text and d.textlength(text, font=font) > max_w:
        text = text.rsplit(" ", 1)[0]
    if text != orig:
        raise ValueError(f"TRUNCATED in {what}: {orig!r} -> {text!r}")
    return text


def kicker(d, x, y, num, text, color=RED):
    fb = f(SANS_B, 11)
    d.ellipse([x, y + 1, x + 12, y + 13], fill=color)
    d.text((x + 4 if num < 10 else x + 1.5, y + 2), str(num),
           font=f(SANS_B, 8), fill=(255, 255, 255))
    d.text((x + 16, y + 1.5), text.upper(), font=fb, fill=color)
    return y + 14


def draw_map(d, x0, y0, w, h, pins, dots):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(205, 225, 240),
                outline=(150, 150, 140), width=1)

    def px(lon, lat):
        return (x0 + (lon + 180) / 360.0 * w,
                y0 + (83 - lat) / 139.0 * h)

    for poly in LAND_POLYS:
        d.polygon([px(lo, la) for lo, la in poly], fill=LAND,
                  outline=(180, 165, 135))
    for lo, la in dots:
        x, y = px(lo, la)
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(70, 70, 70))
    for pin in pins:
        # (n, lon, lat, colour) or (n, lon, lat, colour, off_lon, off_lat)
        n, lo, la, col = pin[0], pin[1], pin[2], pin[3]
        tx, ty = px(lo, la)
        if len(pin) > 4:
            x, y = px(pin[4], pin[5])
            d.line([tx, ty, x, y], fill=(60, 60, 60), width=1)
        else:
            x, y = tx, ty
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=col,
                  outline=(255, 255, 255), width=1)
        d.text((x - 3 if n < 10 else x - 5, y - 5), str(n),
               font=f(SANS_B, 8), fill=(255, 255, 255))


def flag(d, x, y, w, h, kind):
    d.rectangle([x, y, x + w, y + h], outline=(90, 90, 90), width=1)
    if kind == "cn":
        d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        for sx, sy, r in [(7, 6, 3), (16, 3, 2), (19, 8, 2), (16, 14, 2),
                          (10, 15, 2)]:
            d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                      fill=(255, 222, 0))
    elif kind == "ru":
        d.rectangle([x, y, x + w, y + h // 3], fill=(255, 255, 255))
        d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 60, 180))
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(220, 30, 30))
    elif kind == "us":
        for i in range(7):
            d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                        fill=RED if i % 2 == 0 else (255, 255, 255))
        d.rectangle([x, y, x + w * 0.42, y + h * 0.55], fill=BLUE)
        for sx in range(3):
            for sy in range(2):
                d.ellipse([x + 3 + sx * 6, y + 3 + sy * 6,
                           x + 5 + sx * 6, y + 5 + sy * 6],
                          fill=(255, 255, 255))


# ---------------- lead panels (240 x 106, caption strip at bottom) --------
def panel_shenzhen(d, x, y, w, h):
    """Shenzhen: Xi greets Trump; three flags over the summit table."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 240))
    d.rectangle([x, y, x + w, y + 20], fill=PURPLE)
    d.text((x + 8, y + 4), "APEC  •  SHENZHEN",
           font=f(SANS_B, 10), fill=(255, 255, 255))
    for bx, bw, bh in [(8, 18, 24), (30, 14, 36), (48, 22, 30),
                       (74, 15, 42), (93, 20, 28), (117, 15, 38),
                       (136, 22, 32), (162, 14, 44), (180, 20, 28),
                       (204, 15, 36), (222, 16, 24)]:
        d.rectangle([x + bx, y + 80 - bh, x + bx + bw, y + 80],
                    fill=(170, 165, 190))
    fw, fh, gap = 48, 26, 8
    total = 3 * fw + 2 * gap
    sx = x + (w - total) // 2
    for i, (kind, name) in enumerate([("cn", "CHINA"), ("ru", "RUSSIA"),
                                      ("us", "USA")]):
        fx = sx + i * (fw + gap)
        flag(d, fx, y + 26, fw, fh, kind)
        d.text((fx + fw // 2 - len(name) * 2.5, y + 54), name,
               font=f(SANS_B, 8), fill=INK)
    # plane landing on the tarmac strip
    d.rectangle([x + 10, y + 80, x + w - 10, y + 86], fill=(120, 85, 40))
    d.polygon([(x + w - 78, y + 72), (x + w - 38, y + 72), (x + w - 26, y + 75),
               (x + w - 26, y + 79), (x + w - 38, y + 82), (x + w - 78, y + 82)],
              fill=(245, 245, 245), outline=(120, 120, 120))
    d.polygon([(x + w - 62, y + 72), (x + w - 54, y + 65), (x + w - 48, y + 72)],
              fill=(245, 245, 245), outline=(120, 120, 120))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=PURPLE)
    d.text((x + 8, y + h - 17), "SHENZHEN",
           font=f(SANS_B, 9), fill=(255, 255, 255))
    d.text((x + w - 132, y + h - 17), "TRILATERAL • THU 19 NOV",
           font=f(SANS_B, 9), fill=(255, 255, 255))


def panel_gulf(d, x, y, w, h):
    """The Gulf: Qeshm, Kuwait and Bahrain, drones intercepted."""
    d.rectangle([x, y, x + w, y + h], fill=SAND)
    d.polygon([(x + 56, y + 36), (x + 104, y + 28), (x + w, y + 44),
               (x + w, y + h), (x + 34, y + h), (x + 24, y + 66)],
              fill=SEA)
    d.text((x + w - 40, y + 4), "IRAN", font=f(SANS_B, 9), fill=(60, 60, 60))
    d.text((x + 8, y + 4), "KUWAIT", font=f(SANS_B, 9), fill=(60, 60, 60))
    d.text((x + 76, y + 32), "BAHRAIN", font=f(SANS_B, 8), fill=(60, 60, 60))
    d.ellipse([x + w - 76, y + 20, x + w - 34, y + 36], fill=(200, 180, 140),
              outline=(120, 100, 70))
    d.polygon([(x + w - 58, y + 8), (x + w - 53, y + 18),
               (x + w - 48, y + 8), (x + w - 53, y + 14)], fill=(255, 140, 0))
    d.text((x + w - 70, y + 26), "QESHM", font=f(SANS_B, 7), fill=(60, 60, 60))
    d.rectangle([x + 6, y + 54, x + 38, y + 76], fill=(200, 190, 170))
    d.pieslice([x + 8, y + 36, x + 36, y + 64], 180, 360,
               fill=(245, 245, 240), outline=(150, 150, 150))
    pts = [(x + 44, y + 58), (x + 96, y + 44), (x + 152, y + 38),
           (x + 200, y + 48)]
    for i in range(len(pts) - 1):
        ax, ay = pts[i]
        bx, by = pts[i + 1]
        for s in range(0, 10, 2):
            t0, t1 = s / 10.0, (s + 1) / 10.0
            d.line([ax + (bx - ax) * t0, ay + (by - ay) * t0,
                    ax + (bx - ax) * t1, ay + (by - ay) * t1],
                   fill=RED, width=2)
    d.polygon([(x + 40, y + 54), (x + 50, y + 58), (x + 40, y + 62)],
              fill=(40, 40, 45))
    d.polygon([(x + 196, y + 44), (x + 206, y + 48), (x + 196, y + 52)],
              fill=(40, 40, 45))
    for cx, cy in [(x + 96, y + 48), (x + 136, y + 54)]:
        d.line([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED, width=3)
        d.line([cx - 5, cy + 5, cx + 5, cy - 5], fill=RED, width=3)
    d.rectangle([x + w - 74, y + h - 46, x + w - 14, y + h - 34],
                fill=(120, 40, 40))
    d.rectangle([x + w - 66, y + h - 54, x + w - 50, y + h - 46],
                fill=(120, 40, 40))
    d.polygon([(x + w - 42, y + h - 68), (x + w - 36, y + h - 56),
               (x + w - 30, y + h - 68), (x + w - 36, y + h - 62)],
              fill=(255, 140, 0))
    d.rectangle([x + 74, y + 60, x + 172, y + 74], fill=GREEN)
    d.text((x + 79, y + 62), "DRONES INTERCEPTED", font=f(SANS_B, 9),
           fill=(255, 255, 255))
    d.rectangle([x + 94, y + 76, x + 196, y + 88], fill=RED)
    d.text((x + 99, y + 78), "QESHM: US STRIKE", font=f(SANS_B, 9),
           fill=(255, 255, 255))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=INK)
    d.text((x + 8, y + h - 17), "STRAIT OF HORMUZ  •  THE GULF",
           font=f(SANS_B, 9), fill=(255, 255, 255))


def panel_eu45(d, x, y, w, h):
    """EU loan: big €45bn with a 20/25 split bar and a ring of stars."""
    d.rectangle([x, y, x + w, y + h], fill=(0, 40, 100))
    # ring of twelve EU stars, top right
    cx, cy, r = x + w - 26, y + 22, 14
    for i in range(12):
        ang = 2 * math.pi * i / 12.0 - math.pi / 2
        sx, sy = cx + r * math.cos(ang), cy + r * math.sin(ang)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)
    d.text((x + 10, y + 8), "€45bn", font=f(SERIF_B, 40), fill=(255, 255, 255))
    d.text((x + 10, y + 52), "EU LOAN FOR UKRAINE — 2027",
           font=f(SANS_B, 12), fill=GOLD)
    # split bar: €20bn budget aid / €25bn military
    bx, by, bw, bh = x + 10, y + 68, w - 20, 14
    d.rectangle([bx, by, bx + bw * 20 // 45, by + bh], fill=BLUE)
    d.rectangle([bx + bw * 20 // 45, by, bx + bw, by + bh], fill=GOLD)
    d.text((bx + 4, by + 2), "€20bn BUDGET", font=f(SANS_B, 8),
           fill=(255, 255, 255))
    d.text((bx + bw * 20 // 45 + 4, by + 2), "€25bn MILITARY",
           font=f(SANS_B, 8), fill=(20, 20, 20))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=INK)
    d.text((x + 8, y + h - 17), "BRUSSELS • REPAID FROM REPARATIONS",
           font=f(SANS_B, 9), fill=(255, 255, 255))


def panel_voyager(d, x, y, w, h):
    """Voyager 1: Earth, the Sun, and a distance scale to 25.9bn km."""
    d.rectangle([x, y, x + w, y + h], fill=(8, 10, 26))
    for sx, sy, r in [(14, 12, 1.5), (60, 8, 1), (110, 16, 1.5),
                      (170, 10, 1), (210, 20, 1.5), (40, 30, 1),
                      (150, 28, 1), (196, 34, 1), (90, 6, 1)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill=(255, 255, 255))
    # the Sun, far left
    d.ellipse([x + 8, y + 40, x + 26, y + 58], fill=(255, 200, 40))
    d.ellipse([x + 12, y + 44, x + 22, y + 54], fill=(255, 230, 120))
    # Earth
    d.ellipse([x + 40, y + 40, x + 60, y + 60], fill=(40, 110, 200))
    d.ellipse([x + 44, y + 44, x + 52, y + 50], fill=(60, 170, 90))
    d.ellipse([x + 50, y + 52, x + 56, y + 57], fill=(60, 170, 90))
    d.text((x + 38, y + 62), "EARTH", font=f(SANS_B, 8), fill=(255, 255, 255))
    # the distance line, Earth to Voyager
    d.line([x + 62, y + 50, x + w - 34, y + 50], fill=(255, 255, 255), width=2)
    for tx in [x + 100, x + 140, x + 180]:
        d.line([tx, y + 46, tx, y + 54], fill=(255, 255, 255), width=1)
    # Voyager: dish + boom, at the far end
    vx, vy = x + w - 30, y + 50
    d.line([vx - 14, vy, vx + 6, vy], fill=(180, 180, 190), width=2)
    d.polygon([(vx, vy - 8), (vx + 12, vy - 2), (vx, vy + 4)], fill=(220, 220, 230))
    d.line([vx, vy, vx - 8, vy + 10], fill=(180, 180, 190), width=2)
    d.text((vx - 26, y + 62), "VOYAGER 1", font=f(SANS_B, 8),
           fill=(255, 255, 255))
    d.text((x + 10, y + 8), "25.9bn km  •  ONE LIGHT-DAY OUT",
           font=f(SANS_B, 11), fill=GOLD)
    d.text((x + 10, y + 24), "FIRST HUMAN-MADE OBJECT TO REACH IT",
           font=f(SANS_B, 9), fill=(255, 255, 255))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=INK)
    d.text((x + 8, y + h - 17), "10:16 GMT  •  25,900,000,000 KM",
           font=f(SANS_B, 9), fill=(255, 255, 255))


# ---------------- card illustrations (190 x 60, caption strip) -------
def caption(d, x, y, w, text, fill):
    d.rectangle([x, y, x + w, y + 14], fill=fill)
    d.text((x + 6, y + 2), text, font=f(SANS_B, 9), fill=(255, 255, 255))


def scene(d, x, y, w, h, kind):
    # h = 60: scene 0..46, caption strip 46..60
    if kind == "drones":
        d.rectangle([x, y, x + w, y + 46], fill=(210, 225, 240))
        for dx, dy in [(x + 16, y + 10), (x + 70, y + 6), (x + 124, y + 12)]:
            d.polygon([(dx, dy), (dx + 20, dy + 5), (dx, dy + 10)],
                      fill=(40, 40, 45))
            d.line([dx - 12, dy + 5, dx - 2, dy + 5], fill=(120, 120, 125),
                   width=2)
        for cx, cy in [(x + 44, y + 26), (x + 100, y + 30), (x + 152, y + 24)]:
            d.line([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED, width=3)
            d.line([cx - 5, cy + 5, cx + 5, cy - 5], fill=RED, width=3)
        d.text((x + 8, y + 30), "141", font=f(SANS_B, 14), fill=INK)
        d.text((x + 40, y + 34), "DRONES", font=f(SANS_B, 9), fill=INK)
        d.text((x + 118, y + 30), "126 DOWNED", font=f(SANS_B, 10), fill=RED)
        caption(d, x, y + 46, w, "KYIV  •  AIR DEFENCE", BLUE)
    elif kind == "peltola":
        d.rectangle([x, y, x + w, y + 46], fill=(225, 235, 245))
        # Capitol dome
        d.rectangle([x + 10, y + 28, x + 52, y + 44], fill=(255, 255, 255),
                    outline=(150, 150, 150))
        d.pieslice([x + 18, y + 10, x + 44, y + 36], 180, 360,
                   fill=(255, 255, 255), outline=(150, 150, 150))
        d.line([x + 31, y + 6, x + 31, y + 10], fill=(120, 120, 120), width=2)
        # Alaska outline
        d.polygon([(x + 66, y + 20), (x + 96, y + 12), (x + 128, y + 16),
                   (x + 140, y + 28), (x + 118, y + 40), (x + 84, y + 40),
                   (x + 68, y + 32)], fill=(200, 215, 190),
                  outline=(60, 90, 60))
        d.text((x + 150, y + 6), "56–44", font=f(SANS_B, 14), fill=BLUE)
        d.text((x + 150, y + 24), "SENATE", font=f(SANS_B, 10), fill=INK)
        caption(d, x, y + 46, w, "WASHINGTON  •  ALASKA", BLUE)
    elif kind == "peace":
        d.rectangle([x, y, x + w, y + 46], fill=(235, 240, 250))
        # two small flags on a table
        d.line([x + 30, y + 8, x + 30, y + 34], fill=(120, 120, 120), width=2)
        d.line([x + 66, y + 8, x + 66, y + 34], fill=(120, 120, 120), width=2)
        d.rectangle([x + 30, y + 8, x + 54, y + 20], fill=(255, 255, 255),
                    outline=(90, 90, 90))
        d.rectangle([x + 30, y + 11, x + 54, y + 13], fill=BLUE)
        d.rectangle([x + 30, y + 15, x + 54, y + 17], fill=BLUE)
        d.rectangle([x + 66, y + 8, x + 90, y + 20], fill=(255, 255, 255),
                    outline=(90, 90, 90))
        d.rectangle([x + 66, y + 8, x + 90, y + 12], fill=(20, 20, 20))
        d.rectangle([x + 66, y + 16, x + 90, y + 20], fill=GREEN)
        d.polygon([(x + 66, y + 8), (x + 78, y + 14), (x + 66, y + 20)],
                  fill=RED)
        d.rectangle([x + 16, y + 34, x + 104, y + 42], fill=(170, 130, 90))
        # tents, right
        d.polygon([(x + 120, y + 42), (x + 140, y + 16), (x + 160, y + 42)],
                  fill=(245, 245, 240), outline=(150, 140, 120))
        d.polygon([(x + 152, y + 42), (x + 170, y + 22), (x + 188, y + 42)],
                  fill=(245, 245, 240), outline=(150, 140, 120))
        d.text((x + 120, y + 4), "950,000", font=f(SANS_B, 11), fill=RED)
        caption(d, x, y + 46, w, "GAZA  •  CEASEFIRE UNDER STRAIN", ORANGE)
    elif kind == "cyclone":
        d.rectangle([x, y, x + w, y + 46], fill=(200, 220, 235))
        # coastline, left
        d.polygon([(x, y), (x + 30, y), (x + 22, y + 46), (x, y + 46)],
                  fill=SAND)
        # spiral storm
        cx, cy = x + 110, y + 24
        for r in [6, 12, 18]:
            d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
                  fill=(255, 255, 255), width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))
        d.text((x + 140, y + 6), "90–100", font=f(SANS_B, 11), fill=INK)
        d.text((x + 140, y + 20), "KM/H", font=f(SANS_B, 9), fill=INK)
        caption(d, x, y + 46, w, "BAY OF BENGAL  •  LANDFALL 20 NOV", TEAL)
    elif kind == "cop31":
        d.rectangle([x, y, x + w, y + 46], fill=(225, 240, 230))
        # globe
        d.ellipse([x + 10, y + 6, x + 46, y + 42], fill=(60, 130, 200),
                  outline=(40, 90, 160))
        d.ellipse([x + 18, y + 14, x + 28, y + 22], fill=(60, 170, 90))
        d.ellipse([x + 30, y + 26, x + 40, y + 34], fill=(60, 170, 90))
        # thermometer, rising
        d.rectangle([x + 58, y + 8, x + 66, y + 34], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.rectangle([x + 60, y + 20, x + 64, y + 32], fill=RED)
        d.ellipse([x + 55, y + 32, x + 69, y + 44], fill=RED)
        # contested wording: two opposing arrows
        d.line([x + 84, y + 16, x + 118, y + 16], fill=GREEN, width=3)
        d.polygon([(x + 118, y + 16), (x + 108, y + 11), (x + 108, y + 21)],
                  fill=GREEN)
        d.line([x + 118, y + 30, x + 84, y + 30], fill=RED, width=3)
        d.polygon([(x + 84, y + 30), (x + 94, y + 25), (x + 94, y + 35)],
                  fill=RED)
        d.text((x + 128, y + 8), "NET ZERO", font=f(SANS_B, 10), fill=INK)
        d.text((x + 128, y + 22), "BY 2030?", font=f(SANS_B, 10), fill=RED)
        caption(d, x, y + 46, w, "ANTALYA  •  CLIMATE TALKS", GREEN)
    elif kind == "jeffries":
        d.rectangle([x, y, x + w, y + 46], fill=(235, 235, 245))
        # Capitol columns
        d.rectangle([x + 10, y + 26, x + 48, y + 44], fill=(255, 255, 255),
                    outline=(150, 150, 150))
        for cx in [16, 26, 36]:
            d.rectangle([x + cx, y + 30, x + cx + 4, y + 44], fill=(180, 180, 180))
        d.pieslice([x + 16, y + 10, x + 42, y + 32], 180, 360,
                   fill=(255, 255, 255), outline=(150, 150, 150))
        # tally board
        d.rectangle([x + 62, y + 8, x + 150, y + 40], fill=NAVY)
        d.text((x + 68, y + 12), "251–11", font=f(SANS_B, 16),
               fill=(255, 255, 255))
        d.text((x + 68, y + 30), "DEMOCRATS", font=f(SANS_B, 8), fill=GOLD)
        d.text((x + 156, y + 8), "FIRST", font=f(SANS_B, 8), fill=INK)
        d.text((x + 156, y + 20), "BLACK", font=f(SANS_B, 8), fill=INK)
        d.text((x + 156, y + 32), "SPEAKER", font=f(SANS_B, 8), fill=INK)
        caption(d, x, y + 46, w, "HOUSE DEMOCRATS  •  NOMINATION", BLUE)
    elif kind == "elobeid":
        d.rectangle([x, y, x + w, y + 46], fill=(240, 235, 220))
        # Sudan outline
        d.polygon([(x + 16, y + 8), (x + 52, y + 6), (x + 66, y + 18),
                   (x + 60, y + 40), (x + 34, y + 44), (x + 18, y + 30)],
                  fill=(220, 200, 160), outline=(120, 100, 70))
        d.ellipse([x + 36, y + 18, x + 48, y + 30], fill=RED)
        d.text((x + 52, y + 20), "EL OBEID", font=f(SANS_B, 9), fill=INK)
        # drone, top right
        d.polygon([(x + 158, y + 4), (x + 178, y + 9), (x + 158, y + 14)],
                  fill=(40, 40, 45))
        d.text((x + 96, y + 6), "37 KILLED", font=f(SANS_B, 11), fill=RED)
        d.text((x + 96, y + 21), "2,230 CIVILIANS", font=f(SANS_B, 9), fill=INK)
        d.text((x + 96, y + 33), "KILLED IN 2026", font=f(SANS_B, 9), fill=INK)
        caption(d, x, y + 46, w, "SUDAN  •  AMNESTY PROBE", GREEN)
    elif kind == "inflation":
        d.rectangle([x, y, x + w, y + 46], fill=(245, 240, 225))
        # rising price line
        pts = [(x + 10, y + 38), (x + 34, y + 32), (x + 58, y + 26),
               (x + 82, y + 14)]
        d.line(pts, fill=RED, width=3)
        d.polygon([(x + 82, y + 14), (x + 74, y + 12), (x + 78, y + 22)],
                  fill=RED)
        d.text((x + 88, y + 4), "3.6%", font=f(SANS_B, 14), fill=RED)
        # gold bar falling
        d.rectangle([x + 128, y + 18, x + 150, y + 40], fill=GOLD,
                    outline=(150, 110, 20))
        d.line([x + 154, y + 14, x + 154, y + 34], fill=RED, width=2)
        d.polygon([(x + 154, y + 40), (x + 149, y + 32), (x + 159, y + 32)],
                  fill=RED)
        d.text((x + 162, y + 24), "GOLD", font=f(SANS_B, 9), fill=INK)
        caption(d, x, y + 46, w, "LONDON  •  MARKETS FALL", BLUE)
    elif kind == "ebola":
        d.rectangle([x, y, x + w, y + 46], fill=(245, 240, 225))
        d.polygon([(x + 10, y + 40), (x + 32, y + 12), (x + 54, y + 40)],
                  fill=(250, 250, 245), outline=(150, 140, 120))
        d.rectangle([x + 28, y + 20, x + 36, y + 34], fill=RED)
        d.rectangle([x + 21, y + 27, x + 43, y + 31], fill=RED)
        d.ellipse([x + 70, y + 8, x + 82, y + 20], fill=(255, 255, 255),
                  outline=(120, 120, 120))
        d.rectangle([x + 66, y + 20, x + 86, y + 42], fill=(255, 255, 255),
                    outline=(120, 120, 120))
        for i, bh in enumerate([8, 14, 22]):
            d.rectangle([x + 100 + i * 14, y + 42 - bh, x + 110 + i * 14, y + 42],
                        fill=GREEN)
        d.text((x + 144, y + 6), "11,300+", font=f(SANS_B, 11), fill=RED)
        d.text((x + 144, y + 22), "CASES", font=f(SANS_B, 9), fill=INK)
        caption(d, x, y + 46, w, "DR CONGO  •  EBOLA", GREEN)
    elif kind == "gta":
        d.rectangle([x, y, x + w, y + 46], fill=(30, 20, 50))
        # neon dusk skyline
        for bx, bw, bh, col in [(8, 16, 20, (255, 120, 180)),
                                (28, 12, 30, (120, 220, 255)),
                                (44, 20, 24, (255, 200, 80)),
                                (68, 14, 34, (255, 120, 180)),
                                (86, 18, 22, (120, 220, 255)),
                                (108, 14, 28, (255, 200, 80))]:
            d.rectangle([x + bx, y + 44 - bh, x + bx + bw, y + 44], fill=col)
        d.rectangle([x + 128, y + 8, x + 182, y + 40], fill=(255, 255, 255),
                    outline=(200, 200, 200))
        d.text((x + 142, y + 12), "VI", font=f(SERIF_B, 20), fill=(30, 20, 50))
        caption(d, x, y + 46, w, "OUT 19 NOV  •  13 YEARS ON", PURPLE)


# ---------------- content -------------------------------------------------
REGIONS = [
    ("Europe", 8, BLUE), ("Middle East", 3, ORANGE), ("Asia", 6, PURPLE),
    ("Africa", 5, GREEN), ("Americas", 17, RED), ("Oceania", 1, TEAL),
    ("Global & Space", 5, GOLDD),
]

LEADS = [
    ("ASIA • APEC", PURPLE, panel_shenzhen,
     "Xi greets Trump in Shenzhen as APEC opens",
     "Xi welcomes Trump on arrival; Putin denounces sanctions; "
     "trilateral set for Thursday."),
    ("MIDDLE EAST • GULF", ORANGE, panel_gulf,
     "Kuwait and Bahrain intercept Iran's drones",
     "After the US strike on Qeshm; tanker hit in Hormuz, 1 missing, "
     "11 hurt; Houthis fire at the Saudi pipeline."),
    ("EUROPE • EU LOAN", BLUE, panel_eu45,
     "EU proposes €45bn loan for Ukraine in 2027",
     "€20bn budget aid + €25bn military, repaid from Russian "
     "reparations."),
    ("GLOBAL & SPACE • VOYAGER", GOLDD, panel_voyager,
     "Voyager 1 one light-day from Earth",
     "First human-made object to reach it: 25.9bn km, at 10:16 GMT."),
]

CARDS = [
    (5, "EUROPE • 141 DRONES", BLUE, "drones",
     "141 drones over Ukraine, 126 downed",
     "6 hurt in Dnipro; Kyiv seeks 12 more jets, France sends Mirage "
     "2000-5F."),
    (6, "AMERICAS • PELTOLA WINS", RED, "peltola",
     "Peltola beats Sullivan; Senate 56–44",
     "AP calls it; first Alaska Native elected to the Senate."),
    (7, "MIDDLE EAST • BOARD OF PEACE", ORANGE, "peace",
     "Board of Peace faults Israel and Hamas",
     "WHO: 950,000 displaced on flood-prone ground; cold kills in "
     "tents."),
    (8, "ASIA • CYCLONE AKVAN", PURPLE, "cyclone",
     "Cyclone Akvan churns in the Bay of Bengal",
     "90–100 km/h, 730 km south of Gopalpur; landfall due 20 Nov."),
    (9, "GLOBAL • COP31 DEADLOCK", GOLDD, "cop31",
     "COP31 split over fossil-fuel phase-out",
     "EU calls the first draft 'untenable'; net-zero-2030 wording "
     "contested."),
    (10, "AMERICAS • JEFFRIES 251–11", RED, "jeffries",
     "Jeffries nominated Speaker-designate 251–11",
     "First Black Speaker in waiting; formal House vote in January."),
    (11, "AFRICA • EL OBEID", GREEN, "elobeid",
     "RSF drone strikes kill 37 in El Obeid",
     "Amnesty urges a war-crimes probe; UN: 2,230 civilians killed "
     "in 2026."),
    (12, "EUROPE • INFLATION", BLUE, "inflation",
     "UK inflation 3.6%; Fed eyes bigger hikes",
     "Gold below $3,800; markets fall: CAC −1.62%, DAX −2.08%, "
     "S&P −1.03%."),
    (13, "AFRICA • EBOLA", GREEN, "ebola",
     "Ebola cases pass 11,300 in DR Congo",
     "Nearly 3 in 4 under-5s die; Bunia, Beni epicentres; vaccines "
     "in Phase 2."),
    (14, "AMERICAS • GTA VI", RED, "gta",
     "GTA VI hits shelves tomorrow",
     "After 13 years; 14.9m pre-orders."),
]

ALSO = [
    (15, "Bangladesh: 55 factories shut; blasts in 28 districts"),
    (16, "Haiti backs Salvadoran troops; security pact signed"),
    (17, "Ethiopia and Eritrea mass forces on their border"),
    (18, "Myanmar reviews ASEAN ties; ICJ ruling due Thu"),
    (19, "UK, Australia sanction settlers; 72-year-old killed"),
    (20, "US outages reach NSA network; Java flaw found by AI"),
    (21, "Waymo suspends driverless rides on US highways"),
    (22, "Deutsche Bank leak: 15 million internal documents"),
    (23, "US AI-chip curbs tighten in SE Asia; Beijing warns"),
    (24, "Anthropic IPO priced at $83 a share"),
    (25, "Nvidia board rules out return of ousted CEO Huang"),
    (26, "Slovakia protests against PM Fico's government"),
    (27, "Italy approves antisemitism law; free-speech worries"),
    (28, "EU acts against Temu; NATO unveils new comms strategy"),
    (29, "Kalshi halts 'mention' markets after CFTC order"),
    (30, "House Oversight letters to Trump Jr., Vance and Miller"),
    (31, "Fed's Cook refuses Dec 14 hearing unless Hassett out"),
    (32, "White House drops FDA nominee Overton"),
    (33, "ICE: no ships for deportations; New Jersey sues DHS"),
    (34, "Baltimore students sue Omnilert over AI gun error"),
    (35, "AI models mistake civilians for targets, Vals finds"),
    (36, "Markets fall; Brent $91.55; Bitcoin $64,649"),
    (37, "Taiwan: 10 PLA sorties, 11 ships; Russian jets off coast"),
    (38, "Russian An-12 crashes in Siberia; all 19 aboard dead"),
    (39, "Uganda: Mugumya charged with treason in military court"),
    (40, "Sudan army gains in West Kordofan; Libya drug seizures"),
    (41, "Brazil: ~20 isolated Indigenous people emerge"),
    (42, "Costa Rican journalist investigating drug gangs killed"),
    (43, "Pope Leo XIV appeals against hate after Peru tour"),
    (44, "Australia wages fastest rise since 2023; NZ alert lifted"),
    (45, "OpenAI launches GPT-6.2 Astra/Sol; Reliance 1,600 sats"),
]

PINS = [
    (1, 114.1, 22.5, PURPLE),            # Shenzhen
    (2, 48.0, 29.3, ORANGE),             # Kuwait
    (3, 4.4, 50.8, BLUE, 15, 56),        # Brussels, offset up-right
    (4, -118.2, 34.1, GOLDD),            # JPL — Voyager 1 tracked from here
    (5, 30.5, 50.4, BLUE),               # Kyiv
    (6, -150.0, 61.0, RED),              # Alaska
    (7, 34.5, 31.5, ORANGE, 42, 27),     # Gaza, offset right
    (8, 87.0, 16.0, PURPLE),             # Bay of Bengal
    (9, 30.7, 36.9, GOLDD, 38, 41),      # Antalya, offset up-right
    (10, -77.0, 38.9, RED),              # Washington DC
    (11, 30.2, 13.2, GREEN),             # El Obeid
    (12, -0.1, 51.5, BLUE, -13, 57),     # London, offset up-left
    (13, 30.2, 1.6, GREEN),              # Bunia
    (14, -80.2, 25.8, RED),              # Miami (Vice City)
]
DOTS = [
    (90.4, 23.8), (-72.3, 18.9), (39.0, 12.0), (96.0, 21.0),
    (35.2, 31.9), (-76.8, 39.1), (-122.4, 37.8), (8.7, 50.1),
    (103.8, 1.4), (-122.4, 37.8), (-121.0, 37.4), (17.1, 48.1),
    (12.5, 41.9), (7.0, 49.0), (-74.0, 40.7), (-77.0, 38.9),
    (-77.0, 38.9), (-77.0, 38.9), (-74.0, 40.7), (-76.6, 39.3),
    (-122.0, 37.8), (-0.1, 51.5), (121.0, 23.5), (86.0, 55.4),
    (32.6, 0.3), (28.5, 12.5), (-62.0, -3.0), (-84.0, 9.7),
    (-77.0, -12.0), (149.1, -35.3), (72.8, 19.1),
]

DATE_CHECK = (
    "DATE CHECK — Not 18 November, so not on this page: the Kerch Bridge "
    "collapse, Nvidia's results, the Knesset speaker vote and Mongolia's "
    "president quitting (17 Nov). The US strike on Qeshm was Tuesday night "
    "and appears only as the cause of today's drones. Every story above "
    "happened or was first reported on Wednesday 18 November 2026.")


def build(out="entry.png"):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    mx = 20

    # ---- navy masthead with calendar block ----
    d.rectangle([0, 0, W, 100], fill=NAVY)
    d.text((mx, 8), "THE WORLD TODAY  •  ONE DAY, IN ONE PICTURE",
           font=f(SANS_B, 13), fill=GOLD)
    d.text((mx, 26), "Wednesday 18 November 2026",
           font=f(SERIF_B, 46), fill=(255, 255, 255))
    d.text((mx, 78), "45 STORIES  •  6 CONTINENTS  •  7 REGIONS  •  ONE PAGE",
           font=f(SANS_B, 12), fill=(255, 255, 255))
    # calendar block, top right
    cx0, cy0, cw, chh = 884, 8, 120, 84
    d.rectangle([cx0, cy0, cx0 + cw, cy0 + chh], fill=(255, 255, 255))
    d.rectangle([cx0, cy0, cx0 + cw, cy0 + 20], fill=RED)
    d.text((cx0 + 44, cy0 + 3), "NOV", font=f(SANS_B, 13), fill=(255, 255, 255))
    d.text((cx0 + 38, cy0 + 22), "18", font=f(SERIF_B, 34), fill=NAVY)
    d.text((cx0 + 24, cy0 + 62), "WED 2026", font=f(SANS_B, 12), fill=RED)

    # ---- region bar + legend ----
    total = sum(c for _, c, _ in REGIONS)
    assert total == 45, f"region counts sum to {total}, not 45"
    bx = mx
    bar_y, bar_h = 106, 18
    for name, count, col in REGIONS:
        seg = 984 * count // 45
        d.rectangle([bx, bar_y, bx + seg, bar_y + bar_h], fill=col)
        d.text((bx + seg // 2 - 3, bar_y + 3), str(count),
               font=f(SANS_B, 11), fill=(255, 255, 255))
        bx += seg
    lx = mx
    ly = 128
    for i, (name, count, col) in enumerate(REGIONS):
        d.rectangle([lx, ly + 2, lx + 10, ly + 12], fill=col)
        lab = f"{name} {count}"
        d.text((lx + 13, ly), lab, font=f(SANS_B, 10), fill=INK)
        lx += 13 + d.textlength(lab, font=f(SANS_B, 10)) + 16

    # ---- day in numbers strip ----
    d.rectangle([0, 144, W, 166], fill=INK)
    nums = ("141 DRONES OVER UKRAINE  •  €45BN EU LOAN  •  11,300+ EBOLA "
            "CASES  •  251–11 JEFFRIES  •  25.9BN KM VOYAGER  •  55 "
            "BANGLADESH FACTORIES SHUT")
    nums = one_line(d, nums, f(SANS_B, 12), W - 2 * mx, "numbers strip")
    d.text((mx, 149), nums, font=f(SANS_B, 12), fill=(255, 255, 255))

    # ---- four leads ----
    pw, ph, pg = 240, 106, 8
    for i, (kick, col, panel, head, deck) in enumerate(LEADS):
        x = mx + i * (pw + pg)
        panel(d, x, 172, pw, ph)
        kicker(d, x, 282, i + 1, kick, col)
        para(d, x, 300, head, f(SERIF_B, 19), pw, max_lines=2,
             what=f"lead {i + 1} headline")
        para(d, x, 340, deck, f(SERIF, 11), pw, max_lines=2, leading=13,
             what=f"lead {i + 1} deck")
    d.line([mx, 372, W - mx, 372], fill=INK, width=2)

    # ---- ten cards, two rows of five ----
    cw, chh, cg = 190, 60, 8
    for idx, (num, kick, col, kind, head, deck) in enumerate(CARDS):
        row, c = divmod(idx, 5)
        x = mx + c * (cw + cg)
        y = 380 + row * 150
        scene(d, x, y, cw, 60, kind)
        kicker(d, x, y + 64, num, kick, col)
        para(d, x, y + 82, head, f(SERIF_B, 14), cw, max_lines=2,
             what=f"card {num} headline")
        para(d, x, y + 116, deck, f(SERIF, 11), cw, max_lines=2, leading=13,
             what=f"card {num} deck")

    # ---- map + also list ----
    y0 = 686
    d.line([mx, y0 - 8, W - mx, y0 - 8], fill=INK, width=2)
    d.text((mx, y0 - 4), "WHERE IT HAPPENED", font=f(SANS_B, 13), fill=RED)
    d.text((mx + 360, y0 - 4), "ALSO ON WEDNESDAY 18 NOVEMBER",
           font=f(SANS_B, 13), fill=RED)
    draw_map(d, mx, y0 + 16, 330, 200, PINS, DOTS)
    d.text((mx, y0 + 220),
           "Pins: stories 1–14  •  dots: 15–45  •  Pin 4: Voyager 1, "
           "tracked from JPL",
           font=f(SANS, 10), fill=(90, 90, 90))
    lx = mx + 360
    colw = 310
    for i, (n, item) in enumerate(ALSO):
        col, row = divmod(i, 16)
        x = lx + col * (colw + 14)
        yy = y0 + 16 + row * 13.4
        d.ellipse([x, yy + 1, x + 13, yy + 14], fill=PURPLE)
        d.text((x + 2 if n < 10 else x + 0.5, yy + 2.5), str(n),
               font=f(SANS_B, 8), fill=(255, 255, 255))
        item = one_line(d, item, f(SERIF, 12), colw - 18,
                        f"also {n}")
        d.text((x + 18, yy + 1), item, font=f(SERIF, 12), fill=INK)

    # ---- date check box + sources ----
    d.line([mx, 916, W - mx, 916], fill=INK, width=2)
    d.rectangle([mx, 922, W - mx, 992], outline=RED, width=2, fill=(255, 250, 245))
    d.text((mx + 8, 928), "DATE CHECK", font=f(SANS_B, 11), fill=RED)
    para(d, mx + 8, 944, DATE_CHECK, f(SANS, 11), W - 2 * mx - 8,
         max_lines=3, leading=13, what="date check")
    d.text((mx, 1000),
           "Sources: Reuters, AP, AFP, BBC, IMD, Amnesty International, "
           "European Commission, NPR — 18 November 2026. All drawings "
           "original.",
           font=f(SANS, 11), fill=(90, 90, 90))

    # ---- count verification ----
    n_total = len(LEADS) + len(CARDS) + len(ALSO)
    assert n_total == 45, f"total stories {n_total}, not 45"
    assert len(ALSO) == 31 and [n for n, _ in ALSO] == list(range(15, 46))
    assert len(DOTS) == 31, f"{len(DOTS)} dots, need 31"

    img.save(out, optimize=True)
    print(out, img.size, len(open(out, "rb").read()), "bytes")


if __name__ == "__main__":
    build(os.path.join(HERE, "entry.png"))
