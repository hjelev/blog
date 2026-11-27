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

## 3. Catalogue

Templates live in `templates/`; copy one and edit — don't start from a blank file.

| Type | Template | viewBox | Notes |
|---|---|---|---|
| header | `header.svg` | 0 0 1000 360 | **Visual first**: a big illustrative motif on the right ~40 %, title (≤ 6 words) + one-line subtitle on the left. At most 3 short supporting lines. Not a wall of text — detail belongs in figures. |
| flow | `flow.svg` | 0 0 1000 300–420 | 3–5 boxes left→right with arrows; label arrows if meaningful; highlight the failing/important hop. |
| compare | `compare.svg` | 0 0 1000 380–460 | Two columns, red "before"/green "after" (or two options), same structure on each side so differences pop. |
| terminal | `terminal.svg` | 0 0 1000 300–480 | Window chrome (three dots), `$` prompt in green, output in muted, the key line highlighted in yellow/red. Use real commands from the post. |
| stat cards | `stats.svg` | 0 0 1000 260 | 3–4 cards, big number/word (40–56 px) + short label. |
| decision | `decision.svg` | 0 0 1000 420–520 | Question diamonds/pills → yes/no branches → outcome boxes (green = recommended). |
| architecture | build from flow/compare | 0 0 1000 400–520 | Icons for devices, grouped zones (LAN / internet) as dashed rounded rects with a label. |

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
