
import pandas as pd
from collections import defaultdict
from typing import List, Dict, Optional
from utils import get_logger, ensure_dir
from config import OUTPUT_DIR
import os

logger = get_logger(__name__)

# weights for event types (tweakable)
EVENT_WEIGHTS = {
    "view": 1.0,
    "click": 0.5,
    "add_to_cart": 2.0,
    "purchase": 5.0
}

def compute_popularity(interactions: pd.DataFrame, by: Optional[str] = None) -> pd.DataFrame:
    """
    Compute popularity scores.
    If `by` is None -> global (product_id)
    If `by` == 'category' -> requires interactions to have 'category' column
    Returns DataFrame with columns [group_key, product_id, score]
    """
    df = interactions.copy()
    # map weights
    df['weight'] = df['event_type'].map(EVENT_WEIGHTS).fillna(0.0)
    if by is None:
        scores = df.groupby('product_id')['weight'].sum().reset_index().rename(columns={'weight': 'score'})
        scores = scores.sort_values('score', ascending=False).reset_index(drop=True)
        return scores
    elif by == 'category':
        if 'category' not in df.columns:
            raise ValueError("Category column not present in interactions")
        scores = df.groupby(['category', 'product_id'])['weight'].sum().reset_index().rename(columns={'weight': 'score'})
        scores = scores.sort_values(['category', 'score'], ascending=[True, False])
        return scores
    else:
        raise ValueError("Unsupported grouping for popularity: %s" % by)

def top_k_global(popularity_df: pd.DataFrame, k: int = 10) -> List[str]:
    """
    Return top-k product_ids globally.
    """
    return popularity_df.head(k)['product_id'].astype(str).tolist()

def top_k_by_category(popularity_df: pd.DataFrame, category: str, k: int = 10) -> List[str]:
    """
    Return top-k in a given category (assumes popularity_df grouped by category).
    """
    df = popularity_df[popularity_df['category'] == category]
    return df.head(k)['product_id'].astype(str).tolist()

def save_popularity(pop_df: pd.DataFrame, fname: str = "popularity.csv"):
    ensure_dir(OUTPUT_DIR)
    out_path = os.path.join(OUTPUT_DIR, fname)
    pop_df.to_csv(out_path, index=False)
    logger.info("Saved popularity to %s", out_path)
