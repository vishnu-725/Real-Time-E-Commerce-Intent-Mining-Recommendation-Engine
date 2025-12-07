

from typing import List, Callable, Dict
import pandas as pd
from utils import get_logger
from collections import defaultdict

logger = get_logger(__name__)

def precision_at_k(pred: List[str], truth: List[str], k: int) -> float:
    if k <= 0:
        return 0.0
    pred_k = pred[:k]
    if not pred_k:
        return 0.0
    return len(set(pred_k).intersection(set(truth))) / float(k)

def recall_at_k(pred: List[str], truth: List[str], k: int) -> float:
    if not truth:
        return 0.0
    pred_k = pred[:k]
    return len(set(pred_k).intersection(set(truth))) / float(len(set(truth)))

def evaluate_sessions(interactions_df: pd.DataFrame,
                      recommender_fn: Callable[[str, str, int], List[str]],
                      k: int = 10,
                      sample_sessions: int = None) -> Dict[str, float]:
    """
    Evaluate a recommender over sessions.

    interactions_df expected columns:
        user_id, session_id, product_id, event_type, is_positive

    recommender_fn(user_id, session_id, k) -> list of product_id strings

    Returns aggregate metrics: precision@k, recall@k
    """
    # build ground truth per session: purchased products
    grouped = interactions_df.groupby('session_id')
    sessions = list(grouped.groups.keys())
    if sample_sessions:
        sessions = sessions[:sample_sessions]

    precs = []
    recs = []
    for sess in sessions:
        sess_df = grouped.get_group(sess)
        user = sess_df['user_id'].iloc[0]
        truth = sess_df[sess_df['is_positive'] == 1]['product_id'].astype(str).tolist()
        if len(truth) == 0:
            # skip sessions with no positive labels for evaluation
            continue
        # call recommender
        preds = recommender_fn(user, sess, k)
        p = precision_at_k(preds, truth, k)
        r = recall_at_k(preds, truth, k)
        precs.append(p)
        recs.append(r)
    # aggregate
    results = {
        "precision_at_%d" % k: float(sum(precs) / len(precs)) if precs else 0.0,
        "recall_at_%d" % k: float(sum(recs) / len(recs)) if recs else 0.0,
        "evaluated_sessions": len(precs)
    }
    logger.info("Evaluated %d sessions: P@%d=%.4f R@%d=%.4f", results["evaluated_sessions"], k, results["precision_at_%d" % k], k, results["recall_at_%d" % k])
    return results

# Example wrappers to use with evaluate_sessions:

def popularity_recommender_factory(popularity_df):
    """
    Returns a recommender function (user_id, session_id, k) -> top-k product ids
    popularity_df: DataFrame with product_id ordered by popularity
    """
    top_list = popularity_df['product_id'].astype(str).tolist()
    def recommend(user_id, session_id, k):
        return top_list[:k]
    return recommend

def content_recommender_factory():
    """
    Returns a recommender function calling content_based.recommend_similar
    as a fallback: here we use the last viewed product in session as query (simple heuristic).
    """
    from content_based import recommend_similar
    def recommend(user_id, session_id, k):
        # to be provided with context of interactions DataFrame externally
        # In practice, we will capture last viewed product for the session
        # For demonstration, this wrapper should be closure-captured in runner
        return []
    return recommend
