"""Write YouTube subtitle files (Urdu + English .srt) for a long video built with build_long.py.

Usage: python3 subtitles_long.py <project_dir>

Reads subtitles_cues.json (one cue per spoken sentence, timed from the voice alignment) and
subtitles_ur.json (one Urdu line per cue). Verse quotes in the Urdu are marked «N|text»; each
text must be an exact excerpt of Maududi's translation of Yusuf 12:N in assets/surah12_ur.json,
so no Quran translation is ever typed from memory. Writes subtitles/ur.srt and subtitles/en.srt.
"""
import json
import re
import sys
from pathlib import Path


def ts(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def main() -> None:
    d = Path(sys.argv[1])
    cues = json.loads((d / "subtitles_cues.json").read_text(encoding="utf-8"))
    ur = json.loads((d / "subtitles_ur.json").read_text(encoding="utf-8"))["lines"]
    maududi = json.loads((d / "assets/surah12_ur.json").read_text(encoding="utf-8"))["verses"]
    if len(ur) != len(cues):
        sys.exit(f"{len(cues)} cues but {len(ur)} Urdu lines")
    bad = []
    for i, line in enumerate(ur):
        for v, text in re.findall(r"«(\d+)\|([^»]+)»", line):
            if norm(text) not in norm(maududi[v]):
                bad.append(f"cue {i}: 12:{v} excerpt not in Maududi: {text}")
    if bad:
        sys.exit("\n".join(bad))
    out = d / "subtitles"
    out.mkdir(exist_ok=True)
    for lang, texts in (("ur", [re.sub(r"«\d+\|([^»]+)»", r"“\1”", t) for t in ur]), ("en", [c["en"] for c in cues])):
        blocks = []
        for i, (c, text) in enumerate(zip(cues, texts)):
            nxt = cues[i + 1]["start"] if i + 1 < len(cues) else c["end"] + 2
            start, end = max(c["start"] - 0.05, 0), min(c["end"] + 0.6, nxt - 0.05)
            blocks.append(f"{i + 1}\n{ts(start)} --> {ts(end)}\n{text}\n")
        (out / f"{lang}.srt").write_text("\n".join(blocks), encoding="utf-8")
    print(f"wrote {len(cues)} cues: subtitles/ur.srt, subtitles/en.srt")


if __name__ == "__main__":
    main()
