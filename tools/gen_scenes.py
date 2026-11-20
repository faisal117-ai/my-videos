"""Make Gemini stills for a Short: python3 tools/gen_scenes.py <short-dir> [keys...]
Reads <dir>/scenes.json: {"style": "...", "aspect": "9:16", "scenes": {"s1": "...", ...}} and writes
<dir>/assets/gen/<key>.jpg (1188x2112 for 9:16, slight overscan for camera moves)."""
import json, base64, sys, subprocess, io, concurrent.futures as cf
from pathlib import Path
from PIL import Image, ImageEnhance

RULES = ("Ordinary people only; no prophets, no religious or holy figures, no halos, no angels, no women as the "
         "focus, no close-up portraits. No text, no letters, no writing, no logos. ")
MODEL = "gemini-2.5-flash-image"

def trim_bars(im):
    """Crop black letterbox/pillarbox bars Gemini sometimes adds."""
    g = im.convert("L"); w, h = g.size
    rows = [y for y in range(h) if max(g.crop((0, y, w, y + 1)).getdata()) > 24]
    cols = [x for x in range(w) if max(g.crop((x, 0, x + 1, h)).getdata()) > 24]
    if rows and cols and (rows[0] > 4 or h - rows[-1] > 4 or cols[0] > 4 or w - cols[-1] > 4):
        im = im.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))
    return im


def gen(d, cfg, k):
    body = {"contents": [{"parts": [{"text": cfg["style"] + " " + RULES + cfg["scenes"][k]}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": cfg.get("aspect", "9:16")}}}
    out = subprocess.run(["curl", "-sS", "-H", "x-goog-api-key: proxy-injected", "-H", "Content-Type: application/json",
                          "-d", json.dumps(body), f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"],
                         capture_output=True, text=True).stdout
    r = json.loads(out)
    if "error" in r:
        return k, "ERROR " + r["error"]["message"][:200]
    c = (r.get("candidates") or [{}])[0]
    if "content" not in c:
        return k, "blocked " + str(c.get("finishReason", r.get("promptFeedback")))[:120]
    for p in c["content"]["parts"]:
        if "inlineData" in p:
            im = Image.open(io.BytesIO(base64.b64decode(p["inlineData"]["data"]))).convert("RGB")
            im = trim_bars(im)
            size = (1188, 2112) if cfg.get("aspect", "9:16") == "9:16" else (2112, 1188)
            tw, th = size
            s = max(tw / im.width, th / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
            l, u = (im.width - tw) // 2, (im.height - th) // 2; im = im.crop((l, u, l + tw, u + th))
            im = ImageEnhance.Sharpness(im).enhance(1.3)
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
