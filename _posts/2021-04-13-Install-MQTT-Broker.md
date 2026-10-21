---
layout: post
title: How to Install Mosquitto Broker on Raspberry Pi
date: 2021-04-12
categories: raspberry-pi
---
1. Install the mosquitto broker with the command below:

sudo apt install -y mosquitto mosquitto-clients

2. Create a password file (you'll be promted to enter the password).

`mosquitto_passwd -c passwordfile user`

3. move the password file to /etc/mosquitto
 
`sudo mv passwordfile /etc/mosquitto/`
 
4. Update mosquitto broker config so it uses the created password file.

Create a custom config file in `/etc/mosquitto/conf.d`

`sudo nano /etc/mosquitto/conf.d/config.cfg`

Here is the configuration I am using and it works fine with Home Assistant:

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

Here is how to check mosquitto logs.

`sudo cat /var/log/mosquitto/mosquitto.log`
