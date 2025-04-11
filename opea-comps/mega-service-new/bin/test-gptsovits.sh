#!/bin/bash

# Test health endpoint
echo "Testing health endpoint..."
curl http://localhost:8000/health
echo -e "\n\n"

# Test processing an audio file
echo "Testing audio processing..."
curl -X POST http://localhost:8000/gpt-sovits \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "test-123",
    "service_name": "GPTSoVITS",
    "method": "process",
    "parameters": {
      "audio_file": "andrew-ref-10s.wav"
    }
  }'
echo -e "\n\n"

# Test uploading a new audio file
echo "Testing audio upload..."
curl -X POST http://localhost:8000/upload-audio \
  -F "file=@audio/andrew-ref-10s.wav"
echo -e "\n\n" 