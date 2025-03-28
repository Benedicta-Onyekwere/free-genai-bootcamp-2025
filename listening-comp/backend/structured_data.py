import openai
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
import os
import json
import datetime

# Load environment variables from .env file
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

class TranscriptStructurer:
    def __init__(self):
        """Initialize the transcript structurer."""
        self.system_prompt = """You are a helpful assistant that structures Japanese transcripts into practice questions.
For each transcript segment, create questions that test listening comprehension.
DO NOT translate the Japanese text to English - keep it in Japanese with kanji/hiragana/katakana.
Include romaji for pronunciation help.
Format your response as a JSON array of question objects."""

    def structure_transcript(self, transcript_text: str) -> List[Dict]:
        """Structure the transcript into practice questions."""
        try:
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("""OpenAI API key not found in environment variables.
Please make sure you have created a .env file with your API key:
OPENAI_API_KEY=your-api-key-here""")

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Please structure this transcript into practice questions:\n\n{transcript_text}"}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse the response into JSON
            response_text = response.choices[0].message['content'].strip()
            
            # Remove markdown code block if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]  # Remove ```json
            if response_text.startswith("```"):
                response_text = response_text[3:]  # Remove ```
            if response_text.endswith("```"):
                response_text = response_text[:-3]  # Remove trailing ```
                
            response_text = response_text.strip()
            
            try:
                structured_data = json.loads(response_text)
                if not isinstance(structured_data, list):
                    raise ValueError("Response was not a JSON array")
                return structured_data
            except json.JSONDecodeError:
                return [{"error": "Failed to parse response as JSON", "raw_response": response_text}]
                
        except Exception as e:
            return [{"error": f"Error structuring transcript: {str(e)}"}]

    def save_transcript(self, transcript_text: str, filename: str) -> bool:
        """Save raw transcript to a file"""
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(transcript_text)
            return True
        except Exception as e:
            print(f"Error saving transcript: {str(e)}")
            return False

    def save_structured_data(self, structured_data: List[Dict], filename: str) -> bool:
        """Save structured data to a JSON file"""
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(structured_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving structured data: {str(e)}")
            return False

    def save_questions(self, structured_text: str, filename: str) -> bool:
        """Save structured questions to a file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(structured_text)
            return True
        except Exception as e:
            print(f"Error saving questions: {str(e)}")
            return False

    def load_transcript(self, filename: str) -> Optional[str]:
        """Load structured questions from a file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading questions: {str(e)}")
            return None

    def count_characters(self, text: str) -> Tuple[int, int]:
        """Count Japanese and total characters in text."""
        if not text:
            return 0, 0
            
        def is_japanese(char):
            return any([
                '\u4e00' <= char <= '\u9fff',  # Kanji
                '\u3040' <= char <= '\u309f',  # Hiragana
                '\u30a0' <= char <= '\u30ff',  # Katakana
            ])
        
        jp_chars = sum(1 for char in text if is_japanese(char))
        return jp_chars, len(text)

if __name__ == "__main__":
    # Sample transcript for testing
    sample_transcript = """
    1番
    男の人は図書館で勉強しています。女の人が話しかけます。
    女：すみません、この席空いてますか。
    男：はい、どうぞ。
    女：ありがとうございます。あの、ペンを借りてもいいですか。
    男：はい、どうぞ。
    ナレーター：女の人は何をしますか。

    2番
    レストランで男の人と女の人が話しています。
    女：このレストラン、初めて来たんですけど、何がおすすめですか。
    男：そうですね。魚料理がとても美味しいですよ。特にサーモンがおすすめです。
    女：そうですか。じゃあ、それにしようかな。
    ナレーター：女の人は何を注文しようと思っていますか。
    """

    # Create timestamp for unique filenames
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Initialize structurer
    structurer = TranscriptStructurer()
    
    # Save raw transcript
    transcript_path = os.path.join(os.path.dirname(__file__), "transcripts", f"test_transcript_{timestamp}.txt")
    if structurer.save_transcript(sample_transcript, transcript_path):
        print(f"Raw transcript saved to: {transcript_path}")
    
    # Structure and save the data
    structured_data = structurer.structure_transcript(sample_transcript)
    structured_path = os.path.join(os.path.dirname(__file__), "transcripts", f"structured_transcript_{timestamp}.json")
    if structurer.save_structured_data(structured_data, structured_path):
        print(f"Structured data saved to: {structured_path}")
    
    print("\nStructured Data Preview:")
    print(json.dumps(structured_data, ensure_ascii=False, indent=2))