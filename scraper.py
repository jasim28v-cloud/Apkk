#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                                                            ║
║  💖  FILE VAULT - Pink Rose APK Builder  💖              ║
║     WhatsApp UI + AES Encryption + GitHub Actions           ║
║     WITH GRADLE WRAPPER (READY TO BUILD)                    ║
║                                                            ║
║  🔐  Password: 1234                                       ║
║  🎨  Theme: Pink Rose Glass                                ║
║  📁  File Manager + Encrypt/Decrypt                        ║
║                                                            ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import json
import zipfile
import urllib.request
import stat

# ═══════════════════════════════════════════════════════════
# 💖 CONFIGURATION
# ═══════════════════════════════════════════════════════════

PROJECT_NAME = "FileVault"
PACKAGE_NAME = "com.zhare.filevault"
APP_PASSWORD = "1234"
GRADLE_VERSION = "8.2"
GRADLE_DIST_URL = f"https://services.gradle.org/distributions/gradle-{GRADLE_VERSION}-bin.zip"

TOTAL_FILES = 0
TOTAL_LINES = 0
ROOT_DIR = os.path.join(os.getcwd(), PROJECT_NAME)

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

def write_binary(filepath, content):
    global TOTAL_FILES
    full_path = os.path.join(ROOT_DIR, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'wb') as f:
        f.write(content)
    TOTAL_FILES += 1
    print(f"  ✅ {filepath} (binary)")

def section(title):
    print(f"\n{'='*60}")
    print(f"  💖 {title}")
    print(f"{'='*60}")

# ═══════════════════════════════════════════════════════════
# 💖 DOWNLOAD GRADLE WRAPPER
# ═══════════════════════════════════════════════════════════

def download_gradle_wrapper():
    section("DOWNLOADING GRADLE WRAPPER")
    
    # gradlew (shell script)
    gradlew_content = """#!/bin/sh
# Gradle wrapper script
##############################################################################
##  Gradle start up script for UN*X
##############################################################################
# Attempt to set APP_HOME
PRG="$0"
while [ -h "$PRG" ]; do
    ls=`ls -ld "$PRG"`
    link=`expr "$ls" : '.*-> \\(.*\\)$'`
    if expr "$link" : '/.*' > /dev/null; then
        PRG="$link"
    else
        PRG=`dirname "$PRG"`"/$link"
    fi
done
SAVED="`pwd`"
cd "`dirname \"$PRG\"`/" >/dev/null
APP_HOME="`pwd -P`"
cd "$SAVED" >/dev/null

APP_NAME="Gradle"
APP_BASE_NAME=`basename "$0"`

DEFAULT_JVM_OPTS='"-Xmx64m" "-Xms64m"'

MAX_FD="maximum"

warn () {
    echo "$*"
}

die () {
    echo
    echo "$*"
    echo
    exit 1
}

OS_NAME="`uname`"
case "$OS_NAME" in
    CYGWIN* | MINGW* | MSYS* )
        SEPARATOR=";"
        ;;
    *)
        SEPARATOR=":"
        ;;
esac

CLASSPATH=$APP_HOME/gradle/wrapper/gradle-wrapper.jar

if [ ! -f "$CLASSPATH" ]; then
    die "ERROR: Gradle wrapper JAR not found: $CLASSPATH"
fi

GRADLE_OPTS="${GRADLE_OPTS} -Dorg.gradle.appname=${APP_BASE_NAME}"

exec java $DEFAULT_JVM_OPTS $JAVA_OPTS $GRADLE_OPTS \\
    -classpath "$CLASSPATH" \\
    org.gradle.wrapper.GradleWrapperMain "$@"
"""
    write_file("gradlew", gradlew_content)
    os.chmod(os.path.join(ROOT_DIR, "gradlew"), 0o755)

    # gradlew.bat (Windows)
    gradlew_bat = """@rem Gradle wrapper script for Windows
@if "%DEBUG%"=="" @echo off
@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal
set DIRNAME=%~dp0
if "%DIRNAME%"=="" set DIRNAME=.
@rem This is normally unused
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%
set DEFAULT_JVM_OPTS="-Xmx64m" "-Xms64m"
set CLASSPATH=%APP_HOME%\\gradle\\wrapper\\gradle-wrapper.jar
@rem Execute Gradle
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %GRADLE_OPTS% "-Dorg.gradle.appname=%APP_BASE_NAME%" -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*
:end
@rem End local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" endlocal
:omega
"""
    write_file("gradlew.bat", gradlew_bat)

    # Download gradle-wrapper.jar
    wrapper_jar_url = "https://raw.githubusercontent.com/gradle/gradle/v8.2.0/gradle/wrapper/gradle-wrapper.jar"
    print(f"  📥 Downloading gradle-wrapper.jar...")
    try:
        urllib.request.urlretrieve(wrapper_jar_url, os.path.join(ROOT_DIR, "gradle/wrapper/gradle-wrapper.jar"))
        print(f"  ✅ gradle/wrapper/gradle-wrapper.jar")
        TOTAL_FILES += 1
    except:
        print(f"  ⚠️ Could not download gradle-wrapper.jar, creating placeholder")
        write_binary("gradle/wrapper/gradle-wrapper.jar", b'placeholder')

    # gradle-wrapper.properties
    write_file("gradle/wrapper/gradle-wrapper.properties", f"""distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-{GRADLE_VERSION}-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""")

# ═══════════════════════════════════════════════════════════
# 💖 BUILD PROJECT FILES
# ═══════════════════════════════════════════════════════════

