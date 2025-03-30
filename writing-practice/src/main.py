import streamlit as st
from components.setup_state import setup_state
from components.practice_state import practice_state
from components.review_state import review_state
from services.sentence_generator import generate_sentence
from services.grading_system import grade_submission
import json

# Initialize session state
if 'app_state' not in st.session_state:
    st.session_state.app_state = 'setup'
if 'current_sentence' not in st.session_state:
    st.session_state.current_sentence = ''
if 'words_collection' not in st.session_state:
    # TODO: Implement API call to fetch words
    st.session_state.words_collection = []

st.title("Japanese Writing Practice")

# State management
if st.session_state.app_state == 'setup':
    setup_state()
elif st.session_state.app_state == 'practice':
    practice_state()
elif st.session_state.app_state == 'review':
    review_state() 