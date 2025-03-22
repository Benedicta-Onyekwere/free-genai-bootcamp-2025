# Vocabulary Importer

A tool for generating and managing vocabulary for language learning applications.

## Japanese Vocabulary Generator

An internal tool for rapidly populating a language learning application with vocabulary words and word groups. Built using Streamlit and OpenAI's GPT-3.5 API.

## Business Goal

The prototype of the language learning app is built, but we need to quickly populate the application with word and word groups so students can begin testing the system.

There is currently no interface for manually adding words or words groups and the process would be too tedious. 

### Framework Selection
The application is built with Streamlit, chosen from the following approved options:
- ✅ Streamlit (selected for data-centric UI and rapid development)
- ⭕ Gradio
- ⭕ FastHTML

### LLM Integration Options
The tool supports two LLM integration approaches:
1. ✅ Managed/Serverless LLM API (currently using OpenAI's GPT-3.5)
2. ⭕ Local LLM serving via OPEA (planned for future implementation)

### Solution
This internal tool addresses these needs by:
- Automating vocabulary generation using LLM (GPT-3.5)
- Providing a user-friendly interface for vocabulary management
- Supporting import/export functionality for batch processing

### Technical Implementation
- **Framework**: Streamlit (chosen for rapid prototyping and data-focused UI)
- **LLM Integration**: OpenAI's GPT-3.5 API (managed LLM solution)
- **Data Format**: JSON for easy import/export compatibility

## Features

- Generate Japanese vocabulary words based on topics and JLPT levels
- Detailed breakdown of each word into its syllable components
- Support for various word types (kanji, kana, mixed)
- Export vocabulary lists as JSON for database import
- Import and validate existing vocabulary JSON files
- Usage tracking and cost estimation
- Persistent API key management

## Example Output

![Generated Vocabulary](../free-genai-bootcamp-2025/lang-portal/assets/vocab-gen-output.png)
*Example of generated vocabulary showing detailed word breakdowns with kanji, romaji, and syllable components*

![Technology Vocabulary](../free-genai-bootcamp-2025/lang-portal/assets/tech-vocab-output.png)
*Example of technology-related vocabulary showing mixed usage of kanji (電話), hiragana (でんわ), and katakana (コンピュータ)*

## Development Process

### 1. Initial Setup
- Created Streamlit application structure
- Implemented OpenAI API integration
- Set up basic UI components for vocabulary generation

### 2. Word Structure Implementation
- Developed JSON structure for vocabulary words
- Added validation for proper word formatting
- Implemented caching system for API responses

### 3. Syllable Breakdown Enhancement
#### Challenge:
Initially, the system wasn't correctly breaking down words into their syllable components, especially for:
- Mixed kanji-kana words
- Words with multiple readings
- Single kanji with multiple syllables

#### Solution:
- Implemented strict validation rules
- Created detailed examples in the prompt
- Added specific patterns for different word types:
  ```json
  {
    "kanji": "食べる",
    "romaji": "taberu",
    "english": "to eat",
    "parts": [
      {
        "kanji": "食",
        "romaji": ["ta"]
      },
      {
        "kanji": "べ",
        "romaji": ["be"]
      },
      {
        "kanji": "る",
        "romaji": ["ru"]
      }
    ]
  }
  ```

### 4. API Response Formatting
#### Challenge:
The OpenAI API sometimes returned inconsistent formats or incorrect field names.

#### Solution:
- Added comprehensive validation checks
- Implemented transformation function for incorrect formats
- Set temperature to 0 for more consistent responses
- Added explicit examples in the system prompt

### 5. Cache Management
#### Challenge:
Cached responses were persisting between sessions, causing outdated or incorrect results.

#### Solution:
- Implemented automatic cache clearing on startup
- Added force refresh option
- Created unique cache keys based on topic, JLPT level, and word count

### 6. User Interface Improvements
- Added usage statistics
- Implemented progress tracking
- Created download functionality for generated vocabulary
- Added import/export capabilities

## Technical Details

### Validation Rules
- Root must be `{"words": [...]}`
- Each word must have: kanji, romaji, english, parts
- Each part must have kanji and romaji fields
- Romaji must be an array with one syllable per element

### Word Patterns
1. Single kanji, single syllable: `木 → 木[ki]`
2. Single kanji, multiple syllables: `雨 → 雨[a] + め[me]`
3. Multiple kanji: `天気 → 天[ten] + 気[ki]`
4. Mixed kanji-kana: `食べる → 食[ta] + べ[be] + る[ru]`
5. Pure kana: `ひとつ → ひ[hi] + と[to] + つ[tsu]`

## Setup and Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up your API key:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and replace `your_key_here` with your actual OpenAI API key
   - Alternatively, you can enter your API key directly in the application's sidebar
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Security Note

⚠️ Important: Never commit your `.env` file or expose your API key. The `.env` file is included in `.gitignore` to prevent accidental commits. If you prefer not to use a .env file to avoid accidentally committing your key, you can enter it directly in the application's sidebar - it will only be stored in session state and will need to be re-entered when you restart the application.

## Future Improvements

- Add support for custom word lists
- Implement pronunciation audio
- Add example sentences
- Create export options for different formats (CSV, Excel)
- Add stroke order diagrams for kanji 