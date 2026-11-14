"""Second-generation film thumbnails: bright, one big image, 3-5 bold words.
Usage: python3 tools/thumbs_v2.py  -> thumbs/<id>.html and thumbs/<id>.jpg (1280x720)
No prophet, righteous woman or angel is ever drawn; people never appear."""
import math
import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "thumbs"
CSS = """
@font-face { font-family: K; src: url("file:///usr/share/fonts/opentype/inter/Inter-Black.otf"); }
html,body { margin:0; width:1280px; height:720px; overflow:hidden; background:#000; }
svg.bg { position:absolute; inset:0; }
.t { position:absolute; font-family:K; text-transform:uppercase; color:#fff; line-height:0.92;
  letter-spacing:-0.01em; -webkit-text-stroke: 14px #000; paint-order: stroke fill;
  text-shadow: 0 8px 24px rgba(0,0,0,0.8); }
.y { color:#ffd21f; } .b { color:#8fe3ff; } .r { color:#ff4a3a; }
.chip { position:absolute; top:26px; left:30px; font-family:K; font-size:30px; letter-spacing:0.06em;
  color:#111; background:#ffd21f; border:5px solid #000; border-radius:14px; padding:6px 16px; }
"""


def page(svg: str, text: str, chip: str) -> str:
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<svg class="bg" width="1280" height="720" viewBox="0 0 1280 720">{svg}</svg>'
            f'{text}<div class="chip">{chip}</div></body></html>')


def stars(n, x0, x1, y0, y1, seed, r=(1.0, 2.6)):
    rnd = random.Random(seed)
    return "".join(f'<circle cx="{rnd.uniform(x0,x1):.0f}" cy="{rnd.uniform(y0,y1):.0f}" '
                   f'r="{rnd.uniform(*r):.1f}" fill="#fff" opacity="{rnd.uniform(.5,1):.2f}"/>' for _ in range(n))


CROWN = ('<path d="M -150 60 L -170 -80 L -85 -10 L 0 -120 L 85 -10 L 170 -80 L 150 60 Z" fill="#ffd21f" '
         'stroke="#000" stroke-width="12" stroke-linejoin="round"/>'
         '<rect x="-155" y="55" width="310" height="44" rx="8" fill="#e8a400" stroke="#000" stroke-width="12"/>'
         '<circle cx="0" cy="-120" r="20" fill="#ff4a3a" stroke="#000" stroke-width="8"/>'
         '<circle cx="-170" cy="-80" r="16" fill="#8fe3ff" stroke="#000" stroke-width="8"/>'
         '<circle cx="170" cy="-80" r="16" fill="#8fe3ff" stroke="#000" stroke-width="8"/>')


