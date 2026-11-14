"""Build a Haq Stories Short (HyperFrames project) from a spec + narration timings.

Usage: python build_short.py <project_dir>

Reads <project_dir>/spec.json and <project_dir>/assets/timings.json (from tts.py).
Writes index.html and compositions/*.html. One beat per narration line.

spec.json:
{
  "accent": "#f2a33a",            # highlight colour for *words*, chips, embers
  "embers": true,                  # rising sparks in warm moods
  "beats": [
    {"text": "They built a *fire* to burn him…", "sub": "Then Allah gave it one command.",
     "mood": {"warm": 0.6, "cool": 0}, "ref": "Al-Anbiya 21:68", "reveal": false},
    {"arabic": "…", "translation": "…", "ref": "…", "mood": {...}},
    {"cta": true, "text": "Follow for more stories of the prophets."}
  ]
}
The number of beats must equal the number of narration lines.
"""
import html
import wave
import json
import random
import re
import sys
from pathlib import Path

W, H = 1080, 1920
HOLD_END = 1.4  # seconds the last frame holds after the voice ends
LEAD = 0.15     # a beat appears this long before its line is spoken

FONT_FACES = """
      @font-face { font-family: "Cormorant Garamond"; font-weight: 600; font-style: normal;
        src: url("assets/fonts/cormorant-garamond-latin-600-normal.woff2") format("woff2"); }
      @font-face { font-family: "Cormorant Garamond"; font-weight: 600; font-style: italic;
        src: url("assets/fonts/cormorant-garamond-latin-600-italic.woff2") format("woff2"); }
      @font-face { font-family: "Noto Nastaliq Urdu"; font-weight: 400;
        src: url("assets/fonts/noto-nastaliq-urdu-arabic-400-normal.woff2") format("woff2"); }
      @font-face { font-family: "Amiri Quran"; font-weight: 400;
        src: url("assets/fonts/amiri-quran-arabic-400-normal.woff2") format("woff2"); }
"""


def esc(s: str) -> str:
    return html.escape(s, quote=True).replace("ﷺ", '<span class="saw">ﷺ</span>')


def words_html(text: str, prefix: str) -> tuple[str, int]:
    """*word* -> accent. Returns markup with one span per word and the word count."""
    out, n = [], 0
    for tok in text.split():
        hi = tok.startswith("*") or tok.endswith("*") or "*" in tok
        clean = tok.replace("*", "")
        cls = "w hi" if hi else "w"
        out.append(f'<span class="{cls}" id="{prefix}-w{n}">{esc(clean)}</span>')
        n += 1
    return " ".join(out), n


def beat_html(i: int, beat: dict, dur: float, spoken: float, accent: str) -> str:
    bid = f"b{i + 1}"
    parts, js = [], []
    reveal = beat.get("reveal", i != 0)  # frame 0 is the thumbnail: the hook is already there

    if beat.get("arabic"):
        ars = f' style="font-size:{beat["ar_size"]}px"' if beat.get("ar_size") else ""
        parts.append(f'<div id="{bid}-ar" class="ar" dir="rtl" lang="ar"{ars}>{esc(beat["arabic"])}</div>')
        parts.append(f'<div id="{bid}-tr" class="tr">{esc(beat["translation"])}</div>')
        js.append(f'tl.fromTo("#{bid}-ar", {{opacity: 0, y: 30, filter: "blur(10px)"}}, '
                  f'{{opacity: 1, y: 0, filter: "blur(0px)", duration: 0.9, ease: "power2.out"}}, 0.05);')
        js.append(f'tl.fromTo("#{bid}-tr", {{opacity: 0, y: 20}}, '
                  f'{{opacity: 1, y: 0, duration: 0.7, ease: "power2.out"}}, 0.6);')
    elif beat.get("cta"):
        words, n = words_html(beat["text"], bid)
        parts.append(f'<div id="{bid}-cta-mark" class="mark">حق کہانیاں</div>')
        parts.append(f'<div id="{bid}-txt" class="txt cta">{words}</div>')
        parts.append(f'<div id="{bid}-btn" class="btn">Follow · Haq Stories</div>')
        js.append(f'tl.fromTo("#{bid}-cta-mark", {{opacity: 0, scale: 0.92}}, '
                  f'{{opacity: 1, scale: 1, duration: 0.8, ease: "power2.out"}}, 0);')
        js.append(f'tl.fromTo("#{bid} .w", {{opacity: 0, y: 18}}, {{opacity: 1, y: 0, duration: 0.35, '
                  f'ease: "power2.out", stagger: {max(spoken * 0.7 / max(n, 1), 0.04):.3f}}}, 0.15);')
        js.append(f'tl.fromTo("#{bid}-btn", {{opacity: 0, y: 24}}, '
                  f'{{opacity: 1, y: 0, duration: 0.5, ease: "back.out(1.6)"}}, 0.5);')
    else:
        words, n = words_html(beat["text"], bid)
        size = beat.get("size")
        style = f' style="font-size:{size}px"' if size else ""
        cls = "txt hook" if beat.get("hook") else "txt"
        parts.append(f'<div id="{bid}-txt" class="{cls}"{style}>{words}</div>')
        if beat.get("sub"):
            parts.append(f'<div id="{bid}-sub" class="sub">{esc(beat["sub"])}</div>')
        if reveal:
            stagger = max(spoken * 0.78 / max(n, 1), 0.04)
            js.append(f'tl.fromTo("#{bid} .w", {{opacity: 0, y: 22, filter: "blur(6px)"}}, '
                      f'{{opacity: 1, y: 0, filter: "blur(0px)", duration: 0.32, ease: "power2.out", '
                      f'stagger: {stagger:.3f}}}, 0.12);')
        else:
            # Hook: fully on screen at frame 0, then breathes.
            if beat.get("hook"):
                # Every word is readable on frame 0 and lands with a punch in the first half second.
                js.append(f'tl.fromTo("#{bid}-txt", {{scale: 1.18}}, {{scale: 1, duration: 0.35, ease: "back.out(2)"}}, 0);')
            else:
                js.append(f'tl.fromTo("#{bid}-txt", {{scale: 1}}, {{scale: 1.04, duration: {dur:.2f}, ease: "none"}}, 0);')
            if beat.get("sub"):
                js.append(f'tl.fromTo("#{bid}-sub", {{opacity: 0, y: 16}}, '
                          f'{{opacity: 1, y: 0, duration: 0.5, ease: "power2.out"}}, {spoken * 0.45:.2f});')
        js.append(f'tl.fromTo("#{bid} .hi", {{textShadow: "0 0 0px rgba(0,0,0,0)"}}, '
                  f'{{textShadow: "0 0 28px var(--accent)", duration: 0.6, ease: "power1.out"}}, {spoken * 0.5:.2f});')

    if beat.get("options"):
        correct = beat.get("correct")
        rows = []
        for k, opt in enumerate(beat["options"]):
            cls = "opt"
            if correct is not None:
                cls += " right" if k == correct else " wrong"
            rows.append(f'<div id="{bid}-o{k}" class="{cls}"><b>{"ABC"[k]}</b>{esc(opt)}</div>')
        parts.append(f'<div id="{bid}-opts" class="opts">{"".join(rows)}</div>')
        if correct is None:
            at = beat.get("opt_at") or [0.6 + 0.55 * k for k in range(len(beat["options"]))]
            for k, t in enumerate(at):
                js.append(f'tl.fromTo("#{bid}-o{k}", {{opacity: 0, x: -30}}, {{opacity: 1, x: 0, duration: 0.3, '
                          f'ease: "power2.out"}}, {t:.2f});')
        else:
            js.append(f'tl.fromTo("#{bid} .wrong", {{opacity: 1}}, {{opacity: 0.3, duration: 0.4}}, 0.7);')
            js.append(f'tl.fromTo("#{bid} .right", {{scale: 1}}, {{scale: 1.06, duration: 0.35, ease: "back.out(2)"}}, 0.7);')
        if beat.get("count"):
            # "Three, two, one" closes the spoken line.
            for c, at in zip("321", beat.get("count_at") or (spoken - 1.75, spoken - 1.15, spoken - 0.55)):
                parts.append(f'<div id="{bid}-c{c}" class="count">{c}</div>')
                js.append(f'tl.fromTo("#{bid}-c{c}", {{opacity: 0, scale: 1.4}}, {{keyframes: [{{opacity: 1, scale: 1, duration: 0.2}}, '
                          f'{{opacity: 0, duration: 0.25, delay: 0.25}}]}}, {max(at, 0.1):.2f});')

    if beat.get("lights"):
        parts.append(f'<div id="{bid}-orbs" class="orbs"><div id="{bid}-orb1" class="orb"></div><div id="{bid}-orb2" class="orb"></div></div>')
        js.append(f'tl.fromTo("#{bid}-orbs", {{y: 260, opacity: 0}}, {{y: -60, opacity: 1, duration: {dur:.2f}, ease: "sine.out"}}, 0);')
        js.append(f'tl.fromTo("#{bid}-orb1", {{x: -150}}, {{x: -70, duration: {dur:.2f}, ease: "sine.inOut"}}, 0);')
        js.append(f'tl.fromTo("#{bid}-orb2", {{x: 150}}, {{x: 70, duration: {dur:.2f}, ease: "sine.inOut"}}, 0);')

    if beat.get("ur"):
        parts.append(f'<div id="{bid}-ur" class="ur" dir="rtl" lang="ur" data-layout-allow-overflow>{esc(beat["ur"])}</div>')
        js.append(f'tl.fromTo("#{bid}-ur", {{opacity: 0, y: 10}}, {{opacity: 1, y: 0, duration: 0.35, ease: "power2.out"}}, 0.15);')

    if beat.get("ref"):
        parts.append(f'<div id="{bid}-ref" class="ref">{esc(beat["ref"])}</div>')
        js.append(f'tl.fromTo("#{bid}-ref", {{opacity: 0, y: 12}}, '
                  f'{{opacity: 1, y: 0, duration: 0.45, ease: "power2.out"}}, 0.35);')

    # Every beat but the last leaves the same way, landing just before its end.
    if not beat.get("cta"):
        js.append(f'tl.fromTo("#{bid}-wrap", {{opacity: 1}}, {{opacity: 0, duration: 0.22, ease: "power1.in"}}, {dur - 0.24:.2f});')

    body = "\n      ".join(parts)
    side, rail = (60, 60) if beat.get("arabic") or beat.get("cta") else (90, beat.get("_text_right", 140))
    allow = " data-layout-allow-overflow" if beat.get("lights") else ""
    script = "\n    ".join(js)
    return f"""<template>
  <style>
    #{bid} {{ position: absolute; inset: 0; }}
    #{bid}-wrap {{ position: absolute; left: {side}px; right: {rail}px; top: {beat["_top"]}px; bottom: {beat["_bottom"]}px;
      display: flex; flex-direction: column; justify-content: center; gap: 34px; }}
  </style>
  <div id="{bid}" data-composition-id="{bid}" data-width="{W}" data-height="{H}">
    <div id="{bid}-wrap" class="clip" data-start="0" data-duration="{dur:.2f}"{allow}>
      {body}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {script}
    window.__timelines["{bid}"] = tl;
  </script>
</template>
"""


def jagged(cx: float, cy: float, rx: float, ry: float, n: int, rough: float, seed: int) -> str:
    """A rough, rock-like closed outline around an ellipse."""
    import math
    rnd = random.Random(seed)
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        f = 1 + rnd.uniform(-rough, rough)
        pts.append((cx + rx * f * math.cos(a), cy + ry * f * math.sin(a)))
    # Smooth curves through the midpoints: rounded, uneven rock instead of spikes.
    mids = [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2) for i in range(n)]
    d = f"M {mids[-1][0]:.0f} {mids[-1][1]:.0f} "
    d += " ".join(f"Q {pts[i][0]:.0f} {pts[i][1]:.0f} {mids[i][0]:.0f} {mids[i][1]:.0f}" for i in range(n))
    return d + " Z"


def cave_scene(total: float) -> tuple[str, str, str]:
    """Inside a cave, looking out at a moonlit valley. Returns (css, markup, js)."""
    rnd = random.Random(19)
    stars, sjs = [], []
    for k in range(60):
        x, y = rnd.uniform(240, 840), rnd.uniform(300, 900)
        r = rnd.uniform(1.5, 4)
        stars.append(f'<div id="st{k}" class="st" style="left:{x:.0f}px;top:{y:.0f}px;width:{r:.1f}px;height:{r:.1f}px"></div>')
        period = rnd.uniform(1.6, 3.4)
        sjs.append(f'tl.fromTo("#st{k}", {{opacity: {rnd.uniform(0.25, 0.5):.2f}}}, {{opacity: 1, duration: {period / 2:.2f}, '
                   f'ease: "sine.inOut", yoyo: true, repeat: {int(total / (period / 2)) + 1}}}, {rnd.uniform(0, 1.2):.2f});')
    back = jagged(540, 700, 385, 470, 22, 0.10, 3)
    front = jagged(540, 725, 335, 425, 18, 0.13, 5)
    frame = "M -60 -60 H 1140 V 1980 H -60 Z "
    css = """
    #night { position: absolute; inset: 0; background: linear-gradient(180deg, #0b1830 0%, #1a2b4a 55%, #0e1626 100%); }
    .st { position: absolute; border-radius: 50%; background: #eef4ff; box-shadow: 0 0 6px rgba(220,235,255,0.9); }
    #moon { position: absolute; left: 610px; top: 420px; width: 110px; height: 110px; border-radius: 50%;
      background: radial-gradient(circle at 40% 38%, #fffdf3 0%, #ece6d2 60%, #d6cfb8 100%);
      box-shadow: 0 0 60px 20px rgba(230,236,255,0.35), 0 0 180px 60px rgba(160,190,255,0.18); }
    #hills { position: absolute; inset: 0; width: 100%; height: 100%; }
    #rock-wrap { position: absolute; inset: -60px; }
    #rock { position: absolute; inset: 0; width: 100%; height: 100%; }
"""
    markup = f"""
    <div id="night" class="clip" data-start="0" data-duration="{total:.2f}">
      {"".join(stars)}
      <div id="moon"></div>
      <svg id="hills" viewBox="0 0 1080 1920" preserveAspectRatio="none">
        <path fill="#101a2d" d="M 0 1010 C 160 930 300 960 420 1000 C 560 1046 700 930 860 960 C 960 980 1030 1000 1080 990 V 1920 H 0 Z"/>
        <path fill="#0a111e" d="M 0 1070 C 200 1020 330 1060 500 1080 C 660 1100 820 1030 1080 1060 V 1920 H 0 Z"/>
      </svg>
    </div>
    <div id="cave" class="clip" data-start="0" data-duration="{total:.2f}">
      <div id="rock-wrap">
        <svg id="rock" viewBox="-60 -60 1200 2040" preserveAspectRatio="none">
          <defs>
            <radialGradient id="rockb" cx="540" cy="700" r="900" gradientUnits="userSpaceOnUse">
              <stop offset="0" stop-color="#3a3542"/><stop offset="0.45" stop-color="#1c1922"/><stop offset="1" stop-color="#0a090c"/>
            </radialGradient>
            <radialGradient id="rockf" cx="540" cy="720" r="1300" gradientUnits="userSpaceOnUse">
              <stop offset="0" stop-color="#17141c"/><stop offset="0.4" stop-color="#0b0a0e"/><stop offset="1" stop-color="#030204"/>
            </radialGradient>
          </defs>
          <path fill="url(#rockb)" fill-rule="evenodd" d="{frame}{back}"/>
          <path fill="url(#rockf)" fill-rule="evenodd" d="{frame}{front}"/>
        </svg>
      </div>
    </div>"""
    js = "\n    ".join(sjs) + (f'\n    tl.fromTo("#rock-wrap", {{scale: 1}}, {{scale: 1.12, duration: {total:.2f}, ease: "none"}}, 0);'
                                f'\n    tl.fromTo("#moon", {{y: 0}}, {{y: -30, duration: {total:.2f}, ease: "none"}}, 0);')
    return css, markup, js


