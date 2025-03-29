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

# OpenAI model
MODEL_ID = "gpt-3.5-turbo"

class TranscriptStructurer:
    def __init__(self, model_id: str = MODEL_ID):
        """Initialize the transcript structurer with OpenAI."""
        self.model_id = model_id
        self.prompts = {
            1: """Extract questions from section 問題1 of this JLPT transcript where the answer can be determined solely from the conversation without needing visual aids.
            
            ONLY include questions that meet these criteria:
            - The answer can be determined purely from the spoken dialogue
            - No spatial/visual information is needed (like locations, layouts, or physical appearances)
            - No physical objects or visual choices need to be compared
            
            For example, INCLUDE questions about:
            - Times and dates
            - Numbers and quantities
            - Spoken choices or decisions
            - Clear verbal directions
            
            DO NOT include questions about:
            - Physical locations that need a map or diagram
            - Visual choices between objects
            - Spatial arrangements or layouts
            - Physical appearances of people or things

            Format each question exactly like this:
 
            <question>
            Introduction:
            [the situation setup in japanese]
            
            Conversation:
            [the dialogue in japanese]
            
            Question:
            [the question being asked in japanese]

            Options:
            1. [first option in japanese]
            2. [second option in japanese]
            3. [third option in japanese]
            4. [fourth option in japanese]
            </question>

            Rules:
            - Only extract questions from the 問題1 section
            - Only include questions where answers can be determined from dialogue alone
            - Ignore any practice examples (marked with 例)
            - Do not translate any Japanese text
            - Do not include any section descriptions or other text
            - Output questions one after another with no extra text between them""",

            2: """Extract questions from section 問題2 of this JLPT transcript where the answer can be determined solely from the conversation without needing visual aids.
            
            ONLY include questions that meet these criteria:
            - The answer can be determined purely from the spoken dialogue
            - No spatial/visual information is needed (like locations, layouts, or physical appearances)
            - No physical objects or visual choices need to be compared
            
            For example, INCLUDE questions about:
            - Times and dates
            - Numbers and quantities
            - Spoken choices or decisions
            - Clear verbal directions
            
            DO NOT include questions about:
            - Physical locations that need a map or diagram
            - Visual choices between objects
            - Spatial arrangements or layouts
            - Physical appearances of people or things

            Format each question exactly like this:
 
            <question>
            Introduction:
            [the situation setup in japanese]
            
            Conversation:
            [the dialogue in japanese]
            
            Question:
            [the question being asked in japanese]

            Options:
            1. [first option in japanese]
            2. [second option in japanese]
            3. [third option in japanese]
            4. [fourth option in japanese]
            </question>

            Rules:
            - Only extract questions from the 問題2 section
            - Only include questions where answers can be determined from dialogue alone
            - Ignore any practice examples (marked with 例)
            - Do not translate any Japanese text
            - Do not include any section descriptions or other text
            - Output questions one after another with no extra text between them""",

            3: """Extract all questions from section 問題3 of this JLPT transcript.
            Format each question exactly like this:
 
            <question>
            Situation:
            [the situation in japanese where a phrase is needed]
            
            Question:
            何と言いますか

            Options:
            1. [first option in japanese]
            2. [second option in japanese]
            3. [third option in japanese]
            4. [fourth option in japanese]
            </question>
 
            Rules:
            - Only extract questions from the 問題3 section
            - Ignore any practice examples (marked with 例)
            - Do not translate any Japanese text
            - Do not include any section descriptions or other text
            - Output questions one after another with no extra text between them"""
        }

    def structure_transcript(self, transcript_text: str) -> Dict[int, str]:
        """Structure the transcript into sections using separate prompts."""
        results = {}
        
        try:
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("""OpenAI API key not found in environment variables.
Please make sure you have created a .env file with your API key:
OPENAI_API_KEY=your-api-key-here""")

            # Process each section
            for section_num in range(1, 4):
                response = openai.ChatCompletion.create(
                    model=self.model_id,
                    messages=[
                        {"role": "system", "content": self.prompts[section_num]},
                        {"role": "user", "content": f"Please structure this transcript into practice questions:\n\n{transcript_text}"}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                # Get the response text
                response_text = response.choices[0].message['content'].strip()
                results[section_num] = response_text
                
        except Exception as e:
            print(f"Error structuring transcript: {str(e)}")
            return {}
            
        return results

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

    def save_questions(self, structured_sections: Dict[int, str], base_filename: str) -> bool:
        """Save each section to a separate file"""
        try:
            # Create questions directory if it doesn't exist
            os.makedirs(os.path.dirname(base_filename), exist_ok=True)
            
            # Save each section
            for section_num, content in structured_sections.items():
                filename = f"{os.path.splitext(base_filename)[0]}_section{section_num}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
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
    structurer = TranscriptStructurer()
    transcript = structurer.load_transcript("backend/data/transcripts/sY7L5cfCWno.txt")
    if transcript:
        structured_sections = structurer.structure_transcript(transcript)
        structurer.save_questions(structured_sections, "backend/data/questions/sY7L5cfCWno.txt")