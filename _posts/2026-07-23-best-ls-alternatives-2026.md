---
title: "Best ls Alternatives in 2026"
date: 2026-07-23
categories: [linux, macos, cli]
---

# Best ls Alternatives in 2026

`ls` has been listing files the same basic way for decades, and for plain output it's still fine. But a handful of modern replacements add colored, icon-annotated, Git-aware output while staying just as fast (or close to it) — and they're common enough now that you'll see them in a lot of dotfiles repos. Here's a rundown of the main options.

## eza

[eza](https://github.com/eza-community/eza) is the most widely used option today, and it's specifically the **community-maintained continuation of `exa`** (more on that below) — `exa` was declared unmaintained, and a group of contributors forked it as `eza` to keep development going.

Notable features:

- Drop-in `ls` replacement — most people just `alias ls=eza`.
- Git integration (`eza --git`) shows tracked/modified/staged/untracked status per file.
- Support for extended file attributes, SELinux contexts on Linux, and clickable terminal hyperlinks.
- A `theme.yml` config file for customizing colors and per-file-type icons (icons render properly once you have a [Nerd Font](/nerd-fonts-what-why-how-to-install/) installed).
- Available for Linux, macOS, and Windows.

Install:

```bash
# macOS
brew install eza

# Cargo (any platform with Rust installed)
cargo install eza

# Debian/Ubuntu — needs a third-party repo, since eza isn't always in default repos
sudo mkdir -p /etc/apt/keyrings
wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc | sudo gpg --dearmor -o /etc/apt/keyrings/gierens.gpg
echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" | sudo tee /etc/apt/sources.list.d/gierens.list
sudo apt update
sudo apt install -y eza

# Windows (Scoop)
scoop install eza
```

Arch Linux, Fedora, NixOS, and several other package managers carry it too — see the [official install docs](https://github.com/eza-community/eza/blob/main/INSTALL.md) for the full list.

## lsd (LSDeluxe)

[lsd](https://github.com/lsd-rs/lsd) is another Rust rewrite of `ls`, and it was explicitly inspired by `colorls` (see below) but implemented in Rust for speed. Its main differentiator from eza is that it leans further into Nerd Font icons by default rather than as an opt-in — the project's own docs specifically recommend installing a patched Nerd Font (or Font Awesome) before using it, since icons are a core part of its default output.

Install:

```bash
# macOS / Linuxbrew
brew install lsd

# Cargo
cargo install lsd

# Debian sid/bookworm and Ubuntu 23.04+
sudo apt install lsd

# Windows (Scoop)
scoop install lsd
```

Once installed, alias it the same way as eza:

```bash
alias ls='lsd'
alias ll='lsd -l'
alias la='lsd -a'
alias lt='lsd --tree'
```

## exa (legacy — largely superseded)

[exa](https://github.com/ogham/exa) was the original modern `ls` replacement that both eza and lsd trace their lineage or inspiration back to. It's the tool that popularized this whole category — colored output, Git awareness, tree view — written in Rust. It has since been marked unmaintained by its original author, which is exactly why the `eza` fork exists. If you're starting fresh today, there's little reason to install `exa` specifically instead of `eza`; I'm including it here mainly for context, since you may still see it referenced in older blog posts or dotfiles.

## colorls

[colorls](https://github.com/athityakumar/colorls) takes a different approach from the other three: instead of a compiled binary, it's a **Ruby gem** that wraps `ls` output with Font Awesome icons and file-type-specific coloring. It was an early, influential entry in this space and directly inspired lsd's design.

Trade-offs to know about:

- Requires a Ruby runtime, which adds startup overhead compared to the Rust-based tools.
- Its development pace has slowed relative to eza and lsd.
- If you're already in a Ruby-heavy environment, though, it integrates naturally and doesn't require pulling in Rust/Cargo just for a file lister.

Install:

```bash
gem install colorls
```

## Picking one

- Want the most actively developed, most feature-complete option with strong Git integration? Go with **eza**.
- Want icons on by default and a very "at a glance" visual layout? Go with **lsd**.
- Already have a Ruby toolchain and don't want another Rust binary on the system? **colorls** is a reasonable, if slower, choice.
- Found `exa` referenced somewhere? Substitute **eza** — same lineage, actively maintained.

Whichever one you pick, install a [Nerd Font](/nerd-fonts-what-why-how-to-install/) first — all four of these rely on Nerd Font or Font Awesome glyphs for their icon output, and without one you'll just see broken-box placeholders instead of icons.
