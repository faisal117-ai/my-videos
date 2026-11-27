"""Animate one still of a Short into a short moving clip (Atlas Cloud image-to-video) for the motion-first hook test.

Usage: python3 tools/animate_clip.py <short-dir> <beat-index> "<what moves>" [--model M] [--secs 5]

The still must be committed and pushed (it is sent as a raw.githubusercontent URL pinned to HEAD).
Writes <short-dir>/assets/gen/<key>_anim.mp4 and points spec.json photos[beat] at it; build_short.py plays
.mp4 photos muted from the beat's start. Then run tools/build_short.py and render as usual.
Rule check after every clip: NO person may appear that was not in the still, and never a holy figure (CLAUDE.md).
Cost (Nov 2026): seedance-2.0-fast ~$0.07/s of video, so a 5 s hook is ~$0.36.
"""
import json, subprocess, sys, time
from pathlib import Path

API = "https://api.atlascloud.ai/api/v1/model"
HDR = ["-H", "Authorization: Bearer proxy-injected", "-H", "Content-Type: application/json"]
NO_PEOPLE = ("Keep the exact same composition, camera angle and lighting. Subtle, realistic cinematic motion only. "
             "Do NOT add any person, face, figure, hand or silhouette that is not already in the image; existing tiny "
             "distant people may only move slightly. No text, no letters, no logos. Bright clear daylight colours.")


def curl(args):
    out = subprocess.run(["curl", "-sS", *HDR, *args], capture_output=True, text=True).stdout
    return json.loads(out)


def main():
    d, i, motion = Path(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "bytedance/seedance-2.0-fast/image-to-video"
    secs = int(sys.argv[sys.argv.index("--secs") + 1]) if "--secs" in sys.argv else 5
    spec_p = d / "spec.json"
    spec = json.loads(spec_p.read_text(encoding="utf-8"))
    rel = spec["photos"][i]
    if rel.endswith(".mp4"):
        sys.exit(f"beat {i} is already a clip: {rel}")
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    url = f"https://raw.githubusercontent.com/faisal117-ai/my-videos/{head}/{d.as_posix().split('my-videos/')[-1]}/{rel}"
    body = {"model": model, "image": url, "prompt": f"{motion}. {NO_PEOPLE}", "duration": secs}
    r = curl(["-X", "POST", f"{API}/generateVideo", "-d", json.dumps(body)])
    pid = (r.get("data") or {}).get("id")
    if not pid:
        sys.exit(f"Atlas refused: {r}")
    print("prediction", pid)
    for _ in range(120):
        time.sleep(10)
        p = curl([f"{API}/prediction/{pid}"]).get("data") or {}
        st = p.get("status")
        if st in ("completed", "succeeded"):
            out = (p.get("outputs") or [None])[0]
            key = Path(rel).stem + "_anim"
            dst = d / "assets/gen" / f"{key}.mp4"
            subprocess.run(["curl", "-sSL", "-o", str(dst), out], check=True)
            spec["photos"][i] = f"assets/gen/{key}.mp4"
            spec_p.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
            print("saved", dst, "and spec photos[%d] updated; now check every frame for people" % i)
            return
        if st in ("failed", "error", "canceled"):
            sys.exit(f"failed: {p.get('error') or p}")
    sys.exit("timed out waiting for the clip")


if __name__ == "__main__":
    main()
