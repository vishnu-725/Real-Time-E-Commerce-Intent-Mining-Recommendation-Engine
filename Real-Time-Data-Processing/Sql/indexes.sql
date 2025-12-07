-- Index on user_id in events_clean for faster queries
CREATE INDEX IF NOT EXISTS idx_events_clean_user_id 
    ON events_clean (user_id);

-- Index on timestamp in events_clean for time-based queries
CREATE INDEX IF NOT EXISTS idx_events_clean_event_timestamp 
    ON events_clean (event_timestamp);

-- Index on user_id in user_sessions for lookup
CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id 
    ON user_sessions (user_id);
