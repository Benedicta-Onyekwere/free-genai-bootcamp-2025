from typing import List, Dict
from pydantic import BaseModel, Field
import ollama
import os
import re
import json

class WordPart(BaseModel):
    """Model for a word part (kanji/kana character and its reading)."""
    kanji: str
    romaji: List[str]

class VocabularyItem(BaseModel):
    """Model for a vocabulary item with full word info and its parts."""
    kanji: str
    romaji: str
    english: str
    parts: List[WordPart] = Field(description="Breakdown of word parts with readings")

class VocabularyResponse(BaseModel):
    """Model for the complete vocabulary response."""
    vocabulary: List[VocabularyItem]

def load_prompt(filename: str) -> str:
    """Load prompt template from file."""
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                              'prompts', filename)
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def split_lyrics_into_chunks(lyrics: str, max_chars: int = 500) -> List[str]:
    """
    Split lyrics into manageable chunks while preserving sentence boundaries.
    
    Args:
        lyrics (str): Full lyrics text
        max_chars (int): Maximum characters per chunk
        
    Returns:
        List[str]: List of lyrics chunks
    """
    # Split by sentence endings (。, ！, ？) or line breaks
    sentences = re.split(r'([。！？\n])', lyrics)
    chunks = []
    current_chunk = ""
    
    for i in range(0, len(sentences), 2):
        sentence = sentences[i]
        # Add the sentence ending punctuation back if it exists
        if i + 1 < len(sentences):
            sentence += sentences[i + 1]
            
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence
            
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

async def extract_vocabulary(lyrics: str, language: str = "japanese") -> List[Dict]:
    """
    Extract vocabulary from lyrics using Ollama.
    
    Args:
        lyrics (str): Song lyrics text
        language (str): Target language for vocabulary extraction (currently supports Japanese)
        
    Returns:
        List[Dict]: List of vocabulary items with kanji, romaji, meanings, and part breakdowns
    """
    try:
        # Load prompt template
        prompt_template = load_prompt('Extract-Vocabulary.md')
        
        # Split lyrics into manageable chunks
        chunks = split_lyrics_into_chunks(lyrics)
        all_vocabulary = []
        
        # Process each chunk
        for chunk in chunks:
            # Add lyrics chunk to prompt
            prompt = f"{prompt_template}\n\nLyrics:\n{chunk}"

            # Get response from Ollama
            response = await ollama.chat(
                model="mistral",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a Japanese language expert that breaks down words into their components.
                        You MUST extract EVERY meaningful word from the lyrics, not just a sample.
                        ALWAYS follow these rules:
                        - Use EXACT field names: kanji, romaji, english, parts
                        - Break EVERY word into its proper parts
                        - Use actual Japanese characters in kanji field
                        - Each romaji array should contain ONE syllable
                        - Include ALL parts of the word
                        - Process EVERY word in the given text
                        - Ensure romaji is 100% accurate following Hepburn romanization"""
                    },
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Parse the JSON response
            try:
                response_text = response['message']['content']
                # Extract the JSON part from the response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    vocab_data = json.loads(json_str)
                    # Validate with Pydantic
                    vocab_response = VocabularyResponse(**vocab_data)
                    all_vocabulary.extend([item.model_dump() for item in vocab_response.vocabulary])
            except Exception as e:
                print(f"Error parsing response: {e}")
                continue
        
        # Remove duplicates while preserving order
        seen = set()
        unique_vocabulary = []
        for item in all_vocabulary:
            item_key = (item['kanji'], item['romaji'], item['english'])
            if item_key not in seen:
                seen.add(item_key)
                unique_vocabulary.append(item)
        
        return unique_vocabulary

    except Exception as e:
        print(f"Error extracting vocabulary: {e}")
        return [] 