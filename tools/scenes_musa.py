"""Scenes for long video 2, the story of Musa (AS). Loaded by build_long.py through spec.json
"scene_module": "scenes_musa". Each scene takes (t, L, E, D) like the Yusuf scenes and returns
(css, markup); ids and classes use the § prefix, which build_long replaces per chapter.

Channel rules: Musa (AS) and Harun (AS) are never shown in any form; neither are Musa's mother and
sister, the wife of Pharaoh or the women of Madyan. Pharaoh, soldiers, magicians and crowds are
small faceless silhouettes. Allah is never represented: His words are voice and text only.
"""
import math
import random

from build_long import H, W, dunes, motes, person, starfield, svg


# ---------------------------------------------------------------- shared pieces
def sea_band(t, id_, y, amp, color, period, n=12):
    """A 2×-wide wave band that drifts left forever."""
    seg = 3840 / n
    d = f"M 0 {y} " + " ".join(f"Q {seg * k + seg / 4:.0f} {y - amp} {seg * k + seg / 2:.0f} {y} T {seg * (k + 1):.0f} {y}"
                                for k in range(n))
    t.cycle(f"#{id_}", "x: 0", "x: -1920", period)
    return (f'<div id="{id_}" style="position:absolute;left:0;top:0;width:3840px;height:1080px">'
            f'<svg viewBox="0 0 3840 1080" width="3840" height="1080"><path fill="{color}" d="{d} V 1080 H 0 Z"/></svg></div>')


def soldier(x, h):
    """A faceless soldier with a spear."""
    return person(x, h) + f'<rect x="{x + h * 0.2:.0f}" y="{-h * 1.25:.0f}" width="3" height="{h * 1.25:.0f}"/>'


def crowd(n, x0, x1, h, seed, spear=False):
    r = random.Random(seed)
    f = soldier if spear else person
    return "".join(f(r.uniform(x0, x1), h * r.uniform(0.85, 1.1)) for _ in range(n))


def moon(left, top, size=120):
    return (f'<div style="position:absolute;left:{left}px;top:{top}px;width:{size}px;height:{size}px;border-radius:50%;'
            f'background:radial-gradient(circle at 40% 38%,#fffdf3,#e6dfc8 65%,#cfc7ae);box-shadow:0 0 70px 24px rgba(230,236,255,0.3)"></div>')


def torches(p, pts, t):
    out = []
    for k, (x, y) in enumerate(pts):
        out.append(f'<div id="{p}{k}" class="§torch" style="left:{x:.0f}px;top:{y:.0f}px"></div>')
        t.loop(f"#{p}{k}", "opacity: 0.65, scale: 0.9", "opacity: 1, scale: 1.1", 0.25 + (k % 5) * 0.04, (k % 7) * 0.05)
    return "".join(out)


TORCH_CSS = """
    .§torch { position: absolute; width: 18px; height: 18px; margin: -9px; border-radius: 50%;
      background: radial-gradient(circle, #fff1c9 0%, #ffae4a 50%, rgba(255,140,40,0) 75%); box-shadow: 0 0 30px 12px rgba(255,150,60,0.35); }
"""

STAFF = '<rect x="-6" y="-170" width="12" height="340" rx="6" fill="#7a5634"/><path d="M -6 -170 Q -30 -200 -10 -215" stroke="#7a5634" stroke-width="12" fill="none" stroke-linecap="round"/>'
SNAKE = ('<path d="M -260 30 C -200 -40 -140 80 -80 10 S 40 -50 100 20 S 200 60 250 -10" stroke="#3c4a2a" stroke-width="34" fill="none" stroke-linecap="round"/>'
         '<ellipse cx="262" cy="-16" rx="38" ry="24" fill="#3c4a2a"/><circle cx="276" cy="-24" r="5" fill="#e8d36a"/>')


def pyramids(y, color):
    return "".join(f'<path d="M {x - w} {y} L {x} {y - h} L {x + w} {y} Z" fill="{color}"/>' for x, w, h in [(380, 230, 210), (700, 170, 150), (1580, 260, 240)])


# ---------------------------------------------------------------- scenes
def hook(t, L, E, D):
    """The shore at night: the crowd on the sand, the sea ahead, Pharaoh's torches coming."""
    pts = [(1300 + k * 34 + (k % 3) * 8, 640 + (k % 4) * 6) for k in range(26)]
    css = TORCH_CSS + """
    #§sky { background: linear-gradient(180deg, #03050e 0%, #0d1832 60%, #1a2440 100%); }
    #§army { position: absolute; inset: 0; }
"""
    markup = f"""
      <div id="§sky" class="§full"></div>{starfield("§h", 80, 3, (0, 0, W, 520), t)}{moon(260, 120)}
      {svg('<path fill="#0b1020" d="M 0 640 Q 960 610 1920 640 V 1080 H 0 Z"/><path fill="#1a160f" d="M 900 700 Q 1400 650 1920 680 V 1080 H 900 Z"/>')}
      {sea_band(t, "§w1", 720, 14, "#14223e", 16)}{sea_band(t, "§w2", 800, 18, "#0f1a30", 12)}
      {svg(f'<g fill="#07070c" transform="translate(0,760)">{crowd(60, 980, 1500, 50, 7)}</g>')}
      <div id="§army">{svg(f'<g fill="#040408" transform="translate(0,660)">{crowd(40, 1300, 1900, 30, 9, True)}</g>')}{torches("§t", pts, t)}</div>"""
    t.to("#§army", "x: 300", "x: 0", 0, D, "none")
    return css, markup


