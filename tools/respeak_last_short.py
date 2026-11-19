"""Replace the last spoken line of a Short (e.g. "Follow for more.") with new text.
Usage: python3 tools/respeak_last_short.py <short-dir> "<new last line>"
Cuts narration.wav at the old last line's start, records the new line with the same voice (ElevenLabs,
key added by the proxy), appends it, and fixes timings.json and narration.json."""
import base64, json, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tts_eleven import DEFAULT

d = Path(sys.argv[1]); new = sys.argv[2]
nar = json.loads((d / "narration.json").read_text(encoding="utf-8"))
tim = json.loads((d / "assets/timings.json").read_text(encoding="utf-8"))
el = {**DEFAULT, **nar.get("eleven", {})}
prev = " ".join(nar["lines"][-3:-1])
body = json.dumps({"text": new, "model_id": el["model_id"], "voice_settings": el["settings"], "previous_text": prev})
r = subprocess.run(["curl", "-sS", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{el['voice_id']}?output_format=mp3_44100_128",
                    "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json", "-d", body], capture_output=True)
if r.stdout[:1] == b"{": sys.exit(r.stdout[:300])
with tempfile.TemporaryDirectory() as t:
    t = Path(t); (t / "new.mp3").write_bytes(r.stdout)
    start = tim[-1]["start"]
    wav = d / "assets/narration.wav"
    sr = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=sample_rate,channels", "-of", "csv=p=0", str(wav)], capture_output=True, text=True).stdout.strip().split(",")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-t", f"{start:.3f}", str(t / "head.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(t / "new.mp3"), "-af", "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse",
                    "-ar", sr[0], "-ac", sr[1], str(t / "new.wav")], check=True)
    newlen = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(t / "new.wav")], capture_output=True, text=True).stdout)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(t / "head.wav"), "-i", str(t / "new.wav"), "-f", "lavfi", "-t", "0.3", "-i", f"anullsrc=r={sr[0]}:cl={'stereo' if sr[1]=='2' else 'mono'}",
                    "-filter_complex", "[0][1][2]concat=n=3:v=0:a=1", str(wav)], check=True)
tim[-1] = {"text": new, "start": start, "end": round(start + newlen, 3)}
(d / "assets/timings.json").write_text(json.dumps(tim, ensure_ascii=False, indent=2), encoding="utf-8")
nar["lines"][-1] = new
(d / "narration.json").write_text(json.dumps(nar, ensure_ascii=False, indent=2), encoding="utf-8")
print(d.name, "new last line", round(newlen, 2), "s")
