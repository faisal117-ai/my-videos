"""Re-record single lines of a long film's narration and splice them into the existing takes.

Usage: python3 tools/respeak_lines.py <project_dir> <edits.json> [--dry]

edits.json: {"<chapter>": {"<line>": "new text", ...}, ...}   (0-based, like narration/chNN.json)

Only the edited lines are sent to ElevenLabs (with the neighbouring lines as context, so the
delivery matches); every other line keeps its original audio. Each chapter's narration.wav,
take.json (character alignment), timings.json and narration/chNN.json are rewritten so
build_long.py, soundscape_long.py and srt_en_long.py work unchanged afterwards.
The new line is level-matched to the line it replaces. The API key is added by the proxy.
"""
import base64
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from tts_eleven import AR, DEFAULT, mixed_take  # noqa: E402

SR = 48000
MARGIN = 0.06  # seconds kept around the new line's first and last character


def read_wav(path: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(path), "-f", "f32le",
                          "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def write_wav(path: Path, x: np.ndarray) -> None:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1",
                    "-i", "-", "-c:a", "pcm_s16le", str(path)], input=x.astype(np.float32).tobytes(), check=True)


def rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(x ** 2))) if len(x) else 0.0


def voiced_span(x: np.ndarray, frame: float = 0.01, below_peak_db: float = 40.0) -> tuple[float, float]:
    """First and last moment the audio is within below_peak_db of its loudest 10 ms frame."""
    n = int(frame * SR)
    fr = x[:len(x) // n * n].reshape(-1, n)
    db = 20 * np.log10(np.sqrt(np.mean(fr ** 2, axis=1)) + 1e-9)
    on = np.where(db > db.max() - below_peak_db)[0]
    return on[0] * frame, (on[-1] + 1) * frame


def speak(text: str, prev: str, nxt: str, el: dict) -> tuple[np.ndarray, dict]:
    if el["model_id"] != "eleven_v3" and AR.search(text):
        # Arabic inside an English line: English on v2, the Arabic run on eleven_v3 (voice.md).
        with tempfile.TemporaryDirectory() as tmp:
            wav, st, en = mixed_take(text, el, tmp)
            audio = read_wav(Path(wav))
        return audio, {"characters": list(text), "character_start_times_seconds": st,
                       "character_end_times_seconds": en}
    body = {"text": text, "model_id": el["model_id"], "voice_settings": el["settings"]}
    if el["model_id"] != "eleven_v3":  # v3 does not take request context
        body |= {"previous_text": prev, "next_text": nxt}
    res = subprocess.run(
        ["curl", "-sS", "-X", "POST",
         f"https://api.elevenlabs.io/v1/text-to-speech/{el['voice_id']}/with-timestamps?output_format=mp3_44100_128",
         "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json", "--data-binary", "@-"],
        input=json.dumps(body).encode(), capture_output=True, check=True)
    data = json.loads(res.stdout)
    if "audio_base64" not in data:
        sys.exit(f"ElevenLabs error: {json.dumps(data)[:400]}")
    with tempfile.TemporaryDirectory() as tmp:
        mp3 = Path(tmp) / "line.mp3"
        mp3.write_bytes(base64.b64decode(data["audio_base64"]))
        audio = read_wav(mp3)
    al = data["alignment"]
    if len(al["characters"]) != len(text):
        sys.exit(f"alignment length {len(al['characters'])} != text length {len(text)} for: {text}")
    return audio, al


def main() -> None:
    d = Path(sys.argv[1])
    edits = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    dry = "--dry" in sys.argv
    total_chars = 0
    for ch_s, line_edits in sorted(edits.items(), key=lambda kv: int(kv[0])):
        n = int(ch_s)
        a = d / f"assets/ch{n:02d}"
        nf = d / f"narration/ch{n:02d}.json"
        cfg = json.loads(nf.read_text(encoding="utf-8"))
        el = {**DEFAULT, **cfg.get("eleven", {})}
        lead = cfg.get("lead", 0.3)
        lines = cfg["lines"]
        new_lines = list(lines)
        for k, t in line_edits.items():
            new_lines[int(k)] = t
        total_chars += sum(len(t) for t in line_edits.values())
        for k, t in sorted(line_edits.items(), key=lambda kv: int(kv[0])):
            print(f"ch{n:02d}:{k}  {lines[int(k)]}\n     → {t}")
        if dry:
            continue

        wav = read_wav(a / "narration.wav")
        timings = json.loads((a / "timings.json").read_text(encoding="utf-8"))
        take = json.loads((a / "take.json").read_text(encoding="utf-8"))
        assert len(timings) == len(lines)
        assert len(take["characters"]) == len(" ".join(lines)), f"ch{n}: take.json does not match the lines"
        wlen = len(wav) / SR
        cuts = [0.0] + [(timings[k]["end"] + timings[k + 1]["start"]) / 2 for k in range(len(lines) - 1)] + [wlen]

        out, chars, cs, ce, new_t = [], [], [], [], []
        off = 0.0  # seconds written so far
        pos = 0    # char index into the old joined text
        for k, line in enumerate(lines):
            c0, c1 = cuts[k], cuts[k + 1]
            s, e = timings[k]["start"], timings[k]["end"]
            if str(k) not in line_edits:
                seg = wav[int(round(c0 * SR)):int(round(c1 * SR))]
                shift = off - c0
                chars += take["characters"][pos:pos + len(line)]
                cs += [t + shift for t in take["character_start_times_seconds"][pos:pos + len(line)]]
                ce += [t + shift for t in take["character_end_times_seconds"][pos:pos + len(line)]]
                new_t.append({"text": line, "start": round(s + shift, 3), "end": round(e + shift, 3)})
            else:
                text = new_lines[k]
                prev = " ".join(new_lines[max(0, k - 2):k])
                nxt = " ".join(new_lines[k + 1:k + 3])
                audio, al = speak(text, prev, nxt, el)
                # Trim by the sound itself (eleven_v3's alignment can end before the speech does),
                # then fit the character times into that span.
                v0, v1 = voiced_span(audio)
                at0, at1 = al["character_start_times_seconds"][0], al["character_end_times_seconds"][-1]
                k_ = (v1 - v0) / max(at1 - at0, 1e-3)
                al["character_start_times_seconds"] = [v0 + (t - at0) * k_ for t in al["character_start_times_seconds"]]
                al["character_end_times_seconds"] = [v0 + (t - at0) * k_ for t in al["character_end_times_seconds"]]
                t0, t1 = v0, v1
                a0, a1 = max(0.0, t0 - MARGIN), min(len(audio) / SR, t1 + MARGIN)
                clip = audio[int(a0 * SR):int(a1 * SR)]
                old = wav[int(s * SR):int(e * SR)]
                if rms(clip) > 0 and rms(old) > 0:
                    clip = clip * (rms(old) / rms(clip))
                pre = np.zeros(max(0, int(round((s - c0 - (t0 - a0)) * SR))), dtype=np.float32)
                post = np.zeros(max(0, int(round((c1 - e - (a1 - t1)) * SR))), dtype=np.float32)
                seg = np.concatenate([pre, clip, post])
                base = off + len(pre) / SR - a0  # wav time of the clip's t = 0
                chars += al["characters"]
                cs += [t + base - lead for t in al["character_start_times_seconds"]]
                ce += [t + base - lead for t in al["character_end_times_seconds"]]
                new_t.append({"text": text, "start": round(t0 + base, 3), "end": round(t1 + base, 3)})
            out.append(seg)
            off += len(seg) / SR
            pos += len(line) + 1
            if k < len(lines) - 1:  # the joining space
                chars.append(" ")
                cs.append(ce[-1])
                ce.append(ce[-1])

        # The old take.json times were relative to the take (wav time - lead); keep that convention.
        # Unchanged lines were shifted in that frame already, since both frames differ by the same lead.
        assert len(chars) == len(" ".join(new_lines))
        write_wav(a / "narration.wav", np.concatenate(out))
        (a / "take.json").write_text(json.dumps({"characters": chars, "character_start_times_seconds": cs,
                                                  "character_end_times_seconds": ce}), encoding="utf-8")
        (a / "timings.json").write_text(json.dumps(new_t, indent=2, ensure_ascii=False), encoding="utf-8")
        cfg["lines"] = new_lines
        nf.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"ch{n:02d}: {wlen:.2f}s → {off:.2f}s")
    print(f"characters sent: {total_chars}")


if __name__ == "__main__":
    main()
