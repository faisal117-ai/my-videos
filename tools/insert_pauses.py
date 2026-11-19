"""Insert silence before chosen narration lines of a film (a dramatic pause before each turn).
Usage: python3 tools/insert_pauses.py <film-dir> '{"4": {"1": 0.8}, "9": {"3": 1.0}}'   (chapter -> line -> seconds)
Rewrites assets/chNN/narration.wav, timings.json and take.json (character times) so build_long.py keeps the
captions, cards and photo changes in sync. Run once per fresh recording (a marker file prevents doubling)."""
import json, subprocess, sys, tempfile
from pathlib import Path
d = Path(sys.argv[1]); plan = json.loads(sys.argv[2])
for ch, lines in plan.items():
    a = d / f"assets/ch{int(ch):02d}"
    mark = a / "pauses.json"
    if mark.exists(): print("skip (already paused)", a.name); continue
    tim = json.loads((a / "timings.json").read_text(encoding="utf-8"))
    take = json.loads((a / "take.json").read_text(encoding="utf-8"))
    text_lines = json.loads((d / f"narration/ch{int(ch):02d}.json").read_text(encoding="utf-8"))["lines"]
    wav = a / "narration.wav"
    sr = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=sample_rate", "-of", "csv=p=0", str(wav)], capture_output=True, text=True).stdout.strip()
    # cut points: just before each chosen line's start (in the gap after the previous line)
    cuts = sorted((int(k), float(v)) for k, v in lines.items())
    with tempfile.TemporaryDirectory() as t:
        t = Path(t); parts = []; prev = 0.0
        for i, (li, secs) in enumerate(cuts):
            cut = (tim[li - 1]["end"] + tim[li]["start"]) / 2 if li > 0 else tim[0]["start"] * 0.5
            p = t / f"p{i}.wav"; subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-ss", f"{prev:.3f}", "-to", f"{cut:.3f}", str(p)], check=True)
            s = t / f"s{i}.wav"; subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-t", f"{secs}", "-i", f"anullsrc=r={sr}:cl=mono", str(s)], check=True)
            parts += [p, s]; prev = cut
        p = t / "last.wav"; subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-ss", f"{prev:.3f}", str(p)], check=True); parts.append(p)
        (t / "l.txt").write_text("".join(f"file '{x}'\n" for x in parts))
        out = t / "out.wav"; subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(t / "l.txt"), "-ac", "1", "-ar", sr, str(out)], check=True)
        out.replace(wav)
    # shift timings and character times
    pos = [0]
    for l in text_lines: pos.append(pos[-1] + len(l) + 1)
    for li, secs in cuts:
        for x in tim[li:]: x["start"] += secs; x["end"] += secs
        c0 = pos[li]
        for key in ("character_start_times_seconds", "character_end_times_seconds"):
            take[key] = [v + secs if i >= c0 else v for i, v in enumerate(take[key])]
    (a / "timings.json").write_text(json.dumps(tim, ensure_ascii=False, indent=2), encoding="utf-8")
    (a / "take.json").write_text(json.dumps(take), encoding="utf-8")
    mark.write_text(json.dumps(lines))
    print(a.name, "pauses", lines)
