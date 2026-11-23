# Haq Stories | حق کہانیاں: voice profile
(inferred from our own narration scripts: long/01-yusuf, 02-musa, 03-ibrahim and Shorts 08–21)

- Faceless, animated. A calm, reverent storyteller (one male narrator voice), never a host talking to camera.
- Tells the story in plain past tense, short sentences, present-tense only for the lesson at the end.
- Speaks to Muslim families, English-speaking first, Urdu second; assumes faith, explains context.
- **Honorifics, every time a name is said or written (the user's rule, 17 Nov):**
  - every prophet: narration "Prophet Yusuf, alayhis salaam" / Urdu "حضرت یوسف علیہ السلام"; on screen and titles "(AS)";
  - the Holy Prophet: narration "the Prophet Muhammad, peace be upon him" / Urdu "صلی اللہ علیہ وسلم"; on screen "ﷺ";
  - Companions: narration "Umar, Razi Allah hu Anhu" (a woman: "Razi Allah hu Anha"; several: "Razi Allah hu Anhum") /
    Urdu "رضی اللہ عنہ / عنہا / عنہم"; on screen and titles "(RA)".
  Check every script for a bare name before it goes to ElevenLabs.
- Always "Allah"; Quran verses quoted only from Sahih International / Maududi, with references.
- Never: hype words ("INSANE", "SHOCKING", "you won't believe"), invented details, numbers not in the
  Quran or sahih hadith, drawing any prophet, righteous woman, Companion or angel.
- Hope and mercy at the end of every story.

## Narrator voice (user's choice, 19 Nov 2026)
- **Callum** stays the channel's voice, English and Urdu (user tested Adam, Brian, George, Daniel, David, Declan and the
  Urdu library voices Kamran, Amjid, Naqsh; results in scripts/voice-samples/RESULTS.md).
- The default Callum (N2lVS1w4EtoT3dr4eOWO) stops working on **31 Dec 2026**. From then on use the Voice Library
  version "Callum - Husky Trickster" (**5OSluWlAJntR1KG2pWaB**, tested 19 Nov: works in English and Urdu, sounds
  slightly deeper). Switch every narration.json before the first video made after 31 Dec. The user should add it to
  My Voices in ElevenLabs so it stays available.
- 19 Nov (later): the user's own clone "Faisal Narrator (Haq Stories)" (lxAuND1y6e93CWiS40Uz, made from a cleaned
  3.2 min recording, works only with eleven_v3) tested best in Urdu (native, 6.3 st expressive), but the user chose
  **C: keep Callum** for everything. Do not switch voices unless the user asks.


- **Urdu honorific for two prophets (user, 20 Nov 2026):** use "علیہ السلام" (not "علیہما السلام") in Urdu narration and captions, e.g. "حضرت موسیٰ اور حضرت یوسف علیہ السلام".

## Callum and "Astaghfirullah" (20 Nov 2026)
Callum (multilingual v2) says the غ in أَسْتَغْفِرُ اللَّهَ as an English hard "g" (failed the speech-to-text check 6 times).
Rule: don't voice Astaghfirullah with Callum; say "ask Allah for forgiveness" and show أَسْتَغْفِرُ اللَّهَ on screen.
Hasbunallahu wa ni'mal wakeel passes (EN and UR). Check every Arabic phrase with the strict YES/NO check before showing the user.
- Hindustani Shorts (23 Nov): spoken Arabic duas (Hasbunallah, Astaghfirullah) are NOT voiced; voice says the Urdu meaning, Arabic + Hindi shown on screen (Callum's ح/ع/غ are Urdu-style).

## Arabic Names and duas: eleven_v3 (user approved 23 Nov 2026: "V3 is excellent")
- Names of Allah, duas and short Arabic phrases are voiced with Callum on **eleven_v3**, written in Arabic script with full
  vowel marks (e.g. حَسْبُنَا اللّٰهُ وَنِعْمَ الْوَكِيْلُ), then checked with speech-to-text letter by letter before use.
- Test 23 Nov (tests/names/): v3 got 10/10 Names right (incl. ح ع غ ق) and all 4 duas (Hasbunallah, Astaghfirullah,
  La hawla wa la quwwata illa billah, Masha'Allah). v2 (multilingual) dropped the long "aa" in Ar-Rahman: never use v2 for Arabic.
- This replaces the earlier workaround (Arabic shown on screen only). English Shorts may voice the Arabic phrase as a v3 clip.
- Tool (23 Nov): tools/tts_eleven.py does this automatically: when a v2 (English) narration contains Arabic script, the English parts are voiced on v2 and each Arabic run on eleven_v3, joined with 0.12 s gaps; check each Arabic line with tools/arabic_check.py <id> <line>. First used on 38-fire (both clips YES).

## Multiple voices in dialogue (user approved 23 Nov 2026: "Save it")
- Callum narrates everything, including every word of prophets, the Prophet ﷺ, Companions, righteous women, angels and jinn
  ("He said: …"). Never a voice that "plays" a holy figure (acting them = depicting them).
- Other speakers (rulers, chiefs, ordinary people in a story: Pharaoh, Ibrahim's father, the two men before Dawud, the
  Queen's chiefs, the lender/borrower) may get a distinct male voice, only when a Short or film has real back-and-forth dialogue.
- No female voice acting: women's words (e.g. the Queen of Sheba, Hajar) are quoted by the narrator.
- Each new voice is tested and sent to the user to hear before its first use.
