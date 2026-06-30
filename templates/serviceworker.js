const STATIC_CACHE = 'pos-static-v1';
const DYNAMIC_CACHE = 'pos-dynamic-v1';
const urlsToCache = [
  '/',
  '/inventario/',
  '/productos/',
  '/productos/crear/',
  '/inventario/mermas/crear/',
  '/static/manifest.json',
  '/static/inventario/css/inventario.css',
  '/static/img/no-image.png',
  '/static/js/offline/idb.js',
  '/static/js/offline/queue.js',
  '/static/js/offline/products-offline.js',
  '/static/js/offline/inventario-offline.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => cache.addAll(urlsToCache))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(key => key !== STATIC_CACHE && key !== DYNAMIC_CACHE)
          .map(key => caches.delete(key))
    ))
    .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  if (event.request.url.includes('/serviceworker.js')) return;

  const requestUrl = new URL(event.request.url);

  if (event.request.mode === 'navigate' || requestUrl.pathname === '/') {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const copy = response.clone();
          caches.open(DYNAMIC_CACHE).then(cache => cache.put(event.request, copy));
          return response;
        })
        .catch(() => caches.match(event.request).then(cached => cached || caches.match('/')))
    );
    return;
  }

  if (requestUrl.origin === location.origin && requestUrl.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(event.request).then(cached => {
        return cached || fetch(event.request).then(response => {
          const copy = response.clone();
          caches.open(DYNAMIC_CACHE).then(cache => cache.put(event.request, copy));
          return response;
        });
      })
    );
    return;
  }

  event.respondWith(fetch(event.request).catch(() => caches.match(event.request)));
});