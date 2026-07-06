#!/usr/bin/env python3
"""
FILE VAULT - WhatsApp-Style Secret File Manager
AES-256 Encryption | Password: 1234
Files appear CORRUPTED outside the app
"""

import os
import urllib.request

PROJECT_NAME = "FileVault"
PACKAGE_NAME = "com.zhare.filevault"
ROOT_DIR = os.path.join(os.getcwd(), PROJECT_NAME)

TOTAL_FILES = 0
TOTAL_LINES = 0

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

def build_all():
    section("ROOT BUILD FILES")

    write_file("settings.gradle", f'rootProject.name = "{PROJECT_NAME}"\ninclude ":app"\n')

    write_file("build.gradle", """buildscript {
    repositories { google(); mavenCentral() }
    dependencies { classpath "com.android.tools.build:gradle:8.2.0" }
}
allprojects { repositories { google(); mavenCentral() } }
""")

    write_file("gradle.properties", "org.gradle.jvmargs=-Xmx2048m\nandroid.useAndroidX=true\nandroid.nonTransitiveRClass=true\n")

    write_file(".gitignore", "*.iml\n.gradle\n.idea\n/build\n*.apk\n*.jks\n")

    write_file("gradlew", '#!/bin/sh\nexec java -classpath "$(dirname "$0")/gradle/wrapper/gradle-wrapper.jar" org.gradle.wrapper.GradleWrapperMain "$@"\n')
    os.chmod(os.path.join(ROOT_DIR, "gradlew"), 0o755)

    write_file("gradlew.bat", '@echo off\njava -classpath "%~dp0\\gradle\\wrapper\\gradle-wrapper.jar" org.gradle.wrapper.GradleWrapperMain %*\n')

    write_file("gradle/wrapper/gradle-wrapper.properties", "distributionUrl=https\\://services.gradle.org/distributions/gradle-8.2-bin.zip\n")

    print("  📥 Downloading gradle-wrapper.jar...")
    try:
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/gradle/gradle/v8.2.0/gradle/wrapper/gradle-wrapper.jar",
            os.path.join(ROOT_DIR, "gradle/wrapper/gradle-wrapper.jar")
        )
        TOTAL_FILES += 1
        print("  ✅ gradle-wrapper.jar downloaded")
    except Exception as e:
        print(f"  ⚠️ Could not download: {e}")

    section("APP BUILD FILE")

    write_file("app/build.gradle", f"""plugins {{ id "com.android.application" }}

android {{
    namespace "{PACKAGE_NAME}"
    compileSdk 34
    defaultConfig {{
        applicationId "{PACKAGE_NAME}"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }}
    buildTypes {{
        release {{ minifyEnabled false }}
    }}
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }}
}}

dependencies {{
    implementation "androidx.appcompat:appcompat:1.6.1"
    implementation "com.google.android.material:material:1.11.0"
    implementation "androidx.recyclerview:recyclerview:1.3.2"
    implementation "androidx.swiperefreshlayout:swiperefreshlayout:1.1.0"
}}
""")

    section("ANDROID MANIFEST")

    write_file("app/src/main/AndroidManifest.xml", f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE" />
    <application android:allowBackup="true" android:label="File Vault 💖" android:theme="@style/Theme.FileVault" android:requestLegacyExternalStorage="true">
        <activity android:name=".ui.LockScreenActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        <activity android:name=".ui.ChatScreenActivity" />
        <activity android:name=".ui.FileManagerActivity" />
    </application>
</manifest>
""")

    section("JAVA - CRYPTO")

    write_file("app/src/main/java/com/zhare/filevault/crypto/AESHelper.java", """package com.zhare.filevault.crypto;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.security.MessageDigest;

public class AESHelper {
    private static final String SECRET = "1234";

    private static SecretKeySpec getKey() throws Exception {
        MessageDigest sha = MessageDigest.getInstance("SHA-256");
        return new SecretKeySpec(sha.digest(SECRET.getBytes("UTF-8")), "AES");
    }

    public static byte[] encrypt(byte[] data) throws Exception {
        Cipher c = Cipher.getInstance("AES/ECB/PKCS5Padding");
        c.init(Cipher.ENCRYPT_MODE, getKey());
        return c.doFinal(data);
    }

    public static byte[] decrypt(byte[] data) throws Exception {
        Cipher c = Cipher.getInstance("AES/ECB/PKCS5Padding");
        c.init(Cipher.DECRYPT_MODE, getKey());
        return c.doFinal(data);
    }

    public static byte[] encryptFile(byte[] d) throws Exception { return encrypt(d); }
    public static byte[] decryptFile(byte[] d) throws Exception { return decrypt(d); }
}
""")

    section("JAVA - MODELS")

    write_file("app/src/main/java/com/zhare/filevault/models/FileItem.java", """package com.zhare.filevault.models;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class FileItem {
    private String name, path, type;
    private long size, mod;
    private boolean dir, enc;

    public FileItem(File f) {
        name = f.getName();
        path = f.getAbsolutePath();
        size = f.length();
        dir = f.isDirectory();
        enc = name.toLowerCase().endsWith(".vault");
        mod = f.lastModified();
        type = getType();
    }

    private String getType() {
        if (dir) return "📁 مجلد";
        String n = name.toLowerCase();
        if (n.matches(".*\\.(jpg|png|gif)$")) return "🖼️ صورة";
        if (n.matches(".*\\.(mp4|mkv)$")) return "🎬 فيديو";
        if (n.matches(".*\\.(mp3|wav)$")) return "🎵 صوت";
        if (n.endsWith(".pdf")) return "📄 PDF";
        if (n.endsWith(".apk")) return "📦 APK";
        if (n.endsWith(".vault")) return "🔒 مشفر";
        return "📄 ملف";
    }

    public String getName() { return name; }
    public String getPath() { return path; }
    public long getSize() { return size; }
    public boolean isDirectory() { return dir; }
    public boolean isEncrypted() { return enc; }
    public String getType() { return type; }

    public String getSizeFmt() {
        if (dir) return "";
        if (size < 1024) return size + " B";
        if (size < 1048576) return String.format("%.1f KB", size / 1024.0);
        return String.format("%.1f MB", size / 1048576.0);
    }

    public String getDate() {
        return new SimpleDateFormat("yyyy/MM/dd HH:mm", Locale.getDefault()).format(new Date(mod));
    }
}
""")

    write_file("app/src/main/java/com/zhare/filevault/models/ChatItem.java", """package com.zhare.filevault.models;

public class ChatItem {
    private String message, time;
    private boolean sent;

    public ChatItem(String message, boolean sent) {
        this.message = message;
        this.sent = sent;
        this.time = java.text.SimpleDateFormat.getTimeInstance(
            java.text.DateFormat.SHORT, java.util.Locale.getDefault()
        ).format(new java.util.Date());
    }

    public String getMessage() { return message; }
    public String getTime() { return time; }
    public boolean isSent() { return sent; }
}
""")

    section("JAVA - ADAPTERS")

    write_file("app/src/main/java/com/zhare/filevault/ui/FileAdapter.java", """package com.zhare.filevault.ui;

import android.graphics.Color;
import android.view.*;
import android.widget.TextView;
import androidx.recyclerview.widget.RecyclerView;
import com.zhare.filevault.R;
import com.zhare.filevault.models.FileItem;
import java.util.*;

public class FileAdapter extends RecyclerView.Adapter<FileAdapter.VH> {
    private List<FileItem> list = new ArrayList<>();
    private Click c;

    interface Click {
        void onClick(FileItem f);
        void onLong(FileItem f);
    }

    public FileAdapter(Click c) { this.c = c; }

    static class VH extends RecyclerView.ViewHolder {
        TextView icon, name, info;
        VH(View v) {
            super(v);
            icon = v.findViewById(R.id.tvIcon);
            name = v.findViewById(R.id.tvName);
            info = v.findViewById(R.id.tvInfo);
        }
    }

    @Override public VH onCreateViewHolder(ViewGroup p, int t) {
        return new VH(LayoutInflater.from(p.getContext()).inflate(R.layout.item_file, p, false));
    }

    @Override public void onBindViewHolder(VH h, int i) {
        FileItem f = list.get(i);
        h.icon.setText(f.isDirectory() ? "📁" : f.isEncrypted() ? "🔒" : "📄");
        h.name.setText(f.getName());
        h.name.setTextColor(f.isEncrypted() ? Color.parseColor("#EC4899") : Color.WHITE);
        h.info.setText(f.getDate() + (f.getSizeFmt().isEmpty() ? "" : " • " + f.getSizeFmt()));
        h.itemView.setOnClickListener(v -> c.onClick(f));
        h.itemView.setOnLongClickListener(v -> { c.onLong(f); return true; });
    }

    @Override public int getItemCount() { return list.size(); }
    public void update(List<FileItem> l) { list = l; notifyDataSetChanged(); }
}
""")

    write_file("app/src/main/java/com/zhare/filevault/ui/ChatAdapter.java", """package com.zhare.filevault.ui;

import android.graphics.Color;
import android.view.*;
import android.widget.FrameLayout;
import android.widget.TextView;
import androidx.recyclerview.widget.RecyclerView;
import com.zhare.filevault.R;
import com.zhare.filevault.models.ChatItem;
import java.util.*;

public class ChatAdapter extends RecyclerView.Adapter<ChatAdapter.VH> {
    private List<ChatItem> list = new ArrayList<>();

    static class VH extends RecyclerView.ViewHolder {
        FrameLayout bubble;
        TextView msg, time;
        VH(View v) {
            super(v);
            bubble = v.findViewById(R.id.bubble);
            msg = v.findViewById(R.id.tvMessage);
            time = v.findViewById(R.id.tvTime);
        }
    }

    @Override public VH onCreateViewHolder(ViewGroup p, int t) {
        return new VH(LayoutInflater.from(p.getContext()).inflate(R.layout.item_chat, p, false));
    }

    @Override public void onBindViewHolder(VH h, int i) {
        ChatItem m = list.get(i);
        h.msg.setText(m.getMessage());
        h.time.setText(m.getTime());
        FrameLayout.LayoutParams lp = (FrameLayout.LayoutParams) h.bubble.getLayoutParams();
        if (m.isSent()) {
            h.bubble.setBackgroundResource(R.drawable.bg_chat_sent);
            lp.gravity = android.view.Gravity.END;
        } else {
            h.bubble.setBackgroundResource(R.drawable.bg_chat_received);
            lp.gravity = android.view.Gravity.START;
        }
        h.bubble.setLayoutParams(lp);
    }

    @Override public int getItemCount() { return list.size(); }
    public void add(ChatItem m) { list.add(m); notifyItemInserted(list.size() - 1); }
    public void setList(List<ChatItem> l) { list = l; notifyDataSetChanged(); }
}
""")

    section("JAVA - ACTIVITIES")

    write_file("app/src/main/java/com/zhare/filevault/ui/LockScreenActivity.java", """package com.zhare.filevault.ui;

import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;
import com.zhare.filevault.R;

public class LockScreenActivity extends AppCompatActivity {
    private EditText et;
    private int fail = 0;

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        getWindow().setStatusBarColor(Color.parseColor("#EC4899"));
        setContentView(R.layout.activity_lock);

        SharedPreferences p = getSharedPreferences("v", MODE_PRIVATE);
        if (p.getBoolean("u", false) && !getIntent().getBooleanExtra("force", false)) {
            open();
            return;
        }

        et = findViewById(R.id.etPass);
        findViewById(R.id.btnGo).setOnClickListener(v -> check());
    }

    private void check() {
        if (et.getText().toString().equals("1234")) {
            getSharedPreferences("v", MODE_PRIVATE).edit().putBoolean("u", true).apply();
            Toast.makeText(this, "✅ مرحباً!", Toast.LENGTH_SHORT).show();
            open();
        } else {
            fail++;
            et.setError("❌ خطأ " + fail + "/3");
            if (fail >= 3) {
                findViewById(R.id.btnGo).setEnabled(false);
                new android.os.Handler().postDelayed(() -> {
                    findViewById(R.id.btnGo).setEnabled(true);
                    fail = 0;
                }, 30000);
            }
        }
    }

    private void open() {
        startActivity(new Intent(this, ChatScreenActivity.class));
        finish();
    }

    @Override
    protected void onPause() {
        super.onPause();
        getSharedPreferences("v", MODE_PRIVATE).edit().putBoolean("u", false).apply();
    }
}
""")

    write_file("app/src/main/java/com/zhare/filevault/ui/ChatScreenActivity.java", """package com.zhare.filevault.ui;

