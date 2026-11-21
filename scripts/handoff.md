# Handoff (updated 19 Nov 2026, night): read this first in a new session

Read next: root `CLAUDE.md` (standing rules + which skill runs at each step), `scripts/checklist.md` (run on every
video), `scripts/channel-plan.md`, `scripts/shorts-plan.md`, `scripts/series-plan.md`, `scripts/voice.md`.

## NOW (19 Nov night): the current state in one place
- **20 Nov: the cave Short's look is the HOUSE STYLE for every Short and film** (user). Details in shorts-plan.md
  "House style approved 20 Nov 2026" (also in channel-plan.md). Cave Short scheduled Fri 20 Nov 13:00 PKT (post 434738300, user's slot); after it goes live: Related video → Musa film, pin the first comment.
- **20 Nov (session_019ZSVGSKwArszmxSEYesnzJ, "my-videos" env): cave talking clips priced, waiting on the user.**
  Atlas works but the balance is **$0.00**: nothing can be generated until the user tops up atlascloud.ai.
  Atlas itself sells `sync/lipsync-v3` ($0.22/s), so the separate Sync MCP / mcp.sync.so secret is NOT needed.
  Men's lines = beats 3, 4, 6, 8, 9 (23.7 s of speech; clips ~26 s with padding). Options (image + our
  Declan/Peter/Adam audio → talking clip): Kling v2.6 Std Avatar $0.048/s ≈ $1.25 (recommended);
  OmniHuman 1.5 $0.12/s ≈ $3.10; Kling video + Sync lipsync-v3 ≈ $7+. The old assets/gen/talk_s*.mp4 are the
  rejected code-made mouths: replace them, don't reuse.
- **User's decision (20 Nov): no talking clips for now.** SadTalker (free, CPU) was too slow; Atlas has $0. Shorts
  and films use Gemini still scenes + code effects, plus the skills and rules as usual. Cave Short rendered
  (shorts/24-cave/24-cave.mp4), waiting for approval; then schedule it (11:00 or 17:00 PKT slot after Sun 22).
- **20 Nov 00:xx PKT, START NEW SESSIONS ON THE "my-videos" ENVIRONMENT.** Session session_019ZSVGScBUUkyUorGhVgReh
  opened on "Default", which has no keys: api.atlascloud.ai is blocked there (proxy 403) and the Gemini/ElevenLabs
  keys are missing. A running session can't be moved onto "my-videos", so the cave Short wasn't touched.
  "my-videos" holds secrets for Atlas, ElevenLabs and Gemini but **none for Sync (mcp.sync.so)** yet.
- **Process rules the user insists on** (they were upset when rules were missed): run checklist.md on every video
  and report each line; use every applicable skill without being reminded (CLAUDE.md table); only what the source
  says; ask before publishing; push to the branch and main after every change; the user is on an iPhone only.
- **Schedule (Metricool, brand 8081200, Asia/Karachi):** Shorts 11:00 and 17:00 PKT, films 18:30. Shorts are
  scheduled through Sun 22 Nov (hoopoe, Nuh, idols, sacrifice; Gemini scenes, mixed). Keep 7 days ahead (Friday review).
- **Films:** Sulaiman EP 3 EN Sat 21 18:30 (post 434496552), UR Sun 22 18:30 (post 434526077), thumbnails set;
  reminders trig_011MzyGvnFdPT5WKHemEMjVJ / trig_01N1XxjsgYTHa8iGgi7qPFCd fire into session_019ZSVGUB7fBBbYPfjP19HVe.
  **Ibrahim = EP 4, Sat 28 EN / Sun 29 UR 18:30** (posts 434202929 / 434203028 still hold OLD renders and "EP 3"
  text): rebuild both with Gemini scenes before then and swap them in. Nuh film = EP 5 (5–6 Dec).
