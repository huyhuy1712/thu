@echo off
REM Start REST API Server
title REST API Server
cd /d d:\teledeaf-care-ai-service
python -m app.api.api_main
pause
