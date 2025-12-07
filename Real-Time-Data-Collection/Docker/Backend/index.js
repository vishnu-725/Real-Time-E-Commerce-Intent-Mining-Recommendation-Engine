const express = require('express');
const app = express();

const kafkaService = require('./services/kafkaService');
const dbService = require('./dbService');
const eventController = require('./controllers/eventController');

app.use(express.json());

// Health check
app.get("/health", (req, res) => {
    res.status(200).send("OK");
});

// API route
app.use("/event", eventController);

const PORT = process.env.PORT || 8080;

async function startServer() {
    try {
        await kafkaService.connectProducer();
        console.log("Kafka Producer connected");

        await dbService.connect();
        console.log("Database connected");

        app.listen(PORT, () => {
            console.log(`Server running on port ${PORT}`);
        });
    } catch (err) {
        console.error("Failed to start server:", err);
    }
}

startServer();
