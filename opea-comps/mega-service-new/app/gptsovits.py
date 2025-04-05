from comps import ServiceRoleType, ServiceType, register_microservice
from comps.cores.proto.api_protocol import (
    ChatCompletionRequest, 
    ChatCompletionResponse
)
import torch
import numpy as np
import librosa
import jax
import os

# Get port from environment variable with fallback
GPT_SOVITS_PORT = int(os.getenv('GPT_SOVITS_PORT', 8889))

@register_microservice(
    name="GPTSoVITS",
    service_role=ServiceRoleType.MEGASERVICE,
    service_type=ServiceType.LLM,
    host="0.0.0.0",
    port=GPT_SOVITS_PORT,  # Use environment variable
    endpoint="/gpt-sovits",
    input_datatype=ChatCompletionRequest,
    output_datatype=ChatCompletionResponse,
)
async def handle_request(request: ChatCompletionRequest) -> ChatCompletionResponse:
    # Verify all imports are working
    versions = {
        'numpy': np.__version__,
        'torch': torch.__version__,
        'librosa': librosa.__version__,
        'jax': jax.__version__
    }
    
    return ChatCompletionResponse(
        model="gpt-sovits",
        choices=[{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": f"GPT-SoVITS service is running. Package versions: {versions}"
            },
            "finish_reason": "stop"
        }],
        usage={
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    )

if __name__ == '__main__':
    print(f'Starting GPT-SoVITS service on port {GPT_SOVITS_PORT}...')
    from comps import opea_microservices
    service = opea_microservices["GPTSoVITS"]
    service.start() 