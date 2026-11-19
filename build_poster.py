#!/usr/bin/env python3
"""Build entry.png — 'Wednesday 18 November 2026' front page.

Own design, own code, own flat drawings. Structure: dark masthead with a
red news ticker, three rich lead diagrams, ten illustrated story cards with
captioned scenes, a real-coastline world map with colour-coded numbered
pins, a numbered also-list, and a sources line — 43 stories in all, every
one a real event reported on 18 November 2026, with contested claims
attributed ("Ukraine says", "Iran says", "reports say"). The world outline
is Natural Earth 110m land data (public domain) in map_data.py.
"""
import math
import sys

sys.path.insert(0, "/home/hatch/workspace/makefun/news-image-20261118")
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


def para(d, x, y, text, font, max_w, fill=INK, leading=None, max_lines=None):
    lh = leading or int(font.size * 1.18)
    lines = wrap(d, text, font, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def one_line(d, text, font, max_w):
    while text and d.textlength(text, font=font) > max_w:
        text = text.rsplit(" ", 1)[0]
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
        d.ellipse([x - 2.5, y - 2.5, x + 2.5, y + 2.5], fill=(90, 90, 90))
    for pin in pins:
        # (n, lon, lat, colour) or (n, lon, lat, colour, off_lon, off_lat)
        n, lo, la, col = pin[0], pin[1], pin[2], pin[3]
        tx, ty = px(lo, la)
        if len(pin) > 4:
            x, y = px(pin[4], pin[5])
            d.line([tx, ty, x, y], fill=(60, 60, 60), width=1)
        else:
            x, y = tx, ty
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=col,
                  outline=(255, 255, 255), width=1)
        d.text((x - 2.5 if n < 10 else x - 4.5, y - 4.5), str(n),
               font=f(SANS_B, 7), fill=(255, 255, 255))


