"""Scenes for long video 3, the story of Ibrahim (AS). Loaded by build_long.py through spec.json
"scene_module": "scenes_ibrahim". Same contract as scenes_musa.py: (t, L, E, D) -> (css, markup).

Channel rules: Ibrahim (AS), Ismail (AS), Lut (AS) and every prophet are never shown in any form;
neither are Hajar, Sarah or the angels (the guests are shown only by the untouched meal). People
in crowds are small faceless silhouettes. Allah is never represented.
"""
import random

from build_long import H, W, dunes, motes, person, starfield, svg
from scenes_musa import SNAKE, TORCH_CSS, crowd, flames, moon, pharaoh, sea_band, torches  # noqa: F401


def idol(x, h, iid=""):
    w = h * 0.42
    i = f' id="{iid}"' if iid else ""
    return (f'<g{i} transform="translate({x:.0f},0)"><rect x="{-w * 0.7:.0f}" y="-14" width="{w * 1.4:.0f}" height="14" fill="#3a2a1c"/>'
            f'<path d="M {-w / 2:.0f} -14 L {-w / 2:.0f} {-h * 0.62:.0f} Q 0 {-h * 0.72:.0f} {w / 2:.0f} {-h * 0.62:.0f} L {w / 2:.0f} -14 Z" fill="#7a6a58"/>'
            f'<circle cx="0" cy="{-h * 0.78:.0f}" r="{w * 0.36:.0f}" fill="#8a7a66"/></g>')


def big_fire(p, t, x0=960, y0=820, n=26, s=2.6):
    r = random.Random(7)
    out = []
    for k in range(n):
        dx = r.uniform(-260, 260)
        h = r.uniform(140, 420) * (1 - abs(dx) / 420)
        out.append(f'<path id="{p}{k}" d="M {x0 + dx - 26 * s / 2:.0f} {y0} Q {x0 + dx:.0f} {y0 - h * s / 2:.0f} {x0 + dx + 26 * s / 2:.0f} {y0} Z" '
                   f'fill="{r.choice(["#ffd27a", "#ff9a3a", "#ffbe5c", "#ff7a2a"])}"/>')
        t.loop(f"#{p}{k}", "scaleY: 0.75", "scaleY: 1.2", r.uniform(0.15, 0.3), r.uniform(0, 0.2))
    return "".join(out)


FIRE_CSS = """
    #§fglow { position: absolute; left: 460px; top: 260px; width: 1000px; height: 800px; border-radius: 50%;
      background: radial-gradient(ellipse, rgba(255,150,60,0.55), rgba(255,100,40,0) 70%); }
    #§cool { position: absolute; inset: 0; opacity: 0;
      background: radial-gradient(ellipse at 50% 70%, rgba(220,240,255,0.75), rgba(150,200,240,0.25) 40%, rgba(0,0,0,0) 70%); }
    #§flowers { opacity: 0; }
"""


def flowers(seed, x0=700, x1=1220, y=830, n=40):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(x0, x1):.0f}" cy="{y - r.uniform(0, 60):.0f}" r="{r.uniform(5, 10):.0f}" fill="{r.choice(["#f2e6a8", "#e8b4c8", "#ffffff", "#b8e0a0"])}"/>' for _ in range(n))


def fire0(t, L, E, D):
    """The fire, seen from far away; it turns cool; the title."""
    css = FIRE_CSS + """
    #§sky { background: linear-gradient(180deg, #05030a 0%, #1a0c0a 55%, #2a120a 100%); }
"""
    fire = big_fire("§bf", t)
    markup = f"""
      <div id="§sky" class="§full"></div><div id="§fglow"></div>
      {svg('<rect x="0" y="820" width="1920" height="260" fill="#120806"/>' + f'<g id="§fire">{fire}</g>'
           + f'<g fill="#050303" transform="translate(0,1000)">{crowd(40, 0, 520, 90, 3)}{crowd(40, 1400, 1920, 90, 4)}</g>'
           + f'<g id="§flowers">{flowers(5)}</g>')}
      {motes("§e", 50, 9, (560, 300, 1360, 820), t, "rgba(255,170,80,0.9)", 400)}
      <div id="§cool" class="§full"></div>"""
    c0 = L[2] + 1.5
    t.fade("#§fire", 1, 0.15, c0, 2.0)
    t.fade("#§fglow", 1, 0.2, c0, 2.0)
    t.fade("#§cool", 0, 1, c0, 2.0)
    t.fade("#§flowers", 0, 1, c0 + 1, 2.0)
    return css, markup


