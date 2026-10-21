---
layout: post
title: Rename bluetooth device in Ubuntu
description: "Rename a paired Bluetooth device in Ubuntu from the terminal with bt-device from bluez-tools, or with bluetoothctl."
date: 2022-10-18
categories: linux
permalink: /linux/ubuntu-rename-bluetooth-device/
redirect_from:
  - /linux/ubuntu-rename-bluetooth-device-copy/
last_modified_at: 2026-10-21
---

![Renaming a paired Bluetooth device from S530 to S530 Blue with bt-device](/static/img/bt-rename-header.svg){: width="1000" height="360"}

Some Bluetooth devices show up in Ubuntu with unhelpful names like `S530` or a bare MAC address. You can give them an alias that's used in the Settings panel and the sound menu.

## Option 1: bt-device

Use `bt-device`, part of the bluez-tools package:

```
sudo apt install bluez-tools
```

Get a list of paired devices:

```
bt-device -l
```

To set the new alias:

```
bt-device --set <mac-address|name> Alias "New Name"
```

For example:

```
bt-device --set S530 Alias "S530 Blue"
```

## Option 2: bluetoothctl (no extra packages)

`bluetoothctl` comes with Ubuntu. Start it, connect to the device, then set the alias:

```
bluetoothctl
[bluetooth]# devices
[bluetooth]# connect AA:BB:CC:DD:EE:FF
[S530]# set-alias S530 Blue
[S530 Blue]# exit
```

The new name shows up right away in the Bluetooth settings and stays after a reboot. To go back to the original name, set the alias to an empty string.
