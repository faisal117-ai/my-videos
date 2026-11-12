"""Build a Haq Stories long video (16:9 HyperFrames project) from spec.json + per-chapter takes.

Usage: python3 build_long.py <project_dir>

Reads:
  spec.json                      chapters: title, scene, cards (verse / text / title / end)
  narration/chNN.json            the lines of each chapter (what Callum read)
  assets/chNN/narration.wav      the take, assets/chNN/timings.json + take.json (alignment)
  assets/surah12.json            Arabic + Sahih International, generated from quran-json
Writes index.html and compositions/cNN.html, one composition per chapter (scene, captions, cards).

Channel rules: no prophet, no woman of the story, no angel is ever drawn. Other people are small
faceless silhouettes; the brothers only as distant shadows.
"""
import html
import json
import math
import random
import re
import sys
import wave
from pathlib import Path

W, H = 1920, 1080
FADE = 0.5

FONT_FACES = """
      @font-face { font-family: "Cormorant Garamond"; font-weight: 600; font-style: normal;
        src: url("assets/fonts/cormorant-garamond-latin-600-normal.woff2") format("woff2"); }
      @font-face { font-family: "Cormorant Garamond"; font-weight: 600; font-style: italic;
        src: url("assets/fonts/cormorant-garamond-latin-600-italic.woff2") format("woff2"); }
      @font-face { font-family: "Amiri Quran"; font-weight: 400;
        src: url("assets/fonts/amiri-quran-arabic-400-normal.woff2") format("woff2"); }
"""


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def hi(s: str) -> str:
    return re.sub(r"\*([^*]+)\*", r'<span class="§hi">\1</span>', esc(s))


# ---------------------------------------------------------------- timeline helpers
class TL:
    """Collects GSAP calls for one composition's timeline `tl`."""

    def __init__(self, total: float):
        self.total, self.js = total, []

    def to(self, sel, frm, to, at, d, ease="sine.inOut"):
        self.js.append(f'tl.fromTo("{sel}", {{{frm}}}, {{{to}, duration: {max(d, 0.05):.2f}, ease: "{ease}", '
                       f'immediateRender: false}}, {max(at, 0):.2f});')

    def fade(self, sel, a, b, at, d=0.8):
        self.to(sel, f"opacity: {a}", f"opacity: {b}", at, d)

    def loop(self, sel, frm, to, period, at=0.0, ease="sine.inOut"):
        reps = int((self.total - at) / period) + 1
        self.js.append(f'tl.fromTo("{sel}", {{{frm}}}, {{{to}, duration: {period:.2f}, ease: "{ease}", yoyo: true, '
                       f'repeat: {reps}, immediateRender: false}}, {at:.2f});')

    def cycle(self, sel, frm, to, period, at=0.0):
        """Repeat from->to without yoyo (drifting things)."""
        reps = int((self.total - at) / period) + 1
        self.js.append(f'tl.fromTo("{sel}", {{{frm}}}, {{{to}, duration: {period:.2f}, ease: "none", '
                       f'repeat: {reps}, immediateRender: false}}, {at:.2f});')


# ---------------------------------------------------------------- shapes
def person(x: float, h: float, lean: float = 0) -> str:
    """A faceless robed silhouette standing on y=0."""
    w = h * 0.34
    return (f'<g transform="translate({x:.0f},0) skewX({lean:.0f})"><circle cx="0" cy="{-h + w * 0.42:.1f}" r="{w * 0.36:.1f}"/>'
            f'<path d="M {-w * 0.32:.1f} {-h + w * 0.8:.1f} Q 0 {-h + w * 0.62:.1f} {w * 0.32:.1f} {-h + w * 0.8:.1f} '
            f'L {w * 0.56:.1f} 0 L {-w * 0.56:.1f} 0 Z"/></g>')


CAMEL = ("M 8 -52 Q 14 -70 30 -64 Q 40 -86 56 -66 Q 66 -60 72 -58 L 82 -84 Q 86 -96 98 -94 L 104 -88 L 94 -84 "
         "L 86 -54 Q 82 -44 74 -42 L 72 0 L 66 0 L 64 -38 L 58 -38 L 58 0 L 52 0 L 50 -40 L 26 -40 L 24 0 L 18 0 "
         "L 18 -40 L 12 -40 L 12 0 L 6 0 L 6 -44 Z")


def camel(x: float, s: float, cls: str = "") -> str:
    return f'<g class="{cls}" transform="translate({x:.0f},0) scale({s:.2f})"><path d="{CAMEL}"/></g>'


def cow(x: float, y: float, s: float, lean: bool, body: str, dark: str, cid: str) -> str:
    ry = 15 if lean else 30
    return (f'<g id="{cid}" transform="translate({x:.0f},{y:.0f}) scale({s:.2f})">'
            f'<rect x="-44" y="-4" width="9" height="40" fill="{dark}"/><rect x="-28" y="-4" width="9" height="40" fill="{dark}"/>'
            f'<rect x="22" y="-4" width="9" height="40" fill="{dark}"/><rect x="38" y="-4" width="9" height="40" fill="{dark}"/>'
            f'<ellipse cx="0" cy="-10" rx="58" ry="{ry}" fill="{body}"/>'
            f'<g class="§head"><ellipse cx="66" cy="-14" rx="18" ry="13" fill="{body}"/>'
            f'<path d="M 60 -26 Q 58 -40 50 -38 M 72 -26 Q 76 -40 84 -36" stroke="#e8dcc0" stroke-width="4" fill="none"/></g>'
            f'{"" if not lean else "".join(f"<path d=\"M {-30 + 12 * k} -18 L {-26 + 12 * k} -2\" stroke=\"{dark}\" stroke-width=\"3\"/>" for k in range(5))}'
            f'</g>')


def dunes(layers) -> str:
    """layers: [(fill, y, amp, seed)] -> svg paths across the width."""
    out = []
    for fill, y, amp, seed in layers:
        r = random.Random(seed)
        pts = [(x, y + r.uniform(-amp, amp)) for x in range(-100, W + 300, 320)]
        d = f"M {pts[0][0]} {pts[0][1]:.0f} "
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            d += f"Q {x0 + 160} {y0 + (y1 - y0) * 0.1 - amp * 0.6:.0f} {x1} {y1:.0f} "
        d += f"V {H + 20} H -100 Z"
        out.append(f'<path fill="{fill}" d="{d}"/>')
    return "".join(out)


def starfield(p: str, n: int, seed: int, box, tl: TL, size=(1.5, 4)) -> str:
    r = random.Random(seed)
    x0, y0, x1, y1 = box
    out = []
    for k in range(n):
        x, y, s = r.uniform(x0, x1), r.uniform(y0, y1), r.uniform(*size)
        out.append(f'<div id="{p}st{k}" class="§st" style="left:{x:.0f}px;top:{y:.0f}px;width:{s:.1f}px;height:{s:.1f}px"></div>')
        if k % 2 == 0:
            tl.loop(f"#{p}st{k}", f"opacity: {r.uniform(0.3, 0.6):.2f}", "opacity: 1", r.uniform(0.9, 1.8), r.uniform(0, 1))
    return "".join(out)


def motes(p: str, n: int, seed: int, box, tl: TL, color="rgba(255,220,160,0.8)", rise=260) -> str:
    r = random.Random(seed)
    x0, y0, x1, y1 = box
    out = []
    for k in range(n):
        x, y, s = r.uniform(x0, x1), r.uniform(y0, y1), r.uniform(2, 5)
        out.append(f'<div id="{p}m{k}" class="§mote" style="left:{x:.0f}px;top:{y:.0f}px;width:{s:.1f}px;height:{s:.1f}px;'
                   f'background:{color};box-shadow:0 0 8px {color}"></div>')
        per = r.uniform(5, 9)
        tl.cycle(f"#{p}m{k}", "y: 0, x: 0", f"y: {-rise}, x: {r.uniform(-60, 60):.0f}", per, r.uniform(0, 1.5))
        tl.loop(f"#{p}m{k}", "opacity: 0", "opacity: 0.9", per / 2, r.uniform(0, 1.5))
    return "".join(out)


BASE_CSS = """
    .§st { position: absolute; border-radius: 50%; background: #eef4ff; box-shadow: 0 0 6px rgba(220,235,255,0.9); }
    .§mote { position: absolute; border-radius: 50%; }
    .§full { position: absolute; inset: 0; }
    .§svg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
"""


def svg(inner: str, id_: str = "", style: str = "") -> str:
    i = f' id="{id_}"' if id_ else ""
    s = f' style="{style}"' if style else ""
    return f'<svg{i} class="§svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none"{s}>{inner}</svg>'


# ---------------------------------------------------------------- scenes
# Each scene gets (t: TL, L: line starts, E: line ends, D: duration) and returns (css, markup).

