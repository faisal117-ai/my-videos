# Haq Stories | حق کہانیاں: standing instructions (loaded every session)

The user works from an iPhone only. Develop on the session branch and push to **both the branch and main**
after every change.

## NEVER make the user repeat these (user, 25 Nov 2026: "always remember things I always have to remind you")
Every new rule the user gives goes into THIS file the same turn (not only into scripts/*), so every session sees it.
1. Score every Short/film with the skills' own tools (title.py, hookscore) before showing it; show the scorecard.
2. Compare the rule version with the best version and recommend as the channel owner.
3. Check length (Shorts 30–45 s, aim 30–35), honorifics, no holy figure in any image (Gemini prompts say NO PEOPLE for
   any scene tied to a holy figure), Arabic voiced with eleven_v3 + speech-to-text check, plain captions (no *chip*).
4. Shorts are BRIGHT (user 25 Nov): warm golden-hour/dawn/daylight scenes, a bright first frame with the key object,
   ~70 % of runtime bright; dark only for the one hardship beat; the turn goes from ~85 % to bright and warm.
5. FORMAT v2 for every Short (shorts-plan.md); films follow scripts/film-guidelines.md (not the Shorts rules).
6. Slots: 10:00 story → film, 16:00 comfort (≈4 comfort : 3 dua-with-answer); films Sat EN / Sun UR 17:00. No Hindustani twins.
7. Every change: commit and push to the branch AND main; log it in scripts/handoff.md.
8. Never publish or swap a video into Metricool without the user's approval of the finished video.

## Read first, every session
1. `scripts/handoff.md`: where things stand, open items, schedule, decisions.
2. `scripts/checklist.md`: run it on EVERY Short and film before showing it to the user, and report each line.
3. `scripts/shorts-plan.md`, `scripts/channel-plan.md` and `scripts/voice.md` for the format and voice rules.

## Use every stored skill that applies, without being reminded (user's rule, 19 Nov 2026)
For each video, run the skills below at their step and tell the user which ones ran and what they found.
| Step | Skill |
|---|---|
| Friday plan | `anthropic-skills:yt-viral`, then `anthropic-skills:yt-plan`; update `scripts/ypp-tracker.md` (Earn-tab screenshot from the user) |
| Film research | `anthropic-skills:deep-research` (Quran / sahih sources only) |
| Script and hook | `anthropic-skills:yt-script` (5 hooks scored with hookscore.py; show the best two) |
| Picture effects / cartoon | `stickman` (code-made effects: dust, light, shake; vertical with STICKMAN_W/H) |
| Shorts from a film | `anthropic-skills:yt-shorts` |
| The user's own recordings | `anthropic-skills:yt-edit` |
| Title and thumbnail | `anthropic-skills:yt-package` |
| Description and tags | `anthropic-skills:yt-seo` |
| Film chapters | `anthropic-skills:yt-chapters` |
| After publishing | `anthropic-skills:yt-comment`, `anthropic-skills:yt-retention` (each chart the user sends), `anthropic-skills:yt-audit` (monthly) |
| Reports | `dataviz`, `anthropic-skills:docs` |
Skills that have nothing to do with videos (keyboard shortcuts, config, code review…) are used only if a task needs them.

## Rules that never bend (details in checklist.md)
- Never show a prophet, the Prophet ﷺ, a Companion, a righteous woman, an angel or jinn in any form.
- Only what the Quran / sahih sources say. Honorific on every name, in voice and on screen.
- Shorts 30–45 s, aim 30–35 (never over 45 s; user 25 Nov, FORMAT v2 in shorts-plan.md). Hook in 5 s, a question held open, suspense, the core message (dua / mercy / gratitude), a real closing lesson,
  and the ending "Watch the full movie(s) of <named film(s)>, link(s) below" (story Shorts) or "Send this to someone who needs it" (comfort Shorts, film link in description/Related video).
- House style = shorts/24-cave (20 Nov; see shorts-plan.md). Gemini scenes for every Short and film; captions in the top band. No instrumental music (voice-only humming is fine).
- Arabic phrases in Arabic script in the TTS text, checked with speech-to-text. Callum narrates.
- After render: `tools/mix.py`. AI-content box ticked. Shorts 11:00 / 17:00, films 18:30 PKT.
- **Every Short and film is scored before it reaches the user (user's rule, 23 Nov 2026; details in checklist.md):**
  Short scorecard /100 (Hook 40 · Payoff/lesson 25 · Retention/pacing 20 · Packaging 5 · Accuracy 10), with the hook rule:
  hook text on screen from frame 0 over one strong image (works on mute), ≤ 10 words, "you" + stakes OR a surprising claim/contradiction in the first 2 s, spoken hook ≤ 3.5 s,
  never a plain description. Build every Short to FORMAT v2 (shorts-plan.md: one verse card, punch line, change every ≤ 4 s, transformation at the turn, humming from the verse, ending ≤ 3 s). Title ≥ 90 and title+cover pair ≥ 90 (yt-package title.py, no 3-word limit).
  **Films follow `scripts/film-guidelines.md` (user, 23 Nov), NOT the Shorts hook/scorecard rules:** packaging (one subject,
  ≤ 4 elements, no repeated words), first 30 s (no intro, promise, loop, hook done by 0:30), moral-epic structure,
  interrupts every 45–90 s, re-hooks, 8–15 min, bulletproof sourcing, the chain; judged Friday on CTR 4–10 %, AVD 40–60 %,
  first-30 s 70 %+, session contribution, returning viewers/subs. Run its pre-publish film check on every film.
- **Rules are guides, not cages (user, 23 Nov 2026):** when a hook (or any element) is good, don't force it into a rule.
  Always compare the rule-following version with the best version and say which one I'd choose as the channel owner, and why.
  Speak up whenever a rule doesn't fit a particular Short or film.
- Never publish without the user's approval of the finished video.