def idoltown(t, L, E, D):
    """A town of temples and statues at dusk; people bowing."""
    r = random.Random(11)
    statues = "".join(idol(x, r.uniform(120, 200)) for x in range(160, 1800, 180))
    css = """
    #§sky { background: linear-gradient(180deg, #1a1030 0%, #5a3040 45%, #d9864a 62%, #3a2216 72%); }
    #§bow { position: absolute; inset: 0; transform-origin: 50% 100%; }
"""
    zig = '<path d="M 760 700 L 760 600 L 820 600 L 820 520 L 880 520 L 880 440 L 1040 440 L 1040 520 L 1100 520 L 1100 600 L 1160 600 L 1160 700 Z" fill="#2a1a14"/>'
    markup = f"""
      <div id="§sky" class="§full"></div>
      {svg(zig + '<rect x="0" y="700" width="1920" height="380" fill="#2a1c12"/>' + f'<g transform="translate(0,860)">{statues}</g>')}
      <div id="§bow">{svg(f'<g fill="#0a0604" transform="translate(0,1060)">{crowd(36, 100, 1820, 110, 12)}</g>')}</div>"""
    t.loop("#§bow", "scaleY: 1", "scaleY: 0.86", 1.6, L[1])
    return css, markup


def sky(t, L, E, D):
    """A star sets, the moon sets, the sun rises and sets; then only the Creator remains (no symbol)."""
    css = """
    #§night { background: linear-gradient(180deg, #02030a 0%, #0b1026 60%, #151a2c 100%); }
    #§day { opacity: 0; background: linear-gradient(180deg, #2a4a7a 0%, #9ab8d8 50%, #f0d0a0 68%, #6a4a30 76%); }
    #§star { position: absolute; left: 1240px; top: 200px; width: 40px; height: 40px; margin: -20px; border-radius: 50%; opacity: 0;
      background: radial-gradient(circle, #fff 0%, #dfe8ff 35%, rgba(200,215,255,0) 70%); box-shadow: 0 0 40px 14px rgba(200,215,255,0.5); }
    #§moon2 { position: absolute; left: 300px; top: 820px; opacity: 0; }
    #§sun2 { position: absolute; left: 820px; top: 860px; width: 240px; height: 240px; border-radius: 50%; opacity: 0;
      background: radial-gradient(circle, #fff6dc 0%, #ffd08a 40%, rgba(255,170,80,0) 72%); }
"""
    markup = f"""
      <div id="§night" class="§full"></div><div id="§day" class="§full"></div>
      {starfield("§s", 60, 21, (0, 0, W, 600), t)}
      <div id="§star"></div><div id="§moon2">{moon(0, 0, 150)}</div><div id="§sun2"></div>
      {svg(dunes([("#1a1612", 780, 25, 61), ("#100e0c", 860, 25, 62)]))}"""
    s0, s1 = L[1], L[2]
    t.to("#§star", "opacity: 0, y: 0", "opacity: 1, y: 40", s0, 1.5, "sine.out")
    t.to("#§star", "y: 40, opacity: 1", "y: 640, opacity: 0", s0 + (s1 - s0) * 0.55, (s1 - s0) * 0.4, "sine.in")
    m1 = L[3]
    t.to("#§moon2", "opacity: 0, y: 0, x: 0", "opacity: 1, y: -560, x: 500", s1, (m1 - s1) * 0.55, "sine.out")
    t.to("#§moon2", "y: -560, x: 500, opacity: 1", "y: 0, x: 1100, opacity: 0", s1 + (m1 - s1) * 0.6, (m1 - s1) * 0.4, "sine.in")
    u1 = L[4]
    t.fade("#§day", 0, 1, m1, 2.0)
    t.to("#§sun2", "opacity: 0, y: 0", "opacity: 1, y: -620", m1, (u1 - m1) * 0.5, "sine.out")
    t.to("#§sun2", "y: -620, opacity: 1", "y: 0, opacity: 0", m1 + (u1 - m1) * 0.55, (u1 - m1) * 0.45, "sine.in")
    t.fade("#§day", 1, 0, u1 - 0.5, 2.0)
    return css, markup


