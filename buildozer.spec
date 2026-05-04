[app]
title = Mobile Games Sens Converter
package.name = sensitivityconverter
package.domain = com.taysindim
version = 1.2
author = Taysin Dim
author_email = haevlob@gmail.com

icon.filename = icon.png
presplash.filename = presplash.png

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
requirements = python3,kivy==2.3.0
orientation = portrait
android.minapi = 21
android.api = 35
android.ndk = 25b
android.accept_sdk_license = True
android.release = True
android.release_artifact = apk
[android]
android.permissions = INTERNET, ACCESS_NETWORK_STATE
