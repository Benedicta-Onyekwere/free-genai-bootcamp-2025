from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.agent import run_agent
from app.database import init_db, add_song_and_vocabulary

class MessageRequest(BaseModel):
    message_request: str

class VocabularyItem(BaseModel):
    word: str
    reading: Optional[str] = None
    meaning: Optional[str] = None
    part_of_speech: Optional[str] = None
    difficulty_level: Optional[str] = None

class AgentResponse(BaseModel):
    lyrics: str
    vocabulary: List[VocabularyItem]

app = FastAPI(
    title="Song Vocabulary Extraction Service",
    description="A service that extracts vocabulary from song lyrics using AI-powered analysis",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Initialize the database on startup."""
    await init_db()

@app.post("/api/agent", response_model=AgentResponse)
async def get_lyrics(request: MessageRequest):
    """
    Get lyrics and extract vocabulary for a song.
    
    Args:
        request (MessageRequest): Request containing the song query
        
    Returns:
        AgentResponse: Lyrics and extracted vocabulary
    """
    try:
        # Run the agent to get lyrics and vocabulary
        result = await run_agent(request.message_request)
        
        if result.get("error"):
            raise HTTPException(status_code=404, detail=result["error"])
            
        # Store results in database
        await add_song_and_vocabulary(
            title=result.get("title", "Unknown"),
            artist=result.get("artist", "Unknown"),
            lyrics=result["lyrics"],
            language="japanese",  # Hardcoded for now
            vocabulary_list=result["vocabulary"]
        )
        
        return AgentResponse(
            lyrics=result["lyrics"],
            vocabulary=result["vocabulary"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 