def home(t, L, E, D):
    """A house at night: a lamp, an idol on a shelf; at the end the door opens to the night."""
    css = """
    #§room { background: linear-gradient(180deg, #140e0a 0%, #2a1c12 60%, #1a120c 100%); }
    #§lamp { position: absolute; left: 1300px; top: 520px; width: 40px; height: 40px; margin: -20px; border-radius: 50%;
      background: radial-gradient(circle, #fff1c9 0%, #ffbe5c 50%, rgba(255,160,60,0) 75%); box-shadow: 0 0 120px 50px rgba(255,170,70,0.3); }
    #§door { position: absolute; left: 260px; top: 300px; width: 300px; height: 560px; background: #050812; }
    #§doorw { position: absolute; left: 260px; top: 300px; width: 300px; height: 560px; background: #3a2a1c; transform-origin: 0% 50%; }
"""
    markup = f"""
      <div id="§room" class="§full"></div>
      <div id="§door">{starfield("§d", 20, 31, (0, 0, 300, 400), t)}</div><div id="§doorw"></div>
      {svg('<rect x="0" y="860" width="1920" height="220" fill="#24170e"/><rect x="900" y="560" width="440" height="20" fill="#4a3220"/>'
           + f'<g transform="translate(1120,560)">{idol(0, 150)}</g>')}
      <div id="§lamp"></div>"""
    t.loop("#§lamp", "opacity: 0.8, scale: 0.95", "opacity: 1, scale: 1.05", 0.45)
    t.to("#§doorw", "scaleX: 1", "scaleX: 0.08", L[6], 2.0, "power2.inOut")
    return css, markup


def temple(t, L, E, D):
    """The temple of idols; all broken except the largest; the people return."""
    r = random.Random(41)
    small = [(220, 220), (420, 250), (620, 230), (1300, 230), (1500, 250), (1700, 220)]
    idols_svg = "".join(idol(x, h, f"§i{k}") for k, (x, h) in enumerate(small)) + idol(960, 470, "§big")
    shards = "".join(f'<rect id="§sh{k}" x="{x + r.uniform(-40, 40):.0f}" y="{860 - h * 0.5 + r.uniform(-40, 40):.0f}" width="{r.uniform(16, 36):.0f}" height="{r.uniform(14, 30):.0f}" fill="#7a6a58" opacity="0"/>'
                     for k, (x, h) in enumerate([s for s in small for _ in range(4)]))
    css = TORCH_CSS + """
    #§bg { background: linear-gradient(180deg, #120c08 0%, #2a1c12 55%, #1a120c 100%); }
    #§light { position: absolute; left: 760px; top: 260px; width: 400px; height: 700px; opacity: 0;
      background: radial-gradient(ellipse 50% 60% at 50% 40%, rgba(255,220,160,0.5), rgba(0,0,0,0) 70%); }
    #§people { position: absolute; inset: 0; opacity: 0; }
"""
    markup = f"""
      <div id="§bg" class="§full"></div>{torches("§t", [(80, 500), (1840, 500)], t)}
      {svg('<rect x="0" y="860" width="1920" height="220" fill="#241810"/>' + ''.join(f'<rect x="{x}" y="200" width="60" height="660" fill="#3a2a1c"/>' for x in (40, 1820))
           + f'<g transform="translate(0,860)">{idols_svg}</g>' + shards)}
      <div id="§light"></div>
      <div id="§people">{svg(f'<g fill="#070504" transform="translate(0,1080)">{crowd(40, 0, 1920, 150, 42)}</g>')}</div>"""
    b0 = L[4] + 0.4
    for k in range(len(small)):
        at = b0 + k * 0.5
        t.fade(f"#§i{k}", 1, 0, at, 0.15)
        for j in range(4):
            t.to(f"#§sh{k * 4 + j}", "opacity: 0, y: 0, rotation: 0", f"opacity: 1, y: {r.uniform(60, 140):.0f}, rotation: {r.uniform(-120, 120):.0f}", at, 0.6, "power2.in")
    t.fade("#§people", 0, 1, L[5], 1.0)
    t.fade("#§light", 0, 1, L[7], 1.2)
    return css, markup


def pyre(t, L, E, D):
    """The great fire; it becomes coolness and safety."""
    css = FIRE_CSS + """
    #§sky { background: linear-gradient(180deg, #0a0404 0%, #2a0c06 55%, #3a1408 100%); }
"""
    fire = big_fire("§pf", t, n=34, s=3.0)
    markup = f"""
      <div id="§sky" class="§full"></div><div id="§fglow"></div>
      {svg('<rect x="0" y="820" width="1920" height="260" fill="#160806"/>' + f'<g id="§fire">{fire}</g>' + f'<g id="§flowers">{flowers(8, 640, 1280)}</g>'
           + f'<g fill="#050303" transform="translate(0,1060)">{crowd(30, 0, 420, 120, 13)}{crowd(30, 1500, 1920, 120, 14)}</g>')}
      {motes("§pe", 70, 10, (500, 200, 1420, 820), t, "rgba(255,170,80,0.9)", 500)}
      <div id="§cool" class="§full"></div>"""
    c0 = L[4] + 2.5
    t.fade("#§fire", 1, 0.1, c0, 2.5)
    t.fade("#§fglow", 1, 0.15, c0, 2.5)
    t.fade("#§cool", 0, 1, c0, 2.5)
    t.fade("#§flowers", 0, 1, c0 + 1.2, 2.0)
    return css, markup


