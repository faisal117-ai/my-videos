# Pre-flight checklist: run on EVERY Short and film BEFORE showing it to the user (user's rule, 19 Nov 2026)

Report the result (each line ✅ or ❌ + fix) to the user together with the video. Sources: shorts-plan.md, channel-plan.md, voice.md.

## Story (script)
- [ ] **Length: Shorts 35–45 s, never over 45 s** (about 90–100 spoken words; our data: 45 s or shorter = 48% pushed, longer = 7–8%).
- [ ] **Hook in one short sentence, first 5 s**: named person (or clear "he"/"a man") + surprising act + promise of the turn; lit first frame.
- [ ] **A question / open loop** the viewer must stay for ("five words he forgot…", "what does a man say…"), answered only near the end.
- [ ] **Suspense**: the answer is held back; a pause (0.6–1.2 s) and a sound (riser / pulse) before every turn; cliffhanger lines.
- [ ] **Core message**: help, dua, hope, Allah's mercy or gratitude; the turn comes through dua / Allah.
- [ ] **A real closing lesson** (one clear action for today, or a dua to save), not a throwaway line.
- [ ] **Honorific on every name, EVERY mention** in voice and on screen: alayhis salaam / (AS), alayhimas salaam (two), peace be upon him / ﷺ, Razi Allah hu Anhu / (RA), rahimahullah / (RH) for a Tabi'i (e.g. Uwais). Also in "Prophet X's full movie" endings. Not inside an exact verse/hadith quote or someone's own words. (User caught misses 20 Nov.)
- [ ] **Arabic phrases** (Masha'Allah, la quwwata illa billah, duas, verses): written in Arabic script in the TTS text, transcribed back with speech-to-text, and offered to the user to hear before publishing (user, 19 Nov: Callum mispronounced "la quwwata").
- [ ] **Only what the Quran / sahih sources say**: no numbers, places or details not in the source; every verse from the package (Sahih International / Maududi) with its reference.
- [ ] **Ending**: "Watch the full movie(s) of <named film(s)>, link(s) below" + a comment question (pinned).

## Picture
- [ ] Never a prophet, the Prophet ﷺ, a Companion, a righteous woman, an angel or jinn in any form; check every image and every animated clip frame.
- [ ] Ordinary people may be shown and may speak (animated clips): only lines from the source.
- [ ] **Ordinary people (crowds, travellers, townsfolk, workers) stay in** (user, 20 Nov). Remove a figure only when it stands in
      for a holy person: a lone or small group of figures at the exact moment the narration speaks of the prophet/righteous person
      (e.g. a man kneeling as "Dawud fell down bowing", figures carrying stones as "father and son built the House").
- [ ] Captions in the top band, picture clear below; reference text ≥ 28 px.
- [ ] Bright by default; dark only briefly at the hardship.

## Sound
- [ ] **No instrumental music**; animated clips' own audio checked (voice + ambience only).
- [ ] Story soundscape + **voice-only humming swelling at the turns and the lesson**, risers, booms, pauses (the 19 Nov movie-style sound).
- [ ] After render: `tools/mix.py` (≈ -14.5 LUFS); films re-encoded CRF 27 (< 100 MB).

## Publishing
- [ ] Title: story question or "X… then Y" (50-50 test), ≤ 100 characters.
- [ ] Description first line "🎥 Watch the full movie: … 👉 link"; **Related video → the film set in Studio on EVERY Short after it goes live** (audit 21 Nov: the one fix); pinned film-link comment; AI-content box ticked.
- [ ] Evening Shorts 17:00, morning 11:00, films 18:30 PKT; 7 days scheduled ahead.

## Skills: use every stored skill that applies (user's rule, 19 Nov 2026)
Report which skills ran with each video. Skills live in the session list (anthropic-skills:yt-*, stickman, deep-research, dataviz, docs).
- [ ] **Plan (Friday review):** `yt-viral` (what beats its channel in our niche this week) → `yt-plan` (next week's Shorts + film).
- [ ] **Research (films):** `deep-research` for the Quran / sahih sources of each story before the script.
- [ ] **Script:** `yt-script`: 5 hooks scored with its hookscore.py, the best two shown to the user, ON SCREEN notes per beat.
- [ ] **Picture:** Gemini scenes; `stickman` engine for code-made effects (dust, light, shake) or cartoon tests.
- [ ] **Shorts from films:** `yt-shorts` picks the self-contained moments of each film.
- [ ] **Edit (user's own recordings):** `yt-edit`.
- [ ] **Title + thumbnail:** `yt-package` lints the pair (truncation, vagueness, duplicates).
- [ ] **Description + tags:** `yt-seo`.
- [ ] **Films:** `yt-chapters` validates the chapter list.
- [ ] **After publishing:** `yt-comment` drafts replies; `yt-retention` on each retention chart the user sends; `yt-audit` once a month; `dataviz` / `docs` for any report.
