from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime

class BaseRequest(BaseModel):
    """Base request model with common fields"""
    request_id: str = Field(..., description="Unique request identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Request timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class BaseResponse(BaseModel):
    """Base response model with common fields"""
    request_id: str = Field(..., description="Request identifier this response corresponds to")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    status: str = Field(..., description="Response status (success/error)")
    message: Optional[str] = Field(None, description="Response message")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class ErrorResponse(BaseResponse):
    """Error response model"""
    error_code: str = Field(..., description="Error code")
    error_details: Optional[Dict[str, Any]] = Field(None, description="Detailed error information")

class ServiceRequest(BaseRequest):
    """Service request model"""
    service_name: str = Field(..., description="Name of the service to invoke")
    method: str = Field(..., description="Method to call")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Method parameters")

    @validator('service_name')
    def validate_service_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Service name cannot be empty")
        return v.strip()

    @validator('method')
    def validate_method(cls, v):
        if not v or not v.strip():
            raise ValueError("Method name cannot be empty")
        return v.strip()

class ServiceResponse(BaseResponse):
    """Service response model"""
    result: Optional[Any] = Field(None, description="Service method result")
    execution_time: float = Field(..., description="Execution time in seconds")

class HealthCheckRequest(BaseRequest):
    """Health check request model"""
    service_name: Optional[str] = Field(None, description="Specific service to check")

class HealthCheckResponse(BaseResponse):
    """Health check response model"""
    service_status: Dict[str, str] = Field(..., description="Status of each service")
    system_status: Dict[str, Any] = Field(..., description="System-wide status information")

class ServiceInfo(BaseModel):
    """Service information model"""
    name: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    status: str = Field(..., description="Service status")
    endpoints: List[str] = Field(..., description="Available endpoints")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional service metadata")

class ServiceDiscoveryRequest(BaseRequest):
    """Service discovery request model"""
    service_type: Optional[str] = Field(None, description="Filter by service type")
    role: Optional[str] = Field(None, description="Filter by service role")

class ServiceDiscoveryResponse(BaseResponse):
    """Service discovery response model"""
    services: List[ServiceInfo] = Field(..., description="List of discovered services") 