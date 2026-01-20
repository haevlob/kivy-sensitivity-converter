[app]

title = Sensitivity Converter

package.name = sensitivityconverter

package.domain = org.test

source.dir = .

source.include_exts = py,png,jpg,kv,atlas

version = 0.1

requirements = hostpython3,python3,kivy  # Добавлен hostpython3 для фикса compilation

icon.filename = %(source.dir)s/data/icon.png

orientation = portrait

fullscreen = 0

android.permissions = INTERNET

android.api = 33

android.minapi = 21

android.accept_sdk_license = True

android.build_tools_version = 33.0.0

android.ndk = 25b

android.bootstrap = sdl2

p4a.branch = develop  # Изменено на develop для фикса bugs

p4a.fork = kivy

android.extra_compile_args = -Wno-implicit-function-declaration -Wno-error=implicit-function-declaration -Wno-incompatible-function-pointer-types -Wno-int-to-void-pointer-cast -Wno-error

android.extra_cflags = -Wno-implicit-function-declaration -Wno-error=implicit-function-declaration

[buildozer]

log_level = 2

warn_on_root = 1
