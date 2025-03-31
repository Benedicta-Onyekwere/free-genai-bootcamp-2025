import streamlit as st
import openai
import os
from datetime import datetime

def generate_text(practice_type):
    try:
        # Set the API key for OpenAI v0.28.0
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        
        if practice_type == "Word":
            prompt = """Generate a single English word that would be appropriate for a beginner Japanese student to translate, along with its correct Japanese translation.
            Return in the format:
            English: [word]
            Japanese: [translation]"""
        else:  # Sentence
            prompt = """Generate a simple English sentence that would be appropriate for a beginner Japanese student to translate, along with its correct Japanese translation.
            Return in the format:
            English: [sentence]
            Japanese: [translation]"""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Japanese language teacher generating English text and Japanese translations for practice."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse the response to extract English and Japanese parts
        content = response.choices[0].message['content'].strip()
        lines = content.split('\n')
        english_text = ""
        expected_japanese = ""
        
        for line in lines:
            if line.startswith('English:'):
                english_text = line.replace('English:', '').strip()
            elif line.startswith('Japanese:'):
                expected_japanese = line.replace('Japanese:', '').strip()
        
        return english_text, expected_japanese
    except Exception as e:
        st.error(f"Error generating text: {str(e)}")
        return None, None

def setup_state():
    """Setup state component with practice type selection and generate button."""
    st.header("Setup")
    
    # Initialize all required session state variables if not present
    if 'current_practice_type' not in st.session_state:
        st.session_state.current_practice_type = "Sentence"
    if 'practice_history' not in st.session_state:
        st.session_state.practice_history = []
    if 'current_practice_item' not in st.session_state:
        st.session_state.current_practice_item = None
    if 'english_text' not in st.session_state:
        st.session_state.english_text = None
    if 'expected_japanese' not in st.session_state:
        st.session_state.expected_japanese = None
    if 'transcribed_text' not in st.session_state:
        st.session_state.transcribed_text = None
    if 'translation' not in st.session_state:
        st.session_state.translation = None
    if 'grade' not in st.session_state:
        st.session_state.grade = None
    if 'grade_recorded' not in st.session_state:
        st.session_state.grade_recorded = False
    
    # Practice type selection
    selected_type = st.radio(
        "Choose practice type:",
        ["Word", "Sentence"]
    )
    
    # If practice type changed, clear current practice item
    if selected_type != st.session_state.current_practice_type:
        st.session_state.current_practice_type = selected_type
        st.session_state.current_practice_item = None
        st.session_state.english_text = None
        st.session_state.expected_japanese = None
        st.session_state.transcribed_text = None
        st.session_state.translation = None
        st.session_state.grade = None
        st.session_state.grade_recorded = False
    
    # Filter practice history based on practice type
    filtered_history = [item for item in st.session_state.practice_history 
                       if isinstance(item, dict) and item.get('type') == selected_type]
    
    # If there are items in practice history, show them first
    if filtered_history:
        st.subheader("Practice History")
        st.write(f"These {selected_type.lower()}s need more practice:")
        
        for item in filtered_history:
            text = item.get('text', '')
            if st.button(f"Practice: {text}", key=f"practice_{text}"):
                # Clear previous state
                st.session_state.transcribed_text = None
                st.session_state.translation = None
                st.session_state.grade = None
                st.session_state.grade_recorded = False
                
                # Set new practice item
                st.session_state.english_text = text
                st.session_state.expected_japanese = item.get('expected_japanese')
                st.session_state.current_practice_item = item
                st.session_state.app_state = "practice"
                st.rerun()
        
        st.divider()
        st.subheader(f"Or Generate a New {selected_type}")
    
    button_label = f"Generate New {selected_type}"
    if st.button(button_label):
        with st.spinner(f"Generating {selected_type.lower()}..."):
            english_text, expected_japanese = generate_text(selected_type)
            if english_text and expected_japanese:
                # Clear previous state
                st.session_state.transcribed_text = None
                st.session_state.translation = None
                st.session_state.grade = None
                st.session_state.grade_recorded = False
                
                # Set new practice item
                english_text = english_text.strip()
                expected_japanese = expected_japanese.strip()
                
                st.session_state.english_text = english_text
                st.session_state.expected_japanese = expected_japanese
                st.session_state.current_practice_item = {
                    'text': english_text,
                    'type': selected_type,
                    'expected_japanese': expected_japanese,
                    'timestamp': datetime.now().isoformat()
                }
                st.session_state.app_state = "practice"
                st.rerun() 