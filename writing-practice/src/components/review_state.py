import streamlit as st
from services.sentence_generator import generate_sentence

def review_state():
    """Review state component showing:
    1. Original English sentence
    2. Transcription of Image
    3. Translation of Transcription
    4. Grade (S Rank score and description)
    5. Next Question button
    """
    st.header("Review")
    
    st.subheader("English Sentence")
    if st.session_state.english_sentence:
        st.write(st.session_state.english_sentence)
    
    st.subheader("Transcription of Image")
    if st.session_state.transcribed_text:
        st.write(st.session_state.transcribed_text)
    
    st.subheader("Translation of Transcription")
    if st.session_state.translation:
        st.write(st.session_state.translation)
    else:
        st.write("Generating translation...")
    
    st.subheader("Grading")
    if st.session_state.grade:
        # Split the grade response into lines and process each section
        sections = st.session_state.grade.split('\n\n')  # Split on double newlines to separate sections
        
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
        if st.session_state.english_sentence in st.session_state.practice_history:
            grade = None
            for line in st.session_state.grade.split('\n'):
                if line.startswith('Grade:'):
                    grade = line.split(':')[1].strip()
                    break
                    
            if grade in ['S', 'A']:
                st.success("Great job! This sentence has been mastered and will be removed from practice history.")
                st.session_state.practice_history.remove(st.session_state.english_sentence)
    else:
        if st.session_state.translation:
            st.write("Generating feedback...")
        else:
            st.write("Waiting for translation...")
    
    if st.button("Practice Again"):
        st.session_state.app_state = "setup"
        st.session_state.english_sentence = None
        st.session_state.transcribed_text = None
        st.session_state.translation = None
        st.session_state.grade = None
        st.rerun() 