def palace(t, L, E, D):
    """Egypt at dusk: pyramids, a great pylon, soldiers marching past homes whose lamps go out."""
    homes = []
    for k in range(9):
        x = 60 + k * 210
        homes.append(f'<rect x="{x}" y="760" width="170" height="140" fill="#2a1d14"/><rect x="{x + 60}" y="820" width="50" height="80" fill="#120c08"/>')
    wins = "".join(f'<div id="§win{k}" class="§win" style="left:{95 + k * 210}px"></div>' for k in range(9))
    for k in range(9):
        off = L[3] + 0.6 + k * 0.35
        per = 0.4 + k * 0.03
        t.js.append(f'tl.fromTo("#§win{k}", {{opacity: 0.8}}, {{opacity: 1, duration: {per:.2f}, ease: "sine.inOut", yoyo: true, '
                    f'repeat: {max(int(off / per) - 2, 0)}, immediateRender: false}}, 0);')
        t.fade(f"#§win{k}", 1, 0, off, 0.3)
    css = """
    #§sky { background: linear-gradient(180deg, #1a1030 0%, #6a3a3a 45%, #d9864a 62%, #3a2216 75%); }
    #§sun { position: absolute; left: 860px; top: 470px; width: 200px; height: 200px; border-radius: 50%;
      background: radial-gradient(circle, #ffe4a8 0%, #ff9a50 50%, rgba(255,120,60,0) 72%); }
    .§win { position: absolute; top: 790px; width: 26px; height: 26px; background: #ffc670; box-shadow: 0 0 24px 8px rgba(255,190,100,0.45); }
    #§march { position: absolute; inset: 0; }
"""
    pylon = ('<path d="M 1180 700 L 1220 300 L 1420 300 L 1460 700 Z M 1500 700 L 1540 300 L 1740 300 L 1780 700 Z" fill="#3a2618"/>'
             '<rect x="1440" y="420" width="80" height="280" fill="#120c08"/><circle cx="1480" cy="360" r="28" fill="#c98a3a"/>')
    markup = f"""
      <div id="§sky" class="§full"></div><div id="§sun"></div>
      {svg(pyramids(700, "#4a2c1e") + '<rect x="0" y="690" width="1920" height="390" fill="#2e1f14"/>' + pylon + "".join(homes))}
      {wins}
      <div id="§march">{svg(f'<g fill="#0c0806" transform="translate(0,960)">{crowd(14, 0, 900, 110, 4, True)}</g>')}</div>"""
    t.to("#§march", "x: -900", "x: 1400", 0, D, "none")
    t.loop("#§sun", "scale: 1", "scale: 1.05", 3)
    return css, markup


def river(t, L, E, D):
    """The Nile: a basket drifting from the reeds at night to Pharaoh's palace at dawn, then a
    home with an empty cradle that is filled again. No person is shown."""
    r = random.Random(12)
    reeds = "".join(f'<path d="M {x:.0f} 1080 Q {x + r.uniform(-20, 20):.0f} {1080 - h / 2:.0f} {x + r.uniform(-30, 30):.0f} {1080 - h:.0f}" '
                    f'stroke="#122018" stroke-width="{r.uniform(5, 9):.0f}" fill="none"/>' for x, h in [(r.uniform(0, 600), r.uniform(120, 260)) for _ in range(50)])
    css = """
    #§night { background: linear-gradient(180deg, #050816 0%, #101a36 55%, #1a2440 100%); }
    #§dawn { background: linear-gradient(180deg, #2a2a4e 0%, #b9785a 52%, #e8b07a 62%, #2a3a50 70%); opacity: 0; }
    #§basket { position: absolute; left: 380px; top: 770px; width: 240px; height: 130px; opacity: 0; }
    #§home { opacity: 0; background: linear-gradient(180deg, #120d0a 0%, #241912 60%, #1a120d 100%); }
    #§lamp { position: absolute; left: 1400px; top: 380px; width: 40px; height: 40px; border-radius: 50%;
      background: radial-gradient(circle, #fff1c9 0%, #ffbe5c 50%, rgba(255,160,60,0) 75%); box-shadow: 0 0 90px 40px rgba(255,170,70,0.3); }
    #§warm { background: radial-gradient(ellipse at 50% 80%, rgba(255,190,110,0.45), rgba(255,160,80,0) 65%); opacity: 0; }
    #§fill { opacity: 0; }
"""
    basket = ('<svg id="§basket" viewBox="0 0 240 130"><ellipse cx="120" cy="112" rx="110" ry="14" fill="rgba(200,220,255,0.15)"/>'
              '<path d="M 10 50 Q 120 150 230 50 Z" fill="#8a6234"/><path d="M 22 62 Q 120 140 218 62 M 40 82 Q 120 135 200 82" stroke="#5e4020" stroke-width="5" fill="none"/>'
              '<path d="M 30 52 Q 120 10 210 52 Z" fill="#cdbb95"/></svg>')
    cradle = ('<g transform="translate(760,640)"><path d="M 0 236 Q 200 290 400 236" stroke="#4a3322" stroke-width="16" fill="none" stroke-linecap="round"/>'
              '<rect x="20" y="80" width="20" height="160" rx="6" fill="#5a3e28"/><rect x="360" y="80" width="20" height="160" rx="6" fill="#5a3e28"/>'
              '<rect x="40" y="130" width="320" height="96" rx="10" fill="#6a4a30"/><path d="M 50 150 H 350 M 50 178 H 350 M 50 206 H 350" stroke="#4a3322" stroke-width="5"/>'
              '<g id="§fill"><path d="M 52 132 Q 110 86 200 96 Q 290 86 348 132 Z" fill="#d8c8a4"/></g></g>')
    markup = f"""
      <div id="§night" class="§full"></div><div id="§dawn" class="§full"></div>{starfield("§r", 50, 2, (0, 0, W, 420), t)}
      {svg('<g fill="#0a0c16"><path d="M 1150 640 L 1150 470 L 1200 470 L 1200 420 L 1920 420 L 1920 640 Z"/>'
           + "".join(f'<rect x="{1220 + k * 120}" y="480" width="24" height="160"/>' for k in range(6)) + '</g>')}
      <div class="§full" style="top:640px;background:linear-gradient(180deg,#0f1c34,#0a1426)"></div>
      {sea_band(t, "§w1", 680, 8, "#13223e", 18)}{basket}{sea_band(t, "§w2", 780, 12, "#0e1a32", 13)}{svg(reeds)}
      <div id="§home" class="§full"><div id="§lamp"></div><div id="§warm" class="§full"></div>{svg(cradle)}</div>"""
    t.fade("#§basket", 0, 1, L[2], 1.2)
    t.loop("#§basket", "y: -6, rotation: -3", "y: 6, rotation: 3", 1.1, L[2])
    t.to("#§basket", "x: 0", "x: 820", L[3] - 0.5, L[5] - L[3], "sine.inOut")
    t.fade("#§dawn", 0, 1, L[3], 4)
    t.fade("#§home", 0, 1, L[5] - 0.3, 1)
    t.loop("#§lamp", "opacity: 0.8", "opacity: 1", 0.5, L[5])
    t.fade("#§fill", 0, 1, L[7], 1.2)
    t.fade("#§warm", 0, 1, L[7], 2)
    return css, markup


