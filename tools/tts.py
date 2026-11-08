"""Narration for Haq Stories Shorts (local Kokoro voice).

Usage: python tts.py lines.json out_dir

lines.json: {"voice": "am_michael", "speed": 0.92, "gap": 0.35, "lines": ["...", "..."]}
Writes out_dir/narration.wav and out_dir/timings.json ([{text, start, end}]).

Arabic names and honorifics are spoken from the IPA in OVERRIDES, because the
default English phonemizer mispronounces them ("Allah" as "AL-uh", etc.).
"""
import json
import re
import sys
from pathlib import Path

import espeakng_loader
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
from phonemizer import phonemize
from phonemizer.backend.espeak.wrapper import EspeakWrapper

EspeakWrapper.set_library(espeakng_loader.get_library_path())
EspeakWrapper.set_data_path(espeakng_loader.get_data_path())

CACHE = Path.home() / ".cache/hyperframes/tts"
MODEL = CACHE / "models/kokoro-v1.0.onnx"
VOICES = CACHE / "voices/voices-v1.0.bin"

# Longest phrases first so multi-word honorifics win over single names.
OVERRIDES = {
    "sallallahu alayhi wa sallam": "sˌʌlˌɑːlˈɑːhu ʕɐlˈeɪhi wɐ sˈʌlləm",
    "alayhis salaam": "ɐlˈeɪhɪs sɐlˈɑːm",
    "Allah's": "ɐllˈɑːz",
    "Allah": "ɐllˈɑː",
    "Hazrat": "hˈʌzɹət",
    "Ibrahim": "ɪbɹɑːhˈiːm",
    "Sulaiman": "sʊleɪmˈɑːn",
    "Yusuf": "jˈuːsʊf",
    "Yaqub": "jɑːkˈuːb",
    "Al-Anbiya": "ɐl ɐmbiˈjɑː",
    "Al-Kahf": "ɐl kˈɑhf",
    "An-Naml": "ɐn nˈæml",
    "Ash-Sharh": "ɐʃ ʃˈɑːɹh",
    "Quran": "kʊɹˈɑːn",
    "jinn": "dʒˈɪn",
}
PATTERN = re.compile("|".join(re.escape(k) for k in OVERRIDES), re.IGNORECASE)
LOOKUP = {k.lower(): v for k, v in OVERRIDES.items()}


def to_phonemes(text: str) -> str:
    parts, last = [], 0
    for m in PATTERN.finditer(text):
        chunk = text[last : m.start()]
        if chunk.strip():
            parts.append(phonemize(chunk, language="en-us", backend="espeak",
                                   with_stress=True, preserve_punctuation=True).strip())
        parts.append(LOOKUP[m.group(0).lower()])
        last = m.end()
    tail = text[last:]
    if tail.strip():
        parts.append(phonemize(tail, language="en-us", backend="espeak",
                               with_stress=True, preserve_punctuation=True).strip())
    out = " ".join(parts)
    out = re.sub(r"\s+([,.!?;:])", r"\1", out)
    return re.sub(r"\s+", " ", out).strip()


def main() -> None:
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    kokoro = Kokoro(str(MODEL), str(VOICES))
    voice, speed, gap = cfg.get("voice", "am_michael"), cfg.get("speed", 0.92), cfg.get("gap", 0.35)
    lead = cfg.get("lead", 0.3)

    sr = 24000
    audio = [np.zeros(int(lead * sr), dtype=np.float32)]
    t, timings = lead, []
    for line in cfg["lines"]:
        samples, sr = kokoro.create(to_phonemes(line), voice=voice, speed=speed, is_phonemes=True)
        dur = len(samples) / sr
        timings.append({"text": line, "start": round(t, 3), "end": round(t + dur, 3)})
        audio += [samples.astype(np.float32), np.zeros(int(gap * sr), dtype=np.float32)]
        t += dur + gap

    sf.write(out / "narration.wav", np.concatenate(audio), sr)
    (out / "timings.json").write_text(json.dumps(timings, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{t:.2f}s total")
    for x in timings:
        print(f"{x['start']:6.2f}-{x['end']:6.2f}  {x['text']}")


if __name__ == "__main__":
    main()