def storm_scene(spec: dict, beats: list, total: float) -> tuple[str, str, str]:
    """Night storm with rain and lightning that clears into dawn. Returns (css, markup, js)."""
    rnd = random.Random(23)
    drops, djs = [], []
    for k in range(90):
        x = rnd.uniform(-100, W + 60)
        h = rnd.uniform(60, 120)
        period = rnd.uniform(0.55, 0.9)
        drops.append(f'<div id="rd{k}" class="rd" style="left:{x:.0f}px;height:{h:.0f}px;opacity:{rnd.uniform(0.25, 0.6):.2f}"></div>')
        djs.append(f'rt.fromTo("#rd{k}", {{y: -200, x: 0, rotation: 12}}, {{y: 2150, x: -440, rotation: 12, duration: {period:.2f}, '
                   f'ease: "none", repeat: {int((total + 3) / period) + 1}}}, {3 - rnd.uniform(0, period):.2f});')
    clouds = []
    for k in range(5):
        clouds.append(f'<div id="cl{k}" class="cl" style="left:{rnd.uniform(-500, 500):.0f}px;top:{rnd.uniform(-200, 500):.0f}px"></div>')
    sun_at = beats[spec.get("sunrise_beat", 0)]["start"]
    flashes = "".join(
        f'\n    tl.fromTo("#bolt", {{opacity: 0}}, {{keyframes: [{{opacity: 0.85, duration: 0.05}}, {{opacity: 0.1, duration: 0.08}}, '
        f'{{opacity: 0.6, duration: 0.05}}, {{opacity: 0, duration: 0.4}}], immediateRender: false}}, {t:.2f});' for t in spec.get("lightning", []))
    css = """
    #stormsky { position: absolute; inset: 0; background: linear-gradient(180deg, #0b0f17 0%, #161c28 50%, #0e1118 100%); }
    .cl { position: absolute; width: 1400px; height: 700px; border-radius: 50%;
      background: radial-gradient(ellipse at 50% 50%, rgba(70,80,100,0.45) 0%, rgba(40,46,60,0.25) 45%, rgba(0,0,0,0) 70%); }
    #sun { position: absolute; left: 390px; top: 1300px; width: 300px; height: 300px; border-radius: 50%; opacity: 0;
      background: radial-gradient(circle, #fff3d6 0%, #ffd38a 35%, rgba(255,170,80,0.5) 60%, rgba(255,140,60,0) 72%); }
    #bolt { position: absolute; inset: 0; background: radial-gradient(ellipse at 60% 20%, rgba(220,230,255,0.9), rgba(160,180,230,0.3) 50%, rgba(0,0,0,0) 80%); opacity: 0; }
    #rain-g { position: absolute; inset: 0; }
    .rd { position: absolute; top: 0; width: 2px; background: linear-gradient(180deg, rgba(200,215,240,0), rgba(200,215,240,0.8)); }
"""
    markup = f"""
    <div id="storm" class="clip" data-start="0" data-duration="{total:.2f}">
      <div id="stormsky"></div>
      {"".join(clouds)}
      <div id="sun"></div>
      <div id="bolt"></div>
    </div>
    <div id="rain" class="clip" data-start="0" data-duration="{total:.2f}"><div id="rain-g" style="opacity:{beats[0]["mood"].get("rain", 0)}">
      {"".join(drops)}
    </div></div>"""
    cjs = "".join(f'\n    tl.fromTo("#cl{k}", {{x: 0}}, {{x: {(-1) ** k * 160}, duration: {total:.2f}, ease: "none"}}, 0);' for k in range(5))
    js = ("const rt = gsap.timeline({ paused: true });\n    " + "\n    ".join(djs)
          + f"\n    tl.add(rt.tweenFromTo(3, {3 + total:.2f}, {{ ease: \"none\" }}), 0);"
          + cjs + flashes
          + f'\n    tl.fromTo("#sun", {{y: 0, opacity: 0}}, {{y: -190, opacity: 1, duration: 5, ease: "sine.out", immediateRender: false}}, {sun_at:.2f});'
          + f'\n    tl.fromTo("#stormsky", {{opacity: 1}}, {{opacity: 0.35, duration: 4, ease: "sine.inOut", immediateRender: false}}, {sun_at:.2f});')
    return css, markup, js


def mosque_scene(spec: dict, beats: list, total: float) -> tuple[str, str, str]:
    """A simple old mosque at night: palm pillars, palm-leaf roof, lamps, the trunk, the pulpit.
    No people are shown. Returns (css, markup, js)."""
    rnd = random.Random(31)
    pillars = []
    for k, (x, w, shade) in enumerate([(40, 34, 0.55), (230, 26, 0.4), (420, 22, 0.32), (600, 22, 0.32), (760, 26, 0.4)]):
        pillars.append(f'<div class="pil" style="left:{x}px;width:{w}px;opacity:{shade}"></div>')
    lamps, ljs = [], []
    for k, (x, y) in enumerate([(250, 520), (540, 470), (720, 560)]):
        lamps.append(f'<div class="lampcord" style="left:{x + 9}px;height:{y - 250}px"></div>'
                     f'<div id="lamp{k}" class="lamp" style="left:{x}px;top:{y}px"></div>')
        period = rnd.uniform(0.18, 0.32)
        ljs.append(f'tl.fromTo("#lamp{k}", {{opacity: 0.75}}, {{opacity: 1, duration: {period:.2f}, ease: "sine.inOut", '
                   f'yoyo: true, repeat: {int(total / period) + 1}}}, {rnd.uniform(0, 0.3):.2f});')
    shafts = "".join(f'<div class="shaft" style="left:{x}px"></div>' for x in (150, 470, 760))
    pulpit_at = beats[spec.get("pulpit_beat", 1)]["start"]
    cry = beats[spec.get("cry_beat", 2)]
    cry_at, cry_end = cry["start"], cry["start"] + cry["dur"]
    hook_cry = spec.get("hook_cry", True)
    css = """
    #mosque { position: absolute; inset: 0; background: linear-gradient(180deg, #0b0a0e 0%, #17110d 55%, #1e150f 100%); }
    #wall { position: absolute; left: 0; right: 0; top: 260px; bottom: 380px;
      background: linear-gradient(180deg, #1d1612 0%, #2a1f17 100%); }
    #roof { position: absolute; left: 0; right: 0; top: 0; height: 270px;
      background: repeating-linear-gradient(90deg, #120d0a 0 26px, #1c140f 26px 30px, #0e0a08 30px 44px); }
    #roofbeam { position: absolute; left: 0; right: 0; top: 250px; height: 26px; background: #0d0907; }
    .shaft { position: absolute; top: 260px; width: 180px; height: 1200px;
      background: linear-gradient(180deg, rgba(190,210,255,0.16), rgba(190,210,255,0)); }
    #floor { position: absolute; left: 0; right: 0; bottom: 0; height: 400px;
      background: linear-gradient(180deg, #2b1f16 0%, #1a120d 100%); }
    .pil { position: absolute; top: 250px; bottom: 380px; border-radius: 6px;
      background: repeating-linear-gradient(180deg, #3a2a1d 0 22px, #2c2016 22px 26px); }
    .lampcord { position: absolute; top: 260px; width: 2px; background: rgba(60,45,30,0.9); }
    .lamp { position: absolute; width: 20px; height: 20px; border-radius: 50%;
      background: radial-gradient(circle, #fff1c9 0%, #ffbe5c 50%, rgba(255,160,60,0) 75%);
      box-shadow: 0 0 40px 18px rgba(255,170,70,0.35), 0 0 140px 60px rgba(255,150,60,0.12); }
    #trunk { position: absolute; left: 860px; top: 250px; width: 120px; bottom: 360px; border-radius: 14px 14px 8px 8px;
      background: repeating-linear-gradient(180deg, #7a5a3c 0 26px, #5a4129 26px 31px),
                  linear-gradient(90deg, rgba(0,0,0,0.35), rgba(255,220,170,0.12) 45%, rgba(0,0,0,0.45));
      background-blend-mode: multiply; box-shadow: 0 0 60px rgba(0,0,0,0.6); }
    #trunkbase { position: absolute; left: 840px; width: 160px; bottom: 340px; height: 40px; border-radius: 50%;
      background: #120c08; opacity: 0.7; }
    .ripple { position: absolute; left: 920px; top: 1020px; width: 300px; height: 300px; margin: -150px;
      border-radius: 50%; border: 6px solid rgba(255,214,150,0.75); opacity: 0; }
    #pulpit { position: absolute; left: 120px; bottom: 330px; width: 330px; height: 330px; opacity: 0; }
"""
    ripples = "".join(f'<div id="rp{k}" class="ripple"></div>' for k in range(3))
    markup = f"""
    <div id="mosque" class="clip" data-start="0" data-duration="{total:.2f}">
      <div id="wall"></div>
      {"".join(pillars)}
      <div id="roof"></div><div id="roofbeam"></div>
      {shafts}
      <div id="floor"></div>
      {"".join(lamps)}
      <svg id="pulpit" viewBox="0 0 330 330">
        <rect x="200" y="20" width="16" height="310" fill="#4a3322"/>
        <rect x="20" y="230" width="110" height="100" fill="#6a4a30"/>
        <rect x="110" y="150" width="110" height="180" fill="#7a5638"/>
        <rect x="200" y="70" width="110" height="260" fill="#86603e"/>
        <rect x="200" y="62" width="110" height="12" fill="#a37a52"/>
        <rect x="110" y="142" width="110" height="12" fill="#a37a52"/>
        <rect x="20" y="222" width="110" height="12" fill="#a37a52"/>
      </svg>
      <div id="trunkbase"></div>
      <div id="trunk"></div>
      {ripples}
    </div>"""
    js = ["\n    ".join(ljs)]
    js.append(f'tl.fromTo("#pulpit", {{opacity: 0, y: 40}}, {{opacity: 1, y: 0, duration: 1.2, ease: "power2.out", immediateRender: false}}, {pulpit_at + 0.6:.2f});')
    windows = [(cry_at, cry_end)] + ([(0.05, 2.8)] if hook_cry else [])
    for a, b in windows:
        n = int((b - a) / 0.09)
        js.append(f'tl.fromTo("#trunk", {{x: 0}}, {{x: 5, duration: 0.045, ease: "sine.inOut", yoyo: true, repeat: {n * 2 - 1}, immediateRender: false}}, {a:.2f});')
        for k in range(3):
            reps = max(int((b - a - 0.6 * k) / 1.8) - 1, 0)
            js.append(f'tl.fromTo("#rp{k}", {{scale: 0.3, opacity: 0.7}}, {{scale: 2.4, opacity: 0, duration: 1.8, ease: "power1.out", '
                      f'repeat: {reps}, immediateRender: false}}, {a + 0.6 * k:.2f});')
    js.append(f'tl.fromTo("#trunk", {{x: 0}}, {{x: 0, duration: 0.01, immediateRender: false}}, {cry_end:.2f});')
    return css, markup, "\n    ".join(js)


ANT = ('<g fill="#140d08"><ellipse cx="-11" cy="0" rx="7" ry="5"/><ellipse cx="0" cy="0" rx="5" ry="4"/>'
       '<ellipse cx="9" cy="-1" rx="4" ry="3.6"/><path d="M -4 2 L -9 9 M 0 3 L 0 10 M 3 2 L 8 9 M -4 -2 L -9 -8 M 0 -3 L 1 -9 M 3 -2 L 8 -8 '
       'M 11 -3 L 16 -9 M 11 -3 L 17 -4" stroke="#140d08" stroke-width="1.6" fill="none"/></g>')


def soldier(x: float, h: float) -> str:
    """A tiny faceless marching silhouette with a spear."""
    w = h * 0.28
    return (f'<g transform="translate({x:.0f},0)"><circle cx="0" cy="{-h + w * 0.55:.1f}" r="{w * 0.42:.1f}"/>'
            f'<rect x="{-w / 2:.1f}" y="{-h + w:.1f}" width="{w:.1f}" height="{h * 0.55:.1f}" rx="2"/>'
            f'<rect x="{-w / 2:.1f}" y="{-h * 0.26:.1f}" width="{w * 0.38:.1f}" height="{h * 0.26:.1f}"/>'
            f'<rect x="{w * 0.12:.1f}" y="{-h * 0.26:.1f}" width="{w * 0.38:.1f}" height="{h * 0.26:.1f}"/>'
            f'<rect x="{w * 0.55:.1f}" y="{-h * 1.35:.1f}" width="2" height="{h * 1.3:.1f}"/></g>')


