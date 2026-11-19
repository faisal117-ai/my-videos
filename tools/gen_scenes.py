"""Make Gemini stills for a Short: python3 tools/gen_scenes.py <short-dir> [keys...]
Reads <dir>/scenes.json: {"style": "...", "aspect": "9:16", "scenes": {"s1": "...", ...}} and writes
<dir>/assets/gen/<key>.jpg (1188x2112 for 9:16, slight overscan for camera moves)."""
import json, base64, sys, subprocess, io, concurrent.futures as cf
from pathlib import Path
from PIL import Image, ImageEnhance

RULES = ("Ordinary people only; no prophets, no religious or holy figures, no halos, no angels, no women as the "
         "focus, no close-up portraits. No text, no letters, no writing, no logos. ")
MODEL = "gemini-2.5-flash-image"

def gen(d, cfg, k):
    body = {"contents": [{"parts": [{"text": cfg["style"] + " " + RULES + cfg["scenes"][k]}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": cfg.get("aspect", "9:16")}}}
    out = subprocess.run(["curl", "-sS", "-H", "x-goog-api-key: proxy-injected", "-H", "Content-Type: application/json",
                          "-d", json.dumps(body), f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"],
                         capture_output=True, text=True).stdout
    r = json.loads(out)
    if "error" in r:
        return k, "ERROR " + r["error"]["message"][:200]
    for p in r["candidates"][0]["content"]["parts"]:
        if "inlineData" in p:
            im = Image.open(io.BytesIO(base64.b64decode(p["inlineData"]["data"]))).convert("RGB")
            size = (1188, 2112) if cfg.get("aspect", "9:16") == "9:16" else (2112, 1188)
            im = ImageEnhance.Sharpness(im.resize(size, Image.LANCZOS)).enhance(1.3)
            im.save(d / "assets/gen" / f"{k}.jpg", quality=90)
            return k, "ok"
    return k, "no image"

if __name__ == "__main__":
    d = Path(sys.argv[1]); cfg = json.loads((d / "scenes.json").read_text(encoding="utf-8"))
    (d / "assets/gen").mkdir(parents=True, exist_ok=True)
    keys = sys.argv[2:] or list(cfg["scenes"])
    with cf.ThreadPoolExecutor(7) as ex:
        for k, s in ex.map(lambda k: gen(d, cfg, k), keys):
            print(d.name, k, s)
