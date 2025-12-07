const express = require('express');
const app = express();

const kafkaService = require('./services/kafkaService');
const dbService = require('./dbService');
const eventController = require('./controllers/eventController');

app.use(express.json());

// Health endpoint
app.get("/health", (req, res) => {
    res.status(200).send("OK");
});

// Event API routes
app.use("/event", eventController);

const PORT = process.env.PORT || 8080;

async function startServer() {
    try {
        console.log("Connecting Kafka Producer...");
        await kafkaService.connectProducer();
        console.log("Kafka Producer connected");

        console.log("Connecting PostgreSQL...");
        await dbService.connect();
        console.log("Database connected");

        app.listen(PORT, () => {
            console.log(`Backend server running on port ${PORT}`);
        });
    } catch (err) {
        console.error("❌ Server failed to start:", err);
        process.exit(1);
    }
}

startServer();