def valley_scene(spec: dict, beats: list, total: float) -> tuple[str, str, str]:
    """The valley of the ants: an army on the horizon, birds, marching ants, one ant that calls.
    Sulaiman (AS) and the jinn are never shown. Returns (css, markup, js)."""
    rnd = random.Random(41)
    halt = beats[spec.get("halt_beat", 4)]["start"]
    call = beats[spec.get("call_beat", 3)]
    rush_at = call["start"]
    hero_at = beats[spec.get("hero_beat", 2)]["start"]

    army = []
    for row, (y, h, n, op) in enumerate([(1200, 62, 24, 0.85), (1232, 84, 20, 1.0)]):
        xs = [rnd.uniform(-40, 1500) for _ in range(n)]
        army.append(f'<g transform="translate(0,{y})" fill="#0d0a10" opacity="{op}">' + "".join(soldier(x, h) for x in xs) + "</g>")
    banners = "".join(
        f'<g transform="translate({x},1080)"><rect x="0" y="0" width="5" height="150" fill="#0d0a10"/>'
        f'<rect id="fl{k}" class="flag" x="5" y="2" width="64" height="40" fill="{c}"/></g>'
        for k, (x, c) in enumerate([(180, "#7a2e2a"), (520, "#2c4a6b"), (860, "#7a5a2a"), (1200, "#2f5a3a")]))
    birds, bjs = [], []
    for k in range(14):
        x, y, sc = rnd.uniform(0, 1500), rnd.uniform(1000, 1110), rnd.uniform(1.4, 2.2)
        birds.append(f'<g transform="translate({x:.0f},{y:.0f}) scale({sc:.2f})"><path id="bd{k}" class="bird" '
                     f'd="M -16 0 Q -8 -9 0 0 Q 8 -9 16 0" stroke="#0d0a10" stroke-width="3" fill="none"/></g>')
        per = rnd.uniform(0.28, 0.42)
        bjs.append(f'tl.fromTo("#bd{k}", {{scaleY: 1}}, {{scaleY: -0.6, transformOrigin: "50% 100%", duration: {per:.2f}, ease: "sine.inOut", yoyo: true, '
                   f'repeat: {int(total / per) + 1}}}, {rnd.uniform(0, 0.3):.2f});')

    ants, ajs = [], []
    hole_x, hole_y = 540, 1560
    for k in range(26):
        y0 = rnd.uniform(1430, 1800)
        x0 = rnd.choice([-60, 1140])
        per = rnd.uniform(5, 8)
        ants.append(f'<g transform="translate({x0},{y0:.0f})"><g id="an{k}" class="ant">'
                    f'<g transform="scale({1 if x0 < 0 else -1},1) scale(2.2)">{ANT}</g></g></g>')
        mid = rnd.uniform(0.25, 0.75)
        ajs.append(f'tl.fromTo("#an{k}", {{x: 0, y: 0, opacity: 1}}, {{x: {(hole_x - x0) * mid:.0f}, y: {(hole_y - y0) * mid * 0.4:.0f}, '
                   f'duration: {rush_at:.2f}, ease: "none"}}, 0);')
        ajs.append(f'tl.fromTo("#an{k}", {{x: {(hole_x - x0) * mid:.0f}, y: {(hole_y - y0) * mid * 0.4:.0f}, opacity: 1}}, '
                   f'{{x: {hole_x - x0}, y: {hole_y - y0:.0f}, opacity: 0, duration: {rnd.uniform(1.6, 3.2):.2f}, ease: "power1.in", '
                   f'immediateRender: false}}, {rush_at + rnd.uniform(0.2, 1.2):.2f});')

    css = """
    #vsky { position: absolute; inset: 0; background: linear-gradient(180deg, #0d1526 0%, #24304a 38%, #7a4a3a 52%, #d98a4e 62%, #f0b46a 66%, #3a2418 72%); }
    #vhills { position: absolute; inset: 0; width: 100%; height: 100%; }
    #army { position: absolute; left: 0; top: 0; width: 1500px; height: 1920px; }
    #vground { position: absolute; left: 0; right: 0; top: 1240px; bottom: 0;
      background: linear-gradient(180deg, #4a3220 0%, #2e2015 40%, #1c140e 100%); }
    #mound { position: absolute; left: 390px; top: 1500px; width: 300px; height: 130px; border-radius: 50% 50% 8% 8%;
      background: radial-gradient(ellipse at 50% 30%, #6a4a30, #3e2a1a 70%); }
    #hole { position: absolute; left: 515px; top: 1545px; width: 50px; height: 26px; border-radius: 50%; background: #0b0705; }
    #antsvg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
    #hero { position: absolute; left: 650px; top: 1390px; width: 300px; height: 180px; opacity: 0; }
    #pebble { position: absolute; left: 670px; top: 1490px; width: 260px; height: 80px; border-radius: 50%;
      background: radial-gradient(ellipse at 40% 30%, #8a7058, #4e3c2c 70%); opacity: 0; }
    .call { position: absolute; left: 800px; top: 1470px; width: 160px; height: 160px; margin: -80px; border-radius: 50%;
      border: 5px solid rgba(255,220,160,0.8); opacity: 0; }
"""
    calls = "".join(f'<div id="cr{k}" class="call"></div>' for k in range(3))
    markup = f"""
    <div id="valley" class="clip" data-start="0" data-duration="{total:.2f}">
      <div id="vsky"></div>
      <svg id="vhills" viewBox="0 0 1080 1920" preserveAspectRatio="none">
        <path fill="#3a2a34" d="M 0 1170 C 180 1120 320 1150 470 1165 C 640 1185 780 1110 1080 1150 V 1920 H 0 Z"/>
      </svg>
      <svg id="army" viewBox="0 0 1500 1920">
        {"".join(birds)}
        {"".join(army)}
        {banners}
      </svg>
      <div id="vground"></div>
      <div id="mound"></div><div id="hole"></div>
      <svg id="antsvg" viewBox="0 0 1080 1920">{"".join(ants)}</svg>
      <div id="pebble"></div>
      <svg id="hero" viewBox="-60 -40 120 80"><g transform="scale(2.6)">{ANT}</g></svg>
      {calls}
    </div>"""
    js = ["\n    ".join(bjs), "\n    ".join(ajs)]
    js.append(f'tl.fromTo("#army", {{x: 0}}, {{x: -420, duration: {halt:.2f}, ease: "none"}}, 0);')
    for k in range(4):
        js.append(f'tl.fromTo("#fl{k}", {{scaleX: 1}}, {{scaleX: 0.82, duration: 0.35, ease: "sine.inOut", yoyo: true, '
                  f'repeat: {int(total / 0.35) + 1}, transformOrigin: "0% 50%"}}, {k * 0.1:.2f});')
    js.append(f'tl.fromTo("#pebble", {{opacity: 0}}, {{opacity: 1, duration: 0.6, immediateRender: false}}, {hero_at:.2f});')
    js.append(f'tl.fromTo("#hero", {{opacity: 0, x: 60}}, {{opacity: 1, x: 0, duration: 0.9, ease: "power2.out", immediateRender: false}}, {hero_at + 0.2:.2f});')
    js.append(f'tl.fromTo("#hero", {{y: 0}}, {{y: -6, duration: 0.25, ease: "sine.inOut", yoyo: true, repeat: {int(call["dur"] / 0.25)}, immediateRender: false}}, {rush_at:.2f});')
    for k in range(3):
        reps = max(int((call["dur"] - 0.5 * k) / 1.5) - 1, 0)
        js.append(f'tl.fromTo("#cr{k}", {{scale: 0.4, opacity: 0.85}}, {{scale: 2.6, opacity: 0, duration: 1.5, ease: "power1.out", '
                  f'repeat: {reps}, immediateRender: false}}, {rush_at + 0.5 * k:.2f});')
    return css, markup, "\n    ".join(js)


def yusuf_scene(spec: dict, beats: list, total: float) -> tuple[str, str, str]:
    """Yusuf (AS) Part 1: a well at night, the dream sky, the brothers as distant shadows, and the
    view from inside the well. Yusuf (AS) and Yaqub (AS) are never shown. Returns (css, markup, js)."""
    rnd = random.Random(53)
    b = lambda key, default: beats[spec.get(key, default)]
    dream, warn, well, inside = b("dream_beat", 1), b("warn_beat", 2), b("well_beat", 3), b("inside_beat", 4)

    # Dream sky: eleven stars on an arc, the sun and the moon; they bow near the end of the dream line.
    stars = []
    for k in range(11):
        a = 3.14159 * (0.12 + 0.76 * k / 10)
        x, y = 540 - 380 * __import__("math").cos(a), 1560 - 300 * __import__("math").sin(a)
        stars.append(f'<div id="ys{k}" class="ystar" style="left:{x:.0f}px;top:{y:.0f}px"></div>')
    twinkles = [f'tl.fromTo("#ys{k}", {{opacity: 0.6}}, {{opacity: 1, duration: {rnd.uniform(0.5, 0.9):.2f}, yoyo: true, '
                f'repeat: {int(total / 0.5)}, ease: "sine.inOut"}}, {rnd.uniform(0, 0.5):.2f});' for k in range(11)]
    bow_at = dream["start"] + max(dream["spoken"] - 1.6, 0.5)
    dunes = ('<path fill="#1b1a26" d="M 0 1230 C 200 1180 380 1210 560 1235 C 760 1262 900 1190 1080 1215 V 1920 H 0 Z"/>'
             '<path fill="#13121c" d="M 0 1330 C 240 1290 420 1340 620 1350 C 820 1360 960 1300 1080 1320 V 1920 H 0 Z"/>')
    # Faceless walkers without spears (the soldier shape minus its spear).
    bros = re.sub(r'<rect [^>]*width="2"[^>]*/>', "", "".join(soldier(x, 74) for x in [430, 492, 540, 610, 668, 720, 790, 846, 900, 968]))
    css = """
    #ydesert, #ydream, #yinside { position: absolute; inset: 0; }
    #ysky { position: absolute; inset: 0; background: linear-gradient(180deg, #070b18 0%, #142037 55%, #22283c 100%); }
    #ymoon { position: absolute; left: 800px; top: 1010px; width: 110px; height: 110px; border-radius: 50%;
      background: radial-gradient(circle at 40% 38%, #fffdf3, #e6dfc8 65%, #cfc7ae);
      box-shadow: 0 0 70px 24px rgba(230,236,255,0.3); }
    #ydunes { position: absolute; inset: 0; width: 100%; height: 100%; }
    #ywell { position: absolute; left: 340px; top: 1380px; width: 400px; height: 260px; }
    #ybros { position: absolute; left: 0; top: 1150px; width: 1080px; height: 110px; overflow: visible; opacity: 0; }
    #dsky { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 40%, #1d2a52 0%, #0b1026 60%, #05070f 100%); }
    .ystar { position: absolute; width: 26px; height: 26px; margin: -13px; border-radius: 50%;
      background: radial-gradient(circle, #ffffff 0%, #dfe8ff 35%, rgba(200,215,255,0) 70%);
      box-shadow: 0 0 24px 8px rgba(200,215,255,0.45); }
    #dsun { position: absolute; left: 170px; top: 1080px; width: 150px; height: 150px; border-radius: 50%;
      background: radial-gradient(circle, #fff2c8 0%, #ffc860 45%, rgba(255,170,60,0) 72%); }
    #dmoon { position: absolute; left: 790px; top: 1100px; width: 110px; height: 110px; border-radius: 50%;
      background: radial-gradient(circle at 40% 38%, #fffdf3, #e6dfc8 65%, #cfc7ae); box-shadow: 0 0 50px 16px rgba(230,236,255,0.3); }
    #dset { position: absolute; inset: 0; }
    #iwall { position: absolute; inset: 0; background: radial-gradient(circle at 50% 70%, rgba(0,0,0,0) 0 170px, #1a140f 190px, #0a0705 70%); }
    #ihole { position: absolute; left: 340px; top: 1150px; width: 400px; height: 400px; border-radius: 50%;
      background: radial-gradient(circle, #f6efe0 0%, #cfd9f0 40%, #6a7aa0 75%); }
    #ibeam { position: absolute; left: 140px; top: 1250px; width: 800px; height: 700px; transform-origin: 50% 0%;
      background: radial-gradient(ellipse 50% 70% at 50% 20%, rgba(240,235,220,0.35), rgba(240,235,220,0.12) 45%, rgba(240,235,220,0) 75%); }
    #istones { position: absolute; inset: 0; background: repeating-linear-gradient(180deg, rgba(255,255,255,0.03) 0 38px, rgba(0,0,0,0.25) 38px 42px); }
"""
    markup = f"""
    <div id="ydesert" class="clip" data-start="0" data-duration="{total:.2f}">
      <div id="ysky"></div><div id="ymoon"></div>
      <svg id="ydunes" viewBox="0 0 1080 1920" preserveAspectRatio="none">{dunes}</svg>
      <svg id="ybros" viewBox="0 0 1080 110"><g transform="translate(0,100)" fill="#07060a">{bros}</g></svg>
      <svg id="ywell" viewBox="0 0 400 260">
        <defs><linearGradient id="wst" x1="0" x2="1"><stop offset="0" stop-color="#2a2620"/><stop offset="0.5" stop-color="#5a5244"/><stop offset="1" stop-color="#211d18"/></linearGradient></defs>
        <rect x="20" y="70" width="360" height="170" rx="10" fill="url(#wst)"/>
        <path d="M 20 110 H 380 M 20 150 H 380 M 20 190 H 380" stroke="rgba(0,0,0,0.35)" stroke-width="4"/>
        <ellipse cx="200" cy="70" rx="180" ry="48" fill="#6a6152"/>
        <ellipse cx="200" cy="72" rx="150" ry="36" fill="#030202"/>
      </svg>
    </div>
    <div id="ydream" class="clip" data-start="0" data-duration="{total:.2f}" style="opacity:0">
      <div id="dsky"></div>
      <div id="dset"><div id="dsun"></div><div id="dmoon"></div>{"".join(stars)}</div>
    </div>
    <div id="yinside" class="clip" data-start="0" data-duration="{total:.2f}" style="opacity:0">
      <div id="istones"></div><div id="iwall"></div><div id="ihole"></div><div id="ibeam"></div>
    </div>"""
    js = ["\n    ".join(twinkles)]
    fade = lambda sel, a, b2, t, d=0.8: f'tl.fromTo("{sel}", {{opacity: {a}}}, {{opacity: {b2}, duration: {d}, ease: "sine.inOut", immediateRender: false}}, {t:.2f});'
    js.append(fade("#ydream", 0, 1, dream["start"]))
    js.append(f'tl.fromTo("#dset", {{y: 0, scale: 1}}, {{y: 160, scale: 0.88, duration: 1.4, ease: "power2.inOut", immediateRender: false}}, {bow_at:.2f});')
    js.append(fade("#ydream", 1, 0, well["start"]))
    js.append(fade("#ybros", 0, 1, well["start"] + 0.3))
    js.append(f'tl.fromTo("#ybros", {{x: 0}}, {{x: -260, duration: {well["dur"]:.2f}, ease: "none", immediateRender: false}}, {well["start"]:.2f});')
    js.append(f'tl.fromTo("#ywell", {{scale: 1}}, {{scale: 1.6, duration: {well["dur"]:.2f}, ease: "power1.in", transformOrigin: "50% 30%", immediateRender: false}}, {well["start"]:.2f});')
    js.append(fade("#yinside", 0, 1, inside["start"], 0.6))
    js.append(f'tl.fromTo("#ibeam", {{opacity: 0.2, scaleY: 0.6}}, {{opacity: 1, scaleY: 1, duration: 3, ease: "sine.out", immediateRender: false}}, {inside["start"] + 0.5:.2f});')
    js.append(f'tl.fromTo("#ihole", {{scale: 0.9}}, {{scale: 1.08, duration: {total - inside["start"]:.2f}, ease: "none", immediateRender: false}}, {inside["start"]:.2f});')
    return css, markup, "\n    ".join(js)


