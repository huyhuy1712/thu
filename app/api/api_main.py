"""
REST API Server for Sign Language Recognition via gRPC
Runs on port 8000 and communicates with gRPC server on port 50051
"""
import uvicorn
from app.api.grpc_api import api_app


if __name__ == "__main__":
    print(" Starting Sign Language Recognition REST API...")
    print(" API Server running on http://localhost:8000")
    print(" Docs available at http://localhost:8000/docs")
    print(" gRPC Server: localhost:50051")
    
    uvicorn.run(
        api_app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
