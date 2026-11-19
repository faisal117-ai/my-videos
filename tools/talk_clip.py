"""Code-made 'talking' for a Gemini still: the jaw/lips area is warped open and closed in time with the
speaker's voice (loudness envelope), plus a slight breathing sway. Free, no AI video.

Usage: python3 tools/talk_clip.py <short-dir> <job.json>
job.json: [{"img": "assets/gen/s4.jpg", "out": "assets/gen/talk_s4.mp4", "t0": 22.69, "dur": 8.6,
            "mouth": [901, 1120], "w": 30, "drop": 4, "speech": [[23.8, 30.4]]}]
t0/dur: picture time the clip covers (its beat start, beat length + 0.6). speech: windows (picture time)
where this man is talking. mouth: lip centre in image pixels; w: half-width of the mouth; drop: max jaw
drop in pixels. Reads <dir>/assets/narration.wav for the envelope.
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np, cv2

FPS = 30

def envelope(wav, fps):
    with wave.open(str(wav)) as w:
        sr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32)
    if ch > 1: x = x.reshape(-1, ch).mean(1)
    hop = sr // fps
    frames = len(x) // hop
    rms = np.sqrt(np.mean(x[:frames * hop].reshape(frames, hop) ** 2, axis=1))
    return rms

def main():
    d = Path(sys.argv[1]); jobs = json.loads(Path(sys.argv[2]).read_text())
    rms = envelope(d / "assets/narration.wav", FPS)
    for j in jobs:
        img = cv2.imread(str(d / j["img"])); H, W = img.shape[:2]
        mx, my = j["mouth"]; w = j.get("w", 30); drop = j.get("drop", 4)
        n = int(round(j["dur"] * FPS))
        # envelope for this man only, normalised on his own speech
        a = np.zeros(n)
        idx = [int(round((j["t0"] + k / FPS) * FPS)) for k in range(n)]
        on = np.array([any(s <= j["t0"] + k / FPS <= e for s, e in j["speech"]) for k in range(n)])
        vals = np.array([rms[i] if 0 <= i < len(rms) else 0 for i in idx])
        peak = np.percentile(vals[on], 90) if on.any() else 1
        a = np.clip(vals / (peak + 1e-6), 0, 1.2) * on
        a = np.convolve(a, [0.25, 0.5, 0.25], mode="same")  # soften
        a = np.where(a < 0.12, 0, a)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        # jaw: pixels below the lip line move down, fading with distance (an elliptical region)
        gx = np.exp(-((xx - mx) / (w * 1.25)) ** 2)
        below = np.clip((yy - my) / (w * 0.15) + 0.5, 0, 1)
        fall = np.exp(-np.clip(yy - my, 0, None) / (w * 1.6))
        jaw = (gx * below * fall).astype(np.float32)
        # lips: a thin dark gap at the lip line that opens with the jaw
        gap = (np.exp(-((xx - mx) / (w * 0.7)) ** 2) * np.exp(-((yy - my) / 1.6) ** 2)).astype(np.float32)
        out = d / j["out"]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                              "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                              "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
        for k in range(n):
            o = float(a[k]) * drop
            sway = 1.2 * np.sin(2 * np.pi * k / (FPS * 3.2))  # gentle breathing / sway, pixels
            mapy = yy - jaw * o - sway * np.exp(-((yy - my + 3 * w) / (6 * w)) ** 2) * np.exp(-((xx - mx) / (5 * w)) ** 2)
            fr = cv2.remap(img, xx, mapy.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            if o > 0.3:
                dark = (gap * min(1.0, o / drop) * 0.55)[..., None]
                fr = (fr * (1 - dark) + fr * 0.25 * dark).astype(np.uint8)
            p.stdin.write(fr.tobytes())
        p.stdin.close(); p.wait()
        print("wrote", out, f"{n} frames, talking {on.mean() * 100:.0f}%")

if __name__ == "__main__":
    main()
