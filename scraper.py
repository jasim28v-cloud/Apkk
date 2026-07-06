#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                                                            ║
║  💖  FILE VAULT - Pink Rose Secure APK Builder  💖       ║
║     WhatsApp-Style UI + AES Encryption + GitHub Actions     ║
║                                                            ║
║  🔐  Password: 1234                                       ║
║  🎨  Theme: Pink Rose Glass                                ║
║  📁  File Manager + Encrypt/Decrypt                        ║
║                                                            ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import json
import shutil

# ═══════════════════════════════════════════════════════════
# 💖 CONFIGURATION
# ═══════════════════════════════════════════════════════════

PROJECT_NAME = "FileVault"
PACKAGE_NAME = "com.zhare.filevault"
APP_PASSWORD = "1234"
PRIMARY_COLOR = "#ec4899"
SECONDARY_COLOR = "#f472b6"

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

def section(title):
    print(f"\n{'='*60}")
    print(f"  💖 {title}")
    print(f"{'='*60}")

# ═══════════════════════════════════════════════════════════
# 💖 BUILD PROJECT
# ═══════════════════════════════════════════════════════════

def build_all():
    section("ANDROID PROJECT STRUCTURE")

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
""")

    # settings.gradle
    write_file("settings.gradle", f"""rootProject.name = "{PROJECT_NAME}"
include ':app'
""")

    # gradle.properties
    write_file("gradle.properties", """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true
""")

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
        versionCode 1
        versionName "1.0"
    }}

    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
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
    implementation 'com.google.code.gson:gson:2.10.1'
}}
""")

    # AndroidManifest.xml
    write_file("app/src/main/AndroidManifest.xml", f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{PACKAGE_NAME}">

    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
    <uses-permission android:name="android.permission.READ_MEDIA_VIDEO" />
    <uses-permission android:name="android.permission.READ_MEDIA_AUDIO" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="File Vault 💖"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.FileVault"
        android:requestLegacyExternalStorage="true">

        <activity
            android:name=".ui.LockScreenActivity"
            android:exported="true"
            android:theme="@style/Theme.FileVault">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <activity
            android:name=".ui.MainActivity"
            android:theme="@style/Theme.FileVault" />

        <activity
            android:name=".ui.FileViewerActivity"
            android:theme="@style/Theme.FileVault" />

    </application>
</manifest>
""")

    # ProGuard
    write_file("app/proguard-rules.pro", """-keep class com.zhare.filevault.** { *; }
-keep class javax.crypto.** { *; }
-keep class java.security.** { *; }
""")

    section("JAVA SOURCE FILES")

    # AES Encryption Helper
    write_file("app/src/main/java/com/zhare/filevault/crypto/AESHelper.java", f"""package com.zhare.filevault.crypto;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.security.MessageDigest;
import java.util.Base64;

public class AESHelper {{
    private static final String ALGORITHM = "AES";
    private static final String SECRET_KEY = "{APP_PASSWORD}";

    private static SecretKeySpec getSecretKey() throws Exception {{
        MessageDigest sha = MessageDigest.getInstance("SHA-256");
        byte[] key = sha.digest(SECRET_KEY.getBytes("UTF-8"));
        return new SecretKeySpec(key, ALGORITHM);
    }}

    public static byte[] encrypt(byte[] data) throws Exception {{
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, getSecretKey());
        return cipher.doFinal(data);
    }}

    public static byte[] decrypt(byte[] data) throws Exception {{
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, getSecretKey());
        return cipher.doFinal(data);
    }}

    public static String encryptToBase64(String text) {{
        try {{
            byte[] encrypted = encrypt(text.getBytes("UTF-8"));
            return Base64.getEncoder().encodeToString(encrypted);
        }} catch (Exception e) {{
            e.printStackTrace();
            return null;
        }}
    }}

    public static String decryptFromBase64(String encryptedText) {{
        try {{
            byte[] decoded = Base64.getDecoder().decode(encryptedText);
            byte[] decrypted = decrypt(decoded);
            return new String(decrypted, "UTF-8");
        }} catch (Exception e) {{
            e.printStackTrace();
            return null;
        }}
    }}

    public static byte[] encryptFile(byte[] fileData) throws Exception {{
        return encrypt(fileData);
    }}

    public static byte[] decryptFile(byte[] fileData) throws Exception {{
        return decrypt(fileData);
    }}
}}
""")

    # FileItem Model
    write_file("app/src/main/java/com/zhare/filevault/models/FileItem.java", """package com.zhare.filevault.models;

