# New film thumbnails and titles (14 Nov 2026)

Why: the Yusuf film got 1,500 impressions but only 0.8% clicked (healthy is 4–10%). The old
thumbnails (thin serif text on dark scenes) turn into a dark smudge at phone size.
New style: one big bright image, 3–5 huge bold words, the "X… then Y" shape that works on our Shorts.
Made by `tools/thumbs_v2.py`. No prophet, righteous woman, angel or person is drawn.

| Film | Use first | For Test & Compare | New title |
|---|---|---|---|
| Yusuf (published) | `yusuf-a-well.jpg` | `yusuf-b-dream.jpg`, `yusuf-c-split.jpg` | His Brothers Threw Him in a Well… He Became King \| Prophet Yusuf (AS) Full Story |
| Musa (published) | `musa-a-sea.jpg` | `musa-b-pharaoh.jpg`, `musa-c-basket.jpg` | The Sea Split… and Pharaoh Drowned \| Prophet Musa (AS) Full Story |
| Ibrahim (Sat 21 Nov) | `ibrahim-a-fire.jpg` | `ibrahim-b-idols.jpg`, `ibrahim-c-kaaba.jpg` | Thrown Into the Fire… It Became Cool \| Prophet Ibrahim (AS) Full Story |
| Ibrahim Urdu (Sun 22 Nov) | `ibrahim-ur-fire.jpg` | – | (unchanged) Hazrat Ibrahim AS Ka Mukammal Waqia \| Full Movie in Urdu \| حضرت ابراہیمؑ |

The Ibrahim films are updated in Metricool. Yusuf and Musa are already published, so they are changed
in YouTube Studio: video → Details → Title and Thumbnail (phone), or Thumbnail → Test & compare
(computer) with all three options.

## Update (14 Nov, night): packaging rules applied (yt-package)
The first set broke two rules: the thumbnail repeated the title, and it had 5–6 words (3 is the
ceiling at feed size). Titles were 65–80 characters (desktop search cuts at 60) and carried no number.

| Film | Title (scored) | Thumbnail (3 words, different from the title) |
|---|---|---|
| Yusuf | Prophet Yusuf (AS): The Dream of 11 Stars Came True (100/100; Quran 12:4) | `final-yusuf.jpg` "DOWN THE WELL" |
| Musa | Prophet Musa (AS) and the 9 Signs Pharaoh Denied (100/100; Quran 17:101) | `final-musa.jpg`: the original art the user preferred, "THE SEA SPLIT" in bold |
| Ibrahim | Prophet Ibrahim (AS): The Fire That Became Cool (84/100, no number in the Quran story) | `final-ibrahim.jpg` "THROWN IN ALIVE" |
| Ibrahim Urdu | unchanged | `final-ibrahim-ur.jpg` "زندہ آگ میں" |

Voice profile for packaging: `scripts/voice.md`.

## Decision (14 Nov, night): the user prefers the bright 5–6-word set
Back in use: Yusuf `yusuf-a-well.jpg` (changed in Studio by the user), Ibrahim `ibrahim-a-fire.jpg` with
"Thrown Into the Fire… It Became Cool | Prophet Ibrahim (AS) Full Story", Ibrahim Urdu `ibrahim-ur-fire.jpg`
(Metricool updated). Musa keeps its original thumbnail. The `final-*` three-word versions stay here for a
Test & Compare later; the CTR numbers will decide.