# ---------------- lead panels (flat diagrams, drawn from scratch) --------
def panel_kerch(d, x, y, w, h):
    """Kerch Strait: an arched bridge, one span dropped into the sea."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h - 44, x + w, y + h], fill=SEA)
    for i in range(5):
        d.arc([x + 12 + i * 62, y + h - 34, x + 52 + i * 62, y + h - 14],
              200, 340, fill=(255, 255, 255), width=2)
    # arch ribs rising from the water
    d.arc([x + 20, y + 18, x + w // 2 + 10, y + 96], 180, 360,
          fill=(70, 70, 78), width=5)
    d.arc([x + w // 2 - 6, y + 18, x + w - 20, y + 96], 180, 360,
          fill=(70, 70, 78), width=5)
    # road deck, broken in the middle
    d.rectangle([x + 8, y + 52, x + w // 2 - 14, y + 60], fill=(70, 70, 78))
    d.rectangle([x + w // 2 + 34, y + 52, x + w - 8, y + 60], fill=(70, 70, 78))
    d.rectangle([x + 8, y + 64, x + w // 2 - 14, y + 70], fill=(100, 100, 108))
    d.rectangle([x + w // 2 + 34, y + 64, x + w - 8, y + 70], fill=(100, 100, 108))
    for bx in range(x + 16, x + w - 16, 30):
        if x + w // 2 - 20 < bx < x + w // 2 + 36:
            continue
        d.rectangle([bx, y + 70, bx + 4, y + h - 44], fill=(90, 90, 98))
    # the fallen span, tilted down into the strait, in red
    d.polygon([(x + w // 2 - 14, y + 54), (x + w // 2 + 34, y + 60),
               (x + w // 2 + 28, y + 70), (x + w // 2 - 18, y + 64)],
              fill=RED)
    d.polygon([(x + w // 2 + 10, y + 66), (x + w // 2 + 34, y + 60),
               (x + w // 2 + 28, y + 70), (x + w // 2 + 8, y + 74)],
              fill=(120, 25, 25))
    # smoke, blast star and flames at the gap
    for cx, cy, r in [(x + w // 2 - 4, y + 32, 9), (x + w // 2 + 12, y + 22, 12),
                      (x + w // 2 + 28, y + 32, 8), (x + w // 2 - 22, y + 26, 7)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(110, 110, 115))
    d.polygon([(x + w // 2 - 6, y + 40), (x + w // 2 + 4, y + 52),
               (x + w // 2 + 14, y + 40), (x + w // 2 + 4, y + 46)],
              fill=(255, 170, 0))
    d.polygon([(x + w // 2 + 16, y + 52), (x + w // 2 + 24, y + 62),
               (x + w // 2 + 32, y + 52), (x + w // 2 + 24, y + 58)],
              fill=(255, 120, 0))
    # debris floating in the sea
    for dx, dy, dw in [(x + w // 2 + 2, y + h - 38, 14),
                       (x + w // 2 + 24, y + h - 32, 10),
                       (x + w // 2 - 24, y + h - 30, 8)]:
        d.rectangle([dx, dy, dx + dw, dy + 4], fill=(70, 70, 78))
    # a drone with a dashed trail, upper left
    jx, jy = x + 30, y + 26
    d.polygon([(jx, jy), (jx + 18, jy + 5), (jx, jy + 10)], fill=(40, 40, 45))
    for s in range(0, 16, 4):
        d.line([jx - s, jy + 5, jx - s - 2, jy + 5], fill=(120, 120, 125), width=2)
    d.text((x + 8, y + 6), "CRIMEA", font=f(SANS_B, 10), fill=(60, 60, 60))
    d.text((x + w - 52, y + 6), "RUSSIA", font=f(SANS_B, 10), fill=(60, 60, 60))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=INK)
    d.text((x + 8, y + h - 19), "KERCH STRAIT  •  ONE ARCH DOWN",
           font=f(SANS_B, 10), fill=(255, 255, 255))


def panel_gulf(d, x, y, w, h):
    """The Gulf: Qeshm, Kuwait and Bahrain, drones overhead, a tanker hit."""
    d.rectangle([x, y, x + w, y + h], fill=SAND)
    # the Gulf sea, lower right
    d.polygon([(x + 70, y + 44), (x + 130, y + 34), (x + w, y + 52),
               (x + w, y + h), (x + 40, y + h), (x + 30, y + 80)],
              fill=SEA)
    d.text((x + w - 52, y + 6), "IRAN", font=f(SANS_B, 10), fill=(60, 60, 60))
    d.text((x + 10, y + 6), "KUWAIT", font=f(SANS_B, 10), fill=(60, 60, 60))
    d.text((x + 96, y + 40), "BAHRAIN", font=f(SANS_B, 9), fill=(60, 60, 60))
    # Qeshm island, struck from the air
    d.ellipse([x + w - 96, y + 26, x + w - 44, y + 46], fill=(200, 180, 140),
              outline=(120, 100, 70))
    # strike star above the island, smoke far to the left over the sea
    d.polygon([(x + w - 72, y + 12), (x + w - 66, y + 24),
               (x + w - 60, y + 12), (x + w - 66, y + 18)], fill=(255, 140, 0))
    d.ellipse([x + 168, y + 12, x + 188, y + 32], fill=(110, 110, 115))
    d.text((x + w - 90, y + 32), "QESHM", font=f(SANS_B, 8), fill=(60, 60, 60))
    # air base on the Kuwait coast
    d.rectangle([x + 8, y + 66, x + 46, y + 92], fill=(200, 190, 170))
    d.pieslice([x + 10, y + 44, x + 42, y + 76], 180, 360,
               fill=(245, 245, 240), outline=(150, 150, 150))
    d.line([x + 26, y + 44, x + 26, y + 36], fill=(120, 120, 120), width=2)
    d.ellipse([x + 24, y + 34, x + 28, y + 38], fill=(120, 120, 120))
    # drone flight paths, dashed red, with interception crosses
    pts = [(x + 56, y + 70), (x + 120, y + 54), (x + 190, y + 46),
           (x + 250, y + 58)]
    for i in range(len(pts) - 1):
        ax, ay = pts[i]
        bx, by = pts[i + 1]
        for s in range(0, 10, 2):
            t0, t1 = s / 10.0, (s + 1) / 10.0
            d.line([ax + (bx - ax) * t0, ay + (by - ay) * t0,
                    ax + (bx - ax) * t1, ay + (by - ay) * t1],
                   fill=RED, width=2)
    d.polygon([(x + 52, y + 66), (x + 64, y + 70), (x + 52, y + 74)],
              fill=(40, 40, 45))
    d.polygon([(x + 244, y + 54), (x + 256, y + 58), (x + 244, y + 62)],
              fill=(40, 40, 45))
    for cx, cy in [(x + 120, y + 58), (x + 170, y + 66)]:
        d.line([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED, width=3)
        d.line([cx - 6, cy + 6, cx + 6, cy - 6], fill=RED, width=3)
    # tanker ablaze in the strait
    d.rectangle([x + w - 92, y + h - 58, x + w - 18, y + h - 44],
                fill=(120, 40, 40))
    d.rectangle([x + w - 82, y + h - 68, x + w - 64, y + h - 58],
                fill=(120, 40, 40))
    d.polygon([(x + w - 52, y + h - 86), (x + w - 44, y + h - 70),
               (x + w - 36, y + h - 86), (x + w - 44, y + h - 76)],
              fill=(255, 140, 0))
    d.ellipse([x + w - 56, y + h - 92, x + w - 38, y + h - 74],
              fill=(110, 110, 115))
    d.rectangle([x + 92, y + 74, x + 212, y + 90], fill=GREEN)
    d.text((x + 98, y + 77), "DRONES INTERCEPTED", font=f(SANS_B, 10),
           fill=(255, 255, 255))
    d.rectangle([x + 118, y + 92, x + 228, y + 106], fill=RED)
    d.text((x + 124, y + 94), "QESHM: US STRIKE", font=f(SANS_B, 10),
           fill=(255, 255, 255))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=INK)
    d.text((x + 8, y + h - 19), "STRAIT OF HORMUZ  •  THE GULF",
           font=f(SANS_B, 10), fill=(255, 255, 255))


def flag(d, x, y, w, h, kind):
    d.rectangle([x, y, x + w, y + h], outline=(90, 90, 90), width=1)
    if kind == "cn":
        d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        for sx, sy, r in [(8, 7, 4), (20, 4, 2), (24, 10, 2), (20, 17, 2),
                          (12, 19, 2)]:
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
                d.ellipse([x + 3 + sx * 7, y + 3 + sy * 7,
                           x + 6 + sx * 7, y + 6 + sy * 7], fill=(255, 255, 255))


def panel_shenzhen(d, x, y, w, h):
    """Shenzhen: Xi hosts Putin at APEC; Trump lands for Thursday's summit."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 240))
    d.rectangle([x, y, x + w, y + 24], fill=PURPLE)
    d.text((x + 8, y + 5), "APEC  •  SHENZHEN SUMMIT",
           font=f(SANS_B, 11), fill=(255, 255, 255))
    # skyline behind the table
    for bx, bw, bh in [(10, 22, 30), (38, 16, 44), (60, 26, 36),
                       (92, 18, 50), (116, 24, 32), (146, 18, 46),
                       (170, 26, 38), (202, 16, 52), (224, 24, 34),
                       (254, 18, 44), (278, 22, 30)]:
        d.rectangle([x + bx, y + 96 - bh, x + bx + bw, y + 96],
                    fill=(170, 165, 190))
    # three flags over the summit table
    fw, fh, gap = 62, 34, 12
    total = 3 * fw + 2 * gap
    sx = x + (w - total) // 2
    for i, (kind, name) in enumerate([("cn", "CHINA"), ("ru", "RUSSIA"),
                                      ("us", "USA")]):
        fx = sx + i * (fw + gap)
        flag(d, fx, y + 32, fw, fh, kind)
        d.text((fx + fw // 2 - len(name) * 3, y + 70), name,
               font=f(SANS_B, 9), fill=INK)
        d.rectangle([fx + 8, y + 84, fx + fw - 8, y + 90], fill=(120, 85, 40))
    # a jet landing on the tarmac strip
    d.rectangle([x + 12, y + 96, x + w - 12, y + 104], fill=(120, 85, 40))
    d.polygon([(x + w - 96, y + 88), (x + w - 46, y + 88), (x + w - 30, y + 92),
               (x + w - 30, y + 96), (x + w - 46, y + 100), (x + w - 96, y + 100)],
              fill=(245, 245, 245), outline=(120, 120, 120))
    d.polygon([(x + w - 76, y + 88), (x + w - 66, y + 80), (x + w - 58, y + 88)],
              fill=(245, 245, 245), outline=(120, 120, 120))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=PURPLE)
    d.text((x + 8, y + h - 19), "SHENZHEN • WED 18 NOV",
           font=f(SANS_B, 10), fill=(255, 255, 255))
    d.text((x + w - 150, y + h - 19), "TRILATERAL • THU 19 NOV",
           font=f(SANS_B, 10), fill=(255, 255, 255))