import java.io.File;

public class FileItem {
    private String name;
    private String path;
    private long size;
    private boolean isDirectory;
    private boolean isEncrypted;
    private String mimeType;

    public FileItem(File file) {
        this.name = file.getName();
        this.path = file.getAbsolutePath();
        this.size = file.length();
        this.isDirectory = file.isDirectory();
        this.isEncrypted = file.getName().endsWith(".enc");
        this.mimeType = getMimeType(file.getName());
    }

    private String getMimeType(String name) {
        String ext = name.substring(name.lastIndexOf(".") + 1).toLowerCase();
        switch (ext) {
            case "jpg": case "jpeg": return "🖼️ صورة";
            case "png": case "gif": return "🖼️ صورة";
            case "mp4": case "mkv": return "🎬 فيديو";
            case "mp3": case "wav": return "🎵 صوت";
            case "pdf": return "📄 PDF";
            case "doc": case "docx": return "📝 Word";
            case "apk": return "📦 APK";
            case "enc": return "🔒 مشفر";
            default: return "📁 ملف";
        }
    }

    public String getName() { return name; }
    public String getPath() { return path; }
    public long getSize() { return size; }
    public boolean isDirectory() { return isDirectory; }
    public boolean isEncrypted() { return isEncrypted; }
    public String getMimeType() { return mimeType; }

    public String getSizeFormatted() {
        if (size < 1024) return size + " B";
        if (size < 1024 * 1024) return String.format("%.1f KB", size / 1024.0);
        if (size < 1024 * 1024 * 1024) return String.format("%.1f MB", size / (1024.0 * 1024));
        return String.format("%.1f GB", size / (1024.0 * 1024 * 1024));
    }
}
""")

    # FileAdapter for RecyclerView
    write_file("app/src/main/java/com/zhare/filevault/ui/FileAdapter.java", """package com.zhare.filevault.ui;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.zhare.filevault.R;
import com.zhare.filevault.models.FileItem;
import java.util.List;

public class FileAdapter extends RecyclerView.Adapter<FileAdapter.ViewHolder> {
    private List<FileItem> files;
    private OnFileClickListener listener;

    public interface OnFileClickListener {
        void onFileClick(FileItem file);
        void onFileLongClick(FileItem file);
    }

    public FileAdapter(List<FileItem> files, OnFileClickListener listener) {
        this.files = files;
        this.listener = listener;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_file, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        FileItem file = files.get(position);
        holder.tvFileName.setText(file.getName());
        holder.tvFileType.setText(file.getMimeType());
        holder.tvFileSize.setText(file.getSizeFormatted());
        holder.ivIcon.setText(file.isDirectory() ? "📁" : file.getMimeType().substring(0, 2));

        holder.itemView.setOnClickListener(v -> listener.onFileClick(file));
        holder.itemView.setOnLongClickListener(v -> {
            listener.onFileLongClick(file);
            return true;
        });

        // Pink theme accent
        if (file.isEncrypted()) {
            holder.tvFileName.setTextColor(0xFFEC4899);
        }
    }

    @Override
    public int getItemCount() {
        return files.size();
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView ivIcon, tvFileName, tvFileType, tvFileSize;
        ViewHolder(View itemView) {
            super(itemView);
            ivIcon = itemView.findViewById(R.id.ivIcon);
            tvFileName = itemView.findViewById(R.id.tvFileName);
            tvFileType = itemView.findViewById(R.id.tvFileType);
            tvFileSize = itemView.findViewById(R.id.tvFileSize);
        }
    }

