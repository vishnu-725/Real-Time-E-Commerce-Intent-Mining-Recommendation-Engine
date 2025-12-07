const { Kafka } = require('kafkajs');
const config = require('./config');
const dbService = require('./services/dbService');

// Initialize Kafka consumer
const kafka = new Kafka({
  clientId: config.kafka.clientId,
  brokers: config.kafka.brokers
});

const consumer = kafka.consumer({ groupId: config.kafka.groupId });

/**
 * Starts the Kafka consumer to listen for events and save to DB.
 */
async function runConsumer() {
  try {
    // Initialize database
    await dbService.initDb();
    await consumer.connect();
    await consumer.subscribe({ topic: config.kafka.topic, fromBeginning: true });
    console.log('Kafka consumer connected and subscribed to', config.kafka.topic);

    await consumer.run({
      eachMessage: async ({ message }) => {
        const event = JSON.parse(message.value.toString());
        console.log('Consumed event:', event.event_type, 'ID:', event.event_id);
        try {
          await dbService.saveEvent(event);
        } catch (dbError) {
          console.error('Error saving event to DB:', dbError);
        }
      }
    });
  } catch (error) {
    console.error('Error running consumer:', error);
    process.exit(1);
  }
}

runConsumer();
