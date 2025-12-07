const { Kafka } = require("kafkajs");

const kafka = new Kafka({
    clientId: "ecommerce-backend",
    brokers: [process.env.KAFKA_BROKER || "kafka:9092"]
});

let producer = null;

async function connectProducer() {
    producer = kafka.producer();
    await producer.connect();
    console.log("Kafka Producer connected");
}

async function sendMessage(topic, message) {
    if (!producer) {
        throw new Error("Producer not connected");
    }

    await producer.send({
        topic,
        messages: [{ value: message }]
    });
}

module.exports = {
    connectProducer,
    sendMessage
};