def city(t, L, E, D):
    """A city street at night: two men fighting; one falls; a man runs from the far end; then an
    empty road into the desert at dawn. The one who struck is never shown."""
    r = random.Random(21)
    bld = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{900 - y}" fill="{c}"/>'
                  for x, y, w, c in [(0, 420, 260, "#15121c"), (240, 360, 220, "#1b1724"), (450, 470, 260, "#15121c"),
                                     (1200, 380, 240, "#1b1724"), (1430, 440, 260, "#15121c"), (1680, 350, 260, "#1b1724")])
    wins = "".join(f'<rect x="{x:.0f}" y="{y:.0f}" width="22" height="30" fill="#f2b04a" opacity="{r.uniform(0.4, 0.9):.2f}"/>'
                   for x, y in [(r.choice([r.uniform(20, 680), r.uniform(1220, 1880)]), r.uniform(400, 820)) for _ in range(30)])
    css = """
    #§sky { background: linear-gradient(180deg, #05060e 0%, #141a30 70%, #1a1a24 100%); }
    #§fight, #§fall, #§run { position: absolute; inset: 0; }
    #§road { opacity: 0; background: linear-gradient(180deg, #2a2a4e 0%, #c27f68 50%, #e8b07a 58%, #4a3220 60%, #2a1c12 100%); }
"""
    a, b = person(900, 150), person(1010, 150)
    markup = f"""
      <div id="§sky" class="§full"></div>{starfield("§c", 40, 6, (700, 0, 1200, 300), t)}{moon(900, 80, 90)}
      {svg(bld + wins + '<rect x="0" y="900" width="1920" height="180" fill="#100d10"/>')}
      <div id="§fight">{svg(f'<g fill="#050407" transform="translate(0,900)"><g id="§m1">{a}</g><g id="§m2">{b}</g></g>')}</div>
      <div id="§run" style="opacity:0">{svg(f'<g fill="#050407" transform="translate(0,900)"><g id="§rn">{person(1850, 120, -12)}</g></g>')}</div>
      <div id="§road" class="§full">{svg('<path d="M 860 640 L 1060 640 L 1500 1080 L 420 1080 Z" fill="#6a4a30"/>'
           + "".join(f'<ellipse cx="{960 + k * 18 * (-1) ** k}" cy="{1040 - k * 50}" rx="{14 - k}" ry="{6 - k * 0.4:.1f}" fill="#3a2618"/>' for k in range(8)))}</div>"""
    t.loop("#§m1", "x: 0, skewX: 0", "x: 22, skewX: 6", 0.35, L[1])
    t.loop("#§m2", "x: 0, skewX: 0", "x: -22, skewX: -6", 0.32, L[1])
    fall = L[2] + (E[2] - L[2]) * 0.55
    t.to("#§m2", "rotation: 0, x: 0, y: 0", "rotation: 86, x: 60, y: 0", fall, 0.7, "power2.in")
    t.js.append(f'tl.set("#§m2", {{transformOrigin: "50% 100%"}}, 0);')
    t.fade("#§fight", 1, 0, L[5] - 0.2, 0.8)
    t.fade("#§run", 0, 1, L[5], 0.4)
    t.to("#§rn", "x: 0", "x: -900", L[5], E[5] - L[5], "none")
    t.loop("#§rn", "y: 0", "y: -10", 0.18, L[5])
    t.fade("#§road", 0, 1, L[6], 1.2)
    return css, markup


