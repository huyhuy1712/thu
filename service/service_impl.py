import grpc
from typing import List, Dict
import threading
from queue import Queue

from app.loader.models_loaders import initialize_all_models
from app.service.model_service import process_prediction_combine_api

from .. import sign_recognition_pb2 as pb2
from .. import sign_recognition_pb2_grpc as pb2_grpc


class ModelPool:
    """Pool of model instances for load balancing"""
    def __init__(self, num_instances):
        self.pool = Queue(maxsize=num_instances)
        print(f"Initializing {num_instances} model instances...")
        for i in range(num_instances):
            print(f"  Loading model instance {i+1}/{num_instances}...")
            models, device = initialize_all_models()
            self.pool.put((models, device))
        print(f"✅ {num_instances} model instances loaded successfully")
    
    def get_model(self):
        """Get a model instance from the pool (blocks if all busy)"""
        return self.pool.get()
    
    def return_model(self, models, device):
        """Return a model instance to the pool"""
        self.pool.put((models, device))


class SignRecognitionService(pb2_grpc.SignRecognitionServiceServicer):
    def __init__(self, num_model_instances):
        self.model_pool = ModelPool(num_instances=num_model_instances)

    def Recognize(self, request: pb2.RecognizeRequest, context: grpc.ServicerContext) -> pb2.RecognizeResponse:
        models, device = None, None
        try:
            # Get a model instance from the pool
            models, device = self.model_pool.get_model()
            
            frames: List[Dict] = []
            for f in request.frames:
                frame_dict = {
                    "midEyes": {"x": f.midEyes.x, "y": f.midEyes.y, "z": f.midEyes.z},
                    "leftHand": [{"x": lm.x, "y": lm.y, "z": lm.z} for lm in f.leftHand],
                    "rightHand": [{"x": lm.x, "y": lm.y, "z": lm.z} for lm in f.rightHand],
                    "lip": [{"x": lm.x, "y": lm.y, "z": lm.z} for lm in f.lip],
                }
                frames.append(frame_dict)

            jsonRequest = {
                "frames": frames,
                "previous_word": request.previous_word or "",
            }

            result, status_code = process_prediction_combine_api(
                models, device, jsonRequest, request.platform, request.language_code
            )

            if isinstance(result, dict) and "error" in result:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(result["error"])
                return pb2.RecognizeResponse(error=result["error"]) 

            response = pb2.RecognizeResponse(
                results=[pb2.Prediction(class_name=r["Class"], confidence=float(r["Confidence"])) for r in result]
            )
            return response

        except Exception as e:
            msg = f"[Recognize] Unexpected error: {str(e)}"
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(msg)
            return pb2.RecognizeResponse(error=msg)
        finally:
            # Always return the model to the pool
            if models is not None and device is not None:
                self.model_pool.return_model(models, device)
