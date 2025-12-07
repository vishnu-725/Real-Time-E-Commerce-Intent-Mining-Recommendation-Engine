"""
train_dataset.py

Script to create an ML-ready training dataset from event data.
"""
import pandas as pd
import argparse
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from config import DB_URI, EVENTS_TABLE  # expected to be defined in config.py
from sessionize import sessionize_events
from features import compute_session_features
from utils import get_logger, parse_timestamp

def main(args):
    logger = get_logger(__name__)
    
    try:
        # Create database connection
        engine = create_engine(DB_URI)
        logger.info("Connecting to database.")
        
        # Read raw events from database table
        query = f"SELECT * FROM {EVENTS_TABLE}"
        events_df = pd.read_sql(query, engine)
        logger.info(f"Loaded {len(events_df)} events from '{EVENTS_TABLE}' table.")
        
        # Ensure timestamp column is datetime
        if 'timestamp' in events_df.columns:
            try:
                events_df['timestamp'] = pd.to_datetime(events_df['timestamp'])
            except Exception as e:
                # Fallback to safe parsing if needed
                events_df['timestamp'] = events_df['timestamp'].apply(parse_timestamp)
        else:
            logger.error("Timestamp column not found in events data.")
            sys.exit(1)
        
        # Sessionize events (30-minute inactivity threshold)
        sess_df = sessionize_events(events_df, user_col='user_id', time_col='timestamp', session_gap_min=30)
        logger.info(f"Sessionized events into {sess_df['session_id'].nunique()} sessions.")
        
        # Compute session-level features
        features_df = compute_session_features(sess_df, session_id_col='session_id', event_col='event_type', product_col='product_id')
        logger.info(f"Computed features for {len(features_df)} sessions.")
        
        # Write out to CSV
        output_file = args.output or "training_dataset.csv"
        features_df.to_csv(output_file, index=False)
        logger.info(f"Training dataset written to {output_file}")
    
    except SQLAlchemyError as db_err:
        logger.error(f"Database error: {db_err}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during dataset creation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create ML training dataset from events.")
    parser.add_argument("--output", type=str, help="Output CSV file path")
    args = parser.parse_args()
    main(args)
