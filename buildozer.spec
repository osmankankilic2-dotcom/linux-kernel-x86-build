[app]

# (str) Title of your application
title = Aslan Video Indirici

# (str) Package name
package.name = aslanvideodownloader

# (str) Package domain (needed for android packaging)
package.domain = org.aslan

# (str) Source files where the javat/python code is located
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,yt-dlp,certifi,urllib3,idna,charset-normalizer,requests

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (str) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presets
android.accept_sdk_license = true

# (list) List of extra java jar files to add
# android.add_jars = foo.jar,bar.jar

# (list) Architectural builds to support
android.archs = arm64-v8a,armeabi-v7a
