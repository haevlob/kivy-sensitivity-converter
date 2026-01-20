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
requirements = hostpython3==3.9.19,python3,kivy

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

# Автоматическое принятие лицензии SDK
android.accept_sdk_license = True

# Версия build-tools
android.build_tools_version = 33.0.0

# Версия NDK
android.ndk = 25b

# Bootstrap для graphics (SDL2 для Android)
android.bootstrap = sdl2

# Branch python-for-android (master для стабильности)
p4a.branch = master

# Fork python-for-android
p4a.fork = kivy

# Флаги компиляции для фикса errors
android.extra_compile_args = -Wno-implicit-function-declaration -Wno-incompatible-function-pointer-types -Wno-int-to-void-pointer-cast -Wno-error=implicit-function-declaration

[buildozer]

# Уровень логов
log_level = 2

# Предупреждение, если root
warn_on_root = 1