    public void updateList(List<FileItem> newFiles) {
        this.files = newFiles;
        notifyDataSetChanged();
    }
}
""")

    # LockScreenActivity (Password 1234)
    write_file(f"app/src/main/java/com/zhare/filevault/ui/LockScreenActivity.java", f"""package com.zhare.filevault.ui;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.zhare.filevault.R;

public class LockScreenActivity extends AppCompatActivity {{
    private static final String PREFS_NAME = "FileVaultPrefs";
    private static final String PASSWORD = "{APP_PASSWORD}";
    private EditText etPassword;
    private Button btnUnlock;
    private SharedPreferences prefs;
    private int failedAttempts = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_lock);

        // Set pink theme
        getWindow().setStatusBarColor(0xFFEC4899);

        prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);

        // Check if already unlocked
        if (prefs.getBoolean("is_unlocked", false)) {{
            openMain();
            return;
        }}

        etPassword = findViewById(R.id.etPassword);
        btnUnlock = findViewById(R.id.btnUnlock);

        btnUnlock.setOnClickListener(v -> {{
            String input = etPassword.getText().toString();
            if (input.equals(PASSWORD)) {{
                prefs.edit().putBoolean("is_unlocked", true).apply();
                Toast.makeText(this, "✅ مرحباً بك! 💖", Toast.LENGTH_SHORT).show();
                openMain();
            }} else {{
                failedAttempts++;
                etPassword.setError("❌ رمز خطأ!");
                if (failedAttempts >= 3) {{
                    Toast.makeText(this, "❌ كثرة المحاولات! انتظر 30 ثانية", Toast.LENGTH_LONG).show();
                    btnUnlock.setEnabled(false);
                    new android.os.Handler().postDelayed(() -> {{
                        btnUnlock.setEnabled(true);
                        failedAttempts = 0;
                    }}, 30000);
                }}
            }}
        }});
    }}

    @Override
    protected void onPause() {{
        super.onPause();
        prefs.edit().putBoolean("is_unlocked", false).apply();
    }}

    private void openMain() {{
        startActivity(new Intent(this, MainActivity.class));
        finish();
    }}
}}
""")

    # MainActivity (WhatsApp-like UI)
    write_file("app/src/main/java/com/zhare/filevault/ui/MainActivity.java", """package com.zhare.filevault.ui;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
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
import java.util.stream.Collectors;

public class MainActivity extends AppCompatActivity {
    private static final int STORAGE_PERMISSION = 100;
    private RecyclerView rvFiles;
    private FileAdapter adapter;
    private SwipeRefreshLayout swipeRefresh;
    private TabLayout tabLayout;
    private FloatingActionButton fabEncrypt;
    private List<FileItem> allFiles = new ArrayList<>();
    private String currentTab = "all";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Pink theme setup
        getWindow().setStatusBarColor(0xFFEC4899);

        MaterialToolbar toolbar = findViewById(R.id.toolbar);
        toolbar.setTitle("💖 File Vault");
        toolbar.setTitleTextColor(0xFFFFFFFF);
        toolbar.setBackgroundColor(0xFFEC4899);
        setSupportActionBar(toolbar);

        rvFiles = findViewById(R.id.rvFiles);
        swipeRefresh = findViewById(R.id.swipeRefresh);
        tabLayout = findViewById(R.id.tabLayout);
        fabEncrypt = findViewById(R.id.fabEncrypt);

        rvFiles.setLayoutManager(new LinearLayoutManager(this));
        adapter = new FileAdapter(allFiles, new FileAdapter.OnFileClickListener() {
            @Override
            public void onFileClick(FileItem file) {
                if (file.isDirectory()) {
                    loadFiles(file.getPath());
                } else {
                    openFile(file);
                }
            }
            @Override
            public void onFileLongClick(FileItem file) {
                showFileOptions(file);
            }
        });
        rvFiles.setAdapter(adapter);