def sheep(x, y, s, fid=""):
    i = f' id="{fid}"' if fid else ""
    return (f'<g{i} transform="translate({x:.0f},{y:.0f}) scale({s:.2f})"><ellipse cx="0" cy="0" rx="34" ry="22" fill="#e8e0cc"/>'
            f'<ellipse cx="34" cy="-8" rx="12" ry="10" fill="#2a2220"/><rect x="-22" y="16" width="6" height="22" fill="#2a2220"/>'
            f'<rect x="14" y="16" width="6" height="22" fill="#2a2220"/></g>')


def madyan(t, L, E, D):
    """The well of Madyan: shepherds crowd the water; a small flock waits apart (its two keepers
    are never shown); it is watered; a tree's shade; a lit house at dusk."""
    r = random.Random(31)
    flock = "".join(sheep(r.uniform(700, 1150), r.uniform(830, 930), r.uniform(0.8, 1.1)) for _ in range(16))
    apart = "".join(sheep(150 + k * 70 + r.uniform(-10, 10), 900 + (k % 2) * 30, 1.0) for k in range(5))
    css = """
    #§sky { background: linear-gradient(180deg, #4a6a8a 0%, #c9a77a 55%, #e8c08a 64%, #8a6440 70%); }
    #§sun { position: absolute; left: 1500px; top: 140px; width: 160px; height: 160px; border-radius: 50%;
      background: radial-gradient(circle, #fffbe8 0%, #ffe4a0 45%, rgba(255,220,140,0) 72%); }
    #§dusk { opacity: 0; background: linear-gradient(180deg, #1a1430 0%, #6a3a3a 50%, #d9864a 64%, #3a2216 72%); }
    #§apart { position: absolute; inset: 0; }
    #§house { opacity: 0; }
    #§door { position: absolute; left: 1590px; top: 700px; width: 50px; height: 80px; background: #ffc66a; opacity: 0;
      box-shadow: 0 0 60px 24px rgba(255,190,100,0.45); }
"""
    well = ('<g transform="translate(960,860)"><rect x="-140" y="-70" width="280" height="130" rx="8" fill="#6a5a44"/>'
            '<ellipse cx="0" cy="-70" rx="140" ry="36" fill="#8a7a62"/><ellipse cx="0" cy="-68" rx="112" ry="26" fill="#0a0806"/></g>')
    tree = ('<g transform="translate(330,640)"><path d="M -14 260 L -8 40 M -8 120 L -90 30 M -6 90 L 80 10" stroke="#3a2a1c" stroke-width="22" fill="none" stroke-linecap="round"/>'
            '<g fill="#4a6a32"><ellipse cx="-90" cy="10" rx="110" ry="60"/><ellipse cx="60" cy="-10" rx="120" ry="64"/><ellipse cx="-10" cy="-50" rx="120" ry="60"/></g></g>'
            '<ellipse cx="320" cy="910" rx="230" ry="34" fill="rgba(0,0,0,0.25)"/>')
    shep = f'<g fill="#2a1d14" transform="translate(0,880)">{crowd(9, 760, 1180, 120, 5)}</g>'
    markup = f"""
      <div id="§sky" class="§full"></div><div id="§sun"></div><div id="§dusk" class="§full"></div>
      {svg(dunes([("#a07448", 720, 25, 33), ("#8a6038", 800, 25, 34)]) + tree + well + shep + flock)}
      <div id="§apart">{svg(apart)}</div>
      {svg('<g id="§house"><rect x="1500" y="640" width="240" height="140" fill="#3a2418"/><path d="M 1480 650 L 1620 560 L 1760 650 Z" fill="#2a1a10"/></g>')}
      <div id="§door"></div>"""
    t.loop("#§apart", "y: 0", "y: -3", 0.6)
    t.to("#§apart", "x: 0", "x: 520", L[3], 2.5, "sine.inOut")
    t.to("#§apart", "x: 520", "x: 0", L[3] + 4.5, 2.5, "sine.inOut")
    t.fade("#§dusk", 0, 1, L[4], 3)
    t.fade("#§house", 0, 1, L[5], 1.2)
    t.fade("#§door", 0, 1, L[5] + 0.8, 1.2)
    return css, markup


def flames(p, x, y, s, t, n=7):
    out = []
    for k in range(n):
        dx = (k - n / 2) * 12 * s
        h = (60 + (k % 3) * 25) * s
        out.append(f'<path id="{p}{k}" d="M {x + dx - 14 * s:.0f} {y} Q {x + dx:.0f} {y - h:.0f} {x + dx + 14 * s:.0f} {y} Z" '
                   f'fill="{["#ffd27a", "#ff9a3a", "#ffbe5c"][k % 3]}"/>')
        t.loop(f"#{p}{k}", "scaleY: 0.8", "scaleY: 1.2", 0.18 + (k % 4) * 0.05, k * 0.03)
    return "".join(out)


