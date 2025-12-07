import os
import faiss
from core.config import settings

faiss_index = None

def load_faiss_index():
    global faiss_index
    index_path = os.path.join(settings.MODEL_DIR, "faiss.index")
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"FAISS index not found at {index_path}")
    faiss_index = faiss.read_index(index_path)
    return faiss_index

def search(query_vector, top_k=10):
    """
    Search FAISS index.
    query_vector: numpy array (1D)
    """
    global faiss_index
    if faiss_index is None:
        load_faiss_index()
    query_vector = query_vector.astype('float32').reshape(1, -1)
    distances, indices = faiss_index.search(query_vector, top_k)
    return indices.flatten().tolist(), distances.flatten().tolist()