def hall(t, L, E, D, reveal=False):
    """A palace hall in Egypt: columns, high windows, grain sacks; the brothers as far shadows."""
    cols = []
    for side in (-1, 1):
        for k, (dx, h, w) in enumerate([(840, 1000, 120), (600, 820, 92), (440, 690, 72), (330, 600, 56)]):
            x = 960 + side * dx
            top = 1080 - h - (40 - k * 30)
            base = top + h
            cols.append(f'<g opacity="{1 - k * 0.13:.2f}"><rect x="{x - w / 2:.0f}" y="{top:.0f}" width="{w}" height="{h}" fill="url(#§colg)"/>'
                        f'<rect x="{x - w * 0.75:.0f}" y="{top:.0f}" width="{w * 1.5:.0f}" height="{w * 0.35:.0f}" fill="#4a3a26"/>'
                        f'<rect x="{x - w * 0.7:.0f}" y="{base - w * 0.3:.0f}" width="{w * 1.4:.0f}" height="{w * 0.3:.0f}" fill="#2e2418"/></g>')
    floor_lines = "".join(f'<path d="M 960 560 L {x} 1080" stroke="rgba(255,220,160,0.07)" stroke-width="2"/>' for x in range(-600, 2600, 240))
    sacks = []
    r = random.Random(4)
    for cx0, sgn in ((150, 1), (1770, -1)):
        for k in range(6):
            x = cx0 + sgn * (k % 3) * 110 + r.uniform(-15, 15)
            y = 1060 - (k // 3) * 95
            sacks.append(f'<g transform="translate({x:.0f},{y:.0f})"><path d="M -62 0 Q -78 -70 -38 -104 L -20 -122 L 20 -122 '
                         f'L 38 -104 Q 78 -70 62 0 Z" fill="{r.choice(["#8a6a3e", "#7a5c34", "#94744a"])}"/>'
                         f'<path d="M -24 -112 L 24 -112" stroke="#3a2a18" stroke-width="7"/></g>')
    bros = "".join(person(870 + k * 20, 46 + (k % 3) * 3) for k in range(10))
    shafts = "".join(f'<polygon id="§sh{k}" points="{x} 0 {x + 120} 0 {x + 420} 1080 {x + 160} 1080" fill="url(#§shg)" opacity="0.5"/>'
                     for k, x in enumerate((380, 780, 1180)))
    css = """
    #§hsky { background: linear-gradient(180deg, #1a120c 0%, #2a1c12 45%, #120c08 100%); }
    #§bloom { background: radial-gradient(ellipse at 50% 45%, rgba(255,226,170,0.9), rgba(255,190,110,0.35) 40%, rgba(0,0,0,0) 72%); opacity: 0; }
"""
    markup = f"""
      <div id="§hsky" class="§full"></div>
      {svg(f'''<defs><linearGradient id="§colg" x1="0" x2="1"><stop offset="0" stop-color="#2b2116"/><stop offset="0.45" stop-color="#6b5436"/><stop offset="1" stop-color="#21190f"/></linearGradient>
        <linearGradient id="§shg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(255,226,170,0.55)"/><stop offset="1" stop-color="rgba(255,226,170,0)"/></linearGradient>
        <linearGradient id="§flg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2a1a"/><stop offset="1" stop-color="#140d08"/></linearGradient></defs>
        <rect x="0" y="560" width="{W}" height="520" fill="url(#§flg)"/>{floor_lines}
        <rect x="720" y="250" width="480" height="330" fill="#1a120b"/>
        <path d="M 820 580 V 380 Q 960 250 1100 380 V 580 Z" fill="#f2c27a" opacity="0.55"/>
        <rect x="760" y="560" width="400" height="22" fill="#4a3826"/><rect x="800" y="540" width="320" height="22" fill="#5a4630"/>
        <g id="§bros" fill="#0b0805" opacity="0.9" transform="translate(0,620)">{bros}</g>
        {"".join(cols)}{shafts}{"".join(sacks)}''')}
      {motes("§hm", 40, 8, (300, 200, 1600, 1000), t)}
      <div id="§bloom" class="§full"></div>"""
    for k in range(3):
        t.loop(f"#§sh{k}", "opacity: 0.35", "opacity: 0.6", 2.6 + k * 0.7, k * 0.5)
    t.loop("#§bros", "x: 0", "x: 6", 3.2)
    if reveal:
        t.fade("#§bloom", 0, 0.35, L[3], 2.5)
        t.fade("#§bloom", 0.35, 0.15, L[4], 2)
        t.fade("#§bloom", 0.15, 0.55, L[6], 1.5)
        t.fade("#§bloom", 0.55, 0.2, L[8], 2)
        t.fade("#§bloom", 0.2, 0.85, L[11], 2.5)
    return css, markup


def dream_sky(t, bow_at, prefix="§d"):
    stars = []
    for k in range(11):
        a = math.pi * (0.1 + 0.8 * k / 10)
        x, y = 960 - 640 * math.cos(a), 760 - 420 * math.sin(a)
        stars.append(f'<div id="{prefix}s{k}" class="§ystar" style="left:{x:.0f}px;top:{y:.0f}px"></div>')
        t.loop(f"#{prefix}s{k}", "opacity: 0.65", "opacity: 1", 0.6 + (k % 4) * 0.15, k * 0.07)
    markup = f"""<div class="§full §dsky"></div>
        <div id="{prefix}set" class="§full"><div class="§dsun"></div><div class="§dmoon"></div>{"".join(stars)}</div>"""
    if bow_at is not None:
        t.to(f"#{prefix}set", "y: 0, scale: 1", "y: 110, scale: 0.9", bow_at, 1.8, "power2.inOut")
    return markup


DREAM_CSS = """
    .§dsky { background: radial-gradient(ellipse at 50% 45%, #1d2a52 0%, #0b1026 60%, #05070f 100%); }
    .§ystar { position: absolute; width: 34px; height: 34px; margin: -17px; border-radius: 50%;
      background: radial-gradient(circle, #ffffff 0%, #dfe8ff 35%, rgba(200,215,255,0) 70%); box-shadow: 0 0 30px 10px rgba(200,215,255,0.45); }
    .§dsun { position: absolute; left: 330px; top: 640px; width: 190px; height: 190px; border-radius: 50%;
      background: radial-gradient(circle, #fff2c8 0%, #ffc860 45%, rgba(255,170,60,0) 72%); }
    .§dmoon { position: absolute; left: 1430px; top: 660px; width: 130px; height: 130px; border-radius: 50%;
      background: radial-gradient(circle at 40% 38%, #fffdf3, #e6dfc8 65%, #cfc7ae); box-shadow: 0 0 60px 20px rgba(230,236,255,0.3); }
"""


def dream(t, L, E, D):
    bow = E[1] - 1.8
    clouds = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.32:.0f}" fill="#04050b" opacity="0.85"/>'
                     for x, y, rx in [(200, 300, 420), (700, 220, 360), (1200, 330, 460), (1700, 250, 400), (450, 520, 380), (1450, 560, 420)])
    tent = ('<path d="M 160 960 L 300 860 L 440 960 Z" fill="#0a0910"/><rect x="282" y="915" width="36" height="45" fill="#f2b04a" opacity="0.8"/>')
    css = DREAM_CSS + "    #§clouds { opacity: 0; }\n    #§glow { position:absolute; left:220px; top:860px; width:160px; height:140px; border-radius:50%;\n      background: radial-gradient(circle, rgba(255,190,90,0.6), rgba(255,190,90,0) 70%); }\n"
    markup = f"""{dream_sky(t, bow)}
      {svg(dunes([("#16141f", 900, 30, 1), ("#0e0d15", 970, 25, 2)]) + tent)}
      <div id="§glow"></div>
      {svg(clouds, "§clouds")}"""
    t.loop("#§glow", "opacity: 0.6", "opacity: 1", 0.5)
    t.to("#§clouds", "opacity: 0, x: 400", "opacity: 0.85, x: 0", L[3], 3)
    t.to("#§clouds", "opacity: 0.85", "opacity: 0.3", L[5], 2)
    t.to("#§clouds", "opacity: 0.3, x: 0", "opacity: 0.95, x: -120", L[6], 3)
    return css, markup


def well_svg(x, y, s):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect x="-180" y="-100" width="360" height="170" rx="10" fill="url(#§wst)"/>'
            f'<path d="M -180 -60 H 180 M -180 -20 H 180 M -180 20 H 180" stroke="rgba(0,0,0,0.35)" stroke-width="4"/>'
            f'<ellipse cx="0" cy="-100" rx="180" ry="48" fill="#6a6152"/><ellipse cx="0" cy="-98" rx="150" ry="36" fill="#030202"/>'
            f'<rect x="-170" y="-260" width="14" height="170" fill="#3a2e22"/><rect x="156" y="-260" width="14" height="170" fill="#3a2e22"/>'
            f'<rect x="-180" y="-270" width="360" height="16" fill="#4a3a2a"/></g>')


WELL_DEFS = ('<defs><linearGradient id="§wst" x1="0" x2="1"><stop offset="0" stop-color="#2a2620"/>'
             '<stop offset="0.5" stop-color="#5a5244"/><stop offset="1" stop-color="#211d18"/></linearGradient></defs>')


