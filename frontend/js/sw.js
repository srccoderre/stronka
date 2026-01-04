// Service Worker for PWA
const CACHE_NAME = 'portfel-v1';
const STATIC_CACHE = [
    '/',
    '/index.html',
    '/css/style.css',
    '/js/api/index.js',
    '/js/app/init.js',
    '/manifest.json',
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('Caching static assets');
            return cache.addAll(STATIC_CACHE);
        })
    );
    self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames
                    .filter((name) => name !== CACHE_NAME)
                    .map((name) => caches.delete(name))
            );
        })
    );
    self.clients.claim();
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            if (response) {
                return response;
            }

            return fetch(event.request).then((response) => {
                // Don't cache API requests
                if (event.request.url.includes('/api/')) {
                    return response;
                }

                // Cache successful GET requests
                if (event.request.method === 'GET' && response.status === 200) {
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseToCache);
                    });
                }

                return response;
            });
        })
    );
});

// Background sync for offline data
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-data') {
        event.waitUntil(syncData());
    }
});

async function syncData() {
    // Sync offline data when connection is restored
    console.log('Syncing offline data...');
    // Implementation would sync IndexedDB data to API
}