# ---------------- card illustrations (190 x 60, caption strip) -------
def caption(d, x, y, w, text, fill):
    d.rectangle([x, y, x + w, y + 14], fill=fill)
    d.text((x + 6, y + 2), text, font=f(SANS_B, 9), fill=(255, 255, 255))


def icon(d, x, y, w, h, kind):
    # h = 60: scene 0..46, caption strip 46..60
    if kind == "alaska":
        d.rectangle([x, y, x + w, y + 46], fill=(225, 235, 245))
        # ballot box with a tick
        d.rectangle([x + 14, y + 14, x + 66, y + 42], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.rectangle([x + 30, y + 8, x + 50, y + 14], fill=BLUE)
        d.line([x + 22, y + 30, x + 32, y + 38, x + 58, y + 16],
               fill=GREEN, width=3)
        d.text((x + 78, y + 6), "56–44", font=f(SANS_B, 14), fill=BLUE)
        d.text((x + 78, y + 24), "SENATE", font=f(SANS_B, 10), fill=INK)
        d.text((x + 138, y + 6), "PELTOLA", font=f(SANS_B, 10), fill=RED)
        d.text((x + 138, y + 22), "WINS", font=f(SANS_B, 10), fill=INK)
        caption(d, x, y + 46, w, "ALASKA  •  SENATE FLIPS", BLUE)
    elif kind == "knesset":
        d.rectangle([x, y, x + w, y + 46], fill=(235, 240, 250))
        # chamber: arc of seats, red majority
        cx, cy, r = x + 62, y + 42, 28
        for i in range(11):
            ang = math.pi * (1 - i / 10.0)
            px = cx + r * 0.95 * math.cos(ang)
            py = cy - r * 0.95 * math.sin(ang)
            col = RED if i < 7 else BLUE
            d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=col)
        d.rectangle([x + 104, y + 8, x + 170, y + 22], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.text((x + 108, y + 10), "66", font=f(SANS_B, 12), fill=RED)
        d.text((x + 130, y + 10), "OF 120", font=f(SANS_B, 10), fill=INK)
        d.text((x + 104, y + 26), "SPEAKER VOTE", font=f(SANS_B, 9), fill=INK)
        caption(d, x, y + 46, w, "JERUSALEM  •  KNESSET", BLUE)
    elif kind == "gaza":
        d.rectangle([x, y, x + w, y + 46], fill=(230, 238, 245))
        # tents in the cold, snowflakes falling
        for i in range(2):
            tx = x + 12 + i * 52
            d.polygon([(tx, y + 42), (tx + 20, y + 16), (tx + 40, y + 42)],
                      fill=(245, 245, 240), outline=(150, 140, 120))
        for sx, sy in [(x + 120, y + 8), (x + 140, y + 20), (x + 162, y + 10),
                       (x + 176, y + 26), (x + 128, y + 32)]:
            d.text((sx, sy), "*", font=f(SANS_B, 12), fill=(120, 160, 200))
        d.text((x + 118, y + 32), "4TH WINTER", font=f(SANS_B, 9), fill=INK)
        caption(d, x, y + 46, w, "GAZA  •  COLD KILLS IN TENTS", ORANGE)
    elif kind == "ebola":
        d.rectangle([x, y, x + w, y + 46], fill=(245, 240, 225))
        # clinic tent with a red cross
        d.polygon([(x + 10, y + 40), (x + 32, y + 12), (x + 54, y + 40)],
                  fill=(250, 250, 245), outline=(150, 140, 120))
        d.rectangle([x + 28, y + 20, x + 36, y + 34], fill=RED)
        d.rectangle([x + 21, y + 27, x + 43, y + 31], fill=RED)
        # masked health worker
        d.ellipse([x + 70, y + 8, x + 82, y + 20], fill=(255, 255, 255),
                  outline=(120, 120, 120))
        d.rectangle([x + 66, y + 20, x + 86, y + 42], fill=(255, 255, 255),
                    outline=(120, 120, 120))
        # rising case bars
        for i, bh in enumerate([8, 14, 22]):
            d.rectangle([x + 100 + i * 14, y + 42 - bh, x + 110 + i * 14, y + 42],
                        fill=GREEN)
        d.text((x + 144, y + 6), "11,000+", font=f(SANS_B, 11), fill=RED)
        d.text((x + 144, y + 22), "CASES", font=f(SANS_B, 9), fill=INK)
        caption(d, x, y + 46, w, "DR CONGO  •  EBOLA", GREEN)
    elif kind == "measles":
        d.rectangle([x, y, x + w, y + 46], fill=(255, 240, 235))
        # three vaccine vials
        for i, col in enumerate([BLUE, (0, 104, 71), RED]):
            vx = x + 12 + i * 40
            d.rectangle([vx, y + 12, vx + 26, y + 40], fill=(255, 255, 255),
                        outline=INK, width=1)
            d.rectangle([vx, y + 12, vx + 26, y + 20], fill=col)
            d.rectangle([vx + 8, y + 4, vx + 18, y + 12], fill=col)
        # virus particles
        for vx, vy in [(x + 150, y + 14), (x + 168, y + 26), (x + 146, y + 32)]:
            d.ellipse([vx - 6, vy - 6, vx + 6, vy + 6], fill=RED)
            for dx, dy in [(-7, 0), (7, 0), (0, -7), (0, 7)]:
                d.line([vx, vy, vx + dx, vy + dy], fill=RED, width=2)
        caption(d, x, y + 46, w, "MEASLES-FREE STATUS LOST", RED)
    elif kind == "nvidia":
        d.rectangle([x, y, x + w, y + 46], fill=(12, 20, 12))
        d.rectangle([x + 10, y + 8, x + 58, y + 38], fill=(30, 60, 30),
                    outline=(118, 185, 0), width=2)
        d.text((x + 14, y + 14), "NVIDIA", font=f(SANS_B, 11),
               fill=(118, 185, 0))
        for i, bh in enumerate([8, 14, 20, 28]):
            d.rectangle([x + 72 + i * 14, y + 40 - bh, x + 82 + i * 14, y + 40],
                        fill=(118, 185, 0))
        d.text((x + 136, y + 6), "$115.8BN", font=f(SANS_B, 11),
               fill=(118, 185, 0))
        d.text((x + 136, y + 22), "Q4: $130BN", font=f(SANS_B, 9),
               fill=(255, 255, 255))
        caption(d, x, y + 46, w, "NVIDIA QUARTER  •  RECORD SALES", (20, 40, 20))
    elif kind == "an12":
        d.rectangle([x, y, x + w, y + 46], fill=(225, 235, 245))
        # snowy Siberian peaks
        for mx, mw, mh in [(x + 8, 44, 26), (x + 48, 56, 34), (x + 100, 40, 22)]:
            d.polygon([(mx, y + 44), (mx + mw // 2, y + 44 - mh),
                       (mx + mw, y + 44)], fill=(200, 205, 210))
            d.polygon([(mx + mw // 2 - 6, y + 44 - mh), (mx + mw // 2, y + 44 - mh),
                       (mx + mw // 2 + 6, y + 44 - mh),
                       (mx + mw // 2, y + 44 - mh + 8)],
                      fill=(255, 255, 255))
        # cargo plane silhouette
        d.polygon([(x + 118, y + 10), (x + 168, y + 10), (x + 184, y + 14),
                   (x + 184, y + 18), (x + 168, y + 22), (x + 118, y + 22)],
                  fill=(60, 60, 65))
        d.polygon([(x + 138, y + 10), (x + 148, y + 2), (x + 156, y + 10)],
                  fill=(60, 60, 65))
        d.polygon([(x + 124, y + 22), (x + 132, y + 30), (x + 140, y + 22)],
                  fill=(60, 60, 65))
        caption(d, x, y + 46, w, "KEMEROVO  •  ALL 19 ABOARD KILLED", RED)
    elif kind == "westbank":
        d.rectangle([x, y, x + w, y + 46], fill=(240, 235, 225))
        # scales of justice
        d.line([x + 40, y + 8, x + 40, y + 38], fill=INK, width=2)
        d.line([x + 16, y + 10, x + 64, y + 10], fill=INK, width=2)
        d.polygon([(x + 10, y + 10), (x + 22, y + 10), (x + 16, y + 24)],
                  fill=GOLD)
        d.polygon([(x + 58, y + 10), (x + 70, y + 10), (x + 64, y + 24)],
                  fill=GOLD)
        d.rectangle([x + 88, y + 8, x + 182, y + 24], fill=RED)
        d.text((x + 92, y + 10), "SANCTIONED", font=f(SANS_B, 10),
               fill=(255, 255, 255))
        d.text((x + 88, y + 28), "UK + AUSTRALIA", font=f(SANS_B, 10), fill=INK)
        caption(d, x, y + 46, w, "WEST BANK  •  SETTLEMENTS", ORANGE)
    elif kind == "bangladesh":
        d.rectangle([x, y, x + w, y + 46], fill=(240, 240, 235))
        # a bus with flames, paramilitary helmets behind
        d.rectangle([x + 8, y + 18, x + 64, y + 40], fill=(40, 90, 140))
        for wx in [14, 30, 46]:
            d.rectangle([x + wx, y + 22, x + wx + 12, y + 30],
                        fill=(180, 220, 240))
        d.polygon([(x + 76, y + 18), (x + 84, y + 6), (x + 92, y + 18)],
                  fill=(255, 140, 0))
        d.polygon([(x + 94, y + 18), (x + 102, y + 8), (x + 110, y + 18)],
                  fill=(255, 120, 0))
        for hx in [124, 148, 172]:
            d.pieslice([x + hx, y + 22, x + hx + 20, y + 42], 180, 360,
                       fill=(60, 90, 60))
            d.rectangle([x + hx, y + 40, x + hx + 20, y + 42],
                        fill=(60, 90, 60))
        caption(d, x, y + 46, w, "DHAKA  •  UNREST SPREADS", TEAL)
    elif kind == "outages":
        d.rectangle([x, y, x + w, y + 46], fill=(20, 24, 40))
        # server racks, one flashing red
        for i in range(3):
            rx = x + 12 + i * 34
            col = RED if i == 1 else (60, 120, 200)
            d.rectangle([rx, y + 6, rx + 26, y + 40], fill=(40, 50, 70),
                        outline=col, width=2)
            for ly in [12, 20, 28]:
                d.rectangle([rx + 4, y + ly, rx + 14, y + ly + 4], fill=col)
        d.text((x + 122, y + 8), "NSA", font=f(SANS_B, 13), fill=(255, 255, 255))
        d.text((x + 122, y + 24), "NET DOWN", font=f(SANS_B, 9), fill=RED)
        caption(d, x, y + 46, w, "US OUTAGES  •  NSA HIT", (30, 40, 70))


# ---------------- content -------------------------------------------------
LEADS = [
    ("EUROPE • UKRAINE WAR", RED,
     "Ukraine says a Kerch Bridge arch fell into the strait",
     "Drone-and-missile attack, prepared for weeks in seven stages, "
     "Zelensky says. Moscow hits bridges in Kyiv in reply."),
    ("MIDDLE EAST • GULF WAR", RED,
     "Iran fires drones at Kuwait and Bahrain after US strike on Qeshm",
     "Drones at a US base in Kuwait and Bahrain; both say they were "
     "repelled. A tanker is hit in Hormuz; 1 crew missing."),
    ("ASIA • DIPLOMACY", PURPLE,
     "Xi hosts Putin in Shenzhen; Trump lands for Thursday summit",
     "Both denounce sanctions and protectionism. The Quad meets in "
     "Manila; Trump announces a big Philippines trade deal."),
]

CARDS = [
    (4, "US • POLITICS", "alaska", "Peltola flips Alaska; Democrats take the Senate 56–44",
     "First Alaska Native elected to the US Senate, defeating Dan Sullivan."),
    (5, "ISRAEL • POLITICS", "knesset", "Kahana elected Knesset speaker, 66 of 120 votes",
     "A win for PM-elect Eisenkot's camp and a setback for Netanyahu."),
    (6, "MIDDLE EAST • GAZA", "gaza", "Board of Peace faults Israel and Hamas on ceasefire",
     "WHO counts 950,000 displaced on flood-prone ground; cold kills in tents."),
    (7, "AFRICA • HEALTH", "ebola", "Nearly 3 in 4 Ebola children under 5 die in DR Congo",
     "Cases pass 11,000; Bunia, Beni epicentres; vaccines in Phase 2."),
    (8, "AMERICAS • HEALTH", "measles", "US loses measles-elimination status after 26 years",
     "More than 5,400 cases and 10 deaths in 2026."),
    (9, "US • BUSINESS", "nvidia", "Nvidia revenue hits a record $115.8bn",
     "Q4 guidance $130bn; no return for ousted CEO Jensen Huang."),
    (10, "RUSSIA • AIR CRASH", "an12", "Russian An-12 crash in Siberia kills all 19 aboard",
     "Plane came down near Kemerovo; the ministry cites technical failure."),
    (11, "WEST BANK • SANCTIONS", "westbank", "UK and Australia sanction settlement backers",
     "A 72-year-old Palestinian woman is shot dead by settlers in the West Bank."),
    (12, "ASIA • UNREST", "bangladesh", "Paramilitary deployed as unrest spreads in Bangladesh",
     "Blasts and arson in 28 districts; a helper burnt to death."),
    (13, "US • TECHNOLOGY", "outages", "US outages reach the NSA's classified network",
     "Microsoft, FAA, banks hit first; Rubio: no coordinated attack."),
]

ALSO = [
    "Putin not ready for serious peace talks, sources tell NYT",
    "Ukraine seeks 12 more jets; France to send Mirage 2000-5F",
    "Drones over Dnipro injure six; 141 counted, 126 downed",
    "Russian jets off Taiwan; violate Japan airspace off Fukuoka",
    "Ethiopia and Eritrea mass forces along their shared border",
    "Myanmar to review ASEAN ties; ICJ Rohingya ruling due Thu",
    "Turkish court gives Imamoglu 2 more years, a new ban",
    "Thousands protest in Slovakia against Fico, Russia tilt",
    "Italy approves antisemitism law; critics warn on speech",
    "EU acts against Temu; NATO unveils comms strategy",
    "Kalshi halts 'mention' wagers after a CFTC order",
    "House Oversight eyes Trump Jr., Vance and Miller",
    "Fed's Lisa Cook refuses Dec 14 hearing unless Hassett out",
    "White House drops Heidi Overton's FDA nomination",
    "ICE says it will not use ships to deport migrants",
    "New Jersey sues DHS over Delaney Hall inquiry",
    "Students sue Omnilert after chips bag read as a gun",
    "AI models mistake civilians for targets in tests, Vals finds",
    "Anthropic prices IPO at $83, above the $70–78 range",
    "Fed minutes eye inflation; Waller hints at bigger hike",
    "UK inflation 3.6% in Oct; gold falls 2.3% to $3,775",
    "Markets fall: CAC -1.62%, DAX -2.08%, S&P -1.03%",
    "Deutsche Bank leak: 15m documents, Der Spiegel leads",
    "US tightens AI-chip curbs in SE Asia; Beijing warns back",
    "Waymo halts driverless highway rides after CA warning",
    "Voyager 1 is one light-day from Earth, a first",
    "Cambridge Dictionary picks 'Human' as Word of the Year",
    "GTA VI hits shelves tomorrow after a 13-year wait",
    "OpenAI launches GPT-6.2 Astra and Sol, prices lower",
    "Reliance plans 1,600 satellites to rival Starlink",
]

PINS = [(1, 36, 45.3, BLUE), (2, 51.5, 26.5, ORANGE), (3, 114.1, 22.5, PURPLE),
        (4, -150, 64, RED), (5, 34.8, 31.8, ORANGE, 37.5, 34.5),
        (6, 34.5, 31.5, ORANGE), (7, 29.5, 0.5, GREEN), (8, -98, 38, RED),
        (9, -122, 37, RED), (10, 86, 55.4, BLUE), (11, -0.1, 51.5, BLUE),
        (12, 90.4, 23.8, PURPLE), (13, -77, 38.9, RED)]
DOTS = [(39, 56), (32, 51), (-74, 40.7), (13, 51), (1, 49), (22, 53),
        (15, 53), (29, 46), (28.9, 41), (10.7, 59.9), (12, 41), (-1, 52),
        (36, 31), (34, 32), (58.4, 23.6), (85, 20), (79, 30), (130.4, 33.6),
        (-75.7, 45.4), (101.7, 3.1), (100.5, 13.7), (127, 37.5),
        (77.2, 28.6), (36.8, -1.3), (1.2, 6.1), (-72.3, 18.5), (-77, 38.9),
        (149.1, -35.3), (130.8, -12.5), (-122, 37.3), (90, 24), (121, 14.6),
        (114, 22.3), (139, 35.7)]


def build(out="entry.png"):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    mx = 20

    # dark masthead
    d.rectangle([0, 0, W, 76], fill=NAVY)
    d.text((mx, 8), "THE WORLD TODAY  •  ONE DAY, IN ONE PICTURE",
           font=f(SANS_B, 13), fill=GOLD)
    d.text((W - mx - 250, 8), "43 STORIES  •  6 CONTINENTS",
           font=f(SANS_B, 13), fill=(255, 255, 255))
    d.text((mx, 26), "Wednesday 18 November 2026",
           font=f(SERIF_B, 54), fill=(255, 255, 255))

    # red ticker
    d.rectangle([0, 76, W, 98], fill=RED)
    tick = ("KERCH BRIDGE DOWN  •  IRAN DRONES AT KUWAIT & BAHRAIN  •  "
            "XI HOSTS PUTIN IN SHENZHEN  •  PELTOLA FLIPS ALASKA  •  "
            "US LOSES MEASLES-FREE STATUS")
    tick = one_line(d, tick, f(SANS_B, 12), W - 2 * mx)
    d.text((mx, 81), tick, font=f(SANS_B, 12), fill=(255, 255, 255))

    # lead panels
    pw, ph, pg = 316, 130, 8
    panel_kerch(d, mx, 104, pw, ph)
    panel_gulf(d, mx + pw + pg, 104, pw, ph)
    panel_shenzhen(d, mx + 2 * (pw + pg), 104, pw, ph)

    # lead headlines
    y = 238
    for i, (kick, col, head, deck) in enumerate(LEADS):
        x = mx + i * (pw + pg)
        kicker(d, x, y, i + 1, kick, col)
        para(d, x, y + 18, head, f(SERIF_B, 20), pw, max_lines=2)
        para(d, x, y + 64, deck, f(SERIF, 13), pw, max_lines=2, leading=15)
    d.line([mx, 334, W - mx, 334], fill=INK, width=2)

    # cards: 2 rows x 5
    cw, chh, cg = 190, 158, 8
    for idx, (num, kick, kind, head, deck) in enumerate(CARDS):
        row, col = divmod(idx, 5)
        x = mx + col * (cw + cg)
        y = 340 + row * (chh + 4)
        icon(d, x, y, cw, 60, kind)
        kicker(d, x, y + 64, num, kick, RED)
        para(d, x, y + 82, head, f(SERIF_B, 15), cw, max_lines=2)
        para(d, x, y + 118, deck, f(SERIF, 12), cw, max_lines=2)

    # map + also list
    y0 = 672
    d.line([mx, y0 - 6, W - mx, y0 - 6], fill=INK, width=2)
    d.text((mx, y0), "WHERE IT HAPPENED", font=f(SANS_B, 13), fill=RED)
    d.text((mx + 360, y0), "ALSO ON WEDNESDAY 18 NOVEMBER",
           font=f(SANS_B, 13), fill=RED)
    draw_map(d, mx, y0 + 20, 330, 260, PINS, DOTS)
    d.text((mx, y0 + 284), "Pins: stories 1–13  •  dots: 14–43",
           font=f(SANS, 10), fill=(90, 90, 90))
    lx = mx + 360
    colw = 300
    for i, item in enumerate(ALSO):
        col, row = divmod(i, 15)
        x = lx + col * (colw + 12)
        yy = y0 + 20 + row * 17
        n = i + 14
        d.ellipse([x, yy + 1, x + 14, yy + 15], fill=PURPLE)
        d.text((x + 2.5 if n < 10 else x + 0.5, yy + 3), str(n),
               font=f(SANS_B, 8), fill=(255, 255, 255))
        item = one_line(d, item, f(SERIF, 11), colw - 18)
        d.text((x + 19, yy + 1), item, font=f(SERIF, 11), fill=INK)

    # footer
    d.line([mx, 980, W - mx, 980], fill=INK, width=2)
    d.text((mx, 986),
           "Every story here happened or was first reported on Wednesday "
           "18 November 2026. Contested claims are marked as claims.",
           font=f(SANS, 11), fill=INK)
    d.text((mx, 1000),
           "Sources: Reuters, AP, AFP, BBC, NYT, WSJ, Just Security, "
           "Horizon, Open Chronicle — 18 November 2026",
           font=f(SANS, 11), fill=(90, 90, 90))

    img.save(out, optimize=True)
    print(out, img.size, len(open(out, "rb").read()), "bytes")


if __name__ == "__main__":
    build()
