from comps import ServiceRoleType, ServiceType, register_microservice
from comps.cores.proto.api_protocol import (
    ChatCompletionRequest, 
    ChatCompletionResponse
)

@register_microservice(
    name="Chat",
    service_role=ServiceRoleType.MEGASERVICE,
    service_type=ServiceType.LLM,
    host="0.0.0.0",
    port=8888,
    endpoint="/james-is-great",
    input_datatype=ChatCompletionRequest,
    output_datatype=ChatCompletionResponse,
)
async def handle_request(request: ChatCompletionRequest) -> ChatCompletionResponse:
    print('handle_request')
    return ChatCompletionResponse(
        model="test-model",
        choices=[{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "James is great!"
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
    print('main')
    from comps import opea_microservices
    service = opea_microservices["Chat"]
    service.start()