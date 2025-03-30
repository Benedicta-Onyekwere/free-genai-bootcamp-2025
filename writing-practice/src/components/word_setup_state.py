import streamlit as st
from services.word_data import get_random_word, get_word_by_level

def word_setup_state():
    """Setup state for word practice."""
    st.subheader("Kanji Word Practice Setup")
    
    # JLPT Level selection
    level = st.selectbox(
        "Select JLPT Level",
        ["N5", "N4", "N3", "N2", "N1"],
        index=0
    )
    
    # Practice history section
    st.subheader("Practice History")
    
    # Add delete history button
    if st.session_state.word_practice_history:
        if st.button("Delete History", key="delete_history"):
            st.session_state.word_practice_history = []
            st.rerun()
        
        for word in st.session_state.word_practice_history:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"Kanji: {word['kanji']}")
            with col2:
                st.write(f"Reading: {word['reading']}")
            with col3:
                st.write(f"Grade: {word.get('grade', 'Not graded')}")
    
    # Get Word button
    if st.button("Get Word"):
        word = get_word_by_level(level) or get_random_word()
        st.session_state.kanji_word = word
        st.session_state.word_app_state = "practice"
        st.rerun() 