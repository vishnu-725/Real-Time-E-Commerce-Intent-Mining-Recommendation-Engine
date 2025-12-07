// index.js
import { Session } from './session.js';
import { EventQueue } from './eventQueue.js';

// Single shared event queue instance
let queue = null;

// Main Tracker class
class Tracker {
  constructor(config = {}) {
    this.config = config;
  }

  // Initialize tracker (should be called once)
  init() {
    // Set up session/user IDs
    Session.init();
    // Set up event queue with config
    queue = new EventQueue(this.config);
    // Track time on page: send event on unload with time spent
    this.startTime = Date.now();
    window.addEventListener('beforeunload', () => {
      const timeSpent = Date.now() - this.startTime;
      queue.enqueue('time_on_page', { milliseconds: timeSpent });
      // Attempt to send on page unload
      queue.sendBatch(true);
    });
    // Track scroll depth
    this.trackScrollDepth();
  }

  // Track a custom event
  track(eventType, payload = {}) {
    if (!queue) {
      console.error('Tracker not initialized. Call tracker.init() first.');
      return;
    }
    queue.enqueue(eventType, payload);
  }

  // Set up scroll tracking to record maximum scroll percentage
  trackScrollDepth() {
    let maxScrollPerc = 0;
    window.addEventListener('scroll', () => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const docHeight = Math.max(
        document.body.scrollHeight, document.documentElement.scrollHeight,
        document.body.offsetHeight, document.documentElement.offsetHeight,
        document.body.clientHeight, document.documentElement.clientHeight
      );
      const winHeight = window.innerHeight;
      const currentPerc = ((scrollTop + winHeight) / docHeight) * 100;
      if (currentPerc > maxScrollPerc) {
        maxScrollPerc = currentPerc;
      }
    });
    window.addEventListener('beforeunload', () => {
      // When user leaves, send final scroll depth if any scrolling occurred
      if (maxScrollPerc > 0) {
        queue.enqueue('scroll_depth', { percent: Math.round(maxScrollPerc) });
      }
    });
  }
}

// Export a single instance (SDK)
const tracker = new Tracker();
// Provide named export for flexibility if needed
export default tracker;
