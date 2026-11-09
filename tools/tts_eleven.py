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


def main() -> None:
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    el = {**DEFAULT, **cfg.get("eleven", {})}
    lead = cfg.get("lead", LEAD)
    lines = cfg["lines"]
    text = " ".join(lines)

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

    # Each line's start/end from the character alignment of the joined text.
    starts = data["alignment"]["character_start_times_seconds"]
    ends = data["alignment"]["character_end_times_seconds"]
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
