import os
import pickle
import json
import numpy as np
from core.config import settings

model_store = {
    "user_embeddings": {},
    "item_embeddings": {},
    "content_embeddings": {},
    "user_history": {},
    "trending_scores": {}
}

def load_embeddings(path: str) -> dict:
    return np.load(path, allow_pickle=True).item()

def load_models():
    """
    Load all embeddings and metadata at API startup.
    """
    model_store["user_embeddings"] = load_embeddings(
        os.path.join(settings.MODEL_DIR, "user_embeddings.npy")
    )

    model_store["item_embeddings"] = load_embeddings(
        os.path.join(settings.MODEL_DIR, "item_embeddings.npy")
    )

    model_store["content_embeddings"] = load_embeddings(
        os.path.join(settings.MODEL_DIR, "content_embeddings.npy")
    )

    with open(os.path.join(settings.MODEL_DIR, "metadata.json")) as f:
        model_store["user_history"] = json.load(f)

    with open(os.path.join(settings.MODEL_DIR, "trending.json")) as f:
        model_store["trending_scores"] = json.load(f)

# Load models at startup
load_models()
