"""English + Hindi subtitles (.srt) for an Urdu long film, timed from the Urdu voice.

Usage: python3 tools/srt_ur_film.py <urdu_project_dir> <english_project_dir>
  e.g. python3 tools/srt_ur_film.py long/04-sulaiman-ur long/04-sulaiman

The Urdu and English scripts have the same chapters and the same number of lines (one English line
per Urdu line), so each Urdu line's time span (index.html chapter start + assets/chNN/timings.json)
carries:
  - en.srt: the source-checked English line (no new translation is made);
  - hi.srt: the Urdu line written in Devanagari (Hindustani transliteration by Gemini, not a
    re-translation; cached in subtitles/hi_lines.json so it can be checked and edited by hand).
Long lines are split at sentence ends; each piece gets time in proportion to its length.
"""
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

MODEL = "gemini-3.8-flash"
MAX = 90  # characters per cue


def ts(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def split(text: str) -> list[str]:
    parts = [p.strip() for p in re.split(r"(?<=[.?!۔؟।])\s+", text.strip()) if p.strip()]
    out = []
    for p in parts:  # merge short pieces, keep each cue under MAX where possible
        if out and len(out[-1]) + len(p) + 1 <= MAX:
            out[-1] += " " + p
        else:
            out.append(p)
    return out or [text.strip()]


def gemini(prompt: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0, "responseMimeType": "application/json"}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json",
                                          "x-goog-api-key": os.environ.get("GEMINI_API_KEY", "proxy-injected")})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]


def to_hindi(lines: list[str]) -> list[str]:
    prompt = (
        "Transliterate each Urdu line below into Hindi (Devanagari script) for Hindi-reading viewers. "
        "Keep the SAME words and meaning (Hindustani): do not translate, summarise, add or drop anything. "
        "Keep honorifics exactly in meaning: علیہ السلام → अलैहिस्सलाम, صلی اللہ علیہ وسلم → सल्लल्लाहु अलैहि वसल्लम, "
        "رضی اللہ عنہ → रज़ियल्लाहु अन्हु; keep Quran verse quotes as quotes. Use नुक़्ता where natural (ज़, फ़, ख़, ग़, क़). "
        "Return a JSON array of strings, one per input line, same count and order.\n\n"
        + json.dumps(lines, ensure_ascii=False))
    out = json.loads(gemini(prompt))
    if len(out) != len(lines):
        raise SystemExit(f"Gemini returned {len(out)} lines for {len(lines)}")
    return out


def main() -> None:
    ur, en = Path(sys.argv[1]), Path(sys.argv[2])
    idx = (ur / "index.html").read_text(encoding="utf-8")
    starts = {int(m.group(1)): float(m.group(2)) for m in re.finditer(
        r'id="c(\d\d)" data-composition-id="c\d\d".*?data-start="([\d.]+)"', idx, re.S)}
    (ur / "subtitles").mkdir(exist_ok=True)
    cache = ur / "subtitles/hi_lines.json"
    hi_all = json.loads(cache.read_text(encoding="utf-8")) if cache.exists() else {}
    spans = []  # (start, end, en_line, hi_line)
    for n in sorted(starts):
        ul = json.loads((ur / f"narration/ch{n:02d}.json").read_text(encoding="utf-8"))["lines"]
        el = json.loads((en / f"narration/ch{n:02d}.json").read_text(encoding="utf-8"))["lines"]
        tm = json.loads((ur / f"assets/ch{n:02d}/timings.json").read_text(encoding="utf-8"))
        if not (len(ul) == len(el) == len(tm)):
            raise SystemExit(f"ch{n:02d}: {len(ul)} Urdu, {len(el)} English, {len(tm)} timings")
        key = f"ch{n:02d}"
        if key not in hi_all:
            hi_all[key] = to_hindi(ul)
            cache.write_text(json.dumps(hi_all, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"{key}: Hindi done")
        for t, e, h in zip(tm, el, hi_all[key]):
            spans.append((starts[n] + t["start"], starts[n] + t["end"], e, h))
    for lang, col in (("en", 2), ("hi", 3)):
        cues = []
        for s in spans:
            a, b, pieces = s[0], s[1], split(s[col])
            total = sum(len(p) for p in pieces)
            t = a
            for p in pieces:
                d = (b - a) * len(p) / total
                cues.append([t, t + d, p])
                t += d
        for k in range(len(cues) - 1):
            cues[k][1] = min(cues[k][1] + 0.4, cues[k + 1][0] - 0.05)
        out = "\n".join(f"{k + 1}\n{ts(a)} --> {ts(b)}\n{t}\n" for k, (a, b, t) in enumerate(cues))
        (ur / f"subtitles/{lang}.srt").write_text(out, encoding="utf-8")
        print(f"subtitles/{lang}.srt: {len(cues)} cues")


if __name__ == "__main__":
    main()
