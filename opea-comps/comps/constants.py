"""
Common constants used across OPEA services.
"""
from enum import Enum

class ServiceRoleType(Enum):
    """Service role types."""
    MEGASERVICE = "megaservice"
    MICROSERVICE = "microservice"
    GATEWAY = "gateway"
    DATABASE = "database"
    CACHE = "cache"
    MESSAGE_BROKER = "message_broker"

class ServiceType(Enum):
    """Service types."""
    LLM = "llm"
    EMBEDDING = "embedding"
    VECTOR_DB = "vector_db"
    TTS = "tts"
    STT = "stt"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"
    DATA = "data"
    API = "api"
    WEB = "web"
    MOBILE = "mobile"
    DESKTOP = "desktop"
    IOT = "iot"
    EDGE = "edge"
    CLOUD = "cloud"
    HYBRID = "hybrid"

# Default service configuration
DEFAULT_SERVICE_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": False,
    "reload": True
}

# API endpoints
API_PREFIX = "/api/v1"
HEALTH_CHECK_ENDPOINT = "/health"
METRICS_ENDPOINT = "/metrics"

# Service status codes
SERVICE_STATUS = {
    "RUNNING": "running",
    "STOPPED": "stopped",
    "ERROR": "error",
    "STARTING": "starting",
    "STOPPING": "stopping"
} 