def shirt_path(stain=False, torn=False):
    d = ("M -70 -90 L -30 -104 Q 0 -86 30 -104 L 70 -90 L 118 -40 L 92 -12 L 64 -40 L 64 90 L -64 90 L -64 -40 "
         "L -92 -12 L -118 -40 Z")
    out = f'<path d="{d}" fill="#d9ccb0"/><path d="M -30 -104 Q 0 -70 30 -104" fill="none" stroke="#a89878" stroke-width="5"/>'
    if stain:
        out += ('<path d="M -40 10 Q -10 -20 20 6 Q 44 30 20 54 Q -6 74 -30 52 Q -56 34 -40 10 Z" fill="#7a1a14" opacity="0.85"/>'
                '<circle cx="34" cy="-30" r="9" fill="#7a1a14" opacity="0.8"/>')
    if torn:
        out += '<path d="M -8 -96 L 6 -60 L -10 -30 L 8 0 L -6 30 L 6 60 L -4 90" fill="none" stroke="#1a120c" stroke-width="7"/>'
    return out


def well(t, L, E, D):
    a_end, b_end = L[6], L[8]
    bros = "".join(person(k * 30, 52 + (k % 3) * 4) for k in range(10))
    css = """
    #§dusk { background: linear-gradient(180deg, #2a1a3a 0%, #8a4a3a 55%, #d88a4a 100%); }
    #§sun { position:absolute; left: 1320px; top: 560px; width: 220px; height: 220px; border-radius: 50%;
      background: radial-gradient(circle, #ffe0a0 0%, #ff9a50 50%, rgba(255,120,60,0) 72%); }
    #§in, #§night { opacity: 0; }
    #§iwall { background: radial-gradient(circle at 50% 30%, rgba(0,0,0,0) 0 230px, #1a140f 250px, #0a0705 75%); }
    #§ihole { position:absolute; left: 730px; top: 90px; width: 460px; height: 460px; border-radius: 50%;
      background: radial-gradient(circle, #f6efe0 0%, #cfd9f0 40%, #6a7aa0 75%); }
    #§ibeam { position:absolute; left: 560px; top: 300px; width: 800px; height: 800px; transform-origin: 50% 0%;
      background: radial-gradient(ellipse 50% 70% at 50% 10%, rgba(240,235,220,0.4), rgba(240,235,220,0.1) 45%, rgba(240,235,220,0) 75%); }
    #§rings { background: repeating-radial-gradient(circle at 50% 30%, rgba(255,255,255,0.04) 0 40px, rgba(0,0,0,0.3) 40px 46px); }
    #§nsky { background: linear-gradient(180deg, #05070f 0%, #101a30 70%, #1a1a24 100%); }
    #§lamp { position:absolute; left: 1140px; top: 520px; width: 260px; height: 260px; border-radius: 50%;
      background: radial-gradient(circle, rgba(255,200,110,0.85), rgba(255,160,70,0.25) 45%, rgba(0,0,0,0) 70%); }
"""
    markup = f"""
      <div id="§a" class="§full"><div id="§dusk" class="§full"></div><div id="§sun"></div>
        {svg(WELL_DEFS + dunes([("#5a3428", 760, 30, 3), ("#3a2018", 830, 30, 4)]) + well_svg(1180, 880, 1.0)
             + f'<g id="§bros" fill="#140c0a" transform="translate(-320,800)">{bros}</g>')}
      </div>
      <div id="§in" class="§full"><div id="§rings" class="§full"></div><div id="§iwall" class="§full"></div>
        <div id="§ihole"></div><div id="§ibeam"></div>{motes("§wm", 26, 21, (640, 500, 1280, 1050), t, "rgba(240,235,220,0.9)", -300)}</div>
      <div id="§night" class="§full"><div id="§nsky" class="§full"></div>{starfield("§n", 70, 5, (0, 0, W, 560), t)}
        {svg('<rect x="0" y="700" width="1920" height="380" fill="#120e10"/><rect x="1000" y="300" width="540" height="420" fill="#1c1612"/>'
             '<path d="M 1160 720 V 470 Q 1270 380 1380 470 V 720 Z" fill="#3a2414"/>'
             '<g id="§shirt" transform="translate(760,900) rotate(-12) scale(1.05)">' + shirt_path(stain=True) + '</g>')}
        <div id="§lamp"></div></div>"""
    t.to("#§bros", "x: -320", "x: 520", 0, a_end, "none")
    t.loop("#§sun", "scale: 1", "scale: 1.05", 3)
    t.fade("#§a", 1, 0, a_end - 0.3, 0.8)
    t.fade("#§in", 0, 1, a_end - 0.3, 0.8)
    t.to("#§ibeam", "opacity: 0.3, scaleY: 0.7", "opacity: 1, scaleY: 1", L[7], 2.5)
    t.to("#§ihole", "scale: 1", "scale: 1.12", a_end, b_end - a_end, "none")
    t.fade("#§in", 1, 0, b_end - 0.3, 0.8)
    t.fade("#§night", 0, 1, b_end - 0.3, 0.8)
    t.loop("#§lamp", "opacity: 0.75, scale: 1", "opacity: 1, scale: 1.06", 0.35, b_end)
    t.to("#§shirt", "opacity: 0", "opacity: 1", L[10], 1)
    return css, markup


def caravan(t, L, E, D):
    b0, c0 = L[2], L[3]
    walkers = ""
    for k in range(6):
        walkers += camel(k * 190, 1.25, "§camel")
        walkers += f'<g transform="translate({k * 190 - 40},0)">{person(0, 62)}</g>'
    coins = "".join(f'<div id="§coin{k}" class="§coin" style="left:{820 + k * 70}px"></div>' for k in range(5))
    pillars = "".join(f'<rect x="{760 + k * 90}" y="420" width="40" height="300" fill="#6a5034"/>' for k in range(5))
    palms = "".join(f'<g transform="translate({x},720)"><path d="M -6 0 Q 0 -150 10 -260 L 18 -260 Q 10 -150 8 0 Z" fill="#2a1e14"/>'
                    f'<path d="M 14 -260 Q -60 -300 -120 -250 M 14 -260 Q 90 -310 140 -240 M 14 -260 Q -20 -330 -70 -330 '
                    f'M 14 -260 Q 60 -340 110 -320" stroke="#24301a" stroke-width="14" fill="none"/></g>' for x in (420, 560, 1500, 1640))
    css = """
    #§day { background: linear-gradient(180deg, #7aa0c8 0%, #e8c890 60%, #e0b070 100%); }
    #§b, #§c { opacity: 0; }
    #§cloth { background: radial-gradient(ellipse at 50% 55%, #8a2a22 0%, #5a1a16 60%, #2a0c0a 100%); }
    .§coin { position:absolute; top: 380px; width: 70px; height: 70px; border-radius: 50%;
      background: radial-gradient(circle at 40% 35%, #fff2c0, #d8a840 55%, #8a6420); box-shadow: 0 6px 18px rgba(0,0,0,0.5); }
    #§eg { background: linear-gradient(180deg, #3a2a4a 0%, #c86a40 55%, #f0b060 100%); }
    #§bucket { transform-origin: 50% 0; }
"""
    markup = f"""
      <div id="§a" class="§full"><div id="§day" class="§full"></div>
        {svg(WELL_DEFS + dunes([("#d0a060", 700, 25, 6), ("#b88848", 780, 25, 7)])
             + f'<g id="§car" fill="#3a2414" transform="translate(-1200,800)">{walkers}</g>' + well_svg(1560, 900, 0.8)
             + '<g id="§bucket"><path d="M 1560 690 V 760" stroke="#3a2e22" stroke-width="4"/><path d="M 1536 760 H 1584 L 1576 800 H 1544 Z" fill="#5a4026"/></g>')}
      </div>
      <div id="§b" class="§full"><div id="§cloth" class="§full"></div>{coins}</div>
      <div id="§c" class="§full"><div id="§eg" class="§full"></div>
        {svg('<rect x="0" y="720" width="1920" height="60" fill="#2a4a5a" opacity="0.8"/><rect x="0" y="780" width="1920" height="300" fill="#3a2414"/>'
             f'<rect x="700" y="400" width="520" height="30" fill="#4a3624"/><rect x="680" y="380" width="560" height="26" fill="#5a4430"/>{pillars}'
             '<rect x="720" y="430" width="480" height="290" fill="#2a1c12" opacity="0.6"/>' + palms)}
      </div>"""
    t.to("#§car", "x: -1200", "x: 300", 0, b0 + 1, "none")
    t.loop(".§camel", "y: 0", "y: -4", 0.45)
    t.to("#§bucket", "y: 90", "y: 0", L[0] + 2.5, max(L[1] - L[0] - 2.5, 1.5), "power1.inOut")
    t.fade("#§a", 1, 0, b0 - 0.3, 0.6)
    t.fade("#§b", 0, 1, b0 - 0.3, 0.6)
    for k in range(5):
        t.to(f"#§coin{k}", "y: -500, rotation: 0", f"y: {120 + (k % 2) * 40}, rotation: {90 + k * 40}", b0 + 0.3 + k * 0.35, 0.7, "bounce.out")
    t.fade("#§b", 1, 0, c0 - 0.3, 0.6)
    t.fade("#§c", 0, 1, c0 - 0.3, 0.6)
    return css, markup


