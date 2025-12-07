# Client-Side Ecommerce Tracker

A complete client-side JavaScript tracker SDK for e-commerce events. This tracker captures user interactions (pageviews, product views, add-to-cart, search queries, etc.), batches events, and sends them to a server endpoint in real time. It supports offline mode, retries with exponential backoff, and stores events in `localStorage` to prevent data loss:contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}.

## How It Works

- **Initialization**: Call `tracker.init(config)` on page load. This sets up user and session IDs, and starts event listeners (scroll depth, time-on-page, online/offline events).
- **User/Session IDs**: A persistent **user_id** is generated once and stored in `localStorage`. Each session (period of user activity) gets a new **session_id**. By default, a session times out after 30 minutes of inactivity, similar to Google Analytics session logic:contentReference[oaicite:2]{index=2}.
- **Event Tracking**: Use `tracker.track(eventType, payload)` to record events. The payload can be any JSON object (e.g., `{ product_id: 123 }`).
- **Automatic Events**: The tracker automatically sends a `scroll_depth` event on page unload, containing the maximum scroll percentage, and a `time_on_page` event with time spent on the page.
- **Event Format**: Every event is a JSON object:
  ```json
  {
    "event_id": "UUID",
    "event_type": "event name",
    "timestamp": "ISO timestamp",
    "session_id": "UUID",
    "user_id": "UUID",
    "device": { ...device info... },
    "context": { "url": "...", "referrer": "...", "title": "..." },
    "payload": { ...custom data... }
  }