def court(t, L, E, D):
    """The king's court: columns, braziers, a king silhouette; the sun rising in the east; the king slumps."""
    cols = "".join(f'<rect x="{x}" y="120" width="90" height="760" fill="#5a4026"/>' for x in (120, 380, 1450, 1710))
    css = TORCH_CSS + """
    #§bg { background: linear-gradient(180deg, #1a100a 0%, #2e1c10 50%, #120a06 100%); }
    #§king { position: absolute; inset: 0; transform-origin: 960px 760px; }
    #§east { position: absolute; left: 520px; top: 300px; width: 880px; height: 300px; opacity: 0; border-radius: 40px;
      background: linear-gradient(90deg, #f2c48a 0%, #6a7aa0 100%); }
    #§esun { position: absolute; left: 540px; top: 470px; width: 140px; height: 140px; border-radius: 50%; opacity: 0;
      background: radial-gradient(circle, #fff3d6 0%, #ffd08a 40%, rgba(255,170,80,0) 72%); }
"""
    markup = f"""
      <div id="§bg" class="§full"></div><div id="§east"></div><div id="§esun"></div>
      {svg('<rect x="0" y="760" width="1920" height="320" fill="#24170e"/><rect x="760" y="700" width="400" height="70" fill="#4a3220"/>' + cols
           + f'<g fill="#0a0604" transform="translate(0,940)">{crowd(10, 280, 700, 120, 61)}{crowd(10, 1220, 1640, 120, 62)}</g>')}
      {torches("§bz", [(560, 690), (1360, 690)], t)}
      <div id="§king">{svg(pharaoh(960, 660, 1.3, "§kg"))}</div>"""
    t.fade("#§east", 0, 0.9, L[4], 1.2)
    t.to("#§esun", "opacity: 0, y: 60", "opacity: 1, y: -100", L[4] + 0.5, 3.0, "sine.out")
    t.to("#§king", "scale: 1, y: 0", "scale: 0.9, y: 30", L[5], 1.5, "power2.inOut")
    return css, markup


def journey(t, L, E, D):
    """An empty desert road at dawn with footprints appearing; at night one bright star for the dua."""
    r = random.Random(71)
    prints = "".join(f'<ellipse id="§fp{k}" cx="{960 + (k % 2) * 30 - 15 + (k - 12) * 4:.0f}" cy="{1060 - k * 18:.0f}" rx="{max(12 - k * 0.3, 4):.0f}" ry="{max(6 - k * 0.15, 2):.0f}" fill="#4a3220" opacity="0"/>' for k in range(24))
    css = """
    #§sky { background: linear-gradient(180deg, #1a2440 0%, #6a5a7a 40%, #e09a6a 62%, #f2c48a 68%, #6a4a30 74%); }
    #§night { opacity: 0; background: linear-gradient(180deg, #02030a 0%, #0b1026 70%, #151a2c 100%); }
    #§bstar { position: absolute; left: 1360px; top: 160px; width: 60px; height: 60px; margin: -30px; border-radius: 50%; opacity: 0;
      background: radial-gradient(circle, #fff 0%, #dfe8ff 35%, rgba(200,215,255,0) 70%); box-shadow: 0 0 60px 20px rgba(200,215,255,0.5); }
"""
    markup = f"""
      <div id="§sky" class="§full"></div><div id="§night" class="§full"></div><div id="§bstar"></div>
      {svg(dunes([("#7a5636", 760, 25, 51), ("#5a3e26", 840, 30, 52), ("#3a2818", 940, 30, 53)])
           + '<path d="M 900 1080 Q 960 900 940 640 L 980 640 Q 1000 900 1020 1080 Z" fill="#8a6a46" opacity="0.6"/>' + prints)}"""
    for k in range(24):
        t.fade(f"#§fp{k}", 0, 1, L[2] + k * 0.45, 0.3)
    t.fade("#§night", 0, 1, L[5] - 0.3, 1.5)
    t.fade("#§bstar", 0, 1, L[5] + 0.6, 1.5)
    t.loop("#§bstar", "scale: 1", "scale: 1.2", 1.2, L[5] + 1.5)
    return css, markup


