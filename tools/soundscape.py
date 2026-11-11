"""Story soundscape + humming bed from ElevenLabs sound generation, mixed under the voice.

Usage: python3 soundscape.py <project_dir>

spec.json "sound": [
  {"prompt": "heavy rain and distant thunder at night", "beat": 0, "offset": 0, "dur": 18,
   "gain": -6, "fade_in": 0, "fade_out": 2},
  ...
]
Each layer starts at its beat's start (+ offset seconds) and lasts dur seconds (max 22 per
generation; longer layers loop). gain is in dB. Writes assets/ambience.wav, which
build_short.py places under the narration. Generated clips are cached in assets/sfx/.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

LEAD = 0.15  # same as build_short.py: a beat appears this long before its line


def generate(prompt: str, dur: float, out: Path) -> None:
    body = json.dumps({"text": prompt, "duration_seconds": min(dur, 22), "prompt_influence": 0.45})
    res = subprocess.run(
        ["curl", "-sS", "-X", "POST", "https://api.elevenlabs.io/v1/sound-generation",
         "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json",
         "--data-binary", "@-", "-o", str(out), "-w", "%{http_code}"],
        input=body.encode(), capture_output=True, check=True)
    if res.stdout.decode().strip() != "200":
        msg = out.read_bytes()[:300].decode(errors="replace")
        out.unlink(missing_ok=True)
        sys.exit(f"ElevenLabs sound generation failed: {msg}")


def clip_lufs(path: Path) -> float:
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    vals = re.findall(r"I:\s+(-?[\d.]+) LUFS", out)
    v = float(vals[-1]) if vals else -20.0
    return v if v > -70 else -20.0


def boost(l: float) -> float:
    """Level-match a clip to REF, but never lift a near-silent clip by more than 25 dB."""
    return max(min(REF - l, 25.0), -25.0)


REF = -20.0  # every generated clip is level-matched to this before its own gain is applied


def main() -> None:
    d = Path(sys.argv[1])
    spec = json.loads((d / "spec.json").read_text(encoding="utf-8"))
    timings = json.loads((d / "assets/timings.json").read_text(encoding="utf-8"))
    total = timings[-1]["end"] + spec.get("hold_end", 1.4)
    starts = [0.0] + [t["start"] - LEAD for t in timings[1:]]
    cache = d / "assets/sfx"
    cache.mkdir(parents=True, exist_ok=True)

    inputs, filters = [], []
    for k, layer in enumerate(spec["sound"]):
        gen_dur = min(layer["dur"], 22)
        key = hashlib.sha1(f'{layer["prompt"]}|{gen_dur}'.encode()).hexdigest()[:12]
        clip = cache / f"{key}.mp3"
        if not clip.exists():
            print(f"generating: {layer['prompt'][:60]}…")
            generate(layer["prompt"], gen_dur, clip)
        start = max(0.0, starts[layer.get("beat", 0)] + layer.get("offset", 0))
        dur = min(layer["dur"], total - start)
        loop = ["-stream_loop", "-1"] if layer["dur"] > gen_dur else []
        inputs += loop + ["-i", str(clip)]
        fi, fo = layer.get("fade_in", 0.5), layer.get("fade_out", 1.5)
        chain = (f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur:.2f},asetpts=PTS-STARTPTS,"
                 f"volume={layer.get('gain', 0) + boost(clip_lufs(clip)) + 14:.2f}dB")
        if fi > 0:
            chain += f",afade=t=in:st=0:d={fi}"
        chain += f",afade=t=out:st={max(0.0, dur - fo):.2f}:d={fo},adelay={int(start * 1000)}:all=1[a{k}]"
        filters.append(chain)

    n = len(spec["sound"])
    mix = "".join(f"[a{k}]" for k in range(n)) + f"amix=inputs={n}:normalize=0:duration=longest,apad=whole_dur={total:.2f},atrim=0:{total:.2f}[out]"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs,
                    "-filter_complex", ";".join(filters + [mix]), "-map", "[out]",
                    "-ar", "48000", str(d / "assets/ambience.wav")], check=True)
    print(f"soundscape: {n} layers, {total:.2f}s")


if __name__ == "__main__":
    main()
