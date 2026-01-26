#!/bin/bash
# Start both gRPC and FastAPI in the same container
# For Render free tier that doesn't support separate gRPC service

echo "🚀 Starting Teledeaf AI Service..."

# Start gRPC server in background
echo "🔌 Starting gRPC server in background..."
python -m grpc_service.server.main &

# Wait a bit for gRPC to start
sleep 2

# Start FastAPI in foreground
echo "📡 Starting FastAPI server..."
exec python -m app.api.api_main
