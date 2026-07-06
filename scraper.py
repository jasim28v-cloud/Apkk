#!/usr/bin/env python3
"""
scraper.py - Project Generator
ينشئ هيكل مشروع Android كامل داخل مجلد gtheb
لتطبيق SecureVault بواجهة محادثة تشبه واتساب
"""

import os
import json

def create_project_structure():
    """إنشاء هيكل المشروع داخل مجلد gtheb"""
    
    base_path = "gtheb"
    
    # المجلدات الأساسية
    dirs = [
        f"{base_path}/app/src/main/java/com/securevault/app",
        f"{base_path}/app/src/main/java/com/securevault/app/ui",
        f"{base_path}/app/src/main/java/com/securevault/app/crypto",
        f"{base_path}/app/src/main/java/com/securevault/app/database",
        f"{base_path}/app/src/main/java/com/securevault/app/models",
        f"{base_path}/app/src/main/java/com/securevault/app/utils",
        f"{base_path}/app/src/main/res/layout",
        f"{base_path}/app/src/main/res/drawable",
        f"{base_path}/app/src/main/res/values",
        f"{base_path}/app/src/main/res/mipmap-hdpi",
        f"{base_path}/app/src/main/res/mipmap-mdpi",
        f"{base_path}/app/src/main/res/mipmap-xhdpi",
        f"{base_path}/app/src/main/res/mipmap-xxhdpi",
        f"{base_path}/app/src/main/res/mipmap-xxxhdpi",
        f"{base_path}/gradle/wrapper",
        f"{base_path}/.github/workflows",
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    print("[+] Created directory structure")
    
    # ========== BUILD FILES ==========
    
    # build.gradle (Project)
    project_build_gradle = """buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.2.0'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}"""
    
    with open(f"{base_path}/build.gradle", "w") as f:
        f.write(project_build_gradle)
    
    # settings.gradle
    settings_gradle = """rootProject.name = "SecureVault"
include ':app'"""
    
    with open(f"{base_path}/settings.gradle", "w") as f:
        f.write(settings_gradle)
    
    # gradle.properties
    gradle_properties = """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true"""
    
    with open(f"{base_path}/gradle.properties", "w") as f:
        f.write(gradle_properties)
    
    # app/build.gradle
    app_build_gradle = """plugins {
    id 'com.android.application'
}

android {
    namespace 'com.securevault.app'
    compileSdk 34

    defaultConfig {
        applicationId "com.securevault.app"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.recyclerview:recyclerview:1.3.2'
    implementation 'androidx.security:security-crypto:1.1.0-alpha06'
}"""
    
    with open(f"{base_path}/app/build.gradle", "w") as f:
        f.write(app_build_gradle)
    
    # proguard-rules.pro
    with open(f"{base_path}/app/proguard-rules.pro", "w") as f:
        f.write("# Add project specific ProGuard rules here.\n")
    
    print("[+] Build files created")
    
    # ========== ANDROID MANIFEST ==========
    
    android_manifest = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE" 
        tools:ignore="ScopedStorage" />

    <application
        android:allowBackup="false"
        android:icon="@mipmap/ic_launcher"
        android:label="SecureVault"
        android:supportsRtl="true"
        android:theme="@style/Theme.SecureVault"
        android:requestLegacyExternalStorage="true"
        tools:targetApi="31">
        
        <!-- شاشة القفل -->
        <activity
            android:name=".ui.LockScreenActivity"
            android:exported="true"
            android:theme="@style/Theme.SecureVault">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
        <!-- واجهة المحادثة الرئيسية -->
        <activity
            android:name=".ui.ChatActivity"
            android:exported="false" />
            
        <!-- عارض الوسائط -->
        <activity
            android:name=".ui.MediaViewerActivity"
            android:exported="false"
            android:theme="@style/Theme.SecureVault.Fullscreen" />
            
    </application>
</manifest>"""
    
    with open(f"{base_path}/app/src/main/AndroidManifest.xml", "w") as f:
        f.write(android_manifest)
    
    print("[+] AndroidManifest.xml created")
    
    # ========== JAVA SOURCE FILES ==========
    
    src = f"{base_path}/app/src/main/java/com/securevault/app"
    
    # MainApplication.java
    main_app = """package com.securevault.app;

import android.app.Application;
import com.securevault.app.database.DatabaseHelper;
import com.securevault.app.crypto.CryptoManager;

public class MainApplication extends Application {
    private static MainApplication instance;
    private DatabaseHelper databaseHelper;
    private CryptoManager cryptoManager;

    @Override
    public void onCreate() {
        super.onCreate();
        instance = this;
        databaseHelper = new DatabaseHelper(this);
        cryptoManager = new CryptoManager();
    }

    public static MainApplication getInstance() {
        return instance;
    }

    public DatabaseHelper getDatabaseHelper() {
        return databaseHelper;
    }

    public CryptoManager getCryptoManager() {
        return cryptoManager;
    }
}"""
    
    with open(f"{src}/MainApplication.java", "w") as f:
        f.write(main_app)
    
    # CryptoManager.java
    crypto_manager = """package com.securevault.app.crypto;

import android.util.Base64;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;
import javax.crypto.Cipher;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public class CryptoManager {
    private static final String AES_GCM = "AES/GCM/NoPadding";
    private static final int GCM_TAG_LENGTH = 128;
    private static final int GCM_IV_LENGTH = 12;
    private static final String SECRET_PIN = "1234"; // PIN الافتراضي
    
    private SecretKeySpec secretKey;

    public CryptoManager() {
        try {
            byte[] key = deriveKey(SECRET_PIN);
            this.secretKey = new SecretKeySpec(key, "AES");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private byte[] deriveKey(String pin) throws Exception {
        MessageDigest sha = MessageDigest.getInstance("SHA-256");
        return sha.digest(pin.getBytes(StandardCharsets.UTF_8));
    }

    public byte[] encrypt(byte[] data) throws Exception {
        byte[] iv = new byte[GCM_IV_LENGTH];
        new SecureRandom().nextBytes(iv);
        
        Cipher cipher = Cipher.getInstance(AES_GCM);
        GCMParameterSpec spec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, spec);
        
        byte[] encrypted = cipher.doFinal(data);
        
        // دمج IV مع البيانات المشفرة
        byte[] combined = new byte[iv.length + encrypted.length];
        System.arraycopy(iv, 0, combined, 0, iv.length);
        System.arraycopy(encrypted, 0, combined, iv.length, encrypted.length);
        
        return combined;
    }

    public byte[] decrypt(byte[] encryptedData) throws Exception {
        byte[] iv = new byte[GCM_IV_LENGTH];
        byte[] data = new byte[encryptedData.length - GCM_IV_LENGTH];
        
        System.arraycopy(encryptedData, 0, iv, 0, GCM_IV_LENGTH);
        System.arraycopy(encryptedData, GCM_IV_LENGTH, data, 0, data.length);
        
        Cipher cipher = Cipher.getInstance(AES_GCM);
        GCMParameterSpec spec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
        cipher.init(Cipher.DECRYPT_MODE, secretKey, spec);
        
        return cipher.doFinal(data);
    }

    public boolean verifyPin(String pin) {
        return SECRET_PIN.equals(pin);
    }
}"""
    
    with open(f"{src}/crypto/CryptoManager.java", "w") as f:
        f.write(crypto_manager)
    
    # DatabaseHelper.java
    db_helper = """package com.securevault.app.database;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import com.securevault.app.models.VaultFile;
import java.util.ArrayList;
import java.util.List;

public class DatabaseHelper extends SQLiteOpenHelper {
    private static final String DB_NAME = "vault.db";
    private static final int DB_VERSION = 1;
    private static final String TABLE_FILES = "vault_files";
    
    public DatabaseHelper(Context context) {
        super(context, DB_NAME, null, DB_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        String createTable = "CREATE TABLE " + TABLE_FILES + " ("
                + "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                + "original_name TEXT, "
                + "encrypted_name TEXT, "
                + "original_path TEXT, "
                + "vault_path TEXT, "
                + "file_type TEXT, "
                + "size LONG, "
                + "date_added LONG, "
                + "is_video INTEGER DEFAULT 0)";
        db.execSQL(createTable);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_FILES);
        onCreate(db);
    }

    public long addFile(VaultFile file) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put("original_name", file.getOriginalName());
        values.put("encrypted_name", file.getEncryptedName());
        values.put("original_path", file.getOriginalPath());
        values.put("vault_path", file.getVaultPath());
        values.put("file_type", file.getFileType());
        values.put("size", file.getSize());
        values.put("date_added", System.currentTimeMillis());
        values.put("is_video", file.isVideo() ? 1 : 0);
        return db.insert(TABLE_FILES, null, values);
    }

    public List<VaultFile> getAllFiles() {
        List<VaultFile> files = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.query(TABLE_FILES, null, null, null, null, null, "date_added DESC");
        
        if (cursor.moveToFirst()) {
            do {
                VaultFile file = new VaultFile(
                    cursor.getLong(0),
                    cursor.getString(1),
                    cursor.getString(2),
                    cursor.getString(3),
                    cursor.getString(4),
                    cursor.getString(5),
                    cursor.getLong(6),
                    cursor.getLong(7),
                    cursor.getInt(8) == 1
                );
                files.add(file);
            } while (cursor.moveToNext());
        }
        cursor.close();
        return files;
    }

    public void deleteFile(long id) {
        SQLiteDatabase db = this.getWritableDatabase();
        db.delete(TABLE_FILES, "id = ?", new String[]{String.valueOf(id)});
    }
}"""
    
    with open(f"{src}/database/DatabaseHelper.java", "w") as f:
        f.write(db_helper)
    
    # VaultFile.java
    vault_file = """package com.securevault.app.models;

public class VaultFile {
    private long id;
    private String originalName;
    private String encryptedName;
    private String originalPath;
    private String vaultPath;
    private String fileType;
    private long size;
    private long dateAdded;
    private boolean isVideo;

    public VaultFile() {}

    public VaultFile(long id, String originalName, String encryptedName,
                     String originalPath, String vaultPath, String fileType,
                     long size, long dateAdded, boolean isVideo) {
        this.id = id;
        this.originalName = originalName;
        this.encryptedName = encryptedName;
        this.originalPath = originalPath;
        this.vaultPath = vaultPath;
        this.fileType = fileType;
        this.size = size;
        this.dateAdded = dateAdded;
        this.isVideo = isVideo;
    }

    // Getters and Setters
    public long getId() { return id; }
    public void setId(long id) { this.id = id; }
    public String getOriginalName() { return originalName; }
    public void setOriginalName(String n) { this.originalName = n; }
    public String getEncryptedName() { return encryptedName; }
    public void setEncryptedName(String n) { this.encryptedName = n; }
    public String getOriginalPath() { return originalPath; }
    public void setOriginalPath(String p) { this.originalPath = p; }
    public String getVaultPath() { return vaultPath; }
    public void setVaultPath(String p) { this.vaultPath = p; }
    public String getFileType() { return fileType; }
    public void setFileType(String t) { this.fileType = t; }
    public long getSize() { return size; }
    public void setSize(long s) { this.size = s; }
    public long getDateAdded() { return dateAdded; }
    public void setDateAdded(long d) { this.dateAdded = d; }
    public boolean isVideo() { return isVideo; }
    public void setVideo(boolean v) { this.isVideo = v; }
}"""
    
    with open(f"{src}/models/VaultFile.java", "w") as f:
        f.write(vault_file)
    
    # FileUtils.java
    file_utils = """package com.securevault.app.utils;

import android.content.Context;
import android.os.Environment;
import com.securevault.app.MainApplication;
import com.securevault.app.crypto.CryptoManager;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;

public class FileUtils {
    private static final String VAULT_FOLDER = ".SecureVault";
    
    public static File getVaultDir() {
        File vault = new File(Environment.getExternalStorageDirectory(), VAULT_FOLDER);
        if (!vault.exists()) {
            vault.mkdirs();
        }
        // إنشاء ملف .nomedia لإخفاء المحتوى من المعرض
        File nomedia = new File(vault, ".nomedia");
        if (!nomedia.exists()) {
            try {
                nomedia.createNewFile();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return vault;
    }

    public static String encryptAndMoveFile(String originalPath) throws Exception {
        File originalFile = new File(originalPath);
        if (!originalFile.exists()) return null;
        
        CryptoManager crypto = MainApplication.getInstance().getCryptoManager();
        
        // قراءة البيانات الأصلية
        byte[] data = new byte[(int) originalFile.length()];
        FileInputStream fis = new FileInputStream(originalFile);
        fis.read(data);
        fis.close();
        
        // تشفير البيانات
        byte[] encrypted = crypto.encrypt(data);
        
        // حفظ في مجلد المخزن
        String encryptedName = "ENC_" + System.currentTimeMillis() + "_" + originalFile.getName();
        File vaultFile = new File(getVaultDir(), encryptedName);
        FileOutputStream fos = new FileOutputStream(vaultFile);
        fos.write(encrypted);
        fos.close();
        
        return vaultFile.getAbsolutePath();
    }

    public static byte[] decryptFile(String vaultPath) throws Exception {
        File vaultFile = new File(vaultPath);
        if (!vaultFile.exists()) return null;
        
        CryptoManager crypto = MainApplication.getInstance().getCryptoManager();
        
        byte[] encrypted = new byte[(int) vaultFile.length()];
        FileInputStream fis = new FileInputStream(vaultFile);
        fis.read(encrypted);
        fis.close();
        
        return crypto.decrypt(encrypted);
    }

    public static boolean isImage(String fileName) {
        String ext = fileName.toLowerCase();
        return ext.endsWith(".jpg") || ext.endsWith(".jpeg") || 
               ext.endsWith(".png") || ext.endsWith(".gif") || 
               ext.endsWith(".bmp") || ext.endsWith(".webp");
    }

    public static boolean isVideo(String fileName) {
        String ext = fileName.toLowerCase();
        return ext.endsWith(".mp4") || ext.endsWith(".avi") || 
               ext.endsWith(".mkv") || ext.endsWith(".mov") || 
               ext.endsWith(".3gp");
    }
}"""
    
    with open(f"{src}/utils/FileUtils.java", "w") as f:
        f.write(file_utils)
    
    print("[+] Java source files created")
    
    # ========== ACTIVITIES ==========
    
    # LockScreenActivity.java
    lock_screen = """package com.securevault.app.ui;

import android.content.Intent;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.google.android.material.button.MaterialButton;
import com.securevault.app.MainApplication;
import com.securevault.app.R;

public class LockScreenActivity extends AppCompatActivity {
    private EditText pinInput;
    private MaterialButton unlockButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_lock_screen);
        
        pinInput = findViewById(R.id.pin_input);
        unlockButton = findViewById(R.id.unlock_button);
        
        unlockButton.setOnClickListener(v -> {
            String pin = pinInput.getText().toString();
            if (MainApplication.getInstance().getCryptoManager().verifyPin(pin)) {
                startActivity(new Intent(this, ChatActivity.class));
                finish();
            } else {
                Toast.makeText(this, "رمز غير صحيح", Toast.LENGTH_SHORT).show();
            }
        });
    }
}"""
    
    with open(f"{src}/ui/LockScreenActivity.java", "w") as f:
        f.write(lock_screen)
    
    # ChatActivity.java
    chat_activity = """package com.securevault.app.ui;

import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.provider.OpenableColumns;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageButton;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.securevault.app.R;
import com.securevault.app.database.DatabaseHelper;
import com.securevault.app.models.VaultFile;
import com.securevault.app.utils.FileUtils;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

public class ChatActivity extends AppCompatActivity {
    private RecyclerView chatRecyclerView;
    private EditText messageInput;
    private ImageButton sendButton, attachButton;
    private FloatingActionButton fabGallery;
    private ChatAdapter chatAdapter;
    private List<ChatMessage> messages;
    private DatabaseHelper dbHelper;
    private static final int PICK_FILE = 100;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);
        
        dbHelper = MainApplication.getInstance().getDatabaseHelper();
        
        chatRecyclerView = findViewById(R.id.chat_recycler);
        messageInput = findViewById(R.id.message_input);
        sendButton = findViewById(R.id.send_button);
        attachButton = findViewById(R.id.attach_button);
        fabGallery = findViewById(R.id.fab_gallery);
        
        messages = new ArrayList<>();
        chatAdapter = new ChatAdapter(this, messages);
        chatRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        chatRecyclerView.setAdapter(chatAdapter);
        
        // رسالة ترحيب
        addMessage("bot", "مرحباً! هذه خزنتك الآمنة 📱\\nيمكنك إرسال الصور والفيديوهات لتشفيرها وحمايتها\\nالرمز: 1234");
        
        sendButton.setOnClickListener(v -> sendMessage());
        
        attachButton.setOnClickListener(v -> {
            Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            intent.setType("*/*");
            intent.putExtra(Intent.EXTRA_MIME_TYPES, new String[]{"image/*", "video/*"});
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            startActivityForResult(intent, PICK_FILE);
        });
        
        fabGallery.setOnClickListener(v -> loadVaultFiles());
    }

    private void sendMessage() {
        String text = messageInput.getText().toString().trim();
        if (!text.isEmpty()) {
            addMessage("user", text);
            messageInput.setText("");
            
            // رد بسيط
            if (text.contains("مرحبا") || text.contains("هلا")) {
                addMessage("bot", "أهلاً بك! 📱 أرسل لي الصور والفيديوهات لحمايتها");
            } else if (text.contains("شكرا")) {
                addMessage("bot", "عفواً! 😊 ملفاتك بأمان");
            }
        }
    }

    private void addMessage(String sender, String content) {
        messages.add(new ChatMessage(sender, content, "text"));
        chatAdapter.notifyItemInserted(messages.size() - 1);
        chatRecyclerView.scrollToPosition(messages.size() - 1);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == PICK_FILE && resultCode == RESULT_OK && data != null) {
            Uri uri = data.getData();
            if (uri != null) {
                processFile(uri);
            }
        }
    }

    private void processFile(Uri uri) {
        try {
            String fileName = getFileName(uri);
            String mimeType = getContentResolver().getType(uri);
            
            // نسخ الملف للتخزين المؤقت
            File tempFile = new File(getCacheDir(), fileName);
            InputStream is = getContentResolver().openInputStream(uri);
            FileOutputStream fos = new FileOutputStream(tempFile);
            byte[] buffer = new byte[1024];
            int read;
            while ((read = is.read(buffer)) != -1) {
                fos.write(buffer, 0, read);
            }
            fos.close();
            is.close();
            
            // تشفير ونقل الملف
            String vaultPath = FileUtils.encryptAndMoveFile(tempFile.getAbsolutePath());
            
            if (vaultPath != null) {
                VaultFile vaultFile = new VaultFile();
                vaultFile.setOriginalName(fileName);
                vaultFile.setEncryptedName(new File(vaultPath).getName());
                vaultFile.setOriginalPath(tempFile.getAbsolutePath());
                vaultFile.setVaultPath(vaultPath);
                vaultFile.setFileType(mimeType);
                vaultFile.setSize(tempFile.length());
                vaultFile.setVideo(FileUtils.isVideo(fileName));
                
                dbHelper.addFile(vaultFile);
                tempFile.delete();
                
                boolean isVideo = FileUtils.isVideo(fileName);
                String icon = isVideo ? "🎬" : "🖼️";
                addMessage("user", icon + " " + fileName + "\\nتم التشفير والحماية ✅");
                addMessage("bot", "تم حماية الملف بنجاح! 🔒\\nلا يمكن لأحد رؤيته الآن");
            }
        } catch (Exception e) {
            e.printStackTrace();
            addMessage("bot", "❌ حدث خطأ أثناء معالجة الملف");
        }
    }

    private String getFileName(Uri uri) {
        String name = "unknown";
        Cursor cursor = getContentResolver().query(uri, null, null, null, null);
        if (cursor != null && cursor.moveToFirst()) {
            int index = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
            if (index >= 0) name = cursor.getString(index);
            cursor.close();
        }
        return name;
    }

    private void loadVaultFiles() {
        List<VaultFile> files = dbHelper.getAllFiles();
        messages.clear();
        addMessage("bot", "📂 الملفات المحمية في خزنتك:");
        
        for (VaultFile file : files) {
            String icon = file.isVideo() ? "🎬" : "🖼️";
            addMessage("user", icon + " " + file.getOriginalName() + 
                       "\\nالحجم: " + formatSize(file.getSize()));
        }
        
        if (files.isEmpty()) {
            addMessage("bot", "لا توجد ملفات محمية بعد 📭\\nأرسل ملفاً للبدء");
        }
    }

    private String formatSize(long size) {
        if (size < 1024) return size + " B";
        if (size < 1024 * 1024) return String.format("%.1f KB", size / 1024.0);
        return String.format("%.1f MB", size / (1024.0 * 1024.0));
    }

    public static class ChatMessage {
        String sender, content, type;
        public ChatMessage(String sender, String content, String type) {
            this.sender = sender;
            this.content = content;
            this.type = type;
        }
        public String getSender() { return sender; }
        public String getContent() { return content; }
        public String getType() { return type; }
    }
}"""
    
    with open(f"{src}/ui/ChatActivity.java", "w") as f:
        f.write(chat_activity)
    
    # ChatAdapter.java
    chat_adapter = """package com.securevault.app.ui;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.recyclerview.widget.RecyclerView;
