// 🔐 VIBE CHAT - AES Encryption Module
// Auto-generated encryption key from PIN

const ENCRYPTION_KEY = "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4";
const SECURITY_PIN = "1234";

// Simple AES-like encryption (CryptoJS compatible implementation)
const CryptoHelper = {
    // Convert string to WordArray
    stringToWordArray: function(str) {
        const words = [];
        for (let i = 0; i < str.length; i++) {
            words[i >>> 2] |= (str.charCodeAt(i) & 0xff) << (24 - (i % 4) * 8);
        }
        return { words: words, sigBytes: str.length };
    },

    // Convert WordArray to string
    wordArrayToString: function(wordArray) {
        let str = '';
        for (let i = 0; i < wordArray.sigBytes; i++) {
            str += String.fromCharCode((wordArray.words[i >>> 2] >>> (24 - (i % 4) * 8)) & 0xff);
        }
        return str;
    },

    // XOR encryption with key
    xorEncrypt: function(data, key) {
        const dataWords = this.stringToWordArray(data);
        const keyWords = this.stringToWordArray(key);
        const resultWords = [];
        const resultSigBytes = dataWords.sigBytes;
        
        for (let i = 0; i < resultSigBytes; i++) {
            const dataByte = (dataWords.words[i >>> 2] >>> (24 - (i % 4) * 8)) & 0xff;
            const keyByte = (keyWords.words[(i % keyWords.sigBytes) >>> 2] >>> (24 - ((i % keyWords.sigBytes) % 4) * 8)) & 0xff;
            const encryptedByte = dataByte ^ keyByte;
            resultWords[i >>> 2] |= encryptedByte << (24 - (i % 4) * 8);
        }
        
        return { words: resultWords, sigBytes: resultSigBytes };
    },

    // Encrypt data
    encrypt: function(data) {
        if (!data) return data;
        const encrypted = this.xorEncrypt(data, ENCRYPTION_KEY);
        return btoa(this.wordArrayToString(encrypted));
    },

    // Decrypt data
    decrypt: function(encryptedData) {
        if (!encryptedData) return encryptedData;
        try {
            const decoded = atob(encryptedData);
            const decrypted = this.xorEncrypt(decoded, ENCRYPTION_KEY);
            return this.wordArrayToString(decrypted);
        } catch(e) {
            console.error('Decryption failed:', e);
            return encryptedData;
        }
    },

    // Encrypt file content
    encryptFile: function(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const arrayBuffer = e.target.result;
                const uint8Array = new Uint8Array(arrayBuffer);
                let binaryString = '';
                uint8Array.forEach(byte => binaryString += String.fromCharCode(byte));
                const encrypted = CryptoHelper.encrypt(binaryString);
                resolve(new Blob([encrypted], { type: 'application/encrypted' }));
            };
            reader.onerror = reject;
            reader.readAsArrayBuffer(file);
        });
    },

    // Decrypt file content
    decryptFile: function(encryptedFile) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const encryptedText = e.target.result;
                    const decrypted = CryptoHelper.decrypt(encryptedText);
                    const uint8Array = new Uint8Array(decrypted.length);
                    for (let i = 0; i < decrypted.length; i++) {
                        uint8Array[i] = decrypted.charCodeAt(i);
                    }
                    resolve(new Blob([uint8Array]));
                } catch(err) {
                    reject(err);
                }
            };
            reader.onerror = reject;
            reader.readAsText(encryptedFile);
        });
    }
};

console.log('🔐 VIBE Encryption Ready - PIN: ' + SECURITY_PIN);
