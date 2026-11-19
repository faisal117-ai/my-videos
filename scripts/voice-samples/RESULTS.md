# Voice test, 19 Nov 2026 (same Sulaiman hook in every voice)
Measured with ElevenLabs speech-to-text (accuracy, language heard) and librosa (pitch, expressiveness, pace).

## Urdu
| Voice | Heard as (auto) | Errors (Urdu forced) | Notes |
|---|---|---|---|
| Kamran M (library) | **Urdu** (0.95) | **0** | only voice heard as native Urdu; most confident; fast (3.35 words/s) |
| Naqsh (library) | Hindi | 0 | auto-transcript heard "mulk" for "malika" |
| Amjid (library) | Hindi | 1 ("aap pahuncha") | flat (2.6 st) |
| Adam (default) | Hindi | 0 | low confidence, flat (2.4 st) |
| Callum, Brian, George (default) | Hindi | 1–2 | all said "صورت" for "سورج" (sun) |

## English (all 0–3% errors)
| Voice | Pitch | Expressiveness | Pace | Notes |
|---|---|---|---|---|
| Adam default, dramatic | 121 Hz | **5.3 st** | 2.59 w/s | most expressive; **default voice, retires 31 Dec 2026** |
| Adam library (dark), dramatic settings | **81 Hz** (deepest) | 3.9 st | ~2.3 w/s | permanent (in My Voices) |
| Daniel / George / Adam default calm | 123–134 Hz | 4.2–4.3 st | 2.2–2.7 | defaults, retire 31 Dec |
| Brian | 90 Hz | 3.9 st | 2.86 | default, retires |
| David (movie trailer) | 114 Hz | 4.1 st | **1.58 w/s** | far too slow for the 5-second hook |
| Callum (current) | 107 Hz | 3.3 st (flattest) | 2.46 | default, retires |

## Faisal's own voice (new clone "Faisal Narrator (Haq Stories)", lxAuND1y6e93CWiS40Uz, 19 Nov)
Made from the user's 3.2 min recording (1:43 Urdu + 1:32 English), cleaned with ElevenLabs Voice Isolator (noise -44 → -52 dB).
| Sample | Model | Heard as | Errors | Expressiveness | Noise | Notes |
|---|---|---|---|---|---|---|
| ur-9 | **eleven_v3** | **Urdu (0.95)** | 3% | **6.3 st (highest of all voices)** | -60 dB | best Urdu result of the whole test |
| en-13 | **eleven_v3** | English | 5% (spelling of the honorific only) | **5.5 st** | -53 dB | clean, no fillers |
| en-12 | multilingual_v2 | English | 19% | 2.7 | -45 | v2 invented "um, uh, yeah": do not use v2 with this clone |
| ur-8 | multilingual_v2 | Hindi | – | 3.4 | -42 | v2 sounds Hindi: do not use |
| en-14 | v2, stability 0.7 | English | 0% | 3.1 | -39 | rushed (9.3 s) and noisier |
For comparison Callum: 3.3 st (English), heard as Hindi in Urdu samples. Old 30-second clone "Own": 1.1–1.6 st, noise -35, "uh".
**Use this clone only with eleven_v3.**
