"""Soundscape + voice track for a long video built with build_long.py.

Usage: python3 soundscape_long.py <project_dir>

Reads spec.json "sound": layers anchored to a chapter and a line:
  {"prompt": "...", "ch": 2, "line": 6, "offset": 1.5, "dur": 3, "gain": -8, "fade_in": 0, "fade_out": 1.5}
  or {"src": "../../shorts/03-cave/assets/sfx/xxx.mp3", ...} to reuse a clip (no credits).
"line" may be omitted (chapter start); "until": [ch, line] sets dur to end at that line, and
"until_end": true to the chapter's end. Layers longer than their clip loop.
Writes assets/ambience.wav and assets/narration.wav (the chapter takes placed on the timeline),
the two inputs tools/mix.py expects. Generation, caching and level-matching are shared with
soundscape.py.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from soundscape import boost, clip_lufs, generate  # noqa: E402


def probe(path: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                capture_output=True, text=True).stdout or 0)


def main() -> None:
    d = Path(sys.argv[1])
    spec = json.loads((d / "spec.json").read_text(encoding="utf-8"))
    idx = (d / "index.html").read_text(encoding="utf-8")
    total = float(re.search(r'id="root"[^>]*data-duration="([\d.]+)"', idx).group(1))
    hosts = {int(m.group(1)): (float(m.group(2)), float(m.group(3))) for m in re.finditer(
        r'id="c(\d\d)" data-composition-id="c\d\d".*?data-start="([\d.]+)" data-duration="([\d.]+)"', idx, re.S)}
    timings = {n: json.loads((d / f"assets/ch{n:02d}/timings.json").read_text(encoding="utf-8")) for n in hosts}

    def at(ch, line=None):
        return hosts[ch][0] + (timings[ch][line]["start"] if line is not None else 0.0)

    # Voice: every chapter take at its place on the timeline.
    vin, vf = [], []
    for k, n in enumerate(sorted(hosts)):
        vin += ["-i", str(d / f"assets/ch{n:02d}/narration.wav")]
        vf.append(f"[{k}:a]aresample=48000,adelay={int(hosts[n][0] * 1000)}:all=1[v{k}]")
    vmix = "".join(f"[v{k}]" for k in range(len(hosts))) + \
        f"amix=inputs={len(hosts)}:normalize=0,apad=whole_dur={total:.2f},atrim=0:{total:.2f}[out]"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *vin, "-filter_complex", ";".join(vf + [vmix]),
                    "-map", "[out]", "-ac", "1", "-ar", "48000", str(d / "assets/narration.wav")], check=True)

    cache = d / "assets/sfx"
    cache.mkdir(parents=True, exist_ok=True)
    inputs, filters = [], []
    for k, layer in enumerate(spec["sound"]):
        start = max(0.0, at(layer["ch"], layer.get("line")) + layer.get("offset", 0))
        if "until" in layer:
            dur = at(*layer["until"]) - start
        elif layer.get("until_end"):
            dur = sum(hosts[layer["ch"]]) - start
        else:
            dur = layer["dur"]
        dur = max(min(dur, total - start), 0.5)
        if layer.get("src"):
            clip = (d / layer["src"]).resolve()
        else:
            gen_dur = min(layer.get("gen", 22), 22)  # beds: one 22 s clip per prompt, looped
            key = hashlib.sha1(f'{layer["prompt"]}|{gen_dur}'.encode()).hexdigest()[:12]
            clip = cache / f"{key}.mp3"
            if not clip.exists():
                print(f"generating: {layer['prompt'][:70]}…", flush=True)
                generate(layer["prompt"], gen_dur, clip)
        loop = ["-stream_loop", "-1"] if dur > probe(clip) - 0.05 else []
        inputs += loop + ["-i", str(clip)]
        fi, fo = layer.get("fade_in", 1.0), layer.get("fade_out", 1.5)
        chain = (f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur:.2f},asetpts=PTS-STARTPTS,"
                 f"volume={layer.get('gain', 0) + boost(clip_lufs(clip)) + 14:.2f}dB")
        if fi > 0:
            chain += f",afade=t=in:st=0:d={fi}"
        chain += f",afade=t=out:st={max(0.0, dur - fo):.2f}:d={min(fo, dur)},adelay={int(start * 1000)}:all=1[a{k}]"
        filters.append(chain)
    n = len(spec["sound"])
    mix = "".join(f"[a{k}]" for k in range(n)) + \
        f"amix=inputs={n}:normalize=0:duration=longest,apad=whole_dur={total:.2f},atrim=0:{total:.2f}[out]"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(filters + [mix]),
                    "-map", "[out]", "-ar", "48000", str(d / "assets/ambience.wav")], check=True)
    print(f"soundscape: {n} layers, voice + bed {total:.2f}s")


if __name__ == "__main__":
    main()
