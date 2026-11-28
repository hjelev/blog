import re, sys
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "scripts"))
from svgkit import *
BLOG = os.path.normpath(os.path.join(_HERE, "..", "..", "..", "..")) + "/"
IMG = BLOG + "static/img/"

def _p(slug):
    import glob
    m = glob.glob(BLOG + "_posts/*" + slug + "*.md")
    assert len(m) == 1, (slug, m)
    return m[0]

def dims(svg):
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', open(IMG + svg).read())
    return vb.group(1), vb.group(2)

def md(svg, alt):
    w, h = dims(svg)
    return f'![{alt}](/static/img/{svg}){{: width="{w}" height="{h}"}}'

def insert_after(slug, snippet, svg, alt):
    """Insert figure after the paragraph/block containing snippet."""
    p = _p(slug); s = open(p).read()
    if f"/static/img/{svg})" in s:
        print("already:", svg); return
    i = s.index(snippet)
    j = s.find("\n\n", i)
    if j == -1: j = len(s)
    s = s[:j] + "\n\n" + md(svg, alt) + s[j:]
    open(p, "w").write(s)

def insert_before(slug, snippet, svg, alt):
    p = _p(slug); s = open(p).read()
    if f"/static/img/{svg})" in s:
        print("already:", svg); return
    i = s.index(snippet)
    s = s[:i] + md(svg, alt) + "\n\n" + s[i:]
    open(p, "w").write(s)

def replace_img(slug, old_src, svg, alt):
    """Replace a whole image line (matched by its src) with the new figure."""
    p = _p(slug); s = open(p).read()
    pat = re.compile(r"!\[[^\]]*\]\(" + re.escape(old_src) + r"[^)]*\)(\{:[^}]*\})?")
    if not pat.search(s):
        print("gone:", old_src); return
    s = pat.sub(lambda m: md(svg, alt), s, count=1)
    open(p, "w").write(s)

def remove_img(slug, old_src):
    p = _p(slug); s = open(p).read()
    pat = re.compile(r"\n?!\[[^\]]*\]\(" + re.escape(old_src) + r"[^)]*\)(\{:[^}]*\})?\n?")
    if not pat.search(s):
        print("gone:", old_src); return
    s = pat.sub("\n", s, count=1)
    s = re.sub(r"\n{3,}", "\n\n", s)
    open(p, "w").write(s)

def header_md(slug, svg, alt):
    """Set/replace the header image (first image right after front matter) and front matter image/thumbnail."""
    p = _p(slug); s = open(p).read()
    fm_end = s.index("\n---", 4) + 4
    fm, body = s[:fm_end], s[fm_end:]
    og = "/static/img/og/" + svg.replace(".svg", ".png")
    for k, v in (("image", og), ("thumbnail", "/static/img/" + svg)):
        if re.search(rf"^{k}:", fm, re.M):
            fm = re.sub(rf"^{k}:.*$", f"{k}: {v}", fm, flags=re.M)
        else:
            fm = fm[:-4] + f"\n{k}: {v}" + fm[-4:]
    b = body.lstrip("\n")
    m = re.match(r"!\[[^\]]*\]\(/static/img/[^)]*-header\.svg\)(\{:[^}]*\})?", b)
    if m:
        b = md(svg, alt) + b[m.end():]
    else:
        b = md(svg, alt) + "\n\n" + b
    open(p, "w").write(fm + "\n\n" + b)
