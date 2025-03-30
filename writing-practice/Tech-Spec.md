# Technical Specifications

## Overview

The Japanese Writing Practice App is a Streamlit-based application that provides two main functionalities:
1. Sentence Practice - For practicing writing complete Japanese sentences
2. Word Practice - For practicing individual kanji words and readings

## Architecture

### Components

1. **State Management**
   - `setup_state.py`: Handles initial setup and sentence/word selection
   - `practice_state.py`: Manages practice interface and input methods
   - `review_state.py`: Handles grading and feedback display
   - `word_*_state.py`: Word practice specific state components

2. **Services**
   - `sentence_generator.py`: Generates practice sentences
   - `grading_system.py`: Handles OCR and AI-powered grading
   - `word_data.py`: Manages word practice data

### Technologies

- **Frontend**: Streamlit
- **OCR**: manga-ocr
- **AI Grading**: OpenAI GPT-3.5
- **Image Processing**: Pillow

## Grading System

### Sentence Grading
- Uses OpenAI GPT-3.5 for comprehensive evaluation
- S-Rank grading system (S, A, B, C, D)
- Evaluates:
  - Meaning accuracy
  - Grammar correctness
  - Natural Japanese usage
- Provides detailed feedback and study suggestions

### Word Grading
- Exact match comparison for readings
- Binary grading (correct/incorrect)
- Immediate feedback
- Progress tracking

## Data Flow

1. **Sentence Practice**
   ```
   Setup → Generate Sentence → User Input → OCR → Translation → 
   Grading → Feedback → History Update
   ```

2. **Word Practice**
   ```
   Setup → Select Word → User Input → Comparison → 
   Grading → Feedback → History Update
   ```

## Security

- OpenAI API key stored in `.streamlit/secrets.toml`
- No user data persistence
- Input validation for file uploads

## Future Enhancements

1. **Planned Features**
   - Handwriting OCR for word practice
   - Spaced repetition system
   - Progress analytics
   - Custom word/sentence lists

2. **Technical Improvements**
   - Offline OCR capabilities
   - Enhanced error handling
   - Performance optimizations
   - User authentication

## Development Guidelines

1. **Code Style**
   - Follow PEP 8
   - Use type hints
   - Document all functions
   - Keep components modular

2. **Testing**
   - Unit tests for services
   - Integration tests for state management
   - Manual testing for UI flows

3. **Version Control**
   - Feature branches
   - Pull request reviews
   - Semantic versioning