[app]
title = Architecture Tool
package.name = architecturetool
package.domain = org.aslan

source.dir = .
source.include_exts = py,kv,json,txt,md,ttf

version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 1

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE


[buildozer]
log_level = 2
warn_on_root = 1

# ANDROID CONFIG (KESİN)
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.2

android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653
android.accept_sdk_license = True
