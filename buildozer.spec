[app]
# ==================================================
# UYGULAMA BİLGİLERİ
# ==================================================
title = Architecture Tool
package.name = architecturetool
package.domain = org.aslan

# ==================================================
# KAYNAK DOSYALAR
# ==================================================
source.dir = .
source.include_exts = py,kv,json,txt,md,ttf

# ==================================================
# #15 — İYİLEŞTİRİLMİŞ HARİÇ TUTULAN DİZİNLER
# ==================================================
source.exclude_dirs = \
    .git,.github,.gitlab,.svn, \
    __pycache__,.mypy_cache,.pytest_cache, \
    venv,.venv,env,.env, \
    build,bin,dist,.buildozer, \
    logs,log,tmp,temp,cache,.cache, \
    tests,test,testing, \
    docs,doc,examples,example,samples

# Hariç tutulan dosya uzantıları
source.exclude_exts = pyc,pyo,log,tmp,bak,swp

# ==================================================
# SÜRÜM
# ==================================================
version = 0.1

# ==================================================
# GEREKSİNİMLER
# ==================================================
requirements = python3,kivy

# ==================================================
# EKRAN / ORYANTASYON
# ==================================================
orientation = portrait
fullscreen = 1

# ==================================================
# ANDROID AYARLARI
# ==================================================
android.api = 33
android.minapi = 21
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.allow_backup = True
android.wakelock = False
android.keyboard_mode = system

# ==================================================
# BUILDOZER AYARLARI (KESİN)
# ==================================================
[buildozer]
log_level = 2
warn_on_root = 1

android.accept_sdk_license = True
android.build_tools_version = 33.0.2

# 🔴 KRİTİK — Buildozer GitHub Actions SDK’sını kullansın
android.sdk_path = /usr/local/lib/android/sdk

# ==================================================
# ⚠️ ASLA EKLEME
# ==================================================
# android.ndk_path =
# android.ndk_version =
