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
        parts.append(f'<div id="{bid}-ar" class="ar" dir="rtl" lang="ar">{esc(beat["arabic"])}</div>')
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

    if beat.get("ref"):
        parts.append(f'<div id="{bid}-ref" class="ref">{esc(beat["ref"])}</div>')
        js.append(f'tl.fromTo("#{bid}-ref", {{opacity: 0, y: 12}}, '
                  f'{{opacity: 1, y: 0, duration: 0.45, ease: "power2.out"}}, 0.35);')

    # Every beat but the last leaves the same way, landing just before its end.
    if not beat.get("cta"):
        js.append(f'tl.fromTo("#{bid}-wrap", {{opacity: 1}}, {{opacity: 0, duration: 0.22, ease: "power1.in"}}, {dur - 0.24:.2f});')

    body = "\n      ".join(parts)
    side, rail = (60, 60) if beat.get("arabic") or beat.get("cta") else (90, 140)
    allow = " data-layout-allow-overflow" if beat.get("lights") else ""
    script = "\n    ".join(js)
    return f"""<template>
  <style>
    #{bid} {{ position: absolute; inset: 0; }}
    #{bid}-wrap {{ position: absolute; left: {side}px; right: {rail}px; top: 330px; bottom: 600px;
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
    elif spec.get("scene") == "storm":
        scene_css, scene_markup, scene_js = storm_scene(spec, beats, total)

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
      .tr {{ font-family: "Cormorant Garamond"; font-style: italic; font-weight: 600; font-size: 74px; line-height: 1.15;
        text-align: center; }}
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

    total = round(timings[-1]["end"] + HOLD_END, 2)
    beats = []
    for i, (b, t) in enumerate(zip(spec["beats"], timings)):
        start = 0.0 if i == 0 else round(t["start"] - LEAD, 2)
        end = total if i == len(timings) - 1 else round(timings[i + 1]["start"] - LEAD, 2)
        beats.append({**b, "start": start, "dur": round(end - start, 2),
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
