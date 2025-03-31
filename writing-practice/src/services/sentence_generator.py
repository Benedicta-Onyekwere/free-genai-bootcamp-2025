import random
import openai
import streamlit as st
import requests
from typing import Dict, List

def fetch_vocabulary(group_id: str = "1") -> List[Dict[str, str]]:
    """Fetch Japanese vocabulary and translations from the API endpoint.
    
    Args:
        group_id (str): The group ID to fetch vocabulary for
    
    Returns:
        List[Dict[str, str]]: List of dictionaries containing Japanese words and their English translations
    """
    try:
        response = requests.get(f'http://localhost:5000/api/groups/{group_id}/raw')
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch vocabulary: {str(e)}")
        # Fallback mock data
        return [
            {"japanese": "食べる", "english": "to eat"},
            {"japanese": "飲む", "english": "to drink"},
            {"japanese": "行く", "english": "to go"},
            {"japanese": "見る", "english": "to see"},
            {"japanese": "読む", "english": "to read"}
        ]

def generate_sentence() -> str:
    """Generate a simple English sentence using JLPT N5 grammar and vocabulary from the API."""
    # Get vocabulary from API
    vocabulary = fetch_vocabulary()
    
    # Select a random word from vocabulary
    selected_word = random.choice(vocabulary)['english']
    
    # Prompt with correct spelling
    prompt = f"""Generate a simple sentence using the following word: {selected_word}
The grammar should be scoped to JLPT N5 grammar.
You can use the following vocabulary to construct a simple sentence:
- simple objects eg. book, car, ramen, sushi
- simple verbs, to drink, to eat, to meet
- simple times eg. tomorrow, today, yesterday"""

    try:
        # Set the API key
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        
        # Make the API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Japanese language teaching assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        st.error(f"Error generating sentence: {str(e)}")
        # Fallback to template-based sentence if LLM fails
        templates = [
            f"I will {selected_word} tomorrow.",
            f"She likes to {selected_word} every day.",
            f"They {selected_word} yesterday.",
        ]
        return random.choice(templates)

def generate_sentence_old():
    """Generate a simple English sentence using JLPT N5 grammar."""
    # Sample vocabulary (to be replaced with API call results)
    sample_words = ["book", "car", "ramen", "sushi", "drink", "eat", "meet"]
    selected_word = random.choice(sample_words)
    
    # LLM prompt as specified in Tech-Spec
    prompt = f"""Generate a simple sentence using the following word: {selected_word}
    The grammar should be scoped to JLPT N5 grammar.
    You can use the following vocabulary to construct a simple sentence:
    - simple objects eg. book, car, ramen, sushi
    - simple verbs, to drink, to eat, to meet
    - simple times eg. tomorrow, today, yesterday"""
    
    try:
        # TODO: Replace with actual OpenAI API call
        # For now, return a simple templated sentence
        templates = [
            f"I will {selected_word} tomorrow.",
            f"She likes to {selected_word} every day.",
            f"They {selected_word} yesterday.",
        ]
        return random.choice(templates)
    except Exception as e:
        st.error(f"Error generating sentence: {str(e)}")
        return "I eat sushi." # Default fallback sentence 