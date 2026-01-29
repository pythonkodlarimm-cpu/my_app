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
android.api = 33
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 1
