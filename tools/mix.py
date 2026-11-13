"""Final audio mix for a rendered Short: voice on top, story soundscape clearly audible.

Usage: python3 mix.py <project_dir> <video.mp4> [bed_offset_lu]

The bed is set bed_offset_lu (default 6) below the voice, then ducked under the voice with a
sidechain compressor, so it rises in the gaps between lines and dips while Callum speaks.
The video stream is copied; the audio is replaced and loudness-normalised to -14 LUFS.
"""
import json
import re
import subprocess
import sys
from pathlib import Path


def lufs(path: Path) -> float:
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1])


def main() -> None:
    d = Path(sys.argv[1])
    video = Path(sys.argv[2])
    offset = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0
    voice, bed = d / "assets/narration.wav", d / "assets/ambience.wav"
    gain = (lufs(voice) - offset) - lufs(bed)
    tmp = video.with_suffix(".mix.mp4")
    pre = (f"[1:a]aresample=48000,aformat=channel_layouts=stereo,asplit=2[v1][v2];"
           f"[2:a]aresample=48000,aformat=channel_layouts=stereo,volume={gain:.2f}dB[bed];"
           f"[bed][v1]sidechaincompress=threshold=0.05:ratio=2.5:attack=20:release=250:makeup=1[duck];"
           f"[v2][duck]amix=inputs=2:normalize=0:duration=longest,afade=t=in:st=0:d=0.05")
    # Two-pass loudnorm: measure the whole mix, then apply one fixed (linear) gain. Single-pass
    # loudnorm starts with a guessed gain and can push the first transient over 0 dBTP.
    probe = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(video), "-i", str(voice), "-i", str(bed),
                            "-filter_complex", pre + ",loudnorm=I=-14:TP=-2:LRA=11:print_format=json[a]",
                            "-map", "[a]", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    norm = (f"loudnorm=I=-14:TP=-2:LRA=11:linear=true:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}")
    graph = pre + f",{norm},aresample=48000,alimiter=limit=0.7:level=false[a]"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video), "-i", str(voice),
                    "-i", str(bed), "-filter_complex", graph, "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart",
                    str(tmp)], check=True)
    tmp.replace(video)
    print(json.dumps({"bed_gain_db": round(gain, 1), "final_lufs": lufs(video)}))


if __name__ == "__main__":
    main()
