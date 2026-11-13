# Long video 2: Musa (AS): Upload details

**Files**
- Video: `renders/02-musa.mp4` (1920×1080, 11:30, −14.5 LUFS). Not in git if it is over 100 MB.
- Thumbnail: `thumbnail/thumbnail.jpg` (1280×720)
- Subtitles: `subtitles/en.srt` (English, timed from the voice). No Urdu file this time.

**When:** after the Short "She put her baby in the river…" (Musa's mother), which leads into it.

## Title
Prophet Musa (AS) and Pharaoh: The Complete Story from the Quran

## Description
A baby who was meant to be killed was carried by a river into the palace of the very king who wanted him dead. Years later, he stood between that king's army and the sea, and said: "No! Indeed, with me is my Lord; He will guide me." (Ash-Shu'ara 26:62)

This is the complete story of Prophet Musa (AS), told in order from the Quran: the basket on the river, the flight to Madyan, the fire on the mountain, the staff and the magicians, the signs, the parting of the sea, and the end of Pharaoh.

Chapters
0:00 Intro
0:39 The Tyrant of Egypt
1:25 The Basket on the River
2:29 One Blow in the City
3:28 The Well of Madyan
4:29 The Fire on the Mountain
5:38 Expand My Chest
6:37 Before Pharaoh
7:19 The Magicians
8:33 The Signs
9:14 The Sea
9:56 Now?
10:45 The Lesson

Sources: Surah Al-Qasas (28), Taha (20), Ash-Shu'ara (26), Al-A'raf (7), Yunus (10) and An-Nazi'at (79). English translation: Sahih International. Every quoted verse is shown on screen with its reference.

No prophet is shown in any form. Their words are carried only by the voice and the text.

Watch next: The Complete Story of Prophet Yusuf (AS) from the Quran.

Subscribe to Haq Stories | حق کہانیاں for the stories of the prophets, from the Quran.

#ProphetMusa #StoriesOfTheProphets #QuranStories

## Tags
prophet musa story, story of prophet musa, musa and pharaoh, moses in islam, musa and firaun, parting of the sea quran, hazrat musa ka waqia, hazrat musa story in urdu, musa and the magicians, surah qasas, surah taha, stories of the prophets, quran stories, islamic stories, haq stories

## Upload settings
- **Thumbnail:** upload `thumbnail/thumbnail.jpg` in Studio if Metricool's custom thumbnail doesn't show (YouTube only accepts it on verified channels).
- **Subtitles:** Subtitles → Add language → English → Upload file → *With timing* → `subtitles/en.srt`.
- **Altered or synthetic content:** No. **Made for kids:** No. **Category:** Education.
- **End screen:** Subscribe + the Yusuf (AS) long video.
- **Playlist:** "Stories of the Prophets | Complete Stories".

## After you publish
- Pin a comment: "Which moment hit you hardest: the basket on the river, the dua at the well, or the sea? 👇"
- On the Short "She put her baby in the river…": set **Related video** to this video.

## Rebuilding
```bash
cd long/02-musa
python3 ../../tools/build_long.py .          # scenes from tools/scenes_musa.py
python3 ../../tools/soundscape_long.py .
npx --yes hyperframes@0.9.23 render -q delivery -o renders/02-musa.mp4
python3 ../../tools/mix.py . renders/02-musa.mp4
python3 ../../tools/srt_en_long.py .
node ../../tools/screenshot.js $PWD/thumbnail/thumbnail.html $PWD/thumbnail/thumbnail.jpg
```