def valley(t, L, E, D):
    """The valley of Makkah: dry, empty; a water skin and dates; a light running between Safa and
    Marwa seven times (Hajar is never shown); Zamzam bursting from the ground."""
    r = random.Random(81)
    css = """
    #§sky { background: linear-gradient(180deg, #3a5a8a 0%, #d8b88a 55%, #e8c08a 64%, #8a6440 72%); }
    #§dot { position: absolute; left: 0; top: 0; width: 26px; height: 26px; margin: -13px; border-radius: 50%; opacity: 0;
      background: radial-gradient(circle, #fffbe8, rgba(255,230,160,0) 70%); box-shadow: 0 0 30px 10px rgba(255,230,160,0.5); }
    #§spring { position: absolute; left: 960px; top: 900px; }
    .§sp { position: absolute; left: 0; top: 0; width: 14px; height: 14px; margin: -7px; border-radius: 50%; opacity: 0;
      background: radial-gradient(circle, #f2fbff, #8fd0f0 60%, rgba(140,200,240,0) 75%); }
    #§pool { position: absolute; left: 820px; top: 880px; width: 280px; height: 60px; border-radius: 50%; opacity: 0;
      background: radial-gradient(ellipse, #bfe6f6, #5aa8d0 60%, rgba(90,168,208,0) 72%); }
"""
    drops = "".join(f'<div id="§sp{k}" class="§sp"></div>' for k in range(26))
    markup = f"""
      <div id="§sky" class="§full"></div>
      {svg('<path d="M -50 900 L 200 420 L 420 560 L 600 380 L 760 900 Z" fill="#6a4a30"/><path d="M 1160 900 L 1320 400 L 1500 520 L 1700 360 L 1980 900 Z" fill="#6a4a30"/>'
           + '<path d="M 0 900 Q 960 860 1920 900 V 1080 H 0 Z" fill="#a07448"/>'
           + '<g transform="translate(860,920)"><path d="M 0 0 Q 20 -40 50 -20 Q 70 10 40 30 Q 10 30 0 0 Z" fill="#7a5634"/><ellipse cx="110" cy="20" rx="34" ry="18" fill="#5a3e24"/></g>'
           + '<text x="300" y="860" font-family="Inter" font-weight="700" font-size="30" letter-spacing="6" fill="rgba(255,240,210,0.85)" text-anchor="middle">SAFA</text>'
           + '<text x="1600" y="860" font-family="Inter" font-weight="700" font-size="30" letter-spacing="6" fill="rgba(255,240,210,0.85)" text-anchor="middle">MARWA</text>')}
      <div id="§dot"></div><div id="§pool"></div><div id="§spring">{drops}</div>"""
    s0 = L[4] + 0.3
    run = (E[4] - L[4]) / 7.2
    t.fade("#§dot", 0, 1, s0, 0.3)
    for k in range(7):
        a, b = (300, 1600) if k % 2 == 0 else (1600, 300)
        t.to("#§dot", f"x: {a}, y: 800", f"x: {b}, y: 800", s0 + k * run, run * 0.95, "sine.inOut")
    t.fade("#§dot", 1, 0, s0 + 7 * run, 0.4)
    z0 = L[5] + 0.6
    t.fade("#§pool", 0, 1, z0, 0.8)
    for k in range(26):
        ang = r.uniform(-0.5, 0.5)
        hgt = r.uniform(120, 260)
        per = r.uniform(0.9, 1.4)
        reps = int((D - z0) / per) + 1
        t.js.append(f'tl.fromTo("#§sp{k}", {{x: 0, y: 0, opacity: 0}}, {{keyframes: [{{x: {ang * hgt * 0.6:.0f}, y: {-hgt:.0f}, opacity: 1, duration: {per / 2:.2f}, ease: "power2.out"}}, '
                    f'{{x: {ang * hgt * 1.2:.0f}, y: -10, opacity: 0, duration: {per / 2:.2f}, ease: "power2.in"}}], repeat: {reps}, immediateRender: false}}, {z0 + r.uniform(0, per):.2f});')
    return css, markup


BIRD = ('<g><path d="M -34 0 Q -14 -26 0 -4 Q 14 -26 34 0 Q 14 -8 0 6 Q -14 -8 -34 0 Z" fill="#f4efe4"/>'
        '<ellipse cx="0" cy="2" rx="9" ry="6" fill="#f4efe4"/></g>')


