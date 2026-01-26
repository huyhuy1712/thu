# gRPC Sign Recognition Service

This is a gRPC refactor of the existing FastAPI-based sign language recognition service.

## Setup

```bash
python -m pip install -r requirements.txt
python -m grpc_tools.protoc -I "d:\teledeaf-care-ai-service\grpc_service\protos" --python_out="d:\teledeaf-care-ai-service\grpc_service" --grpc_python_out="d:\teledeaf-care-ai-service\grpc_service" "d:\teledeaf-care-ai-service\grpc_service\protos\sign_recognition.proto"
```

## Set up and start
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

## Gen the proto files
python -m grpc_tools.protoc -I grpc_service\protos --python_out=grpc_service --grpc_python_out=grpc_service grpc_service\protos\sign_recognition.proto


## Start the server uses gRPC
python -m grpc_service.server.main

## Start the server uses REST API
serve run app.main:deployment --reload

## run file comparation

## Testing

## both 
python comparison_test.py --requests 10
## fasapi
python comparison_test.py --mode fastapi --requests 10
## grpc
python comparison_test.py --mode grpc --requests 10


## Test API 

## Run the Server

```bash
python -m grpc_service.server.main
```

## Test Client

```bash
python -m grpc_service.client.test_client
```

## REST API Server (For Frontend)

The REST API server provides HTTP endpoints that wrap the gRPC service, allowing frontend applications to call it directly via REST/JSON.

### Start the REST API Server

```bash
python -m app.api.api_main
```

The API server will:
- Run on `http://localhost:8000`
- Connect to gRPC server on `localhost:50051`
- Provide Swagger docs at `http://localhost:8000/docs`

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Recognize Sign Language
```bash
curl -X POST http://localhost:8000/v1/api/sign-language/recognize \
  -H "Content-Type: application/json" \
  -d '{
    "frames": [[...]],
    "platform": "web",
    "language_code": "vn",
    "previous_word": ""
  }'
```

**Request Body:**
```json
{
  "frames": [[frame_data_list]],
  "platform": "web",
  "language_code": "vn",
  "previous_word": ""
}
```

**Response:**
```json
{
  "recognized_sign": "hello",
  "confidence": 0.95,
  "platform": "web",
  "language_code": "vn"
}
```

## Running Both Services

### Terminal 1: Start gRPC Server
```bash
python -m grpc_service.server.main
```

### Terminal 2: Start REST API Server
```bash
python -m app.api.api_main
```

Now the frontend can call the REST API at port 8000!

## Notes
- The gRPC server reuses the existing model loading and inference pipeline from `app/`.
- The REST API server acts as a gateway between HTTP clients and the gRPC service.
- Ensure you run commands from the workspace root so imports like `app.service.model_service` resolve correctly.
- Set `GRPC_PORT` env var to change the gRPC listening port (default: 50051).