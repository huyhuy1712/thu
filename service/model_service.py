from app.service.json_compare_service import rearrange_landmark_data_concatenated_padded
from app.loader.models_loaders import get_model
from app.api.models import RequestModel
from torch.nn import functional as F
from app.util.util import convert_none_to_nan
from app.util.util_v3 import process_data
import torch
from http import HTTPStatus
import numpy as np

def process_prediction_combine_api(models, device, jsonRequest, platform, language_code):
    try:
        # Check if we need to process frames
        if "frames" in jsonRequest:
            frames = jsonRequest.get("frames", [])
            
            # Check first frame's data completeness
            if len(frames) > 0:
                first_frame = frames[0]
                left_hand_count = len(first_frame.get("leftHand", []))
                right_hand_count = len(first_frame.get("rightHand", []))
                lip_count = len(first_frame.get("lip", []))
                mid_eyes_count = len(first_frame.get("midEyes", []))
                total_landmarks = left_hand_count + right_hand_count + lip_count + mid_eyes_count
                
                # If incomplete (less than 83 points), pad all frames
                if total_landmarks < 83:
                    processed_frames = []
                    for frame in frames:
                        # Ensure each section has required count, pad with 0
                        mid_eyes = frame.get("midEyes", [])
                        if not isinstance(mid_eyes, list):
                            mid_eyes = [mid_eyes] if mid_eyes else [{"x": 0.0, "y": 0.0, "z": 0.0}]
                        if len(mid_eyes) == 0:
                            mid_eyes = [{"x": 0.0, "y": 0.0, "z": 0.0}]
                        
                        left_hand = list(frame.get("leftHand", []))
                        while len(left_hand) < 21:
                            left_hand.append({"x": 0.0, "y": 0.0, "z": 0.0})
                        
                        right_hand = list(frame.get("rightHand", []))
                        while len(right_hand) < 21:
                            right_hand.append({"x": 0.0, "y": 0.0, "z": 0.0})
                        
                        lip = list(frame.get("lip", []))
                        while len(lip) < 40:
                            lip.append({"x": 0.0, "y": 0.0, "z": 0.0})
                        
                        processed_frames.append({
                            "midEyes": mid_eyes[:1],
                            "leftHand": left_hand[:21],
                            "rightHand": right_hand[:21],
                            "lip": lip[:40]
                        })
                    
                    # Duplicate to 10 frames if needed
                    while len(processed_frames) < 10:
                        processed_frames.append(processed_frames[0])
                    
                    jsonRequest["frames"] = processed_frames
                
                # Also check total sequence length
                elif len(frames) < 10:
                    while len(jsonRequest["frames"]) < 10:
                        jsonRequest["frames"].append(jsonRequest["frames"][0])
        
        jsonData = rearrange_landmark_data_concatenated_padded(jsonRequest)
            
        jsonData["data"] = convert_none_to_nan(jsonData.get("data"))
        seriData = RequestModel(data=jsonData["data"])
        crawl_data = seriData.data
        result = process_prediction_v3(models, device, crawl_data, platform, language_code)

        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"[process_prediction] Error processing prediction: {str(e)}."}, HTTPStatus.INTERNAL_SERVER_ERROR
    

def process_prediction_v3(models, device, crawl_data, platform, language_code):
    try:       
        deviceTorch = torch.device(device)
        model, label_mapping, seqlength, model_path = get_model(models, platform=platform, language_code=language_code)  

        x = torch.tensor(crawl_data[0].x)
        y = torch.tensor(crawl_data[0].y)
        z = torch.tensor(crawl_data[0].z)
        input_data = torch.column_stack((x, y, z))
        
        input_data = input_data.view(-1, 83, 3)[:, 1:, :]
        
        input_data = input_data.view(-1, 82*3).unsqueeze(0)
        
        input_data = input_data.permute(0, 2, 1)
        
        # Set version to 2 for model using use_semi_isolated_norm
        input_data = torch.unsqueeze(process_data(input_data, 2), dim=0).to(deviceTorch)

        print('INPUT_DATA_SHAPE', input_data.shape)
        
        with torch.inference_mode():
            pred = model(input_data, training=False)

            # Model outputs shape [batch, num_classes]; apply softmax across class axis
            probabilities = F.softmax(pred, dim=-1)
            confidence, predicted_class = torch.max(probabilities, dim=-1)

            # Batch size is 1 during inference
            class_idx = predicted_class.squeeze(0).cpu().item()
            confidences = confidence.squeeze(0).cpu().item()

            predictions = label_mapping[class_idx]
            return [{"Class": predictions, "Confidence": confidences}], HTTPStatus.OK

    except Exception as e:
        return {
            "error": f"[process_prediction] Error processing prediction: {str(e)}."}, HTTPStatus.INTERNAL_SERVER_ERROR