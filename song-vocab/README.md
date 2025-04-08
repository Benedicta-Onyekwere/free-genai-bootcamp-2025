# Song Vocabulary Extraction Service

A service that extracts vocabulary from song lyrics using AI-powered analysis.

## Project Structure
```
song-vocab/
├── app/
│   ├── main.py              # FastAPI application
│   ├── agent.py             # reAct agent implementation
│   ├── database.py          # SQLite database operations
│   └── tools/
│       ├── extract_vocabulary.py
│       ├── get_page_content.py
│       └── search_web.py
├── requirements.txt         # Python dependencies
```

## Development Process

### Initial Setup and Configuration
This project was implemented based on the Song Vocab Techspec provided in the bootcamp materials. The techspec outlined the architecture, components, and implementation details that guided the development of this service.

1. Created FastAPI application structure with necessary endpoints
2. Implemented reAct agent pattern for intelligent song analysis
   - Uses a thought-action-observation cycle for processing requests
   - Integrates with Ollama for natural language understanding
   - Manages tool execution and response generation
3. Set up SQLite database for vocabulary storage

### Key Commands Used
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Pull the Mistral model for Ollama
curl http://localhost:11434/api/pull -d '{"name": "mistral"}'

# Run the FastAPI server
PYTHONPATH=$PWD python -m uvicorn app.main:app --reload

# Test the API endpoint
curl -X POST http://localhost:8000/api/agent \
  -H "Content-Type: application/json" \
  -d '{"message_request": "Find lyrics for YOASOBI Idol"}'
```

### Challenges and Resolutions

1. **Import Resolution Issues**
   - Challenge: Relative imports causing module not found errors
   - Resolution: Switched to absolute imports using proper Python package structure
   - Files affected: `agent.py`, `main.py`

2. **Ollama Client API Changes**
   - Challenge: The Ollama client API had changed significantly from what was described in the techspec
   - Resolution: We had to make several code changes to work with the current API:
     - Changed client initialization from `ollama.Client()` to `ollama.AsyncClient(host='http://localhost:11434')`
     - Updated the chat method from `client.chat.completions.create()` to `client.chat()`
     - Modified the parameters structure for the chat method
     - Added manual response parsing since the instructor package's response model functionality wasn't compatible
     - Implemented custom JSON extraction from the model's response text
   - Code changes in `agent.py`:
     ```python
     # Old code (from techspec)
     self.client = ollama.Client()
     response = self.client.chat.completions.create(
         model="mistral",
         messages=[{"role": "user", "content": prompt}],
         response_model=AgentResponse
     )
     
     # New code (updated for current API)
     self.client = ollama.AsyncClient(host='http://localhost:11434')
     response = await self.client.chat(
         model="mistral",
         messages=[{"role": "user", "content": prompt}]
     )
     
     # Added manual response parsing
     response_text = response['message']['content']
     # Extract thought, action, and final_answer from response_text
     # Create AgentResponse object manually
     ```

3. **Instructor Package Compatibility & Response Parsing**
   - **Challenge:** The `instructor` package, initially intended for structured response parsing, was incompatible with the Ollama API's response format or the way the `ollama` library handled responses. The `response_model` parameter in the `chat` method did not function as expected.
   - **Resolution:** We removed the `response_model` parameter and implemented manual parsing logic within the `SongLyricsAgent.process_request` method in `agent.py`. This involved:
     - Receiving the raw text response from Ollama.
     - Using string searching and JSON loading (`json.loads`) within try-except blocks to reliably extract the `thought`, `action` (including tool name and arguments), and `final_answer` fields from the model's output, even if the formatting wasn't perfect JSON.
     - Manually constructing the `AgentResponse` Pydantic model from the extracted fields.
   - **Files affected:** `agent.py`

4. **Debugging Agent Logic & Tool Execution**
   - **Challenge:** Debugging the agent's reasoning cycle (thought -> action -> observation) and ensuring tools were called correctly with the right arguments extracted by the LLM required careful logging and iteration. Sometimes the LLM wouldn't format the action parameters correctly.
   - **Resolution:** Added detailed logging throughout the `process_request` and `execute_tool` methods in `agent.py` to track the agent's state, the LLM's output, the tool being called, and the observation received. Implemented retry logic in `execute_tool` to handle transient tool failures. Improved prompts to guide the LLM towards better-formatted action requests.
   - **Files affected:** `agent.py`

5. **Port Conflicts During Development**
    - **Challenge:** When restarting the `uvicorn` server during development (especially after errors or background processes), the default port (8000) was often still in use, preventing the server from starting.
    - **Resolution:** Regularly used terminal commands (`lsof -ti:8000 | xargs kill -9`) before restarting the server to ensure the port was free. Included this step implicitly in the development workflow.
    - **Files affected:** None (Workflow adjustment)

## Prerequisites

- Python 3.10 or higher
- Virtual environment (venv)
- Ollama (pre-installed during bootcamp setup)

## Setup

1. **Activate Virtual Environment**
   ```bash
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Pull the Mistral Model**
   ```bash
   curl http://localhost:11434/api/pull -d '{"name": "mistral"}'
   ```
   
   Mistral is a powerful open-source language model that we use for:
   - Understanding and analyzing song lyrics
   - Extracting vocabulary items with accurate meanings
   - Processing natural language queries from users
   - Generating structured responses for the agent

4. **Start the Service**
   ```bash
   PYTHONPATH=$PWD python -m uvicorn app.main:app --reload
   ```

## Usage

Send a POST request to `/api/agent` with your song query:

```bash
curl -X POST http://localhost:8000/api/agent \
  -H "Content-Type: application/json" \
  -d '{"message_request": "song title and artist"}'
```

[View Screenshot](../lang-portal/assets/song-vocab-screenshot.png)

## Development

1. **Database Schema**
   - SQLite database with two tables:
     - `songs`: stores song metadata (id, title, artist, lyrics, language)
     - `vocabulary`: stores extracted words (word, reading, meaning, part_of_speech, difficulty_level)


