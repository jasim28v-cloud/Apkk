// 💚 VIBE CHAT - WhatsApp Style App
// 🔐 Encrypted | 💾 External Storage

// ═══════════════ STATE ═══════════════
let currentUser = null;
let currentChatId = null;
let currentChatUser = null;
let chatsList = [];
let pinAttempt = '';
const CORRECT_PIN = '1234';

// ═══════════════ PIN LOCK ═══════════════
function initPinLock() {
    const keypad = document.getElementById('pinKeypad');
    const keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '', '0', 'delete'];
    
    keypad.innerHTML = keys.map(key => {
        if (key === '') return '<div class="pin-key empty"></div>';
        if (key === 'delete') return '<div class="pin-key delete" onclick="deletePinDigit()"><i class="fas fa-delete-left"></i></div>';
        return `<div class="pin-key" onclick="addPinDigit('${key}')">${key}</div>`;
    }).join('');
    
    updatePinDots();
}

function addPinDigit(digit) {
    if (pinAttempt.length >= 4) return;
    pinAttempt += digit;
    updatePinDots();
    
    if (pinAttempt.length === 4) {
        setTimeout(() => {
            if (pinAttempt === CORRECT_PIN) {
                unlockApp();
            } else {
                showPinError();
            }
        }, 200);
    }
}

function deletePinDigit() {
    pinAttempt = pinAttempt.slice(0, -1);
    updatePinDots();
    document.getElementById('pinError').textContent = '';
}

function updatePinDots() {
    const dots = document.querySelectorAll('.pin-dot');
    dots.forEach((dot, i) => {
        dot.classList.toggle('filled', i < pinAttempt.length);
        dot.classList.remove('error');
    });
}

function showPinError() {
    const dots = document.querySelectorAll('.pin-dot');
    dots.forEach(d => d.classList.add('error'));
    document.getElementById('pinError').textContent = '❌ رمز خاطئ! حاول مرة أخرى';
    pinAttempt = '';
    setTimeout(() => {
        dots.forEach(d => d.classList.remove('error', 'filled'));
        document.getElementById('pinError').textContent = '';
    }, 1000);
}

function unlockApp() {
    document.getElementById('pinLock').classList.add('hidden');
    document.getElementById('app').classList.add('visible');
    initApp();
    console.log('🔓 VIBE Chat Unlocked');
}

function lockApp() {
    document.getElementById('pinLock').classList.remove('hidden');
    document.getElementById('app').classList.remove('visible');
    pinAttempt = '';
    updatePinDots();
}

// ═══════════════ APP INIT ═══════════════
async function initApp() {
    await ExternalStorage.init();
    updateStorageInfo();
    setupAuth();
}

function updateStorageInfo() {
    if ('storage' in navigator && 'estimate' in navigator.storage) {
        navigator.storage.estimate().then(estimate => {
            const usedMB = (estimate.usage / 1024 / 1024).toFixed(1);
            const totalMB = (estimate.quota / 1024 / 1024).toFixed(1);
            document.getElementById('storageInfo').textContent = `💾 المستخدم: ${usedMB}MB / المتاح: ${totalMB}MB`;
        });
    }
}

// ═══════════════ AUTH ═══════════════
function setupAuth() {
    auth.onAuthStateChanged(async (user) => {
        if (user) {
            currentUser = {
                uid: user.uid,
                name: user.email.split('@')[0],
                email: user.email,
                avatar: '',
                bio: '💚 VIBE Chat'
            };
            
            const snapshot = await db.ref('users/' + user.uid).once('value');
            if (snapshot.exists()) {
                currentUser = { ...currentUser, ...snapshot.val() };
            } else {
                await db.ref('users/' + user.uid).set(currentUser);
            }
            
            updateProfileUI();
            loadChats();
            listenForMessages();
        } else {
            // Anonymous auth
            auth.signInAnonymously().catch(console.error);
        }
    });
}

