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
    return html.escape(s, quote=True)


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
        parts.append(f'<div id="{bid}-txt" class="txt"{style}>{words}</div>')
        if beat.get("sub"):
            parts.append(f'<div id="{bid}-sub" class="sub">{esc(beat["sub"])}</div>')
        if reveal:
            stagger = max(spoken * 0.78 / max(n, 1), 0.04)
            js.append(f'tl.fromTo("#{bid} .w", {{opacity: 0, y: 22, filter: "blur(6px)"}}, '
                      f'{{opacity: 1, y: 0, filter: "blur(0px)", duration: 0.32, ease: "power2.out", '
                      f'stagger: {stagger:.3f}}}, 0.12);')
        else:
            # Hook: fully on screen at frame 0, then breathes.
            js.append(f'tl.fromTo("#{bid}-txt", {{scale: 1}}, {{scale: 1.04, duration: {dur:.2f}, ease: "none"}}, 0);')
            if beat.get("sub"):
                js.append(f'tl.fromTo("#{bid}-sub", {{opacity: 0, y: 16}}, '
                          f'{{opacity: 1, y: 0, duration: 0.5, ease: "power2.out"}}, {spoken * 0.45:.2f});')
        js.append(f'tl.fromTo("#{bid} .hi", {{textShadow: "0 0 0px rgba(0,0,0,0)"}}, '
                  f'{{textShadow: "0 0 28px var(--accent)", duration: 0.6, ease: "power1.out"}}, {spoken * 0.5:.2f});')

    if beat.get("ref"):
        parts.append(f'<div id="{bid}-ref" class="ref">{esc(beat["ref"])}</div>')
        js.append(f'tl.fromTo("#{bid}-ref", {{opacity: 0, y: 12}}, '
                  f'{{opacity: 1, y: 0, duration: 0.45, ease: "power2.out"}}, 0.35);')

    # Every beat but the last leaves the same way, landing just before its end.
    if not beat.get("cta"):
        js.append(f'tl.fromTo("#{bid}-wrap", {{opacity: 1}}, {{opacity: 0, duration: 0.22, ease: "power1.in"}}, {dur - 0.24:.2f});')

    body = "\n      ".join(parts)
    side, rail = (60, 60) if beat.get("arabic") or beat.get("cta") else (90, 140)
    script = "\n    ".join(js)
    return f"""<template>
  <style>
    #{bid} {{ position: absolute; inset: 0; }}
    #{bid}-wrap {{ position: absolute; left: {side}px; right: {rail}px; top: 330px; bottom: 600px;
      display: flex; flex-direction: column; justify-content: center; gap: 34px; }}
  </style>
  <div id="{bid}" data-composition-id="{bid}" data-width="{W}" data-height="{H}">
    <div id="{bid}-wrap" class="clip" data-start="0" data-duration="{dur:.2f}">
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


def atmos_html(spec: dict, beats: list, total: float) -> str:
    accent = spec["accent"]
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
        pw, pc, pe = prev.get("warm", 0), prev.get("cool", 0), min(1, prev.get("warm", 0) * 1.4)
        w, c, e = m.get("warm", 0), m.get("cool", 0), min(1, m.get("warm", 0) * 1.4)
        mood_js.append(f'tl.fromTo("#warm-g", {{opacity: {pw}}}, {{opacity: {w}, duration: 0.9, ease: "sine.inOut", immediateRender: false}}, {b["start"]:.2f});')
        mood_js.append(f'tl.fromTo("#cool-g", {{opacity: {pc}}}, {{opacity: {c}, duration: 1.2, ease: "sine.inOut", immediateRender: false}}, {b["start"]:.2f});')
        mood_js.append(f'tl.fromTo("#embers-g", {{opacity: {pe:.2f}}}, {{opacity: {e:.2f}, duration: 0.9, immediateRender: false}}, {b["start"]:.2f});')
        prev = m
    m0 = beats[0]["mood"]
    breathes = int(total / 1.6)

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
    .em {{ position: absolute; bottom: -20px; border-radius: 50%; background: {accent};
      box-shadow: 0 0 12px {accent}, 0 0 24px rgba(255,120,40,0.6); }}
    #vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 45%, rgba(0,0,0,0.7) 100%); }}
    #brand {{ position: absolute; top: 210px; left: 0; right: 0; text-align: center; font-family: Inter; font-weight: 700;
      font-size: 28px; letter-spacing: 0.32em; color: rgba(245,234,214,0.72); }}
    #brand span {{ color: {accent}; }}
  </style>
  <div id="atmos" data-composition-id="atmos" data-width="{W}" data-height="{H}" data-layout-allow-overflow>
    <div id="sky" class="clip" data-start="0" data-duration="{total:.2f}"></div>
    <div id="warm" class="clip" data-start="0" data-duration="{total:.2f}"><div id="warm-g" style="opacity:{m0.get('warm', 0)}"><div id="warm-b"></div></div></div>
    <div id="cool" class="clip" data-start="0" data-duration="{total:.2f}"><div id="cool-g" style="opacity:{m0.get('cool', 0)}"></div></div>
    <div id="embers" class="clip" data-start="0" data-duration="{total:.2f}"><div id="embers-g" style="opacity:{min(1, m0.get('warm', 0) * 1.4):.2f}">
      {"".join(embers)}
    </div></div>
    <div id="vig" class="clip" data-start="0" data-duration="{total:.2f}"></div>
    <div id="brand" class="clip" data-start="0" data-duration="{total:.2f}">HAQ <span>·</span> STORIES</div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
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
                 f'data-duration="{total:.2f}" data-track-index="11" data-volume="0.55"></audio>')
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
