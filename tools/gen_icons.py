#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成小程序用到的线性图标（PNG），避免引入图标字体。

用法：python tools/gen_icons.py
输出：miniprogram/assets/icons/*.png（81x81，透明背景）
"""
import os

from PIL import Image, ImageDraw

SS = 8               # 超采样倍数
SIZE = 81            # 输出尺寸（微信 tabBar 推荐 81x81）
FONT = None

NORMAL = (138, 148, 146, 255)   # #8A9492
ACTIVE = (15, 107, 92, 255)     # #0F6B5C
MUTED = (147, 157, 154, 255)    # #939D9A

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "miniprogram", "assets", "icons")


def canvas():
    return Image.new("RGBA", (SIZE * SS, SIZE * SS), (0, 0, 0, 0))


def pt(x, y):
    return (x * SS, y * SS)


def dot(d, p, r, color):
    d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=color)


def stroke(d, points, color, width):
    w = width * SS
    coords = [pt(x, y) for x, y in points]
    d.line(coords, fill=color, width=int(w), joint="curve")
    for end in (coords[0], coords[-1]):
        dot(d, end, w / 2.0, color)


def ring(d, cx, cy, r, color, width):
    d.ellipse([pt(cx - r, cy - r), pt(cx + r, cy + r)],
              outline=color, width=int(width * SS))


def disc(d, cx, cy, r, color):
    d.ellipse([pt(cx - r, cy - r), pt(cx + r, cy + r)], fill=color)


def icon_home(d, c):
    stroke(d, [(15, 39), (40, 16), (65, 39)], c, 4)
    stroke(d, [(22, 35), (22, 64), (58, 64), (58, 35)], c, 4)
    stroke(d, [(34, 64), (34, 50), (46, 50), (46, 64)], c, 4)


def icon_triage(d, c):
    ring(d, 40, 40, 25, c, 4)
    stroke(d, [(40, 28), (40, 52)], c, 4)
    stroke(d, [(28, 40), (52, 40)], c, 4)


def icon_record(d, c):
    stroke(d, [(23, 24), (58, 24)], c, 4)
    stroke(d, [(23, 40), (58, 40)], c, 4)
    stroke(d, [(23, 56), (44, 56)], c, 4)


def icon_me(d, c):
    ring(d, 40, 29, 11, c, 4)
    d.arc([pt(21, 44), pt(59, 82)], 195, 345, fill=c, width=4 * SS)


def icon_search(d, c):
    ring(d, 36, 36, 17, c, 4.5)
    stroke(d, [(48, 48), (62, 62)], c, 4.5)


def icon_calendar(d, c):
    d.rounded_rectangle([pt(17, 21), pt(63, 65)], radius=7 * SS,
                        outline=c, width=int(4 * SS))
    stroke(d, [(17, 33), (63, 33)], c, 4)
    stroke(d, [(29, 12), (29, 24)], c, 4)
    stroke(d, [(51, 12), (51, 24)], c, 4)
    for x in (30, 40, 50):
        disc(d, x, 47, 3, c)


def icon_clock(d, c):
    ring(d, 40, 40, 25, c, 4)
    stroke(d, [(40, 24), (40, 41)], c, 4)
    stroke(d, [(40, 41), (52, 47)], c, 4)


def icon_pin(d, c):
    disc(d, 40, 31, 15, c)
    d.polygon([pt(26.5, 37), pt(53.5, 37), pt(40, 68)], fill=c)
    disc(d, 40, 31, 6, (0, 0, 0, 0))


ICONS = {
    "home": icon_home,
    "triage": icon_triage,
    "record": icon_record,
    "me": icon_me,
    "search": icon_search,
    "calendar": icon_calendar,
    "clock": icon_clock,
    "pin": icon_pin,
}


def render(name, color):
    img = canvas()
    draw = ImageDraw.Draw(img)
    ICONS[name](draw, color)
    return img.resize((SIZE, SIZE), Image.LANCZOS)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    tab_icons = ("home", "triage", "record", "me")
    for name in tab_icons:
        render(name, NORMAL).save(os.path.join(OUT_DIR, "tab-%s.png" % name), optimize=True)
        render(name, ACTIVE).save(os.path.join(OUT_DIR, "tab-%s-on.png" % name), optimize=True)
    for name in ("search", "calendar", "clock", "pin"):
        render(name, MUTED).save(os.path.join(OUT_DIR, "ic-%s.png" % name), optimize=True)
    print("icons written to %s" % os.path.normpath(OUT_DIR))


if __name__ == "__main__":
    main()