def fade(sel: str, a: float, b: float, t: float, d: float = 0.8) -> str:
    return (f'tl.fromTo("{sel}", {{opacity: {a}}}, {{opacity: {b}, duration: {d}, ease: "sine.inOut", '
            f'immediateRender: false}}, {t:.2f});')


def loop(sel: str, frm: str, to: str, period: float, total: float, start: float = 0) -> str:
    """A seek-safe yoyo loop that runs for the whole Short."""
    return (f'tl.fromTo("{sel}", {{{frm}}}, {{{to}, duration: {period / 2:.2f}, ease: "sine.inOut", yoyo: true, '
            f'repeat: {int(total / (period / 2)) + 1}}}, {start:.2f});')


def donkey_svg(body: str = "#8a6646") -> str:
    """A side-on donkey silhouette in a 400×300 box (head to the right)."""
    return (f'<g fill="{body}"><ellipse cx="200" cy="150" rx="112" ry="56"/>'
            '<rect x="112" y="178" width="18" height="98" rx="6"/><rect x="142" y="182" width="18" height="94" rx="6"/>'
            '<rect x="250" y="182" width="18" height="94" rx="6"/><rect x="280" y="178" width="18" height="98" rx="6"/>'
            '<polygon points="276,128 328,62 356,80 312,166"/>'
            '<ellipse cx="358" cy="86" rx="44" ry="24" transform="rotate(32 358 86)"/>'
            '<polygon points="326,64 330,8 346,60"/><polygon points="342,66 356,12 362,66"/>'
            f'<path d="M 90 135 Q 66 170 76 214" stroke="{body}" stroke-width="9" fill="none"/></g>')


def bones_svg(prefix: str) -> str:
    """The donkey's skeleton, piece by piece, in donkey_svg's box. Each piece has its own id so it
    can lie scattered on the ground and then rise into place."""
    bone = 'stroke="#e9dfc7" stroke-linecap="round" fill="none"'
    pieces = [
        f'<ellipse cx="356" cy="86" rx="34" ry="17" fill="#e9dfc7" transform="rotate(32 356 86)"/>',
        f'<path d="M 298 138 L 342 88" {bone} stroke-width="10"/>',
        f'<path d="M 104 126 Q 200 112 300 132" {bone} stroke-width="10"/>',
        f'<ellipse cx="118" cy="142" rx="22" ry="16" fill="#e9dfc7"/>',
    ]
    pieces += [f'<path d="M {x} 124 Q {x + 14} 168 {x} 196" {bone} stroke-width="6"/>' for x in range(150, 271, 24)]
    pieces += [f'<path d="M {x} 156 L {x} 276" {bone} stroke-width="9"/>' for x in (121, 151, 259, 289)]
    return "".join(f'<g id="{prefix}{k}">{p}</g>' for k, p in enumerate(pieces)), len(pieces)


def ruins_scene(spec: dict, beats: list, total: float) -> tuple[str, str, str]:
    """2:259: a ruined town at dusk, a time-lapse of a hundred years, the unspoiled food and the
    donkey's bones raised and clothed. The man himself is never shown. Returns (css, markup, js)."""
    rnd = random.Random(61)
    b = lambda key, default: beats[spec.get(key, default)]
    lapse, food, raise_ = b("lapse_beat", 2), b("food_beat", 4), b("raise_beat", 5)

    # Broken walls, a fallen arch and roofless houses on the skyline.
    town = []
    x = -20
    while x < 1100:
        w, h = rnd.uniform(70, 150), rnd.uniform(90, 230)
        top = 1430 - h
        # A jagged broken top edge.
        pts = [(x, 1430), (x, top + rnd.uniform(0, 40))]
        for k in range(1, 5):
            pts.append((x + w * k / 5, top + rnd.uniform(0, 70)))
        pts += [(x + w, top + rnd.uniform(20, 90)), (x + w, 1430)]
        town.append('<polygon points="' + " ".join(f"{px:.0f},{py:.0f}" for px, py in pts) + '"/>')
        if rnd.random() < 0.5:  # a dark window gap
            town.append(f'<rect x="{x + w * 0.35:.0f}" y="{top + 60:.0f}" width="{w * 0.22:.0f}" height="34" fill="#160e0b"/>')
        x += w + rnd.uniform(-10, 30)
    arch = ('<path d="M 600 1430 L 600 1250 Q 600 1170 680 1170 Q 760 1170 760 1250 L 760 1300 L 735 1290 '
            'L 735 1250 Q 735 1195 680 1195 Q 625 1195 625 1250 L 625 1430 Z"/>')
    rubble = "".join(f'<ellipse cx="{rnd.uniform(0, 1080):.0f}" cy="{rnd.uniform(1435, 1470):.0f}" '
                     f'rx="{rnd.uniform(10, 34):.0f}" ry="{rnd.uniform(6, 14):.0f}"/>' for _ in range(26))

    # Counter: 0 → 100, each decade fades through.
    counts = "".join(f'<div id="rc{k}" class="rcnt" style="opacity:0" data-layout-allow-occlusion>{k * 10}</div>' for k in range(11))
    bones, nb = bones_svg("rbn")

    css = """
    #rsky { position: absolute; inset: 0; background: linear-gradient(180deg, #120d1c 0%, #3a2338 38%, #a3533a 58%, #e39a52 66%, #2a1912 76%); }
    #rnight { position: absolute; inset: 0; background: linear-gradient(180deg, #03040c 0%, #0a1026 60%, #0d0c14 100%); opacity: 0; }
    #rsun { position: absolute; left: 470px; top: 1290px; width: 150px; height: 150px; border-radius: 50%;
      background: radial-gradient(circle, #fff1c8 0%, #ffb860 45%, rgba(255,150,60,0) 72%); }
    #rtown { position: absolute; inset: 0; width: 100%; height: 100%; }
    #rground { position: absolute; left: 0; right: 0; top: 1430px; bottom: 0;
      background: linear-gradient(180deg, #3b2617 0%, #24170f 45%, #120b07 100%); }
    .rcnt { position: absolute; left: 0; right: 0; top: 1500px; text-align: center; font-family: Inter; font-weight: 900;
      font-size: 190px; color: var(--accent); text-shadow: 0 0 40px rgba(242,176,74,0.55); }
    #rcap { position: absolute; left: 0; right: 0; top: 1720px; text-align: center; font-family: Inter; font-weight: 700;
      font-size: 40px; letter-spacing: 0.3em; color: rgba(245,234,214,0.85); opacity: 0; }
    #rfood { position: absolute; left: 70px; top: 1500px; width: 400px; height: 250px; opacity: 0; }
    #rglow { position: absolute; left: 20px; top: 1430px; width: 500px; height: 380px; border-radius: 50%; opacity: 0;
      background: radial-gradient(ellipse, rgba(255,220,150,0.45), rgba(255,200,120,0) 70%); }
    #rbones, #rdonkey { position: absolute; left: 560px; top: 1330px; width: 440px; height: 330px; overflow: visible; }
    #rdonkey { opacity: 0; filter: drop-shadow(0 0 18px rgba(255,200,130,0.45)); }
"""
    food_svg = ('<svg id="rfood" viewBox="0 0 400 250">'
                '<ellipse cx="300" cy="225" rx="80" ry="14" fill="rgba(0,0,0,0.4)"/>'
                '<path d="M 250 120 Q 240 60 290 50 Q 345 45 345 115 Q 350 200 300 215 Q 245 210 250 120 Z" fill="#7a4f2c"/>'
                '<path d="M 280 52 L 284 30 L 300 30 L 302 50" fill="#5e3b20"/>'
                '<ellipse cx="140" cy="215" rx="140" ry="20" fill="rgba(0,0,0,0.4)"/>'
                '<path d="M 20 140 Q 140 250 260 140 Z" fill="#8a5a30"/>'
                '<path d="M 30 150 Q 140 238 250 150 M 45 170 Q 140 236 235 170 M 70 192 Q 140 232 210 192" stroke="#5e3b20" stroke-width="5" fill="none"/>'
                + "".join(f'<circle cx="{cx}" cy="{cy}" r="15" fill="#6b2f6a"/>' for cx, cy in
                          [(70, 128), (95, 120), (82, 104), (110, 132), (60, 112), (98, 98), (125, 115)])
                + '<ellipse cx="175" cy="122" rx="52" ry="26" fill="#c98a45"/><ellipse cx="175" cy="114" rx="40" ry="14" fill="#dca061"/>'
                '<circle cx="225" cy="132" r="18" fill="#7a3d4a"/><circle cx="140" cy="138" r="14" fill="#5a7a2a"/>'
                '</svg>')
    markup = f"""
    <div id="ruins" class="clip" data-start="0" data-duration="{total:.2f}">
      <div id="rsky"></div><div id="rsun"></div><div id="rnight"></div>
      <svg id="rtown" viewBox="0 0 1080 1920" preserveAspectRatio="none"><g fill="#1f1410">{"".join(town)}{arch}</g><g fill="#2b1c13">{rubble}</g></svg>
      <div id="rground"></div>
      <div id="rcount" data-layout-allow-occlusion>{counts}<div id="rcap" data-layout-allow-occlusion>YEARS</div></div>
      <div id="rglow"></div>
      {food_svg}
      <svg id="rbones" viewBox="0 0 400 300" style="opacity:0">{bones}</svg>
      <svg id="rdonkey" viewBox="0 0 400 300">{donkey_svg()}</svg>
    </div>"""

    js = []
    # The sun sinks slowly through the opening lines.
    js.append(f'tl.fromTo("#rsun", {{y: -120}}, {{y: 40, duration: {lapse["start"]:.2f}, ease: "none"}}, 0);')
    # Time-lapse: day and night flicker past, the counter climbs to 100.
    t0, span = lapse["start"] + 0.3, lapse["dur"] - 0.6
    cycles = 7
    per = span / cycles
    js.append(f'tl.fromTo("#rnight", {{opacity: 0}}, {{opacity: 0.92, duration: {per / 2:.2f}, ease: "sine.inOut", yoyo: true, '
              f'repeat: {cycles * 2 - 1}, immediateRender: false}}, {t0:.2f});')
    js.append(f'tl.fromTo("#rsun", {{y: 300}}, {{y: -420, duration: {per:.2f}, ease: "none", repeat: {cycles - 1}, '
              f'immediateRender: false}}, {t0:.2f});')
    js.append(f'tl.fromTo("#rsun", {{y: -420}}, {{y: 40, duration: 0.6, ease: "sine.out", immediateRender: false}}, {t0 + span:.2f});')
    step = span / 11
    for k in range(11):
        at = t0 + k * step
        last = k == 10
        js.append(f'tl.fromTo("#rc{k}", {{opacity: 0, scale: 0.8}}, {{opacity: 1, scale: 1, duration: 0.12, immediateRender: false}}, {at:.2f});')
        if not last:
            js.append(f'tl.fromTo("#rc{k}", {{opacity: 1}}, {{opacity: 0, duration: 0.12, immediateRender: false}}, {at + step:.2f});')
    js.append(fade("#rcap", 0, 1, t0, 0.4))
    js.append(fade("#rc10", 1, 0, food["start"], 0.6))
    js.append(fade("#rcap", 1, 0, food["start"], 0.6))
    # The food: unchanged, glowing. The bones: scattered on the ground.
    js.append(fade("#rfood", 0, 1, food["start"] + 0.2))
    js.append(f'tl.fromTo("#rglow", {{opacity: 0}}, {{opacity: 1, duration: 0.9, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false}}, {food["start"] + 1.6:.2f});')
    bones_at = food["start"] + food["spoken"] * 0.62
    js.append(fade("#rbones", 0, 1, bones_at))
    rise_at = raise_["start"] + 0.9
    for k in range(nb):
        dx, dy, rot = rnd.uniform(-70, 70), rnd.uniform(60, 150), rnd.uniform(-80, 80)
        js.append(f'tl.fromTo("#rbn{k}", {{x: {dx:.0f}, y: {dy:.0f}, rotation: {rot:.0f}, transformOrigin: "50% 50%"}}, '
                  f'{{x: 0, y: 0, rotation: 0, duration: 1.6, ease: "power2.inOut", immediateRender: false}}, {rise_at + k * 0.08:.2f});')
        js.append(f'tl.set("#rbn{k}", {{x: {dx:.0f}, y: {dy:.0f}, rotation: {rot:.0f}, transformOrigin: "50% 50%"}}, 0);')
    flesh_at = rise_at + 2.6
    js.append(fade("#rdonkey", 0, 1, flesh_at, 1.4))
    js.append(fade("#rbones", 1, 0.0, flesh_at + 0.6, 1.0))
    js.append(f'tl.fromTo("#rdonkey", {{scale: 1}}, {{scale: 1.04, duration: 1.2, ease: "sine.inOut", yoyo: true, repeat: 3, '
              f'transformOrigin: "50% 100%", immediateRender: false}}, {flesh_at + 1.4:.2f});')
    return css, markup, "\n    ".join(js)


