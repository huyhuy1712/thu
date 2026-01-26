# Multi-stage build for Teledeaf AI Service
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application code
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Expose ports
EXPOSE 50051 8000

# Default: Run FastAPI server (Render sẽ override)
CMD ["python", "-m", "app.api.api_main"]
