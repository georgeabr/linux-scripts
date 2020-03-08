#!/bin/bash
#In KDE, COPY PASTE from other apps to firefox-wayland or between firefox tabs DOES NOT WORK.
# https://bugs.kde.org/show_bug.cgi?id=411682 
gsettings set org.gnome.desktop.interface cursor-size 32
gsettings set org.gnome.desktop.interface cursor-blink false
MOZ_ENABLE_WAYLAND=1 firefox-developer-edition
