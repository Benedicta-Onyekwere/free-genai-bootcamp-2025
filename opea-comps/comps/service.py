from enum import Enum
from typing import Optional, Dict, Any, Type, Callable
from dataclasses import dataclass
from fastapi import FastAPI

class ServiceRoleType(Enum):
    """Enumeration of service role types."""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    WORKER = "worker"
    API = "api"
    MEGASERVICE = "megaservice"

class ServiceType(Enum):
    """Enumeration of service types."""
    GPT_SOVITS = "gpt-sovits"
    TTS = "tts"
    ASR = "asr"
    CHAT = "chat"
    VLLM = "vllm"
    LLM = "llm"

@dataclass
class ServiceConfig:
    """Configuration for a microservice."""
    name: str
    service_role: ServiceRoleType
    service_type: ServiceType
    host: str
    port: int
    endpoint: str
    input_datatype: Type
    output_datatype: Type
    config: Optional[Dict[str, Any]] = None

class Microservice:
    """Base class for microservices."""
    def __init__(self, config: ServiceConfig):
        self.config = config
        self.app = FastAPI()
        self._setup_routes()

    def _setup_routes(self):
        """Setup FastAPI routes for the service."""
        @self.app.post(self.config.endpoint)
        async def handle_request(request: self.config.input_datatype) -> self.config.output_datatype:
            # This will be overridden by the actual implementation
            pass

    def start(self):
        """Start the service."""
        import uvicorn
        uvicorn.run(
            self.app,
            host=self.config.host,
            port=self.config.port,
            reload=True
        )

def register_microservice(
    name: str,
    service_role: ServiceRoleType,
    service_type: ServiceType,
    host: str = "0.0.0.0",
    port: int = 8000,
    endpoint: str = "/",
    input_datatype: Optional[Type] = None,
    output_datatype: Optional[Type] = None,
    config: Optional[Dict[str, Any]] = None
) -> Callable:
    """
    Decorator to register a microservice.
    
    Args:
        name: Name of the service
        service_role: Role of the service
        service_type: Type of the service
        host: Host to run the service on
        port: Port to run the service on
        endpoint: API endpoint
        input_datatype: Input data type
        output_datatype: Output data type
        config: Additional configuration
    """
    def decorator(func: Callable) -> Callable:
        from .opea_microservices import register_service
        service_config = ServiceConfig(
            name=name,
            service_role=service_role,
            service_type=service_type,
            host=host,
            port=port,
            endpoint=endpoint,
            input_datatype=input_datatype,
            output_datatype=output_datatype,
            config=config
        )
        register_service(name, service_config, func)
        return func
    return decorator 