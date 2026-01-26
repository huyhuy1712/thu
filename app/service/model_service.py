from app.service.json_compare_service import rearrange_landmark_data_concatenated_padded
from app.loader.models_loaders import get_model
from app.api.models import RequestModel
from torch.nn import functional as F
from app.util.util import convert_none_to_nan
from app.util.util_v3 import process_data
import torch
from http import HTTPStatus

def process_prediction_combine_api(models, device, jsonRequest, platform, language_code):
    try:
        # similarResult, jsonData = test_manual_file_similarity(json_data=jsonRequest, language_code=language_code)
        
        # if similarResult:
        #     first_item = similarResult[0]
        #     similarLabel = first_item.get("Class")
        #     similarConfidence = first_item.get("Confidence")

        #     if (similarConfidence >= 500):
        #         return [{"Class": similarLabel, "Confidence": 1}], status.HTTP_200_OK
        jsonData = rearrange_landmark_data_concatenated_padded(jsonRequest)
            
        jsonData["data"] = convert_none_to_nan(jsonData.get("data"))
        seriData = RequestModel(data=jsonData["data"])
        crawl_data = seriData.data
        result = process_prediction_v3(models, device, crawl_data, platform, language_code)

        return result

    except Exception as e:
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
            probabilities = F.softmax(pred, dim=0)
            confidence, predicted_class = torch.max(probabilities, dim=0)
            confidences = confidence.cpu().item()
            predictions = label_mapping[predicted_class.cpu().item()]
            return [{"Class": predictions, "Confidence": confidences}], HTTPStatus.OK

    except Exception as e:
        return {
            "error": f"[process_prediction] Error processing prediction: {str(e)}."}, HTTPStatus.INTERNAL_SERVER_ERROR