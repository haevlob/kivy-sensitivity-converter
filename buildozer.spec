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

android.accept_sdk_license = True

android.build_tools_version = 33.0.0

android.ndk = 23b  # Самая стабильная версия NDK для p4a

android.bootstrap = sdl2

p4a.branch = master

p4a.fork = kivy

android.extra_compile_args = -Wno-error -Wno-implicit-function-declaration -Wno-incompatible-pointer-types -Wno-int-to-pointer-cast -Wno-unused-variable -Wno-unused-but-set-variable

[buildozer]

log_level = 2

warn_on_root = 1
