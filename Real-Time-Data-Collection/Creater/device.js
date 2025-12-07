// device.js
export const Device = {
  getInfo() {
    const nav = navigator;
    const conn = nav.connection || nav.mozConnection || nav.webkitConnection;
    return {
      userAgent: nav.userAgent,
      platform: nav.platform,
      language: nav.language,
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight,
        pixelRatio: window.devicePixelRatio
      },
      connection: conn ? {
        effectiveType: conn.effectiveType,
        downlink: conn.downlink,
        rtt: conn.rtt
      } : null,
      online: nav.onLine
    };
  }
};