def doors(t, L, E, D):
    side_doors, panels = [], []
    # Left wall runs from x=0 (near) to x=760 (far); doors shrink with depth.
    for k, (xa, xb) in enumerate([(70, 250), (330, 450), (520, 600)]):
        ya_t, ya_b = 300 * xa / 760, 1080 - 320 * xa / 760
        yb_t, yb_b = 300 * xb / 760, 1080 - 320 * xb / 760
        top_a, top_b = ya_t + (ya_b - ya_t) * 0.25, yb_t + (yb_b - yb_t) * 0.25
        quad = f"{xa},{top_a:.0f} {xb},{top_b:.0f} {xb},{yb_b:.0f} {xa},{ya_b:.0f}"
        for sgn, pid in ((1, f"§dl{k}"), (-1, f"§dr{k}")):
            q = quad if sgn == 1 else " ".join(f"{W - float(p.split(',')[0]):.0f},{p.split(',')[1]}" for p in quad.split())
            side_doors.append(f'<polygon points="{q}" fill="#050302"/>')
            panels.append(f'<polygon id="{pid}" points="{q}" fill="url(#§wood)" stroke="#1a0f08" stroke-width="4"/>')
    css = """
    #§walls { background: #120b07; }
    #§back { position:absolute; left: 860px; top: 420px; width: 200px; height: 340px; background: #f2c886;
      box-shadow: 0 0 120px 40px rgba(255,200,120,0.35); }
    #§backdoor { position:absolute; left: 860px; top: 420px; width: 200px; height: 340px; background: #3a2414;
      border: 6px solid #1a0f08; transform-origin: 0% 50%; }
    #§husband { position:absolute; left: 905px; top: 560px; width: 110px; height: 200px; opacity: 0; }
    .§lampw { position:absolute; width: 120px; height: 120px; border-radius:50%;
      background: radial-gradient(circle, rgba(255,190,100,0.7), rgba(255,160,70,0) 70%); }
    #§tshirt { opacity: 0; }
"""
    lamps = "".join(f'<div id="§lw{k}" class="§lampw" style="left:{x}px;top:{y}px"></div>'
                    for k, (x, y) in enumerate([(280, 300), (1520, 300), (560, 420), (1240, 420)]))
    markup = f"""
      <div id="§walls" class="§full"></div>
      {svg('<defs><linearGradient id="§wood" x1="0" x2="1"><stop offset="0" stop-color="#5a3a20"/><stop offset="1" stop-color="#3a2414"/></linearGradient></defs>'
           '<polygon points="0,0 760,300 760,760 0,1080" fill="#2a1a10"/><polygon points="1920,0 1160,300 1160,760 1920,1080" fill="#24160d"/>'
           '<polygon points="0,1080 760,760 1160,760 1920,1080" fill="#1a110a"/><polygon points="0,0 1920,0 1160,300 760,300" fill="#0e0805"/>'
           '<rect x="760" y="300" width="400" height="460" fill="#2e1d12"/>' + "".join(side_doors) + "".join(panels))}
      <div id="§back"></div>
      {svg(person(960, 190), "§husband", "fill:#0a0604")}
      <div id="§backdoor"></div>{lamps}
      {svg('<g id="§tshirt" transform="translate(960,960) rotate(8) scale(1.2)">' + shirt_path(torn=True) + '</g>')}"""
    for k in range(3):
        for pid, origin in ((f"§dl{k}", "0% 50%"), (f"§dr{k}", "100% 50%")):
            t.to(f"#{pid}", f"scaleX: 0, transformOrigin: '{origin}'", f"scaleX: 1, transformOrigin: '{origin}'",
                 L[0] + 0.8 + k * 0.55 + (0.25 if pid.startswith("§dr") else 0), 0.45, "power2.in")
    for k in range(4):
        t.loop(f"#§lw{k}", "opacity: 0.7", "opacity: 1", 0.3 + k * 0.07)
    t.to("#§cam", "scale: 1", "scale: 1.25", L[3], 2.2, "power2.in")
    t.to("#§backdoor", "scaleX: 1", "scaleX: 0.08", L[4] - 0.2, 0.9, "power2.out")
    t.fade("#§husband", 0, 1, L[4] + 0.3, 0.8)
    t.fade("#§tshirt", 0, 1, L[3] + 1.2, 0.8)
    t.to("#§cam", "scale: 1.25", "scale: 1", L[6], 2.5, "power2.inOut")
    return css, markup


def banquet(t, L, E, D):
    r = random.Random(12)
    items = []
    for k in range(6):
        x = 360 + k * 240
        items.append(f'<ellipse cx="{x}" cy="740" rx="70" ry="18" fill="#c8a868"/>')
        for j in range(5):
            items.append(f'<circle cx="{x - 34 + j * 17}" cy="{722 - (j % 2) * 14}" r="17" fill="{r.choice(["#e8902a", "#d07020", "#8a2a5a", "#6a8a2a"])}"/>')
        kid = f"§knife{k}"
        items.append(f'<g transform="translate({x + 95},770)"><g id="{kid}"><g transform="rotate(-20)"><rect x="0" y="-4" width="70" height="8" fill="#d8dce0"/>'
                     f'<rect x="-36" y="-6" width="36" height="12" rx="3" fill="#4a2a14"/></g></g></g>')
    arches = "".join(f'<path d="M {x} 600 V 260 Q {x + 120} 120 {x + 240} 260 V 600 Z" fill="#2a3450" opacity="0.8"/>'
                     for x in (220, 840, 1460))
    lamps = "".join(f'<g id="§hl{k}" transform="translate({x},0)"><path d="M 0 0 V 170" stroke="#3a2a1a" stroke-width="3"/>'
                    f'<path d="M -26 170 H 26 L 16 214 H -16 Z" fill="#b8883a"/><circle cx="0" cy="226" r="40" fill="url(#§lg)"/></g>'
                    for k, x in enumerate((520, 960, 1400)))
    bars = "".join(f'<rect x="{x}" y="0" width="46" height="1080" fill="#000"/>' for x in range(120, 1920, 190))
    css = """
    #§room { background: linear-gradient(180deg, #2a1810 0%, #3a2216 60%, #1a0e08 100%); }
    #§cool { background: radial-gradient(ellipse at 50% 30%, rgba(160,190,240,0.35), rgba(0,0,0,0) 65%); opacity: 0; }
    #§bars { opacity: 0; }
"""
    markup = f"""
      <div id="§room" class="§full"></div>
      {svg('<defs><radialGradient id="§lg"><stop offset="0" stop-color="rgba(255,210,130,0.9)"/><stop offset="1" stop-color="rgba(255,170,80,0)"/></radialGradient></defs>'
           + arches + '<rect x="200" y="760" width="1520" height="34" fill="#5a3418"/><rect x="230" y="794" width="1460" height="120" fill="#3a200e"/>'
           + '<rect x="160" y="900" width="1600" height="180" fill="#5a1a22"/>' + "".join(items) + lamps)}
      <div id="§cool" class="§full"></div>
      {svg(bars, "§bars")}"""
    for k in range(3):
        t.loop(f"#§hl{k}", f"rotation: -2, transformOrigin: '50% 0%'", f"rotation: 2, transformOrigin: '50% 0%'", 1.6 + k * 0.3)
    t.to("#§knife2", "y: 0, rotation: 0, opacity: 1", "y: 140, rotation: 70, opacity: 1", L[3] + 0.6, 0.6, "power2.in")
    t.fade("#§cool", 0, 1, L[6], 2)
    t.to("#§bars", "opacity: 0, x: -200", "opacity: 0.6, x: 0", L[8], 2.5, "power2.out")
    return css, markup


