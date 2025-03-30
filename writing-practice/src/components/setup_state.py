import streamlit as st
from openai import OpenAI

def generate_sentence():
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Japanese language teacher generating simple English sentences for translation practice."},
                {"role": "user", "content": "Generate a simple English sentence that would be appropriate for a beginner Japanese student to translate. The sentence should use basic vocabulary and grammar."}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating sentence: {str(e)}")
        return None

def setup_state():
    """Setup state component with Generate Sentence button.
    As per Tech-Spec: When user first starts up the app, they will only see a button called "Generate Sentence"
    """
    st.header("Setup")
    
    # If there are sentences in practice history, show them first
    if st.session_state.practice_history:
        st.subheader("Practice History")
        st.write("These sentences need more practice:")
        
        for sentence in st.session_state.practice_history:
            if st.button(f"Practice: {sentence}", key=f"practice_{sentence}"):
                st.session_state.english_sentence = sentence
                st.session_state.app_state = "practice"
                st.rerun()
        
        st.divider()
        st.subheader("Or Generate a New Sentence")
    
    if st.button("Generate New Sentence"):
        with st.spinner("Generating sentence..."):
            sentence = generate_sentence()
            if sentence:
                st.session_state.english_sentence = sentence
                st.session_state.app_state = "practice"
                st.rerun() 