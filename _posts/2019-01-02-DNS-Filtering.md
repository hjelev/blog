---
layout: post
title: "DNS Filtering: Block Ads and Malware with Free DNS Servers"
description: "Free filtering DNS services compared: AdGuard DNS, CleanBrowsing, OpenDNS FamilyShield, Quad9 and self-hosted Pi-hole, with the server IPs to use."
seo_title: "Block Ads and Malware with Free Filtering DNS Servers"
date:   2019-01-02
categories: windows
last_modified_at: 2026-10-21
---

![A filtering DNS server answers normal domains and returns 0.0.0.0 for ad and malware domains](/static/img/dns-filtering-header.svg){: width="1000" height="360"}

## Block ads and protect your network from malware by changing your DNS provider.

It is very easy to block more than 90% of the ads you see when you browse the web or use applications on your phone. All you have to do is use filtered dns service.
There are a couple of them lately and they all offer slightly different services. Some of them block advertisement and malware-serving domains other also offer "Family protection". 

If you create an account at opendns.com you'll be able to choose from more than 50 customizable filtering categories and control what websites your children visit at home.

The easiest way to change the DNS provider for your home network is to change your router network settings by pointing it to some of the DNS providers listed below.

If you have a phone running Android 9 or newer you can set a custom "Private DNS" server that will be used no matter what network you are connected to so you can block ads even when you are outside of your home network. 

![Comparison of AdGuard DNS, Epsilon Eight, CleanBrowsing, OpenDNS FamilyShield, Quad9, Cloudflare for Families and Pi-hole by ads, malware and adult content blocking](/static/img/dns-filtering-compare.svg){: width="1000" height="520"}

## Ad Guard
<https://adguard-dns.io/en/public-dns.html>{:target="_blank"}

Adguard.com offers advertisement blocking plus malware protection.

use these DNS servers if you want ads blocking and malware protection:

* Preferred DNS server: **94.140.14.14**
* Alternative DNS server: **94.140.15.15**

ads blocking, malware protection and "Family protection" servers.

* Preferred DNS server: **94.140.14.15**
* Alternative DNS server: **94.140.15.16**

The old 176.103.130.x addresses were retired, so update your router if you still use them.

For Android Private DNS use `dns.adguard-dns.com` (or `family.adguard-dns.com` for the family filter).

![Android Private DNS settings with the hostname set to dns.adguard-dns.com](/static/img/dns-filtering-android.svg){: width="1000" height="360"}

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
| Google | 8.8.8.8 |  Unfiltered. Most popular option. |
| Cloudflare | 1.1.1.1 | Private and unfiltered. |
| Cloudflare for Families | 1.1.1.2 / 1.1.1.3 | Blocks malware (1.1.1.2), or malware and adult content (1.1.1.3). |
| Yandex DNS | 77.88.8.7 | Old player that blocks malicious domains. Very popular in Russia. |
| Comodo DNS |  8.26.56.26 |  Old player that blocks malicious domains. |