import com.securevault.app.R;
import java.util.List;

public class ChatAdapter extends RecyclerView.Adapter<ChatAdapter.ViewHolder> {
    private final android.content.Context context;
    private final List<ChatActivity.ChatMessage> messages;

    public ChatAdapter(android.content.Context context, List<ChatActivity.ChatMessage> messages) {
        this.context = context;
        this.messages = messages;
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.item_chat_message, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(ViewHolder holder, int position) {
        ChatActivity.ChatMessage msg = messages.get(position);
        holder.messageText.setText(msg.getContent());
        
        if ("bot".equals(msg.getSender())) {
            holder.messageText.setBackgroundResource(R.drawable.bubble_bot);
        } else {
            holder.messageText.setBackgroundResource(R.drawable.bubble_user);
        }
    }

    @Override
    public int getItemCount() {
        return messages.size();
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView messageText;
        ViewHolder(View itemView) {
            super(itemView);
            messageText = itemView.findViewById(R.id.message_text);
        }
    }
}"""
    
    with open(f"{src}/ui/ChatAdapter.java", "w") as f:
        f.write(chat_adapter)
    
    # MediaViewerActivity.java
    media_viewer = """package com.securevault.app.ui;

import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.securevault.app.R;
import com.securevault.app.utils.FileUtils;

public class MediaViewerActivity extends AppCompatActivity {
    private ImageView mediaView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_media_viewer);
        mediaView = findViewById(R.id.media_view);
        
