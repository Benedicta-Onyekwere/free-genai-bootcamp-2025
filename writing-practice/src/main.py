import streamlit as st
import streamlit.components.v1 as components
from components.setup_state import setup_state
from components.practice_state import practice_state
from components.review_state import review_state
from services.grading_system import translate_text, grade_translation
import nest_asyncio

# Apply nest_asyncio to handle nested event loops
nest_asyncio.apply()

# Set page config
st.set_page_config(
    page_title="Japanese Writing Practice",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Japanese Writing Practice App"
    }
)

def main():
    # Initialize session state variables
    if "app_state" not in st.session_state:
        st.session_state.app_state = "setup"
        
    if "english_text" not in st.session_state:
        st.session_state.english_text = None
        
    if "transcribed_text" not in st.session_state:
        st.session_state.transcribed_text = None
        
    if "translation" not in st.session_state:
        st.session_state.translation = None
        
    if "grade" not in st.session_state:
        st.session_state.grade = None
        
    # Initialize practice history
    if "practice_history" not in st.session_state:
        st.session_state.practice_history = []

    st.title("Japanese Writing Practice")
    
    if st.session_state.app_state == "setup":
        setup_state()
    elif st.session_state.app_state == "practice":
        practice_state()
    elif st.session_state.app_state == "review":
        if st.session_state.transcribed_text:
            # Get translation
            if not st.session_state.translation:
                st.session_state.translation = translate_text(st.session_state.transcribed_text)
            
            # Get grade and feedback
            if st.session_state.translation and not st.session_state.grade:
                st.session_state.grade = grade_translation(st.session_state.transcribed_text, st.session_state.translation)
                
                # If grade is C or D, add sentence to practice history
                grade_line = st.session_state.grade.split('\n')[0]
                if ('C' in grade_line or 'D' in grade_line) and st.session_state.english_text not in st.session_state.practice_history:
                    st.session_state.practice_history.append(st.session_state.english_text)
        
        review_state()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}") 