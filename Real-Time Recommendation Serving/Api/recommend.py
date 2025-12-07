from fastapi import APIRouter, HTTPException
from services.recommender_service import get_recommendations

router = APIRouter(prefix="/recommend", tags=["recommend"])


@router.get("/{user_id}")
def recommend_items(user_id: int, top_k: int = 10):
    try:
        recs = get_recommendations(user_id, top_k)
        return {"user_id": user_id, "recommendations": recs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