def prison(t, L, E, D):
    birds = "".join(f'<path id="§bird{k}" d="M {x} {y} q 14 -12 28 0 q 14 -12 28 0" stroke="#1a1410" stroke-width="5" fill="none"/>'
                    for k, (x, y) in enumerate([(1330, 470), (1420, 440), (1480, 500)]))
    css = """
    #§wall { background: #2a2420; }
    #§bricks { background: repeating-linear-gradient(0deg, rgba(0,0,0,0.25) 0 4px, rgba(0,0,0,0) 4px 70px),
      repeating-linear-gradient(90deg, rgba(0,0,0,0.18) 0 4px, rgba(0,0,0,0) 4px 140px); }
    #§win { position:absolute; left: 820px; top: 120px; width: 280px; height: 200px; background: #9ab0d8; }
    #§moon { position:absolute; left: 860px; top: 150px; width: 70px; height: 70px; border-radius:50%;
      background: radial-gradient(circle at 40% 38%, #fffdf3, #e6dfc8 65%, #cfc7ae); }
    #§beam { position:absolute; left: 700px; top: 300px; width: 700px; height: 800px;
      background: linear-gradient(170deg, rgba(200,215,255,0.35), rgba(200,215,255,0) 80%); clip-path: polygon(17% 0, 57% 0, 100% 100%, 0 100%); }
    #§beamhi { position:absolute; inset: 0; opacity: 0;
      background: radial-gradient(ellipse at 52% 60%, rgba(220,230,255,0.35), rgba(0,0,0,0) 60%); }
    .§vig { position:absolute; width: 460px; height: 460px; border-radius:50%; top: 260px; opacity: 0;
      background: radial-gradient(circle, rgba(40,40,70,0.95) 60%, rgba(40,40,70,0) 72%); }
    #§v1 { left: 220px; } #§v2 { left: 1240px; }
    #§dark { background: #000; opacity: 0; }
"""
    markup = f"""
      <div id="§wall" class="§full"></div><div id="§bricks" class="§full"></div>
      <div id="§win"></div><div id="§moon"></div>
      {svg(''.join(f'<rect x="{850 + k * 56}" y="120" width="14" height="200" fill="#1a1612"/>' for k in range(4)))}
      <div id="§beam"></div><div id="§beamhi"></div>
      {svg('<rect x="0" y="900" width="1920" height="180" fill="#1a1612"/><path d="M 0 910 Q 300 880 700 920 T 1920 900 V 1080 H 0 Z" fill="#4a3c22" opacity="0.5"/>')}
      <div id="§v1" class="§vig"></div><div id="§v2" class="§vig"></div>
      {svg('<g id="§grapes">' + ''.join(f'<circle cx="{450 + (k % 3) * 34 - (k // 3) * 0}" cy="{430 + (k // 3) * 32}" r="18" fill="#6a2a6a"/>' for k in range(9))
           + '<path d="M 400 560 H 520 L 500 640 H 420 Z" fill="#8a6a3a"/></g>'
           + '<g id="§bread"><ellipse cx="1470" cy="580" rx="110" ry="40" fill="#b8884a"/><ellipse cx="1430" cy="560" rx="50" ry="26" fill="#d8a860"/>'
           + '<ellipse cx="1510" cy="556" rx="46" ry="24" fill="#c89850"/>' + birds + '</g>', "§dreams", "opacity:0")}
      <div id="§dark" class="§full"></div>"""
    t.fade("#§v1", 0, 1, L[2], 0.8)
    t.fade("#§v2", 0, 1, L[2] + 1.2, 0.8)
    t.fade("#§dreams", 0, 1, L[2] + 0.4, 1)
    for k in range(3):
        t.loop(f"#§bird{k}", "y: 0", "y: -10", 0.3 + k * 0.05, L[2])
    for s in ("#§v1", "#§v2", "#§dreams"):
        t.fade(s, 1, 0, L[4], 0.8)
    t.fade("#§beamhi", 0, 1, L[5], 2)
    t.loop("#§beam", "opacity: 0.85", "opacity: 1", 2.4)
    # Years pass: the moon crosses the window again and again, the light goes day and night.
    years = L[9] - 0.2
    t.js.append(f'tl.fromTo("#§moon", {{x: -120}}, {{x: 260, duration: 0.7, ease: "none", repeat: 6, immediateRender: false}}, {years:.2f});')
    t.js.append(f'tl.fromTo("#§win", {{backgroundColor: "#9ab0d8"}}, {{backgroundColor: "#f0d8a0", duration: 0.35, yoyo: true, repeat: 11, '
                f'ease: "sine.inOut", immediateRender: false}}, {years:.2f});')
    t.fade("#§dark", 0, 0.35, years + 4.5, 1.5)
    return css, markup


def cows(t, L, E, D):
    fat = "".join(cow(1060 + k * 115, 700 + (k % 2) * 40, 0.95, False, "#8a6a4a", "#5a4430", f"§f{k}") for k in range(7))
    lean = "".join(cow(k * 115, 720 + (k % 2) * 40, 0.95, True, "#5a5048", "#3a342c", f"§l{k}") for k in range(7))
    green = "".join(f'<g id="§g{k}" transform="translate({120 + k * 70},1060)"><path d="M 0 0 Q 4 -90 0 -170" stroke="#4a8a3a" stroke-width="6" fill="none"/>'
                    + "".join(f'<ellipse cx="{(-1) ** j * 10}" cy="{-150 + j * 14}" rx="8" ry="16" fill="#6ab04a"/>' for j in range(6)) + '</g>' for k in range(7))
    dry = "".join(f'<g id="§y{k}" transform="translate({1340 + k * 70},1060)"><path d="M 0 0 Q 14 -80 30 -150" stroke="#8a7240" stroke-width="5" fill="none"/>'
                  + "".join(f'<ellipse cx="{24 + (-1) ** j * 8}" cy="{-136 + j * 12}" rx="6" ry="12" fill="#a08a50"/>' for j in range(5)) + '</g>' for k in range(7))
    rain = "".join(f'<path d="M {x} {y} l -20 60" stroke="rgba(200,220,255,0.6)" stroke-width="3"/>'
                   for x, y in ((random.Random(k).uniform(0, 2100), random.Random(k + 99).uniform(-200, 900)) for k in range(140)))
    css = """
    #§dsk { background: radial-gradient(ellipse at 50% 30%, #3a3a6a 0%, #1a1a3a 55%, #0a0a1a 100%); }
    #§drought { background: linear-gradient(180deg, rgba(160,90,40,0.55), rgba(120,60,20,0.35)); opacity: 0; }
    #§rain { opacity: 0; }
    #§lean, #§ears { opacity: 0; }
"""
    markup = f"""
      <div id="§dsk" class="§full"></div>{starfield("§c", 50, 9, (0, 0, W, 450), t)}
      {svg('<rect x="0" y="560" width="1920" height="70" fill="#2a4a6a" opacity="0.8"/><rect x="0" y="630" width="1920" height="450" fill="#1e3218"/>'
           + f'<g id="§fat">{fat}</g><g id="§lean">{lean}</g><g id="§ears">{green}{dry}</g>')}
      <div id="§drought" class="§full"></div>
      {svg(f'<g id="§rainf">{rain}</g>', "§rain")}"""
    t.loop(".§head", "rotation: 0", "rotation: 12", 1.4)
    t.fade("#§lean", 0, 1, L[1] + 1, 0.8)
    t.to("#§lean", "x: -900", "x: 0", L[1] + 1, 3, "power1.out")
    t.to("#§fat", "opacity: 1", "opacity: 0", L[1] + 3.8, 1.5)
    t.fade("#§ears", 0, 1, L[1] + 4.5, 0.8)
    for k in range(7):
        t.loop(f"#§g{k}", "rotation: -3, transformOrigin: '50% 100%'", "rotation: 3, transformOrigin: '50% 100%'", 1.3 + k * 0.1)
    t.to("#§ears", "scale: 1, transformOrigin: '50% 100%'", "scale: 1.12, transformOrigin: '50% 100%'", L[6], 3)
    t.fade("#§drought", 0, 1, L[7], 2)
    t.fade("#§drought", 1, 0, L[8], 1.5)
    t.fade("#§rain", 0, 1, L[8], 1)
    t.cycle("#§rainf", "y: -200", "y: 200", 0.5, L[8])
    return css, markup


def granary(t, L, E, D):
    silos = []
    for k in range(5):
        x = 360 + k * 300
        silos.append(f'<g transform="translate({x},820)"><clipPath id="§cl{k}"><rect x="-80" y="-300" width="160" height="300"/></clipPath>'
                     f'<rect x="-80" y="-300" width="160" height="300" fill="#a8885a"/>'
                     f'<rect id="§fill{k}" x="-80" y="-300" width="160" height="300" fill="#e0b860" clip-path="url(#§cl{k})" opacity="0.65"/>'
                     f'<path d="M -86 -300 Q 0 -420 86 -300 Z" fill="#c8a06a"/><rect x="-22" y="-80" width="44" height="80" fill="#3a2a18"/></g>')
    workers = "".join(f'<g class="§wk">{person(k * 260, 70)}<rect x="{k * 260 - 20}" y="-86" width="40" height="22" rx="8" fill="#8a6a3e"/></g>' for k in range(8))
    css = """
    #§sky { background: linear-gradient(180deg, #2a3a6a 0%, #c87a5a 60%, #f0c080 100%); }
    #§sun { position:absolute; left: 860px; top: 520px; width: 200px; height: 200px; border-radius: 50%;
      background: radial-gradient(circle, #fff0c0 0%, #ffc060 50%, rgba(255,160,60,0) 72%); }
    #§haze { background: linear-gradient(180deg, rgba(170,100,40,0.6), rgba(120,70,30,0.45)); opacity: 0; }
"""
    markup = f"""
      <div id="§sky" class="§full"></div><div id="§sun"></div>
      {svg('<rect x="0" y="560" width="1920" height="120" fill="#3a6a8a"/><rect id="§glint" x="900" y="580" width="120" height="80" fill="#ffe0a0" opacity="0.5"/>'
           '<rect x="0" y="680" width="1920" height="400" fill="#6a5030"/>' + "".join(silos)
           + f'<g id="§wks" fill="#1a120a" transform="translate(-200,980)">{workers}</g>')}
      <div id="§haze" class="§full"></div>"""
    t.to("#§sun", "y: 120", "y: -280", 0, L[5], "sine.out")
    t.loop("#§glint", "opacity: 0.3", "opacity: 0.7", 0.8)
    t.to("#§wks", "x: -200", "x: 260", 0, D, "none")
    for k in range(5):
        t.to(f"#§fill{k}", "y: 300", "y: 0", L[5] + k * 0.6, max(L[8] - L[5] - 2, 4), "power1.inOut")
    t.fade("#§haze", 0, 1, L[8], 2.5)
    return css, markup