def star5(cx, cy, r, fill="#fff2a8"):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append(f"{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'


# ---------------- Yusuf ----------------
def yusuf_well():
    rings = "".join(f'<circle cx="840" cy="330" r="{r}" fill="{c}"/>' for r, c in
                    [(1100, "#0c0805"), (760, "#21160d"), (600, "#2f2014"), (470, "#3d2a1a"), (360, "#4a331f")])
    bricks = "".join(f'<path d="M {840+260*math.cos(a):.0f} {330+260*math.sin(a):.0f} L {840+560*math.cos(a):.0f} {330+560*math.sin(a):.0f}" '
                     f'stroke="#140d07" stroke-width="6"/>' for a in [i*math.pi/9 for i in range(18)])
    sky = ('<defs><radialGradient id="sk" cx="0.5" cy="0.45" r="0.6"><stop offset="0" stop-color="#ffffff"/>'
           '<stop offset="0.5" stop-color="#bfe8ff"/><stop offset="1" stop-color="#4aa8e8"/></radialGradient>'
           '<radialGradient id="gl" cx="0.66" cy="0.46" r="0.5"><stop offset="0" stop-color="rgba(255,250,220,0.55)"/>'
           '<stop offset="1" stop-color="rgba(255,250,220,0)"/></radialGradient></defs>')
    svg = (sky + rings + bricks + '<circle cx="840" cy="330" r="250" fill="url(#sk)" stroke="#000" stroke-width="10"/>'
           '<path d="M 1010 80 Q 1005 400 1020 720" stroke="#c89a5a" stroke-width="16" fill="none"/>'
           '<path d="M 1010 80 Q 1005 400 1020 720" stroke="#000" stroke-width="4" fill="none" stroke-dasharray="14 18"/>'
           '<rect width="1280" height="720" fill="url(#gl)"/>'
           '<g transform="translate(1110,610) scale(0.55)">' + CROWN + '</g>')
    text = ('<div class="t" style="left:40px;top:110px;font-size:138px">Thrown<br>in a well…</div>'
            '<div class="t y" style="left:40px;top:470px;font-size:128px">…became<br>king</div>')
    return page(svg, text, "PROPHET YUSUF (AS)")


def yusuf_dream():
    defs = ('<defs><radialGradient id="n" cx="0.5" cy="0.35" r="0.8"><stop offset="0" stop-color="#2a3a9a"/>'
            '<stop offset="1" stop-color="#070a26"/></radialGradient>'
            '<radialGradient id="s" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#fff7c0"/>'
            '<stop offset="0.6" stop-color="#ffc21f"/><stop offset="1" stop-color="#ff8a00"/></radialGradient>'
            '<radialGradient id="h" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="rgba(255,200,60,0.6)"/>'
            '<stop offset="1" stop-color="rgba(255,200,60,0)"/></radialGradient></defs>')
    eleven = "".join(star5(640 + 470*math.cos(a), 470 + 300*math.sin(a), 38)
                     for a in [math.pi + (i+0.5)*math.pi/11 for i in range(11)])
    svg = (defs + '<rect width="1280" height="720" fill="url(#n)"/>' + stars(140, 0, 1280, 0, 720, 3) +
           '<circle cx="250" cy="560" r="220" fill="url(#h)"/><circle cx="250" cy="560" r="105" fill="url(#s)" stroke="#000" stroke-width="8"/>'
           '<path d="M 1050 470 a 100 100 0 1 0 60 160 a 80 80 0 1 1 -60 -160 Z" fill="#f2f6ff" stroke="#000" stroke-width="8"/>'
           + eleven)
    text = ('<div class="t" style="left:0;right:0;text-align:center;top:285px;font-size:118px">11 stars<br>'
            '<span class="y">bowed to him…</span></div>')
    return page(svg, text, "PROPHET YUSUF (AS)")


def yusuf_split():
    svg = ('<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff0b0"/>'
           '<stop offset="1" stop-color="#ffb000"/></linearGradient></defs>'
           '<rect width="640" height="720" fill="#0e1424"/>' + stars(60, 0, 640, 0, 360, 9) +
           '<rect x="640" width="640" height="720" fill="url(#g)"/>'
           '<g stroke="#000" stroke-width="10"><rect x="150" y="430" width="340" height="230" fill="#5a5a66"/>'
           '<ellipse cx="320" cy="430" rx="170" ry="48" fill="#000"/>'
           '<path d="M 170 430 L 170 250 L 470 250 L 470 430" fill="none" stroke="#6b4a2a" stroke-width="18"/></g>'
           '<path d="M 150 500 H 490 M 150 570 H 490 M 260 430 V 660 M 380 430 V 660" stroke="#3a3a44" stroke-width="6"/>'
           '<g transform="translate(960,470)">' + CROWN.replace("-150 60", "-150 60") + '</g>'
           '<path d="M 560 380 L 720 380 L 720 330 L 810 410 L 720 490 L 720 440 L 560 440 Z" fill="#fff" stroke="#000" stroke-width="10"/>')
    text = ('<div class="t" style="left:30px;top:95px;font-size:112px">From a<br>well…</div>'
            '<div class="t" style="left:700px;top:95px;font-size:112px;color:#fff">…to a<br><span class="r">throne</span></div>')
    return page(svg, text, "PROPHET YUSUF (AS)")


# ---------------- Musa ----------------
def musa_sea():
    defs = ('<defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fe6ff"/>'
            '<stop offset="0.4" stop-color="#1e8ad6"/><stop offset="1" stop-color="#062a5c"/></linearGradient>'
            '<linearGradient id="p" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff3c4"/>'
            '<stop offset="1" stop-color="#d89a40"/></linearGradient>'
            '<radialGradient id="l" cx="0.5" cy="0.35" r="0.4"><stop offset="0" stop-color="rgba(255,255,230,0.95)"/>'
            '<stop offset="1" stop-color="rgba(255,255,230,0)"/></radialGradient></defs>')
    svg = (defs + '<rect width="1280" height="720" fill="#ffd27a"/><rect width="1280" height="720" fill="url(#l)"/>'
           '<path d="M 560 300 L 720 300 L 1100 720 L 180 720 Z" fill="url(#p)" stroke="#000" stroke-width="8"/>'
           '<path d="M 0 40 Q 300 0 560 90 L 560 300 L 180 720 L 0 720 Z" fill="url(#w)" stroke="#000" stroke-width="10"/>'
           '<path d="M 1280 40 Q 980 0 720 90 L 720 300 L 1100 720 L 1280 720 Z" fill="url(#w)" stroke="#000" stroke-width="10"/>'
           '<path d="M 0 40 Q 300 0 560 90 L 560 120 Q 300 40 0 80 Z" fill="#fff"/>'
           '<path d="M 1280 40 Q 980 0 720 90 L 720 120 Q 980 40 1280 80 Z" fill="#fff"/>'
           '<g stroke="#bff0ff" stroke-width="6" fill="none" opacity="0.7"><path d="M 60 250 Q 250 230 420 300"/>'
           '<path d="M 40 430 Q 200 410 330 470"/><path d="M 1220 250 Q 1030 230 860 300"/><path d="M 1240 430 Q 1080 410 950 470"/></g>')
    text = ('<div class="t" style="left:0;right:0;text-align:center;top:150px;font-size:150px">The sea<br>'
            '<span class="y">split</span></div>')
    return page(svg, text, "PROPHET MUSA (AS)")


def musa_pharaoh():
    defs = ('<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a0e2e"/>'
            '<stop offset="1" stop-color="#7a2a3a"/></linearGradient>'
            '<linearGradient id="w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b9ee8"/>'
            '<stop offset="1" stop-color="#04203f"/></linearGradient></defs>')
    stripes = "".join(f'<path d="M {-150+i*0} {-60+i*40} " />' for i in range(0))
    nemes = ('<defs><clipPath id="nm"><path d="M -170 260 L -150 -40 Q -140 -170 0 -190 Q 140 -170 150 -40 L 170 260 L 95 260 L 85 10 L -85 10 L -95 260 Z"/></clipPath></defs>'
             '<g transform="translate(960,500) rotate(-12)">'
             '<g clip-path="url(#nm)">' + "".join(
                 f'<rect x="-200" y="{-200+i*36}" width="400" height="36" fill="{c}"/>'
                 for i, c in enumerate(["#ffd21f", "#1f3fae"] * 7)) + '</g>'
             '<path d="M -170 260 L -150 -40 Q -140 -170 0 -190 Q 140 -170 150 -40 L 170 260 L 95 260 L 85 10 L -85 10 L -95 260 Z" '
             'fill="none" stroke="#000" stroke-width="12" stroke-linejoin="round"/>'
             '<path d="M -150 -40 Q 0 -80 150 -40" stroke="#000" stroke-width="10" fill="none"/>'
             '<path d="M -18 -175 Q -10 -240 18 -232 Q 34 -214 10 -200 L 14 -170 Z" fill="#ffd21f" stroke="#000" stroke-width="8"/></g>')
    svg = (defs + '<rect width="1280" height="720" fill="url(#sk)"/>' + nemes +
           '<path d="M 0 560 Q 160 420 330 520 Q 480 600 620 470 Q 760 380 880 560 Q 1000 640 1120 470 Q 1210 380 1280 450 L 1280 720 L 0 720 Z" '
           'fill="url(#w)" stroke="#000" stroke-width="10"/>'
           '<path d="M 0 560 Q 160 420 330 520 Q 480 600 620 470 Q 760 380 880 560 Q 1000 640 1120 470 Q 1210 380 1280 450" '
           'stroke="#fff" stroke-width="14" fill="none"/>'
           '<g fill="#fff">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in
                                       [(610, 450, 14), (640, 430, 9), (870, 540, 12), (1110, 450, 13), (330, 500, 10)]) + '</g>')
    text = ('<div class="t" style="left:40px;top:100px;font-size:124px">Pharaoh\'s<br>last words…</div>')
    return page(svg, text, "PROPHET MUSA (AS)")


