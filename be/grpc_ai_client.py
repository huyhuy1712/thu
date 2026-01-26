import os
import grpc
from typing import List, Tuple

from api.grpc_generated import sign_recognition_pb2 as pb2
from api.grpc_generated import sign_recognition_pb2_grpc as pb2_grpc

AI_GRPC_HOST = os.getenv("AI_GRPC_HOST", "localhost")
AI_GRPC_PORT = os.getenv("AI_GRPC_PORT", "50051")
AI_GRPC_TARGET = f"{AI_GRPC_HOST}:{AI_GRPC_PORT}"

# Build gRPC frames from generic x/y/z arrays expected by RequestModel.
def _to_grpc_frames(frames: List[dict]):
    grpc_frames = []
    for f in frames:
        # Handle both dict and Pydantic model objects
        if hasattr(f, 'x'):  # Pydantic model
            xs = f.x
            ys = f.y
            zs = f.z
        else:  # dict
            xs = f.get("x", [])
            ys = f.get("y", [])
            zs = f.get("z", [])
        
        landmarks = []
        for x, y, z in zip(xs, ys, zs):
            landmarks.append(pb2.Landmark(x=float(x), y=float(y), z=float(z)))
        # Use first landmark as midEyes fallback to satisfy required field
        mid = landmarks[0] if landmarks else pb2.Landmark(x=0.0, y=0.0, z=0.0)
        grpc_frames.append(
            pb2.Frame(
                midEyes=mid,
                leftHand=landmarks,
                rightHand=[],
                lip=[],
            )
        )
    return grpc_frames


def recognize_sign_grpc(frames: List[dict], platform: str = "web", language_code: str = "au") -> Tuple[str, float, str, int]:
    """Call AI gRPC Recognize.
    Returns: (predicted_class, confidence, error, http_status)
    """
    try:
        grpc_frames = _to_grpc_frames(frames)
        req = pb2.RecognizeRequest(
            frames=grpc_frames,
            previous_word="",
            platform=platform,
            language_code=language_code,
        ) 
        with grpc.insecure_channel(AI_GRPC_TARGET) as channel:
            stub = pb2_grpc.SignRecognitionServiceStub(channel)
            res = stub.Recognize(req, timeout=10)
        if res.results:
            best = res.results[0]
            return best.class_name, best.confidence, "", 200
        return "", 0.0, res.error or "No result", 500
    except Exception as exc:  # broad to return error string to caller
        return "", 0.0, str(exc), 500


def health_check_grpc(timeout: int = 3) -> Tuple[bool, str]:
    """Check connectivity to AI gRPC service."""
    try:
        with grpc.insecure_channel(AI_GRPC_TARGET) as channel:
            grpc.channel_ready_future(channel).result(timeout=timeout)
        return True, "ok"
    except Exception as exc:
        return False, str(exc)
