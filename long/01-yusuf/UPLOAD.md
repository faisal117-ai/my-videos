# Long video 1: Yusuf (AS): Upload details

**Files**
- Video: `renders/01-yusuf.mp4` (1920×1080, 30 fps, 14:08, −14.6 LUFS). Not in git (too large); rebuild with the steps at the bottom.
- Thumbnail: `thumbnail/thumbnail.jpg` (1280×720)
- Subtitles: `subtitles/ur.srt` (Urdu: verse quotes from Maududi), `subtitles/en.srt` (English)

**When:** after Yusuf Part 2 (Short), while interest is high.

## Title
The Complete Story of Prophet Yusuf (AS) from the Quran | Surah Yusuf

(69 characters, so it isn't cut off in search. The thumbnail carries the hook, "From the Well… to the Throne", so the title doesn't repeat it.)

## Description
His own brothers threw him into a well. Years later, they stood before him begging for grain, and didn't know who he was.

This is the complete story of Hazrat Yusuf (AS), told in order from Surah Yusuf (Chapter 12 of the Quran): the dream of eleven stars, the well, the closed doors, the prison, the king's dream, and the day he said, "No blame will there be upon you today." Allah calls it the best of stories (12:3).

Chapters
0:00 Intro
0:44 The Dream of Eleven Stars
1:30 The Well
2:53 Sold for a Few Coins
3:42 The Closed Doors
4:49 The Women of the City
5:50 Prison and Two Dreams
6:44 The King's Dream
7:46 From Prison to the Storehouses
8:49 The Brothers and the Golden Cup
10:15 "I Only Complain to Allah"
11:17 "I Am Yusuf"
12:19 The Third Shirt
13:30 The Lesson

"There was certainly in their stories a lesson for those of understanding." (Yusuf 12:111)

Sources: every event is from Surah Yusuf (12:3–111). English translation: Sahih International. Urdu subtitles: Maulana Maududi (Tafheem-ul-Quran) for the verses. The name Binyamin comes from tradition; the Quran says "his brother".

No prophet is shown in any form. Their words are carried only by the voice and the text.

اردو سب ٹائٹلز دستیاب ہیں (CC)۔

Subscribe to Haq Stories | حق کہانیاں for the stories of the prophets, from the Quran.

#ProphetYusuf #SurahYusuf #StoriesOfTheProphets

## Tags
prophet yusuf story, story of prophet yusuf, surah yusuf, yusuf and his brothers, hazrat yusuf ka waqia, hazrat yusuf story in urdu, prophet joseph in islam, yusuf alayhis salaam, stories of the prophets, quran stories, best of stories quran, surah yusuf tafseer, islamic stories, prophet stories for adults, haq stories

## Urdu title and description (Settings → Languages → Add translation → Urdu)
**Title:** حضرت یوسف علیہ السلام کا مکمل قصہ، قرآن سے | سورۃ یوسف

**Description:**
ان کے اپنے بھائیوں نے انہیں کنویں میں پھینک دیا۔ برسوں بعد وہی بھائی غلہ مانگتے ہوئے ان کے سامنے کھڑے تھے، اور انہیں پہچانتے تک نہ تھے۔

یہ حضرت یوسف علیہ السلام کا مکمل قصہ ہے، سورۃ یوسف کی ترتیب سے: گیارہ ستاروں کا خواب، کنواں، بند دروازے، قید خانہ، بادشاہ کا خواب، اور وہ دن جب انہوں نے کہا: "آج تم پر کوئی گرفت نہیں"۔

(Then paste the same chapter list as above.)

آیات کا اردو ترجمہ: مولانا مودودی (تفہیم القرآن)۔

## Upload settings
- **Subtitles:** Subtitles → Add language → Urdu → Upload file → *With timing* → `subtitles/ur.srt`. Then English → `subtitles/en.srt`.
- **Video language:** English. **Caption certification:** none needed.
- **Altered or synthetic content:** No (stylised animation; the voice doesn't imitate a real person). Re-check YouTube's wording when you upload.
- **Made for kids:** No.
- **Category:** Education.
- **End screen (last 20 s, over the end card):** Subscribe + "Best for viewer" video.
- **Cards:** at 1:30 (the well), link Yusuf Part 1 (Short).

## After you publish
- Pin a comment: "Which moment hit you hardest: the well, the prison, or "No blame upon you today"? 👇"
- On every Yusuf Short: set **Related video** to this video and pin "Watch the complete story of Yusuf (AS) 👉".

## Rebuilding
```bash
cd long/01-yusuf
python3 ../../tools/build_long.py .          # index.html + compositions/
python3 ../../tools/soundscape_long.py .     # assets/narration.wav + assets/ambience.wav
npx --yes hyperframes@0.9.23 check
npx --yes hyperframes@0.9.23 render -q delivery -o renders/01-yusuf.mp4
python3 ../../tools/mix.py . renders/01-yusuf.mp4
python3 ../../tools/subtitles_long.py .      # subtitles/ur.srt + en.srt
node ../../tools/screenshot.js $PWD/thumbnail/thumbnail.html $PWD/thumbnail/thumbnail.jpg
```
