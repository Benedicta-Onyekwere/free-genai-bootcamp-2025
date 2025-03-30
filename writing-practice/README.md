# Japanese Writing Practice App

A Streamlit application for practicing Japanese writing, featuring both sentence and word practice modes.

## Features

- **Sentence Practice Mode**
  - Practice writing Japanese sentences from English prompts
  - OCR support for handwritten submissions
  - AI-powered grading with S-Rank system
  - Detailed feedback on accuracy, grammar, and natural usage

- **Word Practice Mode**
  - Practice writing Japanese words and readings
  - Support for both typed input and handwritten submissions
  - Immediate feedback on correctness
  - Progress tracking for practiced words

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   - Create `.streamlit/secrets.toml`
   - Add your OpenAI API key:
     ```toml
     OPENAI_API_KEY = "your-api-key"
     ```

## Usage

Run the application:
```bash
streamlit run src/main.py
```

For word practice mode:
```bash
streamlit run src/word_main.py
```

## Project Structure

- `src/`
  - `main.py` - Main sentence practice application
  - `word_main.py` - Word practice application
  - `components/` - UI state management components
  - `services/` - Core functionality (grading, OCR, etc.)
- `.streamlit/` - Streamlit configuration
- `requirements.txt` - Project dependencies
- `Tech-Spec.md` - Technical specifications

## Contributing

See `Tech-Spec.md` for detailed technical specifications and contribution guidelines.

## Current Issues

1. OpenSSL Warning:
   ```
   urllib3 v2 only supports OpenSSL 1.1.1+, currently using LibreSSL 2.8.3
   ```

2. Torch Warning:
   ```
   Examining the path of torch.classes raised: Tried to instantiate class '__path__._path'
   ```

## Setup Instructions

1. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   cd /path/to/writing-practice
   source venv/bin/activate
   venv/bin/streamlit run src/main.py
   ```

## Application Flow

1. **Setup State**
   - User sees "Generate Sentence" button
   - Clicking generates a practice sentence
   - Transitions to Practice State

2. **Practice State**
   - Displays the English sentence to practice
   - Provides image upload for handwritten Japanese
   - Submit button for grading

3. **Review State**
   - Shows original sentence
   - Displays OCR transcription
   - Shows translation and grade
   - Option to generate next question

## Next Steps

1. Implement actual OpenAI integration for sentence generation
2. Enhance grading system with better feedback
3. Add word collection API integration
4. Resolve OpenSSL and Torch warnings
5. Add proper error handling
6. Implement user session management

## Notes

- Currently using mock data for some functionality
- OCR is implemented using manga-ocr
- Future updates will include more sophisticated grading 