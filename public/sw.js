/* DA Launchpad service worker (hand-written). Scope = the site base path.
 * - Install: precache app shell + every built page/asset listed in precache.json (written by scripts/gen-sw.mjs).
 * - Navigations: network-first with cache fallback (offline works, updates arrive when online).
 * - /data/ files, pagefind, sql-wasm: stale-while-revalidate runtime cache.
 * - Pyodide CDN (jsDelivr): cache-first runtime cache.
 */
const VERSION = 'v1';
const SHELL = 'dal-shell-' + VERSION;
const RUNTIME = 'dal-runtime-' + VERSION;
const PYO = 'dal-pyodide-' + VERSION;
const scope = self.registration.scope;

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(SHELL);
    let list = [];
    try { list = await (await fetch(new URL('precache.json', scope), { cache: 'no-store' })).json(); } catch (e) { /* dev or missing */ }
    list = [''].concat(list);
    // add individually so one failure doesn't abort install
    await Promise.all(list.map((p) => cache.add(new Request(new URL(p, scope), { cache: 'reload' })).catch(() => {})));
    self.skipWaiting();
  })());
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const keep = [SHELL, RUNTIME, PYO];
    for (const k of await caches.keys()) if (!keep.includes(k)) await caches.delete(k);
    await self.clients.claim();
  })());
});

async function staleWhileRevalidate(req, name) {
  const cache = await caches.open(name);
  const hit = await cache.match(req);
  const net = fetch(req).then((res) => { if (res.ok) cache.put(req, res.clone()); return res; }).catch(() => hit);
  return hit || net;
}

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const u = new URL(req.url);
  if (u.hostname === 'cdn.jsdelivr.net') {
    event.respondWith((async () => {
      const cache = await caches.open(PYO);
      const hit = await cache.match(req);
      if (hit) return hit;
      const res = await fetch(req);
      if (res.ok) cache.put(req, res.clone());
      return res;
    })());
    return;
  }
  if (u.origin !== location.origin || !u.href.startsWith(scope)) return;
  const rel = u.href.slice(scope.length);
  if (req.mode === 'navigate') {
    event.respondWith((async () => {
      try {
        const res = await fetch(req);
        const c = await caches.open(SHELL); c.put(req, res.clone());
        return res;
      } catch (e) {
        return (await caches.match(req, { ignoreSearch: true })) || (await caches.match(new URL('', scope))) || Response.error();
      }
    })());
    return;
  }
  if (/^(data\/|pagefind\/|sql-wasm\.wasm|practice-data\.json)/.test(rel)) {
    event.respondWith(staleWhileRevalidate(req, RUNTIME));
    return;
  }
  event.respondWith((async () => (await caches.match(req)) || staleWhileRevalidate(req, RUNTIME))());
});
