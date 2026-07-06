// 💾 VIBE CHAT - External Storage Handler
// 🔐 All files encrypted before storage

const ExternalStorage = {
    DB_NAME: 'VIBE_Chat_Storage',
    DB_VERSION: 1,
    STORE_NAME: 'encrypted_files',
    PIN: '1234',
    
    init: function() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.DB_NAME, this.DB_VERSION);
            
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains(this.STORE_NAME)) {
                    db.createObjectStore(this.STORE_NAME, { keyPath: 'id' });
                }
            };
            
            request.onsuccess = (event) => {
                this.db = event.target.result;
                console.log('💾 External storage ready');
                resolve(true);
            };
            
            request.onerror = (event) => {
                console.error('Storage error:', event.target.error);
                reject(event.target.error);
            };
        });
    },
    
    saveFile: function(id, file, metadata = {}) {
        return new Promise((resolve, reject) => {
            CryptoHelper.encryptFile(file).then(encryptedBlob => {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const transaction = ExternalStorage.db.transaction([ExternalStorage.STORE_NAME], 'readwrite');
                    const store = transaction.objectStore(ExternalStorage.STORE_NAME);
                    
                    store.put({
                        id: id,
                        data: e.target.result,
                        type: file.type,
                        name: file.name,
                        encrypted: true,
                        metadata: metadata,
                        timestamp: Date.now()
                    });
                    
                    transaction.oncomplete = () => resolve(id);
                    transaction.onerror = (e) => reject(e.target.error);
                };
                reader.readAsDataURL(encryptedBlob);
            }).catch(reject);
        });
    },
    
    getFile: function(id) {
        return new Promise((resolve, reject) => {
            const transaction = ExternalStorage.db.transaction([ExternalStorage.STORE_NAME], 'readonly');
            const store = transaction.objectStore(ExternalStorage.STORE_NAME);
            const request = store.get(id);
            
            request.onsuccess = (event) => {
                const record = event.target.result;
                if (!record) return resolve(null);
                
                if (record.encrypted && record.data) {
                    const base64Data = record.data.split(',')[1];
                    const encryptedBlob = new Blob([atob(base64Data)], { type: 'application/encrypted' });
                    CryptoHelper.decryptFile(encryptedBlob).then(decryptedBlob => {
                        resolve({
                            blob: new Blob([decryptedBlob], { type: record.type }),
                            name: record.name,
                            type: record.type,
                            metadata: record.metadata
                        });
                    }).catch(reject);
                } else {
                    resolve(record);
                }
            };
            
            request.onerror = (e) => reject(e.target.error);
        });
    },
    
    deleteFile: function(id) {
        return new Promise((resolve, reject) => {
            const transaction = ExternalStorage.db.transaction([ExternalStorage.STORE_NAME], 'readwrite');
            const store = transaction.objectStore(ExternalStorage.STORE_NAME);
            store.delete(id);
            transaction.oncomplete = () => resolve(true);
            transaction.onerror = (e) => reject(e.target.error);
        });
    },
    
    getAllFiles: function() {
        return new Promise((resolve, reject) => {
            const transaction = ExternalStorage.db.transaction([ExternalStorage.STORE_NAME], 'readonly');
            const store = transaction.objectStore(ExternalStorage.STORE_NAME);
            const request = store.getAll();
            request.onsuccess = (e) => resolve(e.target.result);
            request.onerror = (e) => reject(e.target.error);
        });
    }
};

console.log('💾 External Storage Ready');
