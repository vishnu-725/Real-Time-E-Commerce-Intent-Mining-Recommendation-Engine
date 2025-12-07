

from typing import List, Dict, Tuple
import math
from collections import defaultdict
from phase3.utils import get_logger

logger = get_logger(__name__)

def normalize_scores(score_map: Dict[str, float]) -> Dict[str, float]:
    """
    Min-max normalize the scores to [0,1]
    """
    if not score_map:
        return {}
    vals = list(score_map.values())
    mn = min(vals); mx = max(vals)
    denom = mx - mn if mx != mn else 1.0
    return {k: (v - mn) / denom for k, v in score_map.items()}

def blend_scores(cf_scores: Dict[str, float],
                 content_scores: Dict[str, float],
                 popularity_scores: Dict[str, float],
                 weights: Tuple[float,float,float] = (0.6, 0.3, 0.1),
                 top_k: int = 10) -> List[Tuple[str,float]]:
    """
    cf_scores/content_scores/popularity_scores: dict product_id -> score
    weights: (alpha, beta, gamma)
    Return top_k list of (product_id, score) sorted desc
    """
    alpha, beta, gamma = weights
    cf_n = normalize_scores(cf_scores)
    cont_n = normalize_scores(content_scores)
    pop_n = normalize_scores(popularity_scores)
    merged = defaultdict(float)
    for pid, s in cf_n.items():
        merged[pid] += alpha * s
    for pid, s in cont_n.items():
        merged[pid] += beta * s
    for pid, s in pop_n.items():
        merged[pid] += gamma * s
    # sort and return top_k
    out = sorted(merged.items(), key=lambda x: x[1], reverse=True)[:top_k]
    logger.debug("Hybrid blend top_k: %s", out)
    return out