def store(t, L, E, D):
    sacks = "".join(f'<g id="§sk{k}" transform="translate({230 + k * 146},1040)"><path d="M -58 0 Q -72 -66 -36 -98 L -18 -114 L 18 -114 L 36 -98 Q 72 -66 58 0 Z" fill="#8a6a3e"/>'
                    f'<path d="M -22 -104 L 22 -104" stroke="#3a2a18" stroke-width="6"/></g>' for k in range(11))
    car = "".join(camel(k * 120, 0.8) for k in range(5))
    bros = "".join(person(k * 22, 54) for k in range(10))
    css = """
    #§inner { background: linear-gradient(180deg, #24180e 0%, #3a2616 100%); }
    #§door { position:absolute; left: 760px; top: 160px; width: 400px; height: 560px; background: linear-gradient(180deg, #f6d8a0, #e8b870); }
    #§doornight { position:absolute; left: 760px; top: 160px; width: 400px; height: 560px; background: linear-gradient(180deg, #0a0e20, #1a2238); opacity: 0; }
    #§cup { position:absolute; left: 1380px; top: 600px; width: 90px; height: 110px; }
    .§glow { position:absolute; width: 220px; height: 220px; border-radius: 50%; margin: -110px;
      background: radial-gradient(circle, rgba(255,210,110,0.85), rgba(255,190,80,0) 70%); }
    #§cupglow { left: 1425px; top: 650px; }
    #§found { opacity: 0; }
"""
    markup = f"""
      <div id="§inner" class="§full"></div><div id="§door"></div><div id="§doornight"></div>
      {svg(f'<g transform="translate(860,700)"><g id="§bros" fill="#1a0f06">{bros}</g></g>'
           f'<g id="§car" fill="#3a2414" transform="translate(800,690)" opacity="0">{car}</g>'
           '<rect x="1300" y="710" width="300" height="24" fill="#4a3018"/><rect x="1320" y="734" width="20" height="160" fill="#3a2410"/>'
           '<rect x="1560" y="734" width="20" height="160" fill="#3a2410"/>'
           '<g transform="translate(400,600)"><path d="M 0 0 V 260" stroke="#7a5a2a" stroke-width="8"/><path d="M -120 0 H 120" stroke="#7a5a2a" stroke-width="8"/>'
           '<path d="M -150 70 Q -120 100 -90 70 Z M 90 70 Q 120 100 150 70 Z" fill="#b8883a"/></g>' + sacks)}
      <div id="§cupglow" class="§glow"></div>
      {svg('<g id="§cupg"><path d="M 1395 610 H 1455 Q 1452 660 1425 668 Q 1398 660 1395 610 Z" fill="#e8c050"/>'
           '<rect x="1418" y="668" width="14" height="26" fill="#c8a038"/><rect x="1400" y="692" width="50" height="10" rx="4" fill="#e8c050"/></g>')}
      <div id="§found" class="§glow" style="left:{230 + 10 * 146}px;top:960px"></div>"""
    t.loop("#§cupglow", "scale: 0.9", "scale: 1.15", 0.9)
    t.loop("#§bros", "x: 0", "x: 5", 2.4)
    t.fade("#§doornight", 0, 1, L[3], 1)
    t.fade("#§bros", 1, 0, L[3], 1)
    t.fade("#§doornight", 1, 0, L[5], 1)
    t.fade("#§bros", 0, 1, L[5], 1)
    sx = 230 + 10 * 146
    t.to("#§cupg", "x: 0, y: 0, scale: 1", f"x: {sx - 1425}, y: {940 - 650}, scale: 0.4", L[6] + 0.5, 1.8, "power2.inOut")
    t.to("#§cupglow", "x: 0, y: 0", f"x: {sx - 1425}, y: {940 - 650}", L[6] + 0.5, 1.8, "power2.inOut")
    t.fade("#§cupglow", 1, 0, L[6] + 2.3, 0.5)
    t.fade("#§bros", 1, 0, L[7], 0.6)
    t.fade("#§car", 0, 1, L[7], 0.6)
    t.to("#§car", "x: 800, scale: 1", "x: 1000, scale: 0.7", L[7], L[8] - L[7], "none")
    t.fade("#§car", 1, 0, L[8], 0.6)
    for k in range(11):
        at = L[8] + 0.3 + k * 0.28
        t.to(f"#§sk{k}", "y: 0", "y: -18", at, 0.14, "power1.out")
        t.to(f"#§sk{k}", "y: -18", "y: 0", at + 0.14, 0.14, "power1.in")
    t.fade("#§found", 0, 1, L[8] + 0.3 + 10 * 0.28 + 0.2, 0.5)
    t.loop("#§found", "scale: 0.9", "scale: 1.15", 0.7, L[8] + 3.5)
    t.fade("#§door", 1, 0.25, L[12], 3)
    t.fade("#§found", 1, 0, L[12], 1.5)
    return css, markup


def home_markup(t, p="§"):
    css = f"""
    #{p}room {{ background: linear-gradient(180deg, #120c0a 0%, #1e1410 100%); }}
    #{p}door {{ position:absolute; left: 1180px; top: 200px; width: 380px; height: 640px; overflow: hidden;
      background: linear-gradient(180deg, #05070f 0%, #101a30 80%, #2a2020 100%); }}
    #{p}dawn {{ position:absolute; inset: 0; background: linear-gradient(0deg, rgba(255,170,100,0.8), rgba(255,170,100,0) 70%); opacity: 0; }}
    #{p}lampg {{ position:absolute; left: 560px; top: 470px; width: 420px; height: 420px; border-radius: 50%;
      background: radial-gradient(circle, rgba(255,200,110,0.75), rgba(255,160,70,0.2) 45%, rgba(0,0,0,0) 70%); }}
    #{p}curtain {{ transform-origin: 50% 0; }}
"""
    stars = starfield(p + "h", 30, 13, (1190, 210, 1550, 700), t)
    markup = f"""
      <div id="{p}room" class="§full"></div>
      <div id="{p}door">{stars}<div id="{p}dawn"></div></div>
      {svg(f'<path id="{p}curtain" d="M 1180 200 H 1300 Q 1280 520 1320 840 H 1180 Z" fill="#4a2a1e" opacity="0.92"/>'
           '<rect x="0" y="840" width="1920" height="240" fill="#0e0907"/><rect x="560" y="700" width="420" height="30" fill="#3a2414"/>'
           '<path d="M 740 690 Q 770 650 800 690 L 812 700 H 728 Z" fill="#b8883a"/><path d="M 770 640 Q 760 620 770 600 Q 782 620 770 640 Z" id="' + p + 'flame" fill="#ffd27a"/>'
           '<rect x="200" y="760" width="300" height="80" rx="10" fill="#2a1a14"/>')}
      <div id="{p}lampg"></div>"""
    t.loop(f"#{p}lampg", "opacity: 0.8", "opacity: 1", 0.32)
    t.loop(f"#{p}flame", "scaleY: 0.9, transformOrigin: '50% 100%'", "scaleY: 1.1, transformOrigin: '50% 100%'", 0.22)
    t.loop(f"#{p}curtain", "skewX: -3", "skewX: 3", 2.2)
    return css, markup


def home(t, L, E, D):
    css, markup = home_markup(t)
    css += "    #§cold { background: rgba(60,80,120,0.35); opacity: 0; }\n"
    markup += '\n      <div id="§cold" class="§full"></div>'
    t.fade("#§cold", 0, 1, L[4], 2)
    t.fade("#§cold", 1, 0.4, L[6], 2)
    t.to("#§lampg", "scale: 1", "scale: 1.35", L[6], 2.5)
    t.fade("#§dawn", 0, 1, L[7] + 1, 6)
    t.fade("#§cold", 0.4, 0, L[8], 2)
    return css, markup


def reveal(t, L, E, D):
    return hall(t, L, E, D, reveal=True)