        String vaultPath = getIntent().getStringExtra("vault_path");
        if (vaultPath != null) {
            try {
                byte[] decrypted = FileUtils.decryptFile(vaultPath);
                mediaView.setImageBitmap(BitmapFactory.decodeByteArray(decrypted, 0, decrypted.length));
            } catch (Exception e) {
                Toast.makeText(this, "خطأ في فك التشفير", Toast.LENGTH_SHORT).show();
                finish();
            }
        }
    }
}"""
    
    with open(f"{src}/ui/MediaViewerActivity.java", "w") as f:
        f.write(media_viewer)
    
    print("[+] Activity files created")
    
    # ========== LAYOUT FILES ==========
    
    res = f"{base_path}/app/src/main/res"
    
    # activity_lock_screen.xml
    lock_layout = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:orientation="vertical"
    android:background="#1B5E20"
    android:padding="32dp">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="🔒"
        android:textSize="64sp"
        android:layout_marginBottom="24dp"/>

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="SecureVault"
        android:textColor="#FFFFFF"
        android:textSize="28sp"
        android:textStyle="bold"
        android:layout_marginBottom="8dp"/>

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="أدخل رمز الحماية"
        android:textColor="#A5D6A7"
        android:textSize="16sp"
        android:layout_marginBottom="24dp"/>

    <com.google.android.material.textfield.TextInputLayout
        android:layout_width="280dp"
        android:layout_height="wrap_content"
        android:textColorHint="#FFFFFF"
        app:passwordToggleEnabled="true"
        style="@style/Widget.MaterialComponents.TextInputLayout.OutlinedBox">

        <com.google.android.material.textfield.TextInputEditText
            android:id="@+id/pin_input"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="الرمز السري"
            android:textColor="#FFFFFF"
            android:textColorHint="#A5D6A7"
            android:inputType="numberPassword"
            android:maxLength="4" />
    </com.google.android.material.textfield.TextInputLayout>

    <com.google.android.material.button.MaterialButton
        android:id="@+id/unlock_button"
        android:layout_width="280dp"
        android:layout_height="56dp"
        android:layout_marginTop="24dp"
        android:text="فتح الخزنة"
        android:textSize="16sp"
        app:cornerRadius="28dp"
        style="@style/Widget.MaterialComponents.Button" />

</LinearLayout>"""
    
    with open(f"{res}/layout/activity_lock_screen.xml", "w") as f:
        f.write(lock_layout)
    
    # activity_chat.xml
    chat_layout = """<?xml version="1.0" encoding="utf-8"?>
<androidx.coordinatorlayout.widget.CoordinatorLayout 
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#E5DDD5">

    <!-- شريط العنوان -->
    <com.google.android.material.appbar.AppBarLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:background="#075E54">

        <androidx.appcompat.widget.Toolbar
            android:layout_width="match_parent"
            android:layout_height="56dp"
            app:titleTextColor="#FFFFFF">
            
            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="🔒 SecureVault"
                android:textColor="#FFFFFF"
                android:textSize="18sp"
                android:textStyle="bold" />
                
        </androidx.appcompat.widget.Toolbar>
    </com.google.android.material.appbar.AppBarLayout>

    <!-- قائمة المحادثة -->
    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/chat_recycler"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:layout_marginTop="56dp"
        android:layout_marginBottom="64dp"
        android:padding="8dp"
        android:clipToPadding="false" />

    <!-- شريط الإدخال السفلي -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_gravity="bottom"
        android:background="#F0F0F0"
        android:orientation="horizontal"
        android:padding="8dp"
        android:elevation="8dp">

        <ImageButton
            android:id="@+id/attach_button"
            android:layout_width="40dp"
            android:layout_height="40dp"
            android:src="@android:drawable/ic_menu_attachment"
            android:background="?attr/selectableItemBackgroundBorderless"
            android:contentDescription="إرفاق" />

        <EditText
            android:id="@+id/message_input"
            android:layout_width="0dp"
            android:layout_height="40dp"
            android:layout_weight="1"
            android:layout_marginHorizontal="8dp"
            android:background="@drawable/edittext_bg"
            android:hint="اكتب رسالة أو أرفق ملف..."
            android:paddingHorizontal="16dp"
            android:maxLines="3" />

        <ImageButton
            android:id="@+id/send_button"
            android:layout_width="40dp"
            android:layout_height="40dp"
            android:src="@android:drawable/ic_menu_send"
            android:background="?attr/selectableItemBackgroundBorderless"
            android:contentDescription="إرسال" />
    </LinearLayout>

    <!-- زر المعرض العائم -->
    <com.google.android.material.floatingactionbutton.FloatingActionButton
        android:id="@+id/fab_gallery"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="end|bottom"
        android:layout_margin="16dp"
        android:layout_marginBottom="72dp"
        android:src="@android:drawable/ic_menu_gallery"
        app:backgroundTint="#25D366" />

</androidx.coordinatorlayout.widget.CoordinatorLayout>"""
    
    with open(f"{res}/layout/activity_chat.xml", "w") as f:
        f.write(chat_layout)
    
    # item_chat_message.xml
    item_chat = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:padding="4dp"
    android:orientation="vertical">

    <TextView
        android:id="@+id/message_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:maxWidth="280dp"
        android:padding="12dp"
        android:textSize="15sp" />
