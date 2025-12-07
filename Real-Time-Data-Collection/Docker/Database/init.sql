CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255),
    event_type VARCHAR(255),
    timestamp BIGINT,
    session_id VARCHAR(255),
    user_id VARCHAR(255),
    device JSONB,
    context JSONB,
    payload JSONB
);
