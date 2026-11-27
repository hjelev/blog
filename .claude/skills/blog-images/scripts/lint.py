"""Heuristic SVG lint for blog images: structure, fonts, text overflow."""
import re, sys
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
path = sys.argv[1]
problems, warnings = [], []
try:
    root = ET.parse(path).getroot()
except ET.ParseError as e:
    print(f"FAIL {path}: XML error: {e}"); sys.exit(1)

vb = root.get("viewBox")
if not vb:
    problems.append("missing viewBox")
    W = H = 0
else:
    _, _, W, H = map(float, vb.split())
    if W != 1000:
        warnings.append(f"viewBox width {W:g}, blog standard is 1000")

def inherited(el, attr, parents):
    for p in [el] + parents[::-1]:
        v = p.get(attr)
        if v is None:
            m = re.search(attr + r"\s*:\s*([^;]+)", p.get("style", ""))
            v = m.group(1) if m else None
        if v is not None:
            return v
    return None

def translate_of(parents):
    dx = dy = 0.0
    for p in parents:
        m = re.search(r"translate\(\s*([-\d.]+)[ ,]+([-\d.]+)", p.get("transform", ""))
        if m:
            dx += float(m.group(1)); dy += float(m.group(2))
    return dx, dy

def walk(el, parents):
    if el.tag == NS + "text":
        txt = "".join(el.itertext()).strip()
        size = float(re.sub(r"[^\d.]", "", inherited(el, "font-size", parents) or "16") or 16)
        fam = (inherited(el, "font-family", parents) or "").lower()
        weight = inherited(el, "font-weight", parents) or ""
        anchor = inherited(el, "text-anchor", parents) or "start"
        mono = "mono" in fam or "consolas" in fam or "menlo" in fam
        cw = 0.6 if mono else 0.55
        if weight in ("bold", "700", "800", "900"):
            cw += 0.04
        width = len(txt) * size * cw
        dx, dy = translate_of(parents)
        try:
            x = float(el.get("x", 0)) + dx
            y = float(el.get("y", 0)) + dy
        except ValueError:
            x = y = None
        if size < 13:
            problems.append(f"font-size {size:g} < 13: {txt[:40]!r}")
        if x is not None and W:
            left = x - (width if anchor == "end" else width / 2 if anchor == "middle" else 0)
            right = left + width
            if right > W - 20 or left < 20:
                problems.append(f"text likely overflows canvas (≈{left:.0f}..{right:.0f} of {W:g}): {txt[:50]!r}")
            if y is not None and (y > H - 8 or y - size < 4):
                problems.append(f"text near/outside top/bottom edge (y={y:.0f}): {txt[:40]!r}")
        if not fam:
            warnings.append(f"no font-family for {txt[:30]!r}")
    for c in el:
        walk(c, parents + [el])

walk(root, [])
if root.find(NS + "rect") is None:
    warnings.append("no background rect: image should paint its own background")
raw = open(path, encoding="utf-8").read()
if "<image" in raw and "http" in raw:
    problems.append("external <image> reference: inline everything")

for w in warnings: print(f"warn {path}: {w}")
for p in problems: print(f"FAIL {path}: {p}")
if not problems:
    print(f"ok   {path}")
sys.exit(1 if problems else 0)
