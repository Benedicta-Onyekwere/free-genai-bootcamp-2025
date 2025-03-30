import streamlit as st
from services.sentence_generator import generate_sentence

def review_state():
    """Review state component showing grading results."""
    # Display original sentence
    st.write("### English Sentence")
    st.write(st.session_state.current_sentence)
    
    # Display review results
    st.write("### Review Results")
    results = st.session_state.review_results
    
    st.write("#### Transcription")
    st.write(results['transcription'])
    
    st.write("#### Translation")
    st.write(results['translation'])
    
    st.write("#### Grading")
    st.write(f"Score: {results['grade']}")
    st.write("Feedback:")
    st.write(results['feedback'])
    
    # Next question button
    if st.button("Next Question"):
        # Generate new sentence
        sentence = generate_sentence()
        st.session_state.current_sentence = sentence
        # Clear review results
        st.session_state.review_results = None
        # Transition to practice state
        st.session_state.app_state = 'practice'
        st.rerun() 