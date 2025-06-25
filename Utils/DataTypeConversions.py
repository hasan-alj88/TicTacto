import json

import numpy as np


def numpy2json(array: np.ndarray) -> str:
    """Convert numpy array to JSON string for database storage"""
    return json.dumps(array.tolist())

def json2numpy(json_str: str) -> np.ndarray:
    """Convert JSON string back to numpy array"""
    return np.array(json.loads(json_str))