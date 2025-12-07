

import json
from typing import List, Dict
import pandas as pd
from db import read_sql
from utils import get_logger, ensure_dir
from config import OUTPUT_DIR
import os

logger = get_logger(__name__)

def extract_sessions_from_db(limit: int = None) -> pd.DataFrame:
    """
    Read user_sessions table from DB and return DataFrame.
    Use `limit` to fetch smaller dataset for dev.
    """
    q = "SELECT session_id, user_id, session_start, session_end, events, viewed_products, purchased FROM user_sessions"
    if limit:
        q += f" LIMIT {limit}"
    df = read_sql(q)
    logger.info("Loaded %d sessions from DB", len(df))
    return df

def flatten_sessions(df_sessions: pd.DataFrame) -> pd.DataFrame:
    """
    Convert sessions DataFrame into flattened interactions DataFrame.
    """
    records = []
    for _, row in df_sessions.iterrows():
        session_id = row['session_id']
        user_id = str(row['user_id'])
        # events may be stored as JSON string or Python list
        events = row.get('events') or []
        if isinstance(events, str):
            try:
                events = json.loads(events)
            except Exception:
                events = []
        # Build set of purchased product ids in this session for labeling
        purchased = row.get('purchased') or []
        if isinstance(purchased, str):
            try:
                purchased = json.loads(purchased)
            except Exception:
                purchased = []
        purchased_set = set([str(p) for p in purchased if p is not None])
        for ev in events:
            # event dict expected to have 'event_type' and 'metadata' possibly containing product_id
            ev_type = ev.get('event_type') if isinstance(ev, dict) else None
            ev_ts = ev.get('event_timestamp') if isinstance(ev, dict) else None
            metadata = ev.get('metadata') if isinstance(ev, dict) else {}
            product_id = None
            # try common places for product_id
            if isinstance(metadata, dict):
                product_id = metadata.get('product_id') or metadata.get('id') or metadata.get('productId')
            else:
                # if metadata is string, try to parse
                try:
                    m = json.loads(metadata)
                    product_id = m.get('product_id')
                except Exception:
                    product_id = None
            if product_id is None:
                # skip events without product context
                continue
            product_id = str(product_id)
            is_positive = 1 if product_id in purchased_set else 0
            records.append({
                "user_id": user_id,
                "session_id": session_id,
                "product_id": product_id,
                "event_type": ev_type.lower() if isinstance(ev_type, str) else ev_type,
                "event_ts": pd.to_datetime(ev_ts, utc=True) if ev_ts else None,
                "is_positive": is_positive
            })
    interactions = pd.DataFrame(records)
    logger.info("Flattened to %d interaction rows", len(interactions))
    return interactions

def build_interaction_dataset(limit_sessions: int = None) -> pd.DataFrame:
    ensure_dir(OUTPUT_DIR)
    sessions = extract_sessions_from_db(limit=limit_sessions)
    interactions = flatten_sessions(sessions)
    out_path = os.path.join(OUTPUT_DIR, "interactions.csv")
    interactions.to_csv(out_path, index=False)
    logger.info("Saved interactions CSV to %s", out_path)
    return interactions

if __name__ == "__main__":
    # quick run for dev
    build_interaction_dataset(limit_sessions=5000)
