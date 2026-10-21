---
layout: post
title: "How to Auto Login to Windows 10 Without a Password"
description: "Make Windows 10 sign in automatically without typing a password, using netplwiz or the Sysinternals Autologon tool, and how to undo it."
date:   2018-12-31
categories: windows
last_modified_at: 2026-10-21
---

![Unticking 'Users must enter a user name and password' in netplwiz to sign in automatically](/static/img/win-autologin-header.svg){: width="1000" height="360"}

If you are like me and don't like to enter passwords each time you use your home computer, you'll like this.

This is the easiest way to automatically log in to Windows 10 without entering a password. It works on Windows 11 too.

## Method 1: netplwiz

1. Open the Run dialog by pressing Windows logo and R keys together (Windows+R). Type **netplwiz** and press Enter.
2. In the User Accounts dialog, select your user account and uncheck **Users must enter a user name and password to use this computer**. Click Apply to open the Automatically sign in box.
3. In the Automatically sign in dialog, type your password and then re-enter it to confirm.

Restart your computer to test if the auto login is working.

### The checkbox is missing

On newer builds the checkbox is hidden when Windows Hello is enforced for Microsoft accounts. Open **Settings → Accounts → Sign-in options** and turn off **For improved security, only allow Windows Hello sign-in for Microsoft accounts on this device**. Then open netplwiz again and the checkbox will be back.

## Method 2: Sysinternals Autologon

Microsoft's free [Autologon](https://learn.microsoft.com/en-us/sysinternals/downloads/autologon){:target="_blank"} tool does the same thing. Run it, enter your user name, domain (your PC name) and password, and click **Enable**. It stores the password encrypted instead of in plain text in the registry.

## How to turn it off

Run netplwiz again and tick the checkbox, or click **Disable** in Autologon.

## Is it safe?

Anyone who can physically reach the PC gets into your account, and so does anyone who steals it if the disk isn't encrypted. It's fine for a home media PC or a desktop that never leaves the house. Don't use it on a laptop.
