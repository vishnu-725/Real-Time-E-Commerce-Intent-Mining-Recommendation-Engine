import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_recommend_endpoint():
    user_id = 1
    response = client.get(f"/recommend/{user_id}?top_k=5")
    assert response.status_code == 200
    assert "recommendations" in response.json()
    assert len(response.json()["recommendations"]) <= 5

def test_similar_endpoint():
    item_id = 1
    response = client.get(f"/similar/{item_id}?top_k=3")
    assert response.status_code == 200
    assert "similar_items" in response.json()
    assert len(response.json()["similar_items"]) <= 3

def test_trending_endpoint():
    response = client.get("/trending/?top_k=5")
    assert response.status_code == 200
    assert "trending" in response.json()
    assert len(response.json()["trending"]) <= 5
