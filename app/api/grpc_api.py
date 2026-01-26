from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from pathlib import Path

# Import model service
from app.loader.models_loaders import initialize_all_models
from app.service.model_service import process_prediction_combine_api
from app.api.grpc_models import SignRecognitionRequest, HealthCheckResponse

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
api_app = FastAPI(
    title="Sign Language Recognition API",
    description="REST API for Sign Language Recognition Service (Standalone)",
    version="1.0.0"
)

# Add CORS middleware
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models
loaded_models = None
device = None


@api_app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    global loaded_models, device
    try:
        logger.info("Loading models...")
        loaded_models, device = initialize_all_models()
        logger.info("✅ REST API Server started successfully (Standalone mode)")
        logger.info(f"Device: {device}")
    except Exception as e:
        logger.error(f"❌ Failed to start API server: {e}")
        raise


@api_app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("REST API Server shutting down...")


@api_app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    if loaded_models is None:
        raise HTTPException(
            status_code=503,
            detail="Models not loaded"
        )
    return HealthCheckResponse(
        status="healthy",
        message="REST API server is running (Standalone mode)",
        grpc_server="N/A - Running standalone"
    )


@api_app.post("/v1/api/sign-language/recognize")
async def recognize_sign_language(request: SignRecognitionRequest):
    """
    Recognize sign language from video frames
    
    Args:
        request: SignRecognitionRequest with frames, platform, language_code
        
    Returns:
        JSON response with recognized signs and confidence scores
    """
    try:
        if loaded_models is None or device is None:
            raise HTTPException(
                status_code=503,
                detail="Models not loaded"
            )
        
        # Prepare request data - parse flat coordinate list into structured format
        frames_structured = []
        for frame in request.frames:
            # frame is a list of [x, y, z] coordinates: [midEyes, leftHand points, rightHand points, lip points]
            # Expected: 1 midEyes + 21 leftHand + 21 rightHand + optional lip points
            
            logger.info(f"📊 FastAPI received frame with {len(frame)} points")
            
            # Convert flat list to structured dict with proper coordinate objects
            if len(frame) < 43:  # Minimum: 1 midEyes + 21 left + 21 right
                logger.warning(f"Incomplete frame data: {len(frame)} points, expected at least 43")
            
            structured_frame = {
                "midEyes": {"x": frame[0][0], "y": frame[0][1], "z": frame[0][2]} if len(frame) > 0 else {},
                "leftHand": [{"x": p[0], "y": p[1], "z": p[2]} for p in frame[1:22]] if len(frame) > 1 else [],
                "rightHand": [{"x": p[0], "y": p[1], "z": p[2]} for p in frame[22:43]] if len(frame) > 22 else [],
                "lip": [{"x": p[0], "y": p[1], "z": p[2]} for p in frame[43:]] if len(frame) > 43 else []
            }
            
            logger.info(f"🔄 Converted to: midEyes={structured_frame['midEyes']}, leftHand={len(structured_frame['leftHand'])} points, rightHand={len(structured_frame['rightHand'])} points")
            frames_structured.append(structured_frame)
        
        json_request = {
            "frames": frames_structured,
            "previous_word": request.previous_word or ""
        }
        
        # Call model service directly
        result, status_code = process_prediction_combine_api(
            loaded_models, device, json_request, 
            request.platform, request.language_code
        )
        
        # Process results
        if isinstance(result, dict) and "error" in result:
            logger.error(f"Prediction error: {result['error']}")
            raise HTTPException(
                status_code=int(status_code),
                detail=result["error"]
            )
        
        results = []
        for prediction in result:
            results.append({
                "sign": prediction.get("Class", "unknown"),
                "confidence": prediction.get("Confidence", 0.0)
            })
        
        return {
            "status": "success",
            "results": results,
            "platform": request.platform,
            "language_code": request.language_code,
            "mode": "standalone_rest"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@api_app.get("/")
async def home():
    """Welcome endpoint"""
    ascii_path = Path(__file__).parent.parent / "src" / "welcome_icon.txt"
    try:
        ascii_art = ascii_path.read_text(encoding="utf-8")
        return JSONResponse(
            content={
                "message": "Sign Language Recognition API",
                "version": "1.0.0",
                "endpoints": {
                    "health": "/health",
                    "recognize": "/v1/api/sign-language/recognize"
                }
            }
        )
    except:
        return JSONResponse(
            content={
                "message": "Sign Language Recognition API",
                "version": "1.0.0",
                "endpoints": {
                    "health": "/health",
                    "recognize": "/v1/api/sign-language/recognize"
                }
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api_app, host="0.0.0.0", port=8000)
