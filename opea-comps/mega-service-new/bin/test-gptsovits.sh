#!/bin/bash

# Test health endpoint
echo "Testing health endpoint..."
curl http://localhost:8000/health
echo -e "\n\n"

# Test TTS endpoint
echo "Testing TTS endpoint..."
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a test of the GPT-SoVITS service",
    "reference_audio": "test.wav"
  }' \
  --output audio/output.wav
echo -e "\n\n"

echo "Test completed. Check audio/output.wav for the generated audio." 