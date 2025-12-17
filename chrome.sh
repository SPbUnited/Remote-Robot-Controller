#!/bin/sh

#echo "Starting ReSet controll panell"

export DISPLAY=:0
/usr/bin/chromium --no-sandbox --app=http://127.0.0.1:8001/ --start-fullscreen --window-position=0,0 --kiosk --suppress-message-center-popups
#/usr/bin/chromium-browser

