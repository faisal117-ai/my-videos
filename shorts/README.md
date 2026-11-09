# Haq Stories Shorts pipeline

Each Short is a HyperFrames project in `shorts/NN-name/`, built from two inputs:

- `narration.json`: the lines the AI voice reads (Kokoro `am_michael`, speed 0.92), one per beat.
- `spec.json`: what each beat shows (text with `*highlighted*` words, verse Arabic + translation, reference chip, and the light's mood: `warm` firelight / `cool` soft light).

## Make a new Short

```bash
PY=<venv with kokoro-onnx soundfile>/bin/python   # pip install kokoro-onnx soundfile
HF="node <hyperframes plugin>/skills/hyperframes/scripts/plugin-cli.mjs"

cd shorts/NN-name
$PY ../../tools/tts.py narration.json assets     # voice + timings.json
$PY ../../tools/ambience.py .                    # no-music sound bed
python3 ../../tools/build_short.py .             # index.html + compositions/
$HF check --json                                 # must be all clean
$HF render -q delivery -o NN-name.mp4
ffmpeg -i NN-name.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=7 -c:a aac -b:a 192k -movflags +faststart out.mp4 && mv out.mp4 NN-name.mp4
```

Copy `assets/fonts/` and `assets/vendor/gsap.min.js` from `01-fire` into each new project.

## Rules
- Arabic comes from the `quran-json` npm package (QuranEnc Uthmani text) and is never typed by hand. The English is Sahih International, from the same package.
- Arabic names are pronounced from the IPA in `tools/tts.py` (`OVERRIDES`). Add a name there when the voice gets one wrong.
- No figures or faces. Prophets and Companions are never represented in any way: no figure,
  silhouette, or light/glow standing in for them. Their words and actions are carried only by the
  voice and on-screen text; the scene shows places, objects, animals and nature.
- Other people in a story (crowds, villains, soldiers) are shown as animated, faceless
  silhouettes. Yusuf's (AS) brothers: only as distant shadows. Never shown: Maryam (AS) and the
  righteous women of the stories, angels and jinn (unseen: shown only through wind, shadow or light
  effects in the scene).
- Every Short gets its own scene that matches its story (fire, cave, desert, mosque…). Only the
  branding stays the same: fonts, gold highlights, the HAQ · STORIES label and the end card.
- No music: a quiet fire or air bed only.