def musa_basket():
    defs = ('<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1a3a"/>'
            '<stop offset="1" stop-color="#2d6fa8"/></linearGradient>'
            '<radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="rgba(255,220,120,0.9)"/>'
            '<stop offset="1" stop-color="rgba(255,220,120,0)"/></radialGradient></defs>')
    reeds = "".join(f'<path d="M {x} 720 Q {x+8} {560-h/2} {x+18} {560-h}" stroke="#1d3a1a" stroke-width="10" fill="none"/>'
                    for x, h in [(30, 200), (70, 260), (110, 180), (1150, 230), (1190, 290), (1235, 200)])
    svg = (defs + '<rect width="1280" height="720" fill="url(#sk)"/>' + stars(70, 0, 1280, 0, 300, 5) +
           '<circle cx="1130" cy="330" r="50" fill="#f4f6ff" stroke="#000" stroke-width="8"/>'
           '<path d="M 0 420 H 1280 V 720 H 0 Z" fill="#0d4f86"/>'
           '<g stroke="#5fb4ee" stroke-width="7" fill="none"><path d="M 80 480 H 330"/><path d="M 900 470 H 1180"/>'
           '<path d="M 200 600 H 480"/><path d="M 760 640 H 1080"/></g>'
           '<circle cx="640" cy="520" r="230" fill="url(#g)"/>'
           '<g transform="translate(640,520)" stroke="#000" stroke-width="10" stroke-linejoin="round">'
           '<path d="M -170 -20 Q 0 20 170 -20 L 140 70 Q 0 100 -140 70 Z" fill="#c8862f"/>'
           '<path d="M -150 -18 Q 0 -110 150 -18 Q 0 10 -150 -18 Z" fill="#f4e2b8"/>'
           '<path d="M -150 20 Q 0 50 150 20 M -145 45 Q 0 75 145 45" stroke="#7a4a14" stroke-width="7" fill="none"/></g>'
           + reeds)
    text = ('<div class="t" style="left:0;right:0;text-align:center;top:100px;font-size:116px">A baby in<br>'
            '<span class="y">the river…</span></div>')
    return page(svg, text, "PROPHET MUSA (AS)")