def atmos_html(spec: dict, beats: list, total: float) -> str:
    accent = spec["accent"]
    mote = spec.get("mote", accent)
    floor = spec.get("motes", 0)
    rnd = random.Random(7)
    embers, ejs = [], []
    if spec.get("embers", True):
        for k in range(34):
            x = rnd.uniform(40, W - 40)
            size = rnd.uniform(4, 11)
            period = rnd.uniform(3.2, 6.5)
            delay = rnd.uniform(0, period)
            drift = rnd.uniform(-90, 90)
            reps = int((total + delay) / period) + 1
            embers.append(f'<div id="em{k}" class="em" style="left:{x:.0f}px;width:{size:.1f}px;height:{size:.1f}px"></div>')
            ejs.append(f'et.fromTo("#em{k}", {{y: 0, x: 0, opacity: 0}}, {{keyframes: [{{opacity: 0.95, duration: {period * 0.2:.2f}}}, '
                       f'{{opacity: 0, duration: {period * 0.8:.2f}}}], y: -{rnd.uniform(900, 1500):.0f}, x: {drift:.0f}, '
                       f'duration: {period:.2f}, ease: "none", repeat: {reps}}}, {7 - delay:.2f});')

    mood_js = []
    prev = beats[0]["mood"]
    for b in beats[1:]:
        m = b["mood"]
        pw, pc, pe = prev.get("warm", 0), prev.get("cool", 0), max(floor, min(1, prev.get("warm", 0) * 1.4))
        w, c, e = m.get("warm", 0), m.get("cool", 0), max(floor, min(1, m.get("warm", 0) * 1.4))
        mood_js.append(f'tl.fromTo("#warm-g", {{opacity: {pw}}}, {{opacity: {w}, duration: 0.9, ease: "sine.inOut", immediateRender: false}}, {b["start"]:.2f});')
        mood_js.append(f'tl.fromTo("#cool-g", {{opacity: {pc}}}, {{opacity: {c}, duration: 1.2, ease: "sine.inOut", immediateRender: false}}, {b["start"]:.2f});')
        mood_js.append(f'tl.fromTo("#embers-g", {{opacity: {pe:.2f}}}, {{opacity: {e:.2f}, duration: 0.9, immediateRender: false}}, {b["start"]:.2f});')
        if "rain" in m or "rain" in prev:
            mood_js.append(f'tl.fromTo("#rain-g", {{opacity: {prev.get("rain", 0)}}}, {{opacity: {m.get("rain", 0)}, duration: 1.5, ease: "sine.inOut", immediateRender: false}}, {b["start"]:.2f});')
        prev = m
    m0 = beats[0]["mood"]
    breathes = int(total / 1.6)
    scene_css = scene_markup = scene_js = ""
    if spec.get("scene") == "cave":
        scene_css, scene_markup, scene_js = cave_scene(total)
    elif spec.get("scene") == "yusuf":
        scene_css, scene_markup, scene_js = yusuf_scene(spec, beats, total)
    elif spec.get("scene") == "valley":
        scene_css, scene_markup, scene_js = valley_scene(spec, beats, total)
    elif spec.get("scene") == "mosque":
        scene_css, scene_markup, scene_js = mosque_scene(spec, beats, total)
    elif spec.get("scene") == "storm":
        scene_css, scene_markup, scene_js = storm_scene(spec, beats, total)
    elif spec.get("scene") in SCENES:
        scene_css, scene_markup, scene_js = SCENES[spec["scene"]](spec, beats, total)

    return f"""<template>
  <style>
    #atmos {{ position: absolute; inset: 0; overflow: hidden; }}
    #sky {{ position: absolute; inset: 0; background: linear-gradient(180deg, #07060c 0%, #0d0a12 55%, #160d0c 100%); }}
    #warm, #cool, #embers {{ position: absolute; inset: 0; }}
    #warm-g, #cool-g, #embers-g {{ position: absolute; inset: 0; }}
    #warm-b {{ position: absolute; left: -20%; right: -20%; bottom: -18%; height: 85%;
      background: radial-gradient(ellipse at 50% 100%, rgba(255,170,60,0.95) 0%, rgba(230,90,30,0.55) 30%, rgba(120,30,20,0.25) 55%, rgba(0,0,0,0) 72%); }}
    #cool-g {{
      background: radial-gradient(ellipse at 50% 62%, rgba(215,236,255,0.55) 0%, rgba(120,170,220,0.22) 35%, rgba(0,0,0,0) 70%); }}
    .em {{ position: absolute; bottom: -20px; border-radius: 50%; background: {mote};
      box-shadow: 0 0 12px {mote}, 0 0 24px {mote}; }}{scene_css}
    #vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 45%, rgba(0,0,0,0.7) 100%); }}
    #flash-host {{ position: absolute; inset: 0; }}
    #flash {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 45%, rgba(255,240,215,0.85), rgba(255,200,120,0.25) 60%, rgba(0,0,0,0) 85%); }}
    #brand {{ position: absolute; top: 210px; left: 0; right: 0; text-align: center; font-family: Inter; font-weight: 700;
      font-size: 28px; letter-spacing: 0.32em; color: rgba(245,234,214,0.72); }}
    #brand span {{ color: {accent}; }}
  </style>
  <div id="atmos" data-composition-id="atmos" data-width="{W}" data-height="{H}" data-layout-allow-overflow>
    <div id="sky" class="clip" data-start="0" data-duration="{total:.2f}"></div>
{scene_markup}
    <div id="warm" class="clip" data-start="0" data-duration="{total:.2f}"><div id="warm-g" style="opacity:{m0.get('warm', 0)}"><div id="warm-b"></div></div></div>
    <div id="cool" class="clip" data-start="0" data-duration="{total:.2f}"><div id="cool-g" style="opacity:{m0.get('cool', 0)}"></div></div>
    <div id="embers" class="clip" data-start="0" data-duration="{total:.2f}"><div id="embers-g" style="opacity:{max(floor, min(1, m0.get('warm', 0) * 1.4)):.2f}">
      {"".join(embers)}
    </div></div>
    <div id="vig" class="clip" data-start="0" data-duration="{total:.2f}"></div>
    <div id="flash-host" class="clip" data-start="0" data-duration="0.6"><div id="flash"></div></div>
    <div id="brand" class="clip" data-start="0" data-duration="{total:.2f}">HAQ <span>·</span> STORIES</div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#flash", {{opacity: {spec.get("flash", 0)}}}, {{opacity: 0, duration: 0.55, ease: "power2.out"}}, 0);
    {scene_js}
    tl.fromTo("#warm-b", {{scaleY: 1}}, {{scaleY: 1.06, duration: 0.8, ease: "sine.inOut", yoyo: true, repeat: {breathes}}}, 0);
    {chr(10).join("    " + s for s in mood_js).strip()}
    const et = gsap.timeline({{ paused: true }});
    {chr(10).join("    " + s for s in ejs).strip()}
    // Sparks are already mid-flight on frame 0: play their own timeline from 7 s in.
    tl.add(et.tweenFromTo(7, {7 + total:.2f}, {{ ease: "none" }}), 0);
    window.__timelines["atmos"] = tl;
  </script>
</template>
"""


def waves_svg(id_: str, y: float, amp: float, color: str, n: int = 8) -> str:
    """A wide band of water whose top edge is a wave; 2160 px wide so it can slide left seamlessly."""
    seg = 2160 / n
    d = f"M 0 {y:.0f} " + " ".join(
        f"Q {seg * k + seg / 4:.0f} {y - amp:.0f} {seg * k + seg / 2:.0f} {y:.0f} T {seg * (k + 1):.0f} {y:.0f}" for k in range(n))
    return (f'<svg id="{id_}" class="wv" viewBox="0 0 2160 1920" preserveAspectRatio="none">'
            f'<path fill="{color}" d="{d} V 1920 H 0 Z"/></svg>')


def rain_markup(prefix: str, n: int, seed: int, total: float) -> tuple[str, str]:
    rnd = random.Random(seed)
    drops, js = [], []
    for k in range(n):
        x, h, per = rnd.uniform(-100, W + 300), rnd.uniform(60, 120), rnd.uniform(0.5, 0.85)
        drops.append(f'<div id="{prefix}{k}" class="drop" style="left:{x:.0f}px;height:{h:.0f}px;opacity:{rnd.uniform(0.25, 0.6):.2f}"></div>')
        js.append(f'tl.fromTo("#{prefix}{k}", {{y: -200, x: 0, rotation: 14}}, {{y: 2150, x: -480, rotation: 14, duration: {per:.2f}, '
                  f'ease: "none", repeat: {int(total / per) + 2}}}, {-rnd.uniform(0, per):.2f});')
    return "".join(drops), "\n    ".join(js)


def sea_scene(spec: dict, beats: list, total: float) -> tuple[str, str, str]:
    """Yunus (AS): a coast at dusk, a ship in a storm, the great fish, three darknesses, then dawn
    on a shore with a gourd vine (37:146). Yunus (AS) is never shown. Returns (css, markup, js)."""
    b = lambda key, default: beats[spec.get(key, default)]
    leave, storm, dark, call, saved = b("leave_beat", 1), b("storm_beat", 2), b("dark_beat", 3), b("call_beat", 4), b("saved_beat", 5)
    drops, rain_js = rain_markup("rn", 80, 71, total)
    rnd = random.Random(73)
    bubbles = "".join(f'<div id="bb{k}" class="bub" style="left:{rnd.uniform(200, 880):.0f}px;width:{(s := rnd.uniform(8, 22)):.0f}px;height:{s:.0f}px"></div>'
                      for k in range(16))
    css = """
    #sdusk { position: absolute; inset: 0; background: linear-gradient(180deg, #0c1022 0%, #26304e 45%, #6a4a52 58%, #2a2c3c 66%); }
    #sstorm { position: absolute; inset: 0; background: linear-gradient(180deg, #06080e 0%, #121826 55%, #0a0e16 100%); opacity: 0; }
    #sbolt { position: absolute; inset: 0; opacity: 0;
      background: radial-gradient(ellipse at 40% 20%, rgba(220,230,255,0.9), rgba(160,180,230,0.3) 50%, rgba(0,0,0,0) 80%); }
    .wv { position: absolute; left: 0; top: 0; width: 2160px; height: 1920px; }
    #scoast { position: absolute; inset: 0; width: 100%; height: 100%; }
    #sship { position: absolute; left: 380px; top: 1060px; width: 320px; height: 300px; opacity: 0; }
    #sfish { position: absolute; left: 1100px; top: 1330px; width: 900px; height: 360px; opacity: 0.95; }
    .drop { position: absolute; top: 0; width: 2px; background: linear-gradient(180deg, rgba(200,215,240,0), rgba(200,215,240,0.8)); }
    #srain { position: absolute; inset: 0; opacity: 0; }
    #sd1, #sd2, #sd3 { position: absolute; inset: 0; background: #020205; opacity: 0; }
    #sd3 { background: radial-gradient(ellipse at 50% 60%, #07060a 0%, #000 70%); }
    #sribs { position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; }
    .bub { position: absolute; top: 1800px; border-radius: 50%; border: 2px solid rgba(190,215,255,0.45); opacity: 0; }
    #sdawn { position: absolute; inset: 0; opacity: 0; background: linear-gradient(180deg, #2a3a5e 0%, #c9876a 48%, #f3c08a 60%, #6a8aa0 64%); }
    #ssun { position: absolute; left: 440px; top: 1260px; width: 200px; height: 200px; border-radius: 50%; opacity: 0;
      background: radial-gradient(circle, #fff6dc 0%, #ffd38a 40%, rgba(255,180,90,0) 72%); }
    #sshore { position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; }
"""
    ribs = "".join(f'<path d="M {x} 1100 Q {540 + (x - 540) * 1.25:.0f} 1500 {x} 1900" stroke="rgba(120,90,110,0.35)" stroke-width="10" fill="none"/>'
                   for x in (120, 300, 780, 960))
    markup = f"""
    <div id="sea" class="clip" data-start="0" data-duration="{total:.2f}">
      <div id="sdusk"></div><div id="sstorm"></div><div id="sbolt"></div>
      <svg id="scoast" viewBox="0 0 1080 1920" preserveAspectRatio="none"><g fill="#141826">
        <path d="M 0 1300 L 0 1180 L 60 1180 L 60 1140 L 110 1140 L 110 1190 L 170 1190 L 170 1160 L 230 1160 L 230 1210 L 300 1230 L 330 1300 Z"/></g></svg>
      <svg id="sship" viewBox="0 0 320 300">
        <path d="M 20 210 L 300 210 L 260 270 L 60 270 Z" fill="#1a1410"/>
        <rect x="155" y="40" width="8" height="175" fill="#1a1410"/>
        <path d="M 165 50 Q 250 120 165 195 Z" fill="#cdbfa0"/><path d="M 153 70 Q 90 130 153 190 Z" fill="#b3a585"/>
      </svg>
      {waves_svg("sw1", 1300, 26, "#1c2a44")}
      {waves_svg("sw2", 1420, 34, "#13203a")}
      <svg id="sfish" viewBox="0 0 900 360"><g fill="#05070d">
        <ellipse cx="420" cy="180" rx="380" ry="130"/><path d="M 60 180 L -60 60 L -20 180 L -60 300 Z"/>
        <path d="M 360 60 Q 420 -20 480 60 Z"/></g><circle cx="720" cy="150" r="10" fill="#1a2440"/></svg>
      {waves_svg("sw3", 1560, 40, "#0c1628")}
      <div id="srain">{drops}</div>
      <div id="sd1" style="opacity:0"></div><div id="sd2" style="opacity:0"></div><div id="sd3" style="opacity:0"></div>
      <svg id="sribs" viewBox="0 0 1080 1920" preserveAspectRatio="none">{ribs}</svg>
      {bubbles}
      <div id="sdawn"></div><div id="ssun"></div>
      <svg id="sshore" viewBox="0 0 1080 1920" preserveAspectRatio="none">
        <path fill="#2f4a5e" d="M 0 1380 Q 540 1350 1080 1380 V 1920 H 0 Z"/>
        <path fill="#c9a26a" d="M 0 1560 Q 300 1470 620 1520 Q 880 1560 1080 1500 V 1920 H 0 Z"/>
        <g fill="#3f7a3a"><path d="M 760 1525 Q 840 1420 960 1440 Q 900 1500 760 1525 Z"/><ellipse cx="900" cy="1470" rx="70" ry="40"/>
        <ellipse cx="820" cy="1495" rx="55" ry="30"/><ellipse cx="980" cy="1485" rx="50" ry="28" fill="#4f8a44"/></g>
        <ellipse cx="880" cy="1520" rx="34" ry="22" fill="#b9a24a"/>
      </svg>
    </div>"""
    js = [rain_js]
    for k, (sp, dist) in enumerate([(9, 1080), (7, 1080), (5.5, 1080)]):
        js.append(f'tl.fromTo("#sw{k + 1}", {{x: 0}}, {{x: -{dist}, duration: {sp:.2f}, ease: "none", repeat: {int(total / sp) + 1}}}, 0);')
    # The coast drifts away as he leaves.
    js.append(f'tl.fromTo("#scoast", {{x: 0}}, {{x: -360, duration: {storm["start"]:.2f}, ease: "none"}}, 0);')
    # Storm: the ship rocks, rain, lightning; then the fish passes under.
    s0 = storm["start"]
    js.append(fade("#sship", 0, 1, leave["start"] + 1.0, 1.2))
    js.append(f'tl.fromTo("#sship", {{rotation: -4}}, {{rotation: 4, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: {max(int(s0 / 1.4) - 1, 0)}, transformOrigin: "50% 90%"}}, 0);')
    js.append(f'tl.fromTo("#sship", {{rotation: -12}}, {{rotation: 12, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: {int(storm["dur"] / 0.6)}, transformOrigin: "50% 90%", immediateRender: false}}, {s0:.2f});')
    js.append(fade("#sstorm", 0, 1, s0, 1.0))
    js.append(fade("#srain", 0, 1, s0 + 0.4, 1.0))
    for t in (s0 + 1.2, s0 + 3.0):
        js.append(f'tl.fromTo("#sbolt", {{opacity: 0}}, {{keyframes: [{{opacity: 0.85, duration: 0.05}}, {{opacity: 0.1, duration: 0.08}}, '
                  f'{{opacity: 0.6, duration: 0.05}}, {{opacity: 0, duration: 0.4}}], immediateRender: false}}, {t:.2f});')
    fish_at = s0 + storm["spoken"] * 0.62
    js.append(f'tl.fromTo("#sfish", {{x: 0, y: 60}}, {{x: -1500, y: -60, duration: 3.2, ease: "power1.inOut", immediateRender: false}}, {fish_at:.2f});')
    js.append(fade("#sship", 1, 0, fish_at + 1.6, 0.8))
    # Three darknesses, one per phrase.
    d0, third = dark["start"] + 0.15, dark["spoken"] / 3
    js.append(fade("#srain", 1, 0, d0, 0.6))
    for k in range(3):
        js.append(f'tl.set("#sd{k + 1}", {{opacity: 0}}, 0);')
        js.append(fade(f"#sd{k + 1}", 0, [0.45, 0.75, 1][k], d0 + k * third, 0.9))
    js.append(fade("#sribs", 0, 1, d0 + 2 * third + 0.4, 1.2))
    # The call: bubbles rise in the dark.
    for k in range(16):
        per = rnd.uniform(3, 5)
        js.append(f'tl.fromTo("#bb{k}", {{y: 0, opacity: 0}}, {{keyframes: [{{opacity: 0.8, duration: {per * 0.2:.2f}}}, {{opacity: 0, duration: {per * 0.8:.2f}}}], '
                  f'y: -700, duration: {per:.2f}, ease: "none", repeat: {int(call["dur"] / per) + 1}, immediateRender: false}}, {call["start"] + rnd.uniform(0, 2.5):.2f});')
    # Saved: dawn on the shore.
    sv = saved["start"]
    for sel in ("#sd1", "#sd2", "#sd3", "#sribs"):
        js.append(f'tl.to("{sel}", {{opacity: 0, duration: 1.4, ease: "sine.inOut"}}, {sv:.2f});')
    js.append(fade("#sdawn", 0, 1, sv, 1.6))
    js.append(fade("#sshore", 0, 1, sv + 0.4, 1.6))
    js.append(f'tl.fromTo("#ssun", {{opacity: 0, y: 120}}, {{opacity: 1, y: -60, duration: 4, ease: "sine.out", immediateRender: false}}, {sv + 0.3:.2f});')
    return css, markup, "\n    ".join(js)


