const C='igstudio-v5';
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.add('./')).catch(()=>{}));self.skipWaiting()});
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(n=>n!=C).map(n=>caches.delete(n)))).then(()=>clients.claim())));
self.addEventListener('fetch',e=>{
  if(e.request.method!='GET'||new URL(e.request.url).origin!=location.origin)return;
  e.respondWith(fetch(e.request).then(r=>{const k=r.clone();caches.open(C).then(c=>c.put(e.request,k));return r}).catch(()=>caches.match(e.request)||caches.match('./')));
});
