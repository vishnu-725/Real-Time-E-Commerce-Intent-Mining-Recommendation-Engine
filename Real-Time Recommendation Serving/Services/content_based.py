from core.model_loader import model_store
from utils.scoring_utils import cosine_similarity

def get_similar_items(item_id: int, top_k: int = 10):
    target = model_store["content_embeddings"].get(item_id)
    items = model_store["content_embeddings"]

    if target is None:
        return []

    sims = {}
    for other, emb in items.items():
        sims[other] = cosine_similarity(target, emb)

    sorted_items = sorted(sims.items(), key=lambda x: x[1], reverse=True)
    sorted_items = [i for i, s in sorted_items if i != item_id]

    return sorted_items[:top_k]


def content_score(user_id: int):
    """
    Fallback using item's textual embedding similarity based on user's history.
    """
    user_history = model_store["user_history"].get(user_id, [])
    content_emb = model_store["content_embeddings"]

    if not user_history:
        return {}

    scores = {}
    avg_emb = sum([content_emb[i] for i in user_history]) / len(user_history)

    for item_id, emb in content_emb.items():
        scores[item_id] = cosine_similarity(avg_emb, emb)

    return scores