def river_scene(spec: dict, beats: list, total: float) -> tuple[str, str, str]:
    """Musa's (AS) mother: the Nile at night, a basket set on the water, Pharaoh's palace, an empty
    cradle, and the basket home again. No person is shown: not the mother, the sister, the wife of
    Pharaoh or the baby. Returns (css, markup, js)."""
    b = lambda key, default: beats[spec.get(key, default)]
    pharaoh, cast, carry, empty, back = b("pharaoh_beat", 1), b("cast_beat", 2), b("carry_beat", 3), b("empty_beat", 4), b("back_beat", 5)
    rnd = random.Random(83)
    reeds = "".join(f'<path d="M {x:.0f} 1440 Q {x + rnd.uniform(-20, 20):.0f} {1440 - h / 2:.0f} {x + rnd.uniform(-30, 30):.0f} {1440 - h:.0f}" '
                    f'stroke="#16241a" stroke-width="{rnd.uniform(4, 8):.0f}" fill="none"/>'
                    for x, h in [(rnd.uniform(0, 1080), rnd.uniform(80, 200)) for _ in range(40)])
    torches = "".join(f'<div id="tch{k}" class="tch" style="left:{x}px;top:{y}px"></div>' for k, (x, y) in enumerate([(640, 1105), (780, 1085), (930, 1105)]))
    soldiers = re.sub(r'fill="[^"]*"', "", "".join(soldier(x, 56) for x in range(80, 560, 52)))
    css = """
    #nsky { position: absolute; inset: 0; background: linear-gradient(180deg, #050816 0%, #101a36 55%, #1a2440 100%); }
    #nmoon { position: absolute; left: 160px; top: 1010px; width: 110px; height: 110px; border-radius: 50%;
      background: radial-gradient(circle at 40% 38%, #fffdf3, #e6dfc8 65%, #cfc7ae); box-shadow: 0 0 70px 24px rgba(230,236,255,0.3); }
    #npal { position: absolute; inset: 0; width: 100%; height: 100%; }
    .tch { position: absolute; width: 22px; height: 22px; margin: -11px; border-radius: 50%;
      background: radial-gradient(circle, #fff1c9 0%, #ffae4a 50%, rgba(255,140,40,0) 75%); box-shadow: 0 0 40px 16px rgba(255,150,60,0.35); }
    #nsold { position: absolute; left: 0; top: 1150px; width: 1080px; height: 120px; overflow: visible; opacity: 0; }
    #nriver { position: absolute; left: 0; right: 0; top: 1300px; bottom: 0; background: linear-gradient(180deg, #0f1c34 0%, #0a1426 100%); }
    .wv { position: absolute; left: 0; top: 0; width: 2160px; height: 1920px; }
    #nshine { position: absolute; left: 60px; top: 1320px; width: 320px; height: 600px; opacity: 0.6;
      background: radial-gradient(ellipse 40% 60% at 50% 0%, rgba(230,236,255,0.35), rgba(230,236,255,0) 70%); }
    #nreeds { position: absolute; inset: 0; width: 100%; height: 100%; }
    #nbasket { position: absolute; left: 140px; top: 1500px; width: 240px; height: 130px; opacity: 0; }
    #ndawn { position: absolute; inset: 0; opacity: 0; background: linear-gradient(180deg, #2a2a4e 0%, #b9785a 52%, #e8b07a 62%, #2a3a50 70%); }
    #nhome { position: absolute; inset: 0; opacity: 0; background: linear-gradient(180deg, #120d0a 0%, #241912 60%, #1a120d 100%); }
    #nwin { position: absolute; left: 170px; top: 1060px; width: 200px; height: 260px; border-radius: 100px 100px 0 0;
      background: linear-gradient(180deg, #0c1530, #1a2650); box-shadow: inset 0 0 30px rgba(0,0,0,0.6); }
    #nlamp { position: absolute; left: 820px; top: 1180px; width: 30px; height: 30px; margin: -15px; border-radius: 50%;
      background: radial-gradient(circle, #fff1c9 0%, #ffbe5c 50%, rgba(255,160,60,0) 75%); box-shadow: 0 0 60px 26px rgba(255,170,70,0.3); }
    #nwarm { position: absolute; inset: 0; opacity: 0; background: radial-gradient(ellipse at 50% 80%, rgba(255,190,110,0.45), rgba(255,160,80,0) 65%); }
    #ncradle { position: absolute; left: 320px; top: 1440px; width: 440px; height: 260px; }
    #nfill { opacity: 0; }
"""
    markup = f"""
    <div id="river" class="clip" data-start="0" data-duration="{total:.2f}">
      <div id="nsky"></div><div id="ndawn"></div><div id="nmoon"></div>
      <svg id="npal" viewBox="0 0 1080 1920" preserveAspectRatio="none"><g fill="#0a0c16">
        <path d="M 560 1300 L 560 1120 L 600 1120 L 600 1060 L 1080 1060 L 1080 1300 Z"/>
        <path d="M 660 1060 L 690 960 L 720 1060 Z M 860 1060 L 890 940 L 920 1060 Z"/>
        <rect x="610" y="1140" width="18" height="160"/><rect x="700" y="1140" width="18" height="160"/>
        <rect x="790" y="1140" width="18" height="160"/><rect x="880" y="1140" width="18" height="160"/><rect x="970" y="1140" width="18" height="160"/>
        <path d="M 0 1300 L 0 1240 Q 200 1220 520 1260 L 560 1300 Z"/></g></svg>
      {torches}
      <svg id="nsold" viewBox="0 0 1080 120"><g transform="translate(0,110)" fill="#04050a">{soldiers}</g></svg>
      <div id="nriver"></div>
      {waves_svg("nw1", 1330, 10, "#13223e", 10)}
      <div id="nshine"></div>
      {waves_svg("nw2", 1450, 14, "#0e1a32", 10)}
      <svg id="nbasket" viewBox="0 0 240 130">
        <ellipse cx="120" cy="112" rx="110" ry="14" fill="rgba(200,220,255,0.15)"/>
        <path d="M 10 50 Q 120 150 230 50 Z" fill="#8a6234"/>
        <path d="M 22 62 Q 120 140 218 62 M 40 82 Q 120 135 200 82" stroke="#5e4020" stroke-width="5" fill="none"/>
        <path d="M 30 52 Q 120 10 210 52 Z" fill="#cdbb95"/>
      </svg>
      {waves_svg("nw3", 1610, 18, "#0a1428", 10)}
      <svg id="nreeds" viewBox="0 0 1080 1920" preserveAspectRatio="none" style="opacity:0.0">{reeds}</svg>
      <div id="nhome"><div id="nwin"></div><div id="nlamp"></div><div id="nwarm"></div>
        <svg id="ncradle" viewBox="0 0 440 260">
          <path d="M 40 236 Q 220 290 400 236" stroke="#4a3322" stroke-width="14" fill="none" stroke-linecap="round"/>
          <rect x="60" y="80" width="18" height="160" rx="6" fill="#5a3e28"/><rect x="362" y="80" width="18" height="160" rx="6" fill="#5a3e28"/>
          <circle cx="69" cy="76" r="14" fill="#6a4a30"/><circle cx="371" cy="76" r="14" fill="#6a4a30"/>
          <rect x="78" y="130" width="284" height="96" rx="10" fill="#6a4a30"/>
          <path d="M 90 150 H 350 M 90 178 H 350 M 90 206 H 350" stroke="#4a3322" stroke-width="5"/>
          <g id="nfill"><path d="M 92 132 Q 140 86 220 96 Q 300 86 348 132 Z" fill="#d8c8a4"/>
            <path d="M 130 120 Q 220 98 310 120" stroke="#b7a37c" stroke-width="5" fill="none"/></g>
        </svg></div>
    </div>"""
    js = []
    for k, sp in enumerate((10, 8, 6.5)):
        js.append(f'tl.fromTo("#nw{k + 1}", {{x: 0}}, {{x: -1080, duration: {sp}, ease: "none", repeat: {int(total / sp) + 1}}}, 0);')
    for k in range(3):
        js.append(loop(f"#tch{k}", "opacity: 0.7", "opacity: 1", 0.4 + 0.07 * k, total))
    js.append(fade("#nsold", 0, 1, pharaoh["start"] + 0.3))
    js.append(f'tl.fromTo("#nsold", {{x: -200}}, {{x: 260, duration: {pharaoh["dur"]:.2f}, ease: "none", immediateRender: false}}, {pharaoh["start"]:.2f});')
    js.append(fade("#nsold", 1, 0, cast["start"], 0.6))
    # The basket is set on the water and bobs.
    js.append(fade("#nbasket", 0, 1, cast["start"] + cast["spoken"] * 0.45, 1.0))
    js.append(loop("#nbasket", "y: -6, rotation: -3", "y: 6, rotation: 3", 2.2, total))
    # The river carries it to the palace; dawn rises.
    c0 = carry["start"]
    js.append(f'tl.fromTo("#nbasket", {{x: 0}}, {{x: 520, duration: {carry["dur"]:.2f}, ease: "sine.inOut", immediateRender: false}}, {c0:.2f});')
    js.append(fade("#ndawn", 0, 1, c0 + 0.5, 3))
    js.append(fade("#nmoon", 1, 0, c0 + 0.5, 2))
    # The empty cradle at home; then the basket is home again.
    js.append(fade("#nhome", 0, 1, empty["start"], 0.8))
    js.append(loop("#nlamp", "opacity: 0.75", "opacity: 1", 0.5, total))
    js.append(fade("#nfill", 0, 1, back["start"] + back["spoken"] * 0.3, 1.2))
    js.append(fade("#nwarm", 0, 1, back["start"] + back["spoken"] * 0.3, 2.0))
    js.append(f'tl.fromTo("#ncradle", {{rotation: -2}}, {{rotation: 2, duration: 1.3, ease: "sine.inOut", yoyo: true, repeat: {int(total / 1.3)}, transformOrigin: "50% 100%"}}, 0);')
    return css, markup, "\n    ".join(js)


BIRD = ('<g><path d="M -34 0 Q -14 -26 0 -4 Q 14 -26 34 0 Q 14 -8 0 6 Q -14 -8 -34 0 Z" fill="#f4efe4"/>'
        '<ellipse cx="0" cy="2" rx="9" ry="6" fill="#f4efe4"/></g>')