def shirt(t, L, E, D):
    b0, c0 = L[3], L[5]
    car = "".join(camel(k * 170, 1.1, "§camel") for k in range(5))
    hc, hm = home_markup(t, "§k")
    winds = "".join(f'<path id="§wind{k}" d="M -300 {300 + k * 90} Q 0 {260 + k * 90} 300 {300 + k * 90} T 900 {300 + k * 90}" '
                    f'stroke="rgba(230,220,200,0.35)" stroke-width="4" fill="none"/>' for k in range(5))
    css = DREAM_CSS + hc + """
    #§msky { background: linear-gradient(180deg, #05070f 0%, #14203a 70%, #2a2a3a 100%); }
    #§bundle { position:absolute; width: 90px; height: 90px; border-radius: 50%; left: 1280px; top: 640px;
      background: radial-gradient(circle, rgba(255,240,200,0.95), rgba(255,220,150,0) 70%); }
    #§b, #§c { opacity: 0; }
    #§sight { background: radial-gradient(circle at 42% 60%, rgba(255,240,210,1), rgba(255,220,160,0.5) 40%, rgba(0,0,0,0) 75%); opacity: 0; }
"""
    markup = f"""
      <div id="§a" class="§full"><div id="§msky" class="§full"></div>{starfield("§s", 60, 17, (0, 0, W, 600), t)}
        {svg(dunes([("#1a1a26", 760, 25, 11), ("#121220", 840, 25, 12)]) + f'<g id="§car" fill="#06060a" transform="translate(1900,800)">{car}</g>')}
        <div id="§bundle"></div>{svg(winds, "§winds", "opacity:0")}</div>
      <div id="§b" class="§full">{hm}<div id="§sight" class="§full"></div></div>
      <div id="§c" class="§full">{dream_sky(t, L[6] + 0.3, "§q")}</div>"""
    t.to("#§car", "x: 1900", "x: 300", 0, b0, "none")
    t.to("#§bundle", "x: 0", f"x: {300 - 1900}", 0, b0, "none")
    t.loop("#§bundle", "opacity: 0.6", "opacity: 1", 0.6)
    t.loop(".§camel", "y: 0", "y: -4", 0.45)
    t.fade("#§winds", 0, 1, L[2], 1)
    for k in range(5):
        t.cycle(f"#§wind{k}", "x: -400", "x: 1900", 3 + k * 0.4, L[2] + k * 0.3)
    t.fade("#§a", 1, 0, b0 - 0.3, 0.7)
    t.fade("#§b", 0, 1, b0 - 0.3, 0.7)
    t.to("#§sight", "opacity: 0, scale: 0.3", "opacity: 1, scale: 1.4", L[3] + 2.5, 1.8, "power2.out")
    t.to("#§sight", "opacity: 1", "opacity: 0.45", L[3] + 4.5, 2)
    t.fade("#§b", 1, 0, c0 - 0.3, 0.8)
    t.fade("#§c", 0, 1, c0 - 0.3, 0.8)
    return css, markup


def lesson(t, L, E, D):
    css = """
    #§nsky { background: radial-gradient(ellipse at 50% 100%, #1a2240 0%, #0a0e20 55%, #03040a 100%); }
    #§spin { position:absolute; left: -400px; top: -900px; width: 2720px; height: 2720px; transform-origin: 50% 50%; }
"""
    markup = f"""
      <div id="§nsky" class="§full"></div>
      <div id="§spin">{starfield("§l", 220, 23, (0, 0, 2720, 2720), t, (1.5, 3.5))}</div>
      {svg(WELL_DEFS + dunes([("#0e0e18", 880, 20, 31), ("#08080e", 950, 20, 32)]) + well_svg(320, 900, 0.45)
           + '<g fill="#08080e"><rect x="1500" y="700" width="260" height="200"/><path d="M 1500 700 Q 1630 600 1760 700 Z"/>'
           + ''.join(f'<rect x="{1510 + k * 50}" y="720" width="18" height="180" fill="#151525"/>' for k in range(5)) + '</g>')}"""
    t.to("#§spin", "rotation: 0", "rotation: 14", 0, D, "none")
    return css, markup


SCENES = {"hall": hall, "dream": dream, "well": well, "caravan": caravan, "doors": doors, "banquet": banquet,
          "prison": prison, "cows": cows, "granary": granary, "store": store, "home": home, "reveal": reveal,
          "shirt": shirt, "lesson": lesson}


# ---------------------------------------------------------------- captions and cards
def chunks(line: str, max_words=13):
    """Split a spoken line into caption chunks: (char offset, text)."""
    parts, pos = [], 0
    for m in re.finditer(r".+?(?:[.?!:…](?=\s)|$)", line):
        seg = m.group(0)
        if seg.strip():
            parts.append((m.start() + len(seg) - len(seg.lstrip()), seg.strip()))
    out = []
    for off, seg in parts:
        words = seg.split()
        while len(words) > max_words:
            # Break at the comma nearest the middle, else in the middle.
            spots = [i for i, w in enumerate(words[:-2]) if w.endswith(",") and 3 <= i + 1 <= len(words) - 3]
            mid = len(words) / 2
            cut = min(spots, key=lambda i: abs(i + 1 - mid)) + 1 if spots else int(mid)
            first = " ".join(words[:cut])
            out.append((off, first))
            off += len(first) + 1
            words = words[cut:]
        out.append((off, " ".join(words)))
    merged = []
    for off, txt in out:
        if merged and len(txt.split()) <= 2 and len(merged[-1][1].split()) + len(txt.split()) <= max_words + 2:
            merged[-1] = (merged[-1][0], merged[-1][1] + " " + txt)
        else:
            merged.append((off, txt))
    return merged


# quran-json's Uthmani text writes the open tanween marks with the code points the KFGQPC Hafs font
# expects (U+0657 fathatan, U+065E dammatan, U+0656 kasratan). Amiri Quran draws those as other
# marks (or not at all), so for display they are re-encoded to the standard open-tanween code points.
# Only the encoding changes; the text itself still comes from the package, never typed by hand.
OPEN_TANWEEN = str.maketrans({"\u0657": "\u08F0", "\u065E": "\u08F1", "\u0656": "\u08F2"})


def show_en(s: str) -> str:
    return s.replace("Joseph", "Joseph [Yusuf]").replace("Jacob", "Jacob [Yaqub]")


def card_html(cid: str, card: dict, quran: dict) -> str:
    if card.get("end"):
        return (f'<div id="{cid}" class="§card §end"><div class="§mark">HAQ <span>·</span> STORIES</div>'
                f'<div class="§endt">Stories of the prophets, from the Quran</div><div class="§btn">Subscribe</div></div>')
    if card.get("title"):
        return (f'<div id="{cid}" class="§card"><div class="§title">{esc(card["title"])}</div>'
                f'<div class="§tsub">{esc(card["sub"])}</div></div>')
    if card.get("text"):
        return (f'<div id="{cid}" class="§card"><div class="§ctext">{hi(card["text"])}</div>'
                f'<div class="§ref">{esc(card["ref"])}</div></div>')
    v = quran[str(card["v"])]
    words = v["ar"].split(" ")
    a, b = card["ar"]
    ar = " ".join(words[a:b + 1]).translate(OPEN_TANWEEN)
    if card["en"] not in v["en"]:
        sys.exit(f"12:{card['v']}: English excerpt not found in Sahih International: {card['en']!r}")
    lead = "…" if not v["en"].startswith(card["en"]) else ""
    tail = "" if v["en"].rstrip(" .").endswith(card["en"]) else "…"
    en = f"“{lead}{show_en(card['en'])}{tail}”"
    return (f'<div id="{cid}" class="§card"><div class="§ar" dir="rtl" lang="ar">{esc(ar)}</div>'
            f'<div class="§en">{esc(en)}</div><div class="§ref">Yusuf 12:{card["v"]}</div></div>')


CHAPTER_CSS = """
    .§cam { position: absolute; inset: 0; transform-origin: 50% 55%; }
    .§scrim { position: absolute; left: 0; right: 0; bottom: 0; height: 300px;
      background: linear-gradient(0deg, rgba(0,0,0,0.75), rgba(0,0,0,0)); }
    .§cap { position: absolute; left: 210px; right: 210px; bottom: 64px; text-align: center;
      font-family: "Cormorant Garamond"; font-weight: 600; font-size: 54px; line-height: 1.12; color: #f5ead6;
      text-shadow: 0 3px 18px rgba(0,0,0,0.9); }
    .§cardwrap { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
      background: radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0.72) 0%, rgba(0,0,0,0.45) 50%, rgba(0,0,0,0) 80%); }
    .§card { max-width: 1400px; display: flex; flex-direction: column; align-items: center; gap: 26px; text-align: center; }
    .§ar { font-family: "Amiri Quran"; font-size: 70px; line-height: 1.8; color: #fff6e6; text-shadow: 0 0 30px rgba(215,236,255,0.4); }
    .§en { font-family: "Cormorant Garamond"; font-style: italic; font-weight: 600; font-size: 50px; line-height: 1.18; color: #f5ead6;
      text-shadow: 0 3px 18px rgba(0,0,0,0.9); }
    .§ctext { font-family: "Cormorant Garamond"; font-weight: 600; font-size: 76px; line-height: 1.1; color: #f5ead6;
      text-shadow: 0 3px 22px rgba(0,0,0,0.9); }
    .§hi { color: var(--accent); }
    .§ref { font-family: Inter, sans-serif; font-weight: 700; font-size: 28px; letter-spacing: 0.16em; text-transform: uppercase;
      color: var(--accent); border: 2px solid var(--accent); border-radius: 999px; padding: 10px 24px; background: rgba(0,0,0,0.4); }
    .§title { font-family: "Cormorant Garamond"; font-weight: 600; font-size: 118px; line-height: 1.02; color: #f5ead6;
      text-shadow: 0 4px 30px rgba(0,0,0,0.8); }
    .§tsub { font-family: "Cormorant Garamond"; font-style: italic; font-weight: 600; font-size: 52px; color: var(--accent); }
    .§mark { font-family: Inter, sans-serif; font-weight: 700; font-size: 64px; letter-spacing: 0.32em; color: #f5ead6; }
    .§mark span { color: var(--accent); }
    .§endt { font-family: "Cormorant Garamond"; font-style: italic; font-weight: 600; font-size: 52px; color: #f5ead6; }
    .§btn { font-family: Inter, sans-serif; font-weight: 700; font-size: 34px; letter-spacing: 0.08em; color: #120b08;
      background: var(--accent); border-radius: 999px; padding: 18px 48px; }
    .§label { position: absolute; left: 90px; top: 70px; }
    .§label b { display: block; font-family: Inter, sans-serif; font-weight: 700; font-size: 28px; letter-spacing: 0.3em; color: var(--accent); }
    .§label i { display: block; font-family: "Cormorant Garamond"; font-style: normal; font-weight: 600; font-size: 60px; color: #f5ead6;
      text-shadow: 0 3px 18px rgba(0,0,0,0.9); }
    .§brand { position: absolute; right: 80px; top: 70px; font-family: Inter, sans-serif; font-weight: 700; font-size: 28px;
      letter-spacing: 0.32em; color: rgba(245,234,214,0.7); }
    .§brand span { color: var(--accent); }
    .§fade { position: absolute; inset: 0; background: #000; }
"""


