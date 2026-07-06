#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                                                            ║
║  💖  FILE VAULT - Pink Rose Secret File Manager  💖       ║
║     WhatsApp-Style Chat UI                                 ║
║     AES-256 Encryption for External Storage                ║
║     Password: 1234                                         ║
║     Files appear CORRUPTED outside the app                 ║
║                                                            ║
║  🔥  Built for GitHub Actions APK Generation               ║
║                                                            ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import json
import urllib.request

# ═══════════════════════════════════════════════════════════
# 💖 CONFIGURATION
# ═══════════════════════════════════════════════════════════

PROJECT_NAME = "FileVault"
PACKAGE_NAME = "com.zhare.filevault"
APP_PASSWORD = "1234"
ROOT_DIR = os.path.join(os.getcwd(), PROJECT_NAME)

TOTAL_FILES = 0
TOTAL_LINES = 0

# ═══════════════════════════════════════════════════════════
# 💖 UTILITIES
# ═══════════════════════════════════════════════════════════

def write_file(filepath, content):
    global TOTAL_FILES, TOTAL_LINES
    full_path = os.path.join(ROOT_DIR, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    lines = content.count('\n') + 1
    TOTAL_FILES += 1
    TOTAL_LINES += lines
    print(f"  ✅ {filepath} ({lines} lines)")

def section(title):
    print(f"\n{'='*60}")
    print(f"  💖 {title}")
    print(f"{'='*60}")

# ═══════════════════════════════════════════════════════════
# 💖 BUILD ALL
# ═══════════════════════════════════════════════════════════

def build_all():
    section("ROOT BUILD FILES")

    write_file("settings.gradle", f"""rootProject.name = "{PROJECT_NAME}"
include ':app'
""")

    write_file("build.gradle", """buildscript {
    repositories { google(); mavenCentral() }
    dependencies { classpath 'com.android.tools.build:gradle:8.2.0' }
}
allprojects { repositories { google(); mavenCentral() } }
""")

    write_file("gradle.properties", """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true
""")

    write_file(".gitignore", """*.iml
.gradle
.idea
/build
*.apk
*.jks
""")

    # Gradle wrapper
    write_file("gradlew", """#!/bin/sh
APP_HOME="`pwd -P`"
CLASSPATH=$APP_HOME/gradle/wrapper/gradle-wrapper.jar
exec java -classpath "$CLASSPATH" org.gradle.wrapper.GradleWrapperMain "$@"
""")
    os.chmod(os.path.join(ROOT_DIR, "gradlew"), 0o755)

    write_file("gradlew.bat", """@echo off
set CLASSPATH=%~dp0\\gradle\\wrapper\\gradle-wrapper.jar
java -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*
""")

    write_file("gradle/wrapper/gradle-wrapper.properties", """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.2-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""")

    print("  📥 Downloading gradle-wrapper.jar...")
    try:
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/gradle/gradle/v8.2.0/gradle/wrapper/gradle-wrapper.jar",
            os.path.join(ROOT_DIR, "gradle/wrapper/gradle-wrapper.jar")
        )
        TOTAL_FILES += 1
        print("  ✅ gradle-wrapper.jar downloaded")
    except Exception as e:
        print(f"  ⚠️ Could not download jar: {e}")

    section("APP BUILD FILE")

    write_file("app/build.gradle", f"""plugins {{ id 'com.android.application' }}

android {{
    namespace '{PACKAGE_NAME}'
    compileSdk 34

    defaultConfig {{
        applicationId '{PACKAGE_NAME}'
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0.0"
    }}

    buildTypes {{
        debug {{ debuggable true }}
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }}
    }}

    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.recyclerview:recyclerview:1.3.2'
    implementation 'androidx.swiperefreshlayout:swiperefreshlayout:1.1.0'
    implementation 'androidx.documentfile:documentfile:1.0.1'
}}
""")

    write_file("app/proguard-rules.pro", """-keep class com.zhare.filevault.** { *; }
-keep class javax.crypto.** { *; }
-keep class java.security.** { *; }
""")

    section("ANDROID MANIFEST")

    write_file("app/src/main/AndroidManifest.xml", f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <!-- External Storage Permissions -->
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
    <uses-permission android:name="android.permission.READ_MEDIA_VIDEO" />
    <uses-permission android:name="android.permission.READ_MEDIA_AUDIO" />
    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="File Vault 💖"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.FileVault"
        android:requestLegacyExternalStorage="true"
        tools:targetApi="34">

        <!-- Lock Screen (LAUNCHER) -->
        <activity
            android:name=".ui.LockScreenActivity"
            android:exported="true"
            android:screenOrientation="portrait"
            android:theme="@style/Theme.FileVault">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <!-- Chat Screen (WhatsApp-Style) -->
        <activity
            android:name=".ui.ChatScreenActivity"
            android:screenOrientation="portrait"
            android:theme="@style/Theme.FileVault" />

        <!-- File Manager Screen -->
        <activity
            android:name=".ui.FileManagerActivity"
            android:screenOrientation="portrait"
            android:theme="@style/Theme.FileVault" />

    </application>
</manifest>
""")

    section("JAVA - CRYPTO")

    write_file("app/src/main/java/com/zhare/filevault/crypto/AESHelper.java", f"""package com.zhare.filevault.crypto;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.security.MessageDigest;
import java.security.SecureRandom;

/**
 * 💖 AES-256 Encryption/Decryption
 * Uses password-based key derivation (SHA-256)
 * Files encrypted with this CANNOT be opened outside the app
 */
public class AESHelper {{

    private static final String ALGORITHM = "AES";
    private static final String TRANSFORMATION = "AES/ECB/PKCS5Padding";
    private static final String SECRET = "{APP_PASSWORD}";

    private static SecretKeySpec getSecretKey() throws Exception {{
        MessageDigest sha = MessageDigest.getInstance("SHA-256");
        byte[] key = sha.digest(SECRET.getBytes("UTF-8"));
        return new SecretKeySpec(key, ALGORITHM);
    }}

    /**
     * Encrypt byte array
     */
    public static byte[] encrypt(byte[] data) throws Exception {{
        Cipher cipher = Cipher.getInstance(TRANSFORMATION);
        cipher.init(Cipher.ENCRYPT_MODE, getSecretKey());
        return cipher.doFinal(data);
    }}

    /**
     * Decrypt byte array
     */
    public static byte[] decrypt(byte[] data) throws Exception {{
        Cipher cipher = Cipher.getInstance(TRANSFORMATION);
        cipher.init(Cipher.DECRYPT_MODE, getSecretKey());
        return cipher.doFinal(data);
    }}

    /**
     * Encrypt file data (returns corrupted-looking bytes)
     */
    public static byte[] encryptFile(byte[] fileData) throws Exception {{
        return encrypt(fileData);
    }}

    /**
     * Decrypt file data (returns original bytes)
     */
    public static byte[] decryptFile(byte[] encryptedData) throws Exception {{
        return decrypt(encryptedData);
    }}

    /**
     * Quick check if password is correct
     */
    public static boolean verifyPassword(String password) {{
        return SECRET.equals(password);
    }}
}}
""")

    section("JAVA - MODELS")

    write_file("app/src/main/java/com/zhare/filevault/models/FileItem.java", """package com.zhare.filevault.models;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/**
 * 💖 File Model
 */
public class FileItem {
    private String name, path, mimeType;
    private long size, lastModified;
    private boolean isDirectory, isEncrypted;

    public FileItem(File file) {
        this.name = file.getName();
        this.path = file.getAbsolutePath();
        this.size = file.length();
        this.isDirectory = file.isDirectory();
        this.isEncrypted = name.toLowerCase().endsWith(".vault");
        this.lastModified = file.lastModified();
        this.mimeType = detectType();
    }

    private String detectType() {
        if (isDirectory) return "📁 مجلد";
        String n = name.toLowerCase();
        if (n.matches(".*\\.(jpg|jpeg|png|gif|bmp|webp)$")) return "🖼️ صورة";
        if (n.matches(".*\\.(mp4|mkv|avi|mov|3gp)$")) return "🎬 فيديو";
        if (n.matches(".*\\.(mp3|wav|ogg|m4a|aac)$")) return "🎵 صوت";
        if (n.matches(".*\\.(pdf)$")) return "📄 PDF";
        if (n.matches(".*\\.(doc|docx)$")) return "📝 وورد";
        if (n.matches(".*\\.(apk)$")) return "📦 APK";
        if (n.matches(".*\\.(zip|rar|7z)$")) return "🗜️ مضغوط";
        if (n.endsWith(".vault")) return "🔒 مشفر";
        return "📄 ملف";
    }

    // Getters
    public String getName() { return name; }
    public String getPath() { return path; }
    public long getSize() { return size; }
    public boolean isDirectory() { return isDirectory; }
    public boolean isEncrypted() { return isEncrypted; }
    public String getMimeType() { return mimeType; }

    public String getSizeFormatted() {
        if (isDirectory) return "";
        if (size < 1024) return size + " B";
        if (size < 1024 * 1024) return String.format(Locale.US, "%.1f KB", size / 1024.0);
        if (size < 1024 * 1024 * 1024) return String.format(Locale.US, "%.1f MB", size / (1024.0 * 1024));
        return String.format(Locale.US, "%.1f GB", size / (1024.0 * 1024 * 1024));
    }

    public String getDateFormatted() {
        return new SimpleDateFormat("yyyy/MM/dd HH:mm", Locale.getDefault())
            .format(new Date(lastModified));
    }
}
""")

    write_file("app/src/main/java/com/zhare/filevault/models/ChatItem.java", """package com.zhare.filevault.models;

/**
 * 💖 Chat Message Model (WhatsApp-Style)
 */
public class ChatItem {
    private String message;
    private String time;
    private boolean isSent; // true = sent by user, false = received (system)

    public ChatItem(String message, boolean isSent) {
        this.message = message;
        this.isSent = isSent;
        this.time = java.text.SimpleDateFormat.getTimeInstance(
            java.text.DateFormat.SHORT, java.util.Locale.getDefault()
        ).format(new java.util.Date());
    }

    public String getMessage() { return message; }
    public String getTime() { return time; }
    public boolean isSent() { return isSent; }
}
""")

    section("JAVA - ADAPTERS")

    write_file("app/src/main/java/com/zhare/filevault/ui/FileAdapter.java", """package com.zhare.filevault.ui;

import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.zhare.filevault.R;
import com.zhare.filevault.models.FileItem;
import java.util.ArrayList;
import java.util.List;

/**
 * 💖 File List Adapter (RecyclerView)
 */
public class FileAdapter extends RecyclerView.Adapter<FileAdapter.ViewHolder> {

    private List<FileItem> files = new ArrayList<>();
    private OnFileClickListener listener;

    public interface OnFileClickListener {
        void onFileClick(FileItem file, int position);
        void onFileLongClick(FileItem file, int position);
    }

    public FileAdapter(OnFileClickListener listener) {
        this.listener = listener;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
            .inflate(R.layout.item_file, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        FileItem file = files.get(position);

        // Icon
        if (file.isDirectory()) {
            holder.tvIcon.setText("📁");
        } else if (file.isEncrypted()) {
            holder.tvIcon.setText("🔒");
        } else {
            holder.tvIcon.setText("📄");
        }

        // Name
        holder.tvName.setText(file.getName());
        
        // Encrypted files in PINK
        if (file.isEncrypted()) {
            holder.tvName.setTextColor(Color.parseColor("#EC4899"));
        } else {
            holder.tvName.setTextColor(Color.WHITE);
        }

        // Info
        String info = file.getDateFormatted();
        if (!file.getSizeFormatted().isEmpty()) {
            info += " • " + file.getSizeFormatted();
        }
        info += " • " + file.getMimeType();
        holder.tvInfo.setText(info);

        // Click listeners
        holder.itemView.setOnClickListener(v -> {
            if (listener != null) listener.onFileClick(file, position);
        });

        holder.itemView.setOnLongClickListener(v -> {
            if (listener != null) listener.onFileLongClick(file, position);
            return true;
        });
    }

    @Override
    public int getItemCount() {
        return files.size();
    }

    public void updateList(List<FileItem> newFiles) {
        this.files = newFiles;
        notifyDataSetChanged();
    }

    public FileItem getItem(int position) {
        return files.get(position);
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvIcon, tvName, tvInfo;

        ViewHolder(View itemView) {
            super(itemView);
            tvIcon = itemView.findViewById(R.id.tvIcon);
            tvName = itemView.findViewById(R.id.tvName);
            tvInfo = itemView.findViewById(R.id.tvInfo);
        }
    }
}
""")

    write_file("app/src/main/java/com/zhare/filevault/ui/ChatAdapter.java", """package com.zhare.filevault.ui;

import android.graphics.Color;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.zhare.filevault.R;
import com.zhare.filevault.models.ChatItem;
import java.util.ArrayList;
import java.util.List;

/**
 * 💖 WhatsApp-Style Chat Adapter
 */
public class ChatAdapter extends RecyclerView.Adapter<ChatAdapter.ViewHolder> {

    private List<ChatItem> messages = new ArrayList<>();

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
            .inflate(R.layout.item_chat, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        ChatItem msg = messages.get(position);

        holder.tvMessage.setText(msg.getMessage());
        holder.tvTime.setText(msg.getTime());

        FrameLayout.LayoutParams params = (FrameLayout.LayoutParams) holder.bubble.getLayoutParams();

        if (msg.isSent()) {
            // User message (Right side - Pink)
            holder.bubble.setBackgroundResource(R.drawable.bg_chat_sent);
            holder.tvMessage.setTextColor(Color.WHITE);
            holder.tvTime.setTextColor(Color.parseColor("#CCFFFFFF"));
            params.gravity = Gravity.END;
        } else {
            // System message (Left side - Dark)
            holder.bubble.setBackgroundResource(R.drawable.bg_chat_received);
            holder.tvMessage.setTextColor(Color.WHITE);
            holder.tvTime.setTextColor(Color.parseColor("#99FFFFFF"));
            params.gravity = Gravity.START;
        }

        holder.bubble.setLayoutParams(params);
    }

    @Override
    public int getItemCount() {
        return messages.size();
    }

    public void addMessage(ChatItem msg) {
        messages.add(msg);
        notifyItemInserted(messages.size() - 1);
    }

    public void setMessages(List<ChatItem> msgs) {
        this.messages = msgs;
        notifyDataSetChanged();
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        FrameLayout bubble;
        TextView tvMessage, tvTime;

        ViewHolder(View itemView) {
            super(itemView);
            bubble = itemView.findViewById(R.id.bubble);
            tvMessage = itemView.findViewById(R.id.tvMessage);
            tvTime = itemView.findViewById(R.id.tvTime);
        }
    }
}
""")

    section("JAVA - ACTIVITIES")

    write_file(f"app/src/main/java/com/zhare/filevault/ui/LockScreenActivity.java", f"""package com.zhare.filevault.ui;

import android.animation.ArgbEvaluator;
import android.animation.ValueAnimator;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.zhare.filevault.R;
import com.zhare.filevault.crypto.AESHelper;

/**
 * 💖 Lock Screen - First Activity
 * Requires password 1234 to access the app
 */
public class LockScreenActivity extends AppCompatActivity {{

    private static final String PREF_NAME = "FileVaultPrefs";
    private static final String KEY_UNLOCKED = "is_unlocked";
    private static final String CORRECT_PASSWORD = "{APP_PASSWORD}";

    private EditText etPassword;
    private Button btnUnlock;
    private TextView tvTitle;
    private SharedPreferences prefs;
    private int failedAttempts = 0;
    private Handler handler = new Handler();

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_lock);

        // Pink status bar
        getWindow().setStatusBarColor(Color.parseColor("#EC4899"));
        getWindow().setNavigationBarColor(Color.parseColor("#0D0610"));

        prefs = getSharedPreferences(PREF_NAME, MODE_PRIVATE);

        // Auto-login if already unlocked
        if (prefs.getBoolean(KEY_UNLOCKED, false) && 
            !getIntent().getBooleanExtra("force_lock", false)) {{
            openApp();
            return;
        }}

        initViews();
        setupAnimation();
    }}

    private void initViews() {{
        tvTitle = findViewById(R.id.tvTitle);
        etPassword = findViewById(R.id.etPassword);
        btnUnlock = findViewById(R.id.btnUnlock);

        etPassword.requestFocus();

        btnUnlock.setOnClickListener(v -> verifyPassword());

        // Enter key
        etPassword.setOnEditorActionListener((v, actionId, event) -> {{
            verifyPassword();
            return true;
        }});
    }}

    private void setupAnimation() {{
        // Pulsing title color
        ValueAnimator colorAnim = ValueAnimator.ofObject(
            new ArgbEvaluator(),
            Color.parseColor("#EC4899"),
            Color.parseColor("#F472B6"),
            Color.parseColor("#EC4899")
        );
        colorAnim.setDuration(2000);
        colorAnim.setRepeatCount(ValueAnimator.INFINITE);
        colorAnim.setRepeatMode(ValueAnimator.REVERSE);
        colorAnim.addUpdateListener(anim -> 
            tvTitle.setTextColor((int) anim.getAnimatedValue()));
        colorAnim.start();
    }}

    private void verifyPassword() {{
        String input = etPassword.getText().toString().trim();

        if (input.isEmpty()) {{
            etPassword.setError("❌ أدخل رمز الدخول!");
            shakeView();
            return;
        }}

        if (AESHelper.verifyPassword(input)) {{
            // SUCCESS
            prefs.edit().putBoolean(KEY_UNLOCKED, true).apply();
            Toast.makeText(this, "✅ مرحباً بك! 💖", Toast.LENGTH_SHORT).show();

            handler.postDelayed(this::openApp, 400);
        }} else {{
            // FAILED
            failedAttempts++;
            etPassword.setText("");
            etPassword.setError("❌ رمز خطأ! (" + failedAttempts + "/3)");
            shakeView();

            if (failedAttempts >= 3) {{
                lockApp();
            }}
        }}
    }}

    private void lockApp() {{
        btnUnlock.setEnabled(false);
        etPassword.setEnabled(false);
        btnUnlock.setText("⏳ انتظر 30 ثانية...");

        Toast.makeText(this, "🔒 تم القفل لمدة 30 ثانية", Toast.LENGTH_LONG).show();

        handler.postDelayed(() -> {{
            btnUnlock.setEnabled(true);
            etPassword.setEnabled(true);
            btnUnlock.setText("🔓 فتح");
            failedAttempts = 0;
        }}, 30000);
    }}

    private void shakeView() {{
        Animation shake = AnimationUtils.loadAnimation(this, R.anim.shake);
        findViewById(R.id.lockContainer).startAnimation(shake);
    }}

    private void openApp() {{
        startActivity(new Intent(this, ChatScreenActivity.class));
        finish();
        overridePendingTransition(R.anim.slide_in_right, R.anim.slide_out_left);
    }}

    @Override
    protected void onPause() {{
        super.onPause();
        // Re-lock when app goes to background
        prefs.edit().putBoolean(KEY_UNLOCKED, false).apply();
    }}

    @Override
    public void onBackPressed() {{
        super.onBackPressed();
        finishAffinity();
    }}
}}
""")

    write_file("app/src/main/java/com/zhare/filevault/ui/ChatScreenActivity.java", """package com.zhare.filevault.ui;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Environment;
