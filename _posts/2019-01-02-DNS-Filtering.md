---
layout: post
title: DNS Filtering
date:   2019-01-02
categories: windows
---
## Block ads and protect your network from malware by changing your DNS provider.

It is very easy to block more than 90% of the ads you see when you browse the web or use applications on your phone. All you have to do is use filtered dns service.
There are coule of them lately and they all offer slightly different services. Some of them block advertisement and malware-serving domains other also offer "Family protection". 

If you create an account at opendns.com you'll be able to choose from more than 50 customizable filtering categories and control what websites your children visit at home.

The easiest way to change the DNS provider for your home network is to change your router network settings by pointing it to some of the DNS providers listed below.

If you have a phone running Android 9 you can set a custom DNS server that will be used no mather what network you are connected to so you can block ads even when you are outside of your home network. 

## Ad Guard
<http://dns.adguard.com>{:target="_blank"}

Adguard.com offers advertisement blocking plus malware protection.

use these DNS servers if you want ads blocking and malware protection:

* Preferred DNS server: **176.103.130.130**
* Alternative DNS server: **176.103.130.131**

ads blocking, malware protection and "Family protection" servers.

* Preferred DNS server: **176.103.130.132**
* Alternative DNS server: **176.103.130.134**

{:.text-center}
![adguard dns](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/AdGuard.svg/220px-AdGuard.svg.png)

## PrivateDNS - EPSILON EIGHT 

<https://www.epsiloneight.com/private-dns>{:target="_blank"}

Block over 114k advertisement and malware-serving domains

* Preferred DNS server: **138.68.250.168** 

## CleanBrowsing DNS

<https://cleanbrowsing.org/filters>{:target="_blank"}

They have 3 free content filters available via IPv4 and IPv6. Choose the one that fits your needs the most. 

All their IP addresses accept DNS request to the standard port 53 and 5353. DNS over TLS is available over port 853 and DNScrypt over port 8443.

| Type | Server | Description |
|--|--|--|
| Security Filter 	| **185.228.168.9**   	| Malicious domains blocked (phishing/ malware).                          	|
| Adult Filter    	| **185.228.168.10**  	| Adult domains blocked. Search Engines set to safe mode +Security Filter 	|
| Family Filter   	| **185.228.168.168** 	| Proxies VPNs & Mixed Adult Content blocked. Youtube to safe mode +Adult 	|


## Open DNS
<https://www.opendns.com/setupguide/#familyshield>{:target="_blank"}

OpenDNS Family Shield

Pre-configured to block adult content — set it & forget it
* Preferred DNS server: **208.67.222.123**
* Alternative DNS server: **208.67.220.123**

## Quad 9
<https://www.quad9.net>{:target="_blank"}

Quad 9 provides malware and malicious domains protection - there is no ads blocking.

* Preferred DNS server: **9.9.9.9**
* Alternative DNS server: **149.112.112.112**

## Pi-hole®: A black hole for Internet advertisements
<https://pi-hole.net/>{:target="_blank"}

This is a self hosted option. You can host pi-hole on a raspberry pi, docker container or VM and maintain your own block lists.
You can also use this with one of the DNS providers mentioned above.

<https://firebog.net/>{:target="_blank"} - block lists to use with pi-hole


## Other DNS providers


| Provider  |  DNS Server | Description |
|--|--|--|
| Google | 8.8.8.8 |  Private and unfiltered. Most popular option. |
| Google | 8.8.8.8 |  Private and unfiltered. Most popular option. |
| CloudFlare | 1.1.1.1 | Private and unfiltered. New player. |
| Yandex DNS | 77.88.8.7 | Old player that blocks malicious domains. Very popular in Russia. |
| Comodo DNS |  8.26.56.26 |  Old player that blocks malicious domains. |
