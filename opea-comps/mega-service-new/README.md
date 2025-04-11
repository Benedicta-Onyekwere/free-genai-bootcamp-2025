# Mega Service Implementation

This project implements a Text-to-Speech (TTS) system using GPT-SoVITS (Generative Pre-trained Transformer - Speaker Voice Identity Transfer System) for voice cloning and speech synthesis. The system consists of two main services that work together to provide voice cloning and text-to-speech capabilities.

## Services Overview

### GPT-SoVITS Service
GPT-SoVITS (Generative Pre-trained Transformer - Speaker Voice Identity Transfer System) is a voice cloning and speech synthesis system that can:
- Clone a speaker's voice from a short reference audio
- Generate speech in the cloned voice from text input
- Transfer voice characteristics between speakers

The service provides the following endpoints:
- `/health` - Health check endpoint
- `/process` - Process reference audio and generate speech
- `/tts` - Text-to-speech endpoint

### TTS Service
TTS (Text-to-Speech) is a service that converts written text into spoken words. Our implementation:
- Takes text input and a reference audio file
- Processes the reference audio to extract voice characteristics
- Uses GPT-SoVITS to generate speech in the reference voice
- Returns the generated audio file

The service provides the following endpoints:
- `/health` - Health check endpoint
- `/tts` - Main text-to-speech endpoint
- `/status` - Check status of audio generation

## Implementation Details

### Project Structure
```
/opea-comps
├── comps/                      # Shared components and protocols
│   ├── cores/
│   │   └── proto/             # API protocol definitions
│   └── constants.py           # Shared constants
├── mega-service-new/          # Main service implementation
│   ├── app/                  # Application code
│   │   ├── service/         # GPT-SoVITS service code
│   │   └── tts/            # TTS service implementation
│   ├── bin/                 # Utility scripts
│   ├── models/             # Model files and weights
│   ├── audio/             # Reference audio files
│   └── output/            # Generated audio files
└── setup.py               # Package configuration
```

### Docker Configuration
- Separate Dockerfiles for each service:
  - `Dockerfile.gptsovits` for GPT-SoVITS service
  - `Dockerfile.tts` for TTS service
- Shared volume mounts for:
  - `/app/audio` - Reference audio files
  - `/app/output` - Generated audio files
  - `/app/models` - Model files
- Environment variables:
  - `GPT_SOVITS_URL` - URL of GPT-SoVITS service
  - `MODEL_PATH` - Path to model files
  - `AUDIO_PATH` - Path to audio files
  - `OUTPUT_PATH` - Path to output files

## Service Integration

### GPT-SoVITS Implementation
The GPT-SoVITS service is the core component that:
1. Processes reference audio to extract voice characteristics
2. Generates speech in the target voice
3. Provides voice cloning capabilities
4. Handles model loading and inference

### TTS Integration
The TTS service acts as a high-level interface that:
1. Receives text input and reference audio
2. Forwards the reference audio to GPT-SoVITS for processing
3. Uses the processed voice characteristics to generate speech
4. Returns the generated audio to the user

This integration allows for a seamless user experience where:
- Users only need to interact with the TTS service
- The complexity of voice cloning is abstracted away
- Multiple voice models can be managed efficiently
- Audio processing is optimized through caching

## Getting Started

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd mega-service-new
   ```

2. **Set Up Environment**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -e ../opea-comps
   pip install -r app/requirements.txt
   ```

3. **Download Models**
   ```bash
   # Run the model download script
   ./bin/download-models.sh
   ```

4. **Start Services**
   ```bash
   # Start all services using Docker Compose
   docker-compose up -d
   ```

## Testing

1. **Test GPT-SoVITS Service**
   ```bash
   ./bin/test-gptsovits.sh
   ```

2. **Test TTS Service**
   ```bash
   ./bin/test-tts.sh
   ```

3. **Test Service Integration**
   ```bash
   # Test the complete flow from text to speech
   curl -X POST http://localhost:8001/tts \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Hello, this is a test.",
       "reference_audio": "path/to/reference.wav"
     }'
   ```

## Challenges and Solutions

1. **Module Import Issues**
   - Problem: GPT-SoVITS module not found in Docker container
   - Solution: Created proper Python package structure with `setup.py` and `__init__.py` files
   - Added `comps` directory for shared components
   - Implemented proper import paths in service code

2. **Docker Configuration**
   - Problem: Missing dependencies and incorrect paths
   - Solution: Created separate Dockerfiles for each service
   - Added proper volume mounts for shared directories

3. **Service Communication**
   - Problem: Inconsistent API protocols between services
   - Solution: Created standardized protocol definitions in `comps/cores/proto/`
   - Implemented proper request/response handling

4. **Model Management**
   - Problem: Large model files and version control
   - Solution: Created separate `models` directory
   - Added proper `.gitignore` rules for model files
   - Implemented model download scripts

5. **Service Integration**
   - Problem: Complex interaction between TTS and GPT-SoVITS services
   - Solution: Created clear API contracts and error handling
   - Implemented proper status tracking and monitoring
   - Added caching for processed voice models

## Current Status

### Working Components
- Service infrastructure is fully set up
- Docker containers are properly configured
- Basic audio processing is functional
- Test endpoints are working
- Error handling is implemented
- Service integration is complete

### In Progress
- Actual GPT-SoVITS model integration
- Voice cloning implementation
- Speech synthesis quality improvements
- Performance optimization

### Placeholder Implementation
Currently using a simple sine wave (440 Hz) as placeholder audio while implementing the full GPT-SoVITS model integration. This allows us to:
- Verify service communication
- Test the infrastructure
- Ensure proper file handling
- Validate the testing framework

## Next Steps
1. Implement actual GPT-SoVITS model
2. Add voice cloning capabilities
3. Improve speech synthesis quality
4. Add more comprehensive testing
5. Implement caching and optimization 