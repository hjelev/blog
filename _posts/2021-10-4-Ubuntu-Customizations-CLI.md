---
layout: post
title: "Ubuntu Customizations from the Command Line (gsettings)"
description: "Tweak Ubuntu from the terminal with gsettings: minimize on click in the dock, dock transparency, full path in Files, and a wallpaper slideshow script."
date: 2021-10-04
categories: linux
redirect_from:
  - /ubuntu/Ubuntu-Customizations-CLI/
---

![gsettings commands for dock minimize-on-click, dock opacity, full path in Files and wallpaper](/static/img/ubuntu-gsettings-header.svg){: width="1000" height="360"}

## How do I enable 'minimize on click' on Ubuntu dock

Open Terminal and run

`gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize'`

To revert to the default option, simply run

`gsettings reset org.gnome.shell.extensions.dash-to-dock click-action`

# How to make dock background 80% transparent in Ubuntu

First enable custom colors:

`gsettings set org.gnome.shell.extensions.dash-to-dock transparency-mode 'FIXED'`

Then, to set transparency to 80%, issue the command

`gsettings set org.gnome.shell.extensions.dash-to-dock background-opacity 0.2`

Change 0.0 to any number between 0 and 1.

To reset to the default setting:

`gsettings reset org.gnome.shell.extensions.dash-to-dock background-opacity`

# Make file manager always show full path (not only with ctrl + l)
`gsettings set org.gnome.nautilus.preferences always-use-location-entry true`

# Create a wallpaper slideshow using bash script and cron
Save this script as a bash file, update the `DIR` variable to point to your photo collection and schedule it with a cronjob.
```
#!/usr/bin/env bash

# Update the DIR variable to point to your photos

DIR="/home/masoko/Pictures/wallpapers/reddit"
PIC=$(ls $DIR/* | shuf -n1)

RUID=$(who | awk 'FNR == 1 {print $1}')
RUSER_UID=$(id -u ${RUID})
sudo -u ${RUID} DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/${RUSER_UID}/bus" gsettings set org.gnome.desktop.background picture-uri "file://$PIC"
exit
```
