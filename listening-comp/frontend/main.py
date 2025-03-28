import streamlit as st
from typing import Dict
import json
from collections import Counter
import re

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.get_transcript import YouTubeTranscriptDownloader

from backend.chat import JapaneseTutor
from backend.structured_data import TranscriptStructurer


# Page config
st.set_page_config(
    page_title="Japanese Learning Assistant",
    page_icon="🎌",
    layout="wide"
)

# Initialize session state
if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

def render_header():
    """Render the header section"""
    st.title("🎌 Japanese Learning Assistant")
    st.markdown("""
    Transform YouTube transcripts into interactive Japanese learning experiences.
    
    This tool demonstrates:
    - Base LLM Capabilities
    - RAG (Retrieval Augmented Generation)
    - Amazon Bedrock Integration
    - Agent-based Learning Systems
    """)

def render_sidebar():
    """Render the sidebar with component selection"""
    with st.sidebar:
        st.header("Development Stages")
        
        # Main component selection
        selected_stage = st.radio(
            "Select Stage:",
            [
                "1. Chat with Nova",
                "2. Raw Transcript",
                "3. Structured Data",
                "4. RAG Implementation",
                "5. Interactive Learning"
            ]
        )
        
        # Stage descriptions
        stage_info = {
            "1. Chat with Nova": """
            **Current Focus:**
            - Basic Japanese learning
            - Understanding LLM capabilities
            - Identifying limitations
            """,
            
            "2. Raw Transcript": """
            **Current Focus:**
            - YouTube transcript download
            - Raw text visualization
            - Initial data examination
            """,
            
            "3. Structured Data": """
            **Current Focus:**
            - Text cleaning
            - Dialogue extraction
            - Data structuring
            """,
            
            "4. RAG Implementation": """
            **Current Focus:**
            - Bedrock embeddings
            - Vector storage
            - Context retrieval
            """,
            
            "5. Interactive Learning": """
            **Current Focus:**
            - Scenario generation
            - Audio synthesis
            - Interactive practice
            """
        }
        
        st.markdown("---")
        st.markdown(stage_info[selected_stage])
        
        return selected_stage

def render_chat_stage():
    """Render an improved chat interface"""
    st.header("Chat with Nova")

    # Initialize JapaneseTutor instance if not in session state
    if 'japanese_tutor' not in st.session_state:
        st.session_state.japanese_tutor = JapaneseTutor()

    # Introduction text
    st.markdown("""
    Start by exploring Nova's base Japanese language capabilities. Try asking questions about Japanese grammar, 
    vocabulary, or cultural aspects.
    
    You can ask about:
    - Basic greetings and phrases
    - Common locations and directions
    - Grammar points like は vs が
    - Verb forms like ます form
    """)

    # Initialize chat history if not exists
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])

    # Chat input area
    if prompt := st.chat_input("Ask about Japanese language..."):
        # Process the user input
        process_message(prompt)

    # Example questions in sidebar
    with st.sidebar:
        st.markdown("### Try These Examples")
        example_questions = [
            "How do I say 'Where is the train station?' in Japanese?",
            "Explain the difference between は and が",
            "What's the polite form of 食べる?",
            "How do I say hello in Japanese?",
            "How do I say thank you in Japanese?",
            "How do I ask for directions politely?"
        ]
        
        for q in example_questions:
            if st.button(q, use_container_width=True, type="secondary"):
                # Process the example question
                process_message(q)
                st.rerun()

    # Add a clear chat button
    if st.session_state.messages:
        if st.button("Clear Chat", type="primary"):
            st.session_state.messages = []
            st.rerun()

def process_message(message: str):
    """Process a message and generate a response"""
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": message})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(message)

    # Generate and display assistant's response
    with st.chat_message("assistant", avatar="🤖"):
        response = st.session_state.japanese_tutor.generate_response(message)
        if response:
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})



def count_characters(text):
    """Count Japanese and total characters in text"""
    if not text:
        return 0, 0
        
    def is_japanese(char):
        return any([
            '\u4e00' <= char <= '\u9fff',  # Kanji
            '\u3040' <= char <= '\u309f',  # Hiragana
            '\u30a0' <= char <= '\u30ff',  # Katakana
        ])
    
    jp_chars = sum(1 for char in text if is_japanese(char))
    return jp_chars, len(text)

