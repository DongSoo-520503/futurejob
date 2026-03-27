// FutureJob 서비스 워커 — 대용량 데이터 파일 캐싱
const CACHE_NAME      = 'futurejob-static-v1';
const DATA_CACHE_NAME = 'futurejob-data-v1';

// 설치 시 기본 파일 캐시
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache =>
      cache.addAll(['/index.html', '/style.css'])
    )
  );
  self.skipWaiting();
});

// 이전 버전 캐시 정리
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(k => k !== CACHE_NAME && k !== DATA_CACHE_NAME)
          .map(k => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // ── data/*.json : 캐시 우선 (처음 한 번만 다운로드) ──────────
  if (url.pathname.startsWith('/data/') && url.pathname.endsWith('.json')) {
    event.respondWith(
      caches.open(DATA_CACHE_NAME).then(cache =>
        cache.match(event.request).then(cached => {
          if (cached) return cached;                          // 캐시 있으면 즉시 반환
          return fetch(event.request).then(response => {
            if (response.ok) cache.put(event.request, response.clone());
            return response;
          }).catch(() => cached);                            // 오프라인 대비
        })
      )
    );
    return;
  }

  // ── 그 외 : 네트워크 우선, 실패 시 캐시 ─────────────────────
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});
