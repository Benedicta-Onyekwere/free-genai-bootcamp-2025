# Ollama Server Setup

This directory contains the configuration for running an Ollama server using Docker Compose.

## Quick Start

1. **Prerequisites**
   - Docker Desktop installed and running
   - Docker Compose v2 or later

2. **Set Environment Variables**
   ```bash
   HOST_IP=<your-local-ip>  # Your machine's local IP address (see "Getting Your IP" below)
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
   - Check server logs for successful startup

## Getting Your IP

### macOS
```sh
ipconfig getifaddr en0  # For Wi-Fi
# or
ipconfig getifaddr en1  # For Ethernet
```

### Linux
```sh
sudo apt install net-tools
ifconfig
# or
echo $(hostname -I | awk '{print $1}')
```

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

### Docker Compose File
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
    networks:
      - default

networks:
  default:
    driver: bridge
```

### Advanced Configuration
To persist models between container restarts:
```yaml
services:
  ollama-server:
    # ... other configuration ...
    volumes:
      - ./models:/root/.ollama/models
```

## System Information

### Server Details
- Version: 0.6.1
- Memory: 7.1 GB available out of 7.7 GB total
- Mode: CPU (no GPU acceleration)
- Internal Port: 11434
- External Port: 8008 (configurable)

### Technical Notes
- Bridge network mode enables host machine access to Ollama API
- Models must be explicitly downloaded using `/api/pull`
- Default context length: 2048
- Request queue limit: 512
- New SSH key generated on first run
- Models are removed when container is destroyed (unless using volume mount)

## Troubleshooting

- If you see YAML syntax errors, check file indentation
- Verify Docker Desktop is running
- Ensure ports are not in use
- Check server logs for startup issues
- Verify environment variables are set correctly