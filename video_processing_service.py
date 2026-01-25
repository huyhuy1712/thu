"""
Service để lấy video từ MinIO, extract frames, và gửi tới AI gRPC service.
"""
import cv2
import numpy as np
from io import BytesIO
from typing import List, Tuple
from api.services.minIo_service import MinIOService
from api.services.grpc_ai_client import recognize_sign_grpc


class VideoProcessingService:
    """Extract frames từ video và gửi tới AI service."""
    
    def __init__(self):
        self.minio_service = MinIOService()
    
    def extract_frames_from_minio(
        self, 
        minio_path: str, 
        sample_rate: int = 5,
        bucket_name: str = "teledeaf"
    ) -> List[np.ndarray]:
        """
        Lấy video từ MinIO, extract frames.
        
        Args:
            minio_path: path tới video file trong MinIO (ví dụ: "videos/my_sign.mp4")
            sample_rate: lấy 1 frame cứ mỗi N frame (default 5)
            bucket_name: tên bucket MinIO
        
        Returns:
            Danh sách frames (np.ndarray)
        """
        try:
            # Lấy video từ MinIO
            response = self.minio_service.client.get_object(bucket_name, minio_path)
            video_bytes = response.read()
            
            # Đọc video từ bytes
            video_buffer = BytesIO(video_bytes)
            video_array = np.frombuffer(video_bytes, dtype=np.uint8)
            
            # Lưu vào temp file để OpenCV đọc
            import tempfile
            import os
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
                tmp_file.write(video_bytes)
                tmp_path = tmp_file.name
            
            # Mở video
            cap = cv2.VideoCapture(tmp_path)
            frames = []
            frame_count = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Lấy 1 frame cứ mỗi sample_rate frame
                if frame_count % sample_rate == 0:
                    frames.append(frame)
                
                frame_count += 1
            
            cap.release()
            os.remove(tmp_path)
            
            return frames
        
        except Exception as e:
            raise Exception(f"Error extracting frames from MinIO: {str(e)}")
    
    def extract_landmarks_from_frames(
        self, 
        frames: List[np.ndarray],
        detector
    ) -> List[dict]:
        """
        Extract landmarks (x, y, z) từ frames dùng MediaPipe hoặc detector khác.
        
        Args:
            frames: danh sách frames (np.ndarray)
            detector: MediaPipe Holistic hoặc detector tương tự
        
        Returns:
            Danh sách frame data: [{"x": [...], "y": [...], "z": [...]}, ...]
        """
        frame_data_list = []
        
        for frame in frames:
            try:
                # Chạy detector
                result = detector.process(frame)
                
                # Extract landmarks từ face, hands, pose
                x_coords = []
                y_coords = []
                z_coords = []
                
                # Face landmarks
                if result.face_landmarks:
                    for landmark in result.face_landmarks.landmark:
                        x_coords.append(landmark.x)
                        y_coords.append(landmark.y)
                        z_coords.append(landmark.z)
                
                # Left hand
                if result.left_hand_landmarks:
                    for landmark in result.left_hand_landmarks.landmark:
                        x_coords.append(landmark.x)
                        y_coords.append(landmark.y)
                        z_coords.append(landmark.z)
                
                # Right hand
                if result.right_hand_landmarks:
                    for landmark in result.right_hand_landmarks.landmark:
                        x_coords.append(landmark.x)
                        y_coords.append(landmark.y)
                        z_coords.append(landmark.z)
                
                # Pose
                if result.pose_landmarks:
                    for landmark in result.pose_landmarks.landmark:
                        x_coords.append(landmark.x)
                        y_coords.append(landmark.y)
                        z_coords.append(landmark.z)
                
                frame_data_list.append({
                    "x": x_coords,
                    "y": y_coords,
                    "z": z_coords
                })
            
            except Exception as e:
                print(f"Error processing frame: {str(e)}")
                continue
        
        return frame_data_list
    
    def process_video_from_minio_and_recognize(
        self,
        minio_path: str,
        detector,
        platform: str = "web",
        language_code: str = "au",
        sample_rate: int = 5
    ) -> Tuple[str, float, str, int]:
        """
        Lấy video từ MinIO → extract frames → extract landmarks → gửi tới AI gRPC.
        
        Args:
            minio_path: path tới video trong MinIO
            detector: MediaPipe detector hoặc tương tự
            platform: "web" hoặc "mobile"
            language_code: "au" hoặc "vn"
            sample_rate: lấy 1 frame cứ mỗi N frame
        
        Returns:
            (predicted_class, confidence, error, http_status)
        """
        try:
            # Step 1: Extract frames từ MinIO
            frames = self.extract_frames_from_minio(
                minio_path=minio_path,
                sample_rate=sample_rate
            )
            
            if not frames:
                return "", 0.0, "No frames extracted from video", 400
            
            # Step 2: Extract landmarks từ frames
            frame_data = self.extract_landmarks_from_frames(frames, detector)
            
            if not frame_data:
                return "", 0.0, "No landmarks extracted from frames", 400
            
            # Step 3: Gửi tới AI gRPC service
            predicted_class, confidence, error, status_code = recognize_sign_grpc(
                frame_data,
                platform=platform,
                language_code=language_code
            )
            
            return predicted_class, confidence, error, status_code
        
        except Exception as e:
            return "", 0.0, str(e), 500
