from core.model_loader import model_store

def cf_score(user_id: int):
    user_emb = model_store["user_embeddings"].get(user_id)
    item_emb = model_store["item_embeddings"]

    if user_emb is None:
        return {}

    scores = {}
    for item_id, emb in item_emb.items():
        scores[item_id] = float(user_emb @ emb)

    return scores
