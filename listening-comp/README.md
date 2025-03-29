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
   - Removed audio-related features for stability

3. Data Processing:
   - Successfully processed JLPT format transcripts into structured sections
   - Implemented section-based question extraction (問題1, 問題2, 問題3)
   - Stored processed questions in organized section files
   - Added proper Japanese text handling and formatting

4. Frontend Updates:
   - Added structured data visualization
   - Improved error handling and user feedback
   - Enhanced transcript display with character counting
   - Streamlined UI for better user experience

## Project Structure
```
listening-comp/
├── backend/
│   ├── data/
│   │   └── questions/     # Processed section-based questions
│   ├── chat.py           # Japanese tutor implementation
│   ├── get_transcript.py # YouTube transcript handling
│   ├── structured_data.py # Transcript processing
│   ├── vector_store.py   # Vector storage implementation
│   └── requirements.txt
├── frontend/
│   └── main.py          # Streamlit interface
└── README.md
```

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

## Usage
1. Start with the Chat stage to interact with Nova (Japanese tutor)
2. Use the Raw Transcript stage to download YouTube content
3. Process transcripts in the Structured Data stage to generate section-based questions
4. Practice with interactive learning features
