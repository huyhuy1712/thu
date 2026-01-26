import json
from app.const import SEQ_LEN_10
import torch

from app.model.model_v2 import SiFormerMobile

try:
    from transformers import pipeline
except Exception as e:
    pipeline = None
    print(f"Warning: Could not import transformers.pipeline: {e}")

MODEL_CONFIGS = {
    "web": {
        "vn": {
            "model_path": "app/src/export_model/best_web_model_checkpoint_on_20251105_103820.pth",
            "seqlength": SEQ_LEN_10,
            "label_path": "app/src/web_sign_vn.json"
        },
        "au": {
            "model_path": "app/src/export_model/best_web_model_checkpoint_on_20250924_090910.pth",
            "seqlength": SEQ_LEN_10,
            "label_path": "app/src/web_sign_au.json"
        }
    }
}


def initialize_all_models():
    """
    Initialize all models when the application starts
    """
    loaded_models = {}

    device = 'cuda' if torch.cuda.is_available() else 'cpu'  

    print("⚡ Initializing all models...")
    
    for platform, languages in MODEL_CONFIGS.items():
        print(f"Platform: {platform}")
        loaded_models[platform] = {}
        
        for language_code, config in languages.items():
            
            model_path = config["model_path"]
            seqlength = config["seqlength"]
            label_path = config["label_path"]

            print(f"--Language: {language_code}")
            print(f"--Model path: {config['model_path']}")
            print(f"--Sequence length: {config['seqlength']}")
            print(f"--Label path: {config['label_path']}")
            
            # Load label mapping
            label = json.load(open(label_path, "r", encoding="utf-8"))
            label_mapping = {i: k for i, k in enumerate(label.keys())}

            # Initialize model
            if platform == 'mobile':
                model = SiFormerMobile(num_classes=len(label),
                            num_enc_layers=4, num_dec_layers=3, device=device,
                            IA_encoder=True, IA_decoder=False, seq_len=seqlength,
                            patience=1, cross_attn=True)
            else:  # web
                model = SiFormerMobile(num_classes=len(label),
                            num_enc_layers=3, num_dec_layers=2, device=device,
                            IA_encoder=True, IA_decoder=False, seq_len=seqlength,
                            patience=1, cross_attn=True)
            
            model.load_state_dict(torch.load(model_path, map_location=torch.device(device), weights_only=False)['model_state_dict'])
            model.eval()
        
            # Save model and related information
            loaded_models[platform][language_code] = {
                'model': model,
                'label_mapping': label_mapping,
                'seqlength': seqlength,
                'model_path': model_path
            }
    
    total_models = sum(len(languages) for languages in loaded_models.values())
    print(f"✅ Initialized {total_models} models across {len(loaded_models)} platforms on device: {device}")

    return loaded_models, device


def get_model(loaded_models, platform = 'mobile', language_code = 'au'):
    """
    Get the pre-loaded model by platform and language code
    """    
    if platform not in loaded_models:
        raise ValueError(f"Platform {platform} not found in loaded models")
    
    if language_code not in loaded_models[platform]:
        raise ValueError(f"Language code {language_code} not found for platform {platform}")
        
    model_info = loaded_models[platform][language_code]
    return model_info['model'], model_info['label_mapping'], model_info['seqlength'], model_info['model_path']