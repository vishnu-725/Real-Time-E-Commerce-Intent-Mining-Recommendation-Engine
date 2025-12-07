

import joblib
import os
from typing import Any
from phase3.utils import ensure_dir, get_logger

logger = get_logger(__name__)

def save_joblib(obj: Any, path: str):
    ensure_dir(os.path.dirname(path))
    joblib.dump(obj, path)
    logger.info("Saved object to %s", path)

def load_joblib(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    return joblib.load(path)
