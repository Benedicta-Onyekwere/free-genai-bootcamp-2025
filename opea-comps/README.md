# Ollama Server Setup

This directory contains the configuration for running an Ollama server using Docker Compose.

## Quick Start

1. **Prerequisites**
   - Docker Desktop installed and running
   - Docker Compose v2 or later

2. **Set Environment Variables**
   ```bash
   # Get your local IP using:
   # macOS: ipconfig getifaddr en0 (WiFi) or en1 (Ethernet)
   # Linux: echo $(hostname -I | awk '{print $1}')
   HOST_IP=<your-local-ip>
   NO_PROXY=localhost
   LLM_ENDPOINT_PORT=8008
   LLM_MODEL_ID="llama3.2:1b"
   ```

3. **Start the Server**
   ```bash
   docker compose up
   ```

4. **Verify Installation**
   - Server should be accessible at `http://localhost:8008`
   - First-time setup will download the Ollama image (~2.6GB)
   - Models are removed when container is destroyed (unless using volume mount)
   - Check server logs for successful startup

## Using the Ollama API

1. **Choose a Model**
   - Browse available models at [Ollama Library](https://ollama.com/library)
   - Example: [llama3.2](https://ollama.com/library/llama3.2)

2. **Download a Model**
   ```sh
   curl http://localhost:8008/api/pull -d '{
     "model": "llama3.2:1b"
   }'
   ```

3. **Make Requests**
   ```sh
   curl http://localhost:8008/api/generate -d '{
     "model": "llama3.2:1b",
     "prompt": "Why is the sky blue?"
   }'
   ```

For full API documentation, visit: https://github.com/ollama/ollama/blob/main/docs/api.md

## Configuration

### Docker Configuration
```yaml
version: '3'
services:
  ollama-server:
    image: ollama/ollama
    container_name: ollama-server
    ports:
      - "${LLM_ENDPOINT_PORT}:11434"
    environment:
      - NO_PROXY=${NO_PROXY}
    # Optional: Persist models between restarts
    volumes:
      - ./models:/root/.ollama/models
    networks:
      - default

networks:
  default:
    driver: bridge
```

## Troubleshooting

- If you see YAML syntax errors, check file indentation
- Verify Docker Desktop is running
- Ensure ports are not in use
- Check server logs for startup issues
- Verify environment variables are set correctly

## Mega Service Development

### Chat Service Implementation
The `mega-service-new` directory contains a microservice implementation using the `comps` framework:

1. **Service Structure**
   ```
   mega-service-new/
   ├── app/
   │   ├── requirements.txt  # Python dependencies
   │   └── chat.py          # Main service implementation
   ├── Dockerfile
   └── docker-compose.yml
   ```

2. **Running the Service**
   ```bash
   cd mega-service-new
   docker compose up
   ```
   
   Configuration:
   - Service runs on port 8888
   - Volume mounting enabled for hot reloading
   - Automatic restart policy enabled

3. **Testing the Endpoint**
   ```bash
   curl -X POST http://localhost:8888/james-is-great \
     -H "Content-Type: application/json" \
     -d '{"messages": [], "model": "test-model", "max_tokens": 100}'
   ```

4. **Development Challenges & Solutions**
   - **Challenge**: 404 errors when accessing the endpoint
     - Solution: Properly implemented the `@register_microservice` decorator pattern
     - Ensured correct endpoint registration with FastAPI through the comps framework

   - **Challenge**: Service registration and startup issues
     - Solution: Corrected the service initialization in `chat.py`
     - Used the correct service name in `opea_microservices` dictionary