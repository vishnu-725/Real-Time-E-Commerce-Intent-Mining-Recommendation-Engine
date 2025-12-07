"""
features.py

Feature engineering functions for session data.
"""
import pandas as pd
from typing import Optional

def compute_session_features(df: pd.DataFrame,
                             session_id_col: str = 'session_id',
                             event_col: str = 'event_type',
                             product_col: Optional[str] = None) -> pd.DataFrame:
    """
    Compute session-level features from event data.
    Features include session length, event counts by type, unique product count,
    and time-based features (hour of day, day of week).
    
    Args:
        df (pd.DataFrame): Event-level DataFrame with at least session IDs and event types.
                           Must contain columns for session_id, event_type, and, if provided, product_col.
        session_id_col (str): Column name for session identifier.
        event_col (str): Column name for event type (e.g., 'click', 'view', etc.).
        product_col (str, optional): Column name for product identifier (for unique product count).
    
    Returns:
        pd.DataFrame: Session-level features with one row per session:
            - session_id
            - num_events: total number of events in session
            - session_length_seconds: duration of session in seconds
            - <event_type>_count: count of each event type (e.g., click_count, view_count)
            - unique_product_count (if product_col given)
            - session_start_hour: hour of day session started
            - session_start_dow: day of week (0=Monday) session started
    """
    # Ensure session_id exists
    if session_id_col not in df.columns:
        raise ValueError(f"'{session_id_col}' not found in dataframe")
    # Ensure event_col exists
    if event_col not in df.columns:
        raise ValueError(f"'{event_col}' not found in dataframe")
    
    # Aggregate basic metrics
    group = df.groupby(session_id_col)
    features = pd.DataFrame({
        'num_events': group.size()
    })
    # Determine session start and end
    if 'session_start' in df.columns and 'session_end' in df.columns:
        # Use existing session start and end
        session_bounds = group[['session_start', 'session_end']].first()
    else:
        # Compute from event timestamps (assumes a 'timestamp' column exists)
        if 'timestamp' in df.columns:
            session_bounds = group['timestamp'].agg(['min', 'max']).rename(columns={'min':'session_start', 'max':'session_end'})
        else:
            raise ValueError("Timestamp column not found for computing session start/end")
    # Merge session bounds
    features = features.join(session_bounds)
    # Compute session length
    features['session_length_seconds'] = (features['session_end'] - features['session_start']).dt.total_seconds().astype(int)
    
    # Count event types
    type_counts = df.pivot_table(index=session_id_col,
                                 columns=event_col,
                                 aggfunc='size',
                                 fill_value=0)
    # Rename count columns (e.g., 'click' -> 'click_count')
    if type_counts.columns.size > 0:
        type_counts.columns = [f"{col}_count" for col in type_counts.columns]
        features = features.join(type_counts)
    
    # Unique product count
    if product_col and product_col in df.columns:
        unique_counts = df.groupby(session_id_col)[product_col].nunique().rename('unique_product_count')
        features = features.join(unique_counts)
    
    # Time-based features from session_start
    features['session_start_hour'] = features['session_start'].dt.hour
    features['session_start_dow'] = features['session_start'].dt.dayofweek  # 0 = Monday
    
    # Reset index to include session_id as column
    features = features.reset_index()
    
    return features