def chapter_html(n: int, ch: dict, lines, timings, align, dur: float, quran: dict, last: bool) -> str:
    p = f"c{n:02d}"
    t = TL(dur)
    L = [x["start"] for x in timings]
    E = [x["end"] for x in timings]
    scss, smarkup = SCENES[ch["scene"]](t, L, E, dur)
    scene_js = list(t.js)
    t.js = []

    # Cards: visible from their line until the next card or a few seconds after the line ends.
    cards, intervals = [], []
    clist = ch.get("cards", [])
    for i, c in enumerate(clist):
        s = max(L[c["line"]] - 0.15, 0)
        if c.get("end") or c.get("title"):
            e = dur - (0.05 if last or c.get("end") else FADE)
        else:
            nxt = L[clist[i + 1]["line"]] - 0.25 if i + 1 < len(clist) else dur - FADE
            e = min(nxt, max(E[c["line"]] + 1.2, s + 5.5), dur - FADE)
        intervals.append((s, e))
        cid = f"§k{i}"
        cards.append(f'<div id="{cid}w" class="§cardwrap clip" data-start="{s:.2f}" data-duration="{e - s:.2f}">'
                     f'{card_html(cid, c, quran)}</div>')
        t.to(f"#{cid}w", "opacity: 0", "opacity: 1", s, 0.45, "power2.out")
        t.to(f"#{cid}", "y: 24, scale: 0.98", "y: 0, scale: 1", s, 0.8, "power2.out")

    # Captions from the character alignment of the joined take.
    starts = align["character_start_times_seconds"]
    caps, pos = [], 0
    cap_items = []
    for line in lines:
        for off, txt in chunks(line):
            cap_items.append((starts[pos + off] + 0.3, txt))
        pos += len(line) + 1
    # Drop chunks spoken under a verse card, end each one at the next chunk or card.
    visible = []
    for k, (s, txt) in enumerate(cap_items):
        s = max(s - 0.08, 0)
        if any(a - 0.1 <= s < b for a, b in intervals):
            continue
        e = cap_items[k + 1][0] - 0.08 if k + 1 < len(cap_items) else E[-1] + 0.4
        cut = [a - 0.05 for a, b in intervals if a > s]
        visible.append([s, min([e] + cut), txt, bool(cut and min(cut) < e)])
    # A chunk too short to read joins the next one, unless a card comes between them.
    merged = []
    for s, e, txt, card_after in visible:
        if merged and not merged[-1][3] and abs(merged[-1][1] - s) < 0.05 \
                and merged[-1][1] - merged[-1][0] < 0.3 * len(merged[-1][2].split()) + 0.5 \
                and len(merged[-1][2].split()) + len(txt.split()) <= 18:
            merged[-1] = [merged[-1][0], e, merged[-1][2] + " " + txt, card_after]
        else:
            merged.append([s, e, txt, card_after])
    for k, (s, e, txt, _) in enumerate(merged):
        if e - s >= 0.2:
            caps.append(f'<div id="§cp{k}" class="§cap clip" data-start="{s:.2f}" data-duration="{e - s:.2f}">{esc(txt)}</div>')

    label = ""
    if ch.get("title"):
        label = (f'<div id="§lab" class="§label clip" data-start="0.3" data-duration="4.6"><b>CHAPTER {n}</b><i>{esc(ch["title"])}</i></div>')
        t.to("#§lab", "opacity: 0, x: -20", "opacity: 1, x: 0", 0.3, 0.6, "power2.out")
        t.to("#§lab", "opacity: 1", "opacity: 0", 4.4, 0.5)
    t.to("#§scene", "scale: 1.0, x: 0", f"scale: 1.06, x: {(-1) ** n * 30}", 0, dur, "none")
    if n > 0:
        t.fade("#§fadeIn", 1, 0, 0, FADE)
    t.fade("#§fadeOut", 0, 1, dur - FADE, FADE)

    body = f"""<template>
  <style>
    #{p} {{ position: absolute; inset: 0; overflow: hidden; background: #000; }}{BASE_CSS}{CHAPTER_CSS}{scss}
  </style>
  <div id="{p}" data-composition-id="{p}" data-width="{W}" data-height="{H}">
    <div id="§scene" class="clip" data-start="0" data-duration="{dur:.2f}" style="position:absolute;inset:0" data-layout-allow-overflow>
      <div id="§cam" class="§cam">{smarkup}
      </div>
    </div>
    <div id="§scr" class="§scrim clip" data-start="0" data-duration="{dur:.2f}"></div>
    {label}
    {chr(10).join("    " + c for c in caps).strip()}
    {chr(10).join("    " + c for c in cards).strip()}
    <div id="§fadeIn" class="§fade clip" data-start="0" data-duration="{FADE + 0.05:.2f}" style="opacity:{1 if n > 0 else 0}"></div>
    <div id="§fadeOut" class="§fade clip" data-start="{dur - FADE:.2f}" data-duration="{FADE:.2f}" style="opacity:0"></div>
    <div id="§br" class="§brand clip" data-start="0" data-duration="{dur:.2f}">HAQ <span>·</span> STORIES</div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join("    " + s for s in scene_js + t.js).strip()}
    window.__timelines["{p}"] = tl;
  </script>
</template>
"""
    return body.replace("§", f"{p}-")


def wav_len(path: Path) -> float:
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


def main() -> None:
    d = Path(sys.argv[1])
    spec = json.loads((d / "spec.json").read_text(encoding="utf-8"))
    quran = json.loads((d / "assets/surah12.json").read_text(encoding="utf-8"))["verses"]
    gap = spec.get("gap", 0.7)
    (d / "compositions").mkdir(exist_ok=True)
    hosts, audio, at = [], [], 0.0
    chapters_txt = []
    for n, ch in enumerate(spec["chapters"]):
        a = d / f"assets/ch{n:02d}"
        lines = json.loads((d / f"narration/ch{n:02d}.json").read_text(encoding="utf-8"))["lines"]
        timings = json.loads((a / "timings.json").read_text(encoding="utf-8"))
        align = json.loads((a / "take.json").read_text(encoding="utf-8"))
        if len(lines) != len(timings):
            sys.exit(f"chapter {n}: {len(lines)} lines but {len(timings)} timings")
        vo = wav_len(a / "narration.wav")
        last = n == len(spec["chapters"]) - 1
        dur = round(vo + (1.5 if last else gap), 2)
        (d / f"compositions/c{n:02d}.html").write_text(
            chapter_html(n, ch, lines, timings, align, dur, quran, last), encoding="utf-8")
        hosts.append(f'''      <div id="c{n:02d}" data-composition-id="c{n:02d}" data-composition-src="compositions/c{n:02d}.html"
        data-start="{at:.2f}" data-duration="{dur:.2f}" data-track-index="1" data-track-kind="graphics"
        data-width="{W}" data-height="{H}"></div>''')
        audio.append(f'      <audio id="vo{n:02d}" class="clip" src="assets/ch{n:02d}/narration.wav" data-start="{at:.2f}" '
                     f'data-duration="{vo:.2f}" data-track-index="10" data-volume="1"></audio>')
        chapters_txt.append(f"{int(at // 60)}:{int(at % 60):02d} {ch.get('title') or 'Intro'}")
        at = round(at + dur, 2)
    total = at
    amb = ""
    if (d / "assets/ambience.wav").exists():
        amb = (f'\n      <audio id="amb" class="clip" src="assets/ambience.wav" data-start="0" data-duration="{total:.2f}" '
               f'data-track-index="11" data-volume="{spec.get("bed_volume", 1.0)}"></audio>')
    index = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{FONT_FACES}
      :root {{ --accent: {spec["accent"]}; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ width: 100%; height: 100%; position: relative; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.2f}" data-width="{W}" data-height="{H}">
{chr(10).join(hosts)}
{chr(10).join(audio)}{amb}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    (d / "index.html").write_text(index, encoding="utf-8")
    (d / "chapters.txt").write_text("\n".join(chapters_txt) + "\n", encoding="utf-8")
    print(f"built {len(spec['chapters'])} chapters, {total:.1f}s")
    print("\n".join(chapters_txt))


if __name__ == "__main__":
    main()
