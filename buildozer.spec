[app]
# =========================
# UYGULAMA BİLGİLERİ
# =========================
title = Architecture Tool
package.name = architecturetool
package.domain = org.aslan

# =========================
# KAYNAK DOSYALAR
# =========================
source.dir = .
source.include_exts = py,kv,json,txt,md,ttf
source.exclude_dirs = tests,bin,build,.git,.github,__pycache__
source.exclude_exts = pyc,pyo

# =========================
# SÜRÜM
# =========================
version = 0.1

# =========================
# GEREKSİNİMLER
# =========================
requirements = python3,kivy

# =========================
# EKRAN / ORYANTASYON
# =========================
orientation = portrait
fullscreen = 1

# =========================
# ANDROID AYARLARI
# =========================
android.api = 33
android.minapi = 21
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.allow_backup = True
android.wakelock = False
android.keyboard_mode = system

# =========================
# BUILDOZER AYARLARI
# =========================
[buildozer]
log_level = 2
warn_on_root = 1

# GitHub Actions uyumlu
android.accept_sdk_license = True
android.build_tools_version = 33.0.2

# ❌ ASLA EKLEME
# android.sdk_path =
# android.ndk_path =
