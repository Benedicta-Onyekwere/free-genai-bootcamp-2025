import streamlit as st
from PIL import Image
from manga_ocr import MangaOcr
import io

# Initialize OCR once at module level
try:
    ocr = MangaOcr()
except Exception as e:
    ocr = None
    print(f"Warning: Could not initialize OCR: {str(e)}")

def practice_state():
    """Practice state component showing:
    1. English sentence to translate
    2. Instructions for writing Japanese translation
    3. Option to either upload image or type/paste Japanese text
    """
    st.header("Practice")
    
    st.subheader("English Sentence")
    if st.session_state.english_sentence:
        st.write(st.session_state.english_sentence)
        
    st.subheader("Write the Japanese Translation")
    st.write("""
    Your grade will be based on:
    - Whether your Japanese translation matches the meaning of the English sentence
    - Grammar accuracy
    - Natural Japanese usage
    """)
    
    # Add input method selection
    input_method = st.radio(
        "Choose how to submit your translation:",
        ["Type or paste text", "Upload handwritten image"]
    )
    
    if input_method == "Type or paste text":
        st.write("Enter your Japanese translation below:")
        japanese_text = st.text_area("Japanese translation", height=100)
        
        if st.button("Submit Translation"):
            if japanese_text.strip():
                st.session_state.transcribed_text = japanese_text
                st.session_state.app_state = "review"
                st.rerun()
            else:
                st.error("Please enter your translation before submitting.")
    
    else:  # Upload handwritten image
        st.write("""
        Instructions for handwritten submission:
        1. Write the Japanese translation of the English sentence above on paper
        2. Take a clear photo of your handwritten Japanese
        3. Upload the photo below
        """)
        
        uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
        
        if uploaded_file is not None:
            try:
                # Display the uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_container_width=True)
                
                if st.button("Submit for Review"):
                    if ocr is None:
                        st.error("OCR system is not available. Please use text input instead.")
                        return
                        
                    with st.spinner("Processing image..."):
                        # Process the image with OCR
                        text = ocr(image)
                        st.session_state.transcribed_text = text
                        st.session_state.app_state = "review"
                        st.rerun()
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
    
    if st.button("Back to Setup"):
        st.session_state.app_state = "setup"
        st.session_state.english_sentence = None
        st.rerun() 