import streamlit as st
from typing import Dict
import json
from collections import Counter
import re
from datetime import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.get_transcript import YouTubeTranscriptDownloader

from backend.chat import JapaneseTutor
from backend.structured_data import TranscriptStructurer
from backend.question_store import QuestionStore


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
if 'question_store' not in st.session_state:
    st.session_state.question_store = QuestionStore()

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
        
        # Display saved questions for relevant stages
        if selected_stage in ["3. Structured Data", "5. Interactive Learning"]:
            st.markdown("---")
            st.subheader("Saved Questions")
            
            # List saved questions
            saved_questions = st.session_state.question_store.list_saved_questions()
            if saved_questions:
                for question in saved_questions:
                    # Format timestamp for display
                    timestamp = question.get('timestamp', '')
                    try:
                        # Convert timestamp to datetime and format it
                        dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                        formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        formatted_time = timestamp
                    
                    practice_type = question.get('practice_type', 'Unknown Practice')
                    topic = question.get('topic', 'Unknown Topic')
                    title = f"{practice_type} - {topic}"
                    
                    with st.expander(f"{title} ({formatted_time})"):
                        # Load the question data to show preview
                        loaded_data = st.session_state.question_store.load_questions(question['filename'])
                        if loaded_data and 'questions' in loaded_data:
                            questions = loaded_data['questions']
                            # Show a preview of the dialogue
                            if 'dialogue' in questions:
                                st.markdown("**Preview:**")
                                for line in questions['dialogue'][:2]:  # Show first two lines
                                    st.markdown(f"_{line['speaker']}:_ {line['text']}")
                                if len(questions['dialogue']) > 2:
                                    st.markdown("_... (more lines)_")
                            
                            col1, col2 = st.columns([1, 1])
                            with col1:
                                if st.button("📝 Practice Now", key=f"practice_{question['filename']}"):
                                    # Set up the practice session
                                    st.session_state.current_question = loaded_data.get('questions', {})
                                    st.session_state.current_question_set = loaded_data
                                    # Switch to Interactive Learning stage
                                    st.session_state.selected_stage = "5. Interactive Learning"
                                    # Set practice type and topic from the loaded data
                                    st.session_state.practice_type = loaded_data.get('practice_type')
                                    st.session_state.selected_topic = loaded_data.get('topic')
                                    st.rerun()
                            with col2:
                                if st.button("🗑️ Delete", key=f"delete_{question['filename']}"):
                                    if st.session_state.question_store.delete_questions(question['filename']):
                                        st.success("Question set deleted!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to delete question set.")
            else:
                st.info("No saved questions found.")
        
        # Stage descriptions
        st.markdown("---")
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
    
    if st.session_state.transcript:
        st.subheader("Raw Transcript")
        transcript_text = ""
        for entry in st.session_state.transcript:
            transcript_text += f"{entry['text']}\n"
        st.text_area("Full Transcript", transcript_text, height=200)
        
        if st.button("Structure Transcript"):
            with st.spinner("Processing transcript..."):
                structurer = TranscriptStructurer()
                try:
                    structured_sections = structurer.structure_transcript(st.session_state.transcript)
                    if structured_sections:
                        # Save the structured questions
                        video_id = st.session_state.get('video_id', 'unknown')
                        filename = st.session_state.question_store.save_questions(structured_sections, video_id)
                        st.session_state.structured_data = structured_sections
                        st.success(f"Structured data saved as {filename}!")
                        
                        # Display the structured data
                        st.subheader("Structured Format")
                        st.json(structured_sections)
                    else:
                        st.error("Failed to structure transcript. Please try again.")
                except Exception as e:
                    st.error(f"Error structuring transcript: {str(e)}")
        
        # Display previously structured data if available
        if hasattr(st.session_state, 'structured_data'):
            st.subheader("Current Structured Data")
            st.json(st.session_state.structured_data)
    else:
        st.info("Please download a transcript first in the Raw Transcript stage.")

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
    
    # Initialize session state for interactive learning
    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = None
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'current_question_set' not in st.session_state:
        st.session_state.current_question_set = None
    if 'practice_type' not in st.session_state:
        st.session_state.practice_type = None
    
    # Practice type selection with default to session state
    practice_type = st.selectbox(
        "Select Practice Type",
        ["Dialogue Practice", "Vocabulary Quiz", "Listening Exercise"],
        index=["Dialogue Practice", "Vocabulary Quiz", "Listening Exercise"].index(st.session_state.practice_type) if st.session_state.practice_type else 0,
        key="practice_type_select"
    )
    
    # Topic selection
    if practice_type == "Dialogue Practice":
        topic = st.selectbox(
            "Select Topic",
            ["Daily Conversations", "Shopping", "Restaurant", "Travel", "School Life"],
            index=["Daily Conversations", "Shopping", "Restaurant", "Travel", "School Life"].index(st.session_state.selected_topic) if st.session_state.selected_topic else 0,
            key="topic_select"
        )
        
        # Generate question button
        if st.button("Generate Question"):
            with st.spinner("Generating question..."):
                # Update practice type and topic first
                st.session_state.practice_type = practice_type
                st.session_state.selected_topic = topic
                
                # Create a sample question (replace with actual generation logic)
                question_set = {
                    "video_id": "sample_video",
                    "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
                    "practice_type": practice_type,
                    "topic": topic,
                    "questions": {
                        "scenario": get_scenario_for_topic(topic),
                        "dialogue": get_dialogue_for_topic(topic),
                        "question": "What should you say next?",
                        "options": get_options_for_topic(topic),  # New helper function
                        "correct": 2
                    }
                }
                
                # Save the generated questions
                filename = st.session_state.question_store.save_questions(
                    question_set,
                    question_set["video_id"]
                )
                
                # Update the current question and question set
                st.session_state.current_question = question_set["questions"]
                st.session_state.current_question_set = question_set
                st.success("Question generated and saved!")
                st.rerun()
    else:
        st.info("Other practice types coming soon!")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Practice Scenario")
        if st.session_state.current_question:
            st.write("**Scenario:**", st.session_state.current_question["scenario"])
            st.write("**Dialogue:**")
            for line in st.session_state.current_question["dialogue"]:
                st.write(f"{line['speaker']}: {line['text']}")
            
            # Question and options
            st.write("\n**" + st.session_state.current_question["question"] + "**")
            
            # Use radio buttons for options
            selected_idx = st.radio(
                "Choose your answer:",
                range(len(st.session_state.current_question["options"])),
                format_func=lambda x: st.session_state.current_question["options"][x],
                key="answer_radio"
            )
            
            # Check answer button
            if st.button("Check Answer"):
                correct_idx = st.session_state.current_question["correct"]
                if selected_idx == correct_idx:
                    st.success("Correct! Well done! 🎉")
                else:
                    correct_answer = st.session_state.current_question["options"][correct_idx]
                    st.error(f"Not quite. The correct answer was: {correct_answer}")
        else:
            st.info("Generate a question to start practicing!")
        
    with col2:
        st.subheader("Audio")
        st.info("Audio will be available in future updates")
        
        st.subheader("Feedback")
        if st.session_state.current_question:
            st.info("Practice speaking the dialogue out loud!")
        else:
            st.info("Feedback will appear here after answering")

