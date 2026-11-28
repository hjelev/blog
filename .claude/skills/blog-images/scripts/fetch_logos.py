"""Vendor simple-icons logos into logos.json, reading the package as data only.

Usage: python3 -I fetch_logos.py <extracted simple-icons package dir> slug [slug ...]
Get the package with:  npm pack simple-icons@15.0.0 && tar xzf simple-icons-*.tgz
"""
import json, os, re, sys, unicodedata

pkg, slugs = sys.argv[1], sys.argv[2:]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logos.json")

def title_to_slug(t):
    t = t.lower().replace("+", "plus").replace(".", "dot").replace("&", "and")
    t = unicodedata.normalize("NFD", t)
    return re.sub(r"[^a-z0-9]", "", t)

data = json.load(open(os.path.join(pkg, "data", "simple-icons.json"), encoding="utf-8"))
data = data if isinstance(data, list) else data["icons"]
meta = {(d.get("slug") or title_to_slug(d["title"])): d for d in data}
db = json.load(open(out)) if os.path.exists(out) else {}
for s in slugs:
    f = os.path.join(pkg, "icons", s + ".svg")
    if s not in meta or not os.path.exists(f):
        print("missing:", s); continue
    path = re.search(r'<path d="([^"]+)"', open(f, encoding="utf-8").read()).group(1)
    db[s] = {"title": meta[s]["title"], "hex": meta[s]["hex"], "path": path}
with open(out, "w") as fh:
    json.dump(db, fh, indent=0, sort_keys=True)
print(len(db), "logos in", os.path.normpath(out))
