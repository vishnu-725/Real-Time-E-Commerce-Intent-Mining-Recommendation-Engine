from fastapi import APIRouter, HTTPException
from services.content_based import get_similar_items

router = APIRouter(prefix="/similar", tags=["similar"])


@router.get("/{item_id}")
def similar_items(item_id: int, top_k: int = 10):
    try:
        items = get_similar_items(item_id, top_k)
        return {"item_id": item_id, "similar_items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
