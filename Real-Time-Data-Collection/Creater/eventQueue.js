// eventQueue.js
import { nowTimestamp, generateUUID } from './utils.js';
import { Device } from './device.js';
import { Session } from './session.js';

export class EventQueue {
  constructor(config = {}) {
    // Configuration: endpoint URL, batch size, interval, retry limits, etc.
    this.endpoint = config.endpoint || '/collect'; 
    this.batchSize = config.batchSize || 10; 
    this.batchInterval = config.batchInterval || 5000; // 5s
    this.maxRetries = config.maxRetries || 5;
    this.retryInitialDelay = config.retryInitialDelay || 1000; // 1s
    
    this.queue = []; // In-memory queue
    this.retryCount = 0;
    this.loadingFromStorage();
    this.startBatchTimer();
    this.setupOnlineOfflineListeners();
    this.scheduleHealthPing();
  }

  // Load unsent events from localStorage
  loadingFromStorage() {
    const saved = localStorage.getItem('tracker_queue');
    if (saved) {
      try {
        this.queue = JSON.parse(saved);
      } catch (e) {
        console.warn('Failed to parse saved queue', e);
        this.queue = [];
      }
    }
  }

  // Save current queue to localStorage (for offline safety)
  saveToStorage() {
    try {
      localStorage.setItem('tracker_queue', JSON.stringify(this.queue));
    } catch (e) {
      // Quota exceeded or not available
      console.warn('Could not save queue to localStorage', e);
    }
  }

  // Start periodic batch sending
  startBatchTimer() {
    setInterval(() => this.sendBatch(), this.batchInterval);
  }

  // Listen to online/offline events
  setupOnlineOfflineListeners() {
    window.addEventListener('online', () => {
      console.log('Network online: attempting to send queued events');
      this.sendBatch();
    });
    window.addEventListener('offline', () => {
      console.log('Network offline: events will be queued in localStorage');
    });
    // On unload, attempt final send and save queue
    window.addEventListener('beforeunload', () => {
      this.sendBatch(true);
    });
  }

  // Enqueue a new event
  enqueue(eventType, payload = {}) {
    const event = {
      event_id: generateUUID(),
      event_type: eventType,
      timestamp: nowTimestamp(),
      session_id: Session.getSessionId(),
      user_id: Session.getUserId(),
      device: Device.getInfo(),
      context: {
        url: window.location.href,
        referrer: document.referrer,
        title: document.title
      },
      payload: payload
    };
    this.queue.push(event);
    this.saveToStorage();

    // If batch size reached, send immediately
    if (this.queue.length >= this.batchSize) {
      this.sendBatch();
    }
  }

  // Send a batch of events (all queued or only batchSize?)
  async sendBatch(isUnload = false) {
    if (!navigator.onLine) {
      // Can't send if offline
      return;
    }
    if (this.queue.length === 0) return;

    // Copy and clear queue for sending
    const batch = [...this.queue];
    if (!isUnload) {
      this.queue = [];
      this.saveToStorage();
    }

    try {
      const response = await fetch(this.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(batch)
      });
      if (!response.ok) {
        throw new Error(`Server responded ${response.status}`);
      }
      // Success: reset retry counter
      this.retryCount = 0;
      // If sent as unload, we cannot rely on async, but we tried
    } catch (err) {
      console.warn('Send failed, will retry with backoff', err);
      // If send fails, put events back in queue
      this.queue = batch.concat(this.queue);
      this.saveToStorage();
      this.retryCount++;
      if (this.retryCount <= this.maxRetries) {
        const delay = this.retryInitialDelay * Math.pow(2, this.retryCount - 1);
        setTimeout(() => this.sendBatch(), delay);
      } else {
        console.error('Max retries reached, events may be lost');
      }
    }
  }

  // Periodic health ping to check service availability
  scheduleHealthPing() {
    setInterval(() => {
      this.enqueue('health_ping', { status: 'alive' });
      // Immediately try to send without waiting for batch interval
      this.sendBatch();
    }, 5 * 60 * 1000); // every 5 minutes
  }
}
