import pytest
from core.model_loader import load_models, model_store

def test_load_models():
    load_models()
    assert "user_embeddings" in model_store
    assert isinstance(model_store["user_embeddings"], dict)
    assert "item_embeddings" in model_store
    assert isinstance(model_store["item_embeddings"], dict)
    assert "content_embeddings" in model_store
    assert isinstance(model_store["content_embeddings"], dict)
    assert "user_history" in model_store
    assert isinstance(model_store["user_history"], dict)
    assert "trending_scores" in model_store