# ---------------- Ibrahim ----------------
def flames(cx, base, w, h, n, seed):
    rnd = random.Random(seed)
    out = []
    for layer, col in [(1.0, "#d81e05"), (0.78, "#ff6a00"), (0.55, "#ffb000"), (0.32, "#fff0a0")]:
        for i in range(n):
            x = cx - w/2 + (i + 0.5) * w / n + rnd.uniform(-12, 12)
            fh = h * layer * rnd.uniform(0.6, 1.0)
            fw = w / n * 0.9 * (0.6 + layer * 0.5)
            out.append(f'<path d="M {x-fw:.0f} {base} Q {x-fw*0.6:.0f} {base-fh*0.5:.0f} {x:.0f} {base-fh:.0f} '
                       f'Q {x+fw*0.6:.0f} {base-fh*0.5:.0f} {x+fw:.0f} {base} Z" fill="{col}"/>')
    return "".join(out)


def ibrahim_fire():
    defs = ('<defs><radialGradient id="c" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffffff"/>'
            '<stop offset="0.45" stop-color="#bdf1ff"/><stop offset="1" stop-color="rgba(120,220,255,0)"/></radialGradient></defs>')
    flowers = "".join(f'<g transform="translate({x},{y})"><circle r="15" fill="{c}" stroke="#000" stroke-width="4"/>'
                      f'<circle r="6" fill="#ffd21f"/></g>' for x, y, c in
                      [(560, 640, "#ff7ab8"), (600, 670, "#ffffff"), (650, 650, "#ff7ab8"), (700, 672, "#ffffff"), (735, 640, "#ff7ab8")])
    svg = (defs + '<rect width="1280" height="720" fill="#2a0600"/>' + flames(640, 720, 1400, 700, 16, 4) +
           '<circle cx="645" cy="560" r="250" fill="url(#c)"/>'
           '<path d="M 500 720 Q 520 650 645 640 Q 770 650 790 720 Z" fill="#3fbf5a" stroke="#000" stroke-width="8"/>' + flowers)
    text = ('<div class="t" style="left:0;right:0;text-align:center;top:95px;font-size:118px">Thrown into fire…<br>'
            '<span class="b">it became cool</span></div>')
    return page(svg, text, "PROPHET IBRAHIM (AS)")


