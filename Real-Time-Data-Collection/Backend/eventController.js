const express = require('express');
const router = express.Router();
const kafkaService = require('../services/kafkaService');

// Collect user event
router.post("/collect", async (req, res) => {
    const event = req.body;

    if (!event || !event.userId || !event.action) {
        return res.status(400).json({ error: "Invalid event" });
    }

    try {
        await kafkaService.sendMessage("user-events", JSON.stringify(event));
        res.status(200).json({ status: "Event received" });
    } catch (error) {
        console.error("Error sending event:", error);
        res.status(500).json({ error: "Failed to send event" });
    }
});

// Simple test route
router.get("/view", (req, res) => {
    res.send("Event API Running");
});

module.exports = router;