def render_transcript_stage():
    """Render the raw transcript stage"""
    st.header("Raw Transcript Processing")
    
    # URL input
    url = st.text_input(
        "YouTube URL",
        placeholder="Enter a Japanese lesson YouTube URL (e.g., https://www.youtube.com/watch?v=sY7L5cfCWno)"
    )
    
    # Download button and processing
    if url:
        if st.button("Download Transcript"):
            try:
                with st.spinner('Downloading transcript...'):
                    downloader = YouTubeTranscriptDownloader()
                    transcript = downloader.get_transcript(url)
                    if transcript:
                        # Save the transcript
                        video_id = downloader.extract_video_id(url)
                        st.session_state.video_id = video_id  # Store video_id in session state
                        
                        if downloader.save_transcript(transcript, video_id):
                            st.success(f"Transcript saved successfully to transcripts/{video_id}.txt!")
                        
                        st.session_state.transcript = transcript
                        
                        # Display transcript in a more readable format
                        st.subheader("Raw Transcript")
                        transcript_text = ""
                        for entry in transcript:
                            transcript_text += f"{entry['text']}\n"
                        st.text_area("Full Transcript", transcript_text, height=400)
                        
                        # Display some statistics
                        total_lines = len(transcript)
                        total_chars = sum(len(entry['text']) for entry in transcript)
                        jp_chars, _ = count_characters(transcript_text)
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Total Lines", total_lines)
                        col2.metric("Total Characters", total_chars)
                        col3.metric("Japanese Characters", jp_chars)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure the URL is correct and the video has Japanese subtitles available.")
    else:
        st.info("Please enter a YouTube URL to download its transcript.")

def render_structured_stage():
    """Render the structured data stage"""
    st.header("Structured Data Processing")
    
    if st.session_state.transcript is None:
        st.warning("Please download a transcript first in the Raw Transcript stage.")
        return
        
    try:
        # Create transcript text from session state
        transcript_text = "\n".join(entry['text'] for entry in st.session_state.transcript)
        
        # Initialize structurer
        structurer = TranscriptStructurer()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Raw Transcript")
            st.text_area("Original Text", transcript_text, height=400)
            
        with col2:
            st.subheader("Structured Format")
            if st.button("Structure Transcript"):
                with st.spinner("Structuring transcript..."):
                    structured_data = structurer.structure_transcript(transcript_text)
                    if structured_data:
                        # Save structured data
                        if 'video_id' in st.session_state:
                            structured_path = os.path.join(
                                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "backend",
                                "transcripts",
                                f"{st.session_state.video_id}_structured.json"
                            )
                            if structurer.save_structured_data(structured_data, structured_path):
                                st.success(f"Structured data saved to transcripts/{st.session_state.video_id}_structured.json!")
                        
                        # Display the structured data
                        st.text_area("Structured Text", json.dumps(structured_data, ensure_ascii=False, indent=2), height=400)
                    else:
                        st.error("Failed to structure transcript. Please try again.")
            
    except Exception as e:
        st.error(f"Error processing transcript: {str(e)}")
        st.info("Make sure you have a valid transcript loaded and your OpenAI API key is set correctly.")

def render_rag_stage():
    """Render the RAG implementation stage"""
    st.header("RAG System")
    
    # Query input
    query = st.text_input(
        "Test Query",
        placeholder="Enter a question about Japanese..."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Retrieved Context")
        # Placeholder for retrieved contexts
        st.info("Retrieved contexts will appear here")
        
    with col2:
        st.subheader("Generated Response")
        # Placeholder for LLM response
        st.info("Generated response will appear here")

def render_interactive_stage():
    """Render the interactive learning stage"""
    st.header("Interactive Learning")
    
    # Practice type selection
    practice_type = st.selectbox(
        "Select Practice Type",
        ["Dialogue Practice", "Vocabulary Quiz", "Listening Exercise"]
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Practice Scenario")
        # Placeholder for scenario
        st.info("Practice scenario will appear here")
        
        # Placeholder for multiple choice
        options = ["Option 1", "Option 2", "Option 3", "Option 4"]
        selected = st.radio("Choose your answer:", options)
        
    with col2:
        st.subheader("Audio")
        # Placeholder for audio player
        st.info("Audio will appear here")
        
        st.subheader("Feedback")
        # Placeholder for feedback
        st.info("Feedback will appear here")

def main():
    render_header()
    selected_stage = render_sidebar()
    
    # Render appropriate stage
    if selected_stage == "1. Chat with Nova":
        render_chat_stage()
    elif selected_stage == "2. Raw Transcript":
        render_transcript_stage()
    elif selected_stage == "3. Structured Data":
        render_structured_stage()
    elif selected_stage == "4. RAG Implementation":
        render_rag_stage()
    elif selected_stage == "5. Interactive Learning":
        render_interactive_stage()
    
    # Debug section at the bottom
    with st.expander("Debug Information"):
        st.json({
            "selected_stage": selected_stage,
            "transcript_loaded": st.session_state.transcript is not None,
            "chat_messages": len(st.session_state.messages)
        })

if __name__ == "__main__":
    main()