import android.content.Intent;
import android.graphics.Color;
import android.os.*;
import android.provider.Settings;
import android.net.Uri;
import android.view.View;
import android.widget.*;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.zhare.filevault.R;
import com.zhare.filevault.models.ChatItem;
import java.util.*;

public class ChatScreenActivity extends AppCompatActivity {
    private RecyclerView rv;
    private ChatAdapter ad;
    private EditText et;
    private List<ChatItem> msgs = new ArrayList<>();

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        getWindow().setStatusBarColor(Color.parseColor("#EC4899"));
        setContentView(R.layout.activity_chat);

        rv = findViewById(R.id.rvChat);
        rv.setLayoutManager(new LinearLayoutManager(this));
        ad = new ChatAdapter();
        rv.setAdapter(ad);

        et = findViewById(R.id.etMessage);
        findViewById(R.id.btnSend).setOnClickListener(v -> send());
        findViewById(R.id.btnFiles).setOnClickListener(v -> openFiles());
        findViewById(R.id.btnLock).setOnClickListener(v -> lock());

        welcome();
    }

    private void welcome() {
        addSys("💖 مرحباً بك في File Vault!");
        addSys("📁 ملفاتك محمية بتشفير AES-256");
        addSys("🔒 الملفات تظهر مشوهة خارج التطبيق");
        addSys("📋 /files - فتح الملفات | /lock - قفل");
    }

    private void send() {
        String t = et.getText().toString().trim();
        if (t.isEmpty()) return;
        ad.add(new ChatItem(t, true));
        et.setText("");
        rv.scrollToPosition(msgs.size() - 1);

        if (t.equals("/files") || t.contains("فتح")) openFiles();
        else if (t.equals("/lock") || t.contains("قفل")) lock();
        else if (t.equals("/help")) {
            addSys("/files - فتح الملفات");
            addSys("/lock - قفل التطبيق");
        }
    }

    private void addSys(String m) {
        ChatItem c = new ChatItem(m, false);
        msgs.add(c);
        ad.add(c);
    }

    private void openFiles() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            if (!Environment.isExternalStorageManager()) {
                new AlertDialog.Builder(this)
                    .setTitle("💖 صلاحية")
                    .setMessage("نحتاج صلاحية الوصول للملفات")
                    .setPositiveButton("منح", (d, w) -> {
                        Intent i = new Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION);
                        i.setData(Uri.parse("package:" + getPackageName()));
                        startActivity(i);
                    })
                    .setNegativeButton("إلغاء", null).show();
                return;
            }
        }
        startActivity(new Intent(this, FileManagerActivity.class));
    }

    private void lock() {
        getSharedPreferences("v", MODE_PRIVATE).edit().putBoolean("u", false).apply();
        Intent i = new Intent(this, LockScreenActivity.class);
        i.putExtra("force", true);
        i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(i);
        finish();
    }
}
""")

    write_file("app/src/main/java/com/zhare/filevault/ui/FileManagerActivity.java", """package com.zhare.filevault.ui;