def tur(t, L, E, D):
    """Mount Tur at night: a fire in a tree on the mountainside, a pair of sandals left on the
    ground, and a staff that becomes a snake and a staff again. Allah is never represented."""
    css = """
    #§sky { background: linear-gradient(180deg, #02030a 0%, #0b1026 60%, #151a2c 100%); }
    #§glow { position: absolute; left: 1510px; top: 680px; width: 300px; height: 300px; border-radius: 50%;
      background: radial-gradient(circle, rgba(255,180,90,0.55), rgba(255,140,60,0) 70%); }
    #§obj { position: absolute; inset: 0; opacity: 0; }
    #§staff, #§snake { transform-origin: 960px 900px; }
"""
    fire = flames("§f", 1660, 830, 1.2, t)
    mtn = '<path fill="#0c0d16" d="M -100 1080 L 500 560 L 900 700 L 1300 620 L 1660 830 L 2100 760 L 2100 1080 Z"/>'
    tree = '<path d="M 1660 830 L 1660 780 M 1660 810 L 1620 770 M 1660 800 L 1700 760" stroke="#1a1208" stroke-width="10" fill="none"/>'
    sandals = ('<g id="§sand" opacity="0"><ellipse cx="700" cy="930" rx="60" ry="22" fill="#6a4a2a"/><ellipse cx="800" cy="938" rx="60" ry="22" fill="#6a4a2a"/>'
               '<path d="M 670 924 L 730 924 M 770 932 L 830 932" stroke="#3a2614" stroke-width="6"/></g>')
    markup = f"""
      <div id="§sky" class="§full"></div>{starfield("§u", 120, 41, (0, 0, W, 600), t)}
      {svg(mtn + tree + fire + '<rect x="0" y="880" width="1920" height="200" fill="#08080e"/>' + sandals)}
      <div id="§glow"></div>
      <div id="§obj">{svg(f'<g id="§staff" transform="translate(960,900) rotate(80)">{STAFF}</g><g id="§snake" opacity="0" transform="translate(960,880)">{SNAKE}</g>')}</div>"""
    t.loop("#§glow", "opacity: 0.7, scale: 0.95", "opacity: 1, scale: 1.05", 0.6)
    t.fade("#§sand", 0, 1, L[3] + 2.0, 1.0)
    t.fade("#§sand", 1, 0, L[5], 0.8)
    t.fade("#§obj", 0, 1, L[5] + 0.5, 1.0)
    t.fade("#§staff", 1, 0, L[6] + 2.6, 0.3)
    t.fade("#§snake", 0, 1, L[6] + 2.6, 0.3)
    t.loop("#§snake", "x: -20, skewX: -6", "x: 20, skewX: 6", 0.35, L[6] + 2.6)
    t.fade("#§snake", 1, 0, L[7] + 1.5, 0.4)
    t.fade("#§staff", 0, 1, L[7] + 1.5, 0.4)
    t.fade("#§obj", 1, 0, L[8], 0.8)
    return css, markup


def tur2(t, L, E, D):
    """Dawn over the desert after the night at Tur; the road to Egypt; a palace far away."""
    css = """
    #§sky { background: linear-gradient(180deg, #1a2440 0%, #6a5a7a 40%, #e09a6a 62%, #f2c48a 68%, #6a4a30 74%); }
    #§sun { position: absolute; left: 860px; top: 600px; width: 220px; height: 220px; border-radius: 50%;
      background: radial-gradient(circle, #fff3d6 0%, #ffd08a 40%, rgba(255,170,80,0) 72%); }
    #§rays { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; opacity: 0.35; transform-origin: 970px 710px;
      background: repeating-conic-gradient(from 0deg at 970px 710px, rgba(255,230,180,0.18) 0deg 4deg, rgba(0,0,0,0) 4deg 14deg); }
    #§far { opacity: 0; }
"""
    birds = "".join(f'<path id="§b{k}" d="M {x} {y} q 14 -12 28 0 q 14 -12 28 0" stroke="#2a1d20" stroke-width="4" fill="none"/>'
                    for k, (x, y) in enumerate([(500, 300), (560, 330), (620, 290), (1300, 250), (1360, 280)]))
    for k in range(5):
        t.cycle(f"#§b{k}", "x: -300", "x: 600", 14 + k)
    markup = f"""
      <div id="§sky" class="§full"></div><div id="§rays"></div><div id="§sun"></div>
      {svg('<g id="§far" fill="#4a3424">' + pyramids(740, "#5a3e2a") + '</g>' + dunes([("#7a5636", 760, 25, 51), ("#5a3e26", 840, 30, 52), ("#3a2818", 940, 30, 53)])
           + '<path d="M 900 760 Q 960 900 760 1080 L 1160 1080 Q 1000 900 1020 760 Z" fill="#8a6a46" opacity="0.6"/>' + birds)}"""
    t.to("#§sun", "y: 120", "y: -160", 0, D, "none")
    t.to("#§rays", "rotation: 0", "rotation: 12", 0, D, "none")
    t.fade("#§far", 0, 1, L[5], 3)
    return css, markup


def pharaoh(x, y, s, fid="§ph"):
    """Pharaoh as a faceless silhouette on a throne, with the tall crown shape."""
    return (f'<g id="{fid}" transform="translate({x},{y}) scale({s})"><rect x="-70" y="-120" width="140" height="160" rx="10" fill="#1a1208"/>'
            f'<rect x="-90" y="-250" width="20" height="290" fill="#2a1c0e"/><rect x="70" y="-250" width="20" height="290" fill="#2a1c0e"/>'
            f'<g fill="#050403"><path d="M -40 -40 L -46 -150 Q 0 -170 46 -150 L 40 -40 Z"/><circle cx="0" cy="-185" r="30"/>'
            f'<path d="M -24 -205 L -18 -280 L 18 -280 L 24 -205 Z"/></g></g>')


