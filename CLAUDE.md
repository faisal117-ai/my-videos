# Haq Stories | حق کہانیاں: standing instructions (loaded every session)

The user works from an iPhone only. Develop on the session branch and push to **both the branch and main**
after every change.

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
- Shorts 35–45 s (never over 45 s). Hook in 5 s, a question held open, suspense, the core message (dua / mercy / gratitude), a real closing lesson,
  and the ending "Watch the full movie(s) of <named film(s)>, link(s) below".
- House style = shorts/24-cave (20 Nov; see shorts-plan.md). Gemini scenes for every Short and film; captions in the top band. No instrumental music (voice-only humming is fine).
- Arabic phrases in Arabic script in the TTS text, checked with speech-to-text. Callum narrates.
- After render: `tools/mix.py`. AI-content box ticked. Shorts 11:00 / 17:00, films 18:30 PKT.
- Never publish without the user's approval of the finished video.
