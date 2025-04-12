from fastapi import FastAPI, UploadFile, File
from comps import ServiceRoleType, ServiceType, register_microservice
from comps.cores.proto.api_protocol import (
    ServiceRequest,
    ServiceResponse
)
import numpy as np
import soundfile as sf
from pydantic import BaseModel
import os
import tempfile
from fastapi import HTTPException
from fastapi.responses import FileResponse

# Create FastAPI app
app = FastAPI()

# Audio configuration
SAMPLE_RATE = 16000
DURATION = 3  # seconds

class TTSRequest(BaseModel):
    text: str
    reference_audio: str

def generate_sine_wave(frequency=440, duration=DURATION, sample_rate=SAMPLE_RATE):
    """Generate a simple sine wave audio signal."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = np.sin(2 * np.pi * frequency * t)
    return audio

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """Generate speech from text (placeholder implementation)."""
    try:
        # Generate sine wave
        audio = generate_sine_wave()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            sf.write(temp_file.name, audio, SAMPLE_RATE)
            return FileResponse(
                temp_file.name,
                media_type='audio/wav',
                filename='output.wav'
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# Register the service
register_microservice(
    name="gptsovits-service",
    service_role=ServiceRoleType.MICROSERVICE,
    service_type=ServiceType.TTS,
    port=int(os.getenv('GPT_SOVITS_PORT', 8000))
) 