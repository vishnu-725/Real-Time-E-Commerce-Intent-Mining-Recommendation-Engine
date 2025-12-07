

from typing import Tuple, List, Dict, Optional
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix
from implicit.als import AlternatingLeastSquares
from implicit.nearest_neighbours import bm25_weight
import joblib
import os
from phase3.config import DB_URI, OUTPUT_DIR
from phase3.db import get_engine
from phase3.utils import get_logger, ensure_dir

logger = get_logger(__name__)

MODEL_DIR = os.path.join(OUTPUT_DIR, "als_model")
MODEL_META_FILE = os.path.join(MODEL_DIR, "metadata.joblib")

DEFAULT_PARAMS = {
    "factors": 64,
    "regularization": 0.01,
    "iterations": 20,
    "use_gpu": False,   # set to True if you have GPU + implicit compiled for CUDA
    "calculate_training_loss": True
}

def build_interaction_matrix(interactions: pd.DataFrame,
                             user_col: str = "user_id",
                             item_col: str = "product_id",
                             weight_map: Optional[Dict[str, float]] = None
                             ) -> Tuple[csr_matrix, Dict[str,int], Dict[int,str]]:
    """
    Build a sparse (items x users) CSR matrix required by implicit.
    implicit expects item-user matrix (not user-item).

    Returns:
        matrix (csr_matrix): shape (num_items, num_users)
        user2idx (dict): mapping user_id -> col index
        idx2item (dict): mapping row index -> item_id
    """
    if weight_map is None:
        weight_map = {"view": 1.0, "click": 0.5, "add_to_cart": 2.0, "purchase": 5.0}

    interactions = interactions.copy()
    interactions['weight'] = interactions['event_type'].map(weight_map).fillna(0.0)

    # map ids to ints
    users = interactions[user_col].astype(str).unique().tolist()
    items = interactions[item_col].astype(str).unique().tolist()
    user2idx = {u: i for i, u in enumerate(users)}
    item2idx = {p: i for i, p in enumerate(items)}
    idx2item = {i: p for p, i in item2idx.items()}

    rows = interactions[item_col].astype(str).map(item2idx).to_numpy()
    cols = interactions[user_col].astype(str).map(user2idx).to_numpy()
    data = interactions['weight'].astype(float).to_numpy()

    mat = coo_matrix((data, (rows, cols)), shape=(len(items), len(users)))
    mat = mat.tocsr()
    logger.info("Built item-user matrix with shape %s", mat.shape)
    return mat, user2idx, idx2item

def train_als(interactions: pd.DataFrame,
              params: Dict = None,
              reweight: bool = True) -> Tuple[AlternatingLeastSquares, Dict, Dict]:
    """
    Train ALS model and return model + maps.
    """
    ensure_dir(MODEL_DIR)
    if params is None:
        params = DEFAULT_PARAMS.copy()

    mat, user2idx, idx2item = build_interaction_matrix(interactions)
    # Optionally apply BM25 weighting (or TF-IDF)
    if reweight:
        mat = bm25_weight(mat, K1=100, B=0.8)

    model = AlternatingLeastSquares(factors=params['factors'],
                                    regularization=params['regularization'],
                                    iterations=params['iterations'],
                                    calculate_training_loss=params.get('calculate_training_loss', False))
    logger.info("Training ALS with params %s", params)
    model.fit(mat)
    logger.info("ALS training complete.")
    # save metadata
    meta = {"params": params, "user2idx": user2idx, "idx2item": idx2item}
    joblib.dump(meta, MODEL_META_FILE)
    # implicit model has .save() to persist model factors
    model.save(os.path.join(MODEL_DIR, "als_model.npz"))
    logger.info("Saved ALS model to %s", MODEL_DIR)
    return model, user2idx, idx2item

def load_als(model_dir: str = MODEL_DIR) -> Tuple[AlternatingLeastSquares, Dict, Dict]:
    """
    Load ALS model and metadata.
    """
    meta_file = os.path.join(model_dir, "metadata.joblib")
    model_file = os.path.join(model_dir, "als_model.npz")
    if not os.path.exists(meta_file) or not os.path.exists(model_file):
        raise FileNotFoundError("ALS model not found. Train model first.")
    meta = joblib.load(meta_file)
    model = AlternatingLeastSquares()
    model.load(model_file)
    return model, meta['user2idx'], meta['idx2item']

def recommend_user(model: AlternatingLeastSquares, user2idx: Dict, idx2item: Dict,
                   user_id: str, N: int = 10) -> List[str]:
    """
    Return top-N recommendations (product ids) for a user_id.
    If user_id not seen during training, returns empty list (caller should fallback to popularity).
    """
    user_id = str(user_id)
    if user_id not in user2idx:
        return []
    uidx = user2idx[user_id]
    # implicit expects user index in the user dimension; recommend takes user id as integer index
    recs = model.recommend(uidx, None, N=N)  # first arg is user index, second is user_items (sparse) optional
    # recs -> list of (item_idx, score)
    out = [idx2item[item_idx] for item_idx, score in recs]
    return out

# Example minimal runner
if __name__ == "__main__":
    import pandas as pd
    interactions = pd.read_csv(os.path.join(OUTPUT_DIR, "interactions.csv"))
    model, u2i, i2idx = train_als(interactions)
