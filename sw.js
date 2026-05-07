/**
 * NEPA-PRO Tradesmen — Service Worker
 *
 * Strategy:
 *   - Precache the app shell + icons on install (fast first load offline).
 *   - Stale-while-revalidate for static assets (icons, manifest).
 *   - Network-first with cache fallback for HTML (always fresh when online).
 *   - Pass-through for cross-origin (Stripe, fonts, telephony intents).
 *
 * Bump `VERSION` on each deploy to invalidate the old cache.
 */

const VERSION = "v1.0.0";
const STATIC_CACHE = `tradesmen-static-${VERSION}`;
const RUNTIME_CACHE = `tradesmen-runtime-${VERSION}`;

const APP_SHELL = [
  "/",
  "/index.html",
  "/manifest.webmanifest",
  "/icons/favicon.ico",
  "/icons/favicon-16x16.png",
  "/icons/favicon-32x32.png",
  "/icons/apple-touch-icon.png",
  "/icons/android-chrome-192x192.png",
  "/icons/android-chrome-512x512.png",
  "/icons/icon-maskable-192.png",
  "/icons/icon-maskable-512.png",
  "/icons/safari-pinned-tab.svg",
  "/icons/og-card.png"
];

// ----- INSTALL: precache shell -----
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      return cache.addAll(APP_SHELL).catch((err) => {
        console.warn("[SW] Pre-cache partial failure:", err);
      });
    }).then(() => self.skipWaiting())
  );
});

// ----- ACTIVATE: clean old caches -----
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys
          .filter((k) => k.startsWith("tradesmen-") &&
                        k !== STATIC_CACHE && k !== RUNTIME_CACHE)
          .map((k) => caches.delete(k))
      );
    }).then(() => self.clients.claim())
  );
});

// ----- FETCH: route by request type -----
self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET and cross-origin
  if (request.method !== "GET") return;
  if (url.origin !== self.location.origin) return;
  // Don't cache Stripe checkout redirects or external API calls
  if (url.pathname.startsWith("/api/")) return;

  // HTML: network-first
  if (request.mode === "navigate" || request.destination === "document") {
    event.respondWith(networkFirst(request));
    return;
  }

  // Static assets: stale-while-revalidate
  event.respondWith(staleWhileRevalidate(request));
});

async function networkFirst(request) {
  const cache = await caches.open(RUNTIME_CACHE);
  try {
    const response = await fetch(request);
    cache.put(request, response.clone());
    return response;
  } catch (err) {
    const cached = await cache.match(request);
    if (cached) return cached;
    // Fallback to cached index.html for any navigation
    const fallback = await caches.match("/index.html");
    return fallback || new Response("Offline", { status: 503 });
  }
}

async function staleWhileRevalidate(request) {
  const cache = await caches.open(RUNTIME_CACHE);
  const cached = await cache.match(request);
  const fetchPromise = fetch(request).then((response) => {
    if (response && response.status === 200) {
      cache.put(request, response.clone());
    }
    return response;
  }).catch(() => cached);
  return cached || fetchPromise;
}

// ----- MESSAGE: allow client to trigger immediate update -----
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});