// ═══════════════ CHATS ═══════════════
async function loadChats() {
    const snapshot = await db.ref('chats').once('value');
    const chats = snapshot.val();
    const chatList = document.getElementById('chatList');
    
    if (!chats) {
        chatList.innerHTML = '<div style="padding: 40px; text-align: center; color: #667781;">لا توجد محادثات بعد 💚</div>';
        return;
    }
    
    chatsList = [];
    for (const [chatId, messages] of Object.entries(chats)) {
        const [uid1, uid2] = chatId.split('_');
        const otherUid = uid1 === currentUser.uid ? uid2 : uid1;
        const msgs = Object.values(messages || {});
        const lastMsg = msgs.sort((a, b) => b.timestamp - a.timestamp)[0];
        
        const userSnap = await db.ref('users/' + otherUid).once('value');
        const userData = userSnap.val() || { name: 'مستخدم', avatar: '' };
        
        chatsList.push({
            chatId, otherUid, userData, lastMsg,
            timestamp: lastMsg?.timestamp || 0,
            unread: msgs.filter(m => m.senderId !== currentUser.uid && !m.read).length
        });
    }
    
    chatsList.sort((a, b) => b.timestamp - a.timestamp);
    renderChatList();
}

function renderChatList() {
    const chatList = document.getElementById('chatList');
    
    chatList.innerHTML = chatsList.map(chat => {
        let preview = '';
        if (chat.lastMsg) {
            if (chat.lastMsg.text) preview = CryptoHelper.decrypt(chat.lastMsg.text);
            else if (chat.lastMsg.fileName) preview = '📎 ' + chat.lastMsg.fileName;
        }
        
        return `
            <div class="chat-item" onclick="openChat('${chat.otherUid}', '${escapeHtml(chat.userData.name)}')">
                <div class="chat-avatar">
                    ${chat.userData.avatar ? `<img src="${chat.userData.avatar}">` : '<i class="fas fa-user"></i>'}
                </div>
                <div class="chat-info">
                    <div class="chat-name">${escapeHtml(chat.userData.name)}</div>
                    <div class="chat-preview">${escapeHtml(preview.substring(0, 50))}</div>
                </div>
                <div class="chat-meta">
                    <div class="chat-time">${formatTime(chat.timestamp)}</div>
                    ${chat.unread > 0 ? `<div class="chat-unread">${chat.unread}</div>` : ''}
                </div>
            </div>`;
    }).join('');
    
    if (chatsList.length === 0) {
        chatList.innerHTML = '<div style="padding: 40px; text-align: center; color: #667781;">لا توجد محادثات بعد 💚</div>';
    }
}

// ═══════════════ OPEN CHAT ═══════════════
async function openChat(userId, userName) {
    currentChatUser = { uid: userId, name: userName };
    currentChatId = [currentUser.uid, userId].sort().join('_');
    
    document.getElementById('chatViewName').textContent = userName;
    document.getElementById('chatViewAvatar').innerHTML = '<i class="fas fa-user"></i>';
    document.getElementById('chatList').parentElement.style.display = 'none';
    document.getElementById('chatView').classList.add('active');
    document.getElementById('fabButton').style.display = 'none';
    document.getElementById('searchBar').style.display = 'none';
    
    const userSnap = await db.ref('users/' + userId).once('value');
    if (userSnap.exists() && userSnap.val().avatar) {
        document.getElementById('chatViewAvatar').innerHTML = `<img src="${userSnap.val().avatar}">`;
    }
    
    loadMessages();
    listenForNewMessages();
}

function goBack() {
    document.getElementById('chatView').classList.remove('active');
    document.getElementById('chatList').parentElement.style.display = 'block';
    document.getElementById('fabButton').style.display = 'block';
    document.getElementById('searchBar').style.display = 'none';
    currentChatId = null;
    currentChatUser = null;
    loadChats();
}

