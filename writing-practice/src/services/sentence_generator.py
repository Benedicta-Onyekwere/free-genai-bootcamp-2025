import random
import openai
import streamlit as st

def generate_sentence():
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