import android.Manifest;
import android.content.*;
import android.graphics.Color;
import android.net.Uri;
import android.os.*;
import android.provider.Settings;
import android.view.View;
import android.widget.*;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.zhare.filevault.R;
import com.zhare.filevault.crypto.AESHelper;
import com.zhare.filevault.models.FileItem;
import java.io.*;
import java.util.*;
import java.util.concurrent.*;

public class FileManagerActivity extends AppCompatActivity {
    private RecyclerView rv;
    private FileAdapter ad;
    private TextView tvPath;
    private List<FileItem> all = new ArrayList<>();
    private String curPath;
    private ExecutorService ex = Executors.newSingleThreadExecutor();
    private Handler h = new Handler(Looper.getMainLooper());

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        getWindow().setStatusBarColor(Color.parseColor("#EC4899"));
        setContentView(R.layout.activity_files);

        tvPath = findViewById(R.id.tvPath);
        rv = findViewById(R.id.rvFiles);
        rv.setLayoutManager(new LinearLayoutManager(this));

        ad = new FileAdapter(new FileAdapter.Click() {
            public void onClick(FileItem f) {
                if (f.isDirectory()) load(f.getPath());
                else if (f.isEncrypted()) {
                    new AlertDialog.Builder(FileManagerActivity.this)
                        .setTitle("🔒 مشفر").setMessage("فك التشفير؟")
                        .setPositiveButton("فك", (d, w) -> dec(f))
                        .setNegativeButton("لا", null).show();
                } else {
                    try {
                        Intent i = new Intent(Intent.ACTION_VIEW);
                        i.setDataAndType(Uri.fromFile(new File(f.getPath())), "*/*");
                        startActivity(i);
                    } catch (Exception e) {
                        toast("❌ لا يمكن فتح الملف");
                    }
                }
            }

            public void onLong(FileItem f) {
                String[] opts = f.isEncrypted() ? new String[]{"🔓 فك", "🗑️ حذف"} :
                    f.isDirectory() ? new String[]{"📁 فتح"} :
                    new String[]{"🔒 تشفير", "🗑️ حذف"};
                new AlertDialog.Builder(FileManagerActivity.this)
                    .setTitle(f.getName())
                    .setItems(opts, (d, w) -> {
                        if (opts[w].contains("تشفير")) enc(f);
                        else if (opts[w].contains("فك")) dec(f);
                        else if (opts[w].contains("حذف")) del(f);
                        else if (opts[w].contains("فتح")) load(f.getPath());
                    }).show();
            }
        });
        rv.setAdapter(ad);