def hills(t, L, E, D):
    """Four hills at dawn; four birds; feathers on the hills; the birds fly back."""
    r = random.Random(91)
    hl = [(320, 760), (760, 700), (1180, 730), (1600, 770)]
    fl = [(420, 420), (800, 380), (1140, 400), (1500, 360)]
    birds = "".join(f'<g transform="translate({x},{y}) scale(2)"><g id="§bd{k}">{BIRD}</g></g>' for k, (x, y) in enumerate(fl))
    feathers = []
    for h, (hx, hy) in enumerate(hl):
        for j in range(5):
            feathers.append((f"§ft{h}{j}", hx + r.uniform(-60, 60), hy - 30 + r.uniform(-10, 10), r.uniform(-60, 60), h))
    fsvg = "".join(f'<g transform="translate({x:.0f},{y:.0f})"><g id="{fid}"><path d="M 0 -22 Q 11 0 0 22 Q -11 0 0 -22 Z" fill="#f4efe4"/></g></g>' for fid, x, y, rot, h in feathers)
    css = """
    #§sky { background: linear-gradient(180deg, #121a34 0%, #3a3e66 40%, #c27f68 60%, #f2b880 68%, #4a3a3a 76%); }
"""
    hpaths = "".join(f'<path fill="{c}" d="M {hx - 420} 1080 L {hx - 420} {hy + 200} Q {hx} {hy - 130} {hx + 420} {hy + 200} L {hx + 420} 1080 Z"/>'
                     for (hx, hy), c in zip(hl, ["#2a2026", "#241b22", "#2c2128", "#20181e"]))
    markup = f"""
      <div id="§sky" class="§full"></div>
      {svg(hpaths + fsvg + birds)}"""
    for k in range(4):
        t.loop(f"#§bd{k}", "scaleY: 1", "scaleY: -0.5", 0.18, r.uniform(0, 0.2))
    c0 = L[3] + 1.5
    for k in range(4):
        t.fade(f"#§bd{k}", 1, 0, c0 + 0.2 * k, 0.5)
    for fid, x, y, rot, h in feathers:
        fx, fy = fl[h]
        t.js.append(f'tl.set("#{fid}", {{opacity: 0}}, 0);')
        t.to(f"#{fid}", f"x: {fx - x:.0f}, y: {fy - y:.0f}, rotation: 0, opacity: 0", f"x: 0, y: 0, rotation: {rot:.0f}, opacity: 0.95", c0 + 0.2 * h + r.uniform(0, 0.4), r.uniform(2.2, 3.2), "sine.out")
    b0 = L[4] + 0.6
    for fid, x, y, rot, h in feathers:
        fx, fy = fl[h]
        t.js.append(f'tl.to("#{fid}", {{x: {fx - x:.0f}, y: {fy - y:.0f}, rotation: 0, opacity: 0, duration: 0.9, ease: "power2.in"}}, {b0 + 0.1 * h:.2f});')
    for k in range(4):
        t.fade(f"#§bd{k}", 0, 1, b0 + 0.8 + 0.1 * k, 0.3)
    return css, markup


RAM = ('<g fill="#e8e0cc"><ellipse cx="0" cy="0" rx="70" ry="42"/><rect x="-50" y="30" width="12" height="54" fill="#3a2a20"/><rect x="-20" y="34" width="12" height="50" fill="#3a2a20"/>'
       '<rect x="20" y="34" width="12" height="50" fill="#3a2a20"/><rect x="46" y="30" width="12" height="54" fill="#3a2a20"/>'
       '<ellipse cx="78" cy="-24" rx="26" ry="20"/><path d="M 70 -40 Q 46 -70 72 -78 Q 100 -76 96 -50 Q 92 -36 80 -40" stroke="#b09878" stroke-width="12" fill="none"/></g>')


