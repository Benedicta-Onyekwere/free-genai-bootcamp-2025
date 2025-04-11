from fastapi import FastAPI, UploadFile, File
from comps import ServiceRoleType, ServiceType, register_microservice
from comps.cores.proto.api_protocol import (
    ServiceRequest,
    ServiceResponse
)
import torch
import numpy as np
import librosa
import os
import time
from typing import Optional
import soundfile as sf
from pydantic import BaseModel
import sys
sys.path.append('/app')
from GPT_SoVITS.inference_main import GPT_SoVITS_inference
from fastapi import HTTPException
import torchaudio
import tempfile
import logging
from pathlib import Path

# Create FastAPI app
app = FastAPI()

# Get port from environment variable with fallback
GPT_SOVITS_PORT = int(os.getenv('GPT_SOVITS_PORT', 8000))

# Audio processing configuration
AUDIO_DIR = "/app/audio"
SAMPLE_RATE = 16000  # Standard sample rate for speech processing
OUTPUT_DIR = "/app/output"
MODEL_DIR = "/app/models"

# Model paths
GPT_MODEL_PATH = "/app/models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt"
SOVITS_MODEL_PATH = "/app/models/s2G488k.pth"
BERT_MODEL_PATH = "/app/models/s2D488k.pth"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.chmod(OUTPUT_DIR, 0o777)

# Force CPU usage
if torch.cuda.is_available():
    print("Warning: CUDA is available but forcing CPU mode")
    torch.set_default_tensor_type(torch.FloatTensor)
    torch.backends.cudnn.enabled = False
else:
    print("Running on CPU")

# Set device to CPU
device = torch.device("cpu")
print(f"Using device: {device}")

# Initialize model globally
try:
    gpt_sovits_model = GPT_SoVITS_inference(
        gpt_path=GPT_MODEL_PATH,
        sovits_path=SOVITS_MODEL_PATH,
        bert_path=BERT_MODEL_PATH,
        device=device
    )
    print(f"GPT-SoVITS model initialized successfully on {device}")
except Exception as e:
    print(f"Error initializing GPT-SoVITS model: {e}")
    gpt_sovits_model = None

class TTSRequest(BaseModel):
    text: str
    reference_audio: str

def process_audio(audio_path: str) -> dict:
    """Process audio file and extract features"""
    try:
        # Load audio file
        audio, sr = librosa.load(audio_path, sr=SAMPLE_RATE)
        
        # Extract features
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr)
        
        # Convert to decibels
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        return {
            "audio": audio,
            "sample_rate": sr,
            "mfccs": mfccs,
            "mel_spec": mel_spec_db
        }
    except Exception as e:
        raise Exception(f"Error processing audio: {str(e)}")

async def generate_speech(text: str, reference_audio: str) -> str:
    """Generate speech from text using GPT-SoVITS."""
    if gpt_sovits_model is None:
        raise HTTPException(status_code=500, detail="GPT-SoVITS model not initialized")

    try:
        # Load and process reference audio
        ref_audio_path = os.path.join(AUDIO_DIR, reference_audio)
        if not os.path.exists(ref_audio_path):
            raise HTTPException(status_code=404, detail=f"Reference audio file not found: {reference_audio}")

        # Ensure output directory exists with correct permissions
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.chmod(OUTPUT_DIR, 0o777)

        output_path = os.path.join(OUTPUT_DIR, "output.wav")
        
        # Generate speech using GPT-SoVITS
        gpt_sovits_model.inference(
            text=text,
            ref_audio_path=ref_audio_path,
            output_path=output_path,
            prompt_text=text[:100],  # Use first 100 chars as prompt
            prompt_language="en",
            top_k=3,
            top_p=0.7,
            temperature=0.7
        )

        # Ensure output file has correct permissions
        os.chmod(output_path, 0o666)
        
        return output_path
    except Exception as e:
        print(f"Error generating speech: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate speech: {str(e)}")

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """Convert text to speech using GPT-SoVITS model"""
    try:
        start_time = time.time()
        
        # Validate reference audio file
        ref_audio_path = os.path.join(AUDIO_DIR, request.reference_audio)
        if not os.path.exists(ref_audio_path):
            raise FileNotFoundError(f"Reference audio file not found: {request.reference_audio}")
            
        # Process reference audio
        reference_features = process_audio(ref_audio_path)
        reference_features["reference_audio"] = request.reference_audio
        
        # Generate speech
        output_path = await generate_speech(request.text, request.reference_audio)
        
        execution_time = time.time() - start_time
        
        return {
            "status": "success",
            "message": "TTS request processed successfully",
            "result": {
                "text": request.text,
                "reference_audio": request.reference_audio,
                "output_path": output_path
            },
            "execution_time": execution_time
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/gpt-sovits")
@register_microservice(
    name="GPTSoVITS",
    service_role=ServiceRoleType.MEGASERVICE,
    service_type=ServiceType.LLM,
    host="0.0.0.0",
    port=GPT_SOVITS_PORT,
    endpoint="/gpt-sovits",
    input_datatype=ServiceRequest,
    output_datatype=ServiceResponse,
)
async def handle_request(request: ServiceRequest) -> ServiceResponse:
    start_time = time.time()
    
    try:
        # Get audio file path from request parameters
        audio_file = request.parameters.get("audio_file")
        if not audio_file:
            raise ValueError("No audio file specified in parameters")
            
        audio_path = os.path.join(AUDIO_DIR, audio_file)
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
            
        # Process audio
        audio_features = process_audio(audio_path)
        
        # Verify all imports are working
        versions = {
            'numpy': np.__version__,
            'torch': torch.__version__,
            'librosa': librosa.__version__
        }
        
        execution_time = time.time() - start_time
        
        return ServiceResponse(
            request_id=request.request_id,
            status="success",
            message="Audio processed successfully",
            result={
                "model": "gpt-sovits",
                "versions": versions,
                "audio_features": audio_features
            },
            execution_time=execution_time
        )
        
    except Exception as e:
        execution_time = time.time() - start_time
        return ServiceResponse(
            request_id=request.request_id,
            status="error",
            message=str(e),
            result=None,
            execution_time=execution_time
        )

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """Upload audio file to the service"""
    try:
        # Save the uploaded file
        file_path = os.path.join(AUDIO_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            
        return {
            "status": "success",
            "message": f"File {file.filename} uploaded successfully",
            "file_path": file_path
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if required directories exist
        for dir_path in [AUDIO_DIR, OUTPUT_DIR, MODEL_DIR]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                os.chmod(dir_path, 0o777)
                
        # Check if model files exist
        for model_path in [GPT_MODEL_PATH, SOVITS_MODEL_PATH, BERT_MODEL_PATH]:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
                
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    print(f'Starting GPT-SoVITS service on port {GPT_SOVITS_PORT}...')
    from comps import opea_microservices
    service = opea_microservices["GPTSoVITS"]
    service.start() 