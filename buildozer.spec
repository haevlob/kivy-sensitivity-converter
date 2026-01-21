[app]

title = Sensitivity Converter

package.name = sensitivityconverter

package.domain = com.devon

version = 1.0

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

requirements = python3,kivy==2.3.0

orientation = portrait

android.minapi = 21
android.api = 33
android.ndk = 25b
android.accept_sdk_license = True

android.release = False

[buildozer]

log_level = 2
warn_on_root = 1
