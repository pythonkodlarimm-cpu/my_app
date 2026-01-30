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

# #14 — Hariç tutulan dizinler
source.exclude_dirs = \
    .git,.github,__pycache__, \
    venv,.venv, \
    build,bin,dist, \
    logs,log,tmp,cache, \
    tests,test,docs,examples

# Hariç tutulan dosya uzantıları
source.exclude_exts = pyc,pyo,log

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
# BUILDOZER AYARLARI
# ==================================================
[buildozer]
log_level = 2
warn_on_root = 1

# GitHub Actions + Android uyumlu ayarlar
android.accept_sdk_license = True
android.build_tools_version = 33.0.2

# ==================================================
# ⚠️ ASLA EKLEME (Cloud build için yanlış)
# ==================================================
# android.sdk_path =
# android.ndk_path =
# android.ndk_version =
