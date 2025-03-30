import streamlit as st
from PIL import Image
import io

def word_practice_state():
    """Practice state for kanji word writing."""
    if not st.session_state.kanji_word:
        st.session_state.word_app_state = "setup"
        st.rerun()
        
    st.subheader("Write the reading for this kanji")
    
    # Display the kanji prominently
    st.markdown(f"## {st.session_state.kanji_word['kanji']}")
    st.markdown("---")
    
    # Input methods
    input_method = st.radio(
        "Choose input method:",
        ["Type", "Upload handwriting"]
    )
    
    if input_method == "Type":
        user_input = st.text_input("Enter the reading in hiragana:")
        if user_input:
            st.session_state.transcribed_text = user_input
            
    else:  # Upload handwriting
        uploaded_file = st.file_uploader("Upload your handwritten answer", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded handwriting", use_column_width=True)
            
            # Here you would process the image with OCR
            # For now, we'll just store the image
            st.session_state.transcribed_text = "OCR_PLACEHOLDER"
    
    # Submit button
    if st.button("Submit"):
        if st.session_state.transcribed_text:
            st.session_state.word_app_state = "review"
            st.rerun()
        else:
            st.error("Please provide your answer before submitting.") 