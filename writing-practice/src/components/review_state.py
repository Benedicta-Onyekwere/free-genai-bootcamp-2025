import streamlit as st
import requests
from services.sentence_generator import generate_sentence

def review_state():
    """Review state component showing:
    1. Original English text (word or sentence)
    2. Your Japanese Translation
    3. Translation Check
    4. Grade (S Rank score and description)
    5. Next Question button
    """
    st.header("Review")
    
    # Initialize missing session state variables
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
    
    # Validate current practice item
    current_item = st.session_state.current_practice_item
    if not current_item or not isinstance(current_item, dict):
        st.error("No practice item found. Please start a new practice session.")
        if st.button("Back to Setup"):
            # Clear all practice-related session state
            for key in ['english_text', 'expected_japanese', 'current_practice_item', 
                       'transcribed_text', 'translation', 'grade', 'grade_recorded']:
                if key in st.session_state:
                    st.session_state[key] = None
            st.session_state.app_state = "setup"
            st.rerun()
        return
    
    # Ensure we have all required fields
    english_text = current_item.get('text')
    expected_japanese = current_item.get('expected_japanese')
    practice_type = current_item.get('type', 'Sentence')
    
    if not english_text or not expected_japanese:
        st.error("Missing practice text or expected translation. Please start a new practice session.")
        if st.button("Back to Setup"):
            # Clear all practice-related session state
            for key in ['english_text', 'expected_japanese', 'current_practice_item', 
                       'transcribed_text', 'translation', 'grade', 'grade_recorded']:
                if key in st.session_state:
                    st.session_state[key] = None
            st.session_state.app_state = "setup"
            st.rerun()
        return
    
    # Ensure session state matches current item
    if st.session_state.english_text != english_text or st.session_state.expected_japanese != expected_japanese:
        st.session_state.english_text = english_text
        st.session_state.expected_japanese = expected_japanese
        st.session_state.transcribed_text = None
        st.session_state.translation = None
        st.session_state.grade = None
        st.session_state.grade_recorded = False
    
    st.subheader(f"English {practice_type}")
    st.write(english_text)
    
    st.subheader("Your Japanese Translation")
    if st.session_state.transcribed_text:
        st.write(st.session_state.transcribed_text)
    else:
        st.info("No translation provided yet.")
    
    st.subheader("Translation Check")
    if st.session_state.translation:
        st.write(st.session_state.translation)
    else:
        st.write("Checking translation...")
    
    st.subheader("Grading")
    if st.session_state.grade:
        # Split the grade response into lines and process each section
        sections = st.session_state.grade.split('\n\n')  # Split on double newlines to separate sections
        
        # Extract grade for API
        grade_letter = None
        for section in sections:
            lines = section.strip().split('\n')
            for line in lines:
                if line.startswith('Grade:'):
                    grade_letter = line.split(':')[1].strip()
                    break
        
        # Send data to Flask backend
        if not st.session_state.get('grade_recorded', False):
            try:
                response = requests.post(
                    'http://localhost:5000/api/writing-practice',
                    json={
                        'english_text': english_text,
                        'practice_type': practice_type,
                        'japanese_text': st.session_state.transcribed_text,
                        'expected_japanese': expected_japanese,
                        'translation': st.session_state.translation,
                        'grade': grade_letter
                    }
                )
                if response.status_code == 201:
                    st.session_state.grade_recorded = True
            except requests.exceptions.RequestException as e:
                st.warning(f"Could not record practice data: {str(e)}")
        
        for section in sections:
            lines = section.strip().split('\n')
            for line in lines:
                if line.startswith('Grade:'):
                    st.write("Score:", line.split(':')[1].strip())
                elif line.startswith('Feedback:'):
                    st.write("\nFeedback:")
                    # Get everything after "Feedback:" and display it with proper formatting
                    feedback_text = ':'.join(line.split(':')[1:]).strip()
                    if feedback_text:
                        st.write(feedback_text)
                else:
                    # If it's not a grade line and doesn't start with Feedback:, it's part of the feedback
                    st.write(line.strip())
        
        # Handle practice history
        if english_text not in [item.get('text') for item in st.session_state.practice_history]:
            # Add to practice history
            st.session_state.practice_history.append(current_item)
        else:
            # Find and remove if mastered
            if grade_letter in ['S', 'A']:
                st.success(f"Great job! This {practice_type.lower()} has been mastered and will be removed from practice history.")
                st.session_state.practice_history = [
                    item for item in st.session_state.practice_history 
                    if item.get('text') != english_text
                ]
    else:
        if st.session_state.translation:
            st.write("Generating feedback...")
        else:
            st.write("Waiting for translation check...")
    
    if st.button("Practice Again"):
        # Clear all practice-related session state
        for key in ['english_text', 'expected_japanese', 'current_practice_item', 
                   'transcribed_text', 'translation', 'grade', 'grade_recorded']:
            if key in st.session_state:
                st.session_state[key] = None
        st.session_state.app_state = "setup"
        st.rerun() 