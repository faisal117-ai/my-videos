"""Insert silence before chosen lines of a Short (a dramatic pause before each turn).
Usage: python3 tools/short_pauses.py <short-dir> '{"5": 0.8, "7": 1.0}'   (line index -> seconds)
Rewrites assets/narration.wav and assets/timings.json. Run once per fresh recording (pauses.json marks it)."""
import json, sys, wave
from pathlib import Path
d = Path(sys.argv[1]) / "assets"; plan = {int(k): float(v) for k, v in json.loads(sys.argv[2]).items()}
if (d / "pauses.json").exists(): sys.exit("already paused")
t = json.loads((d / "timings.json").read_text(encoding="utf-8"))
w = wave.open(str(d / "narration.wav")); p = w.getparams(); fr = w.readframes(p.nframes); w.close()
bpf = p.sampwidth * p.nchannels; sr = p.framerate; out = b""; prev = 0
for i in sorted(plan):
    c = int(((t[i - 1]["end"] + t[i]["start"]) / 2) * sr) * bpf
    out += fr[prev:c] + b"\0" * (int(plan[i] * sr) * bpf); prev = c
out += fr[prev:]
for j, x in enumerate(t):
    add = sum(v for i, v in plan.items() if j >= i)
    x["start"] = round(x["start"] + add, 3); x["end"] = round(x["end"] + add, 3)
o = wave.open(str(d / "narration.wav"), "w"); o.setparams(p); o.writeframes(out); o.close()
(d / "timings.json").write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
(d / "pauses.json").write_text(json.dumps(plan), encoding="utf-8")
print("paused; ends at", t[-1]["end"])
