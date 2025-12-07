require('dotenv').config();

module.exports = {
  server: {
    port: process.env.PORT || 3000
  },
  kafka: {
    clientId: process.env.KAFKA_CLIENT_ID || 'ecom-backend',
    brokers: [process.env.KAFKA_BROKER || 'localhost:9092'],
    groupId: process.env.KAFKA_GROUP_ID || 'ecom-backend-group',
    topic: process.env.KAFKA_TOPIC || 'ecom-events'
  },
  db: {
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'ecom',
    port: process.env.DB_PORT || 5432
  }
};
