import pytest
from services.collaborative_filter import cf_score
from core.model_loader import load_models

load_models()

def test_cf_score_exists():
    user_id = 1
    scores = cf_score(user_id)
    assert isinstance(scores, dict)

def test_cf_score_empty_for_unknown_user():
    user_id = 9999
    scores = cf_score(user_id)
    assert scores == {}
