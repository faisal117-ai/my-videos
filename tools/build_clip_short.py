"""Build a vertical Short (HyperFrames project) from moments of a long video, with no new voice.

Usage: python3 build_clip_short.py <short_dir>

<short_dir>/clip.json:
{
  "source": "../../long/01-yusuf",            # the long video project
  "segments": [{"ch": 11, "from": 0, "to": 0, "focus": 960}, ...],   # line ranges, in order
  "beats": [ ... one Shorts beat per line, in order (build_short.py beat fields) ...
             verse beats: {"v": 89, "ar": [1, 9], "en": "<exact Sahih excerpt>", "ur": "..."} ],
  "end": {"text": "Watch the *full story* on the channel", "ur": "..."}
}
Cuts the voice and the sound bed for each segment from the long video (assets/narration.wav and
assets/ambience.wav, made by soundscape_long.py), plays each segment's own scene from the same
moment, scaled to fill 1080x1920 around "focus" (an x in the 1920-wide scene), and lays the
Shorts text beats from build_short.py over it. Then render and run tools/mix.py as for any Short.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_long as BL  # noqa: E402
import build_short as BS  # noqa: E402

GAP = 0.35      # silence between segments
PRE, POST = 0.2, 0.35
END_CARD = 3.4  # seconds of end card after the last line
W, H = 1080, 1920
SCALE = H / BL.H


def host_starts(src: Path):
    idx = (src / "index.html").read_text(encoding="utf-8")
    return {int(m.group(1)): (float(m.group(2)), float(m.group(3))) for m in re.finditer(
        r'id="c(\d\d)" data-composition-id="c\d\d".*?data-start="([\d.]+)" data-duration="([\d.]+)"', idx, re.S)}


def verse(beat: dict, quran: dict) -> dict:
    v = quran[str(beat["v"])]
    a, b = beat["ar"]
    if beat["en"] not in v["en"]:
        sys.exit(f"12:{beat['v']}: English excerpt not in Sahih International: {beat['en']!r}")
    lead = "" if v["en"].startswith(beat["en"]) else "…"
    tail = "" if v["en"].rstrip(" .").endswith(beat["en"]) else "…"
    return {**beat, "arabic": " ".join(v["ar"].split(" ")[a:b + 1]).translate(BL.OPEN_TANWEEN),
            "translation": f"“{lead}{BL.show_en(beat['en'])}{tail}”", "ref": f"Yusuf 12:{beat['v']}"}


def main() -> None:
    d = Path(sys.argv[1])
    clip = json.loads((d / "clip.json").read_text(encoding="utf-8"))
    src = (d / clip["source"]).resolve()
    lspec = json.loads((src / "spec.json").read_text(encoding="utf-8"))
    quran = json.loads((src / "assets/surah12.json").read_text(encoding="utf-8"))["verses"]
    hosts = host_starts(src)
    (d / "assets").mkdir(exist_ok=True)
    (d / "compositions").mkdir(exist_ok=True)

    # 1. Where each segment sits on the long video's timeline and on the Short's.
    segs, lines, at = [], [], 0.0
    for s in clip["segments"]:
        tm = json.loads((src / f"assets/ch{s['ch']:02d}/timings.json").read_text(encoding="utf-8"))
        a = max(tm[s["from"]]["start"] - PRE, 0)
        b = tm[s["to"]]["end"] + POST
        segs.append({**s, "a": a, "b": b, "at": at, "dur": b - a, "tm": tm})
        for k in range(s["from"], s["to"] + 1):
            lines.append({"text": tm[k]["text"], "start": round(at + tm[k]["start"] - a, 3),
                          "end": round(at + tm[k]["end"] - a, 3)})
        at += (b - a) + GAP
    voice_end = at - GAP
    total = round(voice_end + END_CARD, 2)
    if len(clip["beats"]) != len(lines):
        sys.exit(f"{len(clip['beats'])} beats but {len(lines)} lines")
    (d / "assets/timings.json").write_text(json.dumps(lines, indent=2, ensure_ascii=False), encoding="utf-8")

    # 2. Voice and sound bed: the same moments cut from the long video's tracks.
    for name, tail in (("narration.wav", 0.0), ("ambience.wav", END_CARD)):
        ins, fl = [], []
        for k, s in enumerate(segs):
            g = hosts[s["ch"]][0]
            extra = tail if k == len(segs) - 1 else 0.0
            ins += ["-ss", f"{g + s['a']:.3f}", "-t", f"{s['dur'] + extra:.3f}", "-i", str(src / "assets" / name)]
            fade = f",afade=t=out:st={s['dur'] + extra - 1.2:.3f}:d=1.2" if name == "ambience.wav" else ""
            fl.append(f"[{k}:a]afade=t=in:d=0.08{fade},adelay={int(s['at'] * 1000)}:all=1[a{k}]")
        mix = "".join(f"[a{k}]" for k in range(len(segs))) + \
            f"amix=inputs={len(segs)}:normalize=0,apad=whole_dur={total},atrim=0:{total}[out]"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *ins, "-filter_complex",
                        ";".join(fl + [mix]), "-map", "[out]", "-ar", "48000", str(d / "assets" / name)], check=True)

    # 3. Scenes: each segment plays its chapter's scene from the same moment, reframed to 9:16.
    css, markup, js = [], [], []
    for k, s in enumerate(segs):
        ch = lspec["chapters"][s["ch"]]
        chdur = hosts[s["ch"]][1]
        t = BL.TL(chdur)
        L, E = [x["start"] for x in s["tm"]], [x["end"] for x in s["tm"]]
        scss, smark = BL.SCENES[ch["scene"]](t, L, E, chdur)
        p = f"s{k}"
        left = W / 2 - s.get("focus", 960) * SCALE
        css.append((BL.BASE_CSS + scss).replace("§", f"{p}-"))
        markup.append(f'''<div id="{p}-seg" class="clip" data-start="{s["at"]:.2f}" data-duration="{s["dur"] + (END_CARD if k == len(segs) - 1 else GAP):.2f}" style="position:absolute;inset:0;overflow:hidden">
      <div id="{p}-box" style="position:absolute;left:{left:.0f}px;top:0;width:{BL.W}px;height:{BL.H}px;transform-origin:0 0;transform:scale({SCALE:.4f})">
        <div id="{p}-cam" class="{p}-cam" style="position:absolute;inset:0">{smark.replace("§", f"{p}-")}</div>
      </div></div>''')
        body = "\n    ".join(x.replace("tl.", f"st{k}.") for x in t.js).replace("§", f"{p}-")
        play = s["dur"] + (END_CARD if k == len(segs) - 1 else GAP)
        js.append(f"const st{k} = gsap.timeline({{ paused: true }});\n    {body}\n    "
                  f"tl.add(st{k}.tweenFromTo({s['a']:.2f}, {min(s['a'] + play, chdur):.2f}, {{ ease: 'none' }}), {s['at']:.2f});")
        js.append(f'tl.fromTo("#{p}-cam", {{scale: 1}}, {{scale: 1.06, duration: {play:.2f}, ease: "none", transformOrigin: "{s.get("focus", 960)}px 50%", immediateRender: false}}, {s["at"]:.2f});')
        if k > 0:
            js.append(f'tl.fromTo("#{p}-seg", {{opacity: 0}}, {{opacity: 1, duration: 0.35, ease: "sine.inOut", immediateRender: false}}, {s["at"]:.2f});')
    atmos = f"""<template>
  <style>
    #atmos {{ position: absolute; inset: 0; overflow: hidden; background: #000; }}{"".join(css)}
    #scrim {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.45) 55%, rgba(0,0,0,0) 75%); }}
    #brand {{ position: absolute; top: 210px; left: 0; right: 0; text-align: center; font-family: Inter; font-weight: 700;
      font-size: 28px; letter-spacing: 0.32em; color: rgba(245,234,214,0.72); }}
    #brand span {{ color: {lspec["accent"]}; }}
  </style>
  <div id="atmos" data-composition-id="atmos" data-width="{W}" data-height="{H}" data-layout-allow-overflow>
    {chr(10).join("    " + m for m in markup).strip()}
    <div id="scrim" class="clip" data-start="0" data-duration="{total:.2f}"></div>
    <div id="brand" class="clip" data-start="0" data-duration="{total:.2f}">HAQ <span>·</span> STORIES</div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join("    " + x for x in js).strip()}
    window.__timelines["atmos"] = tl;
  </script>