</LinearLayout>"""
    
    with open(f"{res}/layout/item_chat_message.xml", "w") as f:
        f.write(item_chat)
    
    # activity_media_viewer.xml
    media_layout = """<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#000000">

    <ImageView
        android:id="@+id/media_view"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:scaleType="fitCenter" />
</FrameLayout>"""
    
    with open(f"{res}/layout/activity_media_viewer.xml", "w") as f:
        f.write(media_layout)
    
    # ========== DRAWABLE FILES ==========
    
    # bubble_bot.xml
    bubble_bot = """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <solid android:color="#FFFFFF" />
    <corners android:radius="12dp" 
        android:bottomLeftRadius="2dp"/>
    <padding android:left="8dp" android:right="8dp" 
        android:top="4dp" android:bottom="4dp" />
</shape>"""
    
    with open(f"{res}/drawable/bubble_bot.xml", "w") as f:
        f.write(bubble_bot)
    
    # bubble_user.xml
    bubble_user = """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <solid android:color="#DCF8C6" />
    <corners android:radius="12dp" 
        android:bottomRightRadius="2dp"/>
    <padding android:left="8dp" android:right="8dp" 
        android:top="4dp" android:bottom="4dp" />
</shape>"""
    
    with open(f"{res}/drawable/bubble_user.xml", "w") as f:
        f.write(bubble_user)
    
    # edittext_bg.xml
    edit_bg = """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <solid android:color="#FFFFFF" />
    <corners android:radius="20dp" />
    <stroke android:width="1dp" android:color="#E0E0E0" />
