---
layout: post
title: Squeezelite Service Not Mixing with Browser Audio (PipeWire/PulseAudio Fix)
date: 2025-10-12
categories: linux
---

# Squeezelite Service Not Mixing with Browser Audio (PipeWire/PulseAudio Fix)

The Squeezelite audio player is a wonderful headless solution, but getting it to run as a reliable, shareable background service on modern Linux distributions (like Ubuntu, Debian, or Fedora, especially those using PipeWire) can be a nightmare.

This post documents a common, frustrating error and the simple fix that allows Squeezelite to play music alongside other applications, like your browser (YouTube, Spotify Web, etc.).

## The Problem: The Audio "Host is Down" Loop

When setting up Squeezelite as a persistent **systemd service** (often running as a low-privilege user like `daemon` or `squeezelite`), the service either failed to start or immediately grabbed the sound card exclusively.

### The Error Message

The core issue was demonstrated by this error log, which repeats when using devices like `default` or `pulse`:

```
[16:04:06.843393] test_open:281 playback open error: Host is down
[16:04:06.843416] output_init_common:401 unable to open output device: default
```

### Why This Happens

1.  **Exclusive Access:** When running Squeezelite with a raw hardware device (`-o hw:CARD=PCH,DEV=0`), the application takes **exclusive control** of the sound card, blocking the browser.
2.  **Environment Conflict:** When attempting to use the mixing devices (`-o default` or `-o pulse`), the service fails. This is because **System Services** run in a minimal environment and **cannot reliably connect** to the **User Session PipeWire/PulseAudio server** that manages all desktop audio (including your browser). It's a fundamental conflict between a system process and a user-level audio mixer. The "Host is down" error simply means the connection to the mixer server was refused or the socket was not found.

-----

## ✅ The Easy Fix: Switch to a User Autostart Application

The solution is to stop treating Squeezelite as a low-level "system" component and instead run it as a normal "user" application that starts **after** your graphical session (and PipeWire) is fully loaded. This is the only way to guarantee it connects to the active audio mixer.

This method uses a standard **Desktop Entry (.desktop) file**, which works on most Linux desktop environments (GNOME, KDE, XFCE, Cinnamon, etc.).

### Step 1: Disable the Broken System Service

Stop and permanently disable the old service file to prevent conflicts.

```bash
# Stop the running service:
sudo systemctl stop squeezelite.service

# Disable the service so it doesn't try to start on the next reboot:
sudo systemctl disable squeezelite.service
```

### Step 2: Create the Autostart File

We create a configuration file that tells your desktop environment to launch Squeezelite with the correct, shareable device name when you log in.

1.  **Create the directory** (if needed):

    ```bash
    mkdir -p ~/.config/autostart
    ```

2.  **Create the autostart file** (`squeezelite.desktop`):

    ```bash
    nano ~/.config/autostart/squeezelite.desktop
    ```

3.  **Paste and save this content:**

    ```ini
    [Desktop Entry]
    Name=Squeezelite Player
    Comment=Starts Squeezelite audio player on user login
    # Key Fix: Use the 'pipewire' audio output device
    Exec=/usr/bin/squeezelite -n mini-pc -o pipewire
    Terminal=false
    Type=Application
    X-GNOME-Autostart-enabled=true
    ```

    *If `pipewire` doesn't work, try `-o default` or `-o pulse` here, as the autostart environment is much more forgiving than the system service environment.*

### Step 3: Log In and Enjoy Simultaneous Audio

1.  **Log out** of your desktop session.
2.  **Log back in.**

Squeezelite will now start automatically in the background as your user, correctly connecting to the **PipeWire** mixing server. You can now stream music to Squeezelite while simultaneously watching a YouTube video or listening to other audio in your browser\! 