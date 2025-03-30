import streamlit as st
from components.word_setup_state import word_setup_state
from components.word_practice_state import word_practice_state
from components.word_review_state import word_review_state

def main():
    # Initialize session state variables with distinct names
    if "word_app_state" not in st.session_state:
        st.session_state.word_app_state = "setup"
    if "kanji_word" not in st.session_state:
        st.session_state.kanji_word = None
    if "transcribed_text" not in st.session_state:
        st.session_state.transcribed_text = None
    if "word_grade" not in st.session_state:
        st.session_state.word_grade = None
    if "word_practice_history" not in st.session_state:
        st.session_state.word_practice_history = []

    # Title with distinct branding
    st.title("Japanese Writing Practice")
    
    # State management with distinct state names
    if st.session_state.word_app_state == "setup":
        word_setup_state()
    elif st.session_state.word_app_state == "practice":
        word_practice_state()
    elif st.session_state.word_app_state == "review":
        word_review_state()

if __name__ == "__main__":
    main() 