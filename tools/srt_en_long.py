"""English subtitles (.srt) for a long video built with build_long.py, timed from the voice.

Usage: python3 tools/srt_en_long.py <project_dir>
One cue per caption chunk (the same chunks build_long.py shows on screen), placed at the chapter's
start in index.html plus the character alignment of its take. Writes subtitles/en.srt.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_long import chunks  # noqa: E402


def ts(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main() -> None:
    d = Path(sys.argv[1])
    idx = (d / "index.html").read_text(encoding="utf-8")
    starts = {int(m.group(1)): float(m.group(2)) for m in re.finditer(
        r'id="c(\d\d)" data-composition-id="c\d\d".*?data-start="([\d.]+)"', idx, re.S)}
    cues = []
    for n in sorted(starts):
        lines = json.loads((d / f"narration/ch{n:02d}.json").read_text(encoding="utf-8"))["lines"]
        al = json.loads((d / f"assets/ch{n:02d}/take.json").read_text(encoding="utf-8"))
        lead = json.loads((d / f"narration/ch{n:02d}.json").read_text(encoding="utf-8")).get("lead", 0.3)
        cs, ce = al["character_start_times_seconds"], al["character_end_times_seconds"]
        pos = 0
        for line in lines:
            for off, txt in chunks(line):
                a = pos + off
                b = min(a + len(txt) - 1, len(ce) - 1)
                cues.append([starts[n] + lead + cs[a], starts[n] + lead + ce[b], txt])
            pos += len(line) + 1
    for k in range(len(cues) - 1):
        cues[k][1] = min(max(cues[k][1] + 0.3, cues[k][0] + 1.0), cues[k + 1][0] - 0.05)
    (d / "subtitles").mkdir(exist_ok=True)
    out = "\n".join(f"{k + 1}\n{ts(a)} --> {ts(b)}\n{t}\n" for k, (a, b, t) in enumerate(cues))
    (d / "subtitles/en.srt").write_text(out, encoding="utf-8")
    print(f"{len(cues)} cues")


if __name__ == "__main__":
    main()