// ═══════════════ MESSAGES ═══════════════
function loadMessages() {
    const messagesDiv = document.getElementById('chatMessages');
    
    db.ref('chats/' + currentChatId).on('value', (snapshot) => {
        const messages = snapshot.val();
        messagesDiv.innerHTML = `
            <div class="encryption-indicator" style="margin: 8px; border-radius: 8px;">
                🔒 الرسائل مشفرة من الطرف إلى الطرف
            </div>`;
        
        if (!messages) return;
        
        Object.values(messages).sort((a, b) => a.timestamp - b.timestamp).forEach(msg => {
            const isSent = msg.senderId === currentUser.uid;
            const text = msg.text ? CryptoHelper.decrypt(msg.text) : '';
            
            let content = '';
            if (text) {
                content = escapeHtml(text);
            }
            if (msg.fileName) {
                content += `
                    <div class="message-image" onclick="openImageViewer('${msg.fileName}')">
                        📎 ${escapeHtml(msg.fileName)}
                        ${msg.fileType?.startsWith('image/') ? '<br><img src="" id="img_' + msg.timestamp + '" style="max-width:200px;border-radius:8px;">' : ''}
                    </div>`;
            }
            
            messagesDiv.innerHTML += `
                <div class="message ${isSent ? 'sent' : 'received'}">
                    <div class="message-bubble">
                        ${content}
                        <div class="message-time">${formatTime(msg.timestamp)}</div>
                    </div>
                </div>`;
        });
        
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        
        // Load encrypted images
        Object.values(messages).forEach(msg => {
            if (msg.fileName && msg.fileType?.startsWith('image/')) {
                ExternalStorage.getFile(msg.fileName).then(fileData => {
                    if (fileData && fileData.blob) {
                        const url = URL.createObjectURL(fileData.blob);
                        const imgEl = document.getElementById('img_' + msg.timestamp);
                        if (imgEl) imgEl.src = url;
                    }
                });
            }
        });
    });
}

function listenForNewMessages() {
    db.ref('chats/' + currentChatId).on('child_added', () => {
        const messagesDiv = document.getElementById('chatMessages');
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
}

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const text = input.value.trim();
    if (!text || !currentChatId) return;
    
    const encryptedText = CryptoHelper.encrypt(text);
    
    await db.ref('chats/' + currentChatId).push({
        senderId: currentUser.uid,
        text: encryptedText,
        timestamp: Date.now(),
        read: false
    });
    
    input.value = '';
    showToast('✅ تم الإرسال');
}

async function sendFile(input) {
    const file = input.files[0];
    if (!file || !currentChatId) return;
    
    showToast('⏳ جاري رفع وتشفير الملف...');
    
    try {
        const fileId = 'file_' + Date.now() + '_' + file.name;
        await ExternalStorage.saveFile(fileId, file, {
            fileName: file.name,
            fileType: file.type,
            uploadedBy: currentUser.uid
        });
        
        await db.ref('chats/' + currentChatId).push({
            senderId: currentUser.uid,
            fileName: fileId,
            fileType: file.type,
            timestamp: Date.now(),
            read: false
        });
        
        showToast('✅ تم رفع وتشفير الملف');
        updateStorageInfo();
    } catch (err) {
        console.error(err);
        showToast('❌ فشل رفع الملف');
    }
    
    input.value = '';
}

function listenForMessages() {
    db.ref('chats').on('value', (snapshot) => {
        loadChats();
    });
}

// ═══════════════ NEW CHAT ═══════════════
function newChat() {
    const name = prompt('👤 أدخل اسم المستخدم للمحادثة الجديدة:');
    if (!name || !name.trim()) return;
    
    db.ref('users').orderByChild('name').equalTo(name.trim()).once('value', (snapshot) => {
        if (snapshot.exists()) {
            const user = Object.values(snapshot.val())[0];
            openChat(user.uid, user.name);
        } else {
            showToast('❌ المستخدم غير موجود');
        }
    });
}

// ═══════════════ SEARCH ═══════════════
function openSearch() {
    const searchBar = document.getElementById('searchBar');
    searchBar.style.display = searchBar.style.display === 'none' ? 'block' : 'none';
    if (searchBar.style.display === 'block') {
        document.getElementById('searchInput').focus();
    }
}

async function searchUsers() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    if (!query) return;
    
    const snapshot = await db.ref('users').once('value');
    const users = snapshot.val();
    const results = Object.values(users || {}).filter(u => 
        u.name?.toLowerCase().includes(query) && u.uid !== currentUser?.uid
    );
    
    const chatList = document.getElementById('chatList');
    chatList.innerHTML = results.map(u => `
        <div class="chat-item" onclick="openChat('${u.uid}', '${escapeHtml(u.name)}')">
            <div class="chat-avatar">${u.avatar ? `<img src="${u.avatar}">` : '<i class="fas fa-user"></i>'}</div>
            <div class="chat-info"><div class="chat-name">${escapeHtml(u.name)}</div></div>
        </div>
    `).join('') || '<div style="padding: 40px; text-align: center; color: #667781;">لا توجد نتائج</div>';
}

