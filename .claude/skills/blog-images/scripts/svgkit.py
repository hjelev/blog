"""svgkit: build blog images in the house style from short Python specs.

    import sys; sys.path.insert(0, ".claude/skills/blog-images/scripts")
    from svgkit import *
    header("static/img/foo-header.svg", kicker="SELF-HOSTING", title=["Short title", "line two"],
           subtitle="What you'll learn", chip="key › value",
           motif=[icon("phone", 600, 100, 160), link(700, 180, 860, 180), logo("nginx", 860, 120, 110)])

Every builder writes a complete SVG (viewBox 1000 wide, own background) and returns the path.
Coordinates are in viewBox units. Colours: use the names in C (or any hex).
"""
import json, os, re
from xml.sax.saxutils import escape as _esc

C = dict(bg="#14161b", panel="#1d2027", panel2="#262a33", line="#343946", text="#ffffff",
         muted="#9aa3b2", dim="#6b7180", green="#4ec27a", red="#f25f5c", yellow="#febc2e",
         blue="#5b9cf5", orange="#f0883e", purple="#b48ead", term="#0d0f13")
TINT = dict(green="#16291f", red="#2a1a1c", yellow="#2b2615", blue="#172235", orange="#2b1f15",
            purple="#251e26")
SANS = "Atkinson Hyperlegible Next, -apple-system, Segoe UI, Helvetica, Arial, sans-serif"
MONO = "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
_LOGOS = None


def col(c):
    return C.get(c, c)


def esc(s):
    return _esc(str(s), {'"': "&quot;"})


# ---------------------------------------------------------------- text helpers
def text_w(s, size, mono=False, bold=False):
    """Rough rendered width of a string in px."""
    if mono:
        return len(s) * size * 0.6
    w = 0.0
    for ch in s:
        if ch in "il.,:;'|!·": w += 0.28
        elif ch in "fjrt()[]- ": w += 0.36
        elif ch in "mwMW@": w += 0.86
        elif ch.isupper() or ch.isdigit(): w += 0.64
        else: w += 0.53
    return w * size * (1.06 if bold else 1.0)


def wrap(s, max_w, size, mono=False, bold=False):
    words, lines, cur = str(s).split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if cur and text_w(t, size, mono, bold) > max_w:
            lines.append(cur); cur = w
        else:
            cur = t
    if cur: lines.append(cur)
    return lines


def T(x, y, s, size=16, fill="text", bold=False, mono=False, anchor="start", extra=""):
    """A <text> element. `s` may contain [[color|text]] spans and **bold** spans."""
    fam = MONO if mono else SANS
    body = esc(s)
    body = re.sub(r"\*\*(.+?)\*\*", r'<tspan font-weight="700">\1</tspan>', body)
    body = re.sub(r"\[\[(\w+)\|(.+?)\]\]", lambda m: f'<tspan fill="{col(m.group(1))}">{m.group(2)}</tspan>', body)
    w = ' font-weight="700"' if bold else ""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (f'<text x="{x:g}" y="{y:g}" font-family="{fam}" font-size="{size}" fill="{col(fill)}"'
            f'{w}{a} {extra}>{body}</text>')


def TL(x, y, s, max_w, size=16, lh=None, **kw):
    """Wrapped multi-line text; returns (svg, height)."""
    lh = lh or round(size * 1.4)
    lines = wrap(s, max_w, size, kw.get("mono", False), kw.get("bold", False))
    return "".join(T(x, y + i * lh, l, size, **kw) for i, l in enumerate(lines)), lh * len(lines)