def ibrahim_idols():
    def idol(x, s, broken=False, tilt=0):
        body = (f'<g transform="translate({x},640) rotate({tilt}) scale({s})" stroke="#000" stroke-width="{10/s:.1f}" stroke-linejoin="round">'
                '<rect x="-60" y="-40" width="120" height="40" fill="#8a7a66"/>'
                '<path d="M -45 -40 L -50 -230 L 50 -230 L 45 -40 Z" fill="#b8a688"/>'
                '<path d="M -40 -230 L -35 -330 Q 0 -360 35 -330 L 40 -230 Z" fill="#c9b796"/>'
                '<rect x="-24" y="-300" width="16" height="10" fill="#000"/><rect x="8" y="-300" width="16" height="10" fill="#000"/></g>')
        if broken:
            body = (f'<g transform="translate({x},640) scale({s})" stroke="#000" stroke-width="{10/s:.1f}" stroke-linejoin="round">'
                    '<rect x="-60" y="-40" width="120" height="40" fill="#8a7a66"/>'
                    '<path d="M -45 -40 L -48 -120 L -10 -150 L 15 -110 L 46 -140 L 45 -40 Z" fill="#b8a688"/></g>'
                    f'<g transform="translate({x+70*s},690) rotate(80) scale({s*0.8})" stroke="#000" stroke-width="10">'
                    '<path d="M -40 -230 L -35 -330 Q 0 -360 35 -330 L 40 -230 Z" fill="#c9b796"/></g>')
        return body
    axe = ('<g transform="translate(700,250) rotate(28)" stroke="#000" stroke-width="10" stroke-linejoin="round">'
           '<rect x="-10" y="-30" width="20" height="300" fill="#7a4a1c"/>'
           '<path d="M 10 -30 Q 110 -60 120 40 Q 70 20 10 40 Z" fill="#d8dde6"/></g>')
    svg = ('<defs><radialGradient id="t" cx="0.5" cy="0.3" r="0.8"><stop offset="0" stop-color="#ffcf7a"/>'
           '<stop offset="1" stop-color="#7a3a12"/></radialGradient></defs>'
           '<rect width="1280" height="720" fill="url(#t)"/><rect y="640" width="1280" height="80" fill="#4a2a10"/>'
           + idol(150, 0.8, True) + idol(340, 0.9, True) + idol(940, 0.9, True) + idol(1130, 0.8, True)
           + idol(640, 1.6) + axe +
           '<g fill="#8a7a66" stroke="#000" stroke-width="5">' + "".join(
               f'<polygon points="{x},{y} {x+22},{y-14} {x+30},{y+8}"/>' for x, y in
               [(260, 660), (430, 670), (820, 662), (1020, 672), (520, 676)]) + '</g>')
    text = ('<div class="t" style="left:30px;top:100px;font-size:104px">He broke<br>every idol…</div>'
            '<div class="t y" style="left:840px;top:110px;font-size:80px;text-align:right">…except<br>one</div>')
    return page(svg, text, "PROPHET IBRAHIM (AS)")


def ibrahim_kaaba():
    svg = ('<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a1440"/>'
           '<stop offset="1" stop-color="#d77a3a"/></linearGradient>'
           '<radialGradient id="g" cx="0.5" cy="0.6" r="0.5"><stop offset="0" stop-color="rgba(255,225,150,0.9)"/>'
           '<stop offset="1" stop-color="rgba(255,225,150,0)"/></radialGradient></defs>'
           '<rect width="1280" height="720" fill="url(#sk)"/>' + stars(90, 0, 1280, 0, 330, 11) +
           '<path d="M 0 600 Q 200 470 420 560 Q 640 440 860 560 Q 1080 470 1280 600 L 1280 720 L 0 720 Z" fill="#5a3418"/>'
           '<circle cx="640" cy="470" r="330" fill="url(#g)"/>'
           '<g stroke="#000" stroke-width="10" stroke-linejoin="round">'
           '<path d="M 470 340 L 640 300 L 810 340 L 810 620 L 640 680 L 470 620 Z" fill="#141414"/>'
           '<path d="M 640 300 L 640 680" stroke="#2a2a2a" stroke-width="6"/>'
           '<path d="M 470 400 L 640 365 L 810 400 L 810 425 L 640 390 L 470 425 Z" fill="#e8b830"/></g>'
           '<path d="M 0 720 L 0 650 Q 640 600 1280 650 L 1280 720 Z" fill="#c9a26a" stroke="#000" stroke-width="8"/>')
    text = ('<div class="t" style="left:0;right:0;text-align:center;top:95px;font-size:118px">Who built<br>'
            '<span class="y">the Kaaba?</span></div>')
    return page(svg, text, "PROPHET IBRAHIM (AS)")


