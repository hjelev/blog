---
layout: page
title: About
permalink: /about/
description: "Who writes blog.masoko.net: Hristo Jelev's notes on Linux, CLI tools, Raspberry Pi and self-hosting, plus the open-source projects behind them."
---

<div class="about-card">
  <img class="about-card__avatar" src="{{ site.logo }}" alt="{{ site.author }}" width="96" height="96">
  <div>
    <p class="about-card__name">{{ site.author }}</p>
    <p class="about-card__line">Linux · CLI tools · Raspberry Pi · self-hosting</p>
    <p class="about-card__links">
      <a href="{{ site.github }}" target="_blank" rel="noopener">github.com/hjelev</a> ·
      <a href="/feed.xml">RSS</a>
    </p>
  </div>
</div>

I'm {{ site.author }}, and this blog is where I write things down so I can fix or redo them when they break: Linux setup, command-line tools, Raspberry Pi projects, home-lab services and, more recently, security patches and AI coding agents.

Most posts start as notes to myself. If a fix took me an evening to work out, it ends up here so the next person (often me, a year later) can do it in five minutes.

## Things I build

These are the open-source projects that many of the posts come out of:

- **[rpi-mqtt-monitor](https://github.com/hjelev/rpi-mqtt-monitor){:target="_blank" rel="noopener"}**: sends Raspberry Pi system stats to an MQTT broker and Home Assistant.
- **[The Terminal Index](https://cli.masoko.net){:target="_blank" rel="noopener"}**: a curated directory of 240+ open-source CLI and TUI tools.
- **[Shell Buddy](https://github.com/hjelev/sb){:target="_blank" rel="noopener"}**: a TUI file manager with batteries included.
- **[lyrtui](https://github.com/hjelev/lyrtui){:target="_blank" rel="noopener"}**: a fast terminal UI for Lyrion Music Server.
- **[lyr-radio-browser](https://github.com/hjelev/lyr-radio-browser){:target="_blank" rel="noopener"}**: a Lyrion plugin for the radio-browser.info station database.
- **[mp3-gallery](https://github.com/hjelev/mp3-gallery){:target="_blank" rel="noopener"}**: generates a static HTML gallery to host an MP3 collection.

This site is built with [Jekyll](https://jekyllrb.com/){:target="_blank" rel="noopener"} and hosted on [GitHub Pages](https://pages.github.com/){:target="_blank" rel="noopener"}. The source is [on GitHub](https://github.com/hjelev/blog){:target="_blank" rel="noopener"}.

## Get in touch

Found a mistake in a post, or something that no longer works? Send a message and I'll update it.

<form class="contact-form" action="https://formspree.io/f/xvodgobl" method="POST">
  <label>
    Your email
    <input type="email" name="_replyto" required autocomplete="email" placeholder="you@example.com">
  </label>
  <label>
    Your message
    <textarea name="message" required placeholder="Which post, and what's wrong or missing?"></textarea>
  </label>
  <input type="hidden" name="_subject" value="Message from blog.masoko.net">
  <input type="text" name="_gotcha" class="contact-form__trap" tabindex="-1" autocomplete="off" aria-hidden="true">
  <button type="submit">Send</button>
</form>
