from fastapi import FastAPI, HTTPException
from comps import ServiceRoleType, ServiceType, register_microservice
from comps.cores.proto.api_protocol import (
    ServiceRequest,
    ServiceResponse
)
import os
import time
import requests
import torch
import numpy as np
import librosa
import soundfile as sf
from typing import Optional
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI()

# Get port from environment variable with fallback
TTS_PORT = int(os.getenv('TTS_PORT', 8000))

# Configuration
AUDIO_DIR = os.getenv('AUDIO_DIR', '/app/audio')
MODEL_PATH = os.getenv('MODEL_PATH', '/app/tts/models')
CACHE_DIR = os.getenv('CACHE_DIR', '/app/tts/cache')
SAMPLE_RATE = 16000  # Standard sample rate for speech processing
GPT_SOVITS_URL = "http://gptsovits-service:8000"  # Internal Docker network URL

# Ensure cache directory exists and has correct permissions
os.makedirs(CACHE_DIR, exist_ok=True)
os.chmod(CACHE_DIR, 0o777)  # Make directory writable by all

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

def generate_speech(text: str, reference_features: dict) -> np.ndarray:
    """Generate speech from text using GPT-SoVITS model"""
    try:
        # Prepare request to GPT-SoVITS service
        request_data = {
            "text": text,
            "reference_audio": reference_features.get("reference_audio")
        }
        
        # Send request to GPT-SoVITS service
        response = requests.post(
            f"{GPT_SOVITS_URL}/tts",
            json=request_data,
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"GPT-SoVITS service returned error: {response.text}")
            
        # Get the generated audio from the response
        result = response.json()
        if not result.get("status") == "success":
            raise Exception(f"GPT-SoVITS service failed: {result.get('message')}")
            
        # Load the generated audio file
        output_path = result.get("result", {}).get("output_path")
        if not output_path:
            raise Exception("No output path in GPT-SoVITS response")
            
        audio, sr = librosa.load(output_path, sr=SAMPLE_RATE)
        return audio
        
    except Exception as e:
        raise Exception(f"Error generating speech: {str(e)}")

@app.post("/tts")
@register_microservice(
    name="TTS",
    service_role=ServiceRoleType.MICROSERVICE,
    service_type=ServiceType.TTS,
    host="0.0.0.0",
    port=TTS_PORT,
    endpoint="/tts",
    input_datatype=ServiceRequest,
    output_datatype=ServiceResponse,
)
async def handle_request(request: ServiceRequest) -> ServiceResponse:
    start_time = time.time()
    
    try:
        # Get parameters from request
        text = request.parameters.get("text")
        reference_audio = request.parameters.get("reference_audio")
        
        if not text or not reference_audio:
            raise ValueError("Both text and reference_audio are required")
            
        # Validate reference audio file
        ref_audio_path = os.path.join(AUDIO_DIR, reference_audio)
        if not os.path.exists(ref_audio_path):
            raise FileNotFoundError(f"Reference audio file not found: {reference_audio}")
            
        # Process reference audio
        reference_features = process_audio(ref_audio_path)
        reference_features["reference_audio"] = ref_audio_path
        
        # Generate speech using GPT-SoVITS
        generated_audio = generate_speech(text, reference_features)
        
        # Ensure cache directory exists
        os.makedirs(CACHE_DIR, exist_ok=True)
        
        # Save output audio
        output_path = os.path.join(CACHE_DIR, "output.wav")
        sf.write(output_path, generated_audio, SAMPLE_RATE)
        
        # Set permissions on output file
        os.chmod(output_path, 0o666)  # Make file readable and writable by all
        
        execution_time = time.time() - start_time
        
        return ServiceResponse(
            request_id=request.request_id,
            status="success",
            message="TTS request processed successfully",
            result={
                "text": text,
                "reference_audio": reference_audio,
                "output_path": output_path
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

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if required directories exist
        for dir_path in [AUDIO_DIR, MODEL_PATH, CACHE_DIR]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                os.chmod(dir_path, 0o777)  # Make directory writable by all
                
        # Check GPT-SoVITS service health
        response = requests.get(f"{GPT_SOVITS_URL}/health", timeout=5)
        if response.status_code != 200:
            raise Exception("GPT-SoVITS service is not healthy")
                
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    print(f'Starting TTS service on port {TTS_PORT}...')
    from comps import opea_microservices
    service = opea_microservices["TTS"]
    service.start() 