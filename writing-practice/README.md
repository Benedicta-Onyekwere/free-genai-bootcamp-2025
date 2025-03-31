# Japanese Writing Practice App

A Streamlit application for practicing Japanese writing with automated grading and feedback using OCR technology.

## Project Structure

```
writing-practice/
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── src/
│   ├── components/
│   │   ├── setup_state.py    # Initial state with sentence generation
│   │   ├── practice_state.py # Practice state with image upload
│   │   └── review_state.py   # Review state with grading
│   ├── services/
│   │   ├── sentence_generator.py # Generates practice sentences
│   │   └── grading_system.py    # Handles OCR and grading
│   └── main.py             # Main Streamlit application
├── venv/                   # Python virtual environment
├── requirements.txt        # Project dependencies
├── Tech-Spec.md           # Technical specifications
└── README.md              # This file
```

## Setup Progress 

1. **Project Planning**
   - Used created Tech-Spec.md as the foundation for development
   - Defined application architecture and components
   - Outlined grading system and data flow
   - Specified technical requirements and dependencies

2. **Initial Setup**
   - Created project directory structure based on Tech-Spec
   - Set up Python virtual environment
   - Created requirements.txt with necessary dependencies:
     - streamlit==1.32.0
     - Pillow==10.2.0
     - manga-ocr==0.1.14
     - openai==0.28.0
     - requests==2.31.0

3. **Directory Organization**
   - Implemented proper directory structure
   - Removed duplicate directories and unused files
   - Moved Streamlit configuration to correct location

4. **Component Implementation**
   - Created setup_state component for sentence generation
   - Implemented practice_state for image upload
   - Added review_state for grading and feedback
   - Integrated state management in main.py

5. **Services Implementation**
   - Implemented sentence generator with mock data
   - Set up grading system with MangaOCR integration
   - Prepared for future OpenAI API integration

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
   [View Practice Interface](../../lang-portal/assets/study_activities/practice-interface.png)

3. **Review State**
   - Shows original sentence
   - Displays OCR transcription
   - Shows translation and grade
   - Option to generate next question
   ![View Review Interface](../../lang-portal/assets/review-interface.png)

## New Features

1. **Word Practice Mode**
   - Added single word practice functionality
   - Implemented word-specific components:
     - word_setup_state.py
     - word_practice_state.py
     - word_review_state.py
   - Added word_data.py service for word management
   - Created word_main.py entry point

2. **Documentation Updates**
   - Updated project structure to include single word practice components
   - Added setup instructions for both sentence and word practice modes

3. **Usage Instructions**
   For sentence practice:
   ```bash
   streamlit run src/main.py
   ```
   
   For word practice:
   ```bash
   streamlit run src/word_main.py
   ```

## Enhanced Features and Integration

1. **Practice Enhancement**
   - Added retry functionality for failed words/sentences
   - Implemented progress tracking for each practice item
   - Added option to generate new items or retry failed ones
   - Enhanced feedback system with detailed grammar and vocabulary suggestions
   [View Practice Flow](../lang-portal/assets/study_activities/practice-flow.png)

2. **Language Portal Integration**
   - **Backend Connection**
     ```python
     # New API endpoint in Flask backend
     @app.route('/api/writing-practice', methods=['POST'])
     def submit_practice():
         # Process writing practice submission
         # Store in session history
         # Return detailed feedback
     ```
   - Removed mock data from backend
   - Added real-time session tracking
   - Implemented study activity logging
   - Using OpenAI API v0.28.0 for consistent response handling
   [View Backend Integration](../lang-portal/assets/study_activities/backend-arch.png)

3. **Frontend Updates**
   - Added writing practice component to React frontend
   - Implemented Streamlit launcher in portal
   - Created session history display
   - Added study progress tracking
   [View Frontend Updates](../lang-portal/assets/study_activities/frontend-integration.png)

4. **Running the Integrated System**
   ```bash
   # Start Flask backend (port 5000)
   cd lang-portal-flask-react/backend
   source venv/bin/activate
   python app.py --port 5000

   # Start React frontend (port 5175)
   cd ../frontend
   npm run dev -- --port 5175

   # Start Streamlit app (port 8082)
   cd ../../writing-practice
   streamlit run src/main.py --server.port 8082
   ```

5. **Challenges Addressed**
   - Fixed OpenAI API version compatibility issues
   - Implemented consistent response handling
   - Enhanced session state management between portal and Streamlit
   - Improved OCR accuracy with pre-processing

