from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from ray import serve
from app.loader.models_loaders import initialize_all_models
from app.service.model_service import process_prediction_combine_api
from .api.models import RecognitionRequest
from http import HTTPStatus
from pydantic import ValidationError
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


ASCII_PATH = Path(__file__).parent / "src" / "welcome_icon.txt"

ASCII_ART = ASCII_PATH.read_text(encoding="utf-8")

@serve.deployment(
    num_replicas=1,  # Number of model replicas for load balancing
    ray_actor_options={"num_cpus": 2}  # Resources per replica
)
@serve.ingress(app)
class SignLanguageModel:

    def __init__(self):
        """Initialize your AI model here"""
        self.model_name = "Sign Language Recognizer with Siformer"
        self.version = "1.0"
        self.models, self.device = initialize_all_models()

    @app.get("/")
    def home(self):

          return Response(
            content=ASCII_ART.replace("version", self.version),
            media_type="text/plain; charset=utf-8"
        )


    @app.post("/v3/api/sign-language/recognize")
    def recognize_sign_language(self, payload: RecognitionRequest, platform: str, language_code: str):
    
        try:
            import time
            start_total = time.time()
            
            print("🔄 Processing sign to text request...")
            
            # Time to create the payload
            start_payload = time.time()
            request_data = {
                "frames": payload.frames,
                "previous_word": payload.previous_word or ""
            }
            payload_time = (time.time() - start_payload) * 1000
            print(f"⏱️  Payload creation: {payload_time:.2f} ms")
            
            # Time for model inference
            start_inference = time.time()
            data, status_code = process_prediction_combine_api(self.models , self.device, request_data, platform, language_code)
            inference_time = (time.time() - start_inference) * 1000
            print(f"⏱️  Model inference: {inference_time:.2f} ms")
            
            total_time = (time.time() - start_total) * 1000
            print(f"⏱️  Total processing: {total_time:.2f} ms")
            
            return JSONResponse(content={
                "data": data
            }, status_code=status_code)

        except ValidationError as e:
            return JSONResponse(
                content={"error": e.errors()},
                status_code=HTTPStatus.BAD_REQUEST
            )

# Export for serve CLI
deployment = SignLanguageModel.bind()

