[app]

# Название приложения
title = Sensitivity Converter

# Пакет
package.name = sensconverter
package.domain = org.dimonsensitive

# Версия
version = 0.1

# Требуемые модули
requirements = python3,kivy==2.2.1,pyjnius,android

# Исходники
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

# Иконка и прессплеш (если добавишь файлы — укажи пути)
# app_icon = icon.png
# presplash = presplash.jpg

# Ориентация (портретная — стандарт для таких утилит)
orientation = portrait

# Полноэкранный режим
fullscreen = 1

# Логи Buildozer
log_level = 2

# Android
[buildozer]

# Архитектуры (оба, чтобы покрыть все устройства)
android.archs = arm64-v8a, armeabi-v7a

# API и минимальная версия Android
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# Разрешения (интернет не нужен, но если вдруг захочешь добавить рекламу/обновления)
android.permissions = INTERNET

# NDK и SDK пути (Buildozer сам скачает, но можно указать)
# android.ndk_path =
# android.sdk_path =

# Релизный режим (для debug оставь p4a.branch = develop)
p4a.branch = master
