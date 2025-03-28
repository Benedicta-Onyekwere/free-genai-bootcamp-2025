# Listening Learning App

## Business Goal: 
You are an Applied AI Engineer and you have been tasked to build a Language Listening Comprehension App. There are practice listening comprehension examples for language learning tests on youtube.

Pull the youtube content, and use that to generate out similar style listening comprehension.

## Technical Uncertainty:

Don't know Japanese!
Accessing or storing documents as vector store with Sqlite3
TSS might not exist for my target language OR might not be good enough.
ASR might not exist for my target language OR might not be good enough.
Can you pull transcripts for the target videos?

## Technical Requirements:

(Optional) Speech to Text, (ASR) Transcribe. eg Amazon Transcribe. OpenWhisper
Youtube Transcript API (Download Transcript from Youtube)
LLM + Tool Use "Agent"
Sqlite3 - Knowledge Base 
Text to Speech (TTS) eg. Amazon Polly
AI Coding Assistant eg. Amazon Developer Q, Windsurf, Cursor, Github Copilot
Frontend eg. Streamlit.
Guardrails

## Recent Changes and Progress:

1. Code Structure Improvements:
   - Enhanced `get_transcript.py` with better video ID extraction
   - Added Japanese character counting functionality to `structured_data.py`
   - Updated frontend requirements with specific versions
   - Merged useful functionality from services layer

2. Backend Enhancements:
   - Improved error handling in transcript downloading
   - Added character counting for Japanese text analysis
   - Enhanced video ID extraction with more robust patterns

## Setup Instructions
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```
4. Run the application:
   ```bash
   streamlit run frontend/main.py
   ```