def get_scenario_for_topic(topic: str) -> str:
    """Get a relevant scenario based on the topic."""
    scenarios = {
        "Daily Conversations": "At a coffee shop",
        "Shopping": "At a clothing store",
        "Restaurant": "At a family restaurant",
        "Travel": "At the train station",
        "School Life": "In the classroom"
    }
    return scenarios.get(topic, "In a typical situation")

def get_dialogue_for_topic(topic: str) -> list:
    """Get relevant dialogue based on the topic."""
    dialogues = {
        "Daily Conversations": [
            {"speaker": "Person A", "text": "おはようございます。"},
            {"speaker": "Person B", "text": "おはようございます。今日はいい天気ですね。"}
        ],
        "Shopping": [
            {"speaker": "Customer", "text": "すみません、このシャツはいくらですか？"},
            {"speaker": "Staff", "text": "3000円です。"}
        ],
        "Restaurant": [
            {"speaker": "Waiter", "text": "いらっしゃいませ。"},
            {"speaker": "Customer", "text": "すみません、メニューをお願いします。"}
        ],
        "Travel": [
            {"speaker": "Tourist", "text": "すみません、東京駅はどこですか？"},
            {"speaker": "Local", "text": "あ、この道をまっすぐ行ってください。"}
        ],
        "School Life": [
            {"speaker": "Teacher", "text": "みなさん、おはようございます。"},
            {"speaker": "Students", "text": "おはようございます、先生。"}
        ]
    }
    return dialogues.get(topic, [
        {"speaker": "Person A", "text": "こんにちは。"},
        {"speaker": "Person B", "text": "こんにちは。"}
    ])

def get_options_for_topic(topic: str) -> list:
    """Get relevant answer options based on the topic."""
    options = {
        "Daily Conversations": [
            "ええ、本当にいい天気ですね。",
            "いいえ、雨が降っています。",
            "すみません、分かりません。",
            "さようなら。"
        ],
        "Shopping": [
            "ありがとうございます。試着してもいいですか？",
            "高すぎます。もっと安いのはありますか？",
            "はい、これを買います。",
            "すみません、トイレはどこですか？"
        ],
        "Restaurant": [
            "ありがとうございます。",
            "はい、そうです。",
            "お水をください。",
            "さようなら。"
        ],
        "Travel": [
            "ありがとうございます。",
            "分かりました。ありがとうございます。",
            "すみません、もう一度お願いします。",
            "いいえ、結構です。"
        ],
        "School Life": [
            "はい、よろしくお願いします。",
            "すみません、遅れてすみません。",
            "質問があります。",
            "さようなら。"
        ]
    }
    return options.get(topic, [
        "ありがとうございます。",
        "はい、そうです。",
        "すみません。",
        "さようなら。"
    ])

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