def mina(t, L, E, D):
    """A rocky valley: the night of the dream, dawn, a knife on a rock, the ram."""
    css = """
    #§night { background: linear-gradient(180deg, #03040c 0%, #0b1228 60%, #141a2c 100%); }
    #§dawn { opacity: 0; background: linear-gradient(180deg, #2a3a5e 0%, #c9876a 50%, #f3c08a 62%, #8a6a4a 72%); }
    #§knife { opacity: 0; }
    #§ram { opacity: 0; }
    #§glow { position: absolute; left: 1000px; top: 520px; width: 520px; height: 420px; border-radius: 50%; opacity: 0;
      background: radial-gradient(circle, rgba(255,230,170,0.6), rgba(0,0,0,0) 70%); }
"""
    markup = f"""
      <div id="§night" class="§full"></div>{starfield("§m", 80, 101, (0, 0, W, 600), t)}<div id="§dawn" class="§full"></div>
      {svg('<path d="M 0 760 L 300 600 L 600 700 L 900 560 L 1200 680 L 1500 580 L 1920 700 V 1080 H 0 Z" fill="#2a1e18"/>'
           + '<path d="M 0 880 Q 960 840 1920 880 V 1080 H 0 Z" fill="#3a2a1e"/><ellipse cx="760" cy="900" rx="220" ry="60" fill="#4a3826"/>'
           + '<g id="§knife" transform="translate(690,880) rotate(-8)"><rect x="0" y="-6" width="60" height="14" rx="4" fill="#4a3020"/><path d="M 60 -8 L 170 -2 L 170 4 L 60 10 Z" fill="#c8ccd6"/></g>')}
      <div id="§glow"></div>
      {svg(f'<g id="§ram"><g transform="translate(1260,800) scale(1.5)">{RAM}</g></g>')}"""
    t.fade("#§dawn", 0, 1, L[3], 4)
    t.fade("#§knife", 0, 1, L[2] + 1.5, 0.8)
    t.to("#§knife", 'filter: "brightness(1)"', 'filter: "brightness(1.8)"', L[4], 0.3)
    r0 = L[6] + 0.5
    t.fade("#§knife", 1, 0, r0, 0.6)
    t.fade("#§glow", 0, 1, r0, 1.0)
    t.to("#§ram", "opacity: 0, y: 40", "opacity: 1, y: 0", r0 + 0.3, 1.2, "power2.out")
    return css, markup


def tent(t, L, E, D):
    """A tent at night; a roasted calf on a tray, untouched (the guests are never shown); at the end
    the sky fills with stars for his descendants."""
    css = """
    #§sky { background: linear-gradient(180deg, #02030a 0%, #0b1026 60%, #1a1a2a 100%); }
    #§lamp { position: absolute; left: 960px; top: 520px; width: 40px; height: 40px; margin: -20px; border-radius: 50%;
      background: radial-gradient(circle, #fff1c9 0%, #ffbe5c 50%, rgba(255,160,60,0) 75%); box-shadow: 0 0 140px 60px rgba(255,170,70,0.35); }
    #§tray { opacity: 0; }
    #§many { opacity: 0; }
"""
    many = starfield("§mn", 180, 111, (0, 0, W, 560), t, (1.5, 3))
    markup = f"""
      <div id="§sky" class="§full"></div>{starfield("§t", 40, 112, (0, 0, W, 500), t)}<div id="§many" class="§full">{many}</div>
      {svg('<path d="M 560 860 L 960 380 L 1360 860 Z" fill="#5a3e28"/><path d="M 860 860 L 960 600 L 1060 860 Z" fill="#2a1a10"/>'
           + '<rect x="0" y="860" width="1920" height="220" fill="#2a1e14"/>'
           + '<g id="§tray"><ellipse cx="960" cy="960" rx="230" ry="34" fill="#9a7a4a"/><ellipse cx="960" cy="930" rx="140" ry="50" fill="#8a4a24"/>'
           + '<ellipse cx="930" cy="912" rx="60" ry="22" fill="#a85a2c"/></g>')}
      <div id="§lamp"></div>"""
    t.loop("#§lamp", "opacity: 0.8", "opacity: 1", 0.45)
    t.fade("#§tray", 0, 1, L[2] + 1.0, 1.0)
    t.fade("#§many", 0, 1, L[7], 3.0)
    return css, markup


