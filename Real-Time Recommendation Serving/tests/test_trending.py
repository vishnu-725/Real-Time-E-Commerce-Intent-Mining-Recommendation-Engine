import pytest
from services.trending_engine import get_trending_items, trending_boost
from core.model_loader import load_models

load_models()

def test_get_trending_items():
    top_k = 3
    trending = get_trending_items(top_k)
    assert isinstance(trending, list)
    assert len(trending) <= top_k
    assert all(isinstance(i, int) for i in trending)

def test_trending_boost_returns_dict():
    scores = trending_boost()
    assert isinstance(scores, dict)
