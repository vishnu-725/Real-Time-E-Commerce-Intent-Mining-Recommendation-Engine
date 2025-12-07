import uuid
import pandas as pd
from config import Config

def sessionize_events(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert sorted events DataFrame into user sessions based on a timeout.
    Output columns: session_id, user_id, session_start, session_end,
                    viewed_products, added_to_cart, purchased,
                    session_length_seconds, events.
    """
    timeout = Config.SESSION_TIMEOUT_SECONDS
    sessions = []

    # Ensure events are sorted by user and timestamp
    if not df.empty:
        df = df.sort_values(['user_id', 'event_timestamp'])

    # Group events by user_id
    for user, group in df.groupby('user_id'):
        group = group.sort_values('event_timestamp')
        session_start = None
        session_id = None
        viewed = []
        added_to_cart = []
        purchased = []
        current_events = []
        last_ts = None

        for _, row in group.iterrows():
            ts = row['event_timestamp']
            event_type = row['event_type']
            metadata = row.get('metadata') or {}
            # Extract product_id from metadata if present
            product_id = None
            if isinstance(metadata, dict):
                product_id = metadata.get('product_id')

            # Determine if a new session should start
            if last_ts is None or (ts - last_ts).total_seconds() > timeout:
                # If there is an ongoing session, finalize it
                if last_ts is not None:
                    session_end = last_ts
                    session_length = int((session_end - session_start).total_seconds())
                    sessions.append({
                        'session_id': session_id,
                        'user_id': user,
                        'session_start': session_start,
                        'session_end': session_end,
                        'viewed_products': viewed,
                        'added_to_cart': added_to_cart,
                        'purchased': purchased,
                        'session_length_seconds': session_length,
                        'events': current_events
                    })
                # Start a new session
                session_id = str(uuid.uuid4())
                session_start = ts
                viewed = []
                added_to_cart = []
                purchased = []
                current_events = []

            # Record the event in the current session
            event_record = {
                'event_type': event_type,
                'event_timestamp': ts.isoformat(),
                'metadata': metadata
            }
            current_events.append(event_record)

            # Append product to appropriate list
            if event_type == 'view' and product_id:
                viewed.append(product_id)
            elif event_type in ['add_to_cart', 'cart'] and product_id:
                added_to_cart.append(product_id)
            elif event_type == 'purchase' and product_id:
                purchased.append(product_id)

            last_ts = ts

        # Finalize the last session for this user
        if session_id is not None:
            session_end = last_ts
            session_length = int((session_end - session_start).total_seconds())
            sessions.append({
                'session_id': session_id,
                'user_id': user,
                'session_start': session_start,
                'session_end': session_end,
                'viewed_products': viewed,
                'added_to_cart': added_to_cart,
                'purchased': purchased,
                'session_length_seconds': session_length,
                'events': current_events
            })

    # Create DataFrame of sessions
    if sessions:
        return pd.DataFrame(sessions)
    else:
        # Return empty DataFrame with expected columns if no sessions
        columns = ['session_id', 'user_id', 'session_start', 'session_end',
                   'viewed_products', 'added_to_cart', 'purchased',
                   'session_length_seconds', 'events']
        return pd.DataFrame(columns=columns)
