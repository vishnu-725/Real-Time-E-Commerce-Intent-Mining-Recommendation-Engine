// utils.js
// Helper functions for generating unique IDs and formatting timestamps.

// Generate a UUID v4 (for event_id, session_id, user_id, etc.)
export function generateUUID() {
  // Use crypto API if available for secure random values
  if (window.crypto && window.crypto.getRandomValues) {
    const buf = new Uint16Array(8);
    window.crypto.getRandomValues(buf);
    // Convert to hexadecimal and format in UUID v4 pattern
    const S4 = num => {
      let ret = num.toString(16);
      while (ret.length < 4) ret = '0' + ret;
      return ret;
    };
    return (
      S4(buf[0]) + S4(buf[1]) + '-' +
      S4(buf[2]) + '-' +
      // Set high bits of 7th byte to '4'
      ((S4(buf[3]) & 0x0fff) | 0x4000).toString(16) + '-' +
      // Set high bits of 9th byte to variant '8','9','A','B'
      ((S4(buf[4]) & 0x3fff) | 0x8000).toString(16) + '-' +
      S4(buf[5]) + S4(buf[6]) + S4(buf[7])
    );
  } else {
    // Fallback to Math.random (less ideal)
    const template = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx';
    return template.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
}

// Get current ISO timestamp
export function nowTimestamp() {
  return new Date().toISOString();
}
