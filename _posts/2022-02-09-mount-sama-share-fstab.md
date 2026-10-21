---
layout: post
title: "How to Mount a Samba Share on Boot with fstab"
description: "Mount a Samba (CIFS) share automatically at boot on Ubuntu with /etc/fstab, a protected credentials file, and options that avoid boot hangs."
date: 2022-02-08
categories: linux
last_modified_at: 2026-10-21
---

![An /etc/fstab line mounting //server/share on /mnt/share using a credentials file](/static/img/samba-fstab-header.svg){: width="1000" height="360"}

To mount a Samba share every time Ubuntu boots, you add a line to `/etc/fstab`. Here's the quick version and a slightly safer one that keeps your password out of fstab.

## Install cifs-utils

```
sudo apt install cifs-utils
```

## Quick version

Update the path to your samba share, the local mount folder and your samba credentials:

```
//remote/path/to/samba/share /local/mount/folder cifs username=your-user-name-here,password=your-password-here,rw,file_mode=0777,dir_mode=0777       0       0
```

This works, but `/etc/fstab` is readable by every user on the machine, so anyone can read the password.

## Safer version: a credentials file

Create a file that only root can read:

```
sudo nano /root/.smbcredentials
```

```
username=your-user-name-here
password=your-password-here
```

```
sudo chmod 600 /root/.smbcredentials
```

Create the mount folder:

```
sudo mkdir -p /mnt/share
```

Then use this line in `/etc/fstab`:

```
//server/share /mnt/share cifs credentials=/root/.smbcredentials,uid=1000,gid=1000,iocharset=utf8,_netdev,nofail,x-systemd.automount 0 0
```

What the options do:

- `uid` / `gid`: the files will be owned by your user (run `id` to find yours) instead of root.
- `_netdev`: wait for the network before mounting.
- `nofail`: don't hang the boot if the server is down.
- `x-systemd.automount`: mount the share the first time it's accessed, which avoids most boot timing problems.

## Mount it

After you update your fstab file, mount the new entry without rebooting:

```
sudo systemctl daemon-reload
sudo mount -a
```

If `mount -a` prints nothing, it worked. Run `ls /mnt/share` to check.