</shape>"""
    
    with open(f"{res}/drawable/edittext_bg.xml", "w") as f:
        f.write(edit_bg)
    
    # ic_launcher.xml
    ic_launcher = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>"""
    
    with open(f"{res}/mipmap-hdpi/ic_launcher.xml", "w") as f:
        f.write(ic_launcher)
    
    ic_fg = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M54,30 L54,78 M38,54 L70,54"
        android:strokeWidth="4"
        android:strokeColor="#FFFFFF"/>
</vector>"""
    
    with open(f"{res}/drawable/ic_launcher_foreground.xml", "w") as f:
        f.write(ic_fg)
    
    # ========== VALUES FILES ==========
    
    colors_xml = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="primary">#075E54</color>
    <color name="primary_dark">#054C44</color>
    <color name="accent">#25D366</color>
    <color name="white">#FFFFFF</color>
    <color name="black">#000000</color>
    <color name="ic_launcher_background">#1B5E20</color>
</resources>"""
    
    with open(f"{res}/values/colors.xml", "w") as f:
        f.write(colors_xml)
    
    themes_xml = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.SecureVault" parent="Theme.MaterialComponents.Light.NoActionBar">
        <item name="colorPrimary">@color/primary</item>
        <item name="colorPrimaryDark">@color/primary_dark</item>
        <item name="colorAccent">@color/accent</item>
    </style>
    
    <style name="Theme.SecureVault.Fullscreen" parent="Theme.SecureVault">
        <item name="android:windowFullscreen">true</item>
        <item name="android:windowContentOverlay">@null</item>
    </style>
