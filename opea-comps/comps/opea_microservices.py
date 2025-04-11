from typing import Dict, Any, Callable
from .service import ServiceConfig, Microservice

# Global registry for all microservices
opea_microservices: Dict[str, Microservice] = {}

def register_service(name: str, config: ServiceConfig, handler: Callable) -> None:
    """
    Register a new microservice.
    
    Args:
        name: Name of the service
        config: Service configuration
        handler: Request handler function
    """
    service = Microservice(config)
    service.app.post(config.endpoint)(handler)
    opea_microservices[name] = service

def get_service(name: str) -> Microservice:
    """
    Get a registered microservice by name.
    
    Args:
        name: Name of the service
        
    Returns:
        The registered microservice
        
    Raises:
        KeyError: If the service is not found
    """
    if name not in opea_microservices:
        raise KeyError(f"Service '{name}' not found")
    return opea_microservices[name] 