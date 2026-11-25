"""Build a house-style Short (shorts/24-cave look) from one definition file, end to end except the render.

Usage: python3 tools/new_short.py <definition.json>

definition.json:
{
  "id": "33-dinars",
  "lines":  ["spoken line", ...],                      # Callum, one take
  "eleven": {...}                                       # optional (e.g. Urdu: {"model_id": "eleven_v3", ...})
  "beats":  [{...build_short beat...}, ...],            # same count as lines; verse beats use q/ar_words/en/ur_a
  "photos": ["s1", "c02a", ...],                        # one per beat (key of a scene or a crop)
  "scenes": {"style": "...", "scenes": {"s1": "prompt", ...}},     # optional: Gemini 9:16 stills
  "crops":  {"c02a": "long/04-sulaiman/assets/gen/c02a.jpg", ...}, # optional: centre-crop film stills to 9:16
  "pauses": {"7": 1.0},                                 # silence before these lines (turns)
  "shakes": [...], "glows": [...],                      # house-style effects (beat-based)
  "turn": 7, "hum": 9                                   # beat of the main turn (riser+boom) and where humming starts
}
Writes shorts/<id>/ with spec.json, narration.json, assets/, index.html. Then render with npx hyperframes.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageEnhance

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "shorts/25-throne"
SFX = "../../long/04-sulaiman/assets/sfx/"


def run(*a):
    r = subprocess.run([sys.executable, *a], cwd=ROOT, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    print("\n".join(l for l in out if "Deprecat" not in l and "getdata" not in l)[-400:])
    if r.returncode:
        sys.exit(f"failed: {a}")


def main():
    D = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    d = ROOT / "shorts" / D["id"]
    (d / "assets/gen").mkdir(parents=True, exist_ok=True)
    for f in ["AGENTS.md", "CLAUDE.md", "hyperframes.json", "package.json"]:
        if not (d / f).exists():
            shutil.copy(TPL / f, d / f)
    for sub in ["fonts", "vendor"]:
        if not (d / "assets" / sub).exists():
            shutil.copytree(TPL / "assets" / sub, d / "assets" / sub)
    (d / "meta.json").write_text(json.dumps({"id": D["id"], "name": D["id"], "createdAt": "2026-11-20T20:00:00.000Z"}))
    for k, src in D.get("crops", {}).items():
        if (d / f"assets/gen/{k}.jpg").exists():  # keep relit/edited stills on a re-voice (25 Nov)
            continue
        im = Image.open(ROOT / src)
        w, h = im.size
        cw = int(h * 9 / 16)
        x0 = int((w - cw) * D.get("crop_x", {}).get(k, 0.5))
        im = im.crop((x0, 0, x0 + cw, h)).resize((1188, 2112), Image.LANCZOS)
        ImageEnhance.Sharpness(im).enhance(1.2).save(d / f"assets/gen/{k}.jpg", quality=90)
    if D.get("scenes"):
        sc = dict(D["scenes"]); sc.setdefault("aspect", "9:16")
        (d / "scenes.json").write_text(json.dumps(sc, ensure_ascii=False, indent=1), encoding="utf-8")
        missing = [k for k in sc["scenes"] if not (d / f"assets/gen/{k}.jpg").exists()]
        if missing:
            run("tools/gen_scenes.py", str(d), *missing)
    assert len(D["lines"]) == len(D["beats"]) == len(D["photos"]), "lines, beats and photos must match"
    turn, hum = D.get("turn", len(D["beats"]) // 2), D.get("hum", len(D["beats"]) - 3)
    sound = [
        {"prompt": "lib", "src": "../../long/01-yusuf/assets/sfx/992f69b875be.mp3", "beat": 0, "offset": 0, "dur": 100, "gain": -17, "fade_in": 0.5, "fade_out": 1.5},
        {"prompt": "lib", "src": "../03-cave/assets/sfx/03b5f68efefc.mp3", "beat": 0, "offset": 0.2, "dur": 3, "gain": -13, "fade_in": 0.02, "fade_out": 1},
        {"prompt": "lib", "src": SFX + "93fa1b20e45f.mp3", "beat": max(1, turn - 3), "offset": 0, "dur": 8, "gain": -13, "fade_in": 0.5, "fade_out": 1.5},
        {"prompt": "lib", "src": SFX + "72cc4baec592.mp3", "beat": turn, "offset": -3.6, "dur": 3.8, "gain": -8, "fade_in": 0.4, "fade_out": 0.3},
        {"prompt": "lib", "src": SFX + "f0b78dedaad6.mp3", "beat": turn, "offset": 0, "dur": 4, "gain": -7, "fade_in": 0.02, "fade_out": 1.5},
        {"prompt": "lib", "src": "../06-ant/assets/sfx/cabf6e6577de.mp3", "beat": hum, "offset": 0, "dur": 30, "gain": -13, "fade_in": 1.0, "fade_out": 1.5}]
    spec = {"accent": "#f2b04a", "embers": False, "motes": 0.35, "mote": "#f6dcae", "flash": 0.0, "bed_volume": 1.0,
            "hold_end": D.get("hold_end", 0.3 if D.get("v2") else 1.2), "text_top": 300, "text_bottom": 780, "tr_size": 56, "scene": "photos",
            "photos": [f"assets/gen/{p}.jpg" for p in D["photos"]],
            **({"push": 0.12, "shot2": 4.5, "transform": turn, "bright": True} if D.get("v2") else {}),
            "shakes": D.get("shakes", [{"beat": 0, "at": 0.3, "amp": 8, "dur": 1.0}, {"beat": turn, "at": 0.0, "amp": 10, "dur": 1.4}]),
            "glows": D.get("glows", [{"beat": turn, "at": 0.1, "dur": 3.0, "peak": 0.6}, {"beat": hum, "at": 0.2, "dur": 3.5, "peak": 0.85}]),
            "sound": D.get("sound", sound), "beats": D["beats"]}
    verse = {i for i, b in enumerate(D["beats"]) if "q" in b or "arabic" in b}
    for g in spec["glows"]:  # a strong bloom behind a verse card washes out the translation
        if g["beat"] in verse:
            g["peak"] = min(g["peak"], 0.25)
    (d / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    eleven = D.get("eleven", {"voice_id": "N2lVS1w4EtoT3dr4eOWO"})
    (d / "narration.json").write_text(json.dumps({"lead": 0.3, "eleven": eleven, "lines": D["lines"]}, ensure_ascii=False, indent=1), encoding="utf-8")
    if any("q" in b for b in D["beats"]):
        run("tools/fill_verses.py", str(d))
    (d / "assets/pauses.json").unlink(missing_ok=True)
    run("tools/tts_eleven.py", str(d / "narration.json"), str(d / "assets"))
    if D.get("pauses"):
        pauses = dict(D["pauses"])
        if D.get("v2"):  # tighter lesson (user 25 Nov): at most 0.3 s of silence before the last line
            last = str(len(D["lines"]) - 1)
            if last in pauses:
                pauses[last] = min(pauses[last], 0.3)
        run("tools/short_pauses.py", str(d), json.dumps(pauses))
    run("tools/soundscape.py", str(d))
    run("tools/build_short.py", str(d))
    end = json.loads((d / "assets/timings.json").read_text(encoding="utf-8"))[-1]["end"] + spec["hold_end"]
    words = sum(len(l.split()) for l in D["lines"])
    print(f"LENGTH {end:.1f}s, {words} words" + ("  ** OVER 45 s: cut it **" if end > 45.5 else "  ok (30-45 s rule)"))


if __name__ == "__main__":
    main()
