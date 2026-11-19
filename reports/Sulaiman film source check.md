# Sulaiman film passes its source check

The Prophet Sulaiman (AS) film narration (ch00–ch12, 101 lines) is grounded in the Quran from start to finish. **Nothing in it is invented, and nothing comes from Isra'iliyat.** It names nobody the Quran leaves unnamed, adds no numbers or durations, and lists nothing in the queen's gift. Every story beat traces to Surah an-Naml 27:15–44, Saba 34:12–14, Sad 38:30–36, al-Anbiya 21:78–79 and al-Qasas 28:76–81. The one hadith used, Bukhari 3423, backs the "unmatched kingdom" line ([sunnah.com](https://sunnah.com/bukhari:3423)). **Twenty-three lines went beyond the source or misquoted Sahih International (SI), and all 23 are now fixed in the current json files**, which I re-read to check. The slips were small but real. Some were content added from tafsir: "deep" water, a glass palace "over water", the jinn who "could carry" the throne, and a "man" from "the Book". Others were superlatives the verse does not state, such as "the smallest creature" and "stopped for an ant". The rest were quoted verses that drifted from SI wording. One optional softening remains open (12.0, below). **Limit:** this session's network blocked quran.com, api.quran.com, legacy.quran.com, corpus.quran.com and quranenc.com. The SI wording was therefore checked from search excerpts for 27:39–44, 34:14 and 28:78, and from memory for every other verse. Open each verse card on quran.com (Sahih International) once before the voice lock.

## All 23 flagged lines are now fixed

The line number is chapter.line, counted from 0. "Fixed" means the current json files contain the corrected text shown in the Fix column.

| Line | Verse | Issue | Fix (now in narration) | Status |
|---|---|---|---|---|
| 0.1 | 27:40 | Old hook asked the closing question ("what does a man say when Allah gives him everything?") up front, breaking the open-loop structure | "Who could do that? And what would you say, if it were yours?" | Fixed |
| 2.5 | 34:12 | "The jinn worked" implies all jinn; SI: "**among the jinn were those who** worked" ([Q 34:12](https://quran.com/34/12)) | "some of the jinn worked for him" | Fixed |
| 3.2 | 28:78 | "Later in this story" puts Qarun (time of Musa AS) inside Sulaiman's story | "later in this film" | Fixed |
| 3.4 | 27:18 | "The smallest creature" is a superlative the verse lacks ([Q 27:18](https://quran.com/27/18)) | "one tiny ant spoke" | Fixed |
| 4.1 | 27:18 | Quoted ant's words differed from SI | SI wording: "that you not be crushed by Sulaiman and his soldiers, while they perceive not" | Fixed |
| 4.2 | 27:18 | Echo of the quote used the old wording | "while they perceive not" | Fixed |
| 4.5 | 27:19 | The Quran says he smiled, not that he or the army **stopped** ([Q 27:19](https://quran.com/27/19)) | "smiled at the words of an ant" | Fixed |
| 5.3 | 27:22 | "I have learned what you have not learned" is not SI ([Q 27:22](https://quran.com/27/22)) | "I have encompassed in knowledge that which you have not encompassed…" | Fixed |
| 6.1 | 27:23, 34:15 | "In the south" is a place detail with no verse | "A rich land. A great throne. A strong army." | Fixed |
| 6.3 | 27:24 | "A whole nation, every morning" adds frequency and scope the verse lacks ([Q 27:24](https://quran.com/27/24)) | "A whole people, bowing to the sun" | Fixed |
| 7.2 | 27:29–31 | "O chiefs", word order, "Do not be haughty" all differed from SI ([Q 27:29–31](https://quran.com/27/29-31)) | Full SI wording: "O eminent ones, indeed to me has been delivered a noble letter… Be not haughty with me…" | Fixed |
| 7.4 | 27:34 | "She was wise" and "She did not want war" are the narrator's reading; quote cut short ([Q 27:34](https://quran.com/27/34)) | Full verse + "She feared what kings do." | Fixed |
| 9.1 | 27:39 | Word order differed: "strong and trustworthy for it" ([corpus 27:39](https://corpus.quran.com/translation.jsp?chapter=27&verse=39)) | "I am for this task strong and trustworthy" | Fixed |
| 9.3 | 27:40 | SI: "one who had knowledge from **the Scripture**"; the verse never says "a man" ([legacy 27:40](https://legacy.quran.com/27/40)) | "But one who had knowledge from the Scripture said" | Fixed |
| 10.0 | 27:42 | "As though it were it" is Pickthall; SI has "was it" ([corpus 27:42](https://corpus.quran.com/translation.jsp?chapter=27&verse=42)) | "It is as though it was it." | Fixed |
| 10.1 | 27:44 | "**Deep** water" added; SI: "a body of water" ([corpus 27:44](https://corpus.quran.com/translation.jsp?chapter=27&verse=44)) | "she thought it was a body of water" | Fixed |
| 10.3 | 27:44 | "Palace of glass **over water**" is tafsir; the verse says only she *thought* it was water | "A palace of glass she took for water." | Fixed |
| 10.4 | 27:24, 27:43 | "All her life" is a duration no verse gives | "who used to bow to the sun" | Fixed |
| 10.7 | 27:44 | "A whole nation turned" — the verse records only the queen's submission | "how a queen turned from the sun to her Creator" | Fixed |
| 11.1 | 34:14 | "Showed the jinn" vs SI "indicated to them [the jinn]" ([quran.com 34:14 SI](https://quran.com/saba/14/translation/en-sahih-international)) | "nothing indicated to the jinn his death" | Fixed |
| 11.2 | 34:14 | "Upright" (standing) is tafsir; the verse implies only support by the staff | "still leaning on his staff" | Fixed |
| 11.5 | 27:39–40 | The jinn only **offered**; the one with knowledge brought the throne | "The jinn, who offered to bring a throne…" | Fixed |
| 12.6 | 21:68–69 | "A fire so large no one could come near it" is tafsir size detail; no closing "watch the full movies" line | "thrown into a fire… the one command that made it cool and safe… watch the full movies of Prophet Musa and Prophet Yusuf… links below" ([Q 21:69](https://quran.com/21/69)) | Fixed |

## One optional softening and four minor wording gaps remain

Line **12.0** says Allah gave Sulaiman (AS) "a kingdom no one will ever have again". In 38:35 this is his dua ([Q 38:35](https://quran.com/38/35)). The Quran shows the dua answered in 38:36–39, and the Prophet ﷺ treated it as binding: he let a captured ifrit go because he remembered "the invocation of my brother Solomon" ([Bukhari 3423](https://sunnah.com/bukhari:3423), [Bukhari 461](https://sunnah.com/bukhari:461)). The line can therefore stand. "A kingdom such as no one after him would have" mirrors the verse more closely. "The word he kept saying was: thanks" is a fair summary of 27:19, 27:40 and 34:13, not a quotation, so it should not go on a verse card. Four minor differences from SI are also still in the voice track. 2.4 says "evening" where SI says "afternoon" (*rawāḥ* allows either) ([Q 34:12](https://quran.com/34/12)). 4.6 says "among Your righteous servants" where SI says "into [the ranks of]". 7.0 and 7.5 say "return" where SI says "will return" ([Q 27:35](https://quran.com/27/35)). None of these changes the meaning. The on-screen verse cards, however, should carry the exact SI text.

## Conclusion

The pattern behind the 23 fixes matters for the next film. Not one error was invented story. Each one was tafsir colour that had crept in as plain narration ("over water", "upright", "all her life", "a fire so large") or a narrator's emphasis turned into a claim ("smallest", "stopped", "whole nation"). Run future scripts through two checks: does the verse itself say this word, and does a quoted line match SI word for word. The one risk left is the verification limit. The SI quotes were never fetched live, so a single pass of the verse cards on quran.com, or allowing quran.com in the environment, closes it.
