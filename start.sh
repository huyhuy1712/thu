#!/bin/bash
# Start script for Render deployment

echo "🚀 Starting Teledeaf AI Service on Render..."

# Start FastAPI server
if [ "$SERVICE_TYPE" = "api" ]; then
    echo "📡 Starting FastAPI API Server..."
    exec python -m app.api.api_main
    
# Start gRPC server  
elif [ "$SERVICE_TYPE" = "grpc" ]; then
    echo "🔌 Starting gRPC Server..."
    exec python -m grpc_service.server.main
    
# Default: Start FastAPI
else
    echo "📡 Starting FastAPI API Server (default)..."
    exec python -m app.api.api_main
fi
