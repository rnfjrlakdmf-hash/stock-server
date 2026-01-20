import { Capacitor } from '@capacitor/core';

// API Base URL
// Web/Server: Use current hostname (supports localhost, 0.0.0.0, and local IP)
// Android Emulator: "http://10.0.2.2:8000" (via Capacitor detection)
// More robust check for Android environment (including WebView)
const isAndroid = typeof window !== 'undefined' && (
    Capacitor.getPlatform() === 'android' ||
    /Android/i.test(navigator.userAgent)
);

let apiBase = "http://localhost:8000";

if (process.env.NEXT_PUBLIC_API_URL) {
    apiBase = process.env.NEXT_PUBLIC_API_URL;
    if (apiBase.includes('replace-with-your-server')) {
        console.error('[Config] CRITICAL: API URL is still set to placeholder! Please update .env.production');
        // Fallback to local IP if possible, or keep as is (which will fail, but visible in logs)
    }
} else if (typeof window !== 'undefined') {
    if (isAndroid) {
        // Android Emulator or Device in Dev Mode
        // If you want to test on real device with local backend, use your PC's IP or Ngrok
        // For production build, NEXT_PUBLIC_API_URL should be set in .env.production
        apiBase = "http://10.0.2.2:8000"; // Default Android Emulator Loopback
    } else {
        // Web Browser / Desktop
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            apiBase = "http://localhost:8000";
        } else {
            apiBase = `http://${window.location.hostname}:8000`;
        }
    }
    console.log(`[Config] Running on ${isAndroid ? 'Android' : 'Web'}, API URL: ${apiBase}`);
}

export const API_BASE_URL = apiBase;
