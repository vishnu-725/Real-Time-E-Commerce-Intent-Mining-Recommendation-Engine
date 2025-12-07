// session.js
import { generateUUID, nowTimestamp } from './utils.js';

const USER_ID_KEY = 'tracker_user_id';
const SESSION_ID_KEY = 'tracker_session_id';
const SESSION_START_KEY = 'tracker_session_start';

export const Session = {
  // Initialize session and user IDs
  init() {
    this.initUserId();
    this.initSessionId();
  },

  // Retrieve or generate a persistent user ID
  initUserId() {
    let userId = localStorage.getItem(USER_ID_KEY);
    if (!userId) {
      userId = generateUUID();
      localStorage.setItem(USER_ID_KEY, userId);
    }
    this.userId = userId;
  },

  // Start a new session if none exists or if timed out
  initSessionId() {
    const lastSessionStart = localStorage.getItem(SESSION_START_KEY);
    const now = Date.now();
    const SESSION_TIMEOUT = 30 * 60 * 1000; // 30 minutes inactivity

    // If no session or last session was too long ago, create a new one
    if (!lastSessionStart || (now - lastSessionStart) > SESSION_TIMEOUT) {
      const sessionId = generateUUID();
      localStorage.setItem(SESSION_ID_KEY, sessionId);
      localStorage.setItem(SESSION_START_KEY, now.toString());
      this.sessionId = sessionId;
    } else {
      // Reuse existing session
      this.sessionId = localStorage.getItem(SESSION_ID_KEY);
      // Extend session time on interaction
      localStorage.setItem(SESSION_START_KEY, now.toString());
    }
  },

  // Get current session ID
  getSessionId() {
    return this.sessionId;
  },

  // Get persistent user ID
  getUserId() {
    return this.userId;
  }
};
