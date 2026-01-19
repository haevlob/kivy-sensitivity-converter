[app]

# Название приложения
title = Sensitivity Converter

# Пакетное имя (для Android)
package.name = sensitivityconverter

# Доменное имя пакета
package.domain = org.test

# Директория с кодом
source.dir = .

# Расширения файлов для включения
source.include_exts = py,png,jpg,kv,atlas

# Версия приложения
version = 0.1

# Зависимости (обязательно kivy и python3)
requirements = python3,kivy

# Иконка (если есть файл, укажи путь)
icon.filename = %(source.dir)s/data/icon.png

# Ориентация экрана
orientation = portrait

# Полноэкранный режим
fullscreen = 0

# Разрешения (добавь, если нужно интернет или другие)
android.permissions = INTERNET

# Целевая API Android
android.api = 33

# Минимальная API
android.minapi = 21

# Автоматическое принятие лицензии SDK (фикс ошибки)
android.accept_sdk_license = True

# Версия build-tools (для совместимости с Aidl)
android.build_tools_version = 33.0.0

# Версия NDK (рекомендуемая для p4a)
android.ndk = 25b

[buildozer]

# Уровень логов (2 для детального вывода)
log_level = 2

# Предупреждение, если root
warn_on_root = 1
