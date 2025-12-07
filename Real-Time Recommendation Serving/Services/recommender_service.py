from services.collaborative_filter import cf_score
from services.content_based import content_score
from services.hybrid_ranker import rank_scores
from services.trending_engine import trending_boost

def get_recommendations(user_id: int, top_k: int = 10):
    cf = cf_score(user_id)
    cb = content_score(user_id)
    tr = trending_boost()

    final_scores = rank_scores(cf, cb, tr)
    ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

    return [item_id for item_id, score in ranked[:top_k]]
