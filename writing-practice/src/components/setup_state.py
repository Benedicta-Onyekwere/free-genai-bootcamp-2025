import streamlit as st
from services.sentence_generator import generate_sentence

def setup_state():
    """Setup state component with Generate Sentence button."""
    if st.button("Generate Sentence"):
        # Generate a sentence and store it
        sentence = generate_sentence()
        st.session_state.current_sentence = sentence
        # Transition to practice state
        st.session_state.app_state = 'practice'
        st.rerun() 