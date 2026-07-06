// 💚 VIBE CHAT - WhatsApp Style Configuration
// 🔐 Encrypted - PIN: 1234

const firebaseConfig = {
    apiKey: "AIzaSyDqh0Gtl0lIZl8Rt1PvdE67U8yyhjxpJdw",
    authDomain: "gomr-3356f.firebaseapp.com",
    databaseURL: "https://gomr-3356f-default-rtdb.firebaseio.com",
    projectId: "gomr-3356f",
    storageBucket: "gomr-3356f.firebasestorage.app",
    messagingSenderId: "470296286364",
    appId: "1:470296286364:web:2bb6e28a2095757da88959"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.database();

const APP_CONFIG = {
    name: 'VIBE Chat',
    version: '2.0.0',
    pin: '1234',
    primaryColor: '#075e54',
    secondaryColor: '#128c7e'
};

console.log('💚 %cVIBE Chat %cv2.0.0 %c🔐 Secured', 'color: #075e54; font-weight: bold;', 'color: #128c7e;', 'color: #25d366;');
