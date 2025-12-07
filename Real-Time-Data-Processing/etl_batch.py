import os
import json
from datetime import datetime
import pandas as pd
from sqlalchemy import text
from db import read_sql, engine
from config import Config
from sessionize import sessionize_events

def safe_metadata(x):
    """
    Convert metadata to a Python dict if it's a JSON string, else return empty dict or original.
    """
    if pd.isna(x) or x is None:
        return {}
    if isinstance(x, str):
        try:
            return json.loads(x)
        except json.JSONDecodeError:
            return {}
    if isinstance(x, dict):
        return x
    return {}

def run_etl():
    # 1. Extract: read all cleaned events
    query = "SELECT * FROM events_clean"
    df = read_sql(query)

    # 2. Transform:
    if df.empty:
        print("No events to process.")
        return

    # Drop duplicates based on key fields
    df = df.drop_duplicates(subset=['user_id', 'event_type', 'event_timestamp', 'metadata'])
    # Lowercase event_type
    df['event_type'] = df['event_type'].str.lower()
    # Convert event_timestamp to UTC datetime
    df['event_timestamp'] = pd.to_datetime(df['event_timestamp'], utc=True)
    # Safely convert metadata to dict
    df['metadata'] = df['metadata'].apply(safe_metadata)
    # Sort by user and timestamp
    df = df.sort_values(['user_id', 'event_timestamp']).reset_index(drop=True)

    # 3. Sessionize
    session_df = sessionize_events(df)

    # 4. Load: UPSERT sessions into user_sessions
    with engine.begin() as conn:
        for _, row in session_df.iterrows():
            event_list = row['events']
            # Convert events list of dicts to JSON string for insertion
            events_json = json.dumps(event_list) if event_list else json.dumps([])
            insert_query = text("""
                INSERT INTO user_sessions (
                    session_id, user_id, session_start, session_end,
                    viewed_products, added_to_cart, purchased, session_length_seconds, events
                ) VALUES (
                    :session_id, :user_id, :session_start, :session_end,
                    :viewed, :cart, :purchased, :length, :events
                )
                ON CONFLICT (session_id) DO UPDATE
                SET user_id = EXCLUDED.user_id,
                    session_start = EXCLUDED.session_start,
                    session_end = EXCLUDED.session_end,
                    viewed_products = EXCLUDED.viewed_products,
                    added_to_cart = EXCLUDED.added_to_cart,
                    purchased = EXCLUDED.purchased,
                    session_length_seconds = EXCLUDED.session_length_seconds,
                    events = EXCLUDED.events;
            """)
            conn.execute(
                insert_query,
                {
                    "session_id": row['session_id'],
                    "user_id": row['user_id'],
                    "session_start": row['session_start'],
                    "session_end": row['session_end'],
                    "viewed": row['viewed_products'],
                    "cart": row['added_to_cart'],
                    "purchased": row['purchased'],
                    "length": int(row['session_length_seconds']),
                    "events": events_json
                }
            )

    # Save snapshot CSV of sessions
    os.makedirs(Config.BATCH_OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    output_path = os.path.join(Config.BATCH_OUTPUT_DIR, f"sessions_{timestamp}.csv")
    session_df.to_csv(output_path, index=False)
    print(f"Saved session snapshot to {output_path}")

if __name__ == "__main__":
    run_etl()
