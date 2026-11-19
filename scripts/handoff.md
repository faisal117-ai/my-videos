# Handoff (17 Nov 2026, evening): read this first in a new session

Read next: `scripts/channel-plan.md` (start-here index, core message, decisions), `scripts/series-plan.md`,
`scripts/shorts-plan.md`, `scripts/competitor-analysis.md`, `scripts/voice.md`.

## Where things stand
- Channel: Haq Stories | حق کہانیاں (UCVWzdTZ9UL_fxTgOV3mCOGQ), 141 subscribers (16 Nov). Metricool brand 8081200,
  tz Asia/Karachi. Repo working branch → merged to `main` after every change (user's rule).
- Published films: English Yusuf (EP 1), Musa (EP 2); Urdu Musa (EP 1), Urdu Yusuf (EP 2, live 17 Nov 19:00).
- Scheduled in Metricool through Sun 22 Nov: two Shorts a day (11:00, 18:30); Ibrahim English EP 3 Sat 21 18:30,
  Ibrahim Urdu EP 3 Sun 22 18:30 (titles with EP numbers, Urdu/Hindi).
- Google Ads: prepaid PKR 4,250 campaign (English + Urdu Musa) runs out by itself; no more paid ads after it.
- ElevenLabs: about 64,000 characters left on 17 Nov evening (80,000 before the honorific fixes); the user keeps the full schedule; warn before the Khalid arc (12 Dec).

## Open items
- **Opening test, "stayed to watch" (17 Nov, Studio):** Pharaoh (medium, "He called himself a god… until the sea")
  **37.8%** (237 views, 8 h) · four birds (bright) 31% · Musa's mother (dark) 30% · Ayyub (bright) 29.8% (325 views;
  avg 0:23 = 82% of the Short; one big drop around 7–10 s, the second "hardship" line, then flat) · Yunus (bright,
  but its first frame is a near-black sea) **19.8%** (173 views). So brightness alone did not lift it; the first
  line did. Rule approved by the user 17 Nov (now in scripts/shorts-plan.md craft rules): open on a named person + defiance or a surprising act and a
  promise of a turn ("…until", "…then Allah"), not a list of suffering or a gruesome detail; no second hardship
  line, go to the dua by ~6 s; a truly lit first frame. Dark-opening Shorts (wall, Nuh, idols, sacrifice) still
  to compare at the Friday review.
- **Honorifics (17 Nov):** both Ibrahim EP 3 films re-voiced with "alayhis salaam" / "peace be upon him"
  (English 27 lines spliced with tools/respeak_lines.py; Urdu 11 chapters re-recorded whole, since eleven_v3
  timings are too loose to splice). New lengths EN 14:53, UR 15:23; renders swapped into Metricool with the new
  chapter times. ElevenLabs used ~15,500 characters (about 64,000 left if it was 80,000 before). The published
  Yusuf and Musa films stay as they are (user's choice, already live); the sun Short (18 Nov) keeps "one of the prophets" (user's choice).
  This session runs on the "my-videos" environment (the one with the ElevenLabs key).
- **Title test started early (18 Nov):** question titles on Thu 19 11:00 ("Can a Man Who Killed 100 Be Forgiven? 🤲"),
  Fri 20 18:30 ("What Happened After 950 Years? 🌧️"), Sat 21 11:00 ("Why Did He Leave the Biggest Idol Standing? 🪓");
  "X… then Y" kept on Qarun (Thu 18:30), hoopoe (Fri 11:00), sacrifice (Sun 11:00). Videos unchanged.
- **Core message added to this week's Shorts (19 Nov):** Qarun (+28:82, 19 Nov 18:30), Nuh (+54:10 dua, 20 Nov 18:30),
  idols (+21:69, 21 Nov 11:00) re-voiced, re-rendered and swapped in Metricool. Hoopoe and sacrifice unchanged.
- Translations ready to paste (user does it in Studio): `scripts/translations/*.md` (Arabic, Indonesian, Bengali,
  Turkish for English films; Hindi for Urdu films).
