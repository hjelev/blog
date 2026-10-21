---
layout: post
title: "How I Set Up Ubuntu: GNOME Extensions and Apps"
description: "The GNOME extensions and apps I install right after a fresh Ubuntu install: Dash to Panel, ArcMenu, Desktop Clock, Variety and AppImageLauncher."
date: 2025-10-10
categories: linux
last_modified_at: 2026-10-21
---

![Ubuntu desktop with Dash to Panel taskbar, ArcMenu and a Desktop Clock widget](/static/img/my-ubuntu-header.svg){: width="1000" height="360"}

These are the GNOME extensions and apps I install right after a fresh Ubuntu install. They make the desktop feel closer to a classic taskbar layout.

For the command-line tweaks I apply (dock behaviour, transparency, a wallpaper slideshow), see [Ubuntu customizations from the command line]({% post_url 2021-10-4-Ubuntu-Customizations-CLI %}).

## Installing GNOME extensions

The easiest way to install extensions is the Extension Manager app:

```
sudo apt install gnome-shell-extension-manager
```

Open it, search for the extension by name and click Install. You can also install them from [extensions.gnome.org](https://extensions.gnome.org/){:target="_blank"} with the browser add-on.

## Extensions

- **[Dash to Panel](https://extensions.gnome.org/extension/1160/dash-to-panel/){:target="_blank"}**: merges the dock and the top bar into a single Windows-style taskbar.
- **[Desktop Widgets (Desktop Clock)](https://extensions.gnome.org/extension/5156/desktop-clock/){:target="_blank"}**: puts a clock widget on the desktop.
- **[ArcMenu](https://extensions.gnome.org/extension/3628/arcmenu/){:target="_blank"}**: a start-menu style application launcher with search, favourites and lots of layouts.

## Apps

**Variety**: a desktop wallpaper downloader and changer. It can pull images from online sources or your own folders and rotate them on a timer.

```
sudo apt install variety
```

**[AppImageLauncher](https://github.com/TheAssassin/AppImageLauncher){:target="_blank"}**: the first time you open an AppImage, it offers to move it to a central folder and add it to the app menu, so AppImages behave like installed apps. Install the `.deb` from the project's releases page.
