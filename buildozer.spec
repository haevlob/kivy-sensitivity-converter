[app]
title = Sensitivity Converter
package.name = sensconverter
package.domain = org.example

source.dir = .
source.include_exts = py,kv,png,jpg,atlas

version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 1

android.permissions = INTERNET

# 🔒 ФИКС ВЕРСИЙ (ОЧЕНЬ ВАЖНО)
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools_version = 34.0.0

android.archs = arm64-v8a,armeabi-v7a

android.allow_backup = True
android.private_storage = False

[buildozer]
log_level = 2
warn_on_root = 1
