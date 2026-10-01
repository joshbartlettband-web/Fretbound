#!/bin/bash
# Setup for a Claude Code cloud session (or any Ubuntu machine): browser tests, art scripts, and the Android build.
set -e
sudo apt-get update -y
sudo apt-get install -y openjdk-17-jdk-headless aapt apksigner dalvik-exchange libandroid-23-java zipalign
pip install --break-system-packages playwright pillow numpy scipy fonttools brotli
python3 -m playwright install --with-deps chromium
echo "Setup done. Tests: see CLAUDE.md. Build: bash android/build.sh"
