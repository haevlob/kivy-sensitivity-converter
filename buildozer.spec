[app]

# Название приложения (как будет видно в лаунчере)
title = Sensitivity Converter

# Имя пакета (должно быть уникальным, в стиле обратного домена)
package.name = sensitivityconverter

# Домен пакета (обычно org.твойник или com.твойник)
package.domain = org.example

# Версия приложения
version = 1.0

# Точка входа — имя файла с классом App
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Зависимости — очень важно перечислить ВСЕ используемые модули
requirements = python3,kivy==2.3.0

# Ориентация экрана
orientation = portrait

# Разрешения (если нужны — например интернет, камера и т.д.)
# android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

# Иконка и сплеш (пока можно пропустить)
#icon.filename = %(source.dir)s/icon.png
#presplash.filename = %(source.dir)s/presplash.png

# Минимальная версия Android
android.api = 33
android.minapi = 21
android.sdk = 20
android.ndk = 25b

# Тип сборки
android.release = False           # для debug-сборки
# android.release = True          # раскомментировать для release (нужен keystore)

[buildozer]

# Логи — полезно включить на время отладки
log_level = 2
warn_on_root = 1