def build_all():
    # Download Gradle Wrapper first
    download_gradle_wrapper()

    section("ROOT BUILD FILES")

    # Root build.gradle
    write_file("build.gradle", """buildscript {
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
}
""")

    # settings.gradle
    write_file("settings.gradle", f"""rootProject.name = "{PROJECT_NAME}"
include ':app'
""")

    # gradle.properties
    write_file("gradle.properties", """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true
android.enableJetifier=true
""")

    # .gitignore
    write_file(".gitignore", """*.iml
.gradle
/local.properties
/.idea
.DS_Store
/build
/captures
.externalNativeBuild
.cxx
local.properties
/app/build
/app/release
*.apk
*.aab
*.jks
*.keystore
""")

    section("APP BUILD FILES")

    # App build.gradle
    write_file("app/build.gradle", f"""plugins {{
    id 'com.android.application'
}}

android {{
    namespace '{PACKAGE_NAME}'
    compileSdk 34

    defaultConfig {{
        applicationId '{PACKAGE_NAME}'
        minSdk 24
        targetSdk 34
        versionCode {{{{ github.run_number || 1 }}}}
        versionName "1.0.{ {{{ github.run_number || 1 }}} }"
        
        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }}

    buildTypes {{
        debug {{
            applicationIdSuffix ".debug"
            versionNameSuffix "-debug"
            debuggable true
        }}
        release {{
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
    }}

    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }}

    applicationVariants.all {{ variant ->
        variant.outputs.all {{ output ->
            def appName = "{PROJECT_NAME}"
            def buildType = variant.buildType.name
            def versionName = variant.versionName
            outputFileName = "${{appName}}_${{versionName}}_${{buildType}}.apk"
        }}
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.recyclerview:recyclerview:1.3.2'
    implementation 'androidx.swiperefreshlayout:swiperefreshlayout:1.1.0'
    implementation 'androidx.documentfile:documentfile:1.0.1'
    implementation 'com.google.code.gson:gson:2.10.1'
    implementation 'androidx.security:security-crypto:1.1.0-alpha06'
}}
""")

    # AndroidManifest.xml
    write_file("app/src/main/AndroidManifest.xml", f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <!-- Permissions -->
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
        android:requestLegacyExternalStorage="true">

        <!-- Lock Screen (Launcher) -->
        <activity
            android:name=".ui.LockScreenActivity"
            android:exported="true"
            android:theme="@style/Theme.FileVault"
            android:screenOrientation="portrait">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <!-- Main Activity -->
        <activity
            android:name=".ui.MainActivity"
            android:theme="@style/Theme.FileVault"
            android:screenOrientation="portrait" />

        <!-- File Viewer -->
        <activity
            android:name=".ui.FileViewerActivity"
            android:theme="@style/Theme.FileVault"
            android:screenOrientation="portrait" />

    </application>
</manifest>
""")

    # ProGuard
    write_file("app/proguard-rules.pro", """# File Vault ProGuard Rules
-keep class com.zhare.filevault.** { *; }
-keep class javax.crypto.** { *; }
-keep class java.security.** { *; }
-keepclassmembers class * {
    native <methods>;
}
-dontwarn javax.annotation.**
-dontwarn okhttp3.**
-dontwarn okio.**
""")

    section("JAVA SOURCE FILES")

    # AESHelper.java
    write_file("app/src/main/java/com/zhare/filevault/crypto/AESHelper.java", f"""package com.zhare.filevault.crypto;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.util.Base64;

/**
 * 💖 AES-256 Encryption Helper
 * Uses password for key derivation
 */
public class AESHelper {{
    private static final String ALGORITHM = "AES";
    private static final String TRANSFORMATION = "AES/ECB/PKCS5Padding";
    private static final String SECRET_KEY = "{APP_PASSWORD}";

    private static SecretKeySpec getSecretKey() throws Exception {{
        MessageDigest sha = MessageDigest.getInstance("SHA-256");
        byte[] key = sha.digest(SECRET_KEY.getBytes("UTF-8"));
        return new SecretKeySpec(key, ALGORITHM);
    }}

    public static byte[] encrypt(byte[] data) throws Exception {{
        Cipher cipher = Cipher.getInstance(TRANSFORMATION);
        cipher.init(Cipher.ENCRYPT_MODE, getSecretKey());
        return cipher.doFinal(data);
    }}

    public static byte[] decrypt(byte[] data) throws Exception {{
        Cipher cipher = Cipher.getInstance(TRANSFORMATION);
        cipher.init(Cipher.DECRYPT_MODE, getSecretKey());
        return cipher.doFinal(data);
    }}

    public static byte[] encryptFile(byte[] fileData) throws Exception {{
        return encrypt(fileData);
    }}

    public static byte[] decryptFile(byte[] fileData) throws Exception {{
        return decrypt(fileData);
    }}

    public static String encryptToBase64(String text) {{
        try {{
            byte[] encrypted = encrypt(text.getBytes("UTF-8"));
            return Base64.getEncoder().encodeToString(encrypted);
        }} catch (Exception e) {{
            return null;
        }}
    }}

    public static String decryptFromBase64(String encryptedText) {{
        try {{
            byte[] decoded = Base64.getDecoder().decode(encryptedText);
            byte[] decrypted = decrypt(decoded);
            return new String(decrypted, "UTF-8");
        }} catch (Exception e) {{
            return null;
        }}
    }}
}}
""")

    # FileItem.java
    write_file("app/src/main/java/com/zhare/filevault/models/FileItem.java", """package com.zhare.filevault.models;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/**
 * 💖 File Model for display in list
 */
public class FileItem {
    private String name;
    private String path;
    private long size;
    private boolean isDirectory;
    private boolean isEncrypted;
    private boolean isHidden;
    private String mimeType;
    private long lastModified;

    public FileItem(File file) {
        this.name = file.getName();
        this.path = file.getAbsolutePath();
        this.size = file.length();
        this.isDirectory = file.isDirectory();
        this.isHidden = file.isHidden();
        this.isEncrypted = file.getName().toLowerCase().endsWith(".enc");
        this.lastModified = file.lastModified();
        this.mimeType = getMimeType();
    }

    private String getMimeType() {
        if (isDirectory) return "📁 مجلد";
        String nameLower = name.toLowerCase();
        if (nameLower.matches(".*\\.(jpg|jpeg|png|gif|bmp|webp|heic)$")) return "🖼️ صورة";
        if (nameLower.matches(".*\\.(mp4|mkv|avi|mov|wmv|flv|3gp)$")) return "🎬 فيديو";
        if (nameLower.matches(".*\\.(mp3|wav|ogg|m4a|aac|flac)$")) return "🎵 صوت";
        if (nameLower.matches(".*\\.(pdf)$")) return "📄 PDF";
        if (nameLower.matches(".*\\.(doc|docx)$")) return "📝 Word";
        if (nameLower.matches(".*\\.(xls|xlsx)$")) return "📊 Excel";
        if (nameLower.matches(".*\\.(ppt|pptx)$")) return "📽️ PowerPoint";
        if (nameLower.matches(".*\\.(apk)$")) return "📦 APK";
        if (nameLower.matches(".*\\.(zip|rar|7z|tar|gz)$")) return "🗜️ مضغوط";
        if (nameLower.endsWith(".enc")) return "🔒 مشفر";
        return "📄 ملف";
    }

    // Getters
    public String getName() { return name; }
    public String getPath() { return path; }
    public long getSize() { return size; }
    public boolean isDirectory() { return isDirectory; }
    public boolean isEncrypted() { return isEncrypted; }
    public boolean isHidden() { return isHidden; }
    public String getMimeType() { return mimeType; }
    public long getLastModified() { return lastModified; }

    public String getSizeFormatted() {
        if (isDirectory) return "";
        if (size < 1024) return size + " B";
        if (size < 1024 * 1024) return String.format("%.1f KB", size / 1024.0);
        if (size < 1024 * 1024 * 1024) return String.format("%.1f MB", size / (1024.0 * 1024));
        return String.format("%.1f GB", size / (1024.0 * 1024 * 1024));
    }

    public String getDateFormatted() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy/MM/dd HH:mm", Locale.getDefault());
        return sdf.format(new Date(lastModified));
    }
}
""")

    # FileAdapter.java
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
 * 💖 RecyclerView Adapter for File List
 * WhatsApp-style file browser
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
        String icon = file.getMimeType().substring(0, 2);
        
        holder.tvIcon.setText(icon);
        holder.tvFileName.setText(file.getName());
        holder.tvFileInfo.setText(file.getDateFormatted() + 
            (file.getSizeFormatted().isEmpty() ? "" : " • " + file.getSizeFormatted()));
        holder.tvFileType.setText(file.getMimeType());

        // Pink accent for encrypted files
        if (file.isEncrypted()) {
            holder.tvFileName.setTextColor(Color.parseColor("#EC4899"));
            holder.tvIcon.setText("🔒");
        } else if (file.isHidden()) {
            holder.tvFileName.setTextColor(Color.parseColor("#AAFFFFFF"));
        } else {
            holder.tvFileName.setTextColor(Color.parseColor("#FFFFFF"));
        }

        // Folder icon
        if (file.isDirectory()) {
            holder.tvIcon.setText("📁");
        }

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

    public List<FileItem> getFiles() {
        return files;
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvIcon, tvFileName, tvFileInfo, tvFileType;

        ViewHolder(View itemView) {
            super(itemView);
            tvIcon = itemView.findViewById(R.id.tvIcon);
            tvFileName = itemView.findViewById(R.id.tvFileName);
            tvFileInfo = itemView.findViewById(R.id.tvFileInfo);
            tvFileType = itemView.findViewById(R.id.tvFileType);
        }
    }
}
""")

    # LockScreenActivity.java
    write_file(f"app/src/main/java/com/zhare/filevault/ui/LockScreenActivity.java", f"""package com.zhare.filevault.ui;

import android.animation.ArgbEvaluator;
import android.animation.ValueAnimator;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.zhare.filevault.R;

/**
 * 💖 Lock Screen - Password 1234
 * Entry point of the app
 */
public class LockScreenActivity extends AppCompatActivity {{
    private static final String PREFS_NAME = "FileVaultPrefs";
    private static final String KEY_UNLOCKED = "is_unlocked";
    private static final String PASSWORD = "{APP_PASSWORD}";
    
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

        // Set pink status bar
        getWindow().setStatusBarColor(Color.parseColor("#EC4899"));
        getWindow().setNavigationBarColor(Color.parseColor("#0D0610"));

        prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);

        // Auto-login if already unlocked
        if (prefs.getBoolean(KEY_UNLOCKED, false) && !getIntent().getBooleanExtra("force_lock", false)) {{
            openMainApp();
            return;
        }}

        initViews();
        setupAnimations();
    }}

    private void initViews() {{
        etPassword = findViewById(R.id.etPassword);
        btnUnlock = findViewById(R.id.btnUnlock);
        tvTitle = findViewById(R.id.tvTitle);

        // Auto-focus password field
        etPassword.requestFocus();

        btnUnlock.setOnClickListener(v -> verifyPassword());
        
        // Enter key submits
        etPassword.setOnEditorActionListener((v, actionId, event) -> {{
            verifyPassword();
            return true;
        }});
    }}

    private void setupAnimations() {{
        // Pulse animation on title
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
            etPassword.setError("❌ أدخل الرمز!");
            shakeView(etPassword);
            return;
        }}

        if (input.equals(PASSWORD)) {{
            // Success
            prefs.edit().putBoolean(KEY_UNLOCKED, true).apply();
            Toast.makeText(this, "✅ مرحباً بك! 💖", Toast.LENGTH_SHORT).show();
            
            // Delay then open main
            handler.postDelayed(this::openMainApp, 500);
        }} else {{
            // Failed
            failedAttempts++;
            etPassword.setText("");
            etPassword.setError("❌ رمز خطأ! (" + failedAttempts + "/3)");
            shakeView(etPassword);

            if (failedAttempts >= 3) {{
                btnUnlock.setEnabled(false);
                etPassword.setEnabled(false);
                btnUnlock.setText("⏳ انتظر 30 ثانية...");
                
                handler.postDelayed(() -> {{
                    btnUnlock.setEnabled(true);
                    etPassword.setEnabled(true);
                    btnUnlock.setText("🔓 فتح");
                    failedAttempts = 0;
                }}, 30000);
            }}
        }}
    }}

    private void shakeView(View view) {{
        Animation shake = AnimationUtils.loadAnimation(this, R.anim.shake);
        view.startAnimation(shake);
    }}

    private void openMainApp() {{
        startActivity(new Intent(this, MainActivity.class));
        finish();
        overridePendingTransition(R.anim.slide_in_right, R.anim.slide_out_left);
    }}

    @Override
    protected void onPause() {{
        super.onPause();
        // Lock when app goes to background
        prefs.edit().putBoolean(KEY_UNLOCKED, false).apply();
    }}

    @Override
    public void onBackPressed() {{
        super.onBackPressed();
        finishAffinity();
    }}
}}
""")

    # MainActivity.java
    write_file("app/src/main/java/com/zhare/filevault/ui/MainActivity.java", """package com.zhare.filevault.ui;

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
import android.view.Menu;
import android.view.MenuItem;
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
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;
import com.google.android.material.appbar.MaterialToolbar;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.tabs.TabLayout;
import com.zhare.filevault.R;
import com.zhare.filevault.crypto.AESHelper;
import com.zhare.filevault.models.FileItem;
import java.io.*;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * 💖 Main Activity - WhatsApp-style File Manager
 */
public class MainActivity extends AppCompatActivity {
    private RecyclerView rvFiles;
    private FileAdapter adapter;
    private SwipeRefreshLayout swipeRefresh;
    private TabLayout tabLayout;
    private FloatingActionButton fabLock;
    private TextView tvEmpty, tvPath;
    private MaterialToolbar toolbar;
    
    private List<FileItem> allFiles = new ArrayList<>();
    private String currentPath;
    private String currentTab = "all";
    private ExecutorService executor = Executors.newSingleThreadExecutor();
    private Handler mainHandler = new Handler(Looper.getMainLooper());

    private final ActivityResultLauncher<Intent> storagePermissionLauncher = 
        registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                if (Environment.isExternalStorageManager()) {
                    loadFiles(Environment.getExternalStorageDirectory().getAbsolutePath());
                }
            }
        });

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Pink theme
        getWindow().setStatusBarColor(Color.parseColor("#EC4899"));
        getWindow().setNavigationBarColor(Color.parseColor("#0D0610"));

        initViews();
        setupTabs();
        setupListeners();
        requestPermissions();
    }

    private void initViews() {
        toolbar = findViewById(R.id.toolbar);
        rvFiles = findViewById(R.id.rvFiles);
        swipeRefresh = findViewById(R.id.swipeRefresh);
        tabLayout = findViewById(R.id.tabLayout);
        fabLock = findViewById(R.id.fabLock);
        tvEmpty = findViewById(R.id.tvEmpty);
        tvPath = findViewById(R.id.tvPath);

        toolbar.setTitle("💖 File Vault");
        toolbar.setTitleTextColor(Color.WHITE);
        toolbar.setBackgroundColor(Color.parseColor("#EC4899"));
        setSupportActionBar(toolbar);

        rvFiles.setLayoutManager(new LinearLayoutManager(this));
        adapter = new FileAdapter(new FileAdapter.OnFileClickListener() {
            @Override
            public void onFileClick(FileItem file, int position) {
                if (file.isDirectory()) {
                    loadFiles(file.getPath());
                } else {
                    openFile(file);
                }
            }
            @Override
            public void onFileLongClick(FileItem file, int position) {
                showFileOptions(file);
            }
        });
        rvFiles.setAdapter(adapter);
    }

    private void setupTabs() {
        String[] tabs = {"📁 الكل", "🖼️ صور", "🎬 فيديو", "🎵 صوت", "🔒 مشفر"};
        for (String tab : tabs) {
            tabLayout.addTab(tabLayout.newTab().setText(tab));
        }

        tabLayout.addOnTabSelectedListener(new TabLayout.OnTabSelectedListener() {
            @Override public void onTabSelected(TabLayout.Tab tab) {
                switch (tab.getPosition()) {
                    case 0: currentTab = "all"; break;
                    case 1: currentTab = "images"; break;
                    case 2: currentTab = "videos"; break;
                    case 3: currentTab = "audio"; break;
                    case 4: currentTab = "encrypted"; break;
                }
                filterFiles();
            }
            @Override public void onTabUnselected(TabLayout.Tab tab) {}
            @Override public void onTabReselected(TabLayout.Tab tab) {}
        });
    }

    private void setupListeners() {
        swipeRefresh.setOnRefreshListener(() -> {
            if (currentPath != null) {
                loadFiles(currentPath);
            }
            swipeRefresh.setRefreshing(false);
        });

        fabLock.setOnClickListener(v -> {
            getSharedPreferences("FileVaultPrefs", MODE_PRIVATE)
                .edit().putBoolean("is_unlocked", false).apply();
            Intent intent = new Intent(this, LockScreenActivity.class);
            intent.putExtra("force_lock", true);
            startActivity(intent);
            finish();
        });

        toolbar.setNavigationOnClickListener(v -> {
            if (currentPath != null) {
                File current = new File(currentPath);
                File parent = current.getParentFile();
                if (parent != null && parent.canRead()) {
                    loadFiles(parent.getAbsolutePath());
                }
            }
        });
    }

    private void requestPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            if (!Environment.isExternalStorageManager()) {
                showPermissionDialog();
            } else {
                loadFiles(Environment.getExternalStorageDirectory().getAbsolutePath());
            }
        } else {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE)
                    != PackageManager.PERMISSION_GRANTED) {
                requestPermissions(new String[]{
                    Manifest.permission.READ_EXTERNAL_STORAGE,
                    Manifest.permission.WRITE_EXTERNAL_STORAGE
                }, 100);
            } else {
                loadFiles(Environment.getExternalStorageDirectory().getAbsolutePath());
            }
        }
    }

    private void showPermissionDialog() {
        new AlertDialog.Builder(this)
            .setTitle("💖 صلاحيات مطلوبة")
            .setMessage("يحتاج التطبيق صلاحية الوصول لجميع الملفات لعرضها وإدارتها.")
            .setPositiveButton("منح الصلاحية", (d, w) -> {
                Intent intent = new Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION);
                intent.setData(Uri.parse("package:" + getPackageName()));
                storagePermissionLauncher.launch(intent);
            })
            .setNegativeButton("إلغاء", (d, w) -> finish())
            .show();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
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
                if (parent != null && !path.equals("/")) {
                    files.add(new FileItem(parent) {
                        @Override
                        public String getName() { return "📁 .. (رجوع)"; }
                    });
                }

                File[] fileList = dir.listFiles();
                if (fileList != null) {
                    for (File f : fileList) {
                        if (!f.isHidden() || f.getName().startsWith(".")) {
                            files.add(new FileItem(f));
                        }
                    }
                }

                // Sort: directories first, then by name
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
                filterFiles();
                
                if (finalFiles.isEmpty()) {
                    tvEmpty.setVisibility(View.VISIBLE);
                    rvFiles.setVisibility(View.GONE);
                }
            });
        });
    }

    private void filterFiles() {
        List<FileItem> filtered = new ArrayList<>();
        for (FileItem f : allFiles) {
            switch (currentTab) {
                case "images":
                    if (f.getMimeType().contains("صورة")) filtered.add(f);
                    break;
                case "videos":
                    if (f.getMimeType().contains("فيديو")) filtered.add(f);
                    break;
                case "audio":
                    if (f.getMimeType().contains("صوت")) filtered.add(f);
                    break;
                case "encrypted":
                    if (f.isEncrypted()) filtered.add(f);
                    break;
                default:
                    filtered.add(f);
            }
        }
        adapter.updateList(filtered);
    }

    private void openFile(FileItem file) {
        try {
            File f = new File(file.getPath());
            String mimeType;
            String ext = file.getName().toLowerCase();
            
            if (ext.matches(".*\\.(jpg|jpeg|png|gif|bmp)$")) mimeType = "image/*";
            else if (ext.matches(".*\\.(mp4|mkv|avi|3gp)$")) mimeType = "video/*";
            else if (ext.matches(".*\\.(mp3|wav|ogg|m4a)$")) mimeType = "audio/*";
            else if (ext.endsWith(".pdf")) mimeType = "application/pdf";
            else if (ext.endsWith(".apk")) mimeType = "application/vnd.android.package-archive";
            else mimeType = "*/*";

            Intent intent = new Intent(Intent.ACTION_VIEW);
            intent.setDataAndType(Uri.fromFile(f), mimeType);
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            startActivity(Intent.createChooser(intent, "فتح " + file.getName()));
        } catch (Exception e) {
            Toast.makeText(this, "❌ لا يمكن فتح الملف", Toast.LENGTH_SHORT).show();
        }
    }

    private void showFileOptions(FileItem file) {
        String[] options;
        if (file.isEncrypted()) {
            options = new String[]{"🔓 فك التشفير", "📋 نسخ المسار", "📝 إعادة تسمية", "ℹ️ معلومات", "🗑️ حذف"};
        } else if (file.isDirectory()) {
            options = new String[]{"📋 نسخ المسار", "ℹ️ معلومات"};
        } else {
            options = new String[]{"🔒 تشفير", "📋 نسخ المسار", "📝 إعادة تسمية", "ℹ️ معلومات", "🗑️ حذف"};
        }

        new AlertDialog.Builder(this)
            .setTitle("💖 " + file.getName())
            .setIcon(android.R.drawable.ic_menu_manage)
            .setItems(options, (dialog, which) -> {
                switch (options[which]) {
                    case "🔒 تشفير": encryptFile(file); break;
                    case "🔓 فك التشفير": decryptFile(file); break;
                    case "📋 نسخ المسار": copyToClipboard(file.getPath()); break;
                    case "📝 إعادة تسمية": renameFile(file); break;
                    case "ℹ️ معلومات": showFileInfo(file); break;
                    case "🗑️ حذف": deleteFile(file); break;
                }
            })
            .show();
    }

    private void encryptFile(FileItem file) {
        new AlertDialog.Builder(this)
            .setTitle("🔒 تأكيد التشفير")
            .setMessage("سيتم تشفير: " + file.getName() + "\\n\\nسيتم حذف الملف الأصلي!")
            .setPositiveButton("تشفير", (d, w) -> {
                executor.execute(() -> {
                    try {
                        File f = new File(file.getPath());
                        byte[] data = new byte[(int) f.length()];
                        FileInputStream fis = new FileInputStream(f);
                        fis.read(data);
                        fis.close();

                        byte[] encrypted = AESHelper.encryptFile(data);
                        File encryptedFile = new File(file.getPath() + ".enc");
                        FileOutputStream fos = new FileOutputStream(encryptedFile);
                        fos.write(encrypted);
                        fos.close();

                        f.delete();

                        mainHandler.post(() -> {
                            Toast.makeText(this, "✅ تم التشفير!", Toast.LENGTH_SHORT).show();
                            loadFiles(encryptedFile.getParent());
                        });
                    } catch (Exception e) {
                        mainHandler.post(() -> 
                            Toast.makeText(this, "❌ فشل التشفير", Toast.LENGTH_SHORT).show());
                    }
                });
            })
            .setNegativeButton("إلغاء", null)
            .show();
    }

    private void decryptFile(FileItem file) {
        new AlertDialog.Builder(this)
            .setTitle("🔓 تأكيد فك التشفير")
            .setMessage("سيتم فك تشفير: " + file.getName() + "\\n\\nسيتم حذف الملف المشفر!")
            .setPositiveButton("فك", (d, w) -> {
                executor.execute(() -> {
                    try {
                        File f = new File(file.getPath());
                        byte[] data = new byte[(int) f.length()];
                        FileInputStream fis = new FileInputStream(f);
                        fis.read(data);
                        fis.close();

                        byte[] decrypted = AESHelper.decryptFile(data);
                        String originalName = file.getPath().replace(".enc", "");
                        File decryptedFile = new File(originalName);
                        FileOutputStream fos = new FileOutputStream(decryptedFile);
                        fos.write(decrypted);
                        fos.close();

                        f.delete();

                        mainHandler.post(() -> {
                            Toast.makeText(this, "✅ تم فك التشفير!", Toast.LENGTH_SHORT).show();
                            loadFiles(decryptedFile.getParent());
                        });
                    } catch (Exception e) {
                        mainHandler.post(() -> 
                            Toast.makeText(this, "❌ فشل - كلمة السر خطأ", Toast.LENGTH_SHORT).show());
                    }
                });
            })
            .setNegativeButton("إلغاء", null)
            .show();
    }

    private void copyToClipboard(String text) {
        ClipboardManager clipboard = (ClipboardManager) getSystemService(CLIPBOARD_SERVICE);
        ClipData clip = ClipData.newPlainText("path", text);
        clipboard.setPrimaryClip(clip);
        Toast.makeText(this, "✅ تم النسخ", Toast.LENGTH_SHORT).show();
    }

    private void renameFile(FileItem file) {
        android.widget.EditText input = new android.widget.EditText(this);
        input.setText(file.getName());
        input.setTextColor(Color.WHITE);
        input.setHintTextColor(Color.parseColor("#66FFFFFF"));
        
        new AlertDialog.Builder(this)
            .setTitle("📝 إعادة تسمية")
            .setView(input)
            .setPositiveButton("حفظ", (d, w) -> {
                String newName = input.getText().toString().trim();
                if (!newName.isEmpty()) {
                    File f = new File(file.getPath());
                    File newFile = new File(f.getParent(), newName);
                    if (f.renameTo(newFile)) {
                        Toast.makeText(this, "✅ تم!", Toast.LENGTH_SHORT).show();
                        loadFiles(f.getParent());
                    } else {
                        Toast.makeText(this, "❌ فشل", Toast.LENGTH_SHORT).show();
                    }
                }
            })
            .setNegativeButton("إلغاء", null)
            .show();
    }

    private void showFileInfo(FileItem file) {
        String info = "📄 الاسم: " + file.getName() + "\\n"
            + "📁 المسار: " + file.getPath() + "\\n"
            + "📏 الحجم: " + file.getSizeFormatted() + "\\n"
            + "📅 التاريخ: " + file.getDateFormatted() + "\\n"
            + "🔒 مشفر: " + (file.isEncrypted() ? "نعم" : "لا") + "\\n"
            + "📁 مجلد: " + (file.isDirectory() ? "نعم" : "لا");

        new AlertDialog.Builder(this)
            .setTitle("ℹ️ معلومات الملف")
            .setMessage(info)
            .setPositiveButton("حسناً", null)
            .show();
    }

    private void deleteFile(FileItem file) {
        new AlertDialog.Builder(this)
            .setTitle("🗑️ تأكيد الحذف")
            .setMessage("هل أنت متأكد من حذف:\\n" + file.getName() + "\\n\\nلا يمكن التراجع!")
            .setIcon(android.R.drawable.ic_delete)
            .setPositiveButton("🗑️ حذف", (d, w) -> {
                File f = new File(file.getPath());
                boolean deleted;
                if (f.isDirectory()) {
                    deleted = deleteDirectory(f);
                } else {
                    deleted = f.delete();
                }
                if (deleted) {
                    Toast.makeText(this, "✅ تم الحذف", Toast.LENGTH_SHORT).show();
                    loadFiles(f.getParent());
                } else {
                    Toast.makeText(this, "❌ فشل الحذف", Toast.LENGTH_SHORT).show();
                }
            })
            .setNegativeButton("إلغاء", null)
            .show();
    }

    private boolean deleteDirectory(File dir) {
        if (dir.isDirectory()) {
            File[] children = dir.listFiles();
            if (children != null) {
                for (File child : children) {
                    deleteDirectory(child);
                }
            }
        }
        return dir.delete();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main_menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int id = item.getItemId();
        if (id == R.id.action_lock) {
            getSharedPreferences("FileVaultPrefs", MODE_PRIVATE)
                .edit().putBoolean("is_unlocked", false).apply();
            startActivity(new Intent(this, LockScreenActivity.class));
            finish();
        } else if (id == R.id.action_home) {
            loadFiles(Environment.getExternalStorageDirectory().getAbsolutePath());
        } else if (id == R.id.action_about) {
            new AlertDialog.Builder(this)
                .setTitle("💖 File Vault")
                .setMessage("إصدار 1.0\\n\\n🔐 تشفير AES-256\\n📱 واجهة واتساب\\n🎨 تصميم زهري\\n\\nZHARE © 2026")
                .setPositiveButton("💖", null)
                .show();
        }
        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onBackPressed() {
        if (currentPath != null) {
            File current = new File(currentPath);
            File parent = current.getParentFile();
            File root = Environment.getExternalStorageDirectory();
            if (parent != null && !currentPath.equals(root.getAbsolutePath()) && !currentPath.equals("/")) {
                loadFiles(parent.getAbsolutePath());
                return;
            }
        }
        super.onBackPressed();
    }
}
""")

    # FileViewerActivity.java (simple placeholder)
    write_file("app/src/main/java/com/zhare/filevault/ui/FileViewerActivity.java", """package com.zhare.filevault.ui;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import com.zhare.filevault.R;

/**
 * 💖 File Viewer Activity
 */
public class FileViewerActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_viewer);
    }
}
""")

    section("RESOURCES")

    # Colors
    write_file("app/src/main/res/values/colors.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="pink_primary">#EC4899</color>
    <color name="pink_secondary">#F472B6</color>
    <color name="pink_light">#FBCFE8</color>
    <color name="pink_dark">#BE185D</color>
    <color name="surface_dark">#0D0610</color>
    <color name="surface_darker">#08030A</color>
    <color name="white">#FFFFFF</color>
    <color name="text_primary">#FFFFFF</color>
    <color name="text_secondary">#99FFFFFF</color>
    <color name="text_hint">#44FFFFFF</color>
    <color name="success">#4ADE80</color>
    <color name="error">#F87171</color>
    <color name="warning">#FBBF24</color>
</resources>
""")

    # Themes
    write_file("app/src/main/res/values/themes.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.FileVault" parent="Theme.MaterialComponents.DayNight.NoActionBar">
        <item name="colorPrimary">@color/pink_primary</item>
        <item name="colorPrimaryVariant">@color/pink_secondary</item>
        <item name="colorOnPrimary">@color/white</item>
        <item name="colorSecondary">@color/pink_secondary</item>
        <item name="android:statusBarColor">@color/pink_primary</item>
        <item name="android:navigationBarColor">@color/surface_dark</item>
        <item name="android:windowBackground">@color/surface_dark</item>
        <item name="android:textColor">@color/text_primary</item>
    </style>
</resources>
""")

    # Strings
    write_file("app/src/main/res/values/strings.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">File Vault 💖</string>
</resources>
""")

    # Animations
    write_file("app/src/main/res/anim/shake.xml", """<?xml version="1.0" encoding="utf-8"?>
<translate xmlns:android="http://schemas.android.com/apk/res/android"
    android:fromXDelta="0" android:toXDelta="10"
    android:duration="100"
    android:interpolator="@android:anim/cycle_interpolator" />
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

    section("LAYOUT FILES")

    # Lock Screen
    write_file("app/src/main/res/layout/activity_lock.xml", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:background="@color/surface_dark"
    android:padding="32dp">

    <TextView
        android:layout_width="120dp"
        android:layout_height="120dp"
        android:text="💖"
        android:textSize="64sp"
        android:gravity="center"
        android:background="@drawable/bg_icon_circle"
        android:layout_marginBottom="24dp" />

    <TextView
        android:id="@+id/tvTitle"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="File Vault"
        android:textSize="28sp"
        android:textColor="@color/pink_primary"
        android:textStyle="bold"
        android:layout_marginBottom="8dp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="أدخل رمز الدخول للمتابعة"
        android:textSize="14sp"
        android:textColor="@color/text_secondary"
        android:layout_marginBottom="32dp" />

    <EditText
        android:id="@+id/etPassword"
        android:layout_width="260dp"
        android:layout_height="56dp"
        android:inputType="numberPassword"
        android:hint="🔒 ●●●●"
        android:textColor="@color/text_primary"
        android:textColorHint="@color/text_hint"
        android:background="@drawable/bg_input"
        android:paddingStart="20dp"
        android:paddingEnd="20dp"
        android:textAlignment="center"
        android:maxLength="4"
        android:textSize="24sp"
        android:letterSpacing="0.3"
        android:imeOptions="actionDone" />

    <Button
        android:id="@+id/btnUnlock"
        android:layout_width="260dp"
        android:layout_height="56dp"
        android:text="🔓 فتح التطبيق"
        android:textColor="@color/white"
        android:textSize="16sp"
        android:textStyle="bold"
        android:background="@drawable/bg_button"
        android:layout_marginTop="32dp"
        android:elevation="12dp"
        android:stateListAnimator="@null" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="ZHARE © 2026"
        android:textSize="11sp"
        android:textColor="@color/text_hint"
        android:layout_marginTop="48dp" />

</LinearLayout>
""")

    # Main Activity
    write_file("app/src/main/res/layout/activity_main.xml", """<?xml version="1.0" encoding="utf-8"?>
<androidx.coordinatorlayout.widget.CoordinatorLayout 
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/surface_dark"
    android:fitsSystemWindows="true">

    <com.google.android.material.appbar.AppBarLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:background="@color/pink_primary"
        android:fitsSystemWindows="true">

        <com.google.android.material.appbar.MaterialToolbar
            android:id="@+id/toolbar"
            android:layout_width="match_parent"
            android:layout_height="?attr/actionBarSize"
            app:navigationIcon="📁"
            app:titleTextColor="@color/white" />

        <TextView
            android:id="@+id/tvPath"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:textSize="11sp"
            android:textColor="#AAFFFFFF"
            android:paddingStart="16dp"
            android:paddingEnd="16dp"
            android:paddingBottom="4dp"
            android:maxLines="1"
            android:ellipsize="start" />

        <com.google.android.material.tabs.TabLayout
            android:id="@+id/tabLayout"
            android:layout_width="match_parent"
            android:layout_height="48dp"
            android:background="@color/pink_primary"
            app:tabTextColor="#CCFFFFFF"
            app:tabSelectedTextColor="@color/white"
            app:tabIndicatorColor="@color/white"
            app:tabIndicatorHeight="3dp"
            app:tabMode="scrollable" />

    </com.google.android.material.appbar.AppBarLayout>

    <androidx.swiperefreshlayout.widget.SwipeRefreshLayout
        android:id="@+id/swipeRefresh"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        app:layout_behavior="@string/appbar_scrolling_view_behavior">

        <FrameLayout
            android:layout_width="match_parent"
            android:layout_height="match_parent">

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
                android:textSize="16sp"
                android:textColor="@color/text_secondary"
                android:visibility="gone" />

        </FrameLayout>

    </androidx.swiperefreshlayout.widget.SwipeRefreshLayout>

    <com.google.android.material.floatingactionbutton.FloatingActionButton
        android:id="@+id/fabLock"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="bottom|end"
        android:layout_margin="24dp"
        android:src="🔒"
        android:contentDescription="قفل التطبيق"
        app:backgroundTint="@color/pink_primary"
        app:tint="@color/white"
        app:elevation="12dp"
        app:fabSize="normal" />

</androidx.coordinatorlayout.widget.CoordinatorLayout>
""")

    # File Item
    write_file("app/src/main/res/layout/item_file.xml", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="horizontal"
    android:padding="10dp"
    android:gravity="center_vertical"
    android:background="?attr/selectableItemBackground"
    android:minHeight="68dp">

    <TextView
        android:id="@+id/tvIcon"
        android:layout_width="48dp"
        android:layout_height="48dp"
        android:gravity="center"
        android:textSize="26sp"
        android:layout_marginEnd="12dp"
        android:background="@drawable/bg_icon_small"
        android:text="📄" />

    <LinearLayout
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_weight="1"
        android:orientation="vertical"
        android:layout_marginEnd="8dp">

        <TextView
            android:id="@+id/tvFileName"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:textColor="@color/text_primary"
            android:textSize="14sp"
            android:maxLines="1"
            android:ellipsize="end" />

        <TextView
            android:id="@+id/tvFileInfo"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:textColor="@color/text_secondary"
            android:textSize="11sp"
            android:layout_marginTop="3dp" />

    </LinearLayout>

    <TextView
        android:id="@+id/tvFileType"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:textColor="@color/text_hint"
        android:textSize="10sp"
        android:maxLines="1" />

</LinearLayout>
""")

    # Viewer Activity
    write_file("app/src/main/res/layout/activity_viewer.xml", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/surface_dark"
    android:gravity="center">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="💖 File Viewer"
        android:textSize="24sp"
        android:textColor="@color/pink_primary" />

</LinearLayout>
""")

    # Menu
    write_file("app/src/main/res/menu/main_menu.xml", """<?xml version="1.0" encoding="utf-8"?>
<menu xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto">

    <item
        android:id="@+id/action_home"
        android:title="🏠 الرئيسية"
        android:icon="@android:drawable/ic_menu_directions"
        app:showAsAction="ifRoom" />

    <item
        android:id="@+id/action_lock"
        android:title="🔒 قفل"
        android:icon="@android:drawable/ic_lock_lock"
        app:showAsAction="always" />

    <item
        android:id="@+id/action_about"
        android:title="💖 حول التطبيق"
        app:showAsAction="never" />

</menu>
""")

    # Drawables
    write_file("app/src/main/res/drawable/bg_input.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#1AEC4899" />
    <corners android:radius="28dp" />
    <stroke android:width="1.5dp" android:color="#33EC4899" />
</shape>
""")

    write_file("app/src/main/res/drawable/bg_button.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <gradient 
        android:startColor="#EC4899" 
        android:endColor="#F472B6" 
        android:angle="135"
        android:type="linear" />
    <corners android:radius="28dp" />
</shape>
""")

    write_file("app/src/main/res/drawable/bg_icon_circle.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="oval">
    <solid android:color="#1AEC4899" />
    <stroke android:width="2dp" android:color="#33EC4899" />
</shape>
""")

    write_file("app/src/main/res/drawable/bg_icon_small.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#0AEC4899" />
    <corners android:radius="12dp" />
</shape>
""")

    # Mipmap (simple placeholder icons)
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

    section("GITHUB ACTIONS")

    # Main workflow
    write_file(".github/workflows/main.yml", f"""name: 💖 Build File Vault APK

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

env:
  APPLICATION_ID: "{PACKAGE_NAME}"
  APP_NAME: "{PROJECT_NAME}"

jobs:
  build:
    name: 🏗️ Build APK
    runs-on: ubuntu-latest
    
    steps:
      - name: 📥 Checkout Repository
        uses: actions/checkout@v4
      
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
      
      - name: 🔧 Grant Execute Permission
        run: chmod +x gradlew
      
      - name: 🏗️ Build Release APK
        run: ./gradlew assembleRelease
      
      - name: 🏗️ Build Debug APK
        run: ./gradlew assembleDebug
      
      - name: 📦 Upload Release APK
        uses: actions/upload-artifact@v4
        with:
          name: ${{{{ env.APP_NAME }}}}-Release
          path: app/build/outputs/apk/release/*.apk
          retention-days: 30
      
      - name: 📦 Upload Debug APK
        uses: actions/upload-artifact@v4
        with:
          name: ${{{{ env.APP_NAME }}}}-Debug
          path: app/build/outputs/apk/debug/*.apk
          retention-days: 7

  release:
    name: 📦 Create Release
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master'
    
    steps:
      - name: 📥 Download APK
        uses: actions/download-artifact@v4
        with:
          name: ${{{{ env.APP_NAME }}}}-Release
          path: apk/
      
      - name: 🚀 Create Release
        uses: softprops/action-gh-release@v2
        with:
          name: "${{{{ env.APP_NAME }}}} 💖"
          tag_name: "v1.0-${{{{ github.run_number }}}}"
          body: |
            ## 💖 File Vault APK
            
            ### 🎯 المميزات:
            - 🔐 تشفير AES-256
            - 📱 واجهة واتساب
            - 🔒 كلمة سر: 1234
            - 📁 تصفح جميع الملفات
            
            ### 📥 التحميل:
            حمل ملف APK من الأسفل 👇
          files: apk/*.apk
          draft: false
          prerelease: false
        env:
          GITHUB_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}
""")

    # README
    write_file("README.md", f"""# 💖 {PROJECT_NAME}

<div align="center">

![Logo](https://img.shields.io/badge/💖-File_Vault-EC4899?style=for-the-badge)
![Platform](https://img.shields.io/badge/📱-Android-34A853?style=for-the-badge)
![License](https://img.shields.io/badge/📄-MIT-blue?style=for-the-badge)

</div>

---

## 📱 تطبيق أندرويد لإدارة وتشفير الملفات

### 🔐 المميزات:

| الميزة | الوصف |
|--------|-------|
| 🔒 **حماية** | كلمة سر `1234` لدخول التطبيق |
| 🔐 **تشفير** | AES-256 لتشفير الملفات |
| 📁 **تصفح** | جميع ملفات الذاكرة الداخلية والخارجية |
| 🎨 **تصميم** | واجهة تشبه واتساب + لون زهري |
| 📂 **تصنيف** | تبويبات (صور، فيديو، صوت، مشفر) |
| ⚡ **سرعة** | تحميل الملفات في خلفية منفصلة |

---

### 📥 التحميل:

1. اذهب إلى [**Actions**](../../actions)
2. اختر آخر **Build**
3. حمل **APK** من **Artifacts**

أو من [**Releases**](../../releases)

---

### 🚀 البناء من المصدر:

```bash
git clone https://github.com/jasim28v-cloud/Apkk.git
cd Apkk
./gradlew assembleRelease
