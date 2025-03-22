import streamlit as st
import json
import pandas as pd
from pathlib import Path
from openai import OpenAI
from typing import List, Dict
import os
from dotenv import load_dotenv
import hashlib
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize session state for usage tracking
if 'request_count' not in st.session_state:
    st.session_state.request_count = 0
if 'cache' not in st.session_state:
    st.session_state.cache = {}
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv("OPENAI_API_KEY", "")

# Clear cache on startup
if os.path.exists("vocab_cache.json"):
    os.remove("vocab_cache.json")

# Initialize OpenAI client with session state API key
client = OpenAI(
    api_key=st.session_state.api_key if st.session_state.api_key else os.getenv("OPENAI_API_KEY"),
    base_url="https://api.openai.com/v1"
)

class JapaneseVocabGenerator:
    def __init__(self):
        self.cache_file = "vocab_cache.json"
        self.cache = {}  # Start with empty cache

    def load_cache(self):
        """Load cached results from file"""
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                self.cache = json.load(f)
        except FileNotFoundError:
            self.cache = {}

    def save_cache(self):
        """Save cache to file"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)

    def get_cache_key(self, topic: str, jlpt_level: str, num_words: int) -> str:
        """Generate a cache key for the request"""
        return hashlib.md5(f"{topic}-{jlpt_level}-{num_words}".encode()).hexdigest()

    def transform_incorrect_format(self, words_list: List[Dict]) -> List[Dict]:
        """Transform incorrect format into correct format"""
        transformed = []
        for word in words_list:
            # Get the word text from either 'word' or 'kanji' field
            word_text = word.get('word', word.get('kanji', ''))
            
            # Get the meaning from either 'meaning' or 'english' field
            meaning = word.get('meaning', word.get('english', ''))
            
            # Get the romaji reading
            romaji = word.get('romaji', '')
            
            # Count kanji characters
            kanji_chars = [c for c in word_text if '\u4e00' <= c <= '\u9fff']
            
            # Create parts array for each kanji character
            parts = []
            for kanji in kanji_chars:
                parts.append({
                    "kanji": kanji,
                    "romaji": [romaji.split()[0]]  # Use first part of romaji as fallback
                })
            
            # Create properly structured word
            transformed_word = {
                "kanji": word_text,
                "romaji": romaji,
                "english": meaning,
                "parts": parts
            }
            transformed.append(transformed_word)
        
        return transformed

    def generate_vocab_group(self, topic: str, jlpt_level: str, num_words: int, force_refresh: bool = False) -> Dict:
        """Generate Japanese vocabulary words and their definitions using OpenAI API"""
        # Check cache first (unless force refresh is True)
        cache_key = self.get_cache_key(topic, jlpt_level, num_words)
        if not force_refresh and cache_key in self.cache:
            return {"words": self.cache[cache_key]}

        # Track API usage
        st.session_state.request_count += 1
        
        prompt = f"""Return EXACTLY this JSON structure with {num_words} words about {topic} at JLPT {jlpt_level} level.
CRITICAL: Break down EVERY word into its syllables, following these rules:
1. Single kanji with single reading: Keep as one part (e.g., 木 → ["ki"])
2. Compound kanji: Keep each kanji's full reading (e.g., 会社 → 会["kai"] + 社["sha"])
3. Words with kana: Split EVERY kana into its own part, using the actual kana character (e.g., 雨め → 雨["a"] + め["me"])
4. Words commonly written in kana: Use the kana form and split each character (e.g., 魚/さかな → さ["sa"] + か["ka"] + な["na"])
5. Adjectives: Split ALL parts including kana (e.g., 暑い → 暑["a"] + つ["tsu"] + い["i"])

EXAMPLE (COPY THIS STRUCTURE EXACTLY):
{{
  "words": [
    {{
      "kanji": "魚",
      "romaji": "sakana",
      "english": "fish",
      "parts": [
        {{
          "kanji": "さ",
          "romaji": ["sa"]
        }},
        {{
          "kanji": "か",
          "romaji": ["ka"]
        }},
        {{
          "kanji": "な",
          "romaji": ["na"]
        }}
      ]
    }},
    {{
      "kanji": "肉",
      "romaji": "niku",
      "english": "meat",
      "parts": [
        {{
          "kanji": "に",
          "romaji": ["ni"]
        }},
        {{
          "kanji": "く",
          "romaji": ["ku"]
        }}
      ]
    }}
  ]
}}