def birds_scene(spec: dict, beats: list, total: float) -> tuple[str, str, str]:
    """2:260: four birds at dawn; their pieces (shown only as feathers) on four hills; the call;
    the birds fly back. Ibrahim (AS) is never shown. Returns (css, markup, js)."""
    b = lambda key, default: beats[spec.get(key, default)]
    cut, call, back = b("cut_beat", 3), b("call_beat", 4), b("back_beat", 5)
    rnd = random.Random(91)
    hills = [(150, 1430), (400, 1370), (680, 1400), (930, 1440)]
    fly = [(220, 1180), (420, 1120), (640, 1150), (860, 1100)]
    birds = "".join(f'<g transform="translate({x},{y}) scale(1.7)"><g id="bd{k}" class="bdw">{BIRD}</g></g>' for k, (x, y) in enumerate(fly))
    feathers = []
    for h, (hx, hy) in enumerate(hills):
        for j in range(5):
            feathers.append((f"ft{h}_{j}", hx + rnd.uniform(-50, 50), hy - 20 + rnd.uniform(-10, 10), rnd.uniform(-60, 60)))
    feather_svg = "".join(f'<g transform="translate({x:.0f},{y:.0f})"><g id="{fid}"><path d="M 0 -20 Q 10 0 0 20 Q -10 0 0 -20 Z" fill="#f4efe4"/>'
                          f'<path d="M 0 -20 L 0 24" stroke="#cfc6b4" stroke-width="2"/></g></g>' for fid, x, y, r in feathers)
    css = """
    #bsky { position: absolute; inset: 0; background: linear-gradient(180deg, #121a34 0%, #3a3e66 40%, #c27f68 58%, #f2b880 66%, #4a3a3a 74%); }
    #bsun { position: absolute; left: 470px; top: 1250px; width: 160px; height: 160px; border-radius: 50%;
      background: radial-gradient(circle, #fff3d6 0%, #ffd08a 40%, rgba(255,170,80,0) 72%); }
    #bhills { position: absolute; inset: 0; width: 100%; height: 100%; }
    #bbirds, #bfeath { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
    .ring { position: absolute; left: 540px; top: 1600px; width: 300px; height: 300px; margin: -150px; border-radius: 50%;
      border: 5px solid rgba(255,230,180,0.8); opacity: 0; }
"""
    hill_paths = "".join(f'<path fill="{c}" d="M {hx - 260} 1920 L {hx - 260} {hy + 140} Q {hx} {hy - 90} {hx + 260} {hy + 140} L {hx + 260} 1920 Z"/>'
                         for (hx, hy), c in zip(hills, ["#2a2026", "#241b22", "#2c2128", "#20181e"]))
    rings = "".join(f'<div id="cr{k}" class="ring"></div>' for k in range(3))
    markup = f"""
    <div id="hills4" class="clip" data-start="0" data-duration="{total:.2f}">
      <div id="bsky"></div><div id="bsun"></div>
      <svg id="bhills" viewBox="0 0 1080 1920" preserveAspectRatio="none">{hill_paths}
        <path fill="#140f12" d="M 0 1640 Q 540 1580 1080 1640 V 1920 H 0 Z"/></svg>
      <svg id="bfeath" viewBox="0 0 1080 1920">{feather_svg}</svg>
      <svg id="bbirds" viewBox="0 0 1080 1920">{birds}</svg>
      {rings}
    </div>"""
    js = []
    for k in range(4):
        per = rnd.uniform(0.32, 0.42)
        js.append(loop(f"#bd{k}", "scaleY: 1", "scaleY: -0.5", per * 2, total, rnd.uniform(0, 0.2)))
        js.append(loop(f"#bd{k}", "x: -20, y: 0", "x: 20, y: -18", rnd.uniform(3, 4.4), total))
    js.append(f'tl.fromTo("#bsun", {{y: 60}}, {{y: -140, duration: {total:.2f}, ease: "none"}}, 0);')
    # Cut: the birds vanish into feathers that drift down onto the four hills.
    c0 = cut["start"] + cut["spoken"] * 0.35
    for k in range(4):
        js.append(fade(f"#bd{k}", 1, 0, c0 + 0.2 * k, 0.5))
    for fid, x, y, r in feathers:
        h = int(fid[2])
        fx, fy = fly[h]
        js.append(f'tl.set("#{fid}", {{opacity: 0}}, 0);')
        js.append(f'tl.fromTo("#{fid}", {{x: {fx - x:.0f}, y: {fy - y:.0f}, rotation: 0, opacity: 0}}, {{x: 0, y: 0, rotation: {r:.0f}, opacity: 0.95, '
                  f'duration: {rnd.uniform(2.2, 3.4):.2f}, ease: "sine.out", immediateRender: false}}, {c0 + 0.2 * h + rnd.uniform(0, 0.4):.2f});')
    # The call: rings spread across the valley.
    for k in range(3):
        js.append(f'tl.fromTo("#cr{k}", {{scale: 0.3, opacity: 0.85}}, {{scale: 4, opacity: 0, duration: 1.8, ease: "power1.out", immediateRender: false}}, '
                  f'{call["start"] + 0.3 + 0.45 * k:.2f});')
    # Back: the feathers lift and gather, and the four birds fly in fast.
    b0 = back["start"] + 0.2
    for fid, x, y, r in feathers:
        h = int(fid[2])
        fx, fy = fly[h]
        js.append(f'tl.to("#{fid}", {{x: {fx - x:.0f}, y: {fy - y:.0f}, rotation: 0, opacity: 0, duration: 0.9, ease: "power2.in"}}, {b0 + 0.1 * h:.2f});')
    for k in range(4):
        js.append(f'tl.fromTo("#bd{k}", {{opacity: 0}}, {{opacity: 1, duration: 0.3, immediateRender: false}}, {b0 + 0.75 + 0.1 * k:.2f});')
    js.append(f'tl.fromTo("#bbirds", {{scale: 0.8, y: 120}}, {{scale: 1.15, y: -40, duration: 2.6, ease: "power2.out", transformOrigin: "50% 60%", immediateRender: false}}, {b0 + 0.8:.2f});')
    return css, markup, "\n    ".join(js)


def ayyub_scene(spec: dict, beats: list, total: float) -> tuple[str, str, str]:
    """Ayyub (AS): an empty home and a dry field through long years, a spring bursting from the
    ground, then green fields and a lit home. Ayyub (AS) is never shown. Returns (css, markup, js)."""
    b = lambda key, default: beats[spec.get(key, default)]
    years, dua, answer, mercy = b("years_beat", 2), b("dua_beat", 3), b("answer_beat", 4), b("mercy_beat", 5)
    rnd = random.Random(97)
    cracks = "".join(f'<path d="M {x:.0f} {y:.0f} l {rnd.uniform(-40, 40):.0f} {rnd.uniform(10, 30):.0f} l {rnd.uniform(-30, 30):.0f} {rnd.uniform(10, 30):.0f}" '
                     f'stroke="#1a120c" stroke-width="3" fill="none"/>' for x, y in [(rnd.uniform(0, 1080), rnd.uniform(1480, 1880)) for _ in range(40)])
    leaves = "".join(f'<div id="lf{k}" class="leaf" style="left:{rnd.uniform(560, 900):.0f}px"></div>' for k in range(10))
    drops = "".join(f'<div id="sp{k}" class="spd"></div>' for k in range(26))
    stars = "".join(f'<div id="as{k}" class="ast" style="left:{rnd.uniform(0, 1080):.0f}px;top:{rnd.uniform(950, 1300):.0f}px"></div>' for k in range(40))
    css = """
    #asky { position: absolute; inset: 0; background: linear-gradient(180deg, #1a1820 0%, #4a4048 50%, #8a7058 64%, #3a2e26 74%); }
    #anight { position: absolute; inset: 0; opacity: 0; background: linear-gradient(180deg, #03040c 0%, #0b1228 60%, #0d0c14 100%); }
    .ast { position: absolute; width: 4px; height: 4px; border-radius: 50%; background: #eef4ff; box-shadow: 0 0 6px #dde8ff; }
    #astars { position: absolute; inset: 0; opacity: 0; }
    #agreen { position: absolute; inset: 0; opacity: 0; background: linear-gradient(180deg, #2a3e66 0%, #8ab0c8 50%, #f3d39a 62%, #3e6a34 70%); }
    #aland { position: absolute; inset: 0; width: 100%; height: 100%; }
    #alush { position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; }
    #ahouse { position: absolute; left: 120px; top: 1240px; width: 360px; height: 280px; }
    #awin { position: absolute; left: 270px; top: 1380px; width: 60px; height: 70px; background: #120c08; }
    #awinlit { position: absolute; left: 270px; top: 1380px; width: 60px; height: 70px; opacity: 0;
      background: #ffc66a; box-shadow: 0 0 60px 24px rgba(255,190,100,0.45); }
    #atree { position: absolute; left: 600px; top: 1120px; width: 340px; height: 420px; }
    #ablossom { opacity: 0; }
    .leaf { position: absolute; top: 1200px; width: 16px; height: 10px; border-radius: 50%; background: #7a5a32; opacity: 0; }
    #aspring { position: absolute; left: 540px; top: 1700px; }
    .spd { position: absolute; left: 0; top: 0; width: 12px; height: 12px; margin: -6px; border-radius: 50%;
      background: radial-gradient(circle, #f2fbff, #8fd0f0 60%, rgba(140,200,240,0) 75%); opacity: 0; }
    #apool { position: absolute; left: 380px; top: 1680px; width: 320px; height: 60px; border-radius: 50%; opacity: 0;
      background: radial-gradient(ellipse, #bfe6f6, #5aa8d0 60%, rgba(90,168,208,0) 72%); }
"""
    markup = f"""
    <div id="ayyub" class="clip" data-start="0" data-duration="{total:.2f}">
      <div id="asky"></div><div id="agreen"></div><div id="anight"></div><div id="astars">{stars}</div>
      <svg id="aland" viewBox="0 0 1080 1920" preserveAspectRatio="none">
        <path fill="#5a4330" d="M 0 1470 Q 540 1420 1080 1470 V 1920 H 0 Z"/>{cracks}</svg>
      <svg id="alush" viewBox="0 0 1080 1920" preserveAspectRatio="none">
        <path fill="#3e6a2c" d="M 0 1470 Q 540 1420 1080 1470 V 1920 H 0 Z"/>
        <path fill="#4f8236" d="M 0 1560 Q 540 1500 1080 1560 V 1920 H 0 Z"/>
        {"".join(f'<path d="M {x:.0f} 1600 l -8 -40 M {x + 8:.0f} 1600 l 6 -46" stroke="#6aa244" stroke-width="5"/>' for x in range(20, 1080, 46))}</svg>
      <svg id="ahouse" viewBox="0 0 360 280"><path d="M 20 120 L 180 20 L 340 120 Z" fill="#2a1f18"/>
        <rect x="40" y="118" width="280" height="160" fill="#3a2a1e"/><rect x="70" y="170" width="70" height="108" fill="#120c08"/></svg>
      <div id="awin"></div><div id="awinlit"></div>
      <svg id="atree" viewBox="0 0 340 420">
        <path d="M 170 420 L 160 260 L 100 180 M 162 250 L 240 160 M 165 300 L 90 260 M 200 200 L 260 120 M 120 200 L 80 120"
          stroke="#2a1d14" stroke-width="16" stroke-linecap="round" fill="none"/>
        <g id="ablossom" fill="#5f9a3e"><circle cx="100" cy="150" r="60"/><circle cx="250" cy="130" r="70"/><circle cx="175" cy="110" r="80"/>
          <circle cx="90" cy="240" r="46"/><circle cx="260" cy="200" r="50"/>
          <g fill="#f3e2b0"><circle cx="140" cy="90" r="8"/><circle cx="230" cy="110" r="8"/><circle cx="110" cy="170" r="7"/><circle cx="270" cy="170" r="7"/></g></g>
      </svg>
      {leaves}
      <div id="apool"></div><div id="aspring">{drops}</div>
    </div>"""
    js = []
    # Years pass: day and night flicker over the same dry field, leaves fall.
    y0, ysp = years["start"] + 0.2, years["dur"] - 0.4
    per = ysp / 5
    js.append(f'tl.fromTo("#anight", {{opacity: 0}}, {{opacity: 0.85, duration: {per / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 9, immediateRender: false}}, {y0:.2f});')
    for k in range(10):
        per_l = rnd.uniform(2.5, 4)
        js.append(f'tl.fromTo("#lf{k}", {{y: 0, x: 0, rotation: 0, opacity: 0}}, {{keyframes: [{{opacity: 0.9, duration: 0.3}}, {{opacity: 0.9, duration: {per_l - 0.6:.2f}}}, {{opacity: 0, duration: 0.3}}], '
                  f'y: 420, x: {rnd.uniform(-120, 60):.0f}, rotation: {rnd.uniform(180, 540):.0f}, duration: {per_l:.2f}, ease: "none", immediateRender: false}}, {y0 + rnd.uniform(0, ysp - per_l):.2f});')
    # The supplication: night and stars.
    js.append(fade("#anight", 0, 1, dua["start"], 1.0))
    js.append(fade("#astars", 0, 1, dua["start"] + 0.3, 1.2))
    for k in range(40):
        js.append(loop(f"#as{k}", "opacity: 0.3", "opacity: 1", rnd.uniform(1.2, 2.6), total, rnd.uniform(0, 1)))
    js.append(f'tl.fromTo("#ayyub", {{scale: 1}}, {{scale: 1.08, duration: {answer["start"] - dua["start"] + 1:.2f}, ease: "none", transformOrigin: "50% 75%", immediateRender: false}}, {dua["start"]:.2f});')
    js.append(f'tl.to("#ayyub", {{scale: 1, duration: 1.2, ease: "sine.inOut"}}, {answer["start"] + 1:.2f});')
    # Answered: a spring bursts from the ground.
    a0 = answer["start"] + answer["spoken"] * 0.55
    js.append(fade("#apool", 0, 1, a0, 0.8))
    for k in range(26):
        ang = rnd.uniform(-0.5, 0.5)
        hgt = rnd.uniform(160, 340)
        per_s = rnd.uniform(0.9, 1.4)
        js.append(f'tl.fromTo("#sp{k}", {{x: 0, y: 0, opacity: 0}}, {{keyframes: [{{x: {ang * hgt * 0.6:.0f}, y: {-hgt:.0f}, opacity: 1, duration: {per_s / 2:.2f}, ease: "power2.out"}}, '
                  f'{{x: {ang * hgt * 1.2:.0f}, y: -20, opacity: 0, duration: {per_s / 2:.2f}, ease: "power2.in"}}], repeat: {int((total - a0) / per_s) + 1}, immediateRender: false}}, {a0 + rnd.uniform(0, per_s):.2f});')
    # Mercy: dawn, green fields, the tree in leaf, the home lit.
    m0 = mercy["start"]
    js.append(fade("#anight", 1, 0, m0, 1.4))
    js.append(fade("#astars", 1, 0, m0, 1.0))
    js.append(fade("#agreen", 0, 1, m0 + 0.2, 1.8))
    js.append(fade("#alush", 0, 1, m0 + 0.6, 2.0))
    js.append(f'tl.fromTo("#ablossom", {{opacity: 0, scale: 0.6, transformOrigin: "50% 60%"}}, {{opacity: 1, scale: 1, duration: 2.2, ease: "back.out(1.4)", immediateRender: false}}, {m0 + 1.0:.2f});')
    js.append(fade("#awinlit", 0, 1, m0 + 1.8, 1.2))
    return css, markup, "\n    ".join(js)


