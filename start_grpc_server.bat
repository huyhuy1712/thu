@echo off
REM Start gRPC Server
title gRPC Server
cd /d d:\teledeaf-care-ai-service
python -m grpc_service.server.main
pause
