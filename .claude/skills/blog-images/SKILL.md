---
name: blog-images
description: Design and produce the image set for a blog post in this Jekyll repo — a header plus 2–4 in-body figures (flow diagrams, before/after comparisons, terminal mockups, stat cards, decision trees, architecture sketches) as hand-written SVGs, rendered and visually checked, with the OG PNG generated and front matter wired. Use whenever writing a new post, when the user asks for images/diagrams/illustrations/headers for a post, or when an existing post has only one image.
---

# Blog images

Every post gets an **image set**, not a single header. Images are hand-written SVG in
`static/img/`, one consistent visual system, rendered to PNG and *looked at* before they ship.

## 1. Plan the set first (before drawing anything)

Read the whole post, then write a short plan listing each image, where it goes, and what
the reader learns from it that the text alone doesn't give quickly.

| Post length | Images |
|---|---|
| short (< 800 words) | header + 1 figure |
| normal | header + 2–3 figures |
| long guide / comparison | header + 3–4 figures |

Pick figure types from the catalogue (§3) that match the *content*, one per major section
at most. Good triggers:

- a sequence of steps or a request path → **flow**
- "before vs after", "works vs broken", "old vs new" → **compare**
- commands and their output → **terminal**
- 3–4 key numbers/facts → **stat cards**
- "which option should I pick" → **decision tree**
- components talking to each other (phone, router, server, VPN) → **architecture**
- app/tool status lists → **status grid** (only if a markdown table isn't already there)

Don't add a figure that just repeats a table or a code block that's already in the post.

## 2. Visual system (use these tokens exactly)

All images paint their own background, so they look right in both the light and dark site
themes. Default is the **dark card**, which matches the existing headers.

```
bg        #14161b   card background (rect rx="14")
panel     #1d2027   inner panels / boxes
panel-2   #262a33   raised boxes, terminal title bar
line      #343946   borders, dividers, connectors
text      #ffffff   primary text
muted     #9aa3b2   secondary text, labels
dim       #6b7180   tertiary text, grid
green     #4ec27a   ok / works / after
red       #f25f5c   broken / blocked / before
yellow    #febc2e   highlight / the thing to do / setting names
blue      #5b9cf5   neutral accent, links, data flow
orange    #f0883e   warnings, secondary accent
purple    #b48ead   rare third accent
```

Rules:
- **One accent per image is the hero**; green/red only for state. No more than 3 accent colours.
- Fonts: `font-family="JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"`
  for code, paths, terminal, labels; `"Atkinson Hyperlegible Next, -apple-system, Segoe UI, Helvetica, Arial, sans-serif"`
  for headings and prose in diagrams. (Both are self-hosted on the site; fallbacks keep it OK elsewhere.)
- Sizes at 1000-wide: title 34–44 bold, subtitle 17–19, body labels 15–17, small notes ≥ 13.
  Nothing under 13 — it'll be unreadable on phones.
- Padding: 60 px left/right margin on headers, 40 px on figures. Keep 24 px between groups.
- Boxes `rx="10"`, pills `rx` = half height, strokes 1.5–2, connectors 2 with arrow markers.
- Icons: draw simple geometric line icons (stroke 3–4, `stroke-linejoin="round"`), e.g. phone,
  server rack, router, shield, lock, cloud, folder, terminal window. For real products/apps, prefer
  the real logo from simple-icons (`https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/<slug>.svg`,
  inline the `<path>`, fill with the brand hex or white) over an invented drawing.
- Always escape `&` as `&amp;` and `<` as `&lt;` in `<text>`.

## 3. Build with svgkit (preferred) or templates

`scripts/svgkit.py` turns a short Python spec into a finished SVG in the house style, with
wrapping, arrow markers, real brand logos and line icons. Use it rather than hand-writing SVG:

```python
import sys; sys.path.insert(0, ".claude/skills/blog-images/scripts")
from svgkit import *
header("static/img/x-header.svg", kicker="Self-hosting · nginx", title=["Many Python apps,", "one nginx"],
       subtitle="Reverse proxy several Flask apps on one server", chip="proxy_pass :5001", accent="green",
       motif=[logo("nginx", 600, 120, 110), link(730, 175, 800, 175), icon("server", 820, 95, 150, accent="green")])
flow(path, title, steps=[dict(t="Browser", d="example.com"), dict(t="nginx", d=":443", state="green"), ...],
     arrows=[("HTTPS", "blue", None), None, ...], note="takeaway")
```

| Builder | Use for |
|---|---|
| `header` | 1000×360 header: kicker, 1–2 line title, subtitle, optional chip, `motif=[...]` in x 560–960 |
| `flow` | 3–5 steps left→right, per-step `state` (green/red/yellow/blue) or `dashed` |
| `compare` | two columns, before/after or option A/B, ✗/✓ bullets |
| `terminal` | real commands: `("$", cmd)`, `("out", ..)`, `("hl", ..)` yellow band, `("err", ..)`, `("ok", ..)` |
| `stats` | 3–4 big-number cards |
| `cards` | grid of tools/services with `logo=` (simple-icons slug) or `icon=`, optional tag |
| `bars` | horizontal bar comparison (prices, sizes, counts) |
| `timeline` | 3–6 dated events (CVE disclosure, release dates) |
| `checklist` | numbered steps; detail starting with `"$ "` renders as a command |
| `decision` | question → yes (green) / no (red) → optional row of options |
| `table` | small styled table (only if it isn't already a markdown table in the post) |
| `raw` | escape hatch for a custom body on the standard card |

Motif pieces: `icon(name, x, y, size, color, accent)` (see `ICONS`: phone, server, router,
laptop, desktop, window, terminal, shield, shield-check, lock, unlock, key, cloud, globe, folder,
file, cert, speaker, camera, bug, gear, package, chip, board, sdcard, git, wifi, list, check,
cross, block, warning, clock, calendar, house, database, code, user, users, dns, mail, rss,
chart, tag, bolt, search, font, plug, power, thermo, store, vpn, windows), `logo(slug, x, y, size)`,
`link()` dotted connector, `blocked()` / `ok_disc()` overlays, `mini_term()`, `pill()`, `badge()`.
Text accepts `**bold**` and `[[color|text]]` spans.

Logos come from `logos.json` (vendored simple-icons). To add one: `npm pack simple-icons@15.0.0`
into a scratch dir, extract it, then `python3 -I scripts/fetch_logos.py <dir>/package <slug>...`.
Windows has no simple-icons logo — use `icon("windows", ...)`.

Hand-editable starting points are also in `templates/` for one-off layouts.

### Worked examples and post-editing helpers

`examples/postedit.py` has helpers that place figures in a post: `header_md()` (sets the
header and the front matter `image:`/`thumbnail:`), `insert_before()`/`insert_after()` (after
the block containing a snippet), `replace_img()` and `remove_img()`. They're idempotent, so a
batch can be re-run after tweaking a spec. `examples/batch01.py` … `batch11.py` are the specs
that built every image on the blog (Nov 2026). Copy the closest one when starting a new post.

### Gotchas learned the hard way

- Nerd Font / private-use glyphs don't render in the SVGs. Use plain text or `icon()`.
- Runs of spaces collapse unless the text has `xml:space="preserve"` (terminal and mini_term already set it).
- Flow boxes get narrow with 5 steps: keep `d=` details short (the kit warns when one is too wide).
- Long card names collide with tags: the kit moves the tag below, but keep names to about 22 characters.
- `logo()` swaps near-black brand marks to white; pass `"text"` for dark brands (Anthropic, OpenAI, MQTT).
- Every claim in a figure must come from the post. Re-read the section before writing labels.
- A figure must not repeat a code block or table that is already in the post.

## 4. Files and naming

- `static/img/<slug>-header.svg` — header (`<slug>` = short post slug, already used for the header)
- `static/img/<slug>-<what>.svg` — figures, e.g. `android-17-local-network-flow.svg`
- `static/img/og/<slug>-header.png` — OG card, generated (§5), never hand-made

Front matter:
```yaml
image: /static/img/og/<slug>-header.png
thumbnail: /static/img/<slug>-header.svg
```

Embedding (always width/height = the viewBox, always descriptive alt text that states the
point of the image, optional italic caption on the next line):
```markdown
![Alt text that says what the figure shows and concludes](/static/img/<slug>-flow.svg){: width="1000" height="380"}
*Optional short caption.*
```
Header goes right after the front matter. Figures go right after the paragraph that
introduces the idea, never between a heading and its first paragraph.

## 5. Render, look, fix (mandatory)

```bash
.claude/skills/blog-images/scripts/check.sh static/img/<slug>-*.svg
```
This validates each SVG (XML, viewBox, fonts, text running off the canvas, tiny fonts) and
renders PNG previews into `$TMPDIR`/scratchpad (path printed). **Read every preview PNG** and
check for: overlapping text, clipped text, cramped spacing, misaligned arrows, unbalanced
empty space, low contrast. Fix and re-run until clean. Do not ship an image you haven't viewed.

Then generate the OG card from the header:
```bash
.claude/skills/blog-images/scripts/og.sh static/img/<slug>-header.svg
```
View the resulting PNG too.

## 6. Finish

- Report the image list (file, type, placement) to the user.
- Never commit — leave the files for the user to review.
