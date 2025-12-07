
from typing import Tuple, List
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from db import read_sql
from utils import get_logger
from config import OUTPUT_DIR
import os
import pickle

logger = get_logger(__name__)

TFIDF_FILE = os.path.join(OUTPUT_DIR, "tfidf_vectorizer.pkl")
VECTORS_FILE = os.path.join(OUTPUT_DIR, "tfidf_vectors.npz")
NN_MODEL_FILE = os.path.join(OUTPUT_DIR, "nn_model.pkl")
PRODUCTS_DF_FILE = os.path.join(OUTPUT_DIR, "products_df.pkl")

def load_products_from_db() -> pd.DataFrame:
    """
    Load product features from DB.
    Expects table product_features with columns: product_id, title, description, category
    """
    q = "SELECT product_id, title, description, category FROM product_features"
    df = read_sql(q)
    logger.info("Loaded %d products for content-based index", len(df))
    return df

def build_index(products_df: pd.DataFrame = None,
                text_fields: List[str] = ("title", "description"),
                ngram_range=(1,2),
                max_features: int = 50_000) -> Tuple[TfidfVectorizer, any, NearestNeighbors, pd.DataFrame]:
    """
    Build TF-IDF vectorizer and nearest-neighbor model on product text.
    Returns: (vectorizer, vectors, nn_model, products_df)
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if products_df is None:
        products_df = load_products_from_db()
    # create corpus
    def join_text(r):
        parts = []
        for f in text_fields:
            v = r.get(f) if isinstance(r, dict) else r.get(f)
            if pd.isna(v) or v is None:
                continue
            parts.append(str(v))
        return " ".join(parts)
    products_df['corpus'] = products_df.apply(lambda r: " ".join([str(r.get(f) or "") for f in text_fields]), axis=1)
    corpus = products_df['corpus'].fillna("").tolist()
    # TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=ngram_range, max_features=max_features)
    vectors = vectorizer.fit_transform(corpus)
    # Nearest Neighbors (cosine)
    nn = NearestNeighbors(metric='cosine', algorithm='brute')
    nn.fit(vectors)
    # persist useful artifacts
    with open(TFIDF_FILE, "wb") as f:
        pickle.dump(vectorizer, f)
    with open(NN_MODEL_FILE, "wb") as f:
        pickle.dump(nn, f)
    products_df.to_pickle(PRODUCTS_DF_FILE)
    logger.info("Built TF-IDF index: %d products, vectors shape=%s", len(products_df), vectors.shape)
    return vectorizer, vectors, nn, products_df

def recommend_similar(product_id: str, top_k: int = 10,
                      vectorizer=None, nn_model=None, products_df: pd.DataFrame = None) -> List[str]:
    """
    Recommend top_k similar product_ids for a given product_id.
    If vectorizer/nn_model/products_df are None, attempts to load from disk.
    """
    # load artifacts if needed
    import pickle
    if products_df is None:
        products_df = pd.read_pickle(PRODUCTS_DF_FILE)
    if vectorizer is None:
        with open(TFIDF_FILE, "rb") as f:
            vectorizer = pickle.load(f)
    if nn_model is None:
        with open(NN_MODEL_FILE, "rb") as f:
            nn_model = pickle.load(f)
    # find product index
    products_df = products_df.reset_index(drop=True)
    idx_lookup = {str(pid): idx for idx, pid in enumerate(products_df['product_id'].astype(str).tolist())}
    if str(product_id) not in idx_lookup:
        logger.warning("Product id %s not found in products index", product_id)
        return []
    idx = idx_lookup[str(product_id)]
    # compute vector for product and query nearest neighbors
    corpus_text = products_df.loc[idx, 'corpus']
    vec = vectorizer.transform([corpus_text])
    dists, idxs = nn_model.kneighbors(vec, n_neighbors=top_k+1)  # +1 to skip itself
    out = []
    for i in idxs[0]:
        pid = str(products_df.loc[i, 'product_id'])
        if pid == str(product_id):
            continue
        out.append(pid)
        if len(out) >= top_k:
            break
    return out