// ═══════════════ PROFILE ═══════════════
function openProfile() {
    document.getElementById('profilePanel').classList.add('open');
    updateProfileUI();
}

function closeProfile() {
    document.getElementById('profilePanel').classList.remove('open');
}

function updateProfileUI() {
    if (!currentUser) return;
    document.getElementById('profileName').textContent = currentUser.name;
    document.getElementById('profileBio').textContent = currentUser.bio || '💚 VIBE Chat';
    document.getElementById('profileAvatar').innerHTML = currentUser.avatar 
        ? `<img src="${currentUser.avatar}">` 
        : '<i class="fas fa-user"></i>';
}

async function changeAvatar() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = async (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = async (ev) => {
                const base64 = ev.target.result;
                await db.ref('users/' + currentUser.uid).update({ avatar: base64 });
                currentUser.avatar = base64;
                updateProfileUI();
                showToast('✅ تم تحديث الصورة');
            };
            reader.readAsDataURL(file);
        }
    };
    input.click();
}

async function changeBio() {
    const bio = prompt('✏️ أدخل الحالة الجديدة:', currentUser.bio);
    if (bio !== null) {
        await db.ref('users/' + currentUser.uid).update({ bio });
        currentUser.bio = bio;
        updateProfileUI();
        showToast('✅ تم تحديث الحالة');
    }
}

// ═══════════════ THEME ═══════════════
function toggleTheme() {
    document.body.classList.toggle('dark');
    const isDark = document.body.classList.contains('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    showToast(isDark ? '🌙 الوضع الليلي' : '☀️ الوضع النهاري');
}

// ═══════════════ LOGOUT ═══════════════
async function logout() {
    if (confirm('تسجيل الخروج؟')) {
        await auth.signOut();
        lockApp();
        showToast('👋 تم تسجيل الخروج');
    }
}

// ═══════════════ IMAGE VIEWER ═══════════════
async function openImageViewer(fileId) {
    const fileData = await ExternalStorage.getFile(fileId);
    if (fileData && fileData.blob) {
        const url = URL.createObjectURL(fileData.blob);
        document.getElementById('viewerImage').src = url;
        document.getElementById('imageViewer').classList.add('open');
    }
}

function closeImageViewer() {
    document.getElementById('imageViewer').classList.remove('open');
}

// ═══════════════ TOAST ═══════════════
function showToast(msg) {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2000);
}

// ═══════════════ UTILS ═══════════════
function formatTime(ts) {
    if (!ts) return '';
    const d = new Date(ts);
    const now = new Date();
    if (d.toDateString() === now.toDateString()) {
        return d.toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' });
    }
    return d.toLocaleDateString('ar-SA', { month: 'short', day: 'numeric' });
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ═══════════════ INIT ═══════════════
document.addEventListener('DOMContentLoaded', () => {
    initPinLock();
    
    // Check saved theme
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark');
    }
    
    // Auto-lock after 5 minutes of inactivity
    let inactivityTimer;
    function resetInactivityTimer() {
        clearTimeout(inactivityTimer);
        inactivityTimer = setTimeout(() => {
            if (!document.getElementById('pinLock').classList.contains('hidden')) return;
            lockApp();
            showToast('🔒 تم قفل التطبيق تلقائياً');
        }, 5 * 60 * 1000);
    }
    
    ['click', 'touchstart', 'keypress'].forEach(evt => {
        document.addEventListener(evt, resetInactivityTimer);
    });
    
    console.log('💚 %cVIBE Chat %cReady %c🔐', 'color: #075e54;', 'color: #128c7e;', 'font-size: 16px;');
});