def drown_scene(spec: dict, beats: list, total: float) -> tuple[str, str, str]:
    """Yunus 10:90–92: Pharaoh's army (faceless silhouettes with torches) in the dry path between
    two walls of water; the walls crash shut; foam; then a calm sea at dawn. Musa (AS) is never shown."""
    b = lambda key, default: beats[spec.get(key, default)]
    crash, calm = b("crash_beat", 1), b("calm_beat", 3)
    rnd = random.Random(131)
    army = re.sub(r'fill="[^"]*"', "", "".join(soldier(rnd.uniform(380, 700), rnd.uniform(70, 95)) for _ in range(26)))
    torch_pts = [(rnd.uniform(390, 690), rnd.uniform(1210, 1290)) for _ in range(14)]
    torches = "".join(f'<div id="dt{k}" class="dtorch" style="left:{x:.0f}px;top:{y:.0f}px"></div>' for k, (x, y) in enumerate(torch_pts))
    css = """
    #dsky { position: absolute; inset: 0; background: linear-gradient(180deg, #0a0c18 0%, #1e2440 45%, #4a3a4a 60%, #2a2a3a 70%); }
    #dpath { position: absolute; left: 330px; width: 420px; top: 1180px; bottom: 0; background: linear-gradient(180deg, #6a5038, #3a2a1c); }
    #darmy { position: absolute; inset: 0; }
    .dtorch { position: absolute; width: 16px; height: 16px; margin: -8px; border-radius: 50%;
      background: radial-gradient(circle, #fff1c9 0%, #ffae4a 50%, rgba(255,140,40,0) 75%); box-shadow: 0 0 26px 10px rgba(255,150,60,0.35); }
    .dwall { position: absolute; top: 900px; bottom: 0; width: 360px;
      background: linear-gradient(180deg, #e8f4fb 0%, #9cc4de 3%, #3a6a94 14%, #163456 55%, #081a30 100%); box-shadow: 0 0 60px rgba(160,200,240,0.25); }
    #dwl { left: 0; border-radius: 0 40px 0 0; } #dwr { right: 0; border-radius: 40px 0 0 0; }
    #dfoam { position: absolute; inset: 0; opacity: 0;
      background: radial-gradient(ellipse at 50% 70%, rgba(240,250,255,0.9), rgba(200,230,250,0.25) 45%, rgba(0,0,0,0) 75%); }
    #dcalm { position: absolute; inset: 0; opacity: 0; background: linear-gradient(180deg, #1a2440 0%, #6a7a9a 50%, #c8a888 60%, #2a4a6a 62%, #0a2040 100%); }
    .wv { position: absolute; left: 0; top: 0; width: 2160px; height: 1920px; }
    #dsun { position: absolute; left: 440px; top: 1060px; width: 200px; height: 200px; border-radius: 50%; opacity: 0;
      background: radial-gradient(circle, #fff3d6 0%, #ffd08a 40%, rgba(255,180,90,0) 72%); }
"""
    markup = f"""
    <div id="drown" class="clip" data-start="0" data-duration="{total:.2f}">
      <div id="dsky"></div><div id="dpath"></div>
      <div id="darmy"><svg viewBox="0 0 1080 1920" style="position:absolute;inset:0;width:100%;height:100%"><g fill="#07050a" transform="translate(0,1330)">{army}</g></svg>{torches}</div>
      <div id="dwl" class="dwall"></div><div id="dwr" class="dwall"></div>
      <div id="dfoam"></div>
      <div id="dcalm"></div><div id="dsun"></div>
      {waves_svg("dc1", 1200, 14, "#2a4a6a")}{waves_svg("dc2", 1360, 18, "#1a3a5a")}
    </div>"""
    js = []
    for k in range(len(torch_pts)):
        js.append(loop(f"#dt{k}", "opacity: 0.65, scale: 0.9", "opacity: 1, scale: 1.1", 0.5 + (k % 4) * 0.08, total, (k % 5) * 0.05))
    js.append(f'tl.fromTo("#darmy", {{y: 0, scale: 1}}, {{y: 40, scale: 1.06, duration: {crash["start"] + 2:.2f}, ease: "none", transformOrigin: "50% 70%"}}, 0);')
    c0 = crash["start"] + crash["spoken"] * 0.55
    js.append(f'tl.fromTo("#dwl", {{x: 0}}, {{x: 360, duration: 0.9, ease: "power2.in", immediateRender: false}}, {c0:.2f});')
    js.append(f'tl.fromTo("#dwr", {{x: 0}}, {{x: -360, duration: 0.9, ease: "power2.in", immediateRender: false}}, {c0:.2f});')
    js.append(fade("#darmy", 1, 0, c0 + 0.7, 0.3))
    js.append(fade("#dwl", 1, 0, c0 + 1.0, 0.8))
    js.append(fade("#dpath", 1, 0, c0 + 0.7, 0.3))
    js.append(fade("#dwr", 1, 0, c0 + 1.0, 0.8))
    js.append(fade("#dfoam", 0, 1, c0 + 0.7, 0.3))
    js.append(fade("#dfoam", 1, 0.2, c0 + 1.2, 2.5))
    for sel in ("#dc1", "#dc2"):
        js.append(f'tl.set("{sel}", {{opacity: 0}}, 0);')
        js.append(fade(sel, 0, 1, c0 + 0.9, 1.5))
    js.append(f'tl.fromTo("#dc1", {{x: 0}}, {{x: -1080, duration: 14, ease: "none", repeat: {int(total / 14) + 1}}}, 0);')
    js.append(f'tl.fromTo("#dc2", {{x: 0}}, {{x: -1080, duration: 10, ease: "none", repeat: {int(total / 10) + 1}}}, 0);')
    js.append(fade("#dcalm", 0, 1, calm["start"], 2.0))
    js.append(f'tl.fromTo("#dsun", {{opacity: 0, y: 100}}, {{opacity: 1, y: -80, duration: 5, ease: "sine.out", immediateRender: false}}, {calm["start"] + 0.5:.2f});')
    return css, markup, "\n    ".join(js)


SCENES = {"ruins": ruins_scene, "sea": sea_scene, "river": river_scene, "birds": birds_scene, "ayyub": ayyub_scene, "drown": drown_scene}


def vo_len(spec: dict) -> float:
    with wave.open(str(Path(spec["_dir"], "assets/narration.wav"))) as w:
        return w.getnframes() / w.getframerate() - 0.005


def index_html(spec: dict, beats: list, total: float) -> str:
    accent = spec["accent"]
    hosts = []
    for i, b in enumerate(beats):
        bid = f"b{i + 1}"
        hosts.append(f'''      <div id="{bid}" data-composition-id="{bid}" data-composition-src="compositions/{bid}.html"
        data-start="{b["start"]:.2f}" data-duration="{b["dur"]:.2f}" data-track-index="2" data-track-kind="graphics"
        data-width="{W}" data-height="{H}" style="z-index:2"></div>''')
    audio = ""
    if Path(spec["_dir"], "assets/ambience.wav").exists():
        audio = (f'\n      <audio id="amb" class="clip" src="assets/ambience.wav" data-start="0" '
                 f'data-duration="{total:.2f}" data-track-index="11" data-volume="{spec.get("bed_volume", 0.55)}"></audio>')
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>{FONT_FACES}
      :root {{ --ground: #07060c; --ink: #f5ead6; --accent: {accent}; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: var(--ground); }}
      #root {{ width: 100%; height: 100%; position: relative; color: var(--ink); }}
      .txt {{ font-family: "Cormorant Garamond"; font-weight: 600; font-size: 116px; line-height: 1.06;
        letter-spacing: -0.01em; text-shadow: 0 4px 30px rgba(0,0,0,0.65); }}
      .txt .w {{ display: inline-block; }}
      .txt .hi {{ color: var(--accent); }}
      .saw {{ font-family: "Amiri Quran"; font-style: normal; font-size: 0.8em; line-height: 1; }}
      .txt.hook {{ font-size: 132px; text-align: center; line-height: 1.02; }}
      .hook ~ .sub {{ text-align: center; font-size: 76px; }}
      #flash {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 45%, rgba(255,240,215,0.85), rgba(255,200,120,0.25) 60%, rgba(0,0,0,0) 85%); }}
      .txt.cta {{ font-size: 96px; text-align: center; }}
      .sub {{ font-family: "Cormorant Garamond"; font-style: italic; font-weight: 600; font-size: 72px;
        color: rgba(245,234,214,0.82); line-height: 1.15; }}
      .ar {{ font-family: "Amiri Quran"; font-size: 74px; line-height: 1.9; text-align: center; color: #fff6e6;
        text-shadow: 0 0 30px rgba(215,236,255,0.45); }}
      .tr {{ font-family: "Cormorant Garamond"; font-style: italic; font-weight: 600; font-size: {spec.get("tr_size", 74)}px; line-height: 1.15;
        text-align: center; }}
      .ur {{ font-family: "Noto Nastaliq Urdu"; font-size: 46px; line-height: 1.9; color: #fff3dc; text-align: right;
        background: rgba(0,0,0,0.5); border-radius: 18px; padding: 12px 26px 26px; align-self: stretch; }}
      .cta ~ .ur, .ar ~ .ur, .tr ~ .ur {{ text-align: center; }}
      .ref {{ align-self: flex-start; font-family: Inter; font-weight: 700; font-size: 32px; letter-spacing: 0.14em;
        text-transform: uppercase; color: var(--accent); border: 2px solid var(--accent); border-radius: 999px;
        padding: 12px 26px; background: rgba(0,0,0,0.35); }}
      .ar ~ .ref {{ align-self: center; }}
      .orbs {{ position: absolute; left: 0; right: 0; bottom: -420px; height: 200px; }}
      .orb {{ position: absolute; left: 50%; top: 50%; width: 120px; height: 120px; margin: -60px; border-radius: 50%;
        background: radial-gradient(circle, #fff6e0 0%, #ffd27a 40%, rgba(255,190,90,0) 72%);
        box-shadow: 0 0 60px 20px rgba(255,200,110,0.35); }}
      .opts {{ display: flex; flex-direction: column; gap: 22px; }}
      .opt {{ font-family: "Cormorant Garamond"; font-weight: 600; font-size: 76px; padding: 16px 34px;
        border: 2px solid rgba(245,234,214,0.35); border-radius: 24px; background: rgba(0,0,0,0.35); }}
      .opt b {{ font-family: Inter; font-size: 46px; color: var(--accent); margin-right: 26px; }}
      .opt.right {{ border-color: var(--accent); background: rgba(242,163,58,0.18); transform-origin: left center; }}
      .count {{ position: absolute; right: 0; top: -40px; font-family: Inter; font-weight: 900; font-size: 150px;
        color: var(--accent); opacity: 0; }}
      .mark {{ font-family: "Amiri Quran"; font-size: 120px; text-align: center; color: var(--accent); line-height: 1.4; }}
      .btn {{ align-self: center; font-family: Inter; font-weight: 700; font-size: 40px; letter-spacing: 0.08em;
        color: #120b08; background: var(--accent); border-radius: 999px; padding: 22px 48px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.2f}"
      data-width="{W}" data-height="{H}">
      <div id="atmos" data-composition-id="atmos" data-composition-src="compositions/atmos.html"
        data-start="0" data-duration="{total:.2f}" data-track-index="1" data-track-kind="graphics"
        data-width="{W}" data-height="{H}" style="z-index:1"></div>
{chr(10).join(hosts)}
      <audio id="vo" class="clip" src="assets/narration.wav" data-start="0" data-duration="{vo_len(spec):.2f}"
        data-track-index="10" data-volume="1"></audio>{audio}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def main() -> None:
    d = Path(sys.argv[1])
    spec = json.loads((d / "spec.json").read_text(encoding="utf-8"))
    spec["_dir"] = str(d)
    timings = json.loads((d / "assets/timings.json").read_text(encoding="utf-8"))
    if len(timings) != len(spec["beats"]):
        sys.exit(f"{len(spec['beats'])} beats but {len(timings)} narration lines")

    total = round(timings[-1]["end"] + spec.get("hold_end", HOLD_END), 2)
    beats = []
    for i, (b, t) in enumerate(zip(spec["beats"], timings)):
        start = 0.0 if i == 0 else round(t["start"] - LEAD, 2)
        end = total if i == len(timings) - 1 else round(timings[i + 1]["start"] - LEAD, 2)
        beats.append({**b, "_text_right": spec.get("text_right", 140), "_top": spec.get("text_top", 330),
                      "_bottom": spec.get("text_bottom", 600), "start": start, "dur": round(end - start, 2),
                      "spoken": t["end"] - t["start"], "mood": b.get("mood", {"warm": 0.3})})

    (d / "compositions").mkdir(exist_ok=True)
    for i, b in enumerate(beats):
        (d / f"compositions/b{i + 1}.html").write_text(
            beat_html(i, b, b["dur"], b["spoken"], spec["accent"]), encoding="utf-8")
    (d / "compositions/atmos.html").write_text(atmos_html(spec, beats, total), encoding="utf-8")
    (d / "index.html").write_text(index_html(spec, beats, total), encoding="utf-8")
    print(f"built {len(beats)} beats, {total}s")


if __name__ == "__main__":
    main()
