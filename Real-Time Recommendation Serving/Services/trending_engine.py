from core.model_loader import model_store

def get_trending_items(top_k=10):
    trending = model_store["trending_scores"]
    ranked = sorted(trending.items(), key=lambda x: x[1], reverse=True)
    return [i for i, s in ranked[:top_k]]


def trending_boost():
    return model_store["trending_scores"]
