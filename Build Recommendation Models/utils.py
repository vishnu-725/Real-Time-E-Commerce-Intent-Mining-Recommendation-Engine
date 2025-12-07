
import logging
import os
from typing import Iterable, List

def get_logger(name: str = __name__, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        ch = logging.StreamHandler()
        fmt = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        ch.setFormatter(logging.Formatter(fmt))
        logger.addHandler(ch)
    logger.setLevel(level)
    return logger

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def top_k_from_scores(scores: Iterable, candidate_ids: List, k: int):
    """
    Given scores aligned with candidate_ids (iterable), return top-k ids sorted by score desc.
    """
    paired = list(zip(candidate_ids, scores))
    paired.sort(key=lambda x: x[1], reverse=True)
    return [p[0] for p in paired[:k]]