        // Tabs (WhatsApp-like)
        tabLayout.addTab(tabLayout.newTab().setText("📁 الكل"));
        tabLayout.addTab(tabLayout.newTab().setText("🖼️ صور"));
        tabLayout.addTab(tabLayout.newTab().setText("🎬 فيديو"));
        tabLayout.addTab(tabLayout.newTab().setText("🔒 مشفر"));

        tabLayout.addOnTabSelectedListener(new TabLayout.OnTabSelectedListener() {
            @Override public void onTabSelected(TabLayout.Tab tab) {
                switch (tab.getPosition()) {
                    case 0: currentTab = "all"; break;
                    case 1: currentTab = "images"; break;
                    case 2: currentTab = "videos"; break;
                    case 3: currentTab = "encrypted"; break;
                }
                filterFiles();
            }
            @Override public void onTabUnselected(TabLayout.Tab tab) {}
            @Override public void onTabReselected(TabLayout.Tab tab) {}
        });

        swipeRefresh.setOnRefreshListener(() -> {
            loadFiles(Environment.getExternalStorageDirectory().getAbsolutePath());
            swipeRefresh.setRefreshing(false);
        });

        fabEncrypt.setOnClickListener(v -> {
            Toast.makeText(this, "🔒 اختر ملف لتشفيره (ضغطة طويلة)", Toast.LENGTH_SHORT).show();
        });

