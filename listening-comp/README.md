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

## JLPT Question Processing Implementation

The app now successfully processes JLPT listening comprehension questions from YouTube transcripts:

### Section Types
- 問題1: Dialogue-based questions with clear conversation context
- 問題2: Complex dialogue scenarios with multiple speakers
- 問題3: Situational response questions

### Processing Features
- Automatic section detection and categorization
- Structured output with Introduction, Conversation, Question, and Options
- Japanese text preservation with proper formatting
- Question files organized by video ID and section number

### Example Output Structure
```json
{
  "Introduction": "会話の内容について質問します",
  "Conversation": "男: すみません、郵便局はどこですか\n女: ああ、本屋の隣です",
  "Question": "男の人はどこに行きますか",
  "Options": [
    "郵便局",
    "本屋",
    "銀行",
    "駅"
  ]
}
```

## Implementation Progress

### 1. Initial Setup and Basic Functionality
- Set up project structure with backend and frontend directories
- Implemented basic YouTube transcript downloading functionality
- Created initial Streamlit interface for user interaction
- Added basic error handling for transcript downloads

### 2. Transcript Processing and Data Structure
- Enhanced `get_transcript.py` with improved video ID extraction
- Added Japanese character counting functionality to `structured_data.py`
- Implemented section-based question extraction (問題1, 問題2, 問題3)
- Created organized storage structure for processed questions

### 3. Frontend Development
- Developed structured data visualization components
- Added error handling and user feedback mechanisms
- Enhanced transcript display with character counting
- Improved overall UI/UX for better user interaction

### 4. Audio Implementation
- Added AWS Polly integration for text-to-speech
- Created `generated_audio` directory with `.gitkeep`
- Configured ffmpeg for audio processing
- Set up error handling for audio generation
[View Implementation Progress](../lang-portal/assets/implementation_progress.png)

### Current Challenges
1. Audio file overwrite confirmation in automated processes
2. Event loop handling in Streamlit for long-running audio tasks
3. Port configuration and server stability
4. Proper cleanup of generated audio files

### Next Steps
1. Implement proper state management for learning sessions
2. Add question store functionality
3. Enhance audio generation workflow
4. Improve error handling for audio processing