import android.provider.Settings;
import android.net.Uri;
import android.os.Build;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.zhare.filevault.R;
import com.zhare.filevault.models.ChatItem;
import java.util.ArrayList;
import java.util.List;

/**
 * 💖 Main Chat Screen (WhatsApp-Style)
 * The user interacts with the app through chat commands
 */
public class ChatScreenActivity extends AppCompatActivity {

    private RecyclerView rvChat;
    private ChatAdapter chatAdapter;
    private EditText etMessage;
    private ImageButton btnSend, btnFiles, btnLock;
    private TextView tvToolbarTitle;
    
    private List<ChatItem> messages = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);

        // Pink theme
        getWindow().setStatusBarColor(Color.parseColor("#EC4899"));
        getWindow().setNavigationBarColor(Color.parseColor("#0D0610"));

        initViews();
        setupChat();
        showWelcomeMessage();
    }

    private void initViews() {
        tvToolbarTitle = findViewById(R.id.tvToolbarTitle);
        rvChat = findViewById(R.id.rvChat);
        etMessage = findViewById(R.id.etMessage);
        btnSend = findViewById(R.id.btnSend);
        btnFiles = findViewById(R.id.btnFiles);
        btnLock = findViewById(R.id.btnLock);

        tvToolbarTitle.setText("💖 File Vault");

        rvChat.setLayoutManager(new LinearLayoutManager(this));
        chatAdapter = new ChatAdapter();
        rvChat.setAdapter(chatAdapter);

        btnSend.setOnClickListener(v -> sendMessage());
        btnFiles.setOnClickListener(v -> openFileManager());
        btnLock.setOnClickListener(v -> lockApp());

        // Enter to send
        etMessage.setOnEditorActionListener((v, actionId, event) -> {
            sendMessage();
            return true;
        });
    }

    private void setupChat() {
        chatAdapter.setMessages(messages);
    }

    private void showWelcomeMessage() {
        addSystemMessage("💖 مرحباً بك في File Vault!");
        addSystemMessage("📁 ملفاتك محمية بتشفير AES-256");
        addSystemMessage("🔒 الملفات تظهر مشوهة خارج التطبيق");
        addSystemMessage("");
        addSystemMessage("📋 الأوامر المتاحة:");
        addSystemMessage("  📂 /files - فتح مدير الملفات");
        addSystemMessage("  🔒 /lock - قفل التطبيق");
        addSystemMessage("  ℹ️ /help - عرض المساعدة");
        addSystemMessage("  📁 /storage - عرض مساحة التخزين");
        addSystemMessage("");
        addSystemMessage("👇 اضغط على 📂 لفتح الملفات أو اكتب أمراً");
    }

    private void sendMessage() {
        String text = etMessage.getText().toString().trim();
        if (text.isEmpty()) return;

        // Add user message
        ChatItem userMsg = new ChatItem(text, true);
        messages.add(userMsg);
        chatAdapter.addMessage(userMsg);
        etMessage.setText("");

        // Process command
        processCommand(text);

        // Scroll to bottom
        rvChat.scrollToPosition(messages.size() - 1);
    }

    private void processCommand(String text) {
        String cmd = text.toLowerCase();

        if (cmd.equals("/files") || cmd.equals("📂") || cmd.contains("فتح الملفات")) {
            openFileManager();
        } else if (cmd.equals("/lock") || cmd.equals("🔒") || cmd.contains("قفل")) {
            lockApp();
        } else if (cmd.equals("/help") || cmd.equals("ℹ️") || cmd.contains("مساعدة")) {
            showHelp();
        } else if (cmd.equals("/storage") || cmd.contains("تخزين") || cmd.contains("مساحة")) {
            showStorageInfo();
        } else if (cmd.equals("/hi") || cmd.contains("مرحبا") || cmd.contains("هلا")) {
            addSystemMessage("💖 أهلاً بك! كيف أقدر أساعدك؟");
        } else if (!cmd.startsWith("/")) {
            addSystemMessage("❓ لم أفهم. اكتب /help للمساعدة");
        }
    }

    private void addSystemMessage(String msg) {
        ChatItem sysMsg = new ChatItem(msg, false);
        messages.add(sysMsg);
        chatAdapter.addMessage(sysMsg);
    }

    private void openFileManager() {
        // Check permission first
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            if (!Environment.isExternalStorageManager()) {
                AlertDialog.Builder builder = new AlertDialog.Builder(this);
                builder.setTitle("💖 صلاحية مطلوبة")
                    .setMessage("نحتاج صلاحية الوصول لجميع الملفات لعرضها وتشفيرها.")
                    .setPositiveButton("منح الصلاحية", (d, w) -> {
                        Intent intent = new Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION);
                        intent.setData(Uri.parse("package:" + getPackageName()));
                        startActivity(intent);
                    })
                    .setNegativeButton("إلغاء", null)
                    .show();
                return;
            }
        }
        startActivity(new Intent(this, FileManagerActivity.class));
    }

    private void lockApp() {
        getSharedPreferences("FileVaultPrefs", MODE_PRIVATE)
            .edit().putBoolean("is_unlocked", false).apply();
        Intent intent = new Intent(this, LockScreenActivity.class);
        intent.putExtra("force_lock", true);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(intent);
        finish();
    }

    private void showHelp() {
        addSystemMessage("📋 الأوامر:");
        addSystemMessage("  📂 /files - مدير الملفات");
        addSystemMessage("  🔒 /lock - قفل التطبيق");
        addSystemMessage("  📁 /storage - مساحة التخزين");
        addSystemMessage("  ℹ️ /help - هذه القائمة");
    }

    private void showStorageInfo() {
        File path = Environment.getExternalStorageDirectory();
        android.os.StatFs stat = new android.os.StatFs(path.getPath());
        long blockSize = stat.getBlockSizeLong();
        long totalBlocks = stat.getBlockCountLong();
        long availableBlocks = stat.getAvailableBlocksLong();
        long totalGB = (totalBlocks * blockSize) / (1024 * 1024 * 1024);
        long freeGB = (availableBlocks * blockSize) / (1024 * 1024 * 1024);
        addSystemMessage("📁 مساحة التخزين:");
        addSystemMessage("  💾 الإجمالي: " + totalGB + " GB");
        addSystemMessage("  🆓 المتاح: " + freeGB + " GB");
    }

    @Override
    public void onBackPressed() {
        // Minimize instead of exit
        moveTaskToBack(true);
    }
}
""")

    write_file("app/src/main/java/com/zhare/filevault/ui/FileManagerActivity.java", """package com.zhare.filevault.ui;

