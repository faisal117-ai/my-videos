"""Ibrahim EP 3 film thumbnails in the rule-8 style (19 Nov 2026): a rich split scene that shows the turn.

Left, the hardship: a huge fire at night inside the city walls. Right, the turn: the same place made
"coolness and safety" (Al-Anbiya 21:69), bright and green under a clear sky. The headline adds to the
title instead of repeating it: their order "Burn him" (21:68) and Allah's command. No person is drawn.
Usage: python3 tools/thumbs_ibrahim_v3.py  -> thumbs/v3-ibrahim-en.jpg, thumbs/v3-ibrahim-ur.jpg
"""
import random
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from thumbs_v2 import HOT, ROOT, flames, page, stars  # noqa: E402
from thumbs_v3 import ring, urdu  # noqa: E402

OUT = ROOT / "thumbs"


def walls(x0, x1, base, col, seed):
    rnd = random.Random(seed)
    out, x = [], x0
    while x < x1:
        w, h = rnd.randint(70, 140), rnd.randint(90, 190)
        out.append(f'<rect x="{x}" y="{base - h}" width="{w}" height="{h}" fill="{col}" stroke="#000" stroke-width="6"/>')
        for k in range(0, w - 10, 26):  # battlements
            out.append(f'<rect x="{x + k}" y="{base - h - 16}" width="14" height="16" fill="{col}" stroke="#000" stroke-width="4"/>')
        x += w
    return "".join(out)


def flowers(x0, x1, y0, y1, n, seed):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        c = rnd.choice(["#ff6fae", "#fff", "#ffd21f", "#ff8a3d"])
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(6, 11):.0f}" fill="{c}" stroke="#000" stroke-width="3"/>'
                   f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="#e8a400"/>')
    return "".join(out)


def scene() -> str:
    defs = ('<defs><linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#12030a"/>'
            '<stop offset="1" stop-color="#4a0c02"/></linearGradient>'
            '<radialGradient id="heat" cx="0.5" cy="0.8" r="0.6"><stop offset="0" stop-color="rgba(255,150,40,0.85)"/>'
            '<stop offset="1" stop-color="rgba(255,90,20,0)"/></radialGradient>'
            '<linearGradient id="day" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3fa0ff"/>'
            '<stop offset="1" stop-color="#d6f1ff"/></linearGradient>'
            '<radialGradient id="peace" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="rgba(255,255,230,0.95)"/>'
            '<stop offset="1" stop-color="rgba(255,255,230,0)"/></radialGradient>'
            '<clipPath id="L"><path d="M 0 0 L 700 0 L 580 720 L 0 720 Z"/></clipPath>'
            '<clipPath id="R"><path d="M 700 0 L 1280 0 L 1280 720 L 580 720 Z"/></clipPath></defs>')
    left = ('<g clip-path="url(#L)"><rect width="1280" height="720" fill="url(#night)"/>' + stars(40, 0, 700, 0, 260, 3) +
            walls(-20, 720, 560, "#3a1a10", 5) + '<rect width="1280" height="720" fill="url(#heat)"/>'
            '<rect y="560" width="1280" height="160" fill="#2a0d05" stroke="#000" stroke-width="8"/>'
            + flames(330, 690, 700, 560, 9, 4, HOT) +
            '<path d="M 60 690 L 600 690 L 560 650 L 100 650 Z" fill="#5a2c12" stroke="#000" stroke-width="8"/></g>')
    right = ('<g clip-path="url(#R)"><rect width="1280" height="720" fill="url(#day)"/>'
             '<circle cx="1222" cy="345" r="40" fill="#fff6c8" stroke="#000" stroke-width="8"/>'
             + walls(560, 1300, 560, "#e8c48a", 5) +
             '<path d="M 560 560 Q 900 520 1280 560 L 1280 720 L 560 720 Z" fill="#5ccf5a" stroke="#000" stroke-width="8"/>'
             '<path d="M 560 640 Q 900 600 1280 640 L 1280 720 L 560 720 Z" fill="#3fae45" stroke="#000" stroke-width="8"/>'
             '<circle cx="960" cy="560" r="230" fill="url(#peace)"/>'
             '<path d="M 760 690 L 1160 690 L 1130 650 L 790 650 Z" fill="#8a6a44" stroke="#000" stroke-width="8"/>'
             + flowers(780, 1140, 560, 690, 26, 9) + '</g>')
    seam = '<path d="M 700 0 L 580 720" stroke="#000" stroke-width="12"/><path d="M 700 0 L 580 720" stroke="#ffd21f" stroke-width="5"/>'
    return defs + left + right + seam + ring(960, 625, 230, 95)


def en() -> str:
    text = ('<div class="t" style="left:40px;width:560px;text-align:center;top:70px;font-size:104px">“Burn<br>him!”…</div>'
            '<div class="t y" style="left:690px;width:560px;text-align:center;top:70px;font-size:88px">…Allah said:<br>“Be cool”</div>')
    return page(scene(), text, "PROPHET IBRAHIM (AS) · EP 3").replace('<div class="chip">', '<div class="chip" style="top:auto;bottom:26px">')


def ur() -> str:
    text = ('<div class="t u" dir="rtl" style="left:30px;width:580px;text-align:center;top:40px;font-size:92px">اسے جلا دو!…</div>'
            '<div class="t u y" dir="rtl" style="left:670px;width:590px;text-align:center;top:40px;font-size:74px">…اللہ نے آگ<br>ٹھنڈی کر دی</div>')
    return urdu(page(scene(), text, "حضرت ابراہیم علیہ السلام · EP 3")).replace(
        '<div class="chip">', '<div class="chip" style="top:auto;bottom:26px;font-family:U;letter-spacing:0">')


if __name__ == "__main__":
    for k, fn in {"v3-ibrahim-en": en, "v3-ibrahim-ur": ur}.items():
        h = OUT / f"{k}.html"
        h.write_text(fn(), encoding="utf-8")
        subprocess.run(["node", str(ROOT / "tools/screenshot.js"), str(h), str(OUT / f"{k}.jpg")], check=True)
        print(k)
