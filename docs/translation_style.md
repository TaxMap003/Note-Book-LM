# Egyptian Arabic script rules (CPA TCP)

These rules govern `script/script_ar.json`, the Egyptian Arabic version of the NotebookLM video.

## Faithfulness

- Translate every sentence. No simplifying, summarizing, skipping, or adding content.
- Keep every rule, threshold, limit, exception, election, and date exactly as the original states it.
- Keep the original examples: same names, same amounts, same order of computation, same answer.

## What stays in English

- Tax terms and defined terms, spelled exactly as the original and the exam use them: *Adjusted Basis*, *Amount Realized*, *Recognized Gain*, *Boot*, *Hot Assets*, *Outside Basis*, *Inside Basis*, *At-Risk*, *Passive Activity Loss*, *Qualified Business Income*, *Accumulated Adjustments Account*.
- IRC sections, forms, schedules, and acronyms: *Section 1231*, *§179*, *Form 1065*, *Schedule K-1*, *AGI*, *MAGI*, *QBI*, *NOL*, *E&P*, *MACRS*.
- Entity and filing-status names: *C Corporation*, *S Corporation*, *Partnership*, *LLC*, *Married Filing Jointly*.
- Definitions: the definition sentence stays in English, word for word from the original, followed by its faithful Egyptian Arabic rendering (a translation, not a simpler version).

The Egyptian Arabic around the terms is natural teaching speech, for example:
«الـ Adjusted Basis بتاع الـ Partner بيزيد بنصيبه من الـ Taxable Income وبيقل بالـ Distributions».

## Numbers

| | On screen / subtitles (`ar`) | Spoken (`tts`) |
|---|---|---|
| Amounts | `$50,000` | «خمسين ألف دولار» |
| Percentages | `20%` | «عشرين في المية» |
| Years | `2025` | «ألفين خمسة وعشرين» |
| Sections and forms | `Section 1231`, `Form 1065` | `Section twelve thirty-one`, `Form ten sixty-five` (as said in English) |

The spoken line must never contain digits, `$`, or `%`: Nile TTS (XTTS) would expand them into Modern Standard Arabic words («خمسون»), which is not Egyptian.

## Acronyms in the spoken line

A Whisper round-trip of Nile TTS output showed:

- Multi-word English terms in Latin script come back exactly ("Exclusion Ratio", "Total Expected Return").
- Letter acronyms in Latin script are read as words ("AGI" → «أجي», "IRAs" → "Iris"). Write them as Arabic letter names in `tts`: AGI «إيه جي آي», IRA «آي آر إيه», RMDs «آر إم ديز», ROI «آر أو آي», CPA «سي بي إيه», CEO «سي إي أو».
- Acronyms said as words stay in Latin: FAFSA. Numbers said in English stay in Latin words: `five twenty-nine plan`, `four oh one k`.

Subtitles (`ar`) always show the normal English form (AGI, IRA, 401(k)).

## Script format

```json
{
  "title": "…",
  "glossary": [{"term": "Outside Basis", "ar": "الـ basis بتاع الـ partner في الـ partnership interest نفسه"}],
  "units": [
    {
      "id": 7, "start": 41.2, "end": 49.8,
      "en": "Original English sentence(s) from the narration.",
      "parts": [
        {"ar": "النص اللي بيظهر في الـ subtitles، فيه $50,000.", "tts": "النص المنطوق، فيه خمسين ألف دولار."}
      ]
    }
  ]
}
```

- `start` / `end` come from the English transcript (`script/units_en.json`) and must not be edited: they keep the slides in sync.
- Each part is one Nile TTS call and one subtitle cue, at most 160 characters. `tts` defaults to `ar` when omitted.
