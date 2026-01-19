[app]

title = Sensitivity Converter
package.name = sensitivityconverter
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
icon.filename = %(source.dir)s/data/icon.png
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.accept_sdk_license = True  # Это фиксит лицензию!
android.build_tools_version = 33.0.0  # Укажи версию build-tools для совместимости

[buildozer]
log_level = 2
warn_on_root = 1