❌ DO NOT USE:
- "word" instead of "kanji"
- "meaning" instead of "english"
- "pos" or any other fields
- string instead of array for romaji in parts
- Do not combine multiple syllables in one romaji array
- Do not combine multiple kana into one part
- Do not use empty strings for kanji field
- Do not use kanji when the word is commonly written in kana

✅ REQUIRED:
- Root must be {{"words": [...]}}
- Each word must have: kanji, romaji, english, parts
- Break down EVERY word into ALL its syllables
- Each part must have "kanji" and "romaji" fields
- For kana parts, use the actual kana character in the "kanji" field
- Each romaji must be an array with ONE syllable per element
- For words commonly written in kana, use the kana form in parts
- Break down words following these patterns:
  * Single kanji, single syllable (木 → 木[ki])
  * Single kanji + kana (雨め → 雨[a] + め[me])
  * Multiple kanji (天気 → 天[ten] + 気[ki])
  * Kanji + kana (食べる → 食[ta] + べ[be] + る[ru])
  * Pure kana (ひとつ → ひ[hi] + と[to] + つ[tsu])"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a Japanese vocabulary formatter that breaks down words into syllables.
CRITICAL: 
- Use EXACTLY these field names: "words", "kanji", "english", "romaji", "parts"
- Break down EVERY word into its proper syllables
- Each part must use "kanji" and "romaji" fields
- The "kanji" field must contain ONLY valid Japanese characters (kanji, hiragana, or katakana)
- For kana parts, ALWAYS use the actual kana character in the "kanji" field (e.g., め for "me", り for "ri")
- Never use empty strings or omit characters in the kanji field
- Each romaji array element must be ONE syllable
- Follow these patterns:
  * Single kanji, single syllable: 木 → parts: [{"kanji": "木", "romaji": ["ki"]}]
  * Single kanji + kana: 雨め → parts: [{"kanji": "雨", "romaji": ["a"]}, {"kanji": "め", "romaji": ["me"]}]
  * Multiple kanji: 天気 → parts: [{"kanji": "天", "romaji": ["ten"]}, {"kanji": "気", "romaji": ["ki"]}]
  * Mixed kanji-kana: 食べる → parts: [{"kanji": "食", "romaji": ["ta"]}, {"kanji": "べ", "romaji": ["be"]}, {"kanji": "る", "romaji": ["ru"]}]
  * Pure kana: ひとつ → parts: [{"kanji": "ひ", "romaji": ["hi"]}, {"kanji": "と", "romaji": ["to"]}, {"kanji": "つ", "romaji": ["tsu"]}]"""
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            raw_response = response.choices[0].message.content
            
            try:
                result = json.loads(raw_response)
                
                # Ensure we have a words array at root
                if not isinstance(result, dict) or "words" not in result:
                    raise ValueError("Response must have a 'words' array at root level")
                
                if not isinstance(result["words"], list):
                    raise ValueError("'words' must be an array")
                
                if len(result["words"]) != num_words:
                    raise ValueError(f"Expected {num_words} words, got {len(result['words'])}")
                
                # Validate each word
                for word in result["words"]:
                    # Check for incorrect field names
                    if "word" in word or "meaning" in word or "pos" in word:
                        raise ValueError("Invalid field names found. Use 'kanji' and 'english' instead of 'word' and 'meaning'")
                    
                    # Validate word structure
                    required_fields = {"kanji", "romaji", "english", "parts"}
                    if set(word.keys()) != required_fields:
                        raise ValueError(f"Word must have exactly these fields: {required_fields}")
                    
                    if not isinstance(word["parts"], list):
                        raise ValueError("'parts' must be an array")
                    
                    # Validate each part
                    for part in word["parts"]:
                        if not isinstance(part, dict):
                            raise ValueError(f"Each part must be an object, got {type(part)}")
                        
                        # Check for required fields
                        if "kanji" not in part:
                            raise ValueError(f"Missing 'kanji' field in part: {part}")
                        if "romaji" not in part:
                            raise ValueError(f"Missing 'romaji' field in part: {part}")
                        
                        # Validate romaji array
                        if not isinstance(part["romaji"], list):
                            raise ValueError(f"'romaji' must be an array, got {type(part['romaji'])} in part: {part}")
                        
                        # Validate romaji elements
                        if not all(isinstance(r, str) for r in part["romaji"]):
                            raise ValueError(f"Each romaji element must be a string in part: {part}")
                        
                        # Validate kanji field
                        if not isinstance(part["kanji"], str):
                            raise ValueError(f"'kanji' field must be a string, got {type(part['kanji'])} in part: {part}")
                        
                        if not part["kanji"].strip():
                            raise ValueError(f"'kanji' field cannot be empty or whitespace in part: {part}")
                        
                        # Check for valid Japanese characters
                        for char in part["kanji"]:
                            is_kanji = '\u4e00' <= char <= '\u9fff'
                            is_hiragana = '\u3040' <= char <= '\u309f'
                            is_katakana = '\u30a0' <= char <= '\u30ff'
                            
                            if not (is_kanji or is_hiragana or is_katakana):
                                raise ValueError(f"Invalid character '{char}' in kanji field. Must be kanji, hiragana, or katakana. Part: {part}")
                        
                        # Print debug info for the part that passed validation
                        print(f"Validated part: {part}")
                
                # Cache the validated result
                self.cache[cache_key] = result["words"]
                self.save_cache()
                
                return result
                
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON response: {str(e)}")
                
        except Exception as e:
            st.error(f"Error generating vocabulary: {str(e)}")
            raise Exception(f"Failed to generate vocabulary: {str(e)}")

def save_vocab_to_json(vocab_data: List[Dict], filename: str):
    """Save vocabulary data to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(vocab_data, f, indent=2, ensure_ascii=False)