def throne(t, L, E, D):
    """Pharaoh's throne hall: columns, braziers, courtiers; Pharaoh rises as he declares himself lord."""
    cols = "".join(f'<rect x="{x}" y="120" width="90" height="820" fill="url(#§col)"/><rect x="{x - 20}" y="110" width="130" height="40" fill="#5a4026"/>'
                   for x in (120, 380, 1450, 1710))
    braz = [(560, 690), (1360, 690)]
    css = TORCH_CSS + """
    #§bg { background: linear-gradient(180deg, #1a100a 0%, #2e1c10 50%, #120a06 100%); }
    #§pha { position: absolute; inset: 0; transform-origin: 960px 760px; }
    #§heat { opacity: 0; background: radial-gradient(ellipse at 50% 60%, rgba(255,140,60,0.35), rgba(0,0,0,0) 60%); }
"""
    court = f'<g fill="#0a0604" transform="translate(0,940)">{crowd(10, 280, 700, 120, 61)}{crowd(10, 1220, 1640, 120, 62)}</g>'
    markup = f"""
      <div id="§bg" class="§full"></div>
      {svg('<defs><linearGradient id="§col" x1="0" x2="1"><stop offset="0" stop-color="#2b2116"/><stop offset="0.45" stop-color="#7a5e3a"/><stop offset="1" stop-color="#21190f"/></linearGradient></defs>'
           + '<rect x="0" y="760" width="1920" height="320" fill="#24170e"/><rect x="760" y="700" width="400" height="70" fill="#4a3220"/><rect x="800" y="660" width="320" height="50" fill="#5a3e26"/>' + cols + court)}
      {torches("§bz", [(x, y) for x, y in braz], t)}
      <div id="§heat" class="§full"></div>
      <div id="§pha">{svg(pharaoh(960, 660, 1.3))}</div>"""
    t.to("#§pha", "scale: 1", "scale: 1.18", L[4], 1.8, "power2.out")
    t.fade("#§heat", 0, 1, L[4], 1.5)
    return css, markup


def arena(t, L, E, D):
    """The festival: crowds on the stands, ropes and staffs that seem to move, a great snake that
    swallows them, the magicians falling in prostration, Pharaoh on his dais."""
    ropes = "".join(f'<path id="§rp{k}" d="M {x} 900 c 30 -30 60 30 90 0 s 60 30 90 0 s 60 30 90 0" stroke="#8a6a44" stroke-width="10" fill="none" stroke-linecap="round"/>'
                    for k, x in enumerate(range(380, 1500, 140)))
    mags = "".join(f'<g id="§mg{k}" transform="translate({520 + k * 110},960)">{person(0, 120)}</g>' for k in range(9))
    css = """
    #§sky { background: linear-gradient(180deg, #6a8ab0 0%, #d8c09a 60%, #a07a52 70%); }
    #§ropes, #§big { position: absolute; inset: 0; }
    #§big { opacity: 0; }
"""
    stands = ('<path d="M 0 520 L 1920 520 L 1920 760 L 0 760 Z" fill="#6a5034"/>'
              + f'<g fill="#2a1d14" transform="translate(0,600)">{crowd(70, 0, 1920, 60, 71)}</g>'
              + f'<g fill="#2a1d14" transform="translate(0,700)">{crowd(60, 0, 1920, 70, 72)}</g>'
              + '<rect x="0" y="760" width="1920" height="320" fill="#b08a5a"/>')
    markup = f"""
      <div id="§sky" class="§full"></div>
      {svg(stands + pharaoh(1740, 640, 0.55, "§phs"))}
      <div id="§ropes">{svg(ropes)}</div>
      <div id="§big">{svg(f'<g id="§sn" transform="translate(960,900) scale(2.1)">{SNAKE}</g>')}</div>
      {svg(f'<g fill="#1a120c">{mags}</g>', "§mags")}"""
    for k in range(8):
        t.loop(f"#§rp{k}", "skewX: -10, y: 0", "skewX: 10, y: -8", 0.3 + (k % 3) * 0.05, L[2])
    big = L[4] + 0.4
    t.fade("#§big", 0, 1, big, 0.5)
    t.loop("#§sn", "x: -40", "x: 40", 0.45, big)
    t.fade("#§ropes", 1, 0, big + 1.2, 1.0)
    t.fade("#§big", 1, 0, L[6] - 0.3, 0.8)
    for k in range(9):
        t.to(f"#§mg{k}", "rotation: 0, scaleY: 1", "rotation: 0, scaleY: 0.42", L[6] + 0.4 + k * 0.12, 0.7, "power2.in")
    t.js.append('tl.set("#§mags g", {transformOrigin: "50% 100%"}, 0);')
    return css, markup


