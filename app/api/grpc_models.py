from typing import List, Optional
from pydantic import BaseModel


class SignRecognitionRequest(BaseModel):
    """Request model for sign recognition via gRPC"""
    frames: List[list]  # List of frame data (video frames)
    platform: str  # "web" or other platform
    language_code: str  # "vn" or "au"
    previous_word: Optional[str] = ""


class SignRecognitionResponse(BaseModel):
    """Response model for sign recognition"""
    recognized_sign: str
    confidence: float
    platform: str
    language_code: str


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    grpc_server: str
