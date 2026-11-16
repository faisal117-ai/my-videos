# Long video 1 (Urdu): Hazrat Yusuf (AS): Upload details

**Files**
- Video: `01-yusuf-ur.mp4` (1920×1080, ~15:55, Urdu narration, Urdu captions and Maududi verse cards)
- Thumbnail: `../../thumbs/yusuf-ur-well.jpg`

**When:** Tue 17 Nov 2026, 7:00 PM PKT (scheduled in Metricool).

## Title
Hazrat Yusuf AS Ka Mukammal Waqia | Full Movie in Urdu | حضرت یوسفؑ

## Description
جنہیں ان کے اپنے بھائیوں نے کنویں میں پھینک دیا… وہ ایک دن مصر کے خزانوں کے نگران بنے۔ کنواں، غلامی، قید خانہ… اور پھر تخت۔ اور جب وہی بھائی ان کے سامنے کھڑے تھے، تو انہوں نے فرمایا: آج تم پر کوئی گرفت نہیں۔

یہ قرآن سے حضرت یوسف علیہ السلام کا مکمل قصہ ہے، سورۃ یوسف سے: گیارہ ستاروں کا خواب، کنواں، چند درہموں میں فروخت، بند دروازے، قید خانہ، بادشاہ کا خواب، سنہری پیالہ، حضرت یعقوب علیہ السلام کا صبرِ جمیل، اور تیسرا قمیص۔

Hazrat Yusuf AS ka mukammal waqia, Quran se, Urdu mein: bhaiyon ka hasad, kunwan, Misr, qaid khana, badshah ka khwab aur sabr-e-jameel.

"اگلے لوگوں کے ان قصوں میں عقل و ہوش رکھنے والوں کے لیے عبرت ہے" (یوسف 12:111)

ابواب
0:00 آغاز
0:44 گیارہ ستاروں کا خواب
1:36 کنواں
3:07 چند درہموں میں فروخت
3:59 بند دروازے
5:13 شہر کی عورتیں
6:28 قید خانہ اور دو خواب
7:25 بادشاہ کا خواب
8:39 قید خانے سے خزانوں تک
9:55 بھائی اور سنہری پیالہ
11:30 میں اپنے غم کی فریاد اللہ سے کرتا ہوں
12:38 میں یوسف ہوں
13:51 تیسرا قمیص
15:12 سبق

ماخذ: سورۃ یوسف (12)۔ آیات کا اردو ترجمہ: مولانا مودودی (تفہیم القرآن)۔ ہر آیت حوالے کے ساتھ اسکرین پر دکھائی گئی ہے۔

کسی نبی کو کسی بھی شکل میں نہیں دکھایا گیا۔ ان کی باتیں صرف آواز اور تحریر کے ذریعے بیان کی گئی ہیں۔

English version: https://youtu.be/2l7eG427nRY
حضرت موسیٰؑ کا مکمل قصہ (اردو): https://youtu.be/h59TV5hdSew

حق کہانیاں | Haq Stories کو سبسکرائب کریں، قرآن سے انبیاء کے قصوں کے لیے۔

#HazratYusuf #QasasUlAnbiya #IslamicStoriesUrdu

## Tags
hazrat yusuf ka waqia, hazrat yousuf ka qissa, hazrat yusuf story in urdu, yusuf as aur zulekha, surah yusuf ka waqia, qasas ul anbiya urdu, anbiya ke waqiat, islamic movie urdu, full movie in urdu, quran ke waqiat, prophet yusuf story urdu, haq stories

## Upload settings
- **Video language:** Urdu. **Made for kids:** No. **Category:** Education. **Altered or synthetic content:** No.
- **Playlist:** the Urdu playlist, "Anbiya Ke Waqiat | Mukammal Films (Urdu)".

## After you publish
- End screen → the Urdu Musa film. Pin a comment that asks which moment touched them most.
- Shorts about Yusuf (well, three shirts, never lost hope): Related video can point here for Urdu viewers.

## Rebuilding
```bash
cd long/01-yusuf-ur
python3 ../../tools/build_long.py .          # spec.json "lang": "ur"
python3 ../../tools/soundscape_long.py .
npx --yes hyperframes@0.9.23 render -q delivery -o renders/01-yusuf-ur.mp4
python3 ../../tools/mix.py . renders/01-yusuf-ur.mp4
ffmpeg -i renders/01-yusuf-ur.mp4 -c:v libx264 -preset slow -crf 21 -pix_fmt yuv420p -c:a copy -movflags +faststart 01-yusuf-ur.mp4
```
The Urdu narration comes line for line from the checked Urdu subtitles of the English film (subtitles_ur.json);
verse cards are cut from Maududi (quran-cloud) and checked by build_long.py.