        // Request permissions
        requestStoragePermission();
    }

    private void requestStoragePermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            if (!Environment.isExternalStorageManager()) {
                Intent intent = new Intent(android.provider.Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION);
                intent.setData(Uri.parse("package:" + getPackageName()));
                startActivity(intent);
            } else {
                loadFiles(Environment.getExternalStorageDirectory().getAbsolutePath());
            }
        } else {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE)
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.READ_EXTERNAL_STORAGE, Manifest.permission.WRITE_EXTERNAL_STORAGE},
                    STORAGE_PERMISSION);
            } else {
                loadFiles(Environment.getExternalStorageDirectory().getAbsolutePath());
            }
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == STORAGE_PERMISSION && grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            loadFiles(Environment.getExternalStorageDirectory().getAbsolutePath());
        } else {
            Toast.makeText(this, "❌ نحتاج صلاحية الوصول للملفات", Toast.LENGTH_LONG).show();
        }
    }

    private void loadFiles(String path) {
        File dir = new File(path);
        allFiles.clear();
        if (dir.exists() && dir.isDirectory()) {
            File[] files = dir.listFiles();
            if (files != null) {
                // Show parent directory first
                if (!path.equals(Environment.getExternalStorageDirectory().getAbsolutePath())) {
                    File parent = dir.getParentFile();
                    if (parent != null) {
                        allFiles.add(new FileItem(parent) {
                            @Override
                            public String getName() { return "📁 .. (رجوع)"; }
                        });
                    }
                }
                for (File f : files) {
                    if (!f.isHidden()) {
                        allFiles.add(new FileItem(f));
                    }
                }
                // Sort: directories first, then files by name
                allFiles.sort((a, b) -> {
                    if (a.isDirectory() && !b.isDirectory()) return -1;
                    if (!a.isDirectory() && b.isDirectory()) return 1;
                    return a.getName().compareToIgnoreCase(b.getName());
                });
            }
        }
        filterFiles();
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
            Intent intent = new Intent(Intent.ACTION_VIEW);
            String mimeType = "*/*";
            String name = file.getName().toLowerCase();
            if (name.endsWith(".jpg") || name.endsWith(".png")) mimeType = "image/*";
            else if (name.endsWith(".mp4")) mimeType = "video/*";
            else if (name.endsWith(".mp3")) mimeType = "audio/*";
            else if (name.endsWith(".pdf")) mimeType = "application/pdf";
            
            intent.setDataAndType(Uri.fromFile(new File(file.getPath())), mimeType);
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            startActivity(intent);
        } catch (Exception e) {
            Toast.makeText(this, "❌ لا يمكن فتح الملف", Toast.LENGTH_SHORT).show();
        }
    }

    private void showFileOptions(FileItem file) {
        String[] options;
        if (file.isEncrypted()) {
            options = new String[]{"🔓 فك التشفير", "📋 نسخ المسار", "🗑️ حذف"};
        } else {
            options = new String[]{"🔒 تشفير", "📋 نسخ المسار", "🗑️ حذف"};
        }

        new androidx.appcompat.app.AlertDialog.Builder(this)
            .setTitle(file.getName())
            .setItems(options, (dialog, which) -> {
                switch (which) {
                    case 0:
                        if (file.isEncrypted()) {
                            decryptFile(file);
                        } else {
                            encryptFile(file);
                        }
                        break;
                    case 1:
                        copyToClipboard(file.getPath());
                        break;
                    case 2:
                        deleteFile(file);
                        break;
                }
            })
            .show();
    }

    private void encryptFile(FileItem file) {
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

            // Delete original
            f.delete();

            Toast.makeText(this, "✅ تم التشفير: " + encryptedFile.getName(), Toast.LENGTH_SHORT).show();
            loadFiles(f.getParent());
        } catch (Exception e) {
            Toast.makeText(this, "❌ فشل التشفير", Toast.LENGTH_SHORT).show();
            e.printStackTrace();
        }
    }

    private void decryptFile(FileItem file) {
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

            // Delete encrypted file
            f.delete();

            Toast.makeText(this, "✅ تم فك التشفير: " + decryptedFile.getName(), Toast.LENGTH_SHORT).show();
            loadFiles(decryptedFile.getParent());
        } catch (Exception e) {
            Toast.makeText(this, "❌ فشل فك التشفير - كلمة السر خطأ", Toast.LENGTH_SHORT).show();
            e.printStackTrace();
        }
    }

    private void deleteFile(FileItem file) {
        new androidx.appcompat.app.AlertDialog.Builder(this)
            .setTitle("🗑️ حذف")
            .setMessage("هل تريد حذف " + file.getName() + "؟")
            .setPositiveButton("نعم", (d, w) -> {
                File f = new File(file.getPath());
                if (f.delete()) {
                    Toast.makeText(this, "✅ تم الحذف", Toast.LENGTH_SHORT).show();
                    loadFiles(f.getParent());
                } else {
                    Toast.makeText(this, "❌ فشل الحذف", Toast.LENGTH_SHORT).show();
                }
            })
            .setNegativeButton("لا", null)
            .show();
    }

    private void copyToClipboard(String text) {
        android.content.ClipboardManager clipboard = (android.content.ClipboardManager) getSystemService(CLIPBOARD_SERVICE);
        android.content.ClipData clip = android.content.ClipData.newPlainText("path", text);
        clipboard.setPrimaryClip(clip);
        Toast.makeText(this, "✅ تم النسخ", Toast.LENGTH_SHORT).show();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main_menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        if (item.getItemId() == R.id.action_lock) {
            getSharedPreferences("FileVaultPrefs", MODE_PRIVATE).edit().putBoolean("is_unlocked", false).apply();
            startActivity(new Intent(this, LockScreenActivity.class));
            finish();
        } else if (item.getItemId() == R.id.action_settings) {
            Toast.makeText(this, "💖 File Vault v1.0", Toast.LENGTH_SHORT).show();
        }
        return super.onOptionsItemSelected(item);
    }
}
""")

    section("RESOURCES (XML LAYOUTS)")

    # Colors
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

    # Themes
    write_file("app/src/main/res/values/themes.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.FileVault" parent="Theme.MaterialComponents.DayNight.NoActionBar">
        <item name="colorPrimary">#EC4899</item>
        <item name="colorPrimaryVariant">#F472B6</item>
        <item name="colorOnPrimary">#FFFFFF</item>
        <item name="android:statusBarColor">#EC4899</item>
        <item name="android:navigationBarColor">#0D0610</item>
        <item name="android:windowBackground">#0D0610</item>
    </style>
</resources>
""")

    # Lock Screen Layout
    write_file("app/src/main/res/layout/activity_lock.xml", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:background="#0D0610"
    android:padding="32dp">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="💖"
        android:textSize="72sp"
        android:gravity="center"
        android:layout_marginBottom="16dp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="File Vault"
        android:textSize="28sp"
        android:textColor="#EC4899"
        android:textStyle="bold"
        android:layout_marginBottom="8dp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="أدخل رمز الدخول"
        android:textSize="14sp"
        android:textColor="#99FFFFFF"
        android:layout_marginBottom="24dp" />

    <EditText
        android:id="@+id/etPassword"
        android:layout_width="280dp"
        android:layout_height="56dp"
        android:inputType="numberPassword"
        android:hint="🔒 الرمز السري"
        android:textColor="#FFFFFF"
        android:textColorHint="#66FFFFFF"
        android:background="@drawable/bg_input"
        android:padding="16dp"
        android:textAlignment="center"
        android:maxLength="4"
        android:textSize="20sp" />

    <Button
        android:id="@+id/btnUnlock"
        android:layout_width="280dp"
        android:layout_height="56dp"
        android:text="🔓 فتح"
        android:textColor="#FFFFFF"
        android:textSize="16sp"
        android:textStyle="bold"
        android:background="@drawable/bg_button"
        android:layout_marginTop="24dp"
        android:elevation="8dp" />

</LinearLayout>
""")

    # Main Activity Layout
    write_file("app/src/main/res/layout/activity_main.xml", """<?xml version="1.0" encoding="utf-8"?>
<androidx.coordinatorlayout.widget.CoordinatorLayout xmlns:android="http://schemas.android.com/apk/res/android"
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
            android:layout_height="?attr/actionBarSize" />

        <com.google.android.material.tabs.TabLayout
            android:id="@+id/tabLayout"
            android:layout_width="match_parent"
            android:layout_height="48dp"
            android:background="#EC4899"
            app:tabTextColor="#CCFFFFFF"
            app:tabSelectedTextColor="#FFFFFF"
            app:tabIndicatorColor="#FFFFFF"
            app:tabMode="scrollable" />

    </com.google.android.material.appbar.AppBarLayout>

    <androidx.swiperefreshlayout.widget.SwipeRefreshLayout
        android:id="@+id/swipeRefresh"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        app:layout_behavior="@string/appbar_scrolling_view_behavior">

        <androidx.recyclerview.widget.RecyclerView
            android:id="@+id/rvFiles"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:padding="8dp"
            android:clipToPadding="false" />

    </androidx.swiperefreshlayout.widget.SwipeRefreshLayout>

    <com.google.android.material.floatingactionbutton.FloatingActionButton
        android:id="@+id/fabEncrypt"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="bottom|end"
        android:layout_margin="24dp"
        android:src="🔒"
        app:backgroundTint="#EC4899"
        app:tint="#FFFFFF"
        app:elevation="12dp" />

</androidx.coordinatorlayout.widget.CoordinatorLayout>
""")

    # File Item Layout
    write_file("app/src/main/res/layout/item_file.xml", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="horizontal"
    android:padding="12dp"
    android:gravity="center_vertical"
    android:background="?attr/selectableItemBackground"
    android:minHeight="72dp">

    <TextView
        android:id="@+id/ivIcon"
        android:layout_width="48dp"
        android:layout_height="48dp"
        android:gravity="center"
        android:textSize="24sp"
        android:layout_marginEnd="12dp" />

    <LinearLayout
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_weight="1"
        android:orientation="vertical">

        <TextView
            android:id="@+id/tvFileName"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:textColor="#FFFFFF"
            android:textSize="14sp"
            android:textStyle="bold"
            android:maxLines="1"
            android:ellipsize="end" />

        <LinearLayout
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:layout_marginTop="4dp">

            <TextView
                android:id="@+id/tvFileType"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:textColor="#AAFFFFFF"
                android:textSize="12sp" />

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text=" • "
                android:textColor="#66FFFFFF"
                android:textSize="12sp" />

            <TextView
                android:id="@+id/tvFileSize"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:textColor="#AAFFFFFF"
                android:textSize="12sp" />

        </LinearLayout>

    </LinearLayout>

    <TextView
        android:layout_width="24dp"
        android:layout_height="24dp"
        android:text="›"
        android:textColor="#66FFFFFF"
        android:textSize="18sp"
        android:gravity="center" />

</LinearLayout>
""")

    # Menu
    write_file("app/src/main/res/menu/main_menu.xml", """<?xml version="1.0" encoding="utf-8"?>
<menu xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto">

    <item
        android:id="@+id/action_lock"
        android:title="🔒 قفل"
        android:icon="@android:drawable/ic_lock_lock"
        app:showAsAction="always" />

    <item
        android:id="@+id/action_settings"
        android:title="ℹ️ حول"
        app:showAsAction="never" />

</menu>
""")

    # Drawables
    write_file("app/src/main/res/drawable/bg_input.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#1AEC4899" />
    <corners android:radius="28dp" />
    <stroke android:width="1dp" android:color="#33EC4899" />
</shape>
""")

    write_file("app/src/main/res/drawable/bg_button.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <gradient android:startColor="#EC4899" android:endColor="#F472B6" android:angle="135" />
    <corners android:radius="28dp" />
</shape>
""")

    section("GITHUB ACTIONS (CI/CD)")

    # GitHub Actions workflow to build APK
    write_file(".github/workflows/build-apk.yml", f"""name: Build Android APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

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
        key: gradle-${{{{ runner.os }}}}-${{{{ hashFiles('**/*.gradle*') }}}}

    - name: Grant execute permission for gradlew
      run: chmod +x gradlew

    - name: Build APK
      run: ./gradlew assembleRelease

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: {PROJECT_NAME}-APK
        path: app/build/outputs/apk/release/app-release-unsigned.apk
""")

    # README
    write_file("README.md", f"""# 💖 {PROJECT_NAME} - File Vault

## 📱 تطبيق أندرويد لإدارة وتشفير الملفات

### 🔐 المميزات:
- واجهة تشبه واتساب (Tabs + قائمة)
- تصفح جميع ملفات الذاكرة الداخلية والخارجية
- تشفير AES-256 للملفات
- حماية بكلمة سر `1234`
- تصنيف الملفات (صور، فيديو، مشفر)
- تصميم زهري فخم

### 🚀 البناء التلقائي:
يتم بناء APK تلقائياً عبر GitHub Actions عند كل push.

### 📥 التحميل:
1. اذهب إلى **Actions** في المستودع
2. اختر آخر **Build**
3. حمّل ملف **APK** من **Artifacts**

### 💖 ZHARE ❤️
""")

    print(f"""
{'='*60}
  💖 FILE VAULT PROJECT GENERATED! ✨
{'='*60}

  📊 Stats: {TOTAL_FILES} files | {TOTAL_LINES}+ lines

  📁 Project: {PROJECT_NAME}/

  🚀 To build locally:
     cd {PROJECT_NAME}
     ./gradlew assembleRelease

  📦 APK output:
     app/build/outputs/apk/release/app-release.apk

  🔐 Password: 1234

  💖 Push to GitHub → Actions will auto-build APK!
{'='*60}
""")

# ═══════════════════════════════════════════════════════════
# 💖 MAIN
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║  💖  FILE VAULT - Pink Rose APK Builder  ✨         ║
║     WhatsApp UI + AES Encryption + GitHub Actions       ║
╚══════════════════════════════════════════════════════════╝
    """)
    build_all()