def plagues(t, L, E, D):
    """The signs, one after another while the verse is read: flood, locusts, lice, frogs, blood;
    then the night of the exodus."""
    s0, s1 = L[1], E[1]
    step = (s1 - s0) / 5
    r = random.Random(81)
    locusts = "".join(f'<div id="§lc{k}" class="§lc" style="left:{r.uniform(-200, 1900):.0f}px;top:{r.uniform(100, 800):.0f}px"></div>' for k in range(120))
    lice = "".join(f'<div class="§li" style="left:{r.uniform(0, 1920):.0f}px;top:{r.uniform(0, 1080):.0f}px"></div>' for k in range(300))
    frogs = "".join(f'<div id="§fr{k}" class="§fr" style="left:{r.uniform(100, 1800):.0f}px;top:{r.uniform(780, 1000):.0f}px"></div>' for k in range(26))
    css = """
    #§base { background: linear-gradient(180deg, #2a3040 0%, #6a6a6a 55%, #4a3a2a 62%, #2a1c12 100%); }
    #§flood { position: absolute; left: 0; right: 0; bottom: 0; height: 0; background: linear-gradient(180deg, rgba(90,120,160,0.85), rgba(30,50,80,0.95)); }
    .§lc { position: absolute; width: 16px; height: 6px; border-radius: 50%; background: #2a2414; }
    #§locs, #§lice, #§frogs, #§blood, #§exo { position: absolute; inset: 0; opacity: 0; }
    .§li { position: absolute; width: 4px; height: 4px; border-radius: 50%; background: #1a1410; }
    .§fr { position: absolute; width: 46px; height: 30px; border-radius: 50% 50% 40% 40%; background: #4a7a2a; box-shadow: inset 0 -6px 0 #2a4a1a; }
    #§blood { background: linear-gradient(180deg, rgba(0,0,0,0) 55%, #7a1410 60%, #4a0a08 100%); }
    #§exo { background: linear-gradient(180deg, #02030a 0%, #0b1026 70%, #151a2c 100%); }
"""
    markup = f"""
      <div id="§base" class="§full"></div>
      {svg(pyramids(660, "#3a2a20") + '<rect x="0" y="650" width="1920" height="430" fill="#3a2a1c"/>')}
      <div id="§flood"></div>
      <div id="§locs">{locusts}</div><div id="§lice">{lice}</div><div id="§frogs">{frogs}</div><div id="§blood"></div>
      <div id="§exo">{starfield("§x", 90, 82, (0, 0, W, 560), t)}{moon(1500, 120, 100)}
        {svg(f'<rect x="0" y="760" width="1920" height="320" fill="#100c0c"/><g id="§walk" fill="#05050a" transform="translate(0,820)">{crowd(70, 300, 1700, 60, 83)}</g>')}</div>"""
    t.to("#§flood", "height: 0", "height: 420", s0, step, "sine.inOut")
    t.to("#§flood", "height: 420", "height: 0", s0 + step, 0.6, "sine.inOut")
    t.fade("#§locs", 0, 1, s0 + step, 0.3)
    for k in range(120):
        t.cycle(f"#§lc{k}", "x: 0, y: 0", f"x: {r.uniform(300, 700):.0f}, y: {r.uniform(-80, 80):.0f}", r.uniform(0.8, 1.6), s0 + step)
    t.fade("#§locs", 1, 0, s0 + 2 * step, 0.3)
    t.fade("#§lice", 0, 1, s0 + 2 * step, 0.3)
    t.fade("#§lice", 1, 0, s0 + 3 * step, 0.3)
    t.fade("#§frogs", 0, 1, s0 + 3 * step, 0.3)
    for k in range(26):
        t.loop(f"#§fr{k}", "y: 0", "y: -40", 0.25 + (k % 5) * 0.04, s0 + 3 * step)
    t.fade("#§frogs", 1, 0, s0 + 4 * step, 0.3)
    t.fade("#§blood", 0, 1, s0 + 4 * step, 0.5)
    t.fade("#§exo", 0, 1, L[5] - 0.2, 1.2)
    t.to("#§walk", "x: 300", "x: -300", L[5], D - L[5], "none")
    return css, markup


def water_wall(id_, x, w, flip=False):
    """A towering wall of sea water."""
    lip = f'M {x} 300 Q {x + w * 0.5} 250 {x + w} 300'
    return (f'<g id="{id_}"><rect x="{x}" y="300" width="{w}" height="780" fill="url(#§wg)"/>'
            f'<path d="{lip} L {x + w} 330 L {x} 330 Z" fill="#cfe4f2" opacity="0.8"/></g>')


