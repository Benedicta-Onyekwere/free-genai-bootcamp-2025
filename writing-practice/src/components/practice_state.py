import streamlit as st
from services.grading_system import grade_submission

def practice_state():
    """Practice state component with sentence display and image upload."""
    st.write("### English Sentence")
    st.write(st.session_state.current_sentence)
    
    st.write("### Upload your written Japanese")
    uploaded_file = st.file_uploader("Upload your handwritten answer", type=['png', 'jpg', 'jpeg'])
    
    if st.button("Submit for Review"):
        if uploaded_file is not None:
            # Process the submission and get grading results
            results = grade_submission(uploaded_file)
            # Store results in session state
            st.session_state.review_results = results
            # Transition to review state
            st.session_state.app_state = 'review'
            st.rerun()
        else:
            st.error("Please upload an image before submitting.") 