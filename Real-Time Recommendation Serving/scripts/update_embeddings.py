"""
Rebuild user/item/content embeddings after Phase-3 model retraining.
This script can be scheduled or triggered manually.
"""
import numpy as np
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from core.config import settings
import json

MODEL_DIR = settings.MODEL_DIR
os.makedirs(MODEL_DIR, exist_ok=True)

# Example: Rebuild content embeddings
def rebuild_content_embeddings(items: list):
    """
    items: list of dicts with keys ['item_id', 'title', 'description']
    """
    item_ids = [i["item_id"] for i in items]
    descriptions = [i["description"] for i in items]

    tfidf = TfidfVectorizer(max_features=50)
    tfidf_embeddings = tfidf.fit_transform(descriptions).toarray()

    # Save TF-IDF
    with open(os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"), "wb") as f:
        pickle.dump(tfidf, f)

    content_embeddings = {item_id: emb for item_id, emb in zip(item_ids, tfidf_embeddings)}
    np.save(os.path.join(MODEL_DIR, "content_embeddings.npy"), content_embeddings)

    metadata = {item["item_id"]: {"title": item["title"], "description": item["description"]} for item in items}
    with open(os.path.join(MODEL_DIR, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    print("Rebuilt content embeddings and metadata")

if __name__ == "__main__":
    # Example usage
    items = [
        {"item_id": 1, "title": "Red Shoes", "description": "Comfortable running shoes"},
        {"item_id": 2, "title": "Blue Jeans", "description": "Slim fit denim jeans"},
        {"item_id": 3, "title": "Smart Watch", "description": "Fitness tracking smartwatch"},
    ]
    rebuild_content_embeddings(items)
