---
title: "Best TUI File Managers in 2026"
date: 2026-07-23
categories: [linux, macos, cli]
---

# Best TUI File Managers in 2026

Terminal file managers hit a sweet spot for a lot of people: faster than clicking through a GUI file browser, but with a real interface instead of typing `cd` and `ls` over and over. Below are some of the more actively-discussed options going into 2026, including a newer entry worth knowing about — **Shell Buddy**.


## Shell Buddy (sb)

[Shell Buddy](https://sb.masoko.net/) is a keyboard-driven TUI file manager written in Rust, built on the `ratatui` and `crossterm` libraries. It's a single binary aimed at people who want to stay in the terminal for as much of their workflow as possible, rather than dropping to a shell or a separate app for common tasks.

A few things that stand out from its feature list:

- **In-TUI Git workflow** — diff preview, status review, commit, and push without leaving the file manager.
- **AI-drafted commit messages** — generates a commit message from the diff (using Groq or GitHub Models) that you can edit before committing.
- **Inline path filters** — typing `^prefix`, `suffix$`, or `~contains` directly in the path bar live-filters the current listing.
- **One-key integration installs** — it can detect missing optional tools and install them via Homebrew from inside the TUI.
- **Age encryption** — encrypt or decrypt `.age` files in place with a single keypress.
- **Per-file notes** — attach notes to individual files, stored in a hidden `.sb` file per directory.
- **tmux-aware split panes** — `i` opens a shell + preview pane, `E` opens a shell + editor pane, and it falls back to `zellij` if tmux isn't installed.
- **CLI list/tree modes** — `sb -l`, `sb -t`, and `sb -l2` give consistent column output outside the interactive TUI, and `sb <file>` opens a file directly with the best available viewer.
- **Themeable** — ten-plus built-in themes (Nord, Dracula, Gruvbox, Rosé Pine, Everforest, and others), with Nerd Fonts and file-name colors toggled live from a themes menu.

Since it uses Nerd Font glyphs for its icons and theme indicators, it's worth installing one before you try it — see [our Nerd Fonts install guide](/nerd-fonts-what-why-how-to-install/) if you haven't set one up yet.

Install it with Cargo:

```bash
cargo install shell-buddy
```

More install options are on the [Shell Buddy install page](https://sb.masoko.net/install.html), and the source is on [GitHub](https://github.com/hjelev/sb).

## Yazi

[Yazi](https://github.com/sxyazi/yazi) is a Rust-based file manager built around async I/O, which lets it stay responsive even with large directories or image previews. It's gained a lot of attention over the past couple of years for its speed and its built-in image/media preview support. Like Shell Buddy, it's commonly recommended to be paired with a Nerd Font for its icons.

## ranger

[ranger](https://github.com/ranger/ranger) is one of the longer-standing options in this space — a Python, Vim-inspired file manager with a multi-column "miller columns" layout (you see the parent directory, current directory, and a preview of the selected item side by side). It ships with `rifle`, a file opener that tries to pick the right program for a given file type automatically. If you already use Vim, the keybindings will feel familiar immediately.

## nnn

[nnn](https://github.com/jarun/nnn) ("n³") bills itself as an "unorthodox" terminal file manager, and its main selling point is being extremely lightweight and fast while still supporting plugins for things like previews, bookmarks, and file type detection.

## lf

[lf](https://github.com/gokcehan/lf) ("list files") is written in Go and takes clear inspiration from ranger, but aims to be simpler and faster, with configuration done through a small shell-like config language rather than Python.

## superfile

[superfile](https://github.com/yorukot/superfile) is a newer, more visually polished TUI file manager aiming for a more modern look than some of the older tools in this list, with things like a sidebar, multiple panels, and mouse support alongside keyboard navigation.

## Walk (lk)

[Walk](https://github.com/antonmedv/walk) is a minimalist terminal navigator written in Go — less a full file manager and more a fast `cd`/`ls` replacement with fuzzy search, a preview pane, and image preview built in. The binary itself is called `walk`, but the typical setup wraps it in a shell function named `lk` that changes your shell's directory to wherever you navigated to on exit:

```bash
function lk {
  cd "$(walk "$@")"
}
```

Install it via Homebrew, `pkg_add`, or Go:

```bash
brew install walk
# or
go install github.com/antonmedv/walk@latest
```

Once set up, running `lk` drops you into the navigator; pressing `esc` or `q` exits back to your shell already `cd`'d into the last directory you were browsing, while `ctrl+c` exits without changing directory. It also supports Nerd Font icons with the `--icons` flag, in-TUI file deletion (`dd`, with undo via `u`), and yanking the current directory path.

## Midnight Commander (mc)

[Midnight Commander](https://midnight-commander.org/) deserves a mention for context — it's the classic dual-pane, function-key-driven file manager that predates most of the tools above by decades and is still packaged in nearly every Linux distro's repositories. If you want the most "battle-tested" option with the least chance of surprises, this is it.

## Picking one

If you're not sure where to start:

- Want the most modern feature set, with Git and file-encryption built in? Try **Shell Buddy**.
- Want fast async previews (including images)? Try **Yazi**.
- Already comfortable in Vim? Try **ranger** or **lf**.
- Want the smallest possible footprint? Try **nnn**.
- Just want a faster `cd`/`ls` with fuzzy search rather than a full file manager? Try **Walk** (`lk`).
- Want the tool that's been stable since before most of the others existed? Try **Midnight Commander**.

Whichever you pick, installing a [Nerd Font](/nerd-fonts-what-why-how-to-install/) first will make sure icons and status glyphs render correctly instead of showing as boxes.
