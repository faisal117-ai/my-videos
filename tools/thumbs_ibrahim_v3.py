"""Ibrahim EP 3 film thumbnails in the rule-8 style (19 Nov 2026): a rich split scene that shows the turn.

Left, the hardship: a huge fire at night inside the city walls. Right, the turn: the same place made
"coolness and safety" (Al-Anbiya 21:69), bright and green under a clear sky. The headline adds to the
title instead of repeating it: their order "Burn him" (21:68) and Allah's command. Ordinary people (the crowd
and Namrud's soldiers) are drawn from behind (rule 9); nobody is drawn in or near the fire's centre, and no prophet.
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


def person(x, base, s, robe, skin, rim, kind="man", seed=0):
    """One ordinary man seen from behind: robe, shoulders, neck, head with hair, turban or helmet."""
    rnd = random.Random(seed)
    w, h = 62 * s, 150 * s
    lean = rnd.uniform(-6, 6) * s
    body = (f'<path d="M {x - w/2:.0f} {base} Q {x - w*0.62:.0f} {base - h*0.55:.0f} {x - w*0.42 + lean:.0f} {base - h*0.8:.0f} '
            f'Q {x + lean:.0f} {base - h*0.9:.0f} {x + w*0.42 + lean:.0f} {base - h*0.8:.0f} '
            f'Q {x + w*0.62:.0f} {base - h*0.55:.0f} {x + w/2:.0f} {base} Z" fill="{robe}" stroke="#000" stroke-width="{5*s:.1f}"/>')
    fold = f'<path d="M {x + lean*0.5:.0f} {base - h*0.75:.0f} Q {x - 4*s:.0f} {base - h*0.4:.0f} {x + 3*s:.0f} {base}" stroke="rgba(0,0,0,0.35)" stroke-width="{4*s:.1f}" fill="none"/>'
    rim_l = f'<path d="M {x - w/2:.0f} {base} Q {x - w*0.62:.0f} {base - h*0.55:.0f} {x - w*0.42 + lean:.0f} {base - h*0.8:.0f}" stroke="{rim}" stroke-width="{4*s:.1f}" fill="none" opacity="0.9"/>'
    hx, hy, hr = x + lean, base - h * 0.93, 17 * s
    neck = f'<rect x="{hx - 8*s:.0f}" y="{hy:.0f}" width="{16*s:.0f}" height="{h*0.1:.0f}" fill="{skin}" stroke="#000" stroke-width="{3*s:.1f}"/>'
    head = f'<circle cx="{hx:.0f}" cy="{hy - 4*s:.0f}" r="{hr:.0f}" fill="#2a1a10" stroke="#000" stroke-width="{4*s:.1f}"/>'
    ear = f'<ellipse cx="{hx - hr*0.95:.0f}" cy="{hy - 2*s:.0f}" rx="{4*s:.0f}" ry="{6*s:.0f}" fill="{skin}" stroke="#000" stroke-width="{2*s:.1f}"/>'
    top = ""
    if kind == "soldier":
        top = (f'<path d="M {hx - hr*1.15:.0f} {hy - 2*s:.0f} Q {hx:.0f} {hy - hr*2.4:.0f} {hx + hr*1.15:.0f} {hy - 2*s:.0f} Z" '
               f'fill="#b08a3a" stroke="#000" stroke-width="{4*s:.1f}"/>'
               f'<path d="M {x + w*0.5:.0f} {base - h*0.2:.0f} L {x + w*0.75:.0f} {base - h*1.45:.0f}" stroke="#5a3a1a" stroke-width="{6*s:.1f}"/>'
               f'<path d="M {x + w*0.75:.0f} {base - h*1.45:.0f} l {-7*s:.0f} {22*s:.0f} l {14*s:.0f} 0 Z" fill="#cfd6dc" stroke="#000" stroke-width="{3*s:.1f}"/>')
    elif kind == "turban":
        top = (f'<ellipse cx="{hx:.0f}" cy="{hy - hr*0.9:.0f}" rx="{hr*1.15:.0f}" ry="{hr*0.75:.0f}" fill="{rnd.choice(["#e9e2d0", "#c9b48a", "#a33a2a"])}" '
               f'stroke="#000" stroke-width="{4*s:.1f}"/>')
    arm = ""
    if rnd.random() < 0.35:  # one arm raised, pointing or in shock
        ax = x + (w*0.45 if rnd.random() < 0.5 else -w*0.45)
        arm = (f'<path d="M {ax:.0f} {base - h*0.72:.0f} L {ax + (14*s if ax > x else -14*s):.0f} {base - h*1.15:.0f}" '
               f'stroke="{robe}" stroke-width="{16*s:.1f}" stroke-linecap="round"/>'
               f'<circle cx="{ax + (14*s if ax > x else -14*s):.0f}" cy="{base - h*1.17:.0f}" r="{7*s:.0f}" fill="{skin}" stroke="#000" stroke-width="{3*s:.1f}"/>')
    return arm + body + fold + rim_l + neck + head + ear + top


def crowd(x0, x1, base, s, robes, rim, seed, n):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x = x0 + (i + 0.5) * (x1 - x0) / n + rnd.uniform(-14, 14)
        kind = rnd.choice(["man", "turban", "turban", "soldier"])
        out.append(person(x, base + rnd.uniform(-6, 10), s * rnd.uniform(0.9, 1.08), rnd.choice(robes),
                          rnd.choice(["#c68c5a", "#a8714a", "#d9a271"]), rim, kind, seed * 31 + i))
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
            '<path d="M 60 690 L 600 690 L 560 650 L 100 650 Z" fill="#5a2c12" stroke="#000" stroke-width="8"/>'
            + crowd(-10, 640, 735, 1.35, ["#3a2416", "#4a2a1a", "#2e2a3a", "#5a3020"], "#ff9a3a", 2, 6) + '</g>')
    right = ('<g clip-path="url(#R)"><rect width="1280" height="720" fill="url(#day)"/>'
             '<circle cx="1222" cy="345" r="40" fill="#fff6c8" stroke="#000" stroke-width="8"/>'
             + walls(560, 1300, 560, "#e8c48a", 5) +
             '<path d="M 560 560 Q 900 520 1280 560 L 1280 720 L 560 720 Z" fill="#5ccf5a" stroke="#000" stroke-width="8"/>'
             '<path d="M 560 640 Q 900 600 1280 640 L 1280 720 L 560 720 Z" fill="#3fae45" stroke="#000" stroke-width="8"/>'
             '<circle cx="960" cy="560" r="230" fill="url(#peace)"/>'
             '<path d="M 760 690 L 1160 690 L 1130 650 L 790 650 Z" fill="#8a6a44" stroke="#000" stroke-width="8"/>'
             + flowers(780, 1140, 560, 690, 26, 9)
             + crowd(590, 770, 740, 1.3, ["#7a5a9a", "#3a7ac0", "#b0603a"], "#fff6c8", 7, 2)
             + crowd(1150, 1310, 740, 1.3, ["#5a8a4a", "#c9a46a", "#3a7ac0"], "#fff6c8", 8, 2) + '</g>')
    seam = '<path d="M 700 0 L 580 720" stroke="#000" stroke-width="12"/><path d="M 700 0 L 580 720" stroke="#ffd21f" stroke-width="5"/>'
    return defs + left + right + seam + ring(960, 600, 210, 80)


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
