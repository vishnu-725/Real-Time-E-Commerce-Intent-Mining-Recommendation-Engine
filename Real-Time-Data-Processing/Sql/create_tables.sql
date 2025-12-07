-- Create raw events table
CREATE TABLE IF NOT EXISTS events_raw (
    id SERIAL PRIMARY KEY,
    raw_event JSONB NOT NULL,
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create cleaned events table
CREATE TABLE IF NOT EXISTS events_clean (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMPTZ NOT NULL,
    metadata JSONB
);

-- Create user sessions table
CREATE TABLE IF NOT EXISTS user_sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    session_start TIMESTAMPTZ NOT NULL,
    session_end TIMESTAMPTZ NOT NULL,
    viewed_products TEXT[],
    added_to_cart TEXT[],
    purchased TEXT[],
    session_length_seconds INT,
    events JSONB
);