import android.Manifest;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.provider.Settings;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.google.android.material.appbar.MaterialToolbar;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.zhare.filevault.R;
import com.zhare.filevault.crypto.AESHelper;
import com.zhare.filevault.models.FileItem;
import java.io.*;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * 💖 File Manager Activity
 * Browse, Encrypt, Decrypt files on external storage
 * Files encrypted with .vault extension appear CORRUPTED outside the app
 */
public class FileManagerActivity extends AppCompatActivity {

    private RecyclerView rvFiles;
    private FileAdapter adapter;
    private TextView tvPath, tvEmpty;
    private MaterialToolbar toolbar;
    private FloatingActionButton fabLock;

    private List<FileItem> allFiles = new ArrayList<>();
    private String currentPath = "";
    private ExecutorService executor = Executors.newSingleThreadExecutor();
    private Handler mainHandler = new Handler(Looper.getMainLooper());

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_files);

        // Pink theme
        getWindow().setStatusBarColor(Color.parseColor("#EC4899"));
        getWindow().setNavigationBarColor(Color.parseColor("#0D0610"));

        initViews();
        setupListeners();
        
        // Load storage
        if (checkPermission()) {
            loadFiles(Environment.getExternalStorageDirectory().getAbsolutePath());
        }
    }

    private void initViews() {
        toolbar = findViewById(R.id.toolbar);
        rvFiles = findViewById(R.id.rvFiles);
        tvPath = findViewById(R.id.tvPath);
        tvEmpty = findViewById(R.id.tvEmpty);
        fabLock = findViewById(R.id.fabLock);

        toolbar.setTitle("📂 مدير الملفات");
        toolbar.setTitleTextColor(Color.WHITE);
        toolbar.setBackgroundColor(Color.parseColor("#EC4899"));
        toolbar.setNavigationOnClickListener(v -> goBack());
        setSupportActionBar(toolbar);

        rvFiles.setLayoutManager(new LinearLayoutManager(this));
        adapter = new FileAdapter(new FileAdapter.OnFileClickListener() {
            @Override
            public void onFileClick(FileItem file, int position) {
                if (file.isDirectory()) {
                    loadFiles(file.getPath());
                } else {
                    handleFileClick(file);
                }
            }

            @Override
            public void onFileLongClick(FileItem file, int position) {
                showFileOptions(file);
            }
        });
        rvFiles.setAdapter(adapter);
    }

    private void setupListeners() {
        fabLock.setOnClickListener(v -> {
            getSharedPreferences("FileVaultPrefs", MODE_PRIVATE)
                .edit().putBoolean("is_unlocked", false).apply();
            Intent intent = new Intent(this, LockScreenActivity.class);
            intent.putExtra("force_lock", true);
            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
            startActivity(intent);
            finish();
        });
    }

    private boolean checkPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            if (!Environment.isExternalStorageManager()) {
                AlertDialog.Builder builder = new AlertDialog.Builder(this);
                builder.setTitle("💖 صلاحية مطلوبة")
                    .setMessage("نحتاج صلاحية الوصول لجميع الملفات.")
                    .setPositiveButton("منح الصلاحية", (d, w) -> {
                        Intent intent = new Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION);
                        intent.setData(Uri.parse("package:" + getPackageName()));
                        startActivity(intent);
                    })
                    .setNegativeButton("رجوع", (d, w) -> finish())
                    .show();
                return false;
            }
        } else {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE)
                    != PackageManager.PERMISSION_GRANTED) {
                requestPermissions(new String[]{
                    Manifest.permission.READ_EXTERNAL_STORAGE,
                    Manifest.permission.WRITE_EXTERNAL_STORAGE
                }, 100);
                return false;
            }
        }
        return true;
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, 
                                            @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == 100 && grantResults.length > 0 
                && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            loadFiles(Environment.getExternalStorageDirectory().getAbsolutePath());
        }
    }

    private void loadFiles(String path) {
        tvEmpty.setVisibility(View.GONE);
        rvFiles.setVisibility(View.VISIBLE);

        executor.execute(() -> {
            File dir = new File(path);
            List<FileItem> files = new ArrayList<>();

            if (dir.exists() && dir.isDirectory()) {
                // Parent directory
                File parent = dir.getParentFile();
                if (parent != null && !isRoot(path)) {
                    files.add(new FileItem(parent) {
                        @Override
                        public String getName() { return "📁 .. (رجوع)"; }
                    });
                }

                File[] list = dir.listFiles();
                if (list != null) {
                    for (File f : list) {
                        if (!f.isHidden()) {
                            files.add(new FileItem(f));
                        }
                    }
                }

                // Sort
                files.sort((a, b) -> {
                    if (a.isDirectory() && !b.isDirectory()) return -1;
                    if (!a.isDirectory() && b.isDirectory()) return 1;
                    return a.getName().compareToIgnoreCase(b.getName());
                });
            }

            final List<FileItem> finalFiles = files;
            mainHandler.post(() -> {
                currentPath = path;
                allFiles = finalFiles;
                tvPath.setText("📂 " + path);
                adapter.updateList(finalFiles);
                rvFiles.scrollToPosition(0);
            });
        });
    }

    private boolean isRoot(String path) {
        String root = Environment.getExternalStorageDirectory().getAbsolutePath();
        return path.equals(root) || path.equals("/") || path.equals("/storage");
    }

    private void handleFileClick(FileItem file) {
        if (file.isEncrypted()) {
            // Ask to decrypt first
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("🔒 ملف مشفر")
                .setMessage("هذا الملف مشفر. هل تريد فك التشفير؟")
                .setPositiveButton("🔓 فك التشفير", (d, w) -> decryptFile(file))
                .setNegativeButton("إلغاء", null)
                .show();
        } else {
            // Try to open
            try {
                Intent intent = new Intent(Intent.ACTION_VIEW);
                String mime = "*/*";
                String name = file.getName().toLowerCase();
                if (name.matches(".*\\.(jpg|png|gif)$")) mime = "image/*";
                else if (name.matches(".*\\.(mp4|mkv)$")) mime = "video/*";
                else if (name.matches(".*\\.(mp3|wav)$")) mime = "audio/*";
                else if (name.endsWith(".pdf")) mime = "application/pdf";
                else if (name.endsWith(".apk")) mime = "application/vnd.android.package-archive";

                intent.setDataAndType(Uri.fromFile(new File(file.getPath())), mime);
                intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                startActivity(Intent.createChooser(intent, "فتح " + file.getName()));
            } catch (Exception e) {
                Toast.makeText(this, "❌ لا يمكن فتح الملف", Toast.LENGTH_SHORT).show();
            }
        }
    }

    private void showFileOptions(FileItem file) {
        String[] options;
        if (file.isEncrypted()) {
            options = new String[]{"🔓 فك التشفير", "📋 نسخ المسار", "ℹ️ معلومات", "🗑️ حذف"};
        } else if (file.isDirectory()) {
            options = new String[]{"📁 فتح", "📋 نسخ المسار", "ℹ️ معلومات"};
        } else {
            options = new String[]{"🔒 تشفير", "📋 نسخ المسار", "ℹ️ معلومات", "🗑️ حذف"};
        }

        new AlertDialog.Builder(this)
            .setTitle("💖 " + file.getName())
            .setItems(options, (dialog, which) -> {
                String chosen = options[which];
                if (chosen.contains("تشفير")) encryptFile(file);
                else if (chosen.contains("فك")) decryptFile(file);
                else if (chosen.contains("نسخ")) copyPath(file);
                else if (chosen.contains("معلومات")) showInfo(file);
                else if (chosen.contains("حذف")) deleteFile(file);
                else if (chosen.contains("فتح")) loadFiles(file.getPath());
            })
            .show();
    }

    private void encryptFile(FileItem file) {
        new AlertDialog.Builder(this)
            .setTitle("🔒 تأكيد التشفير")
            .setMessage("سيتم تشفير الملف:\n" + file.getName() + 
                "\n\n• سيضاف امتداد .vault\n• الملف الأصلي سيُحذف\n• لن يفتح خارج التطبيق")
            .setPositiveButton("تشفير", (d, w) -> {
                executor.execute(() -> {
                    try {
                        File f = new File(file.getPath());
                        byte[] data = new byte[(int) f.length()];
                        FileInputStream fis = new FileInputStream(f);
                        fis.read(data);
                        fis.close();

                        byte[] encrypted = AESHelper.encryptFile(data);
                        File outFile = new File(file.getPath() + ".vault");
                        FileOutputStream fos = new FileOutputStream(outFile);
                        fos.write(encrypted);
                        fos.close();

                        // Delete original
                        f.delete();

                        mainHandler.post(() -> {
                            Toast.makeText(this, "✅ تم التشفير: " + outFile.getName(), Toast.LENGTH_SHORT).show();
                            loadFiles(outFile.getParent());
                        });
                    } catch (Exception e) {
                        mainHandler.post(() -> Toast.makeText(this, "❌ فشل التشفير", Toast.LENGTH_SHORT).show());
                    }
                });
            })
            .setNegativeButton("إلغاء", null)
            .show();
    }

    private void decryptFile(FileItem file) {
        new AlertDialog.Builder(this)
            .setTitle("🔓 تأكيد فك التشفير")
            .setMessage("سيتم فك تشفير:\n" + file.getName() + "\n\n• سيتم استعادة الملف الأصلي\n• الملف المشفر سيُحذف")
            .setPositiveButton("فك التشفير", (d, w) -> {
                executor.execute(() -> {
                    try {
                        File f = new File(file.getPath());
                        byte[] data = new byte[(int) f.length()];
                        FileInputStream fis = new FileInputStream(f);
                        fis.read(data);
                        fis.close();

                        byte[] decrypted = AESHelper.decryptFile(data);
                        String origPath = file.getPath().replace(".vault", "");
                        File outFile = new File(origPath);
                        FileOutputStream fos = new FileOutputStream(outFile);
                        fos.write(decrypted);
                        fos.close();

                        f.delete();

                        mainHandler.post(() -> {
                            Toast.makeText(this, "✅ تم فك التشفير", Toast.LENGTH_SHORT).show();
                            loadFiles(outFile.getParent());
                        });
                    } catch (Exception e) {
                        mainHandler.post(() -> Toast.makeText(this, "❌ فشل - كلمة السر خطأ", Toast.LENGTH_SHORT).show());
                    }
                });
            })
            .setNegativeButton("إلغاء", null)
            .show();
    }

    private void copyPath(FileItem file) {
        ClipboardManager cm = (ClipboardManager) getSystemService(CLIPBOARD_SERVICE);
        cm.setPrimaryClip(ClipData.newPlainText("path", file.getPath()));
        Toast.makeText(this, "✅ تم نسخ المسار", Toast.LENGTH_SHORT).show();
    }

    private void showInfo(FileItem file) {
        String info = "📄 الاسم: " + file.getName() + "\n"
            + "📁 المسار: " + file.getPath() + "\n"
            + "📏 الحجم: " + file.getSizeFormatted() + "\n"
            + "📅 التاريخ: " + file.getDateFormatted() + "\n"
            + "🔒 مشفر: " + (file.isEncrypted() ? "نعم" : "لا") + "\n"
            + "📂 مجلد: " + (file.isDirectory() ? "نعم" : "لا");

        new AlertDialog.Builder(this)
            .setTitle("ℹ️ معلومات")
            .setMessage(info)
            .setPositiveButton("حسناً", null)
            .show();
    }

    private void deleteFile(FileItem file) {
        new AlertDialog.Builder(this)
            .setTitle("🗑️ تأكيد الحذف")
            .setMessage("هل أنت متأكد؟\n" + file.getName() + "\n\n⚠️ لا يمكن التراجع!")
            .setPositiveButton("حذف", (d, w) -> {
                File f = new File(file.getPath());
                boolean deleted = f.delete();
                if (deleted) {
                    Toast.makeText(this, "✅ تم الحذف", Toast.LENGTH_SHORT).show();
                    loadFiles(f.getParent());
                } else {
                    Toast.makeText(this, "❌ فشل", Toast.LENGTH_SHORT).show();
                }
            })
            .setNegativeButton("إلغاء", null)
            .show();
    }

    private void goBack() {
        if (currentPath != null && !currentPath.isEmpty()) {
            File current = new File(currentPath);
            File parent = current.getParentFile();
            if (parent != null && !isRoot(currentPath)) {
                loadFiles(parent.getAbsolutePath());
            } else {
                finish();
            }
        } else {
            finish();
        }
    }

    @Override
    public void onBackPressed() {
        goBack();
    }
}
""")

    section("XML LAYOUTS")

    write_file("app/src/main/res/layout/activity_lock.xml", """<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:fillViewport="true"
    android:background="#0D0610">

    <LinearLayout
        android:id="@+id/lockContainer"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:gravity="center"
        android:padding="32dp"
        android:layout_gravity="center">

        <!-- Logo -->
        <TextView
            android:layout_width="100dp"
            android:layout_height="100dp"
            android:text="💖"
            android:textSize="56sp"
            android:gravity="center"
            android:background="@drawable/bg_circle"
            android:layout_marginBottom="24dp" />

        <!-- Title -->
        <TextView
            android:id="@+id/tvTitle"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="File Vault"
            android:textSize="32sp"
            android:textColor="#EC4899"
            android:textStyle="bold"
            android:layout_marginBottom="8dp" />

        <!-- Subtitle -->
        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="🔐 أدخل رمز الدخول للمتابعة"
            android:textSize="14sp"
            android:textColor="#99FFFFFF"
            android:layout_marginBottom="40dp" />

        <!-- Password Input -->
        <EditText
            android:id="@+id/etPassword"
            android:layout_width="280dp"
            android:layout_height="60dp"
            android:inputType="numberPassword"
            android:hint="🔒 ●●●●"
            android:textColor="#FFFFFF"
            android:textColorHint="#44FFFFFF"
            android:background="@drawable/bg_input"
            android:paddingStart="20dp"
            android:paddingEnd="20dp"
            android:textAlignment="center"
            android:maxLength="6"
            android:textSize="22sp"
            android:letterSpacing="0.2"
            android:imeOptions="actionDone" />

        <!-- Unlock Button -->
        <Button
            android:id="@+id/btnUnlock"
            android:layout_width="280dp"
            android:layout_height="60dp"
            android:text="🔓 فتح التطبيق"
            android:textColor="#FFFFFF"
            android:textSize="16sp"
            android:textStyle="bold"
            android:background="@drawable/bg_button"
            android:layout_marginTop="36dp"
            android:elevation="12dp" />

        <!-- Footer -->
        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="💖 ZHARE © 2026"
            android:textSize="11sp"
            android:textColor="#44FFFFFF"
            android:layout_marginTop="60dp" />

    </LinearLayout>
