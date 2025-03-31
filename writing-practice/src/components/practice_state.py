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
    1. English text to translate (word or sentence)
    2. Instructions for writing Japanese translation
    3. Option to either upload image or type/paste Japanese text
    """
    st.header("Practice")
    
    practice_type = st.session_state.get('current_practice_type', 'Sentence')
    st.subheader(f"English {practice_type}")
    if st.session_state.english_text:
        st.write(st.session_state.english_text)
        
    st.subheader("Write the Japanese Translation")
    if practice_type == "Word":
        st.write("""
        Your grade will be based on:
        - Correct Japanese word choice
        - Appropriate kanji usage (if applicable)
        - Correct spelling/writing
        """)
    else:
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
        st.write(f"Enter your Japanese translation below:")
        japanese_text = st.text_area("Japanese translation", height=100 if practice_type == "Sentence" else 50)
        
        if st.button("Submit Translation"):
            if japanese_text.strip():
                st.session_state.transcribed_text = japanese_text
                st.session_state.app_state = "review"
                st.rerun()
            else:
                st.error("Please enter your translation before submitting.")
    
    else:  # Upload handwritten image
        st.write(f"""
        Instructions for handwritten submission:
        1. Write the Japanese translation of the English {practice_type.lower()} above on paper
        2. Take a clear photo of your handwritten Japanese
        3. Upload the photo below
        """)
        
        # Container for file uploader and image
        with st.container():
            uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
            
            if uploaded_file is not None:
                try:
                    # Display the uploaded image
                    image_bytes = uploaded_file.read()
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    # Calculate width to make it more compact
                    width = 400  # You can adjust this value
                    aspect_ratio = image.size[1] / image.size[0]
                    height = int(width * aspect_ratio)
                    
                    # Resize image while maintaining aspect ratio
                    image_resized = image.resize((width, height))
                    
                    # Convert back to bytes
                    img_byte_arr = io.BytesIO()
                    image_resized.save(img_byte_arr, format=image.format)
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    # Display image without caption and with custom width
                    st.image(img_byte_arr)
                    
                    if st.button("Submit for Review"):
                        if ocr is None:
                            st.error("OCR system is not available. Please use text input instead.")
                            return
                            
                        with st.spinner("Processing image..."):
                            # Process the image with OCR
                            text = ocr(image)  # Use original image for OCR
                            st.session_state.transcribed_text = text
                            st.session_state.app_state = "review"
                            st.rerun()
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")
    
    if st.button("Back to Setup"):
        st.session_state.app_state = "setup"
        st.session_state.english_text = None
        st.rerun() 