def kaaba(t, L, E, D):
    """The Kaaba rising row by row in the valley; then pilgrims coming from every side."""
    rows = 7
    css = """
    #§sky { background: linear-gradient(180deg, #2a4a7a 0%, #c9a07a 55%, #e8c08a 64%, #8a6440 72%); }
    .§row { position: absolute; left: 820px; width: 280px; height: 50px; background: linear-gradient(180deg, #4a4048, #2a2228);
      border-top: 2px solid #6a5a60; transform-origin: 50% 100%; }
    #§kiswa { position: absolute; left: 820px; top: 520px; width: 280px; height: 350px; opacity: 0; background: #0c0a0c;
      box-shadow: inset 0 60px 0 -20px #0c0a0c, 0 0 60px rgba(0,0,0,0.4); }
    #§band { position: absolute; left: 820px; top: 590px; width: 280px; height: 24px; opacity: 0; background: #c9a04a; }
    #§pil { position: absolute; inset: 0; opacity: 0; }
"""
    rows_html = "".join(f'<div id="§r{k}" class="§row" style="top:{820 - k * 50}px"></div>' for k in range(rows))
    pil = f'<g fill="#1a1210" transform="translate(0,1000)">{crowd(60, 0, 760, 50, 121)}{crowd(60, 1160, 1920, 50, 122)}</g>'
    markup = f"""
      <div id="§sky" class="§full"></div>
      {svg('<path d="M -50 880 L 260 460 L 520 600 L 700 880 Z" fill="#6a4a30"/><path d="M 1220 880 L 1420 480 L 1680 580 L 1980 880 Z" fill="#6a4a30"/>'
           + '<path d="M 0 870 Q 960 850 1920 870 V 1080 H 0 Z" fill="#a07448"/>')}
      {rows_html}<div id="§kiswa"></div><div id="§band"></div>
      <div id="§pil">{svg(pil)}</div>"""
    for k in range(rows):
        t.js.append(f'tl.set("#§r{k}", {{opacity: 0}}, 0);')
        t.to(f"#§r{k}", "opacity: 0, scaleY: 0", "opacity: 1, scaleY: 1", L[1] + 0.3 + k * 0.6, 0.4, "back.out(2)")
    t.fade("#§kiswa", 0, 1, L[5] - 0.5, 1.5)
    t.fade("#§band", 0, 1, L[5] - 0.2, 1.5)
    t.fade("#§pil", 0, 1, L[5] + 0.5, 1.5)
    t.to("#§pil", "y: 120, scale: 1", "y: 0, scale: 1.05", L[5] + 0.5, D - L[5] - 0.5, "none")
    return css, markup


def makkah(t, L, E, D):
    """Night over the valley: the Kaaba under the stars, a soft light."""
    css = """
    #§sky { background: radial-gradient(ellipse at 50% 100%, #1a2240 0%, #0a0e20 55%, #03040a 100%); }
    #§k { position: absolute; left: 880px; top: 640px; width: 160px; height: 200px; background: #0c0a0c; box-shadow: 0 0 80px 30px rgba(255,220,160,0.25); }
    #§kb { position: absolute; left: 880px; top: 680px; width: 160px; height: 14px; background: #c9a04a; }
    #§kglow { position: absolute; left: 760px; top: 560px; width: 400px; height: 360px; border-radius: 50%;
      background: radial-gradient(ellipse, rgba(255,220,160,0.35), rgba(255,220,160,0) 70%); }
"""
    markup = f"""
      <div id="§sky" class="§full"></div>{starfield("§mk", 160, 131, (0, 0, W, 640), t, (1.5, 3.5))}
      {svg('<path d="M -50 860 L 260 520 L 520 640 L 760 860 Z" fill="#14121c"/><path d="M 1160 860 L 1420 540 L 1680 620 L 1980 860 Z" fill="#14121c"/>'
           + '<path d="M 0 840 Q 960 820 1920 840 V 1080 H 0 Z" fill="#1c1820"/>')}
      <div id="§kglow"></div><div id="§k"></div><div id="§kb"></div>"""
    t.loop("#§kglow", "opacity: 0.5, scale: 0.95", "opacity: 1, scale: 1.08", 2.5)
    return css, markup


def lesson3(t, L, E, D):
    """The stars turning slowly over the valley; the end card."""
    css = """
    #§nsky { background: radial-gradient(ellipse at 50% 100%, #1a2240 0%, #0a0e20 55%, #03040a 100%); }
    #§spin { position:absolute; left: -400px; top: -900px; width: 2720px; height: 2720px; transform-origin: 50% 50%; }
    #§k { position: absolute; left: 910px; top: 720px; width: 100px; height: 120px; background: #0c0a0c; box-shadow: 0 0 60px 20px rgba(255,220,160,0.2); }
"""
    markup = f"""
      <div id="§nsky" class="§full"></div>
      <div id="§spin">{starfield("§l", 220, 141, (0, 0, 2720, 2720), t, (1.5, 3.5))}</div>
      {svg('<path d="M 0 840 Q 960 820 1920 840 V 1080 H 0 Z" fill="#1c1820"/>')}<div id="§k"></div>"""
    t.to("#§spin", "rotation: 0", "rotation: 12", 0, D, "none")
    return css, markup


SCENES = {"fire0": fire0, "idoltown": idoltown, "sky": sky, "home": home, "temple": temple, "pyre": pyre, "court": court,
          "journey": journey, "valley": valley, "hills": hills, "mina": mina, "tent": tent, "kaaba": kaaba,
          "makkah": makkah, "lesson3": lesson3}
