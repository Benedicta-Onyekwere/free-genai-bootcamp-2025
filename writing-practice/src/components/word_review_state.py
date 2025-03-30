import streamlit as st

def word_review_state():
    """Review state for grading kanji word practice."""
    if not st.session_state.kanji_word or not st.session_state.transcribed_text:
        st.session_state.word_app_state = "setup"
        st.rerun()

    st.subheader("Review")
    
    # Display the practice details
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Kanji")
        st.markdown(f"## {st.session_state.kanji_word['kanji']}")
    with col2:
        st.markdown("### Your Answer")
        st.write(st.session_state.transcribed_text)
    
    # Grade the answer
    correct_reading = st.session_state.kanji_word["reading"].strip()
    user_answer = st.session_state.transcribed_text.strip()
    
    # Compare the stripped strings for exact match
    is_correct = user_answer == correct_reading
    
    if is_correct:
        grade = "correct"
        feedback = "Perfect match!"
    else:
        grade = "incorrect"
        feedback = "Try again! Practice makes perfect."
    
    st.session_state.word_grade = {
        "grade": grade,
        "feedback": feedback
    }
    
    # Display grade and feedback
    st.markdown("### Grade")
    st.write(st.session_state.word_grade["grade"])
    st.markdown("### Feedback")
    st.write(st.session_state.word_grade["feedback"])
    
    # Add to practice history if not already present
    if st.session_state.kanji_word not in st.session_state.word_practice_history:
        history_entry = {
            **st.session_state.kanji_word,
            "grade": st.session_state.word_grade["grade"]
        }
        st.session_state.word_practice_history.append(history_entry)
    
    # Buttons for next actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Try Again"):
            st.session_state.transcribed_text = None
            st.session_state.word_grade = None
            st.session_state.word_app_state = "practice"
            st.rerun()
    
    with col2:
        if st.button("Show Answer"):
            st.info(f"The correct reading is: {correct_reading}")
    
    # Continue practicing button
    if st.button("Practice Another Word"):
        st.session_state.kanji_word = None
        st.session_state.transcribed_text = None
        st.session_state.word_grade = None
        st.session_state.word_app_state = "setup"
        st.rerun() 