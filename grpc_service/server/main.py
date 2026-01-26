import os
import grpc
from concurrent import futures

from .. import sign_recognition_pb2_grpc as pb2_grpc
from .service_impl import SignRecognitionService

PORT = os.environ.get("GRPC_PORT", "50051")
NUM_MODEL_INSTANCES = int(os.environ.get("NUM_MODEL_INSTANCES", "2"))


def serve():
    # Use max_workers >= num_model_instances to allow concurrent requests
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max(4, NUM_MODEL_INSTANCES * 2)))
    
    # Create service with multiple model instances
    print(f"Starting gRPC server with {NUM_MODEL_INSTANCES} model instances...")
    service = SignRecognitionService(num_model_instances=NUM_MODEL_INSTANCES) 
    
    pb2_grpc.add_SignRecognitionServiceServicer_to_server(service, server) # Register service implementation
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    print(f"✅ gRPC SignRecognitionService listening on port {PORT}")
    print(f"   Worker threads: {max(4, NUM_MODEL_INSTANCES * 2)}")
    print(f"   Model instances: {NUM_MODEL_INSTANCES}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