def parting(t, L, E, D):
    """Dawn: the crowd on the shore, the army's dust behind; the sea splits into two towering walls
    and a dry path opens; the crowd crosses."""
    css = """
    #§sky { background: linear-gradient(180deg, #2a3a5e 0%, #c9876a 48%, #f3c08a 58%, #6a8aa0 62%); }
    #§sea { position: absolute; inset: 0; }
    #§split { position: absolute; inset: 0; opacity: 0; }
    #§dust { position: absolute; left: 1500px; top: 520px; width: 700px; height: 260px; border-radius: 50%;
      background: radial-gradient(ellipse, rgba(200,160,110,0.7), rgba(200,160,110,0) 70%); }
"""
    markup = f"""
      <div id="§sky" class="§full"></div><div id="§dust"></div>
      <div id="§sea">{sea_band(t, "§w1", 600, 12, "#3a5a7a", 15)}{sea_band(t, "§w2", 680, 16, "#2a4a6a", 11)}</div>
      <div id="§split">{svg('<defs><linearGradient id="§wg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a9ac0"/><stop offset="1" stop-color="#1a3a5a"/></linearGradient></defs>'
           + '<rect x="0" y="560" width="1920" height="520" fill="#c9a26a"/><path d="M 820 560 L 1100 560 L 1500 1080 L 420 1080 Z" fill="#b08a56"/>'
           + water_wall("§lw", 0, 820) + water_wall("§rw", 1100, 820))}</div>
      {svg(f'<rect x="0" y="900" width="1920" height="180" fill="#8a6a46"/><g id="§people" fill="#1a120c" transform="translate(0,960)">{crowd(80, 100, 1820, 70, 91)}</g>')}"""
    t.loop("#§dust", "x: 0, opacity: 0.7", "x: -60, opacity: 1", 2)
    sp = L[4] + 3.0
    t.fade("#§split", 0, 1, sp, 1.2)
    t.fade("#§sea", 1, 0, sp, 1.2)
    t.to("#§lw", "y: 500", "y: 0", sp, 2.5, "power2.out")
    t.to("#§rw", "y: 500", "y: 0", sp, 2.5, "power2.out")
    t.to("#§people", "y: 960, scale: 1", "y: 760, scale: 0.55", L[5], E[5] - L[5] + 1.5, "sine.in")
    t.js.append('tl.set("#§people", {transformOrigin: "50% 0%"}, 0);')
    return css, markup


def drown(t, L, E, D):
    """The army in the dry path between the walls; the walls collapse; foam; then a calm sea."""
    r = random.Random(101)
    pts = [(r.uniform(700, 1220), r.uniform(650, 760)) for _ in range(30)]
    css = TORCH_CSS + """
    #§sky { background: linear-gradient(180deg, #2a2a4e 0%, #8a6a7a 50%, #c9a08a 62%); }
    #§army { position: absolute; inset: 0; }
    #§foam { opacity: 0; background: radial-gradient(ellipse at 50% 70%, rgba(240,250,255,0.85), rgba(200,230,250,0.2) 50%, rgba(0,0,0,0) 75%); }
    #§calm { opacity: 0; }
"""
    markup = f"""
      <div id="§sky" class="§full"></div>
      {svg('<defs><linearGradient id="§wg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a7aa0"/><stop offset="1" stop-color="#0a2040"/></linearGradient></defs>'
           + '<rect x="0" y="560" width="1920" height="520" fill="#8a6a46"/>')}
      <div id="§army">{svg(f'<g fill="#0a0606" transform="translate(0,800)">{crowd(60, 700, 1220, 80, 102, True)}</g>')}{torches("§at", pts, t)}</div>
      {svg(water_wall("§lw", 0, 760) + water_wall("§rw", 1160, 760))}
      <div id="§foam" class="§full"></div>
      <div id="§calm" class="§full"><div class="§full" style="background:linear-gradient(180deg,#1a2440 0%,#6a7a9a 45%,#9ab0c8 58%,#2a4a6a 60%,#0a2040 100%)"></div>
        {sea_band(t, "§c1", 640, 10, "#2a4a6a", 18)}{sea_band(t, "§c2", 740, 12, "#1a3a5a", 14)}</div>"""
    t.to("#§army", "x: -200", "x: 100", 0, L[1] + 1.5, "none")
    c0 = L[1] + 2.2
    t.to("#§lw", "x: 0", "x: 420", c0, 1.0, "power2.in")
    t.to("#§rw", "x: 0", "x: -420", c0, 1.0, "power2.in")
    t.fade("#§army", 1, 0, c0 + 0.8, 0.4)
    t.fade("#§foam", 0, 1, c0 + 0.8, 0.3)
    t.fade("#§foam", 1, 0, c0 + 1.4, 2.0)
    t.fade("#§calm", 0, 1, c0 + 1.2, 1.5)
    return css, markup


def lesson2(t, L, E, D):
    """Night over a calm sea, the stars turning slowly."""
    css = """
    #§nsky { background: radial-gradient(ellipse at 50% 100%, #1a2240 0%, #0a0e20 55%, #03040a 100%); }
    #§spin { position:absolute; left: -400px; top: -900px; width: 2720px; height: 2720px; transform-origin: 50% 50%; }
    #§path { position: absolute; left: 760px; top: 600px; width: 400px; height: 480px;
      background: radial-gradient(ellipse 30% 55% at 50% 10%, rgba(230,236,255,0.35), rgba(230,236,255,0) 100%); }
"""
    markup = f"""
      <div id="§nsky" class="§full"></div>
      <div id="§spin">{starfield("§l", 220, 111, (0, 0, 2720, 2720), t, (1.5, 3.5))}</div>
      {moon(900, 360, 120)}
      <div class="§full" style="top:640px;background:linear-gradient(180deg,#0f1c34,#050a14)"></div>
      <div id="§path"></div>
      {sea_band(t, "§l1", 700, 6, "#13223e", 22)}{sea_band(t, "§l2", 820, 10, "#0b1628", 16)}"""
    t.to("#§spin", "rotation: 0", "rotation: 12", 0, D, "none")
    t.loop("#§path", "opacity: 0.6", "opacity: 1", 2)
    return css, markup


SCENES = {"hook": hook, "palace": palace, "river": river, "city": city, "madyan": madyan, "tur": tur, "tur2": tur2,
          "throne": throne, "arena": arena, "plagues": plagues, "parting": parting, "drown": drown, "lesson2": lesson2}
