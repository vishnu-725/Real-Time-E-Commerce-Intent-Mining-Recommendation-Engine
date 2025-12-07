const { Kafka } = require("kafkajs");

const kafka = new Kafka({
    clientId: "ecommerce-app",
    brokers: [process.env.KAFKA_BROKER]
});

let producer = null;

module.exports = {
    connectProducer: async () => {
        if (!producer) {
            producer = kafka.producer();
            await producer.connect();
        }
    },

    produceMessage: async (topic, message) => {
        if (!producer) await module.exports.connectProducer();

        await producer.send({
            topic,
            messages: [{ value: JSON.stringify(message) }]
        });
    }
};
