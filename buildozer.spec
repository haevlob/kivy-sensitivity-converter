[app]
title = Sensitivity Converter
package.name = sensconverter
package.domain = com.devonmobile

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

requirements =
    python3
    kivy==2.3.0             # или kivy==2.4.0 если хочешь самую свежую
    cython==0.29.37         # очень важно — новые версии часто ломают
    pillow                  # если используешь изображения

orientation = portrait
fullscreen = 1

android.permissions =

# Версии Android (актуально на 2026)
android.api = 34
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a   # или только arm64-v8a, если не нужна поддержка старых

p4a.bootstrap = sdl2
p4a.local_recipes =

log_level = 2
warn_on_root = 1
