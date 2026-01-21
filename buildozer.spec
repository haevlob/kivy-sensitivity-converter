[app]
title = Sensitivity Converter
package.name = sensconverter
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 1

icon.filename = %(source.dir)s/icon.png

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

android.archs = arm64-v8a,armeabi-v7a

android.allow_backup = True
android.private_storage = False

android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1
