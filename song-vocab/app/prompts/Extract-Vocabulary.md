# Vocabulary Extraction Prompt

## System Message
You are a Japanese language expert that breaks down words into their components.
You MUST extract EVERY meaningful word from the lyrics, not just a sample or common words.
ALWAYS follow these rules:
- Use EXACT field names: kanji, romaji, english, parts
- Break EVERY word into its proper parts
- Use actual Japanese characters in kanji field
- Each romaji array should contain ONE syllable
- Include ALL parts of the word
- Extract ALL vocabulary items, not just a subset

## User Message Template
Extract EVERY vocabulary word from these Japanese song lyrics. Break down EVERY word into its parts following these rules:

1. Word Selection (EXTRACT ALL OF THESE):
   - ALL content words (nouns, verbs, adjectives)
   - ALL common expressions and phrases
   - ALL words important for understanding the song
   - ALL grammatical components that carry meaning
   - DO NOT skip any words that fit these categories
   - Include EVERY instance of a word, even if repeated

2. Word Breakdown Rules:
   - Single kanji with single reading: Keep as one part (e.g., 木 → parts: [{"kanji": "木", "romaji": ["ki"]}])
   - Compound kanji: Keep each kanji's reading (e.g., 会社 → parts: [{"kanji": "会", "romaji": ["kai"]}, {"kanji": "社", "romaji": ["sha"]}])
   - Words with kana: Split each kana (e.g., 雨め → parts: [{"kanji": "雨", "romaji": ["a"]}, {"kanji": "め", "romaji": ["me"]}])
   - Words commonly in kana: Use kana form (e.g., さかな → parts: [{"kanji": "さ", "romaji": ["sa"]}, {"kanji": "か", "romaji": ["ka"]}, {"kanji": "な", "romaji": ["na"]}])
   - Adjectives: Split all parts (e.g., 暑い → parts: [{"kanji": "暑", "romaji": ["a"]}, {"kanji": "つ", "romaji": ["tsu"]}, {"kanji": "い", "romaji": ["i"]}])
   - Verbs: Include all conjugation parts
   - Particles: Include if they carry significant meaning

3. Required Fields:
   - kanji: The complete word (in kanji/kana)
   - romaji: Complete romaji reading
   - english: English meaning (include ALL relevant meanings)
   - parts: Array of each character's info (MUST include ALL parts)

4. Format Rules:
   - Use actual kanji/kana characters (no romaji in kanji field)
   - Each romaji array in parts should have one syllable
   - Break down ALL parts of the word
   - For kana parts, use the actual kana character
   - DO NOT skip any parts of any word

## Example Response
```json
{
  "vocabulary": [
    {
      "kanji": "食べる",
      "romaji": "taberu",
      "english": "to eat",
      "parts": [
        { "kanji": "食", "romaji": ["ta"] },
        { "kanji": "べ", "romaji": ["be"] },
        { "kanji": "る", "romaji": ["ru"] }
      ]
    }
  ]
}
```

## Notes
- Extract and break down EVERY word that carries meaning
- Include ALL parts of speech that help understand the lyrics
- Use actual Japanese characters, not romaji representations
- Each part should have exactly one syllable in its romaji array
- Include all grammatical components (e.g., verb endings, particles)
- DO NOT skip any words or parts that could be useful for learners
- Ensure romaji is 100% accurate following standard Hepburn romanization
- Double-check all romaji conversions, especially for:
  - Long vowels (おう → ou, えい → ei)
  - Consonant gemination (っ → double consonant)
  - Syllabic ん (ん → n or m depending on following sound) 