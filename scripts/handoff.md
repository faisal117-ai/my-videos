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
- Fri–Sun Shorts: all sent and approved (see below).
- 21 Nov: Fri–Sun Shorts approved and swapped (media pinned to commit 52245e1): pharaoh 436361700,
  stars 436361740, boat 436361776, father 436361818, fire EN 436361847, dawud 436361877, valley 436361914,
  fire UR 436361968. The whole week 23–29 Nov is now final and scheduled.
- Ibrahim film links in the Sat 28 19:00 and Sun 29 16:00/19:00 Shorts point to the channel page: swap to the
  real film URLs at the Sat 28 / Sun 29 18:38 reminders.
- 21 Nov 10:12 PKT: idols Short published early at the user's request (was 11:00): https://www.youtube.com/shorts/rTCmDLREy4s
- 21 Nov: Sulaiman EN film moved 18:30 → 17:00 PKT at the user's request (post 436393722); link-swap reminder moved to 17:08, after-upload reminder to 17:15.
- 21 Nov: weekend moved at the user's request: Sat 21 film 17:00 (436393722) + throne Short 17:30 (436394476); Sun 22 sacrifice Short 10:00 (436394453), Urdu film 17:00 (436394469), Urdu throne Short 17:30 (436394492). Link-swap reminders 17:05, after-upload reminders 17:15.
- 21 Nov: reminders for already-published Shorts (Related video + pinned comment + description link in Studio, since Metricool can't edit live videos): Sat 21 17:20 (hoopoe, Qarun x2, ant), Sun 22 17:20 (Urdu ant, Urdu throne), Sat 28 18:50 (idols, fire, four birds x2, why-idols, sacrifice, stars, father), Sun 29 18:50 (Urdu fire, valley).
- 21 Nov 17:28: Sulaiman EN film LIVE https://youtu.be/rdLEJPHlQi8 (17:00 post failed: Metricool free-plan limit; user upgraded, re-published 17:28). Throne Short moved to 17:50.
  Film link swapped into 13 scheduled posts (throne, Uwais, two-answers, gold, staff, dua, dinars, gift, hope, stars, father, dawud, Ibrahim EN film). FILM_EN filled in UPLOAD.md files.
- 21 Nov 17:50: throne Short live https://www.youtube.com/shorts/To-gOslcAvM (film link in description + first comment). All 22 remaining posts PENDING, none rejected after the upgrade.
- 21 Nov: yt-audit shipped (reports/Channel audit 21 Nov.md). One fix = Shorts → film conversion: Related video + pinned film link on every Short; judge Fri 27 (Sulaiman >300 views).
- 22 Nov 12:00 PKT: Metricool per-video/traffic/country analytics still EMPTY after reconnect (only subs + daily views; subs 174 on 21 Nov). Public counts: Sulaiman EN film 12 views (18.5 h) vs throne Short 513, idols Short 643, sacrifice Short 132 (2 h). Conversion problem confirmed.
- 22 Nov 17:00: Sulaiman UR film LIVE https://youtu.be/s_Ja6UvoWRQ; link swapped into Urdu throne Short (17:30) and Ibrahim UR film first line; FILM_UR filled. Sacrifice Short live 10:00 https://youtube.com/shorts/6yWxmGqPHTA. User setting Related video on 17 published Shorts (16 done by 17:05).
- 22 Nov: user finished Related video + pinned film comment on all 17 published Shorts (Sulaiman EN x4, Musa x2+5 channel Shorts, Yusuf x5 incl. Ayyub, Urdu ant → Urdu film, fire → Musa until Ibrahim is live). Switch fire/idols/sacrifice/four-birds to the Ibrahim film on Sat 28.
- 22 Nov: end screens set by user: Sulaiman EN → Yusuf EN film; Sulaiman UR → Yusuf UR film (+Subscribe). Rule going forward: each new film's end screen → the weakest earlier film in the same language.
- 22 Nov 17:30: Urdu throne Short live https://youtube.com/shorts/NECuXKBGCFA; Related video → Urdu film + pinned comment done by user. Weekend complete.
- 22 Nov: English + Hindi subtitles made for Urdu films (tools/srt_ur_film.py; EN = source-checked English script per line, HI = Devanagari transliteration of the Urdu, cached in subtitles/hi_lines.json). Sulaiman UR: user uploads now; Ibrahim UR: upload after it goes live Sun 29.
- 22–23 Nov (user, Studio): Urdu Sulaiman film video language fixed English → Urdu; EN + HI subtitles published (Hindi title not addable on iPhone, skipped). Malay title + description added to Musa EN, Sulaiman EN, Yusuf EN.
- 23 Nov: Urdu Ibrahim film title → "Hazrat Ibrahim AS Ka Waqia: Aag Thandi Kaise Hui? | Qasas ul Anbiya EP 4 | Full Movie Urdu/Hindi" (post 437904091). Audience (28 d): India 33.5%, Pakistan 12.1%, Malaysia 5.2%; 63% male. Next: Hindustani 19:00 test Shorts Tue–Fri (Urdu voice, Hindi + English captions, no Urdu script), user approves each.
- 23 Nov: Hindustani test (Urdu voice, Hindi + English captions, no Urdu script; tools/build_short.py "hi" field + Devanagari font) approved and scheduled at 19:00 PKT:
  Tue 24 staff 437912279 · Wed 25 dua 437949733 · Thu 26 gift 437949996 · Fri 27 stars 437950341 (ends "Itwar ki shaam" → Urdu Ibrahim film).
  Judge Fri 27: avg > 300 views or Urdu film +50% → keep; else stop. Sun 29 Urdu fire Short still in the old Urdu-script style.
- 23 Nov: Sun 29 19:00 Urdu fire Short replaced by Hindustani 48-fire-hi (no spoken Arabic; post 438341074, same uuid 8528820876309056952; link swap by the Sun 29 Ibrahim UR reminder).
- 23 Nov: packaging rule applied to all 19 Shorts Tue 24–Sun 29: cover frame = 2.0 s (videoCoverMilliseconds 2000) on every post;
  11 titles re-scored to 94–98 (title.py): staff-hi "1 Chhote Se Keede Ne Jinnaat Ko Bataya…", dua "His 1st Dua Wasn't for a Kingdom…",
  dua-hi "1 Dua Pehle, Phir Badshahat…", gift "1 Queen, 1 Fortune…", gift-hi "Malika Saba Ka Tohfa 1 Jawab Mein Wapas!",
  pharaoh "Yunus 10:92: Why Was Pharaoh's Body Kept?", stars "Star, Moon, Sun: All 3 Set…", stars-hi "Sitara, Chaand, Suraj… 3 Doob Gaye!",
  boat "1 Hole in a Poor Man's Boat…", father "Maryam 19:47: How Ibrahim (AS) Answered His Father", valley "1 Mother, 1 Baby, No Water…".
  Post ids changed (uuids same); always getScheduledPosts before editing.
- 23 Nov: covers corrected — English Shorts at end of hook (gold 4.17 s, staff 3.17, calf 3.81, dua 3.68, dinars 4.98, gift 3.34, hope 2.88,
  pharaoh 3.3, stars 2.62, boat 2.98, father 3.77, fire 2.87, dawud 1.5, valley 3.97). Hindustani Shorts had a defect (highlighted *words*
  never resolved, stayed as tiny chips): fixed by plain hook text, re-rendered (commit a24d153), swapped into all 5 posts, covers 3.0 s (stars 2.0 s).
  Rule for future Hindustani Shorts: no *highlight* markup in the English "text" line (word timing comes from the Urdu voice).
- 23 Nov: Ibrahim films moved 18:30 → 17:00 (EN Sat 28 post 438640045, UR Sun 29 post 438640104); fire Shorts 19:00 → 17:30 (EN 438640165,
  Hindustani 438640238). Father + stars Shorts re-rendered with "5 PM" on screen (commit e9364cc; posts 438646341, 438646422); stars-hi text
  "sham 5 baje". Reminders: link swaps 17:05, published-Shorts checklists 17:20; four stale EP 3 thumbnail/translation reminders disabled.
  Weekend film slot is now 17:00 (16:00 = Short teaser, 17:30 = Short after the film).
- 23 Nov 21:50: gold jar rebuilt (hook 'You'd never return found gold. 2 men did. Why?', plain text, 38.7 s, scorecard 92) and swapped into Tue 24 10:00 post 439089615, title 'Who Owns 1 Jar Under Sold Land? 🏺', cover 4.8 s. Lesson: on-screen hook must match spoken words (2 vs 'two' broke the highlight) — keep hook text plain.
- 23 Nov: 29-staff rebuilt (hook "You think jinn know your future? They never knew their king had died.", 39.0 s, scorecard 89, kept over a shorter 92 version, user approved). Swapped into Metricool post 439105406 (uuid 2023529755483783648), Tue 24 16:00, title "1 Staff, 1 Insect: Who Noticed First? 🪵", cover 4950 ms. Next: staff-hi (Tue 19:00).
- 23 Nov: 44-staff-hi rebuilt (hook "جن آپ کا مستقبل جانتے ہیں؟ بادشاہ کی موت تک نہ جان سکے!", 40.4 s, hook ends 5.4 s (v3 Urdu is slow), scorecard 88, approved). Post 439122160 (uuid -886434383434920596), Tue 19:00, title "1 Keeda, 1 Asa: Jinnaat Se Pehle Kisne Jaana? 🪵", cover 5270 ms. Next: calf (Wed 10:00).
- 23 Nov: 31-calf: full hook on screen from frame 0, plain captions, matching Urdu line (voice unchanged, hook 3.96 s), 37.5 s, scorecard 92, approved. Post 439154174 (uuid 3730832418400390064), Wed 10:00, title "1 Idol, 40 Nights: Who Made It? 🐄", cover 3800 ms. 29-staff re-rendering with plain captions (chip defect on Prophet/(AS)); swap file into post 439105406 after. Next: dua (Wed 16:00).
- 23 Nov: 29-staff plain-caption file swapped in (post now 439158156, commit 1eefe17). 32-dua-kingdom: hook 'Before you ask Allah for more, ask this first.' (4.07 s; the old 'first dua' claim was not in the Quran), lesson line lengthened, 37.0 s, rendering; title to be '38:35: The Dua That Got Sulaiman (AS) the Wind 🤲'.
- 23 Nov: 32-dua-kingdom approved, post 439171664 (uuid 2132286735951416163), Wed 16:00, title '38:35: The Dua That Got Sulaiman (AS) the Wind 🤲', cover 3950 ms. Next: dua-hi (Wed 19:00).
- 23 Nov: 45-dua-hi approved, post 439179364 (uuid -3832382285876540682), Wed 19:00, cover 4150 ms. 33-dinars rebuilt (hook 'He threw a thousand dinars into the sea. And it arrived.', title '1 Loan, 0 Witnesses: Only Allah Saw It 🌊'), rendering. Next: gift (Thu 16:00).
- Lesson: 34-gift was 32.2 s (under 35) when approved earlier; check LENGTH on every rebuild.
- 23 Nov: 33-dinars approved, post 439197464 (uuid -3492304906221172532), Thu 10:00, title '1 Loan, 0 Witnesses: Only Allah Saw It 🌊', cover 4050 ms, description line fixed (two men shown close; not prophets). 34-gift (39.1 s, title '1 Royal Gift Refused: What Did Sulaiman (AS) Say? 👑') and 43-hope-mercy (36.8 s, title '39:53: ALL Sins? Even Mine? 🤲') rendering.
- 23 Nov: 34-gift approved, post 439200677 (uuid -2162989109603381851), Thu 16:00, cover 3550 ms. Rendering: hope, then gift-hi. Next: pharaoh (Fri 10:00).
- 23 Nov: 43-hope-mercy approved, post 439209364 (uuid 680823038147841556), Thu 17:00, title '39:53: ALL Sins? Even Mine? 🤲', cover 3150 ms, 35.9 s, named-films ending. Queued renders: gift-hi, pharaoh, stars, stars-hi, boat (title '18:79: Why Did Khidr (AS) Break the Ship? ⛵'), father (title '1 Harsh Threat, 1 Gentle Reply: Ibrahim (AS) 🤲'). Next: fire (Sat 17:30).
- 23 Nov: 46-gift-hi approved, post 439221682 (uuid -1935161179783148220), Thu 19:00, cover 4550 ms.
- 23 Nov: 35-pharaoh-body approved, post 439223577 (uuid 2494877274946356218), Fri 10:00, cover 3350 ms. Queue restarted after worker restart: stars, stars-hi, boat, father, fire (scratchpad q.log).
- 23 Nov: 36-stars approved, post 439235418 (uuid 1759010585170887159), Fri 16:00, title '3 Lights Vanished… Then Ibrahim (AS) Said This ✨', cover 3450 ms. 42-dawud (title '99 Ewes, 1 Ewe: What Did Dawud (AS) Realise? 🐑') and 40-valley (title '14:37: The Valley That Became Makkah 🏜️') rebuilt, queued (q2.log).
- 23 Nov: 47-stars-hi approved, post 439237146 (uuid -3937698609835587191), Fri 19:00, cover 3750 ms. 48-fire-hi rebuilt: hook 'آگ میں پھینکے جائیں… آپ کیا کہیں گے؟', dua spoken with v3 (STT YES ×2), 37.8 s, title '1 Dua Aag Se Pehle: Hazrat Ibrahim AS 🔥' (post uuid 8528820876309056952, Sun 17:30); queued (q3.log).
- 23 Nov: 48-fire-hi approved, post 439253602 (uuid 8528820876309056952), Sun 17:30, title '1 Dua Aag Se Pehle: Hazrat Ibrahim AS 🔥', cover 3650 ms. Boat (cac4173) and father (afd9b05) swaps were DENIED in the permission prompt; still old files in posts 438600754 / 438646341. Ask user.
- 23 Nov: 37-father approved, post 439255335 (uuid 4829974501000432931), Sat 16:00, title '1 Harsh Threat, 1 Gentle Reply: Ibrahim (AS) 🤲', cover 3650 ms. Boat: s4 regenerated with no people (robed figure on the 18:79 card removed, user said do as recommended); re-render queued (q5.log), then swap into post 438600754 (uuid 1418743501483429230), title '18:79: Why Did Khidr (AS) Break the Ship? ⛵', cover 2950 ms.
- 23 Nov: 38-fire approved, post 439256939 (uuid -8991910444640089845), Sat 17:30, title '1 Dua Before the Flames: Ibrahim (AS) 🔥', cover 3850 ms. Remaining: dawud, valley, boat renders → approval → swap.
- 23 Nov: user pre-approved dawud, valley, boat ('Approve them as well') before render; swap each only if my frame check passes clean, else hold and ask. Posts: dawud 438601042 (uuid -5290177016666110690) Sun 10:00 title '99 Ewes, 1 Ewe: What Did Dawud (AS) Realise? 🐑'; valley 438601203 (uuid -7427149286567821287) Sun 16:00 title '14:37: The Valley That Became Makkah 🏜️'; boat 438600754 (uuid 1418743501483429230) Sat 10:00.
- 23 Nov: 42-dawud swapped (frame check clean), post 439260052, cover 4050 ms.
- 23 Nov: 40-valley swapped (frame check clean), post 439264712, cover 4050 ms. Boat re-render (no-people s4) in progress (q5.log).
- 23 Nov: 41-boat swapped (both s1 hook image and s4 regenerated with no people; frame check clean), post 439279358, Sat 10:00, title '18:79: Why Did Khidr (AS) Break the Ship? ⛵', cover 2950 ms.
- WEEK DONE (24–29 Nov): all 18 Shorts rebuilt under the hook rule and swapped into Metricool. Lessons: (1) check LENGTH ≥ 35 on every rebuild (gift, hope, pharaoh, father, fire were under); (2) full hook on screen from frame 0, no highlight markup; (3) Gemini prompts must say ABSOLUTELY NO PEOPLE for any scene tied to a holy figure's action; (4) v3 Urdu hooks run ~4–4.5 s, keep them short.
- 24 Nov: Ibrahim EP 4 films approved and swapped (film-guidelines.md check): EN post 439752935 (Sat 28 17:00) title "1 Blazing Furnace, 0 Burns: Prophet Ibrahim (AS) | EP 4", thumbnail thumbnail-en-v4.jpg, new chapters; UR post 439753044 (Sun 29 17:00) title "1 Bhadakti Aag, 0 Zakhm: Hazrat Ibrahim AS | EP 4", thumbnail-ur-v4.jpg (mirrored), new chapters. Media pinned to 4df6a76. Changes: thumbnails EP 3→4 one-subject; ch00 accuracy (crime = broke idols, 21:56–68); re-hook end of ch02; EN dua via v3 (STT YES). UR film re-encoded at 620k (92 MB). Next films: aim 10–12 min (film-guidelines Rule 5).
- 24 Nov: user changed Studio settings: automatic dubbing OFF (accuracy risk on Quran/duas), third-party AI training OFF. Clips ON, likes shown, not made for kids, no product tagging (decided as channel owner).
- 24 Nov: yt-viral run (reports/Viral niche 24 Nov.md); user shipped the plan: 2 Shorts/day from 30 Nov, 10:00 comfort-verse + 16:00 one-moment miracle. Drafting the 7 comfort Shorts for approval.
- 24 Nov: 49-sea-comfort approved and scheduled Mon 30 10:00 (title '26:62: 1 Sentence Facing a Dead End 🌊', cover 4050 ms). 50-near-comfort (Tue 1 Dec 10:00, 2:186) rendering.
- 24 Nov: 50-near-comfort approved and scheduled Tue 1 Dec 10:00 (title '2:186: How Close Is Your Lord, Really? 🤲', cover 3850 ms). User: do NOT build Wed onward until the Friday 27 Nov review; the remaining comfort Shorts (65:3, 2:286, 13:28, 93:3, 12:87) are approved drafts only.
- 24 Nov: growth plan approved (scripts/channel-plan.md 'Growth plan'). Friday 27 Nov: check Metricool has Instagram/Facebook connected before cross-posting; start daily comment drafts once Shorts have comments; create the 'Stories of the Prophets' playlist (user).
- 24 Nov: follow-button TEST on 29-staff + 44-staff-hi only (re-rendering, swap into today's posts). Removed from all other Shorts at the user's request; decide after seeing the response.
- 24 Nov: follow-button test swapped in: 29-staff post 440010130 (16:00), 44-staff-hi post 440010203 (19:00), media e70d881. Compare their subscribers-gained / stayed-to-watch with the other Shorts this week at the Friday review, then decide.
- 24 Nov: posting times confirmed by user: Shorts at 10:00 and 16:00 PKT (Metricool best-time data: 16:00 is the top hour every day, 10:00 the morning peak; 19:00 ~35–40% lower; weekends ~half). No 15:30 test.
- 24 Nov (user asked if EN + Hindustani twins look identical): Friday decision. If the Hindustani Shorts continue, never same-day twins; space ≥ 5–7 days and give them different scenes + own hook image (avoid self-competition and 'inauthentic/repetitive content' risk at YPP review). Films EN/UR on Sat/Sun are fine.
- 24 Nov (low comments): user keeps first comments as they are (question + film link). User pins the first comment manually after each Short goes live (API can't pin) and checks Studio → Comments → 'Held for review' + Settings → Community defaults. I draft replies to every comment (yt-comment).
- 24 Nov: user keeps all scheduled titles as they are (title.py-scored style). The two live Shorts (gold jar XTofvvKdjgQ, staff C74JJWhj4uE) show different titles on YouTube; left alone (24 h rule).
- 24 Nov 18:35: owner decision (user delegated): keep 44-staff-hi at 19:00 tonight (completes the Hindustani test; no real effect on the English Short's reach).
- 24 Nov: first audience request (comment on the staff Short): viewer asked for 'the ones who struggle and ease by Allah' → supports the comfort-Short plan; replied promising Mon 30 sea Short.
- 24 Nov: comfort-verse Shorts get Related video = 'Ease With Every Hardship' https://youtube.com/shorts/wSX3fbkqLwo (to re-surface it); story Shorts keep the film. Daily 20:47 reminder (trig_01XLLkNEZn59tEPvcyXsdzom) updated.
- 25 Nov ~01:30 PKT: user deleted the 4 Hindustani Short posts (Hindustani test ended). Plan for Wed 25 → Tue 1 (user): story Shorts 10:00 (→ film), comfort Shorts 16:00:
  Wed calf | dua 38:35 · Thu gift | 39:53 · Fri Pharaoh | stars · Sat father | boat + film EN 17:00 + fire 17:30 ·
  Sun Dawud | valley + film UR 17:00 · Mon dinars | sea 26:62 · Tue (Friday review) | near 2:186.
  All rebuilt with template v2 (hook ≤10 words/≤3.5 s, 1 verse card ~6 s, punch line, transformation at the turn,
  change every ≤4 s, humming from the verse, sound event 8–18 s, ending ≤3 s, 30–35 s); each sent for approval, then
  swapped (with its new time) into Metricool. Until swapped, the current versions stay scheduled as the fallback.
- 25 Nov 01:38 PKT: time moves done in Metricool (existing videos): dinars → Mon 30 10:00 (post 440871181), gift → Thu 10:00 (440871301), 39:53 → Thu 16:00 (440871411), father → Sat 10:00 (440871527), boat → Sat 16:00 (440871609), sea → Mon 30 16:00 (440871745), near → Tue 1 16:00 (440871832). Calf Wed 10, dua Wed 16, Pharaoh Fri 10, stars Fri 16, Dawud Sun 10, valley Sun 16 were already right.
- 25 Nov: dua (Wed 16:00) title changed to '38:35: 1 Dua That Began With Forgiveness 🤲' (post 440885287); v2 video swap pending approval.
- 25 Nov ~02:00 PKT: user gave ADVANCE permission to replace all scheduled Shorts with their FORMAT v2 rebuilds overnight (calf, dua, gift, 39:53, Pharaoh, stars, father, boat, fire, Dawud, valley, dinars, sea, near). Swap only if the frame check + scorecard pass; otherwise keep the current version and report.
- 25 Nov: neutral grade (option A) applied; all 14 v2 Shorts rebuilt with build_short and rendering in two queues (scratchpad v2/A.log, B.log). Swap each after frame check + scorecard under the overnight advance permission.
- 25 Nov: user chose A+B: 28 hook + lesson pictures relit to neutral daylight with Gemini image edit (originals in scratchpad relight/orig); fire hook keeps flames in daylight; near hook and 39:53 lesson rooms get morning sun. Re-rendering all 14.
- 25 Nov: daylight-picture rule saved (CLAUDE.md #4, shorts-plan Brightness, gen_scenes.py DAY prompt by default; dark_keys for the hardship beat).
- 25 Nov: picture rule approved (owner version): daylight default, one dark hardship picture, sunrise only at the turn (gen_scenes dark_keys/dawn_keys). From the next Short on; this week's 14 keep their daylight lessons.
- 25 Nov: user: apply the picture rule to this week too. Verse-card pictures relit to daylight, turn pictures (beat 3) relit to sunrise; story hardship picture (beat 1) kept. Boat/Dawud turn pictures split to s5t/s4t. Contact sheet reports/week-pictures-sunrise.jpg. Re-rendering 14.
- 25 Nov 02:20 PKT: v2 calf swapped (post 440918395, cover 4100, commit 27a1f49) and v2 dua swapped (post 440918474, cover 4150). Frame check clean (daylight, sunrise turn, no new figures). Hook ends 4.08/4.10 s (guide 3.5; voice unchanged).
- 25 Nov 02:31 PKT: template tint removed (warm overlay 0, no extra saturation; renders now match source colours). Calf re-swapped (post 440930442) and dua (440930575), media commit 50a805d. Remaining 12 rendering.
- 25 Nov 10:32 PKT: v2 swapped (media 06c10c6/93b6352): gift 441213319, 39:53 441280694, pharaoh 441280866, stars 441281013, father 441281120, boat 441281248. Remaining: fire, dawud, valley, dinars, sea, near.
- 25 Nov 10:37 PKT: ALL 14 v2 Shorts swapped. Fire 441283169, Dawud 441283283, valley 441283379, dinars 441283474, sea 441283571, near 441283647 (media 93b6352). Frames: reports/week-v2-frames.jpg.
- 25 Nov: gift lesson picture redrawn (g5: sunlit garden spring, gold chest set aside in shade, no people); re-rendered 26.5 s; awaiting user approval to swap into post 441213319 (Thu 10:00).
- 25 Nov 10:51 PKT: user approved; new gift swapped, post 441291442 (Thu 26 10:00), media 6323fb3.
- 25 Nov: scorecard run on all 14 v2 Shorts (reports/Scorecard v2 25 Nov.md): 83–98; weakest Dawud 83, valley 85, dinars 87, dua 89.
- 25 Nov: Dawud/valley hook fix BLOCKED: ElevenLabs quota exhausted (49 credits left of 121,124; need ~130 per Short). Dawud re-voice tries gave 4.7/5.5 s hooks (worse). Both restored to the scheduled versions (unchanged in Metricool). New hooks ready: Dawud 'One case of 99 ewes… and a king fell down bowing.' / valley 'No water. No one. Would you trust Allah here?' — redo when credits refill. API key lacks user_read, so the reset date can't be read.
- 25 Nov: credits topped up ($20). Dawud re-voiced: hook 'A king fell down bowing… over one ewe.' (3.54 s, 26.7 s); valley: 'No water. No one. Would you trust Allah here?' (4.17 s, 25.7 s). new_short.py now keeps existing crop stills (a re-voice had reverted valley's relit pictures). Awaiting approval to swap (Dawud 441283283 Sun 10:00, valley 441283379 Sun 16:00).
- 25 Nov 14:43 PKT: user approved; Dawud swapped (post 441470795, title '99 to 1: What Did Dawud (AS) Realise? 🐑', cover 3550) and valley (post 441471022, cover 4200), media 763d13f.
- 25 Nov: dinars re-voiced: hook 'A thousand dinars into the sea… and they arrived.' (9 words, 3.74 s, was 11 words/4.19 s), 29.2 s, score ≈91 (was 87). Awaiting approval to swap into post 441283474 (Mon 30 10:00).
- 25 Nov 15:45 PKT: user approved; dinars swapped, post 441543471 (Mon 30 10:00), cover 3750, media c379e7b.
- 25 Nov: user: the comfort ending 'Send this to someone who needs it' drives WhatsApp shares (analytics). Saved in CLAUDE.md #10; Friday review adds shares per Short.
- 25 Nov: dua Short (38:35) after ~3 h: above the typical-views curve, 94% Shorts feed, WhatsApp = half of 1% external; stayed-to-watch 27% (target 50%). Leak = first 1–2 s; check avg % viewed + shares. Compare with calf at the Friday review.
- 25 Nov: YouTube analysis of dua Short (6 h): 877 views (typical 210–400), avg viewed 60% (typical 47.5–52.4), stayed 28.7% (typical 28.8–34.5). Leak = first frame: thin serif hook on a light beige background = low contrast at feed size; 24–28 s lesson drags. Proposed template fixes (await approval): bolder/high-contrast hook text with a soft dark band, closer first shot; tighter lesson (shorter '…' pause, end right after the lesson).
- 25 Nov: user approved both template fixes: (1) hook text thicker + larger with a dark band, first picture starts closer (build_short HOOK_CSS, #ph0 scale 1.14); (2) tighter lesson: tts_eleven trims model silence around EN/Arabic parts, new_short caps the pause before the last line at 0.3 s (v2). Before/after: reports/hook-v2-before-after.jpg. From next week's Shorts; this week's stay.
- 26 Nov 13:35 PKT: covers moved to 1000 ms on all 11 scheduled Shorts (39:53 442799700, pharaoh 442799848, stars 442799972, father 442800097, boat 442800172, fire 442800337, Dawud 442800414, valley 442800500, dinars 442800620, sea 442800685, near 442800759). Calf/dua/gift already live: user changes the cover in Studio. Rule saved CLAUDE.md #11.
- 26 Nov 13:55 PKT: user approved; 39:53 with new hook style swapped (post 442818356, 16:00, cover 1000, media 445228c). Other 10 re-rendering with the new hook (scratchpad v2 A.log/B.log); each goes to the user for approval before swap.
- 26 Nov 13:56 PKT: batch 1 new-hook swaps approved: pharaoh 442819606, stars 442819714, father 442819820, boat 442819912 (media 80a1e7e, cover 1000).
- 26 Nov 14:10 PKT: batch 2 new-hook swaps approved: fire 442832212, Dawud 442832353, valley 442832399, dinars 442832811, sea 442832993, near 442833082 (media ec71eb0, cover 1000). All 11 remaining Shorts now carry the new hook style. Compare stayed-to-watch vs dua 28.9% / gift 29.3% at the Friday review.
- 26 Nov: Tue 1 Dec 10:00 slot stays empty until the Friday 27 Nov review (user). Build it Sat 28 from the review's findings (story vs comfort, hook type), send for approval.
- 26 Nov: Earn tab (data as of 21 Nov): 187 subs, 8 watch hours (12 mo), 8.5k Shorts views (90 d; target 10M). Logged in ypp-tracker.md.
- 26 Nov: 39:53 (new hook) after ~4 h: ~300+ views, 31 likes (~10%), stayed 24.6%, +7 subscribers (user). Comfort/'you' Shorts convert to subs; add subs-per-Short to the Friday review.
- 26 Nov (later): 39:53 = 858 views, 70 likes (8%), +7 subs, avg viewed 71% (best yet), stayed 28% (same as old-style dua 28.9%/gift 29.3% → bolder hook text alone did NOT lift stayed-to-watch). Next: test motion-first hook (A/B) next week; bring cost to Friday review.
- 27 Nov: user approved the motion-first hook A/B test for next week + ~$10 Atlas Cloud top-up (user tops up; balance $0, API reachable, returns 402 until then). tools/animate_clip.py added (beat still → 5 s clip, spec points to the mp4; build_short plays it muted). Plan in shorts-plan.md.
- 27 Nov: user: remove the animated-hook test. tools/animate_clip.py and the plan removed; no Atlas top-up needed. Next week's Shorts stay stills + camera motion.
- 27 Nov Friday review data: Earn (22 Nov) 195 subs / 11 h / 8.7k Shorts views. 28 d Shorts: 26.4k views, 10.1k engaged, 2.1k likes, +119 subs, stayed 37 % (this week's v2 Shorts only 25–29 % → below channel average). Films 28 d 7.8k views, nearly all ads spike; organic film views tiny (Sulaiman UR 86, Yusuf UR 65, Yusuf EN 56) → Shorts→film conversion failing. Asked user for: Ease + 100-years stayed %, calf stats, film traffic sources.
- 27 Nov Friday review written: reports/Friday review 27 Nov.md (Ease 46.9 % stayed vs v2 bright ~28–30 %; films ads-only; Sulaiman EN CTR 1.4 %). Proposals await user decision.
- 27 Nov: Ease-style A test built (calm_hook: dark first frame brightening by hook end, small italic hook, ≤6-word question hook, re-voiced 2.8–3.3 s): father, fire (Arabic STT YES ×2), valley, sea. Controls B: stars, boat, Dawud, dinars, near. Frames reports/calm-hook-test.jpg. Awaiting approval to swap.
- 27 Nov 14:47 PKT: user approved; calm-hook A test swapped: father 444134705 (Sat 10), fire 444135364 (Sat 17:30), valley 444135444 (Sun 16), sea 444135530 (Mon 16); media 5e555d3, cover 2500 ms (frame 0 is dark by design). Controls B: stars, boat, Dawud, dinars, near. Compare stayed-to-watch next Friday. Next: Sulaiman EN thumbnail/title refresh (CTR 1.4 %); Tue 1 Dec 10:00 new Short (13:28, calm hook, hook → verse fast).
