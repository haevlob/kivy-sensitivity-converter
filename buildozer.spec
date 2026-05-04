[app]

# Название приложения
title = Mobile Games Sens Converter

# Уникальное имя пакета (менять нельзя после первой публикации!)
package.name = sensitivityconverter
package.domain = com.taysindim

# Версия приложения
version = 1.3
author = Taysin Dim
author_email = haevlob@gmail.com

# Иконка и сплеш-экран
icon.filename = icon.png
presplash.filename = presplash.png

# Исходный код
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Зависимости
requirements = python3,kivy==2.3.0

# Ориентация экрана
orientation = portrait

# --- Android настройки ---

# Target API (последняя версия Android 15)
android.api = 35

# Минимальная версия Android (8.0 = RuStore минимум)
android.minapi = 26

# NDK r27 — текущий LTS (долгосрочная поддержка), самый стабильный
android.ndk = 27c

# Архитектура: arm64-v8a покрывает 95%+ современных устройств
android.archs = arm64-v8a

# Принять лицензию SDK автоматически (нужно для GitHub Actions)
android.accept_sdk_license = True

# Формат сборки: apk для RuStore
android.release_artifact = apk

# Разрешения: приложение работает полностью офлайн, разрешения не нужны
# android.permissions =

[buildozer]

# Уровень логов: 1 = нормальный, 2 = подробный (для отладки)
log_level = 1
