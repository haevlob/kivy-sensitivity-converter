[app]

# (str) Title of your application
title = Kivy Sensitivity Converter

# (str) Package name
package.name = kivysensitivityconverter

# (str) Package domain (needed for android/ios packaging)
package.domain = org.haevlob

# (str) Source dir where to find main.py
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
# Do not prefix with './'
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.0  # Pin Kivy to stable version

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
#requirements.source.kivy = ../../kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 2.3.0

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for splashscreen mode)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format.
# see https://lottiefiles.com/ for examples and https://airbnb.design/lottie/
# for general documentation.
# Lottie files can be created using various tools, like Adobe After Effect or Synfig.
#android.presplash_lottie = "path/to/lottie/file.json"

# (str) Adaptive presplash background for splashscreen
#android.adaptive_presplash_background = #FFFFFF

# (list) Permissions
# (See https://python-for-android.readthedocs.io/en/latest/buildoptions/#build-options for all the supported syntaxes and properties)
#android.permissions = android.permission.INTERNET, (name=android.permission.WRITE_EXTERNAL_STORAGE;maxSdkVersion=18)

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
android.ndk = 23b  # Downgraded to 23b for compatibility

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually remain at the default.
android.ndk_api = 21

# (bool) Use --private storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK licenses.
# android.accept_sdk_license = False

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy-based app
# android.theme = @android:style/Theme.NoTitleBar

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (str) Path to a custom whitelist file
#android.whitelist_src =

# (str) Path to a custom blacklist file
#android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# ouya_*.jar or org/android licensing/*.jar.
# You can also use URL, for example:
# jars = https://mycompany.com/myproject.jar
# or absolute paths for when the jar is already installed locally:
# jars = /path/to/myproject.jar
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar,https://mycompany.com/myproject.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
#android.add_src =

# (list) Android AAR archives to add
#android.add_aars =

# (list) Put these files or directories in the apk assets directory.
# Either form may be used, and assets need not exist or be in the source
# directory. That is, 'foo/bar/man.png' will copy from source.dir/foo/bar/man.png
# and 'other_dir' will copy the full contents of other_dir hierachically.
#android.add_assets = source_dir relative path

# (list) Gradle dependencies to add
#android.gradle_dependencies =

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' dependency.
#android.enable_androidx = False

# (list) add java compile options
# this can for example be necessary when importing certain java libraries using the 'android.gradle_dependencies' option
# see https://developer.android.com/studio/write/java8-support for further information
android.add_compile_options = -Wno-incompatible-function-pointer-types  # Suppress pointer type warnings

# (list) Gradle repositories to add {can be necessary for some android.gradle_dependencies}
# please enclose in double quotes 
# e.g. android.gradle_repositories = "maven { url 'https://kotlin.bintray.com/ktor' }"
#android.add_gradle_repositories =

# (list) packaging options to add 
# see https://developer.android.com/reference/proguard.html
# can be necessary to solve issues when using --deps ( --backends ) option on API<27
# for example, to avoid dex being exceeded by api versions that
# are used only in a third-party dependency as lxml (versions greater than 4.6.1)
# and avoid conflicts with the base dependencies.
#android.add_packaging_options = "exclude 'META-INF/NOTICE' / 'META-INF/LICENSE' / 'META-INF/DEPENDENCIES' / 'META-INF/*'"

# (list) Java classes to add as activities to the manifest.
#android.add_activities = com.example.ExampleActivity

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters =

# (list) Copy these files to src/main/res/xml (or res/values/english)?
#android.add_xml =

# (str) launchMode to use for the main activity
#android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Use --assets-public.mp3 (instead of --private) storage
#android.assets_public_mp3 = False

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# In past, was `android.arch` as we weren't supporting builds for multiple archs at the same time.
android.archs = arm64-v8a  # Only build for 64-bit to avoid 32-bit compilation issues

# (int) overrides automatic versionCode computation (used in build.gradle)
# this is not the same as app version and should only be tweaked if you know what you're doing.
# android.numeric_version = 1

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) the filename of the android backup rules (see android SDK docs)
#android.backup_rules = my_backup_rules.xml

# (str) extra arguments for aapt
#android.aapt_opts = 

# (str) Python for android (p4a) branch to use, defaults to master
p4a.branch = master  # Use master branch for stability

# (str) Local path to python-for-android (if not using branch)
#p4a.local_recipes =

# (str) bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (str) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port =

# Control whether the build archive is dated
#p4a.build_archive = False

# enables pretty build output
#p4a.no_byte_compile_python = False

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
 # (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) The development team to use for signing the debug version
#ios.codesign.development_team.debug = <hexstring>

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s


# (str) The development team to use for signing the release version
#ios.codesign.development_team.release = <hexstring>

# (str) URL pointing to .ipa file to be installed by the runner
# Only supported in xcb mode
#ios.manifest.app_url =

# (str) URL pointing to an icon (100x100px) to be displayed by the runner
# Only supported in xcb mode
#ios.manifest.icon_url =


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    # List as sections, where each section is a profile that allow us to easily
#    # switch options such as p4a.branch or p4a.bootstrap.
#    # For example, to build with pygame instead of sdl2, activate the following
#    # profile (don't forget to uncomment)
#[myprofile]
#p4a.bootstrap = pygame
