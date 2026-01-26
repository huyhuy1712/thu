import numpy as np

def convert_none_to_nan(obj):
    if obj is None:
        return np.nan
    elif isinstance(obj, dict):
        return {k: convert_none_to_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_none_to_nan(i) for i in obj]
    return obj