</ScrollView>
""")

    write_file("app/src/main/res/layout/activity_chat.xml", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:background="#0D0610">

    <!-- Toolbar -->
    <com.google.android.material.appbar.MaterialToolbar
        android:id="@+id/toolbar"
        android:layout_width="match_parent"
        android:layout_height="?attr/actionBarSize"
        android:background="#EC4899"
        app:titleTextColor="#FFFFFF">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:gravity="center_vertical"
            android:orientation="horizontal">

            <TextView
                android:id="@+id/tvToolbarTitle"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="💖 File Vault"
                android:textColor="#FFFFFF"
                android:textSize="18sp"
                android:textStyle="bold" />

            <ImageButton
                android:id="@+id/btnFiles"
                android:layout_width="40dp"
                android:layout_height="40dp"
                android:src="📂"
                android:background="?attr/selectableItemBackgroundBorderless"
                android:contentDescription="فتح الملفات"
                android:layout_marginEnd="4dp" />

            <ImageButton
                android:id="@+id/btnLock"
                android:layout_width="40dp"
                android:layout_height="40dp"
                android:src="🔒"
                android:background="?attr/selectableItemBackgroundBorderless"
                android:contentDescription="قفل التطبيق" />

        </LinearLayout>

    </com.google.android.material.appbar.MaterialToolbar>

    <!-- Chat Messages -->
    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/rvChat"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:padding="12dp"
        android:clipToPadding="false" />

    <!-- Input Bar -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center_vertical"
        android:padding="8dp"
        android:background="#1A0D0610"
        android:elevation="8dp">

        <EditText
            android:id="@+id/etMessage"
            android:layout_width="0dp"
            android:layout_height="48dp"
            android:layout_weight="1"
            android:hint="💬 اكتب رسالة أو أمر..."
            android:textColor="#FFFFFF"
            android:textColorHint="#66FFFFFF"
            android:background="@drawable/bg_input_chat"
            android:paddingStart="16dp"
            android:paddingEnd="16dp"
            android:maxLines="3"
            android:inputType="textMultiLine" />

        <ImageButton
            android:id="@+id/btnSend"
            android:layout_width="48dp"
            android:layout_height="48dp"
            android:src="📤"
            android:background="@drawable/bg_send_btn"
            android:layout_marginStart="8dp"
            android:contentDescription="إرسال" />

    </LinearLayout>
</LinearLayout>
""")

    write_file("app/src/main/res/layout/activity_files.xml", """<?xml version="1.0" encoding="utf-8"?>
<androidx.coordinatorlayout.widget.CoordinatorLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#0D0610">

    <com.google.android.material.appbar.AppBarLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:background="#EC4899">

        <com.google.android.material.appbar.MaterialToolbar
            android:id="@+id/toolbar"
            android:layout_width="match_parent"
            android:layout_height="?attr/actionBarSize"
            app:titleTextColor="#FFFFFF"
            app:navigationIcon="⬅️" />

        <TextView
            android:id="@+id/tvPath"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:textColor="#CCFFFFFF"
            android:textSize="11sp"
            android:paddingStart="16dp"
            android:paddingEnd="16dp"
            android:paddingBottom="6dp"
            android:maxLines="1"
            android:ellipsize="start" />

    </com.google.android.material.appbar.AppBarLayout>

    <FrameLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        app:layout_behavior="@string/appbar_scrolling_view_behavior">

        <androidx.recyclerview.widget.RecyclerView
            android:id="@+id/rvFiles"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:padding="4dp"
            android:clipToPadding="false" />

        <TextView
            android:id="@+id/tvEmpty"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_gravity="center"
            android:text="📂 لا توجد ملفات"
            android:textColor="#99FFFFFF"
            android:textSize="16sp"
            android:visibility="gone" />

    </FrameLayout>

    <com.google.android.material.floatingactionbutton.FloatingActionButton
        android:id="@+id/fabLock"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="bottom|end"
        android:layout_margin="20dp"
        android:text="🔒"
        app:backgroundTint="#EC4899"
        app:tint="#FFFFFF"
        app:elevation="12dp" />

</androidx.coordinatorlayout.widget.CoordinatorLayout>
""")

    write_file("app/src/main/res/layout/item_file.xml", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="horizontal"
    android:padding="10dp"
    android:gravity="center_vertical"
    android:minHeight="64dp"
    android:background="?attr/selectableItemBackground">

    <TextView
        android:id="@+id/tvIcon"
        android:layout_width="44dp"
        android:layout_height="44dp"
        android:gravity="center"
        android:textSize="24sp"
        android:background="@drawable/bg_icon"
        android:layout_marginEnd="10dp"
        android:text="📄" />

    <LinearLayout
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_weight="1"
        android:orientation="vertical"
        android:layout_marginEnd="8dp">

        <TextView
            android:id="@+id/tvName"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:textColor="#FFFFFF"
            android:textSize="14sp"
            android:maxLines="1"
            android:ellipsize="end" />

        <TextView
            android:id="@+id/tvInfo"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:textColor="#99FFFFFF"
            android:textSize="11sp"
            android:layout_marginTop="2dp" />

    </LinearLayout>
</LinearLayout>
""")

    write_file("app/src/main/res/layout/item_chat.xml", """<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:paddingStart="16dp"
    android:paddingEnd="16dp"
    android:paddingTop="4dp"
    android:paddingBottom="4dp">

    <LinearLayout
        android:id="@+id/bubble"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:maxWidth="280dp"
        android:orientation="vertical"
        android:padding="12dp">

        <TextView
            android:id="@+id/tvMessage"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:textSize="14sp"
            android:textColor="#FFFFFF" />

        <TextView
            android:id="@+id/tvTime"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:textSize="10sp"
            android:textColor="#99FFFFFF"
            android:layout_marginTop="4dp"
            android:layout_gravity="end" />

    </LinearLayout>
</FrameLayout>
""")

    section("DRAWABLES")

    write_file("app/src/main/res/drawable/bg_circle.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="oval">
    <solid android:color="#1AEC4899" />
    <stroke android:width="2dp" android:color="#33EC4899" />
</shape>
""")

    write_file("app/src/main/res/drawable/bg_input.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#1AEC4899" />
    <corners android:radius="30dp" />
    <stroke android:width="1.5dp" android:color="#33EC4899" />
</shape>
""")

    write_file("app/src/main/res/drawable/bg_button.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <gradient android:startColor="#EC4899" android:endColor="#F472B6" android:angle="135" />
    <corners android:radius="30dp" />
</shape>
""")

    write_file("app/src/main/res/drawable/bg_input_chat.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#15FFFFFF" />
    <corners android:radius="24dp" />
    <stroke android:width="1dp" android:color="#22EC4899" />
</shape>
""")

    write_file("app/src/main/res/drawable/bg_send_btn.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="oval">
    <gradient android:startColor="#EC4899" android:endColor="#F472B6" android:angle="135" />
</shape>
""")

    write_file("app/src/main/res/drawable/bg_chat_sent.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <gradient android:startColor="#EC4899" android:endColor="#F472B6" android:angle="135" />
    <corners android:topLeftRadius="20dp" android:topRightRadius="20dp" android:bottomLeftRadius="20dp" android:bottomRightRadius="4dp" />
</shape>
""")

    write_file("app/src/main/res/drawable/bg_chat_received.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#1AEC4899" />
    <corners android:topLeftRadius="20dp" android:topRightRadius="20dp" android:bottomLeftRadius="4dp" android:bottomRightRadius="20dp" />
    <stroke android:width="1dp" android:color="#22EC4899" />
</shape>
""")

    write_file("app/src/main/res/drawable/bg_icon.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#0AEC4899" />
    <corners android:radius="10dp" />
</shape>
""")

    section("VALUES")

    write_file("app/src/main/res/values/colors.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="pink_primary">#EC4899</color>
    <color name="pink_secondary">#F472B6</color>
    <color name="pink_light">#FBCFE8</color>
    <color name="surface_dark">#0D0610</color>
    <color name="white">#FFFFFF</color>
    <color name="text_primary">#FFFFFF</color>
    <color name="text_secondary">#99FFFFFF</color>
</resources>
""")

    write_file("app/src/main/res/values/themes.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.FileVault" parent="Theme.MaterialComponents.DayNight.NoActionBar">
        <item name="colorPrimary">@color/pink_primary</item>
        <item name="colorPrimaryVariant">@color/pink_secondary</item>
        <item name="colorOnPrimary">@color/white</item>
        <item name="android:statusBarColor">@color/pink_primary</item>
        <item name="android:navigationBarColor">@color/surface_dark</item>
        <item name="android:windowBackground">@color/surface_dark</item>
    </style>
</resources>
""")

    write_file("app/src/main/res/values/strings.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">File Vault 💖</string>
</resources>
""")

    section("ANIMATIONS")

    write_file("app/src/main/res/anim/shake.xml", """<?xml version="1.0" encoding="utf-8"?>
<set xmlns:android="http://schemas.android.com/apk/res/android">
    <translate android:fromXDelta="0" android:toXDelta="15"
        android:duration="80" android:interpolator="@android:anim/cycle_interpolator" />
</set>
""")

    write_file("app/src/main/res/anim/slide_in_right.xml", """<?xml version="1.0" encoding="utf-8"?>
<set xmlns:android="http://schemas.android.com/apk/res/android">
    <translate android:fromXDelta="100%p" android:toXDelta="0"
        android:duration="300" android:interpolator="@android:anim/decelerate_interpolator" />
</set>
""")

    write_file("app/src/main/res/anim/slide_out_left.xml", """<?xml version="1.0" encoding="utf-8"?>
<set xmlns:android="http://schemas.android.com/apk/res/android">
    <translate android:fromXDelta="0" android:toXDelta="-100%p"
        android:duration="300" android:interpolator="@android:anim/accelerate_interpolator" />
</set>
""")

    section("MIPMAP (ICONS)")

    write_file("app/src/main/res/mipmap-hdpi/ic_launcher.xml", """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/pink_primary" />
    <foreground android:drawable="@color/white" />
</adaptive-icon>
""")

    write_file("app/src/main/res/mipmap-hdpi/ic_launcher_round.xml", """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/pink_primary" />
    <foreground android:drawable="@color/white" />
</adaptive-icon>
""")

    section("GITHUB ACTIONS WORKFLOW")

    write_file(".github/workflows/main.yml", """name: 💖 Build File Vault APK

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: 📥 Checkout Repository
        uses: actions/checkout@v4

      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 📝 Generate Project Files
        run: python scraper.py

      - name: 📂 Move Files to Root
        run: |
          cp -r FileVault/* .
          cp -r FileVault/.gitignore . 2>/dev/null || true

      - name: ☕ Setup JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: 📱 Setup Android SDK
        uses: android-actions/setup-android@v3
        with:
          api-level: 34
          build-tools: 34.0.0

      - name: 🔧 Make gradlew Executable
        run: chmod +x gradlew

      - name: 🏗️ Build Debug APK
        run: ./gradlew assembleDebug

      - name: 🏗️ Build Release APK
        run: ./gradlew assembleRelease

      - name: 📦 Upload Debug APK
        uses: actions/upload-artifact@v4
        with:
          name: FileVault-Debug-APK
          path: app/build/outputs/apk/debug/*.apk
          retention-days: 7

      - name: 📦 Upload Release APK
        uses: actions/upload-artifact@v4
        with:
          name: FileVault-Release-APK
          path: app/build/outputs/apk/release/*.apk
          retention-days: 30
""")

    # Final summary
    print(f"""
{'='*60}
  💖 BUILD COMPLETE! ✨
{'='*60}

  📊 Stats:
     • {TOTAL_FILES} files generated
     • {TOTAL_LINES}+ lines of code

  📁 Project: {ROOT_DIR}

  🎯 Features:
     • 💬 WhatsApp-Style Chat Interface
     • 🔐 AES-256 File Encryption
     • 📁 External Storage Browser
     • 🔒 Password: 1234
     • 💖 Pink Rose Glass Theme
     • ⚡ Files Appear CORRUPTED Outside App

  🚀 To Push to GitHub:
     cd {PROJECT_NAME}
     git init
     git add .
     git commit -m "💖 File Vault"
     git remote add origin YOUR_REPO_URL
     git push -u origin main

  ⚡ GitHub Actions will auto-build APK!
     (Then add build-apk.yml for manual builds)

  💖 ZHARE - File Vault Ready!
{'='*60}
""")

# ═══════════════════════════════════════════════════════════
# 💖 MAIN
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  💖  FILE VAULT - WhatsApp-Style Secret Vault  💖     ║
║     AES-256 Encryption | Password 1234                   ║
║     GitHub Actions APK Generator                         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    build_all()
