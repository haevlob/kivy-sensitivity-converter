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

android.ndk = 25b

android.bootstrap = sdl2

p4a.branch = develop

p4a.fork = kivy

android.extra_compile_args = -Wno-implicit-function-declaration -Wno-incompatible-function-pointer-types -Wno-int-to-void-pointer-cast -Wno-error=implicit-function-declaration -Wno-implicit-int

[buildozer]

log_level = 2

warn_on_root = 1