def load_vocab_from_json(filename: str) -> List[Dict]:
    """Load vocabulary data from a JSON file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# Streamlit UI
st.title("Japanese Vocabulary Generator and Manager")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI API Key", 
                           value=st.session_state.api_key,
                           type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.session_state.api_key = api_key
        client.api_key = api_key
        
    if not api_key:
        st.warning("Please enter your OpenAI API key to use the app")
    
    st.divider()
    st.subheader("Usage Statistics")
    st.write(f"Requests made: {st.session_state.request_count}")
    estimated_cost = st.session_state.request_count * 0.001  # $0.001 per request for GPT-3.5-turbo
    st.write(f"Estimated cost: ${estimated_cost:.3f}")
    
    if st.session_state.request_count >= 50:  # Standard limit for GPT-3.5-turbo
        st.warning("Usage limit reached. Please contact administrator.")

# Main content
tab1, tab2 = st.tabs(["Generate Vocabulary", "Import/Export"])

# Generate Vocabulary Tab
with tab1:
    st.header("Generate New Vocabulary")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input("Topic", placeholder="e.g., Business, Technology, Nature")
    with col2:
        force_refresh = st.checkbox("Force Refresh", help="Ignore cache and generate new words")
    
    jlpt_level = st.selectbox(
        "JLPT Level",
        ["N5 (Beginner)", "N4 (Basic)", "N3 (Intermediate)", "N2 (Advanced)", "N1 (Expert)"]
    )
    num_words = st.number_input("Number of Words", min_value=1, max_value=10, value=5,
                               help="Limit: 10 words per request to control costs")
    
    if st.button("Generate Vocabulary", type="primary", 
                 disabled=st.session_state.request_count >= 50):
        if not os.getenv("OPENAI_API_KEY"):
            st.error("Please enter your OpenAI API key in the sidebar.")
        else:
            with st.spinner("Generating vocabulary..."):
                generator = JapaneseVocabGenerator()
                try:
                    vocab_data = generator.generate_vocab_group(topic, jlpt_level, num_words, force_refresh)
                    st.success("Vocabulary generated successfully!")
                    
                    # Show Raw JSON Output with words wrapper
                    st.code(json.dumps(vocab_data, indent=2, ensure_ascii=False), language="json")
                    
                    # Download button - use the full structure
                    st.download_button(
                        label="Download as JSON",
                        data=json.dumps(vocab_data, indent=2, ensure_ascii=False),
                        file_name=f"vocab_japanese_{topic.split(' (')[0].lower().replace(' ', '_')}_{jlpt_level.split(' ')[0].lower()}.json",
                        mime="application/json"
                    )
                except Exception as e:
                    st.error(f"Error generating vocabulary: {str(e)}")

# Import/Export Tab
with tab2:
    st.header("Import/Export Vocabulary")
    
    # File uploader
    uploaded_file = st.file_uploader("Import JSON file", type="json")
    if uploaded_file:
        try:
            vocab_data = json.load(uploaded_file)
            st.success("File imported successfully!")
            df = pd.DataFrame(vocab_data)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error importing file: {str(e)}")
    
    # List existing vocabulary files
    st.subheader("Existing Vocabulary Files")
    vocab_files = list(Path(".").glob("vocab_*.json"))
    if vocab_files:
        for file in vocab_files:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(file.name)
            with col2:
                if st.button("Load", key=str(file)):
                    vocab_data = load_vocab_from_json(str(file))
                    df = pd.DataFrame(vocab_data)
                    st.dataframe(df) 