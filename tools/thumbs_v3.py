"""Third-generation film thumbnails (17–18 Nov 2026, after the Miracle of Islam research).

Layout: one full, bright scene; a bold two-line headline that adds to the title (never repeats it);
one red arrow or circle on the key object; honest words, no news badges. No prophet, righteous woman,
angel or person is ever drawn.
Usage: python3 tools/thumbs_v3.py  -> thumbs/<id>.html and thumbs/<id>.jpg (1280x720)
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from thumbs_v2 import CROWN, ROOT, page, stars, yusuf_dream, yusuf_split  # noqa: E402

OUT = ROOT / "thumbs"
URDU_FONT = (ROOT / "long/02-musa/assets/fonts/noto-nastaliq-urdu-arabic-400-normal.woff2").as_uri()
URDU_CSS = ('@font-face { font-family: U; src: url("' + URDU_FONT + '"); }'
            ' .u { font-family: U; text-transform:none; line-height:1.8; letter-spacing:0; -webkit-text-stroke: 12px #000; }')


def urdu(h: str) -> str:
    return h.replace("</style>", URDU_CSS + "</style>")


def ring(cx, cy, rx, ry):
    """The red circle that marks the key object (black outline so it reads on any background)."""
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#000" stroke-width="22"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#ff2a1f" stroke-width="12"/>')


def arrow(x1, y1, x2, y2):
    """A thick red arrow from (x1,y1) to the tip (x2,y2)."""
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 70 * math.cos(a), y2 - 70 * math.sin(a)
    l = (hx + 46 * math.cos(a + math.pi / 2), hy + 46 * math.sin(a + math.pi / 2))
    r = (hx + 46 * math.cos(a - math.pi / 2), hy + 46 * math.sin(a - math.pi / 2))
    head = f'M {x2} {y2} L {l[0]:.0f} {l[1]:.0f} L {r[0]:.0f} {r[1]:.0f} Z'
    return (f'<path d="M {x1} {y1} L {hx:.0f} {hy:.0f}" stroke="#000" stroke-width="40" stroke-linecap="round"/>'
            f'<path d="{head}" fill="#000" stroke="#000" stroke-width="16" stroke-linejoin="round"/>'
            f'<path d="M {x1} {y1} L {hx:.0f} {hy:.0f}" stroke="#ff2a1f" stroke-width="24" stroke-linecap="round"/>'
            f'<path d="{head}" fill="#ff2a1f"/>')


def headline(top_line: str, bottom_line: str, top=40, size=(86, 104), right=None) -> str:
    pos = f"right:{right}px;text-align:right" if right is not None else "left:0;right:0;text-align:center"
    return (f'<div class="t u" dir="rtl" style="{pos};top:{top}px;font-size:{size[0]}px;white-space:nowrap">{top_line}</div>'
            f'<div class="t u y" dir="rtl" style="{pos};top:{top + int(size[0] * 1.55)}px;font-size:{size[1]}px;white-space:nowrap">{bottom_line}</div>')


def yusuf_ur_day_well() -> str:
    """A: the well in bright daylight; the arrow points into it; the crown shines above it."""
    defs = ('<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3fa0ff"/>'
            '<stop offset="1" stop-color="#bfe6ff"/></linearGradient>'
            '<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="rgba(255,226,90,0.95)"/>'
            '<stop offset="1" stop-color="rgba(255,226,90,0)"/></radialGradient>'
            '<linearGradient id="stone" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a6a44"/>'
            '<stop offset="0.5" stop-color="#c79a62"/><stop offset="1" stop-color="#7a5a36"/></linearGradient></defs>')
    dunes = ('<path d="M 0 520 Q 300 450 620 510 T 1280 490 L 1280 720 L 0 720 Z" fill="#f2c46b" stroke="#000" stroke-width="8"/>'
             '<path d="M 0 610 Q 400 560 820 615 T 1280 600 L 1280 720 L 0 720 Z" fill="#e3a84a" stroke="#000" stroke-width="8"/>')
    well = ('<g stroke="#000" stroke-width="10">'
            '<rect x="770" y="430" width="300" height="190" fill="url(#stone)"/>'
            '<ellipse cx="920" cy="430" rx="150" ry="42" fill="#c79a62"/>'
            '<ellipse cx="920" cy="430" rx="118" ry="28" fill="#0a0603"/>'
            '<path d="M 790 430 L 790 290 L 1050 290 L 1050 430" fill="none" stroke="#6b4a2a" stroke-width="20"/>'
            '<path d="M 770 290 L 1070 290" stroke-width="12"/></g>'
            '<path d="M 920 290 L 920 410" stroke="#c89a5a" stroke-width="8"/>'
            '<path d="M 770 500 H 1070 M 770 560 H 1070 M 850 430 V 620 M 990 430 V 620" stroke="#5a4026" stroke-width="5"/>')
    crown = ('<circle cx="920" cy="175" r="150" fill="url(#glow)"/>'
             '<g transform="translate(920,180) scale(0.5)">' + CROWN + '</g>')
    svg = (defs + '<rect width="1280" height="720" fill="url(#sky)"/>'
           '<circle cx="1180" cy="110" r="60" fill="#fff6c8" stroke="#000" stroke-width="8"/>'
           + dunes + well + crown + arrow(560, 600, 790, 445))
    text = headline("بھائیوں نے کنویں میں پھینکا…", "…اللہ نے بادشاہ بنا دیا", top=70, size=(62, 76), right=590)
    return urdu(page(svg, text, "HAZRAT YUSUF AS · EP 2"))


def yusuf_ur_prison_throne() -> str:
    """B: the dark well on the left, golden throne side on the right; the circle marks the crown."""
    h = yusuf_split()
    h = h.replace('</svg>', ring(960, 455, 220, 150) + '</svg>', 1)
    a = h.index('<div class="t"'); b = h.rindex('<div class="chip">')
    text = ('<div class="t u" dir="rtl" style="left:40px;width:560px;text-align:center;top:70px;font-size:96px">کنویں سے…</div>'
            '<div class="t u y" dir="rtl" style="left:680px;width:560px;text-align:center;top:70px;font-size:110px">…تخت تک</div>')
    return urdu(h[:a] + text + h[b:]).replace("PROPHET YUSUF (AS)", "HAZRAT YUSUF AS · EP 2")


def yusuf_ur_eleven_stars() -> str:
    """C: the dream; the circle marks the eleven stars bowing with the sun and the moon."""
    h = yusuf_dream()
    h = h.replace('</svg>', ring(640, 300, 560, 150) + '</svg>', 1)
    a = h.index('<div class="t"'); b = h.rindex('<div class="chip">')
    text = headline("گیارہ ستارے، سورج اور چاند…", "…سب سجدے میں!", top=448, size=(56, 74))
    return urdu(h[:a] + text + h[b:]).replace("PROPHET YUSUF (AS)", "HAZRAT YUSUF AS · EP 2")


THUMBS = {"v3-yusuf-ur-a-well": yusuf_ur_day_well,
          "v3-yusuf-ur-b-throne": yusuf_ur_prison_throne,
          "v3-yusuf-ur-c-stars": yusuf_ur_eleven_stars}

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for k, fn in THUMBS.items():
        h = OUT / f"{k}.html"
        h.write_text(fn(), encoding="utf-8")
        subprocess.run(["node", str(ROOT / "tools/screenshot.js"), str(h), str(OUT / f"{k}.jpg")], check=True)
        print(k)
