"""Sound mix for one film. build.py runs this inside the film folder.
Edit the marked block only. Plants and EVENTS come from film.js, so sound stays on the picture's clock."""
import json, os, sys
sys.path.insert(0, os.environ["STICKMAN_SCRIPTS"])
from audio_kit import Mix

info = json.load(open("film.json"))
m = Mix(info["dur"], seed=9)

# ---- EDIT FROM HERE: set this from the sound brief ----
import json as _j
TM=_j.load(open("../timing.json")); L=TM["L"]; D=info["dur"]; T=lambda i:L[i][0]
SFX, MUSIC, VOICE = True, False, "vo.wav"
R3=T(10)-.35
if SFX:
    m.wind_bed([(0, .5), (1.2, .5), (1.6, .05), (T(3)-.3, .05), (T(3), 0), (T(4)-.2, 0), (T(4), .06), (T(8)-.2, .1), (T(8), .35), (T(9)-.2, .35), (T(9), .1), (R3, .1), (R3+1.5, .6), (D, .5)])
    m.room_bed([(0, 0), (1.5, 0), (1.8, .35), (T(3)-.3, .35), (T(3), .5), (T(4)-.2, .5), (T(4), .35), (R3+.5, .3), (R3+1.6, 0), (D, 0)])
    m.drone([(0, 0), (1.5, .5), (T(2), .35), (T(3), .1), (T(4), .45), (T(8), .1), (T(9), .5), (R3, .6), (R3+1.6, 0), (D, 0)])
    for k, ts in info["plants"].items():
        for t in ts: m.step(t - .03, pan=.2, g=.16, surface="grass" if k=="worker" else "concrete")
    for e in info["events"]:
        t, k = e["t"], e["k"]
        if k == "rockfall": m.thunder(t, g=.9, pan=.2); m.sfx("impactwood-heavy-001", t, .45, 900, .9, .2, .6); m.sfx("impactsoft-heavy-000", t, .4, 300, 1., 0, .5)
        elif k == "rockmove": m.sfx("impactwood-heavy-001", t, .5, 1100, .6, .3, .5); m.nb(t, 60, 400, 1.2, .05, .9, .5, .3)
        elif k == "rockroll": m.whoosh(t+.4, pan=.4, d=1.6, g=.5); m.thunder(t, g=.6, pan=.4); m.nb(t, 50, 380, 2.2, .1, 1.5, .6, .4)
        elif k == "heart": m.heart(t, g=.5)
if MUSIC:
    m.music(mood="warm")
if VOICE:
    m.voice(VOICE, at=.5, cuts=[(c, h) for c, h in TM["holds"]])
# ---- TO HERE ----
m.write("audio.wav")