        findViewById(R.id.fabLock).setOnClickListener(v -> {
            getSharedPreferences("v", MODE_PRIVATE).edit().putBoolean("u", false).apply();
            Intent i = new Intent(this, LockScreenActivity.class);
            i.putExtra("force", true);
            startActivity(i);
            finish();
        });

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            if (!Environment.isExternalStorageManager()) {
                startActivity(new Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
                    .setData(Uri.parse("package:" + getPackageName())));
            } else load(Environment.getExternalStorageDirectory().getAbsolutePath());
        } else {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE)
                    != PackageManager.PERMISSION_GRANTED) {
                requestPermissions(new String[]{Manifest.permission.READ_EXTERNAL_STORAGE,
                    Manifest.permission.WRITE_EXTERNAL_STORAGE}, 100);
            } else load(Environment.getExternalStorageDirectory().getAbsolutePath());
        }
    }

    private void load(String path) {
        ex.execute(() -> {
            File d = new File(path);
            List<FileItem> list = new ArrayList<>();
            if (d.exists()) {
                File p = d.getParentFile();
                if (p != null) list.add(new FileItem(p) {
                    public String getName() { return "📁 .."; }
                });
                File[] fs = d.listFiles();
                if (fs != null) for (File f : fs) if (!f.isHidden()) list.add(new FileItem(f));
                list.sort((a, b) -> {
                    if (a.isDirectory() && !b.isDirectory()) return -1;
                    if (!a.isDirectory() && b.isDirectory()) return 1;
                    return a.getName().compareToIgnoreCase(b.getName());
                });
            }
            h.post(() -> { curPath = path; all = list; tvPath.setText("📂 " + path); ad.update(list); });
        });
    }

    private void enc(FileItem fi) {
        ex.execute(() -> {
            try {
                File f = new File(fi.getPath());
                byte[] d = new byte[(int) f.length()];
                new FileInputStream(f).read(d);
                byte[] ed = AESHelper.encryptFile(d);
                FileOutputStream fo = new FileOutputStream(fi.getPath() + ".vault");
                fo.write(ed); fo.close();
                f.delete();
                h.post(() -> { toast("✅ تم التشفير"); load(f.getParent()); });
            } catch (Exception e) { h.post(() -> toast("❌ فشل")); }
        });
    }

    private void dec(FileItem fi) {
        ex.execute(() -> {
            try {
                File f = new File(fi.getPath());
                byte[] d = new byte[(int) f.length()];
                new FileInputStream(f).read(d);
                byte[] dd = AESHelper.decryptFile(d);
                FileOutputStream fo = new FileOutputStream(fi.getPath().replace(".vault", ""));
                fo.write(dd); fo.close();
                f.delete();
                h.post(() -> { toast("✅ تم فك التشفير"); load(f.getParent()); });
            } catch (Exception e) { h.post(() -> toast("❌ فشل")); }
        });
    }

    private void del(FileItem fi) {
        new AlertDialog.Builder(this)
            .setTitle("🗑️ حذف").setMessage("حذف " + fi.getName() + "؟")
            .setPositiveButton("نعم", (d, w) -> {
                if (new File(fi.getPath()).delete()) {
                    toast("✅ تم");
                    load(new File(fi.getPath()).getParent());
                } else toast("❌ فشل");
            }).setNegativeButton("لا", null).show();
    }

    private void toast(String m) { Toast.makeText(this, m, Toast.LENGTH_SHORT).show(); }

    @Override
    public void onBackPressed() {
        if (curPath != null) {
            File p = new File(curPath).getParentFile();
            if (p != null) { load(p.getAbsolutePath()); return; }
        }
        super.onBackPressed();
    }
}
""")

    section("XML LAYOUTS")

    write_file("app/src/main/res/layout/activity_lock.xml", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent" android:layout_height="match_parent"
    android:gravity="center" android:background="#0D0610"
    android:orientation="vertical" android:padding="32dp">
    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:text="💖" android:textSize="72sp" android:layout_marginBottom="16dp"/>
    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:text="File Vault" android:textSize="28sp" android:textColor="#EC4899" android:textStyle="bold"/>
    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:text="أدخل رمز الدخول" android:textColor="#99FFFFFF" android:textSize="14sp"
        android:layout_marginTop="8dp" android:layout_marginBottom="24dp"/>
    <EditText android:id="@+id/etPass" android:layout_width="260dp" android:layout_height="56dp"
        android:inputType="numberPassword" android:hint="🔒 ●●●●" android:textColor="#FFFFFF"
        android:background="@drawable/bg_input" android:textAlignment="center"
        android:maxLength="6" android:textSize="22sp"/>
    <Button android:id="@+id/btnGo" android:layout_width="260dp" android:layout_height="56dp"
        android:text="🔓 فتح" android:textColor="#FFFFFF" android:textStyle="bold"
        android:background="@drawable/bg_btn" android:layout_marginTop="32dp"/>
</LinearLayout>
""")

    write_file("app/src/main/res/layout/activity_chat.xml", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent" android:layout_height="match_parent"
    android:orientation="vertical" android:background="#0D0610">
    <LinearLayout android:layout_width="match_parent" android:layout_height="56dp"
        android:background="#EC4899" android:gravity="center_vertical"
        android:paddingStart="16dp" android:paddingEnd="8dp" android:orientation="horizontal">
        <TextView android:layout_width="0dp" android:layout_height="wrap_content"
            android:layout_weight="1" android:text="💖 File Vault" android:textColor="#FFFFFF"
            android:textSize="18sp" android:textStyle="bold"/>
        <ImageButton android:id="@+id/btnFiles" android:layout_width="40dp"
            android:layout_height="40dp" android:src="📂"
            android:background="?attr/selectableItemBackgroundBorderless"/>
        <ImageButton android:id="@+id/btnLock" android:layout_width="40dp"
            android:layout_height="40dp" android:src="🔒"
            android:background="?attr/selectableItemBackgroundBorderless"/>
    </LinearLayout>
    <androidx.recyclerview.widget.RecyclerView android:id="@+id/rvChat"
        android:layout_width="match_parent" android:layout_height="0dp"
        android:layout_weight="1" android:padding="12dp"/>
    <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content"
        android:orientation="horizontal" android:gravity="center_vertical"
        android:padding="8dp" android:background="#1A0D0610">
        <EditText android:id="@+id/etMessage" android:layout_width="0dp"
            android:layout_height="48dp" android:layout_weight="1"
            android:hint="💬 اكتب رسالة..." android:textColor="#FFFFFF"
            android:textColorHint="#66FFFFFF" android:background="@drawable/bg_input_chat"
            android:paddingStart="16dp" android:paddingEnd="16dp" android:maxLines="3"/>
        <ImageButton android:id="@+id/btnSend" android:layout_width="48dp"
            android:layout_height="48dp" android:src="📤"
            android:background="@drawable/bg_send_btn" android:layout_marginStart="8dp"/>
    </LinearLayout>
</LinearLayout>
""")

    write_file("app/src/main/res/layout/activity_files.xml", """<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent" android:layout_height="match_parent"
    android:background="#0D0610">
    <LinearLayout android:layout_width="match_parent" android:layout_height="match_parent"
        android:orientation="vertical">
        <LinearLayout android:layout_width="match_parent" android:layout_height="56dp"
            android:background="#EC4899" android:gravity="center_vertical"
            android:paddingStart="16dp" android:paddingEnd="8dp">
            <TextView android:id="@+id/tvPath" android:layout_width="match_parent"
                android:layout_height="wrap_content" android:text="📂 الملفات"
                android:textColor="#FFFFFF" android:textSize="14sp"/>
        </LinearLayout>
        <androidx.recyclerview.widget.RecyclerView android:id="@+id/rvFiles"
            android:layout_width="match_parent" android:layout_height="0dp"
            android:layout_weight="1" android:padding="4dp"/>
    </LinearLayout>
    <com.google.android.material.floatingactionbutton.FloatingActionButton
        android:id="@+id/fabLock" android:layout_width="wrap_content"
        android:layout_height="wrap_content" android:layout_gravity="bottom|end"
        android:layout_margin="20dp" android:text="🔒"
        app:backgroundTint="#EC4899" app:tint="#FFFFFF"/>
</FrameLayout>
""")

    write_file("app/src/main/res/layout/item_file.xml", """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent" android:layout_height="wrap_content"
    android:orientation="horizontal" android:padding="10dp"
    android:gravity="center_vertical" android:minHeight="64dp"
    android:background="?attr/selectableItemBackground">
    <TextView android:id="@+id/tvIcon" android:layout_width="44dp"
        android:layout_height="44dp" android:gravity="center"
        android:textSize="24sp" android:layout_marginEnd="10dp" android:text="📄"/>
    <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content"
        android:layout_weight="1" android:orientation="vertical">
        <TextView android:id="@+id/tvName" android:textColor="#FFFFFF"
            android:textSize="14sp" android:maxLines="1"/>
        <TextView android:id="@+id/tvInfo" android:textColor="#99FFFFFF"
            android:textSize="11sp" android:layout_marginTop="2dp"/>
    </LinearLayout>
</LinearLayout>
""")

    write_file("app/src/main/res/layout/item_chat.xml", """<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent" android:layout_height="wrap_content"
    android:paddingStart="16dp" android:paddingEnd="16dp"
    android:paddingTop="4dp" android:paddingBottom="4dp">
    <LinearLayout android:id="@+id/bubble" android:layout_width="wrap_content"
        android:layout_height="wrap_content" android:maxWidth="280dp"
        android:orientation="vertical" android:padding="12dp">
        <TextView android:id="@+id/tvMessage" android:layout_width="wrap_content"
            android:layout_height="wrap_content" android:textSize="14sp" android:textColor="#FFFFFF"/>
        <TextView android:id="@+id/tvTime" android:layout_width="wrap_content"
            android:layout_height="wrap_content" android:textSize="10sp"
            android:textColor="#99FFFFFF" android:layout_marginTop="4dp" android:layout_gravity="end"/>
    </LinearLayout>
</FrameLayout>
""")

    section("DRAWABLES")

    write_file("app/src/main/res/drawable/bg_input.xml", '<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle"><solid android:color="#1AEC4899"/><corners android:radius="28dp"/><stroke android:width="1dp" android:color="#33EC4899"/></shape>')
    write_file("app/src/main/res/drawable/bg_btn.xml", '<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle"><gradient android:startColor="#EC4899" android:endColor="#F472B6" android:angle="135"/><corners android:radius="28dp"/></shape>')
    write_file("app/src/main/res/drawable/bg_input_chat.xml", '<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle"><solid android:color="#15FFFFFF"/><corners android:radius="24dp"/><stroke android:width="1dp" android:color="#22EC4899"/></shape>')
    write_file("app/src/main/res/drawable/bg_send_btn.xml", '<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="oval"><gradient android:startColor="#EC4899" android:endColor="#F472B6" android:angle="135"/></shape>')
    write_file("app/src/main/res/drawable/bg_chat_sent.xml", '<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle"><gradient android:startColor="#EC4899" android:endColor="#F472B6" android:angle="135"/><corners android:topLeftRadius="20dp" android:topRightRadius="20dp" android:bottomLeftRadius="20dp" android:bottomRightRadius="4dp"/></shape>')
    write_file("app/src/main/res/drawable/bg_chat_received.xml", '<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle"><solid android:color="#1AEC4899"/><corners android:topLeftRadius="20dp" android:topRightRadius="20dp" android:bottomLeftRadius="4dp" android:bottomRightRadius="20dp"/><stroke android:width="1dp" android:color="#22EC4899"/></shape>')

    section("VALUES")

    write_file("app/src/main/res/values/colors.xml", '<resources><color name="pink">#EC4899</color><color name="dark">#0D0610</color><color name="white">#FFFFFF</color></resources>')
    write_file("app/src/main/res/values/themes.xml", '<resources><style name="Theme.FileVault" parent="Theme.MaterialComponents.DayNight.NoActionBar"><item name="colorPrimary">@color/pink</item><item name="android:statusBarColor">@color/pink</item><item name="android:windowBackground">@color/dark</item></style></resources>')
    write_file("app/src/main/res/values/strings.xml", '<resources><string name="app_name">File Vault 💖</string></resources>')

    section("MIPMAP")

    write_file("app/src/main/res/mipmap-hdpi/ic_launcher.xml", '<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/pink"/><foreground android:drawable="@color/white"/></adaptive-icon>')
    write_file("app/src/main/res/mipmap-hdpi/ic_launcher_round.xml", '<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/pink"/><foreground android:drawable="@color/white"/></adaptive-icon>')

    section("GITHUB ACTIONS")

    write_file(".github/workflows/main.yml", """name: 💖 Build File Vault APK

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: 📥 Checkout
        uses: actions/checkout@v4
      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: 📝 Generate Files
        run: python scraper.py
      - name: 📂 Move Files
        run: |
          if [ -d "FileVault" ]; then
            cp -r FileVault/* .
            cp -r FileVault/.[!.]* . 2>/dev/null || true
            rm -rf FileVault
          fi
          ls -la
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
      - name: 🔧 Make gradlew executable
        run: chmod +x gradlew
      - name: 🏗️ Build Debug APK
        run: ./gradlew assembleDebug
      - name: 🏗️ Build Release APK
        run: ./gradlew assembleRelease
      - name: 📦 Upload Debug APK
        uses: actions/upload-artifact@v4
        with:
          name: FileVault-Debug
          path: app/build/outputs/apk/debug/*.apk
      - name: 📦 Upload Release APK
        uses: actions/upload-artifact@v4
        with:
          name: FileVault-Release
          path: app/build/outputs/apk/release/*.apk
""")

    print(f"""
{'='*60}
  💖 DONE! {TOTAL_FILES} files | {TOTAL_LINES}+ lines
  📁 {ROOT_DIR}
  🔐 Password: 1234
  💖 ZHARE - File Vault Ready!
{'='*60}
""")

if __name__ == "__main__":
    print("💖 FILE VAULT - Building...")
    build_all()
