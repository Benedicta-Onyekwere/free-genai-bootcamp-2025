import streamlit as st
from PIL import Image
from manga_ocr import MangaOcr
import openai
import io

def grade_submission(image_file):
    """Process uploaded image and return grading results as per Tech-Spec:
    1. Transcribe image using MangaOCR
    2. Use LLM for literal translation
    3. Use LLM for grading with S Rank scoring
    4. Return data to frontend
    """
    try:
        st.info("Loading image...")
        # 1. Transcribe using MangaOCR
        # Convert StreamlitUploadedFile to PIL Image
        image_bytes = image_file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        st.info("Initializing OCR model...")
        mocr = MangaOcr()
        
        st.info("Transcribing text...")
        transcribed_text = mocr(image)
        
        if not transcribed_text:
            st.error("No text was detected in the image.")
            return None
            
        st.info("Translating text...")
        # 2. Use LLM for literal translation
        translation_prompt = f"Provide a literal translation of this Japanese text: {transcribed_text}"
        try:
            translation_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Japanese translator. Provide literal translations."},
                    {"role": "user", "content": translation_prompt}
                ]
            )
            translation = translation_response.choices[0].message.content.strip()
        except Exception as e:
            st.error(f"Translation error: {str(e)}")
            translation = "Error generating translation"
        
        st.info("Grading submission...")
        # 3. Use LLM for grading with S Rank scoring
        original_sentence = st.session_state.current_sentence
        grading_prompt = f"""Grade this Japanese translation:
Original English: {original_sentence}
Student's Japanese: {transcribed_text}
Literal Translation: {translation}

Provide:
1. A letter score using the S Rank system
2. A description of whether the attempt was accurate to the English sentence and suggestions."""
        
        try:
            grading_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Japanese language grading assistant."},
                    {"role": "user", "content": grading_prompt}
                ]
            )
            grading_result = grading_response.choices[0].message.content.strip()
            # Extract grade and feedback from the response
            lines = grading_result.split('\n')
            grade = lines[0].strip()  # First line should be the S Rank grade
            feedback = '\n'.join(lines[1:]).strip()  # Rest is feedback
        except Exception as e:
            st.error(f"Grading error: {str(e)}")
            grade = "N/A"
            feedback = "Error generating feedback"
        
        # 4. Return data to frontend
        results = {
            'transcribed_text': transcribed_text,
            'translation': translation,
            'grade': grade,
            'feedback': feedback
        }
        
        st.success("Submission processed successfully!")
        return results
        
    except Exception as e:
        st.error(f"Error processing submission: {str(e)}")
        return None 

def translate_text(text):
    try:
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Japanese to English translator."},
                {"role": "user", "content": f"Translate this Japanese text to English: {text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return None

def grade_translation(original_text, translation):
    try:
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        
        # Get the expected Japanese translation from session state
        expected_japanese = st.session_state.expected_japanese
        english_text = st.session_state.english_text
        
        if not expected_japanese or not english_text:
            st.error("Missing expected translation or English text.")
            return None
        
        # Grade the user's Japanese writing against both the English prompt and expected Japanese
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a Japanese language teacher grading writing practice.
                Be strict about meaning - if the student wrote something with a different meaning than the prompt,
                it should receive a lower grade even if it's grammatically correct Japanese.
                
                Grading criteria:
                S: Perfect translation that matches the meaning exactly and uses natural Japanese
                A: Good translation that captures the meaning well with minor issues
                B: Acceptable translation with some meaning or grammar issues
                C: Poor translation with significant meaning or grammar issues
                D: Incorrect meaning or major grammar issues
                
                Never provide the correct translation in the feedback. Instead, guide the student towards understanding 
                their mistakes and how to improve. Focus on explaining what parts of the meaning they missed or 
                misunderstood, and suggest vocabulary or grammar patterns they should review."""},
                {"role": "user", "content": f"""Grade this Japanese writing practice:
                English Prompt: {english_text}
                Expected Japanese: {expected_japanese}
                Student's Japanese: {original_text}
                Literal Translation of Student's Japanese: {translation}
                
                Provide a comprehensive review with:
                1. Grade (S, A, B, C, or D)
                2. Detailed feedback explaining:
                   - How well the meaning matches the English prompt (be specific about what was missed or incorrect)
                   - Any grammar issues found
                   - Natural Japanese usage evaluation
                3. Learning suggestions:
                   - Specific vocabulary or grammar points to review
                   - Practice tips for similar sentences
                   - Common pitfalls to avoid
                
                Format your response exactly as:
                Grade: [grade]
                
                Feedback:
                1. Meaning Analysis: [explain what parts of the meaning were captured or missed]
                2. Grammar Check: [point out any grammar issues or praise correct usage]
                3. Natural Usage: [comment on how natural the Japanese sounds]
                4. Study Suggestions:
                   - Key vocabulary to review
                   - Grammar patterns to practice
                   - Tips for improvement"""}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Grading error: {str(e)}")
        return None 