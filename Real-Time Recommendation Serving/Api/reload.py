from fastapi import APIRouter
from core.model_loader import load_models

router = APIRouter(prefix="/reload-model", tags=["reload"])


@router.post("/")
def reload_model():
    load_models()
    return {"message": "Model reloaded successfully"}
