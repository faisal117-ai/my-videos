"""Translated titles and descriptions for YouTube (Studio → video → Subtitles/Translations → Add language →
Title & description). Verse quotes come only from the quran-json package (Arabic original; Indonesian, Bengali,
Turkish translations), never typed. Story lines are ours. Writes scripts/translations/<film>.md."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
P = ROOT / "node_modules/quran-json/dist/"
AR = json.loads((P / "quran.json").read_text()); T = {l: json.loads((P / f"quran_{l}.json").read_text()) for l in ["id", "bn", "tr"]}
OT = str.maketrans({"ٗ": "ࣰ", "ٞ": "ࣱ", "ٖ": "ࣲ"})

def ar(s, v, a=1, b=None):
    w = AR[s - 1]["verses"][v - 1]["text"].split()
    return " ".join(w[a - 1:b]).translate(OT)

def q(l, s, v, cut=None):
    t = T[l][s - 1]["verses"][v - 1]["translation"].strip()
    if cut:  # keep only the first sentence ("." / "।") or, for "clause", the first clause (",")
        m = re.search(r"[,،]" if cut == "clause" else r"[.।](?=\s|$)", t)
        if m:
            t = t[:m.start()] + ("" if cut == "clause" else t[m.start()])
    return t.strip(' "')

REF = {"ar": "{name} {s}:{v}", "id": "QS {name} {s}:{v}", "bn": "সূরা {name} {s}:{v}", "tr": "{name} Suresi {s}:{v}"}
SURA = {12: {"ar": "يوسف", "id": "Yusuf", "bn": "ইউসুফ", "tr": "Yusuf"},
        21: {"ar": "الأنبياء", "id": "Al-Anbiya", "bn": "আল-আম্বিয়া", "tr": "Enbiya"},
        26: {"ar": "الشعراء", "id": "Asy-Syu'ara", "bn": "আশ-শুআরা", "tr": "Şuara"}}

FILMS = {
 "yusuf-en": {"url": "https://youtu.be/2l7eG427nRY", "verse": (12, 111), "ar": (1, 7),
   "cut": {"id": "sentence", "bn": "clause", "tr": "sentence"},
   "title": {
    "ar": "ألقاه إخوته في البئر… فأصبح عزيز مصر | قصص الأنبياء الحلقة 1: النبي يوسف عليه السلام",
    "id": "Dibuang Saudaranya ke Sumur… Lalu Berkuasa di Mesir | Kisah Para Nabi EP 1: Nabi Yusuf AS",
    "bn": "ভাইয়েরা তাঁকে কূপে ফেলে দিল… তিনি হলেন মিশরের শাসক | নবীদের কাহিনী পর্ব ১: নবী ইউসুফ (আ.)",
    "tr": "Kardeşleri Onu Kuyuya Attı… Mısır'ın Yöneticisi Oldu | Peygamberler Tarihi 1: Hz. Yusuf (a.s.)"},
   "story": {
    "ar": "القصة الكاملة للنبي يوسف عليه السلام من القرآن الكريم: رؤيا الأحد عشر كوكبًا، البئر، السجن، رؤيا الملك، وعفوه عن إخوته.",
    "id": "Kisah lengkap Nabi Yusuf AS dari Al-Qur'an: mimpi sebelas bintang, sumur, penjara, mimpi raja, dan maafnya kepada saudara-saudaranya.",
    "bn": "কুরআন থেকে নবী ইউসুফ (আ.)-এর সম্পূর্ণ কাহিনী: এগারোটি তারার স্বপ্ন, কূপ, কারাগার, বাদশাহর স্বপ্ন এবং ভাইদের প্রতি তাঁর ক্ষমা।",
    "tr": "Kur'an'dan Hz. Yusuf'un (a.s.) tüm kıssası: on bir yıldız rüyası, kuyu, zindan, kralın rüyası ve kardeşlerini affetmesi."}},
 "musa-en": {"url": "https://youtu.be/I9d00aHMQrQ", "verse": (26, 62), "ar": (1, None), "cut": {},
   "title": {
    "ar": "انشقّ البحر… وغرق فرعون | قصص الأنبياء الحلقة 2: النبي موسى عليه السلام",
    "id": "Laut Terbelah… dan Firaun Tenggelam | Kisah Para Nabi EP 2: Nabi Musa AS",
    "bn": "সমুদ্র দুই ভাগ হলো… আর ফেরাউন ডুবে গেল | নবীদের কাহিনী পর্ব ২: নবী মূসা (আ.)",
    "tr": "Deniz Yarıldı… ve Firavun Boğuldu | Peygamberler Tarihi 2: Hz. Musa (a.s.)"},
   "story": {
    "ar": "القصة الكاملة للنبي موسى عليه السلام من القرآن الكريم: التابوت في النهر، بئر مدين، النار على الجبل، السحرة، انشقاق البحر، ونهاية فرعون.",
    "id": "Kisah lengkap Nabi Musa AS dari Al-Qur'an: peti di sungai, sumur Madyan, api di gunung, para penyihir, laut terbelah, dan akhir Firaun.",
    "bn": "কুরআন থেকে নবী মূসা (আ.)-এর সম্পূর্ণ কাহিনী: নদীতে সিন্দুক, মাদইয়ানের কূপ, পাহাড়ে আগুন, জাদুকরেরা, সমুদ্র বিভক্ত হওয়া এবং ফেরাউনের পরিণতি।",
    "tr": "Kur'an'dan Hz. Musa'nın (a.s.) tüm kıssası: nehirdeki sandık, Medyen kuyusu, dağdaki ateş, sihirbazlar, denizin yarılması ve Firavun'un sonu."}},
 "ibrahim-en": {"url": "(published Sat 21 Nov)", "verse": (21, 69), "ar": (1, None), "cut": {},
   "title": {
    "ar": "أُلقي في النار… فكانت بردًا وسلامًا | قصص الأنبياء الحلقة 3: النبي إبراهيم عليه السلام",
    "id": "Dilempar ke Api… Api Itu Menjadi Dingin | Kisah Para Nabi EP 3: Nabi Ibrahim AS",
    "bn": "আগুনে নিক্ষেপ করা হলো… আগুন শীতল হয়ে গেল | নবীদের কাহিনী পর্ব ৩: নবী ইবরাহিম (আ.)",
    "tr": "Ateşe Atıldı… Ateş Serinledi | Peygamberler Tarihi 3: Hz. İbrahim (a.s.)"},
   "story": {
    "ar": "القصة الكاملة للنبي إبراهيم عليه السلام من القرآن الكريم: الأصنام، النار، وادي مكة وزمزم، الرؤيا والفداء، وبناء الكعبة.",
    "id": "Kisah lengkap Nabi Ibrahim AS dari Al-Qur'an: berhala, api, lembah Makkah dan Zamzam, mimpi dan kurban, serta pembangunan Ka'bah.",
    "bn": "কুরআন থেকে নবী ইবরাহিম (আ.)-এর সম্পূর্ণ কাহিনী: মূর্তি, আগুন, মক্কার উপত্যকা ও যমযম, স্বপ্ন ও কুরবানি এবং কাবা নির্মাণ।",
    "tr": "Kur'an'dan Hz. İbrahim'in (a.s.) tüm kıssası: putlar, ateş, Mekke vadisi ve Zemzem, rüya ve kurban, Kâbe'nin inşası."}},
}
COMMON = {
 "ar": "رسوم متحركة، كل آية تُعرض على الشاشة مع مرجعها. لا يُصوَّر أي نبي بأي شكل. السرد باللغة الإنجليزية.\nاشترك في Haq Stories | حق کہانیاں لقصص الأنبياء من القرآن.",
 "id": "Animasi; setiap ayat ditampilkan di layar beserta rujukannya. Tidak ada nabi yang digambarkan dalam bentuk apa pun. Narasi dalam bahasa Inggris.\nSubscribe Haq Stories | حق کہانیاں untuk kisah para nabi dari Al-Qur'an.",
 "bn": "অ্যানিমেশন; প্রতিটি আয়াত সূত্রসহ পর্দায় দেখানো হয়েছে। কোনো নবীকে কোনো রূপে দেখানো হয়নি। বর্ণনা ইংরেজিতে।\nকুরআনের নবীদের কাহিনীর জন্য Haq Stories | حق کہانیاں সাবস্ক্রাইব করুন।",
 "tr": "Animasyon; her ayet kaynağıyla birlikte ekranda gösterilir. Hiçbir peygamber hiçbir şekilde tasvir edilmez. Anlatım İngilizcedir.\nKur'an'dan peygamber kıssaları için Haq Stories | حق کہانیاں kanalına abone olun."}
NAMES = {"ar": "العربية", "id": "Bahasa Indonesia", "bn": "বাংলা (Bengali)", "tr": "Türkçe"}

out = ROOT / "scripts/translations"; out.mkdir(parents=True, exist_ok=True)
for key, f in FILMS.items():
    s, v = f["verse"]; a, b = f["ar"]
    md = [f"# {key}: translated titles and descriptions", "",
          "YouTube Studio → the video → **Subtitles** (or Translations) → **Add language** → choose the language → "
          "**Title & description** → paste → Publish.", f"Video: {f['url']}", ""]
    for l in ["ar", "id", "bn", "tr"]:
        verse = ar(s, v, a, b) if l == "ar" else q(l, s, v, f["cut"].get(l))
        ref = REF[l].format(name=SURA[s][l], s=s, v=v)
        md += [f"## {NAMES[l]}", "**Title**", "```", f["title"][l], "```", "**Description**", "```",
               f["story"][l], "", f"«{verse}» ({ref})", "", COMMON[l], "```", ""]
        assert len(f["title"][l]) <= 100, (key, l, len(f["title"][l]))
    (out / f"{key}.md").write_text("\n".join(md), encoding="utf-8")
    print(key, "ok")
