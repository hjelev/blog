---
title: "Nerd Fonts: What They Are, Why You Need Them, and How to Install Them"
date: 2026-07-23
categories: [linux, macos, windows, cli]
---

# Nerd Fonts: What They Are, Why You Need Them, and How to Install Them

If you spend time in a terminal, you've probably seen screenshots where file listings, prompts, and status bars are full of clean little icons — a folder glyph next to directories, a language logo next to source files, a Git branch symbol in the prompt. Most of the time, that's not a special app doing custom rendering. It's just a **Nerd Font**.

## What is a Nerd Font?

[Nerd Fonts](https://www.nerdfonts.com/) is an open-source project (maintained on [GitHub](https://github.com/ryanoasis/nerd-fonts)) that takes existing popular monospace fonts — things like Fira Code, JetBrains Mono, Hack, or Cascadia Code — and "patches" them by adding thousands of extra glyphs. Those glyphs are pulled from icon sets such as Font Awesome, Devicons, Octicons, Powerline, Material Design Icons, and a few others, and merged into the font at code points that aren't used by normal text.

The result is a regular monospace coding font that *also* happens to contain icons for programming languages, file types, operating systems, Git status, and more — all renderable as a single character, at any font size, in any app that supports the font.

I'm not fully certain of the exact current glyph count in the latest release — the project has grown over time — so if that number matters to you, it's worth checking the count listed directly on the [Nerd Fonts website](https://www.nerdfonts.com/) or the project's GitHub releases page rather than trusting a fixed figure here.

## Why you need them

You don't strictly *need* a Nerd Font to use a terminal — but a lot of modern CLI and TUI (terminal UI) tools are designed with the assumption that one is installed, and they fall back to showing broken boxes (`▯`) or question marks when it isn't. Nerd Fonts matter if you use:

- **Prompt frameworks** like Starship or Powerlevel10k, which use icons and separators for Git status, language versions, and OS badges.
- **File managers and listers** that show a distinct icon per file type instead of plain text.
- **Status bars and window manager bars** (e.g. in tmux, polybar, or i3status) that use icons for battery, volume, or workspace indicators.
- **Editor/IDE plugins** inside terminal-based editors like Neovim, where file-tree and fuzzy-finder plugins commonly rely on icon glyphs.

Without a patched font, none of this breaks functionally — the tools still work — but you'll see missing-character boxes instead of the intended icons.

### Tools that specifically benefit from a Nerd Font

A few CLI tools worth calling out from [previous posts on this blog](https://blog.masoko.net/ubuntu/Useful-cli-tools/) look noticeably better with a Nerd Font installed:

- **[exa](https://github.com/ogham/exa)** — a modern replacement for `ls`. Its `--icons` flag prints a file-type icon next to each entry, but that flag only renders correctly with a Nerd Font active in your terminal.
- **[btop](https://github.com/aristocratos/btop)** — the resource monitor covered in the [Useful CLI tools](https://blog.masoko.net/ubuntu/Useful-cli-tools/) post. I'm not fully certain every symbol in its default theme requires a patched font specifically (some are just Unicode box-drawing characters), but its bundled themes are commonly recommended to be paired with a Nerd Font — worth checking btop's own documentation if you want to confirm exactly which glyphs need it.
- **[duf](https://github.com/muesli/duf)** — the disk usage utility from the same post; its table borders and bars render more consistently with a Nerd Font-based terminal font.

If you're setting up any of these, installing a Nerd Font first will save you from wondering why the icons look wrong.

## How to install Nerd Fonts

The general idea is the same on every platform: download (or install via package manager) one or more patched font files, register them with your OS, then set your terminal or editor to actually use that font — installing it alone isn't enough, you also have to select it in your terminal's font settings.

### Linux

Manual method (works on any distro):

```bash
mkdir -p ~/.local/share/fonts
cd ~/.local/share/fonts
curl -fLo "JetBrainsMono.zip" https://github.com/ryanoasis/nerd-fonts/releases/latest/download/JetBrainsMono.zip
unzip JetBrainsMono.zip -d JetBrainsMono
rm JetBrainsMono.zip
fc-cache -fv
```

Swap `JetBrainsMono` for whichever font family you prefer — the [Nerd Fonts releases page](https://github.com/ryanoasis/nerd-fonts/releases) lists all available families as separate zip downloads.

Package-manager options exist too, though availability varies by distro:

```bash
# Arch Linux (AUR)
yay -S ttf-jetbrains-mono-nerd
# or, everything at once (large download):
yay -S nerd-fonts-complete
```

I don't have a confirmed, verified list of which font families are packaged for Fedora, openSUSE, or Debian/Ubuntu repos at this moment — package availability shifts, so it's worth checking your distro's package search before assuming a given family is packaged.

### macOS

The easiest route is Homebrew, since Nerd Font casks now live directly in the main `homebrew/cask` repository (no separate tap needed as of mid-2024):

```bash
brew install --cask font-jetbrains-mono-nerd-font
brew install --cask font-fira-code-nerd-font
brew install --cask font-hack-nerd-font
```

You can search for other available families with `brew search nerd-font`. Fonts install to `~/Library/Fonts/` and are available immediately — no cache rebuild step needed.

If you'd rather not use Homebrew, download the zip for your chosen font from the [Nerd Fonts releases page](https://github.com/ryanoasis/nerd-fonts/releases), unzip it, select all the `.ttf` files, and double-click (or right-click → "Install for all users" if you want it available system-wide).

### Windows

A few options, in rough order of convenience:

**Manual install:**
1. Download the zip for your chosen font family from the [Nerd Fonts releases page](https://github.com/ryanoasis/nerd-fonts/releases).
2. Extract it.
3. Select all the `.ttf` files, right-click, and choose **Install** (or **Install for all users**, which needs admin rights).

**Using Scoop:**

```powershell
scoop bucket add nerd-fonts
scoop install JetBrainsMono-NF
```

The exact package name can vary between font families, so use `scoop search nerd-font` to confirm the correct name before installing — I'd rather point you to verify this than give you a name that turns out to be wrong for the specific font you want.

**Using Chocolatey:** some Nerd Font packages exist on the Chocolatey community repo, but from what I found this isn't an official Nerd Fonts distribution channel, just community-maintained packages — worth checking the package page on `community.chocolatey.org` before relying on it.

### After installing, on any platform

Installing the font is only half the job. Open your terminal emulator's settings (Windows Terminal, iTerm2, GNOME Terminal, Alacritty, Kitty, etc.) and set the font explicitly to the Nerd Font variant — it will usually show up with "Nerd Font" appended to its name, e.g. "JetBrainsMono Nerd Font". Some terminals also need this set in a config file rather than a GUI setting; check your specific terminal's docs if the font picker doesn't show it.

## A quick note on this post

I pulled the install commands above from current documentation and package pages rather than from memory alone, since font package names and distribution methods change over time (the Homebrew cask-fonts tap deprecation being one recent example). Even so, it's worth double-checking `scoop search`, `brew search`, or your distro's package index at install time in case something has shifted since this was written.
