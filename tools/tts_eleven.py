"""Narration with ElevenLabs (one take for the whole Short, so the delivery flows).

Usage: python3 tts_eleven.py narration.json out_dir

narration.json: {"eleven": {"voice_id": "...", "model_id": "eleven_multilingual_v2",
                 "settings": {...}}, "lines": ["...", "..."]}
Writes out_dir/narration.wav and out_dir/timings.json ([{text, start, end}]), the same
outputs as tts.py. The API key is added by the session's network proxy, never stored here.
"""
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LEAD = 0.3  # default silence before the first word (narration.json "lead" overrides)
TAIL = 0.3

DEFAULT = {
    "voice_id": "N2lVS1w4EtoT3dr4eOWO",  # Callum: husky, forceful narrator
    "model_id": "eleven_multilingual_v2",
    "settings": {"stability": 0.35, "similarity_boost": 0.8, "style": 0.55, "use_speaker_boost": True},
}


V3 = {"model_id": "eleven_v3", "settings": {"stability": 0.5}}
# Arabic script runs (letters, marks, and the spaces between Arabic words)
AR = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+"
                r"(?:\s+[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+)*")
GAP = 0.12  # silence between a v2 part and a v3 Arabic clip


def synth(text, voice_id, model_id, settings):
    body = json.dumps({"text": text, "model_id": model_id, "voice_settings": settings})
    res = subprocess.run(
        ["curl", "-sS", "-X", "POST",
         f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128",
         "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json", "--data-binary", "@-"],
        input=body.encode(), capture_output=True, check=True)
    data = json.loads(res.stdout)
    if "audio_base64" not in data:
        sys.exit(f"ElevenLabs error: {json.dumps(data)[:400]}")
    return data


def mixed_take(text, el, tmp):
    """English (v2) with Arabic phrases voiced by eleven_v3 (voice.md: never v2 for Arabic).
    Returns (wav path, char start list, char end list) for the whole joined text."""
    parts, pos = [], 0
    for m in AR.finditer(text):
        if m.start() > pos:
            parts.append((pos, m.start(), False))
        parts.append((m.start(), m.end(), True))
        pos = m.end()
    if pos < len(text):
        parts.append((pos, len(text), False))
    starts, ends = [0.0] * len(text), [0.0] * len(text)
    wavs, t = [], 0.0
    for k, (a, b, ar) in enumerate(parts):
        seg = text[a:b]
        if not re.search(r"\w", seg):  # punctuation/space only: no audio
            for i in range(a, b):
                starts[i] = ends[i] = t
            continue
        cfg = V3 if ar else el
        data = synth(seg.strip(), el["voice_id"], cfg["model_id"], cfg["settings"])
        mp3, wav = os.path.join(tmp, f"p{k}.mp3"), os.path.join(tmp, f"p{k}.wav")
        Path(mp3).write_bytes(base64.b64decode(data["audio_base64"]))
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", mp3, "-af", f"apad=pad_dur={GAP}",
                        "-ar", "48000", "-ac", "1", wav], check=True)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav],
                                   capture_output=True, text=True).stdout)
        al = data["alignment"]
        cs, ce = al["character_start_times_seconds"], al["character_end_times_seconds"]
        off = len(seg) - len(seg.lstrip())
        n = len(seg.strip())
        for i in range(a, b):  # map by position (proportional if the model changed the text length)
            j = min(len(cs) - 1, max(0, round((i - a - off) * (len(cs) - 1) / max(1, n - 1)))) if len(cs) != n else min(n - 1, max(0, i - a - off))
            starts[i], ends[i] = cs[j] + t, ce[j] + t
        print(f"  {'v3' if ar else 'v2'} {dur:5.2f}s  {seg.strip()[:60]}")
        wavs.append(wav)
        t += dur
    lst = os.path.join(tmp, "list.txt")
    Path(lst).write_text("".join(f"file '{w}'\n" for w in wavs))
    joined = os.path.join(tmp, "joined.wav")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", joined], check=True)
    return joined, starts, ends


def main() -> None:
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    el = {**DEFAULT, **cfg.get("eleven", {})}
    lead = cfg.get("lead", LEAD)
    lines = cfg["lines"]
    text = " ".join(lines)

    if el["model_id"] != "eleven_v3" and AR.search(text):
        with tempfile.TemporaryDirectory() as tmp:
            joined, starts, ends = mixed_take(text, el, tmp)
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", joined,
                            "-af", (f"adelay={int(lead * 1000)}:all=1," if lead > 0 else "") + f"apad=pad_dur={TAIL}",
                            "-ar", "48000", "-ac", "1", str(out / "narration.wav")], check=True)
        (out / "take.json").write_text(json.dumps({"mixed_v3_arabic": True}), encoding="utf-8")
        write_timings(lines, starts, ends, lead, out)
        return

    body = json.dumps({"text": text, "model_id": el["model_id"], "voice_settings": el["settings"]})
    res = subprocess.run(
        ["curl", "-sS", "-X", "POST",
         f"https://api.elevenlabs.io/v1/text-to-speech/{el['voice_id']}/with-timestamps?output_format=mp3_44100_128",
         "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json", "--data-binary", "@-"],
        input=body.encode(), capture_output=True, check=True)
    data = json.loads(res.stdout)
    if "audio_base64" not in data:
        sys.exit(f"ElevenLabs error: {json.dumps(data)[:400]}")

    with tempfile.TemporaryDirectory() as tmp:
        mp3 = os.path.join(tmp, "take.mp3")
        Path(mp3).write_bytes(base64.b64decode(data["audio_base64"]))
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", mp3,
                        "-af", (f"adelay={int(lead * 1000)}:all=1," if lead > 0 else "") + f"apad=pad_dur={TAIL}",
                        "-ar", "48000", "-ac", "1", str(out / "narration.wav")], check=True)
    (out / "take.json").write_text(json.dumps(data["alignment"]), encoding="utf-8")

    write_timings(lines, data["alignment"]["character_start_times_seconds"],
                  data["alignment"]["character_end_times_seconds"], lead, out)


def write_timings(lines, starts, ends, lead, out):
    """Each line's start/end from the character alignment of the joined text."""
    timings, pos = [], 0
    for line in lines:
        a, b = pos, pos + len(line) - 1
        timings.append({"text": line, "start": round(starts[a] + lead, 3), "end": round(ends[b] + lead, 3)})
        pos += len(line) + 1
    (out / "timings.json").write_text(json.dumps(timings, indent=2, ensure_ascii=False), encoding="utf-8")
    for x in timings:
        print(f"{x['start']:6.2f}-{x['end']:6.2f}  {x['text']}")


if __name__ == "__main__":
    main()
