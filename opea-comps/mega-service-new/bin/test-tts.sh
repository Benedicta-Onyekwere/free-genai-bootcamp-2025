#!/bin/bash

# Test TTS endpoint
echo "Testing TTS endpoint..."
curl -X POST http://localhost:8001/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a test of the TTS service",
    "reference_audio": "test.wav"
  }' \
  --output audio/tts-output.wav

echo "Test completed. Check audio/tts-output.wav for the generated audio." 