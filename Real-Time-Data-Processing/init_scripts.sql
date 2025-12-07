-- docker/init_scripts.sql

-- Create raw events table if not exists
CREATE TABLE IF NOT EXISTS events (
    event_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    product_id BIGINT,
    timestamp TIMESTAMP NOT NULL
);

-- Create sessions table for sessionized data
CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR(255) PRIMARY KEY,
    user_id BIGINT NOT NULL,
    session_start TIMESTAMP NOT NULL,
    session_end TIMESTAMP NOT NULL,
    session_length_seconds INT NOT NULL,
    num_events INT NOT NULL,
    click_count INT DEFAULT 0,
    view_count INT DEFAULT 0,
    add_to_cart_count INT DEFAULT 0,
    purchase_count INT DEFAULT 0,
    unique_product_count INT DEFAULT 0,
    session_start_hour INT,
    session_start_dow INT
);

-- Optional: indexes to speed up queries
CREATE INDEX IF NOT EXISTS idx_events_user ON events(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
