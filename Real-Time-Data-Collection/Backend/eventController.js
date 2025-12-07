const express = require('express');
const router = express.Router();
const kafkaService = require('../services/kafkaService');

router.post('/collect', async (req, res) => {
    try {
        const eventData = req.body;

        if (!eventData.userId || !eventData.event) {
            return res.status(400).json({ error: "Missing required fields" });
        }

        await kafkaService.sendEvent(eventData);

        return res.status(200).json({ message: "Event received", event: eventData });
    } catch (error) {
        console.error("Error in /event/collect:", error);
        return res.status(500).json({ error: "Failed to process event" });
    }
});

// Simple debug test
router.get("/view", (req, res) => {
    res.send("Event API working");
});

module.exports = router;
