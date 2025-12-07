const { Client } = require('pg');
const config = require('../config');

const client = new Client(config.db);

/**
 * Initializes the PostgreSQL database connection and table.
 */
async function initDb() {
  await client.connect();
  // Create events table if not exists
  await client.query(`
    CREATE TABLE IF NOT EXISTS events (
      event_id VARCHAR(255) PRIMARY KEY,
      event_type VARCHAR(255),
      timestamp TIMESTAMP,
      session_id VARCHAR(255),
      user_id VARCHAR(255),
      device JSONB,
      context JSONB,
      payload JSONB
    );
  `);
}

/**
 * Saves an event object into the database.
 * @param {Object} event - The event data to save.
 */
async function saveEvent(event) {
  const query = `
    INSERT INTO events(event_id, event_type, timestamp, session_id, user_id, device, context, payload)
    VALUES($1, $2, $3, $4, $5, $6, $7, $8)
    ON CONFLICT (event_id) DO NOTHING;
  `;
  const values = [
    event.event_id,
    event.event_type,
    event.timestamp,
    event.session_id,
    event.user_id,
    JSON.stringify(event.device),
    JSON.stringify(event.context),
    JSON.stringify(event.payload)
  ];
  await client.query(query, values);
}

module.exports = {
  initDb,
  saveEvent
};
