// sw.js - Service Worker for SecureVault PWA
const CACHE_NAME = 'securevault-v1.0.0';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icons/icon-192.png',
  '/icons/icon-512.png'
];

// تثبيت Service Worker
self.addEventListener('install', (event) => {
  console.log('[SW] Installing Service Worker...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Caching app shell');
        return cache.addAll(ASSETS_TO_CACHE);
      })
      .then(() => {
        console.log('[SW] Skip waiting');
        return self.skipWaiting();
      })
  );
});

// تفعيل Service Worker
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating Service Worker...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => {
            console.log('[SW] Removing old cache:', name);
            return caches.delete(name);
          })
      );
    })
    .then(() => {
      console.log('[SW] Claiming clients');
      return self.clients.claim();
    })
  );
});

// استراتيجية Cache First للصور والفيديوهات
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // للصور والفيديوهات: Cache First
  if (request.destination === 'image' || request.destination === 'video') {
    event.respondWith(
      caches.match(request)
        .then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          return fetch(request)
            .then((response) => {
              if (!response || response.status !== 200) {
                return response;
              }
              const responseToCache = response.clone();
              caches.open(CACHE_NAME)
                .then((cache) => {
                  cache.put(request, responseToCache);
                });
              return response;
            });
        })
    );
    return;
  }

  // للطلبات الأخرى: Network First
  event.respondWith(
    fetch(request)
      .then((response) => {
        const responseToCache = response.clone();
        caches.open(CACHE_NAME)
          .then((cache) => {
            cache.put(request, responseToCache);
          });
        return response;
      })
      .catch(() => {
        return caches.match(request)
          .then((cachedResponse) => {
            return cachedResponse || new Response('Offline', {
              status: 503,
              statusText: 'Service Unavailable'
            });
          });
      })
  );
});

// معالجة التشفير في الخلفية
self.addEventListener('message', (event) => {
  if (event.data && event.data.action === 'encryptFile') {
    handleFileEncryption(event.data.file)
      .then((encryptedData) => {
        event.ports[0].postMessage({
          success: true,
          encryptedData: encryptedData
        });
      })
      .catch((error) => {
        event.ports[0].postMessage({
          success: false,
          error: error.message
        });
      });
  }

  if (event.data && event.data.action === 'decryptFile') {
    handleFileDecryption(event.data.file)
      .then((decryptedData) => {
        event.ports[0].postMessage({
          success: true,
          decryptedData: decryptedData
        });
      })
      .catch((error) => {
        event.ports[0].postMessage({
          success: false,
          error: error.message
        });
      });
  }
});

// تشفير الملفات
async function handleFileEncryption(file) {
  try {
    const arrayBuffer = await file.arrayBuffer();
    
    // توليد مفتاح AES
    const key = await generateAESKey();
    const iv = crypto.getRandomValues(new Uint8Array(12));
    
    // تشفير البيانات
    const encryptedData = await crypto.subtle.encrypt(
      {
        name: 'AES-GCM',
        iv: iv
      },
      key,
      arrayBuffer
    );
    
    // تصدير المفتاح
    const exportedKey = await crypto.subtle.exportKey('raw', key);
    
    // دمج IV + المفتاح + البيانات المشفرة
    const combined = new Uint8Array(iv.length + exportedKey.length + encryptedData.byteLength);
    combined.set(iv, 0);
    combined.set(new Uint8Array(exportedKey), iv.length);
    combined.set(new Uint8Array(encryptedData), iv.length + exportedKey.length);
    
    return combined.buffer;
  } catch (error) {
    console.error('Encryption error:', error);
    throw error;
  }
}

// فك تشفير الملفات
async function handleFileDecryption(encryptedFile) {
  try {
    const arrayBuffer = await encryptedFile.arrayBuffer();
    const data = new Uint8Array(arrayBuffer);
    
    // استخراج IV والمفتاح والبيانات المشفرة
    const iv = data.slice(0, 12);
    const keyData = data.slice(12, 44);
    const encryptedData = data.slice(44);
    
    // استيراد المفتاح
    const key = await crypto.subtle.importKey(
      'raw',
      keyData,
      'AES-GCM',
      false,
      ['decrypt']
    );
    
    // فك التشفير
    const decryptedData = await crypto.subtle.decrypt(
      {
        name: 'AES-GCM',
        iv: iv
      },
      key,
      encryptedData
    );
    
    return decryptedData;
  } catch (error) {
    console.error('Decryption error:', error);
    throw error;
  }
}

// توليد مفتاح AES
async function generateAESKey() {
  return await crypto.subtle.generateKey(
    {
      name: 'AES-GCM',
      length: 256
    },
    true,
    ['encrypt', 'decrypt']
  );
}

// إشعارات Push
self.addEventListener('push', (event) => {
  const options = {
    body: event.data ? event.data.text() : 'تحديث جديد من SecureVault',
    icon: '/icons/icon-192.png',
    badge: '/icons/badge.png',
    vibrate: [200, 100, 200],
    tag: 'securevault-notification',
    data: {
      url: '/'
    }
  };

  event.waitUntil(
    self.registration.showNotification('SecureVault', options)
  );
});

// النقر على الإشعار
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: 'window' })
      .then((clientList) => {
        for (const client of clientList) {
          if (client.url === '/' && 'focus' in client) {
            return client.focus();
          }
        }
        if (clients.openWindow) {
          return clients.openWindow('/');
        }
      })
  );
});