- Upcoming Shorts with dark openings are kept as they are (user's choice, a test): wall Wed, Nuh Fri, idols Sat,
  sacrifice Sun.

## Gemini image generation (19 Nov, in progress)
- The user wants ordinary people that look like animated movies, close to real (Pixar/Disney-style), in Shorts,
  films and thumbnails (film rule 9 in shorts-plan.md). Our SVG/HyperFrames drawing cannot do that look, so we
  use Google's Gemini image model (e.g. gemini-2.5-flash-image) to make the scenes, then animate them (slow
  camera moves, light, effects) under our voice and captions. A flat-figure attempt was rejected and reverted.
- The key: a network secret on the "my-videos" environment, host generativelanguage.googleapis.com, header
  x-goog-api-key, no prefix. The key is a new-style Google "auth key" starting with "AQ." (AI Studio's cURL
  quickstart confirms the X-goog-api-key header). Send "x-goog-api-key: proxy-injected"; the proxy fills it in.
- In the old session (session_019ZSVGUajUktRZV46QR3pPi) Google kept answering 400 API_KEY_INVALID (the first
  version of the secret had a "Bearer" prefix; the user re-added it without one). First job in a new session:
  curl https://generativelanguage.googleapis.com/v1beta/models?pageSize=200 with that header. If 400 again,
  ask the user to create a fresh key in AI Studio (Create API key -> Create in new project) and re-save the
  secret. The user is on an iPhone only (no computer): secrets are added in Safari at claude.ai/code (desktop
  view), environment menu -> Edit -> Network secrets.
- 19 Nov, new session (session_019ZSVGUB7fBBbYPfjP19HVe): still 400 API_KEY_INVALID, with or without the header, so the
  proxy is sending the saved value and Google rejects it. Correction: since mid-2026 AI Studio only issues
  "AQ." auth keys, so the prefix is fine; the saved value itself is wrong (copy, spaces, prefix or old key). The secure key form was declined (it may not show on the iPhone); the user is to re-save the secret
  by hand (new AQ. key, empty prefix), then say "try again".
- FIXED 19 Nov: the secret had the website typed into the Header name box. Re-added with header x-goog-api-key,
  empty prefix -> models list works (200). Image models: gemini-2.5-flash-image, gemini-3.1-flash-image(-preview),
  gemini-3.1-flash-lite-image, gemini-3-pro-image(-preview). Every image model answers 429 "free tier limit: 0",
  so billing must be turned on before any image can be made (test prompt: an ordinary market crowd, 9:16).