</resources>"""
    
    with open(f"{res}/values/themes.xml", "w") as f:
        f.write(themes_xml)
    
    strings_xml = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">SecureVault</string>
</resources>"""
    
    with open(f"{res}/values/strings.xml", "w") as f:
        f.write(strings_xml)
    
    print("[+] Resource files created")
    
    # ========== GITHUB ACTIONS ==========
    
    # main.yml
    main_yml = """name: Build APK

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    name: Build Debug APK
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
        
    - name: Cache Gradle
      uses: actions/cache@v4
      with:
        path: |
          ~/.gradle/caches
          ~/.gradle/wrapper
        key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
        restore-keys: |
          ${{ runner.os }}-gradle-
          
    - name: Grant execute permission for gradlew
      run: chmod +x gradlew
      
    - name: Build Debug APK
      run: ./gradlew assembleDebug
      
    - name: Upload APK Artifact
      uses: actions/upload-artifact@v4
      with:
        name: SecureVault-Debug
        path: app/build/outputs/apk/debug/app-debug.apk
        
    - name: Build Release APK (if keystore available)
      if: false
      run: ./gradlew assembleRelease
      env:
        KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
        KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
        KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}"""
    
    with open(f"{base_path}/.github/workflows/main.yml", "w") as f:
        f.write(main_yml)
    
    # build.yml
    build_yml = """name: Build and Release APK

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:
    inputs:
      version:
        description: 'Version name'
        required: true
        default: '1.0'

jobs:
  build:
    name: Build Release APK
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
        
    - name: Cache Gradle
      uses: actions/cache@v4
      with:
        path: |
          ~/.gradle/caches
          ~/.gradle/wrapper
        key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
        restore-keys: |
          ${{ runner.os }}-gradle-
          
    - name: Build Debug APK
      run: ./gradlew assembleDebug
      
    - name: Upload Debug APK
      uses: actions/upload-artifact@v4
      with:
        name: SecureVault-Debug-${{ github.sha }}
        path: app/build/outputs/apk/debug/app-debug.apk
        
    - name: Create Release
      if: startsWith(github.ref, 'refs/tags/')
      uses: softprops/action-gh-release@v1
      with:
        files: app/build/outputs/apk/debug/app-debug.apk
        name: SecureVault ${{ github.ref_name }}
        body: |
          ## SecureVault APK
          
          تطبيق الخزنة الآمنة لتشفير وحماية الصور والفيديوهات
          
          ### المميزات:
          - واجهة محادثة سهلة الاستخدام
          - تشفير AES-256
          - إخفاء الملفات من المعرض
          - حماية بكلمة مرور
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}"""
    
    with open(f"{base_path}/.github/workflows/build.yml", "w") as f:
        f.write(build_yml)
    
    print("[+] GitHub Actions workflows created")
    
    # ========== GRADLE WRAPPER ==========
    
    gradle_wrapper_props = """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.5-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists"""
    
    with open(f"{base_path}/gradle/wrapper/gradle-wrapper.properties", "w") as f:
        f.write(gradle_wrapper_props)
    
    # gradlew script (shell)
    gradlew = """#!/bin/sh
#
# Gradle start up script
#
# This is a generated file.

# Attempt to set APP_HOME
PRG="$0"
while [ -h "$PRG" ] ; do
    ls=$(ls -ld "$PRG")
    link=$(expr "$ls" : '.*-> \\(.*\\)$')
    if expr "$link" : '/.*' > /dev/null; then
        PRG="$link"
    else
        PRG=$(dirname "$PRG")/"$link"
    fi
done
SAVED="$(pwd)"
cd "$(dirname \"$PRG\")/" >/dev/null
APP_HOME="$(pwd -P)"
cd "$SAVED" >/dev/null

APP_NAME="Gradle"
APP_BASE_NAME=$(basename "$0")

DEFAULT_JVM_OPTS='"-Xmx64m" "-Xms64m"'

MAX_FD="maximum"

warn () {
    echo "$*"
} >&2

die () {
    echo
    echo "$*"
    echo
    exit 1
} >&2

OS_NAME=$(uname)
case "$OS_NAME" in
    Darwin* ) darwin=true;;
    MINGW* ) msys=true;;
    CYGWIN* ) cygwin=true;;
esac

CLASSPATH=$APP_HOME/gradle/wrapper/gradle-wrapper.jar

if [ -n "$JAVA_HOME" ] ; then
    JAVACMD="$JAVA_HOME/bin/java"
else
    JAVACMD="java"
fi

exec "$JAVACMD" $DEFAULT_JVM_OPTS -classpath "$CLASSPATH" org.gradle.wrapper.GradleWrapperMain "$@"
"""
    
    with open(f"{base_path}/gradlew", "w") as f:
        f.write(gradlew)
    
    os.chmod(f"{base_path}/gradlew", 0o755)
    
    # gradlew.bat
    gradlew_bat = """@if "%DEBUG%"=="" @echo off
@rem Gradle startup script for Windows
@rem This is a generated file.

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%"=="" set DIRNAME=.
@rem This is normally unused
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%

@rem Resolve any "." and ".." in APP_HOME to make it shorter.
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi

set DEFAULT_JVM_OPTS="-Xmx64m" "-Xms64m"

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if %ERRORLEVEL% equ 0 goto execute

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto execute

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\\gradle\\wrapper\\gradle-wrapper.jar

@rem Execute Gradle
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %GRADLE_OPTS% "-Dorg.gradle.appname=%APP_BASE_NAME%" -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*

:end
@rem End local scope for the variables with windows NT shell
if %OS%==Windows_NT endlocal

:omega
"""
    
    with open(f"{base_path}/gradlew.bat", "w") as f:
        f.write(gradlew_bat)
    
    print("[+] Gradle wrapper created")
    
    # ========== SUMMARY ==========
    print("\\n" + "="*60)
    print("[✓] تم إنشاء المشروع بنجاح في مجلد gtheb/")
    print("="*60)
    print("\\nبنية المشروع:")
    print("  📁 gtheb/")
    print("  ├── 📁 app/")
    print("  │   ├── 📁 src/main/java/com/securevault/app/")
    print("  │   │   ├── MainApplication.java")
    print("  │   │   ├── 📁 crypto/CryptoManager.java")
    print("  │   │   ├── 📁 database/DatabaseHelper.java")
    print("  │   │   ├── 📁 models/VaultFile.java")
    print("  │   │   ├── 📁 utils/FileUtils.java")
    print("  │   │   └── 📁 ui/")
    print("  │   │       ├── LockScreenActivity.java")
    print("  │   │       ├── ChatActivity.java")
    print("  │   │       ├── ChatAdapter.java")
    print("  │   │       └── MediaViewerActivity.java")
    print("  │   └── 📁 res/layout/ (واجهات XML)")
    print("  ├── 📁 .github/workflows/")
    print("  │   ├── main.yml")
    print("  │   └── build.yml")
    print("  ├── build.gradle")
    print("  ├── settings.gradle")
    print("  └── gradlew")
    print("\\nللاستخدام:")
    print("  1. افتح Android Studio")
    print("  2. اختر 'Open Project'")
    print("  3. حدد مجلد gtheb/")
    print("  4. انتظر تثبيت Gradle")
    print("  5. شغل على هاتفك أو محاكي")
    print("\\nالرمز السري: 1234")
    print("="*60)

if __name__ == "__main__":
    create_project_structure()
