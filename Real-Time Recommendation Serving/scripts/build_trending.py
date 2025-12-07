
import pandas as pd
from sqlalchemy import create_engine
from core.config import settings
import json
import os

# Database connection
DATABASE_URL = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}"
)
engine = create_engine(DATABASE_URL)

def compute_trending(top_n: int = 100) -> dict:
    """
    Compute trending items based on recent events.
    Returns a dict: {item_id: trending_score}
    """
    query = """
        SELECT metadata->>'item_id' AS item_id, COUNT(*) AS views
        FROM events_clean
        WHERE event_type='view'
        GROUP BY item_id
        ORDER BY views DESC
        LIMIT :top_n
    """
    df = pd.read_sql(query, engine, params={"top_n": top_n})
    trending_scores = {int(row["item_id"]): int(row["views"]) for _, row in df.iterrows()}
    return trending_scores

def save_trending(trending_scores: dict):
    path = os.path.join(settings.MODEL_DIR, "trending.json")
    with open(path, "w") as f:
        json.dump(trending_scores, f, indent=2)
    print(f"Saved trending scores to {path}")

if __name__ == "__main__":
    trending_scores = compute_trending()
    save_trending(trending_scores)
