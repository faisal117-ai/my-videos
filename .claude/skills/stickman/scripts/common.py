"""Shared helpers. Everything is written with pathlib and subprocess lists so it runs the same on Windows, macOS and Linux."""
import os, shutil, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
GL_ARGS = ["--use-angle=swiftshader", "--use-gl=angle", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]


def ffmpeg():
    """System ffmpeg if there is one, otherwise the binary from the imageio-ffmpeg package."""
    found = shutil.which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg not found. Run scripts/doctor.py first.")


def browser_args(three_d=False):
    a = ["--allow-file-access-from-files"]
    return a + GL_ARGS if three_d else a


def page_url(folder):
    return (Path(folder).resolve() / "index.html").as_uri()


def is_3d(folder):
    return (Path(folder) / "lib3d.js").exists()


FRAME_JS = "i=>{const s=renderAt(i/30);return [JSON.stringify(s),document.getElementById('c').toDataURL('image/jpeg',.94)]}"

# Frame size: 1920x1080 by default; set STICKMAN_W/STICKMAN_H (e.g. 1080x1920) for vertical Shorts.
VW = int(os.environ.get("STICKMAN_W", "1920"))
VH = int(os.environ.get("STICKMAN_H", "1080"))
# Use an already-installed Chromium (e.g. STICKMAN_CHROME=/opt/pw-browsers/chromium) instead of Playwright's download.
LAUNCH = {"executable_path": os.environ["STICKMAN_CHROME"]} if os.environ.get("STICKMAN_CHROME") else {}