- **Published:** 22-gardens Short (19 Nov 23:57, post 434622811). Still to tell the user: set its Related video to
  the Musa film and pin the comment (Musa https://youtu.be/I9d00aHMQrQ · Yusuf https://youtu.be/2l7eG427nRY).
  After Sulaiman is live (Sat), the hoopoe Short's Related video can point to it.
- **Gemini credit:** $5 prepaid, about $4.5 used (≈90 images + 2 Omni clips). Ask the user to top up before the
  Ibrahim rebuild (Wednesday). Image ~$0.04; Omni video ~$0.07/s at 720p.
- **Voice:** Callum narrates everything (user's choice). After 31 Dec 2026 (default voices retire) switch to the
  library voice "Callum 2.0 - Husky Trickster (Default)", ID 5OSluWlAJntR1KG2pWaB (already in My Voices). The
  user's own clone "Faisal Narrator (Haq Stories)" lxAuND1y6e93CWiS40Uz (eleven_v3 only) is saved but not used.
  Character voices for ordinary men: Declan nmmIJ8k3ukOa1CSFlor3, Peter ZthjuvLPty3kTMaNKVKb, Adam IRHApOXLvnW57QJPQH2P.
- **Cave Short (Bukhari 2272):** shorts/23-cave = stickman cartoon test (not for upload). shorts/24-cave = the
  Gemini version: hook A (yt-script 62/100), title "How Did 3 Men Escape a Sealed Cave? 🪨" (yt-package),
  UPLOAD.md with yt-seo description; 11 scenes, code effects (shakes, light blooms, dust), voices, soundscape.
  Not rendered yet (user stopped it). Code-made mouth movement was rejected by the user. Next: real talking shots
  with Atlas Cloud video + Sync lip-sync (both paid: price it and ask first), then render → mix.py → checklist →
  send the raw.githubusercontent link (the user can't open the in-chat file on the iPhone).
- **Stickman skill:** saved in .claude/skills/stickman, patched for vertical; run with
  `STICKMAN_W=1080 STICKMAN_H=1920 STICKMAN_CHROME=/opt/pw-browsers/chromium`.

## Where things stood on 17 Nov (older detail)
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

## MCP servers added 19 Nov (late), in .mcp.json, load at session start
- **atlascloud** (npx atlascloud-mcp): paid image/video models (Kling, Seedance, Veo; talking avatars). API key saved as a
  network secret for api.atlascloud.ai (Bearer); env ATLASCLOUD_API_KEY=proxy-injected. Tested: 200.
- **sync** (https://mcp.sync.so/mcp): lip-sync. NOT working yet: host blocked and no key. The user is to add a network
  secret in the environment settings (host mcp.sync.so, header x-api-key, empty prefix).
- Next: cave Short (shorts/24-cave) with real talking shots (Atlas video + Sync lips to our Declan/Peter/Adam voices).
  Check prices first and tell the user the cost before generating. The render of 24-cave was stopped by the user;
  spec.json has still pictures only.

## Decision of 19 Nov (late): skills
- **Use every stored skill that applies, without being reminded** (user, 19 Nov). The step-by-step list is in
  CLAUDE.md (root, loaded every session) and checklist.md. Cave Short: yt-script ran (old hook 37/100 → hook A
  62/100, user chose A; "No one knew they were there" removed, not in Bukhari 2272). Next for it: yt-package, yt-seo.
- shorts/23-cave = stickman cartoon test (not for upload); shorts/24-cave = the Gemini version being built
  (11 scenes made, ~$0.44; hook re-voiced in 24-cave/hook/).
- **Code-made mouth movement rejected** (user, 19 Nov: "not good for the channel"). tools/talk_clip.py stays in the
  repo but is not used. Talking characters only with real AI video (Gemini Omni, needs credit) or not at all;
  otherwise still Gemini pictures + camera moves, shakes, light blooms, dust.

## Decision of 19 Nov
- **19 Nov 23:37 PKT:** test Short 22-gardens (Al-Kahf 18:32–42, first real animation: two Gemini Omni 1.2 Flash
  lip-synced clips of ordinary people; question + held-back answer + pauses + humming + lesson) published now at the
  user's request, title "Why Did His Garden Disappear Overnight? 🍇", AI box ticked, links to Musa and Yusuf films.
  Omni request format: POST v1beta/interactions, model gemini-omni-1.2-flash, input [image(b64,mime), text],
  generation_config.video_config.task "image_to_video", response_modalities "video", background true; poll GET
  interactions/<id>; no aspect setting (it follows the image). Every Short/film now goes through scripts/checklist.md.
- **19 Nov evening:** Sulaiman EP 3 EN rendered (10:44), mixed, re-encoded CRF 27 (80 MB, GitHub limit 100 MB;
  raw renders are git-ignored), scheduled in Metricool Sat 21 18:30 with thumbnail-en.jpg and isAiGeneratedContent
  true; reminder trig_011MzyGvnFdPT5WKHemEMjVJ (Sat 18:45, this session). Urdu film (11:41, 85 MB) scheduled Sun 22 18:30 with
  thumbnail-ur.jpg, title shortened to 96 chars (YouTube max 100); reminder trig_01N1XxjsgYTHa8iGgi7qPFCd (Sun 18:45). **Process lessons:** Shorts need `tools/mix.py` after render (README); films need
  `soundscape_long.py` → build → render → `mix.py` → CRF 27 re-encode. Gemini spend ~80 images (~$3.20).
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

### 19/20 Nov late: Sulaiman EP 3 re-made (EN + UR)
- Both films re-rendered with the fixed script, house-style shakes/light blooms, exact verse cards; mixed (-14.5 / -14.3 LUFS), CRF 27: EN 11:03 80 MB, UR 11:43 83 MB. Commit 067251a.
- Waiting for the user's approval. Then swap media, titles, descriptions, chapters and thumbnails in Metricool posts 434496552 (EN, Sat 21 Nov 18:30) and 434526077 (UR, Sun 22 Nov 18:30).
- 20 Nov: user APPROVED. Metricool updated with new mp4s, titles, descriptions + chapters, thumbnails, tags, AI box, pinned-comment text as first comment: EN post now 435454310 (Sat 21 Nov 18:30), UR post now 435454706 (Sun 22 Nov 18:30). Hindi title/description for Sulaiman EP 3 added to scripts/translations/urdu-films-hindi.md (Ibrahim moved to EP 4).
- After they go live: set Related video (EN → Musa film, UR → Urdu Yusuf), add the Hindi translation for the Urdu film, playlist + end screen per UPLOAD.md.

### 20 Nov afternoon: week 23–29 Nov plan APPROVED (scripts/week-plan-23-29nov.md), Ibrahim EP 4 = yes
- User topped up Gemini by $20. Shorts slots move to 10:00 (channel Short) and 16:00 (film Short) from Mon 23.
- 25-throne (EN) approved + scheduled Sat 21 19:00 (post 435490006). Reminder at Sat 18:38 swaps in the film link.
- 26-throne-ur approved + scheduled Sun 22 19:00 (post 435493704). Reminder Sun 18:38 swaps in the Urdu film link.
- Built and rendering: 26-throne-ur (Sun 19:00), 27-uwais (Mon 10:00; Muslim 2542 only, NOT the "stayed home
  instead of meeting the Prophet" story, which is not in that hadith), 28-two-answers (Mon 16:00).
- New tool: tools/short_pauses.py (pauses before turns in a Short).
- Next: Ibrahim film rebuild with Gemini photos (it still uses code-drawn SVG scenes, 15 chapters), then Tue–Sun Shorts.
- 27-uwais (Mon 23 10:00, post 435510123) and 28-two-answers (Mon 23 16:00, post 435510428) approved + scheduled.
  Sat 18:38 reminder (trig_01FzgjE5ti8FsEjnhGMQS6Nh) swaps the EN film link into the throne, Uwais and two-answers posts.
- Ibrahim: 44 Gemini scenes done (long/03-ibrahim/scenes.json, assets/gen). Source check: reports/Ibrahim film source
  check.md (20 lines not in source, 23 wording fixes). Next: rewrite those lines, re-voice (EN splice, UR whole chapters),
  switch spec chapters to "photos" + shakes/glows, EP 4 everywhere, render both, swap into posts 434202929 / 434203028.
- 30-gold-jar approved + scheduled Tue 24 10:00 (post 435546768); Sat reminder also swaps its film link.
- 31-calf approved + scheduled Wed 25 10:00 (post 435558164; Musa film link already real).
- 20 Nov evening: SHORTS LENGTH RULE CORRECTED to 35–45 s (user; channel-plan data: ≤45 s = 48% pushed). All nine week Shorts
  re-cut to 40–45 s (tools/new_short.py + shorts/defs/*.json). Approved re-cuts swapped into Metricool (media only):
  throne Sat 19:00 (now post 435639476), Uwais Mon 10:00 (436042529, final 40 s cut, approved 20 Nov), two answers Mon 16:00 (435639640),
  jar of gold Tue 10:00 (435639723), calf Wed 10:00 (435639828). Still to approve: Urdu throne (Sun 19:00),
  staff, dua, dinars. Renders: a second/third HYPERFRAMES_CACHE_DIR lets Shorts render beside a film.
- Ibrahim EN film rendered (15:35) but 120 MB: re-encoding at ~700 kbps to get under 100 MB. UR film rendering.
- The garden Short was posted twice (19 Nov 23:37 and 23:57): user to set the copy with fewer views to Private.
- 20 Nov night: approved + scheduled: Urdu throne re-cut (Sun 22 19:00, post 435843153), staff (Tue 24 16:00, 435843304),
  dua (Wed 25 16:00, 435843383), dinars (Thu 26 10:00, 435843481). Sat 18:38 reminder swaps the EN film link into every
  Short whose description still has the channel URL; Sun 18:38 reminder does the Urdu throne.
- Ibrahim EN + UR films re-rendering (8 scenes regenerated: no figure that could be read as a prophet/Hajar/Ismail/angel).
  Reminder trig_01VjayWR19wBDhrVAghWAyAW checks them at 01:30 PKT. Still to make for 26–29 Nov: Thu 16:00, Fri, Sat, Sun Shorts.
- 20 Nov late: ALL Shorts through Sun 29 Nov approved + scheduled (35–45 s each):
  Thu 26 16:00 gift (435976283), 17:00 hope 39:53 (435976373); Fri 27 10:00 Pharaoh body (435976467), 16:00 stars (435976549);
  Sat 28 10:00 Khidr boat (435976658), 16:00 father (435976752), 19:00 fire EN (435976903);
  Sun 29 10:00 Dawud (435977052), 16:00 valley (435977159), 19:00 fire UR (435977260).
  Film links: Sat 21 18:38 reminder swaps the Sulaiman link (all Shorts with the channel URL next to "Prophet Sulaiman");
  Sat 28 18:38 (trig_01PmuHD38cHTpXrHsNKZWvX1) Ibrahim EN link into fire EN + valley; Sun 29 18:38 (trig_01Mgd56Lyqi7Va5LYhnGxTn5) Urdu link into fire UR.
- New weekly format: a hope-verse Short (user approved 20 Nov). Next ones: 2:286, 40:60, 13:28.
- yt-retention (Musa EN film): 45% gone by 0:30 because of the spoken title section; rule now: no spoken titles (channel-plan.md).
- Ibrahim EN + UR films rendering (opening cut to 0:26, 19 scenes regenerated people-free). Not yet in Metricool: send links,
  get approval, then swap into posts 434202929 (Sat 28 18:30) / 434203028 (Sun 29 18:30) with EP 4 titles + seo text.
- **Friday 27 Nov review (user, 20 Nov):** yt-viral → yt-plan as usual, PLUS: update scripts/ypp-tracker.md (ask the user for the
  Studio Earn-tab screenshot: subscribers, public watch hours, valid Shorts views; and the Ibrahim film's average view); check the 39:53 hope Short (Thu 26 17:00):
  shares and likes per 1,000 views vs "Ease With Every Hardship"; then make next week's two hope Shorts
  (scripts/hope-shorts-plan.md: Mon 30 26:61–62 Musa → Musa film; Thu 3 Dec 2:286 → Ibrahim film), adjusted to what the data says.
  Also compare: film Shorts (16:00) vs channel Shorts (10:00); the Dawud and Khidr test Shorts (pick the 5–6 Dec film).

## 21 Nov: approved and swapped into Metricool (media pinned to commit a6ea3ea)
- Tue–Thu Shorts: gold jar 436355895, staff 436355944, calf 436355969, dua 436356009, dinars 436356038,
  gift 436356071, hope 39:53 436356097.
- Ibrahim EP 4 films with new thumbnails, titles, chapters and AI box: EN 436356359 (Sat 28 18:30),
  UR 436356457 (Sun 29 18:30). Link swaps after publishing: Sat 28 / Sun 29 18:38 reminders.
- Still to send: Fri–Sun Shorts (pharaoh, stars, boat, father, fire done; dawud, valley, fire-ur rendering).
