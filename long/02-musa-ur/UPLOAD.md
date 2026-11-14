# Long video 2 (Urdu): Hazrat Musa (AS): Upload details

**Files**
- Video: `02-musa-ur.mp4` (1920×1080, 12:12, Urdu narration, Urdu captions and Maududi verse cards)
- Thumbnail: `thumbnail/thumbnail.jpg`

**When:** Sunday evening, the day after the English film (English Saturday, Urdu Sunday).

## Title
Hazrat Musa AS Aur Firaun Ka Mukammal Waqia | Full Movie in Urdu | حضرت موسیٰؑ

## Description
جس بچے کو قتل ہونا تھا، دریا اسے اسی بادشاہ کے محل تک لے گیا جو اس کی جان کا دشمن تھا۔ برسوں بعد وہ اسی بادشاہ کے لشکر اور سمندر کے بیچ کھڑا تھا، اور فرمایا: "ہرگز نہیں، میرے ساتھ میرا رب ہے، وہ ضرور میری رہنمائی فرمائے گا۔" (الشعراء 26:62)

یہ قرآن سے حضرت موسیٰ علیہ السلام کا مکمل قصہ ہے: دریا پر ٹوکری، مدین کا کنواں، طور پر آگ، عصا اور جادوگر، نشانیاں، سمندر کا پھٹنا، اور فرعون کا انجام۔

Hazrat Musa AS ka mukammal waqia, Quran se, Urdu mein: Firaun, Madyan, Koh-e-Toor, jadugar, aur samundar ka phatna.

ابواب
0:00 آغاز
0:38 مصر کا ظالم
1:27 دریا پر ٹوکری
2:38 شہر میں ایک گھونسا
3:44 مدین کا کنواں
4:42 پہاڑ پر آگ
5:46 میرا سینہ کھول دے
6:51 فرعون کے دربار میں
7:35 جادوگر
8:56 نشانیاں
9:43 سمندر
10:29 اب؟
11:25 سبق

ماخذ: سورۃ القصص (28)، طٰہٰ (20)، الشعراء (26)، الاعراف (7)، یونس (10)، النازعات (79)۔ آیات کا اردو ترجمہ: مولانا مودودی (تفہیم القرآن)۔ ہر آیت حوالے کے ساتھ اسکرین پر دکھائی گئی ہے۔

کسی نبی کو کسی بھی شکل میں نہیں دکھایا گیا۔ ان کی باتیں صرف آواز اور تحریر کے ذریعے بیان کی گئی ہیں۔

English version: Prophet Musa (AS) and Pharaoh: The Complete Story from the Quran

حق کہانیاں | Haq Stories کو سبسکرائب کریں، قرآن سے انبیاء کے قصوں کے لیے۔

#HazratMusa #QasasUlAnbiya #IslamicStoriesUrdu

## Tags
hazrat musa ka waqia, hazrat musa aur firaun, musa as ka waqia, firaun ka waqia, hazrat musa story in urdu, qasas ul anbiya urdu, anbiya ke waqiat, islamic movie urdu, full movie in urdu, quran ke waqiat, prophet musa story urdu, haq stories

## Upload settings
- **Video language:** Urdu. **Made for kids:** No. **Category:** Education. **Altered or synthetic content:** No.
- **Playlist:** "Stories of the Prophets | Complete Stories" (or a separate Urdu playlist, "Qasas ul Anbiya | Urdu").

## After you publish
- Pin a comment: "آپ کو اس قصے کا کون سا لمحہ سب سے زیادہ متاثر کر گیا؟ 👇"

## Rebuilding
```bash
cd long/02-musa-ur
python3 ../../tools/build_long.py .          # spec.json "lang": "ur"
python3 ../../tools/soundscape_long.py .
npx --yes hyperframes@0.9.23 render -q delivery -o renders/02-musa-ur.mp4
python3 ../../tools/mix.py . renders/02-musa-ur.mp4
ffmpeg -i renders/02-musa-ur.mp4 -c:v libx264 -preset slow -crf 21 -pix_fmt yuv420p -c:a copy -movflags +faststart 02-musa-ur.mp4
```
