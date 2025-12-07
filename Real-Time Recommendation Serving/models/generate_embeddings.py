import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import faiss
import json

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Example item data
items = [
    {"item_id": 1, "title": "Red Shoes", "description": "Comfortable running shoes"},
    {"item_id": 2, "title": "Blue Jeans", "description": "Slim fit denim jeans"},
    {"item_id": 3, "title": "Smart Watch", "description": "Fitness tracking smartwatch"},
]

item_ids = [i["item_id"] for i in items]
descriptions = [i["description"] for i in items]

# -------------------
# TF-IDF Vectorizer
# -------------------
tfidf = TfidfVectorizer(max_features=50)
tfidf_embeddings = tfidf.fit_transform(descriptions).toarray()

with open(os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"), "wb") as f:
    pickle.dump(tfidf, f)

# -------------------
# Save content embeddings
# -------------------
content_embeddings = {item_id: emb for item_id, emb in zip(item_ids, tfidf_embeddings)}
np.save(os.path.join(MODEL_DIR, "content_embeddings.npy"), content_embeddings)

# -------------------
# User embeddings (dummy random)
# -------------------
user_embeddings = {uid: np.random.rand(50) for uid in range(1, 4)}
np.save(os.path.join(MODEL_DIR, "user_embeddings.npy"), user_embeddings)

# -------------------
# Item embeddings (dummy random)
# -------------------
item_embeddings = {item_id: np.random.rand(50) for item_id in item_ids}
np.save(os.path.join(MODEL_DIR, "item_embeddings.npy"), item_embeddings)

# -------------------
# Metadata
# -------------------
metadata = {item["item_id"]: {"title": item["title"], "description": item["description"]} for item in items}
with open(os.path.join(MODEL_DIR, "metadata.json"), "w") as f:
    json.dump(metadata, f, indent=2)

# -------------------
# Model version
# -------------------
with open(os.path.join(MODEL_DIR, "version.txt"), "w") as f:
    f.write("v1.0")

# -------------------
# Optional: FAISS index
# -------------------
dimension = tfidf_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(tfidf_embeddings.astype('float32'))
faiss.write_index(index, os.path.join(MODEL_DIR, "faiss.index"))

print("All model artifacts generated in 'models/' folder.")