def ibrahim_fire_ur():
    h = ibrahim_fire()
    font = (ROOT / "long/02-musa/assets/fonts/noto-nastaliq-urdu-arabic-400-normal.woff2").as_uri()
    h = h.replace("</style>", '@font-face { font-family: U; src: url("' + font + '"); }'
                  ' .u { font-family: U; text-transform:none; line-height:1.9; letter-spacing:0; -webkit-text-stroke: 12px #000; }</style>')
    start = h.index('<div class="t"'); end = h.index('</div>', start) + 6
    return (h[:start] + '<div class="t u" dir="rtl" style="left:0;right:0;text-align:center;top:70px;font-size:84px">'
            'آگ میں پھینکا گیا…<br><span class="b">آگ ٹھنڈی ہو گئی</span></div>' + h[end:]).replace("PROPHET IBRAHIM (AS)", "HAZRAT IBRAHIM AS")


def three(fn, words, cls="", top=60, size=150):
    """Same art, only three words (yt-package rule: max 3 words, never repeating the title)."""
    h = fn()
    start = h.index('<div class="t'); end = h.rindex('<div class="chip">')
    return (h[:start] + f'<div class="t {cls}" style="left:0;right:0;text-align:center;top:{top}px;font-size:{size}px">{words}</div>'
            + h[end:])


def musa_old_bold():
    """The user's preferred original Musa art, with three bold words instead of the thin serif lines."""
    h = (ROOT / "long/02-musa/thumbnail/thumbnail.html").read_text(encoding="utf-8")
    h = h.replace('cormorant-garamond-latin-600-normal.woff2', (ROOT / "long/02-musa/thumbnail/cormorant-garamond-latin-600-normal.woff2").as_uri())
    h = h.replace("</style>", CSS + "</style>")
    a = h.index('<div id="chip">'); b = h.index("</body>")
    return (h[:a] + '<div class="t" style="left:0;right:0;text-align:center;top:70px;font-size:150px">The sea<br><span class="y">split</span></div>'
            '<div class="chip">PROPHET MUSA (AS)</div>' + h[b:])


def ur_three():
    h = ibrahim_fire_ur()
    start = h.index('<div class="t u"'); end = h.index('</div>', start) + 6
    return h[:start] + ('<div class="t u" dir="rtl" style="left:0;right:0;text-align:center;top:60px;font-size:130px">'
                        'زندہ <span class="b">آگ میں</span></div>') + h[end:]


FINAL = {"final-yusuf": lambda: three(yusuf_well, 'Down the<br><span class="y">well</span>', top=70, size=150),
         "final-musa": musa_old_bold,
         "final-ibrahim": lambda: three(ibrahim_fire, 'Thrown in<br><span class="y">alive</span>', top=60, size=150),
         "final-ibrahim-ur": ur_three}

THUMBS = {"ibrahim-ur-fire": ibrahim_fire_ur, "yusuf-a-well": yusuf_well, "yusuf-b-dream": yusuf_dream, "yusuf-c-split": yusuf_split,
          "musa-a-sea": musa_sea, "musa-b-pharaoh": musa_pharaoh, "musa-c-basket": musa_basket,
          "ibrahim-a-fire": ibrahim_fire, "ibrahim-b-idols": ibrahim_idols, "ibrahim-c-kaaba": ibrahim_kaaba}

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for k, fn in {**THUMBS, **FINAL}.items():
        h = OUT / f"{k}.html"
        h.write_text(fn(), encoding="utf-8")
        subprocess.run(["node", str(ROOT / "tools/screenshot.js"), str(h), str(OUT / f"{k}.jpg")], check=True)
        print(k)