</template>
"""
    (d / "compositions/atmos.html").write_text(atmos, encoding="utf-8")

    # 4. Text beats (the Shorts' own look), one per line, then the end card.
    spec = {"accent": lspec["accent"], "_dir": str(d), "tr_size": clip.get("tr_size", 56), "bed_volume": 1.0}
    beats = []
    raw = [verse(b, quran) if "v" in b else b for b in clip["beats"]] + [{**clip["end"], "cta": True}]
    for i, b in enumerate(raw):
        if i < len(lines):
            start = 0.0 if i == 0 else round(lines[i]["start"] - BS.LEAD, 2)
            end = round(lines[i + 1]["start"] - BS.LEAD, 2) if i + 1 < len(lines) else round(voice_end + 0.2, 2)
            spoken = lines[i]["end"] - lines[i]["start"]
        else:
            start, end, spoken = round(voice_end + 0.2, 2), total, 1.5
        beats.append({**b, "_text_right": 90, "_top": clip.get("text_top", 300), "_bottom": clip.get("text_bottom", 780),
                      "start": start, "dur": round(end - start, 2), "spoken": spoken, "mood": {"warm": 0}})
    for i, b in enumerate(beats):
        (d / f"compositions/b{i + 1}.html").write_text(BS.beat_html(i, b, b["dur"], b["spoken"], spec["accent"]), encoding="utf-8")
    (d / "index.html").write_text(BS.index_html(spec, beats, total), encoding="utf-8")
    print(f"built {len(beats)} beats from {len(segs)} segments, {total}s")


if __name__ == "__main__":
    main()
