import numpy as np
import pickle
import json
import faiss
import os

MODEL_DIR = "models"

def load_user_embeddings():
    return np.load(os.path.join(MODEL_DIR, "user_embeddings.npy"), allow_pickle=True).item()

def load_item_embeddings():
    return np.load(os.path.join(MODEL_DIR, "item_embeddings.npy"), allow_pickle=True).item()

def load_content_embeddings():
    return np.load(os.path.join(MODEL_DIR, "content_embeddings.npy"), allow_pickle=True).item()

def load_tfidf_vectorizer():
    with open(os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"), "rb") as f:
        return pickle.load(f)

def load_metadata():
    with open(os.path.join(MODEL_DIR, "metadata.json")) as f:
        return json.load(f)

def load_faiss_index():
    return faiss.read_index(os.path.join(MODEL_DIR, "faiss.index"))

def load_version():
    with open(os.path.join(MODEL_DIR, "version.txt")) as f:
        return f.read().strip()


if __name__ == "__main__":
    print("User embeddings:", load_user_embeddings())
    print("Item embeddings:", load_item_embeddings())
    print("Content embeddings:", load_content_embeddings())
    print("TF-IDF:", load_tfidf_vectorizer())
    print("Metadata:", load_metadata())
    print("FAISS index loaded:", load_faiss_index())
    print("Model version:", load_version())
