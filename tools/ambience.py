"""Synthesize a no-music ambience bed that follows each beat's mood.

Usage: python ambience.py <project_dir>
warm -> fire crackle and rumble; cool -> a soft, airy tone. Seeded, so rebuilds match.
"""
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 48000


def lowpass(x: np.ndarray, a: float) -> np.ndarray:
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc)
        y[i] = acc
    return y


def main() -> None:
    d = Path(sys.argv[1])
    spec = json.loads((d / "spec.json").read_text(encoding="utf-8"))
    timings = json.loads((d / "assets/timings.json").read_text(encoding="utf-8"))
    total = timings[-1]["end"] + 1.4
    n = int(total * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(11)

    # Mood envelopes, eased between beats.
    warm = np.zeros(n)
    cool = np.zeros(n)
    starts = [0.0] + [x["start"] - 0.15 for x in timings[1:]]
    for i, b in enumerate(spec["beats"]):
        a = int(starts[i] * SR)
        warm[a:] = b.get("mood", {}).get("warm", 0.3)
        cool[a:] = b.get("mood", {}).get("cool", 0)
    k = int(0.9 * SR)
    kernel = np.ones(k) / k
    warm = np.convolve(warm, kernel, mode="same")
    cool = np.convolve(cool, kernel, mode="same")

    # Fire: brown rumble + sparse crackles.
    white = rng.standard_normal(n)
    rumble = np.cumsum(white)
    rumble -= np.convolve(rumble, np.ones(4800) / 4800, mode="same")
    rumble /= np.max(np.abs(rumble)) + 1e-9
    crackle = np.zeros(n)
    for pos in rng.integers(0, n - 2000, size=int(total * 14)):
        L = int(rng.integers(200, 1400))
        crackle[pos:pos + L] += rng.standard_normal(L) * np.exp(-np.linspace(0, 9, L)) * rng.uniform(0.2, 1.0)
    fire = 0.55 * rumble + 0.35 * crackle

    # Cool: a quiet open fifth with slow shimmer.
    pad = (np.sin(2 * np.pi * 196 * t) + 0.6 * np.sin(2 * np.pi * 293.66 * t)
           + 0.3 * np.sin(2 * np.pi * 392 * t)) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t))
    pad /= np.max(np.abs(pad))

    mix = fire * warm * 0.22 + pad * cool * 0.06
    if spec.get("impact"):
        # A low hit on frame 1: tells a scrolling viewer something is happening.
        L = int(0.9 * SR)
        tt = np.arange(L) / SR
        hit = (np.sin(2 * np.pi * (70 - 30 * tt) * tt) * np.exp(-tt * 5)
               + 0.35 * rng.standard_normal(L) * np.exp(-tt * 25))
        mix[:L] += hit * 0.5
    fade = int(0.6 * SR)
    if not spec.get("impact"):
        mix[:fade] *= np.linspace(0, 1, fade)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix = np.clip(mix, -0.95, 0.95).astype(np.float32)
    sf.write(d / "assets/ambience.wav", np.stack([mix, mix], axis=1), SR)
    print(f"ambience {total:.2f}s")


if __name__ == "__main__":
    main()
