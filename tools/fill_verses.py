"""Fill a Short's verse beats from the Quran packages, so no verse is ever typed by hand.

Usage: python3 tools/fill_verses.py <project_dir>
(needs `npm i --no-save quran-json quran-cloud@1.0.0` in the repo root)

In spec.json, a verse beat carries:
  "q": "2:259",              surah:verse
  "ar_words": [a, b],        Arabic words a..b (1-based, inclusive) of the verse
  "en": "…excerpt…",         must be an exact excerpt of Sahih International (quran-json)
  "ur_q": "…excerpt…"        optional; must be an exact excerpt of Maududi (quran-cloud)
The tool writes "arabic", "translation" and (for ur_q) "ur" into the beat, and stops with an
error if any excerpt is not found word for word.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AR = json.loads((ROOT / "node_modules/quran-json/dist/quran.json").read_text(encoding="utf-8"))
EN = json.loads((ROOT / "node_modules/quran-json/dist/quran_en.json").read_text(encoding="utf-8"))
UR = json.loads((ROOT / "node_modules/quran-cloud/dist/quran_ur.json").read_text(encoding="utf-8"))

# Amiri Quran draws the KFGQPC open-tanween code points wrongly; re-encode them for display
# (same fix as build_long.py). The text itself is unchanged.
OPEN_TANWEEN = str.maketrans({"ٗ": "ࣰ", "ٞ": "ࣱ", "ٖ": "ࣲ"})
# Name the audience knows, shown in brackets after the translation's English name.
NAMES = {"Abraham": "Abraham [Ibrahim]", "Moses": "Moses [Musa]", "Job": "Job [Ayyub]",
         "Jonah": "Jonah [Yunus]", "Pharaoh": "Pharaoh [Firaun]"}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[\"“”'‘’…,.;:!?\[\]()-]", " ", s)).strip().lower()


def main() -> None:
    d = Path(sys.argv[1])
    spec = json.loads((d / "spec.json").read_text(encoding="utf-8"))
    bad = []
    for i, b in enumerate(spec["beats"]):
        if "q" not in b:
            continue
        s, v = map(int, b["q"].split(":"))
        words = AR[s - 1]["verses"][v - 1]["text"].split()
        a, z = b["ar_words"]
        b["arabic"] = " ".join(words[a - 1:z]).translate(OPEN_TANWEEN)
        en_full = EN[s - 1]["verses"][v - 1]["translation"]
        if norm(b["en"]) not in norm(en_full):
            bad.append(f"beat {i}: English not in Sahih International {s}:{v}: {b['en']}")
        tr = b["en"]
        for k, val in NAMES.items():
            tr = re.sub(rf"\b{k}\b", val, tr)
        b["translation"] = f"“{tr}”"
        if "ur_q" in b:
            ur_full = UR[s - 1]["verses"][v - 1]["translation"]
            if norm(b["ur_q"]) not in norm(ur_full):
                bad.append(f"beat {i}: Urdu not in Maududi {s}:{v}: {b['ur_q']}")
            b["ur"] = b["ur_q"]
    if bad:
        sys.exit("\n".join(bad))
    (d / "spec.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("verses filled:", sum("q" in b for b in spec["beats"]))


if __name__ == "__main__":
    main()