- 19 Nov 18:00: billing on (prepaid $5 credit, user's choice; tell the user before it runs out). Qarun Short
  rebuilt with 6 Gemini scenes (shorts/17-qarun/assets/gen, scene "photos" in tools/build_short.py: one still per
  beat, slow push-in, cross-fades, shake_beat), moved to 19:00 PKT, swapped in Metricool with isAiGeneratedContent
  true. ~7 images used so far (~$0.28). Next: hoopoe (Fri 11:00), Nuh (Fri 18:30), idols (Sat 11:00).
- Billing: the image model probably needs billing turned on in AI Studio (~$0.04/image); the user has not added
  any yet. If generation fails with a billing/quota error, tell them how (AI Studio -> Set up billing, set a cap).
- Then: make one test image (an ordinary crowd scene, no prophet, Companion, righteous woman or angel) and
  show the user; then rebuild this week's Shorts with people: Qarun (procession + envious onlookers, 28:79),
  hoopoe (Sheba's people bowing to the sun, 27:24), Nuh (chiefs mocking the ship, 11:38), idols (the people
  returning, 21:59); sacrifice has no ordinary people, leave it. Videos with realistic synthetic people go up
  with isAiGeneratedContent true.

## Decision of 19 Nov
- **Schedule change (19 Nov, user):** Ibrahim films moved to Sat 28 (EN) / Sun 29 (UR) 18:30 and become **EP 4**;
  they are to be rebuilt with Gemini scenes (same narration) and swapped in Metricool before then (old renders
  are in the slots as placeholders). **Sulaiman (AS) film = EP 3, Sat 21 (EN) / Sun 22 (UR) 18:30**, script in
  long/04-sulaiman/script.md, waiting for the user's approval before voicing. Nuh film becomes EP 5 (5–6 Dec).
  The old-session reminders for Ibrahim (trig_011f8…, trig_017D9…, trig_013xr…, trig_019fj…) were moved to
  28/29 Nov; their texts still say "EP 3" (prompts can only be edited from that session): read them as EP 4.
- **Shorts ending fixed (19 Nov):** hoopoe, Nuh, idols, sacrifice now end with the voice and card "Watch the full
  movie… link below" (tools/respeak_last_short.py re-voices only the last line). Earlier Shorts this week still
  ended "Follow for more." Apply the ending to every new Short.
- **Captions on photo Shorts:** compact top band (COMPACT_CSS in tools/build_short.py) so the picture is clear.
- **Every Short and film from now on is made with Gemini scenes** (user's rule; shorts-plan.md rule 9).
- **Evening Shorts at 17:00 PKT from 20 Nov** (user's choice; Metricool best-time data peaks 16:00, falls after 17:00). Morning Shorts stay 11:00, films stay 18:30. Nuh moved to Fri 20 Nov 17:00.
- Near-real ordinary people (crowds, soldiers, kings, the man who killed 100…) are now shown in thumbnails and scenes, as a rule (shorts-plan.md film rule 9). Never prophets, the Prophet ﷺ, Companions, righteous women or angels. Film titles lead with a story question.

## Decisions of 17–18 Nov (all recorded in the plan files; apply them to every new script)
- **Honorifics every time** (scripts/voice.md): alayhis salaam / (AS), peace be upon him / ﷺ, Razi Allah hu Anhu / (RA).
- **Core message:** help, prayer (dua), hope and Allah's mercy; the turn comes through dua and Allah's help.
- **Shorts** (scripts/shorts-plan.md): opening rule (named person + surprising act + turn; one hardship line;
  turn by ~6 s; lit first frame); 50-50 title test (story questions vs "X… then Y"); word-by-word captions test;
  sourced topics adopted from Miracle of Islam; Companions never shown in any form (their stories are allowed); no remakes; always 7 days scheduled ahead.
- **Films** (scripts/channel-plan.md): hook → 2–3 open loops → each chapter opens with a question → suspense in
  between (chapter cliffhangers, pause and sound before each turn, the answer held back, never invented drama)
  → takeaway → spoken call to the next film + comment question + end screen.
- **Films' first 30 s** (Urdu Yusuf retention, 19 Nov): ~60% left in the first 30–45 s, then a flat ~35% to the
  end. Hook in one short sentence in 5 s, payoff promised by 0:15, story by 0:30 (channel-plan.md item 9).
  The content holds; the films need exposure (Shorts links, pinned comments, Related video).
- **Shorts end:** "Watch the full movie, link below 🎥" + Related video + link in the description's first line.
- **Colours:** bright by default, dark only briefly at the hardship, brighter at the turn (Shorts and films).
- **Thumbnails:** after every upload, ask the user to change it to YouTube's suggestion (with Claude's prompt and
  headline); the rich split-scene style of thumbs/yt-yusuf-ur-well-throne.png (shorts-plan item 8).
- **Growth:** no paid promotion of any kind; daily Community post; reply in the first hour; series playlists;
  channel link in the user's bios; sponsors and halal affiliate links later.
- **Goal:** $5,000 a month long-term; checkpoints mid-January (500 subscribers, a film with 1,000 free views)
  and end of Ramadan 2027 (close to monetisation). Research: scripts/miracle-of-islam-research.md.

## Reminders already scheduled (they fire into session session_019ZSVGUajUktRZV46QR3pPi)
- Fri 20 Nov 20:00 PKT, weekly review + scripts (trig_01KAksZiQFRiZw9MvWhuAx4b): numbers, Shorts test
  (incl. four birds 31%), films' reach, then Nuh film EP 4 script (28–29 Nov), 12 Shorts for 23–29 Nov, Badr outline (5–6 Dec).
- Sat 21 Nov 18:45 PKT (trig_011f8FxKtHGsCYUpgxGrgkTS) and Sun 22 Nov 18:45 PKT (trig_017D9yP7GadUrptijSAUTz1D): remind the user to remake the Ibrahim EN / UR thumbnail from YouTube Studio's suggestion (user's rule: a reminder after every film upload).
- Sat 21 Nov 19:15 PKT (trig_019fjXXLAADao9mehepfRs9y): Ibrahim translations + Test & Compare thumbnails.
The old reminders (trig_01RXw1oCMbojRK9QmRX24mZg, trig_013d8uKtT1FYWLAk6A9BVE3S, old session) were deleted 17 Nov.
A new session can recreate these for itself (send_later / create_trigger) and delete the old ones.
