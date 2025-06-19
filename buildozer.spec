[app]

# Title of your app (shown on Android)
title = Receipt_app

# Package name (reverse-DNS format, lowercase)
package.name = receiptapp

# Domain (use org.test if you don't have one)
package.domain = org.test

# Path to your main Python file (automatically detects main.py)
source.dir = .
source.main = main.py  # Change to app.py if your file is named differently

# Include all necessary file types
source.include_exts = py,png,jpg,jpeg,kv,ttf,json

# App version
version = 0.1

# Python dependencies (add others like Pillow, requests if needed)
requirements = python3,kivy,reportlab

# Android permissions (uncomment/add as needed)
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Orientation (portrait or landscape)
orientation = portrait

# Android build settings (critical!)
android.api = 30          # Target Android 13
android.minapi = 21       # Minimum Android 5.0 support
android.target = 30

android.ndk = 23b        

android.archs = arm64-v8a, armeabi-v7a  
android.allow_backup = True

# Enable modern AndroidX support
android.enable_androidx = True

# (Optional) Uncomment to add presplash/icon
#presplash.filename = %(source.dir)s/data/presplash.png
#icon.filename = %(source.dir)s/data/icon.png

[buildozer]
# Build logs (helpful for debugging)
log_level = 2