def box(x, y, w, h, fill="panel", stroke="line", rx=10, sw=1.5, dash=None, opacity=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' fill-opacity="{opacity}"' if opacity is not None else ""
    s = f' stroke="{col(stroke)}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" fill="{col(fill)}"{o}{s}{d}/>'


def state_box(x, y, w, h, state=None, dashed=False):
    if state in TINT:
        return box(x, y, w, h, TINT[state], state, sw=2)
    return box(x, y, w, h, "panel", "line", dash="6 5" if dashed else None)


def arrow(x1, y1, x2, y2, color="dim", dash=None, curve=None, sw=2, head=True):
    """Straight arrow, or a cubic curve when curve=(cx1,cy1,cx2,cy2)."""
    c = col(color)
    d = f"M{x1:g} {y1:g} " + (f"C {curve[0]:g} {curve[1]:g}, {curve[2]:g} {curve[3]:g}, " if curve else "L") + f"{x2:g} {y2:g}"
    da = f' stroke-dasharray="{dash}"' if dash else ""
    mk = f' marker-end="url(#m{c[1:]})"' if head else ""
    return f'<path d="{d}" stroke="{c}" stroke-width="{sw}" fill="none"{da}{mk}/>'


def link(x1, y1, x2, y2, color="muted", sw=4):
    """Dotted 'connection' line for header motifs."""
    return (f'<path d="M{x1:g} {y1:g} L{x2:g} {y2:g}" stroke="{col(color)}" stroke-width="{sw}" '
            f'stroke-dasharray="2 10" stroke-linecap="round" fill="none"/>')


def pill(x, y, s, color="yellow", size=15, h=40, mono=True, fill="panel2"):
    w = text_w(s, size, mono) + 44
    return (box(x, y, w, h, fill, "line", rx=h / 2) +
            T(x + 22, y + h / 2 + size * 0.36, s, size, color, mono=mono)), w


def badge(x, y, s, color="green", size=13):
    w = text_w(s, size, True) + 20
    return (box(x, y, w, 24, TINT.get(color, "panel2"), color, rx=12, sw=1.2) +
            T(x + w / 2, y + 16.5, s, size, color, mono=True, anchor="middle")), w


# ---------------------------------------------------------------- logos & icons
def logo(slug, x, y, size, color=None, plate=False):
    """simple-icons logo (vendored in logos.json) in a size×size square. color=None → brand hex,
    'text' → white. plate=True draws a rounded panel behind it."""
    global _LOGOS
    if _LOGOS is None:
        _LOGOS = json.load(open(os.path.join(os.path.dirname(__file__), "..", "logos.json")))
    if slug not in _LOGOS:
        raise KeyError(f"logo {slug!r} not vendored; run scripts/fetch_logos.py")
    L = _LOGOS[slug]
    fill = col(color) if color else "#" + L["hex"]
    if fill.lower() in ("#000000", "#181717", "#111111", "#000"):
        fill = "#ffffff"  # black brand marks are invisible on the dark card
    out = ""
    if plate:
        out += box(x - size * 0.22, y - size * 0.22, size * 1.44, size * 1.44, "panel", "line", rx=size * 0.3)
    s = size / 24
    return out + f'<g transform="translate({x:g} {y:g}) scale({s:.4f})"><path d="{L["path"]}" fill="{fill}"/></g>'


def _ic(body, x, y, size, color, sw):
    s = size / 100
    return (f'<g transform="translate({x:g} {y:g}) scale({s:.4f})" fill="none" stroke="{col(color)}" '
            f'stroke-width="{sw / s:.2f}" stroke-linejoin="round" stroke-linecap="round">{body}</g>')


# 100×100 line icons. Use `A` as a placeholder for the accent colour where an icon has one.
ICONS = {
    "phone": '<rect x="26" y="4" width="48" height="92" rx="9"/><line x1="43" y1="86" x2="57" y2="86"/>',
    "server": '<rect x="12" y="8" width="76" height="24" rx="5"/><rect x="12" y="38" width="76" height="24" rx="5"/><rect x="12" y="68" width="76" height="24" rx="5"/><line x1="24" y1="20" x2="48" y2="20"/><line x1="24" y1="50" x2="48" y2="50"/><line x1="24" y1="80" x2="48" y2="80"/><circle cx="74" cy="20" r="2.5" fill="A" stroke="none"/><circle cx="74" cy="50" r="2.5" fill="A" stroke="none"/><circle cx="74" cy="80" r="2.5" fill="A" stroke="none"/>',
    "router": '<rect x="8" y="52" width="84" height="30" rx="7"/><line x1="28" y1="52" x2="20" y2="22"/><line x1="72" y1="52" x2="80" y2="22"/><circle cx="26" cy="67" r="3" fill="A" stroke="none"/><circle cx="40" cy="67" r="3" fill="A" stroke="none"/><line x1="58" y1="67" x2="80" y2="67"/>',
    "laptop": '<rect x="18" y="20" width="64" height="44" rx="5"/><path d="M6 76 H94 L86 64 H14 Z"/>',
    "desktop": '<rect x="8" y="12" width="84" height="56" rx="6"/><line x1="50" y1="68" x2="50" y2="84"/><line x1="32" y1="86" x2="68" y2="86"/>',
    "window": '<rect x="8" y="14" width="84" height="72" rx="8"/><line x1="8" y1="32" x2="92" y2="32"/><circle cx="20" cy="23" r="2.5" fill="A" stroke="none"/><circle cx="30" cy="23" r="2.5" stroke="none" fill="A"/>',
    "terminal": '<rect x="6" y="14" width="88" height="72" rx="8"/><path d="M22 40 L36 50 L22 60"/><line x1="44" y1="62" x2="64" y2="62"/>',
    "shield": '<path d="M50 6 L86 20 V48 C86 70 70 86 50 94 C30 86 14 70 14 48 V20 Z"/>',
    "shield-check": '<path d="M50 6 L86 20 V48 C86 70 70 86 50 94 C30 86 14 70 14 48 V20 Z"/><path d="M34 50 L46 62 L68 38" stroke="A"/>',
    "lock": '<rect x="18" y="44" width="64" height="48" rx="8"/><path d="M32 44 V30 a18 18 0 0 1 36 0 V44"/><circle cx="50" cy="66" r="5" fill="A" stroke="none"/>',
    "unlock": '<rect x="18" y="44" width="64" height="48" rx="8"/><path d="M32 44 V30 a18 18 0 0 1 34 -8"/><circle cx="50" cy="66" r="5" fill="A" stroke="none"/>',
    "key": '<circle cx="30" cy="50" r="18"/><path d="M48 50 H92 M78 50 V64 M90 50 V60"/>',
    "cloud": '<path d="M28 78 H74 a18 18 0 0 0 2 -36 a26 26 0 0 0 -50 -4 a20 20 0 0 0 2 40 Z"/>',
    "globe": '<circle cx="50" cy="50" r="40"/><ellipse cx="50" cy="50" rx="17" ry="40"/><line x1="10" y1="50" x2="90" y2="50"/><path d="M16 30 H84 M16 70 H84"/>',
    "folder": '<path d="M8 26 a6 6 0 0 1 6 -6 H38 L46 30 H86 a6 6 0 0 1 6 6 V78 a6 6 0 0 1 -6 6 H14 a6 6 0 0 1 -6 -6 Z"/>',
    "file": '<path d="M24 6 H60 L80 26 V94 H24 Z"/><path d="M60 6 V26 H80"/><line x1="36" y1="48" x2="68" y2="48"/><line x1="36" y1="62" x2="68" y2="62"/><line x1="36" y1="76" x2="56" y2="76"/>',
    "cert": '<rect x="8" y="14" width="84" height="58" rx="6"/><line x1="22" y1="32" x2="62" y2="32"/><line x1="22" y1="46" x2="52" y2="46"/><circle cx="72" cy="62" r="12" stroke="A"/><path d="M66 72 L62 92 L72 86 L82 92 L78 72" stroke="A"/>',
    "speaker": '<rect x="22" y="6" width="56" height="88" rx="9"/><circle cx="50" cy="60" r="18"/><circle cx="50" cy="60" r="5" fill="A" stroke="none"/><circle cx="50" cy="24" r="6"/>',
    "camera": '<rect x="6" y="28" width="66" height="44" rx="7"/><path d="M72 42 L94 30 V70 L72 58"/><circle cx="22" cy="42" r="3.5" fill="A" stroke="none"/>',
    "bug": '<ellipse cx="50" cy="56" rx="22" ry="30"/><path d="M38 28 a12 12 0 0 1 24 0"/><path d="M28 46 H12 M28 62 H10 M30 78 L16 88 M72 46 H88 M72 62 H90 M70 78 L84 88"/><line x1="50" y1="34" x2="50" y2="84"/>',
    "gear": '<circle cx="50" cy="50" r="14"/><path d="M50 8 V22 M50 78 V92 M8 50 H22 M78 50 H92 M20 20 L30 30 M70 70 L80 80 M80 20 L70 30 M30 70 L20 80"/><circle cx="50" cy="50" r="30"/>',
    "package": '<path d="M50 6 L90 26 V74 L50 94 L10 74 V26 Z"/><path d="M10 26 L50 46 L90 26 M50 46 V94"/>',
    "chip": '<rect x="24" y="24" width="52" height="52" rx="6"/><rect x="38" y="38" width="24" height="24" rx="3" stroke="A"/><path d="M36 8 V24 M50 8 V24 M64 8 V24 M36 76 V92 M50 76 V92 M64 76 V92 M8 36 H24 M8 50 H24 M8 64 H24 M76 36 H92 M76 50 H92 M76 64 H92"/>',
    "board": '<rect x="6" y="18" width="88" height="64" rx="6"/><rect x="40" y="38" width="22" height="22" rx="2" stroke="A"/><path d="M14 26 H62" stroke-dasharray="3 5"/><rect x="72" y="56" width="22" height="18" rx="2"/><rect x="14" y="62" width="16" height="12" rx="2"/>',
    "sdcard": '<path d="M24 6 H70 L84 20 V94 H24 Z"/><path d="M38 6 V22 M50 6 V22 M62 6 V22"/>',
    "git": '<circle cx="28" cy="20" r="9"/><circle cx="28" cy="80" r="9"/><circle cx="74" cy="40" r="9" stroke="A"/><line x1="28" y1="29" x2="28" y2="71"/><path d="M74 49 C74 66 28 58 28 71"/>',
    "wifi": '<path d="M10 40 a56 56 0 0 1 80 0 M24 55 a36 36 0 0 1 52 0 M38 70 a16 16 0 0 1 24 0"/><circle cx="50" cy="84" r="4" fill="A" stroke="none"/>',
    "list": '<path d="M34 24 H90 M34 50 H90 M34 76 H90"/><circle cx="16" cy="24" r="4" fill="A" stroke="none"/><circle cx="16" cy="50" r="4" fill="A" stroke="none"/><circle cx="16" cy="76" r="4" fill="A" stroke="none"/>',
    "check": '<circle cx="50" cy="50" r="40"/><path d="M32 52 L45 65 L70 38" stroke="A"/>',
    "cross": '<circle cx="50" cy="50" r="40"/><path d="M35 35 L65 65 M65 35 L35 65" stroke="A"/>',
    "block": '<circle cx="50" cy="50" r="40"/><line x1="22" y1="22" x2="78" y2="78"/>',
    "warning": '<path d="M50 8 L94 88 H6 Z"/><line x1="50" y1="38" x2="50" y2="60" stroke="A"/><circle cx="50" cy="73" r="3" fill="A" stroke="none"/>',
    "clock": '<circle cx="50" cy="50" r="40"/><path d="M50 26 V50 L66 60" stroke="A"/>',
    "calendar": '<rect x="10" y="18" width="80" height="72" rx="8"/><line x1="10" y1="38" x2="90" y2="38"/><path d="M30 8 V26 M70 8 V26"/><rect x="26" y="52" width="14" height="12" rx="2" fill="A" stroke="none"/>',
    "house": '<path d="M10 48 L50 12 L90 48"/><path d="M20 40 V88 H80 V40"/><rect x="42" y="60" width="16" height="28"/>',
    "database": '<ellipse cx="50" cy="20" rx="36" ry="12"/><path d="M14 20 V80 a36 12 0 0 0 72 0 V20"/><path d="M14 50 a36 12 0 0 0 72 0"/>',
    "code": '<path d="M34 26 L10 50 L34 74 M66 26 L90 50 L66 74 M58 16 L42 84"/>',
    "user": '<circle cx="50" cy="32" r="18"/><path d="M14 92 a36 36 0 0 1 72 0"/>',
    "users": '<circle cx="36" cy="34" r="15"/><path d="M8 88 a28 28 0 0 1 56 0"/><circle cx="68" cy="30" r="12"/><path d="M66 56 a26 26 0 0 1 28 28"/>',
    "dns": '<circle cx="50" cy="50" r="40"/><ellipse cx="50" cy="50" rx="17" ry="40"/><line x1="10" y1="50" x2="90" y2="50"/>',
    "mail": '<rect x="8" y="20" width="84" height="60" rx="7"/><path d="M8 26 L50 56 L92 26"/>',
    "rss": '<path d="M16 16 a68 68 0 0 1 68 68 M16 42 a42 42 0 0 1 42 42"/><circle cx="22" cy="78" r="6" fill="A" stroke="none"/>',
    "chart": '<path d="M10 10 V90 H90"/><rect x="24" y="52" width="12" height="30" fill="A" stroke="none"/><rect x="44" y="34" width="12" height="48" fill="A" stroke="none"/><rect x="64" y="20" width="12" height="62" fill="A" stroke="none"/>',
    "tag": '<path d="M8 50 V14 a6 6 0 0 1 6 -6 H50 L92 50 L50 92 Z"/><circle cx="28" cy="28" r="6" fill="A" stroke="none"/>',
    "bolt": '<path d="M56 6 L18 56 H48 L42 94 L82 42 H52 Z"/>',
    "search": '<circle cx="42" cy="42" r="28"/><line x1="62" y1="62" x2="90" y2="90"/>',
    "font": '<path d="M12 86 L36 14 L60 86 M20 62 H52"/><path d="M88 86 V58 a14 14 0 1 0 0 1 M88 60 a14 14 0 1 1 0 1"/>',
    "plug": '<path d="M34 8 V30 M66 8 V30"/><path d="M22 30 H78 V50 a28 28 0 0 1 -56 0 Z"/><line x1="50" y1="78" x2="50" y2="94"/>',
    "power": '<path d="M30 24 a36 36 0 1 0 40 0"/><line x1="50" y1="8" x2="50" y2="48"/>',
    "thermo": '<path d="M40 60 V16 a10 10 0 0 1 20 0 V60 a20 20 0 1 1 -20 0"/><circle cx="50" cy="76" r="8" fill="A" stroke="none"/>',
    "store": '<path d="M10 36 L18 12 H82 L90 36"/><path d="M10 36 H90 a12 12 0 0 1 -26 0 a12 12 0 0 1 -26 0 a12 12 0 0 1 -26 0"/><path d="M16 44 V90 H84 V44"/><rect x="40" y="62" width="20" height="28"/>',
    "vpn": '<path d="M50 6 L86 20 V48 C86 70 70 86 50 94 C30 86 14 70 14 48 V20 Z"/><rect x="34" y="46" width="32" height="24" rx="4" stroke="A"/><path d="M40 46 V38 a10 10 0 0 1 20 0 V46" stroke="A"/>',
    "windows": '<rect x="10" y="10" width="36" height="36" rx="3" stroke="A"/><rect x="54" y="10" width="36" height="36" rx="3" stroke="A"/><rect x="10" y="54" width="36" height="36" rx="3" stroke="A"/><rect x="54" y="54" width="36" height="36" rx="3" stroke="A"/>',
}


def icon(name, x, y, size, color="muted", accent=None, sw=4):
    """Line icon in a size×size square at (x, y)."""
    body = ICONS[name].replace('"A"', f'"{col(accent or color)}"')
    return _ic(body, x, y, size, color, sw)


def blocked(cx, cy, r=34, color="red", sw=5):
    """Red 'no entry' disc that sits on top of a connection."""
    c = col(color)
    d = r * 0.68
    return (f'<circle cx="{cx:g}" cy="{cy:g}" r="{r}" fill="{C["bg"]}" stroke="{c}" stroke-width="{sw}"/>'
            f'<line x1="{cx - d:g}" y1="{cy - d:g}" x2="{cx + d:g}" y2="{cy + d:g}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>')


def ok_disc(cx, cy, r=30, color="green", sw=5):
    c = col(color)
    return (f'<circle cx="{cx:g}" cy="{cy:g}" r="{r}" fill="{C["bg"]}" stroke="{c}" stroke-width="{sw}"/>'
            f'<path d="M{cx - r * .45:g} {cy + r * .02:g} L{cx - r * .1:g} {cy + r * .38:g} L{cx + r * .5:g} {cy - r * .35:g}" '
            f'stroke="{c}" stroke-width="{sw}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def mini_term(x, y, w, lines, size=15, title=None):
    """Small terminal window for header motifs. lines: list of strings with [[color|..]] markup."""
    lh = round(size * 1.6)
    h = 44 + lh * len(lines) + 10
    out = box(x, y, w, h, "term", "line", rx=10)
    out += f'<path d="M{x} {y + 10} a10 10 0 0 1 10 -10 h{w - 20} a10 10 0 0 1 10 10 v20 h-{w} z" fill="{C["panel2"]}"/>'
    for i, c in enumerate(("red", "yellow", "green")):
        out += f'<circle cx="{x + 18 + i * 16}" cy="{y + 15}" r="5" fill="{C[c]}"/>'
    if title:
        out += T(x + w / 2, y + 20, title, 13, "dim", mono=True, anchor="middle")
    for i, l in enumerate(lines):
        out += T(x + 16, y + 52 + i * lh, l, size, "muted", mono=True, extra='xml:space="preserve"')
    return out


# ---------------------------------------------------------------- document shell
def _markers(svg):
    cols = sorted(set(re.findall(r'url\(#m([0-9a-fA-F]{6})\)', svg)))
    return "".join(f'<marker id="m{c}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                   f'orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#{c}"/></marker>' for c in cols)


def write(path, w, h, body, defs=""):
    defs = defs + _markers(body)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{SANS}">\n'
           + (f"<defs>{defs}</defs>\n" if defs else "")
           + f'<rect width="{w}" height="{h}" rx="14" fill="{C["bg"]}"/>\n' + body + "\n</svg>\n")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    return path


def _title(title, sub, x=40):
    out, y = "", 52
    if title:
        out += T(x, y, title, 22, bold=True)
    if sub:
        out += T(x, y + 28, sub, 15, "muted")
    return out, (100 if sub else 78) if title else 30


# ---------------------------------------------------------------- builders
def header(path, kicker, title, subtitle, chip=None, motif=(), accent="blue", chip_color="yellow"):
    """1000×360 header. title: list of 1–2 lines (≤ ~16 chars each at 44px). motif: list of SVG
    strings placed in the right ~40% (x 560–960, y 50–310)."""
    a = col(accent)
    defs = (f'<radialGradient id="glow" cx="76%" cy="50%" r="44%"><stop offset="0" stop-color="{a}" stop-opacity="0.2"/>'
            f'<stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>'
            f'<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{C["line"]}"/></pattern>')
    title = [title] if isinstance(title, str) else title
    big = 44 if max(text_w(t, 44, bold=True) for t in title) < 470 else 38
    lines = len(title)
    top = 92 if lines == 2 else 112
    body = (f'<rect x="540" y="0" width="460" height="360" fill="url(#grid)" opacity="0.6"/>'
            f'<rect width="1000" height="360" rx="14" fill="url(#glow)"/>')
    body += T(60, top, kicker.upper(), 15, accent, mono=True, extra='letter-spacing="2"')
    y = top + 56
    for t in title:
        body += T(60, y, t, big, bold=True); y += big + 8
    y += 0
    st, sh = TL(60, y, subtitle, 450, 19, fill="muted")
    body += st; y += sh
    if chip:
        p, _ = pill(60, y + 4, chip, chip_color)
        body += p
    body += "".join(motif)
    return write(path, 1000, 360, body, defs)


def flow(path, title, steps, sub=None, note=None, arrows=None, h=None, step_h=90):
    """Left→right boxes. steps: list of dicts {t, d, state(green/red/yellow/blue/None), dashed, icon, logo}.
    arrows: list of (label, color, dashed) per gap (or None)."""
    head, top = _title(title, sub)
    n = len(steps)
    labw = max([text_w(a[0], 13, True) for a in (arrows or []) if a and a[0]] or [0])
    gap = max(56, labw + 24)
    bw = (920 - gap * (n - 1)) / n
    y = top + 34
    out = head
    for i, s in enumerate(steps):
        x = 40 + i * (bw + gap)
        out += state_box(x, y, bw, step_h, s.get("state"), s.get("dashed"))
        cx = x + bw / 2
        ty = y + step_h / 2 - (6 if s.get("d") else -6)
        if s.get("icon") or s.get("logo"):
            pass
        faded = s.get("dashed")
        lines = wrap(s["t"], bw - 24, 16, bold=True)
        dl = wrap(s.get("d", ""), bw - 20, 14, mono=True) if s.get("d") else []
        for l in dl:
            if text_w(l, 14, True) > bw - 12:
                print(f"warn: flow detail too wide for its box: {l!r} (shorten it)")
        total = len(lines) * 21 + len(dl) * 19
        ty = y + (step_h - total) / 2 + 15
        for l in lines:
            out += T(cx, ty, l, 16, "dim" if faded else "text", bold=True, anchor="middle"); ty += 21
        for l in dl:
            out += T(cx, ty + 2, l, 14, s.get("state") or ("dim" if faded else "muted"), mono=True, anchor="middle"); ty += 19
        if i < n - 1:
            lab, colr, dsh = (arrows[i] if arrows and arrows[i] else (None, "dim", None))
            ay = y + step_h / 2
            out += arrow(x + bw + 4, ay, x + bw + gap - 6, ay, colr, dsh)
            if lab:
                out += T(x + bw + gap / 2, ay - 10, lab, 13, colr, mono=True, anchor="middle")
    yy = y + step_h + 40
    if note:
        nt, nh = TL(40, yy, note, 920, 15, fill="yellow")
        out += nt; yy += nh
    H = h or int(yy + 10)
    return write(path, 1000, H, out)


def compare(path, left, right, title=None, sub=None, h=None):
    """Two columns. left/right: {kicker, title, items:[str], foot, state('red'/'green'/...), mark('✗'/'✓'/'•')}"""
    head, top = _title(title, sub)
    out = head
    y0 = top + (10 if title else 10)
    cols = []
    for i, c in enumerate((left, right)):
        x = 40 + i * 480
        st = c.get("state", "blue")
        mark = c.get("mark", {"red": "✗", "green": "✓"}.get(st, "•"))
        inner = T(x + 30, y0 + 50, c.get("kicker", "").upper(), 14, st, mono=True, extra='letter-spacing="2"')
        ty = y0 + 84
        tt, th = TL(x + 30, ty, c["title"], 380, 24, bold=True)
        inner += tt; ty += th + 18
        for it in c["items"]:
            lines = wrap(it, 360, 16)
            inner += T(x + 30, ty, mark, 16, st, bold=True)
            for j, l in enumerate(lines):
                inner += T(x + 56, ty + j * 22, l, 16, "muted")
            ty += 22 * len(lines) + 12
        if c.get("foot"):
            ty += 14
            ft, fh = TL(x + 30, ty, c["foot"], 380, 14, fill="dim", mono=True)
            inner += ft; ty += fh
        cols.append((x, st, inner, ty))
    bottom = max(c[3] for c in cols) + 18
    for x, st, inner, _ in cols:
        out += box(x, y0, 440, bottom - y0, "panel", "line", rx=12)
        out += f'<rect x="{x}" y="{y0}" width="440" height="6" rx="3" fill="{col(st)}"/>' + inner
    return write(path, 1000, h or int(bottom + 40), out)


def terminal(path, lines, title=None, sub=None, win="user@homelab: ~", size=16):
    """Terminal window. lines: list of (kind, text). kind: '$' prompt, 'out', 'hl' (yellow band),
    'err' (red band), 'ok' (green text), 'dim', '' (blank). Text may use [[color|..]] markup."""
    head, top = _title(title, sub)
    lh = round(size * 1.85)
    y0 = top
    hgt = 70 + lh * len(lines)
    out = head + box(40, y0, 920, hgt, "term", "line")
    out += f'<path d="M40 {y0 + 10} a10 10 0 0 1 10 -10 h900 a10 10 0 0 1 10 10 v28 h-920 z" fill="{C["panel2"]}"/>'
    for i, c in enumerate(("red", "yellow", "green")):
        out += f'<circle cx="{66 + i * 22}" cy="{y0 + 20}" r="6" fill="{C[c]}"/>'
    out += T(500, y0 + 25, win, 14, "muted", mono=True, anchor="middle")
    y = y0 + 80
    for kind, txt in lines:
        if kind == "$":
            out += T(64, y, "[[green|$]] " + txt, size, "text", mono=True, extra='xml:space="preserve"')
        elif kind in ("hl", "err", "okb"):
            c = {"hl": "yellow", "err": "red", "okb": "green"}[kind]
            out += f'<rect x="56" y="{y - lh * 0.68:g}" width="888" height="{lh * 0.92:g}" rx="4" fill="{C[c]}" fill-opacity="0.13"/>'
            out += T(64, y, txt, size, c, mono=True, extra='xml:space="preserve"')
        elif kind:
            c = {"out": "muted", "ok": "green", "dim": "dim", "warn": "orange"}.get(kind, kind)
            out += T(64, y, txt, size, c, mono=True, extra='xml:space="preserve"')
        y += lh
    return write(path, 1000, int(y0 + hgt + 30), out)


def stats(path, cards, title=None, sub=None):
    """3–4 cards: (value, label, detail, color)."""
    head, top = _title(title, sub)
    n = len(cards)
    gap = 20
    w = (920 - gap * (n - 1)) / n
    y = top + 4
    out = head
    for i, (v, lab, det, c) in enumerate(cards):
        x = 40 + i * (w + gap)
        out += box(x, y, w, 176, "panel", "line", rx=12)
        vs = 52 if text_w(v, 52, bold=True) < w - 40 else 38
        out += T(x + 24, y + 80, v, vs, c, bold=True)
        out += T(x + 24, y + 120, lab, 16, "text")
        dt, _ = TL(x + 24, y + 145, det, w - 40, 14, lh=18, fill="muted")
        out += dt
    return write(path, 1000, int(y + 176 + 40), out)


def cards(path, items, title=None, sub=None, cols=3, card_h=None):
    """Grid of tiles. items: dicts {name, desc, logo(slug)|icon(name), tag, tag_color, color}."""
    head, top = _title(title, sub)
    gap = 20
    w = (920 - gap * (cols - 1)) / cols
    rows = [items[i:i + cols] for i in range(0, len(items), cols)]
    out, y = head, top + 4
    for row in rows:
        hs = []
        for it in row:
            dl = len(wrap(it.get("desc", ""), w - 48, 14))
            it["_tag_below"] = bool(it.get("tag")) and (text_w(it["name"], 18, bold=True) + 50 + text_w(it["tag"], 13, True) + 84 > w)
            hs.append(80 + dl * 19 + (8 if it.get("desc") else 0) + (34 if it["_tag_below"] else 0))
        ch = card_h or max(hs)
        for i, it in enumerate(row):
            x = 40 + i * (w + gap)
            out += box(x, y, w, ch, "panel", it.get("border", "line"), rx=12)
            ix = x + 24
            if it.get("logo"):
                out += logo(it["logo"], ix, y + 22, 34, it.get("logo_color"))
            elif it.get("icon"):
                out += icon(it["icon"], ix - 2, y + 20, 38, it.get("color", "muted"), it.get("accent", "blue"), sw=4)
            out += T(ix + 50, y + 46, it["name"], 18, "text", bold=True)
            if text_w(it["name"], 18, bold=True) + 74 > w:
                print(f"warn: card name too wide: {it['name']!r}")
            if it.get("tag"):
                tw = text_w(it["tag"], 13, True) + 20
                by = y + ch - 40 if it["_tag_below"] else y + 26
                b, bw = badge(x + w - 20 - tw, by, it["tag"], it.get("tag_color", "green"))
                out += b
            if it.get("desc"):
                dt, _ = TL(ix, y + 84, it["desc"], w - 48, 14, lh=19, fill="muted")
                out += dt
        y += ch + gap
    return write(path, 1000, int(y + 20), out)


def bars(path, rows, title=None, sub=None, unit="", max_v=None, label_w=230, fmt=None):
    """Horizontal bar chart. rows: (label, value, color, note). Value label drawn at bar end."""
    head, top = _title(title, sub)
    max_v = max_v or max(r[1] for r in rows)
    x0, x1 = 40 + label_w, 860
    out, y = head, top + 10
    for lab, v, c, *note in rows:
        out += T(40, y + 24, lab, 16, "text")
        bw = max(4, (x1 - x0) * v / max_v)
        out += box(x0, y + 6, bw, 26, c, None, rx=5)
        vl = fmt(v) if fmt else f"{v:g}{unit}"
        out += T(x0 + bw + 12, y + 25, vl, 15, c, bold=True, mono=True)
        if note and note[0]:
            out += T(x0, y + 54, note[0], 13, "dim", mono=True)
            y += 20
        y += 52
    return write(path, 1000, int(y + 26), out)


def timeline(path, events, title=None, sub=None):
    """Vertical-ish horizontal timeline. events: (date, label, color). 3–6 events."""
    head, top = _title(title, sub)
    n = len(events)
    y = top + 70
    x0 = 40 + min(110, 460 / max(n, 2))
    out = head + f'<line x1="{x0:g}" y1="{y}" x2="{1000 - x0:g}" y2="{y}" stroke="{C["line"]}" stroke-width="3"/>'
    step = (1000 - 2 * x0) / (n - 1) if n > 1 else 0
    maxh = 0
    for i, (d, lab, c) in enumerate(events):
        x = x0 + i * step
        out += f'<circle cx="{x:g}" cy="{y}" r="9" fill="{C["bg"]}" stroke="{col(c)}" stroke-width="4"/>'
        out += T(x, y - 24, d, 14, c, mono=True, bold=True, anchor="middle")
        lines = wrap(lab, min(step, 220) - 16 if n > 1 else 300, 15)
        for j, l in enumerate(lines):
            out += T(x, y + 40 + j * 20, l, 15, "muted", anchor="middle")
        maxh = max(maxh, len(lines) * 20)
    return write(path, 1000, int(y + 40 + maxh + 20), out)


def checklist(path, items, title=None, sub=None, cols=1):
    """Numbered steps. items: (title, detail) or (title, detail, color). Detail may be a command (mono if it starts with '$ ')."""
    head, top = _title(title, sub)
    out, y = head, top + 6
    colw = 920 / cols
    ys = [y] * cols
    for i, it in enumerate(items):
        t, d, c = (it + ("blue",))[:3] if len(it) == 2 else it
        k = i % cols if cols > 1 else 0
        x = 40 + k * colw
        yy = ys[k]
        out += f'<circle cx="{x + 18}" cy="{yy + 18}" r="17" fill="{TINT.get(c, C["panel2"])}" stroke="{col(c)}" stroke-width="2"/>'
        out += T(x + 18, yy + 24, str(i + 1), 16, c, bold=True, mono=True, anchor="middle")
        tt, th = TL(x + 52, yy + 24, t, colw - 70, 17, bold=True)
        out += tt
        dy = yy + 24 + th
        if d:
            mono = d.startswith("$ ")
            dt, dh = TL(x + 52, dy, d[2:] if mono else d, colw - 70, 14 if mono else 15, lh=20,
                        fill="yellow" if mono else "muted", mono=mono)
            out += dt; dy += dh
        ys[k] = dy + 18
    return write(path, 1000, int(max(ys) + 22), out)


def decision(path, question, yes, no, options=None, title=None, yes_label="yes", no_label="no",
             yes_state="green", no_state="red"):
    """Question pill → yes outcome (green, right) / no outcome (red, left) → optional row of options.
    yes/no: (title, detail). options: list of (title, detail, note|None)."""
    head, top = _title(title, None)
    out = head
    qy = top + 8
    ql = wrap(question, 520, 16, bold=True)
    qh = 20 + 22 * len(ql)
    qw = min(620, max(text_w(l, 16, bold=True) for l in ql) + 80)
    out += box(500 - qw / 2, qy, qw, qh, "panel2", "blue", rx=min(30, qh / 2), sw=2)
    for i, l in enumerate(ql):
        out += T(500, qy + 26 + i * 22, l, 16, "text", bold=True, anchor="middle")
    oy = qy + qh + 56

    def outcome(x, w, t, d, st):
        dl = wrap(d, w - 30, 14) if d else []
        hh = 50 + 19 * len(dl)
        s = state_box(x, oy, w, hh, st)
        s += T(x + w / 2, oy + 30, t, 16, "text" if st == "red" else st, bold=True, anchor="middle")
        for i, l in enumerate(dl):
            s += T(x + w / 2, oy + 52 + i * 19, l, 14, "muted", anchor="middle")
        return s, hh

    s1, h1 = outcome(560, 400, yes[0], yes[1], yes_state)
    s2, h2 = outcome(40, 440, no[0], no[1], no_state)
    out += s1 + s2
    out += arrow(500 + qw * 0.2, qy + qh, 740, oy - 4)
    out += arrow(500 - qw * 0.2, qy + qh, 280, oy - 4)
    my = (qy + qh + oy) / 2 + 5
    out += T((500 + qw * 0.2 + 740) / 2 + 14, my, yes_label, 14, yes_state, mono=True)
    out += T((500 - qw * 0.2 + 280) / 2 - 14, my, no_label, 14, no_state, mono=True, anchor="end")
    bottom = oy + max(h1, h2)
    if options:
        n = len(options)
        gap = 25
        w = (920 - gap * (n - 1)) / n
        py = oy + h2 + 56
        hh = 0
        for i, (t, d, *note) in enumerate(options):
            x = 40 + i * (w + gap)
            dl = wrap(d, w - 30, 14) if d else []
            nl = wrap(note[0], w - 30, 14) if note and note[0] else []
            hh = max(hh, 52 + 20 * (len(dl) + len(nl)))
        for i, (t, d, *note) in enumerate(options):
            x = 40 + i * (w + gap)
            out += box(x, py, w, hh, "panel", "line")
            out += T(x + w / 2, py + 32, t, 16, "text", bold=True, anchor="middle")
            yy = py + 56
            for l in (wrap(d, w - 30, 14) if d else []):
                out += T(x + w / 2, yy, l, 14, "muted", anchor="middle"); yy += 20
            for l in (wrap(note[0], w - 30, 14) if note and note[0] else []):
                out += T(x + w / 2, yy, l, 14, "orange", anchor="middle"); yy += 20
            out += arrow(260, oy + h2, x + w / 2, py - 4)
        bottom = py + hh
    return write(path, 1000, int(bottom + 34), out)


def table(path, header_row, rows, title=None, sub=None, widths=None, states=None):
    """Simple styled table. rows: list of lists; a cell may use [[color|text]] markup.
    widths: column widths summing to ~920."""
    head, top = _title(title, sub)
    n = len(header_row)
    widths = widths or [920 / n] * n
    out, y = head, top + 4
    rh = 46
    out += box(40, y, 920, rh * (len(rows) + 1), "panel", "line", rx=12)
    x = 40
    for w, hcell in zip(widths, header_row):
        out += T(x + 20, y + 29, hcell.upper(), 13, "dim", mono=True, extra='letter-spacing="1"'); x += w
    for r, row in enumerate(rows):
        yy = y + rh * (r + 1)
        out += f'<line x1="40" y1="{yy}" x2="960" y2="{yy}" stroke="{C["line"]}"/>'
        x = 40
        for j, (w, cell) in enumerate(zip(widths, row)):
            out += T(x + 20, yy + 29, cell, 15, "text" if j == 0 else "muted", bold=(j == 0)); x += w
    return write(path, 1000, int(y + rh * (len(rows) + 1) + 30), out)


def raw(path, h, body, defs=""):
    """Escape hatch: custom body on the standard card."""
    return write(path, 1000, h, body, defs)


def fan(x1, y1, items, x=860, size=44, top=None, step=88, color="line"):
    """Header motif: dotted links from a hub at (x1, y1) to a column of plated logos/icons.
    items: 'slug' (logo) or ('icon', name, accent)."""
    top = top if top is not None else 180 - (len(items) - 1) * step / 2 - size / 2
    out = ""
    for i, it in enumerate(items):
        y = top + i * step
        out += link(x1, y1, x - 14, y + size / 2, color, 3)
        if isinstance(it, tuple):
            out += box(x - size * .22, y - size * .22, size * 1.44, size * 1.44, "panel", "line", rx=size * .3)
            out += icon(it[1], x, y, size, "muted", it[2] if len(it) > 2 else "blue", sw=4)
        else:
            out += logo(it, x, y, size, plate=True)
    return out


def matrix(path, cols, rows, title=None, sub=None, label_w=330, legend=None, note=None):
    """Feature matrix. cols: column names. rows: (name, detail, [v...]) with v in
    'y' (green full dot), 'p' (yellow half), 'n' (dim empty), or a short string."""
    head, top = _title(title, sub)
    out, y = head, top + 6
    cw = (920 - label_w) / len(cols)
    for j, c in enumerate(cols):
        out += T(40 + label_w + cw * j + cw / 2, y + 14, c.upper(), 13, "dim", mono=True, anchor="middle", extra='letter-spacing="1"')
    y += 30
    rh = 58
    for i, (name, det, vals) in enumerate(rows):
        yy = y + i * rh
        if i % 2 == 0:
            out += box(40, yy, 920, rh, "panel", None, rx=8)
        out += T(60, yy + (25 if det else 35), name, 16, "text", bold=True)
        if det:
            out += T(60, yy + 45, det, 13, "muted", mono=True)
        for j, v in enumerate(vals):
            cx, cy = 40 + label_w + cw * j + cw / 2, yy + rh / 2
            if v == "y":
                out += f'<circle cx="{cx:g}" cy="{cy:g}" r="9" fill="{C["green"]}"/>'
            elif v == "p":
                out += (f'<circle cx="{cx:g}" cy="{cy:g}" r="8" fill="none" stroke="{C["yellow"]}" stroke-width="2"/>'
                        f'<path d="M{cx:g} {cy - 8:g} a8 8 0 0 1 0 16 z" fill="{C["yellow"]}"/>')
            elif v == "n":
                out += f'<circle cx="{cx:g}" cy="{cy:g}" r="8" fill="none" stroke="{C["line"]}" stroke-width="2"/>'
            else:
                out += T(cx, cy + 5, v, 14, "muted", mono=True, anchor="middle")
    y += len(rows) * rh + 30
    if legend is not False:
        lx = 40
        for sym, lab in (legend or (("y", "yes"), ("p", "partial / depends"), ("n", "no"))):
            cy = y - 5
            if sym == "y": out += f'<circle cx="{lx + 8}" cy="{cy}" r="7" fill="{C["green"]}"/>'
            elif sym == "p": out += f'<circle cx="{lx + 8}" cy="{cy}" r="6" fill="none" stroke="{C["yellow"]}" stroke-width="2"/><path d="M{lx + 8} {cy - 6} a6 6 0 0 1 0 12 z" fill="{C["yellow"]}"/>'
            else: out += f'<circle cx="{lx + 8}" cy="{cy}" r="6" fill="none" stroke="{C["line"]}" stroke-width="2"/>'
            out += T(lx + 22, y, lab, 14, "muted"); lx += 44 + text_w(lab, 14)
        y += 10
    if note:
        nt, nh = TL(40, y + 24, note, 920, 14, fill="dim")
        out += nt; y += nh + 10
    return write(path, 1000, int(y + 24), out)
