---
layout: post
title: How to Install Mosquitto Broker on Raspberry Pi
description: "Install the Mosquitto MQTT broker on a Raspberry Pi, require a username and password, and test it with mosquitto_pub and mosquitto_sub for Home Assistant."
date: 2021-04-12
categories: raspberry-pi
last_modified_at: 2026-10-21
---

Mosquitto is a small, fast MQTT broker that runs happily on any Raspberry Pi. I use it as the message bus between my sensors and Home Assistant. These are the steps to install it and lock it down with a username and password.

## 1. Install Mosquitto

```
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable --now mosquitto
```

`mosquitto-clients` gives you `mosquitto_pub` and `mosquitto_sub` for testing.

## 2. Create a password file

You'll be prompted to enter the password:

```
mosquitto_passwd -c passwordfile user
```

Use `-c` only for the first user. It creates a new file and overwrites an existing one.

## 3. Move the password file to /etc/mosquitto

```
sudo mv passwordfile /etc/mosquitto/
sudo chown mosquitto: /etc/mosquitto/passwordfile
sudo chmod 0700 /etc/mosquitto/passwordfile
```

Recent Mosquitto versions warn if the password file is readable by other users.

## 4. Configure the broker to use the password file

Create a custom config file in `/etc/mosquitto/conf.d`:

```
sudo nano /etc/mosquitto/conf.d/config.conf
```

The file name has to end in `.conf`, otherwise Mosquitto won't load it.

Here is the configuration I am using, and it works fine with Home Assistant:

```
user mosquitto
max_queued_messages 200
listener 1883 0.0.0.0
allow_zero_length_clientid true
allow_duplicate_messages false
autosave_interval 900
autosave_on_changes false
persistence true
persistence_file mosquitto.db
allow_anonymous false
password_file /etc/mosquitto/passwordfile
```

The `listener` line matters: since Mosquitto 2.0 the broker only accepts connections from localhost unless you define a listener.

Restart the broker to load the config:

```
sudo systemctl restart mosquitto
```

## 5. Test it

In one terminal, subscribe to a test topic:

```
mosquitto_sub -h localhost -t test/topic -u user -P your-password
```

In a second terminal, publish a message:

```
mosquitto_pub -h localhost -t test/topic -m "hello" -u user -P your-password
```

If `hello` shows up in the first terminal, the broker works. Try the same command without `-u` and `-P`. It should be refused, which means anonymous access is off.

## Logs

```
sudo cat /var/log/mosquitto/mosquitto.log
sudo journalctl -u mosquitto
```

To connect Home Assistant, add the MQTT integration and point it at the Pi's IP address, port 1883, with the user and password you created.
