import pytest
from services.content_based import get_similar_items, content_score
from core.model_loader import load_models

load_models()

def test_get_similar_items():
    item_id = 1
    result = get_similar_items(item_id, top_k=3)
    assert isinstance(result, list)
    assert all(isinstance(i, int) for i in result)
    assert item_id not in result  # should not include itself

def test_content_score_known_user():
    user_id = 1
    scores = content_score(user_id)
    assert isinstance(scores, dict)

def test_content_score_unknown_user():
    user_id = 9999
    scores = content_score(user_id)
    assert scores == {}
