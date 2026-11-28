import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "postedit.py")).read())

# brotli2shell
m=[T(590,92,"8-byte buffer",14,"muted",mono=True)]
for i in range(8): m.append(box(590+i*34,104,30,40,"panel2","blue",rx=4,sw=1.5))
for i in range(3): m.append(box(862+i*34,104,30,40,TINT["red"],"red",rx=4,sw=2))
m+=[T(912,92,"overflow",14,"red",mono=True,bold=True,anchor="middle"),mini_term(590,176,370,["[[muted|Content-Encoding:]] [[yellow|br]]","[[red|invalid block switch → “need more input”]]"],14)]
header(IMG+"brotli2shell-header.svg","CVE-2026-111497 · Brotli",["Brotli2Shell /","Node2Shell"],"A Brotli decoder bug hitting Node.js, Python, .NET and more",accent="red",motif=m)
flow(IMG+"brotli2shell-bug.svg","How one crafted stream overflows the decoder",[
  dict(t="Crafted br stream",d="one block type"),dict(t="Impossible block switch",d="decode.c",state="yellow"),
  dict(t="Read as “need more input”",d="BROTLI_FALSE, ignored"),dict(t="Bytes keep landing in 8 B buffer",d="out-of-bounds write",state="red")],
  note="The fix returns a real error (BROTLI_DECODER_ERROR_FORMAT_BLOCK_SWITCH, -17) and stops decoding.",step_h=104)
cards(IMG+"brotli2shell-exposure.svg",[
  dict(name="Clients",icon="globe",accent="red",desc="Node fetch(), requests/urllib3, aiohttp, httpx, curl --compressed fetching URLs someone else controls"),
  dict(name="Servers",icon="server",accent="red",desc="Express 5 body-parser by default, ASP.NET Core decompression, Envoy/Istio Brotli filter"),
  dict(name="Files",icon="file",accent="red",desc="Parquet, JPEG XL, PDFs and archives from uploads (FFmpeg, libjxl, ClickHouse)"),
 ],title="Three ways to be exposed",sub="having libbrotli installed is not enough; something must decode untrusted Brotli")
timeline(IMG+"brotli2shell-timeline.svg",[("Feb 27","fix committed upstream, no release tagged","blue"),("Oct 21","Node.js and Google ship fixes","green"),("Oct 21–22","public PoCs on GitHub","orange"),("by Oct 31","listed in CISA KEV","red")],title="Eight months between fix and release")
header_md("brotli2shell","brotli2shell-header.svg","Brotli2Shell: an invalid block switch makes the decoder write past an 8-byte buffer")
insert_before("brotli2shell","### The upstream fix was public","brotli2shell-bug.svg","A crafted Brotli stream forces an impossible block switch; the decoder reads the failure as a need for more input and keeps writing into an 8-byte buffer, overflowing it")
insert_before("brotli2shell","## Is it really remote code execution?","brotli2shell-timeline.svg","Timeline: fix committed upstream February 27 without a release, Node.js and Google ship fixes October 21, public PoCs October 21 to 22, then listed in CISA KEV")
insert_before("brotli2shell","### 1. Clients that decompress","brotli2shell-exposure.svg","Three exposure paths: HTTP clients decoding responses from untrusted URLs, servers decoding Brotli request bodies like Express 5, and tools decoding Brotli inside uploaded files")

# wordpress to static
m=[logo("wordpress",590,110,100,"text"),link(704,160,770,160),icon("file",780,90,140,"muted","green"),T(850,268,"index.html",15,"green",mono=True,anchor="middle"),blocked(640,250,22,"red",4),T(676,257,"PHP",15,"red",mono=True,bold=True)]
header(IMG+"wp-to-static-header.svg","WordPress · static sites",["Convert WordPress","to a static site"],"No PHP on the internet, nothing to patch, free hosting",accent="green",motif=m)
body=T(40,52,"Two ways to do it",22,bold=True)+T(40,80,"Both end with plain HTML on a free host and no PHP exposed",15,"muted")
for r,(lab,c,steps) in enumerate((("A · keep WordPress, export HTML","blue",[("WordPress","localhost / VPN"),("Simply Static","export plugin"),("HTML files","check output"),("Free host","Pages, Netlify…")]),
                                   ("B · migrate to a generator","green",[("WordPress export","XML"),("Markdown","in a Git repo"),("Jekyll / Hugo","build"),("Free host","delete WordPress")]))):
    y=116+r*150
    body+=T(40,y+14,lab,16,c,bold=True,mono=False)
    for i,(t,d) in enumerate(steps):
        x=40+i*236
        body+=box(x,y+30,200,72,TINT[c] if i==3 else "panel",c if i==3 else "line",sw=2 if i==3 else 1.5)+T(x+100,y+62,t,16,bold=True,anchor="middle")+T(x+100,y+86,d,14,"muted",mono=True,anchor="middle")
        if i<3: body+=arrow(x+204,y+66,x+230,y+66,c)
body+=T(40,436,"A: an afternoon, editors keep Gutenberg.   B: a weekend, you write in Markdown.",15,"yellow",extra='xml:space="preserve"')
raw(IMG+"wp-to-static-paths.svg",462,body)
cards(IMG+"wp-to-static-dynamic.svg",[
  dict(name="Comments",icon="users",accent="blue",desc="Giscus or Disqus, or turn them off",tag="replace",tag_color="green"),
  dict(name="Contact forms",icon="mail",accent="blue",desc="Formspree, Netlify Forms or a small function",tag="replace",tag_color="green"),
  dict(name="Search",icon="search",accent="blue",desc="Pagefind indexes the built HTML",tag="replace",tag_color="green"),
  dict(name="Logins, shops",icon="lock",accent="red",desc="Need a backend: keep WordPress for these",tag="stays",tag_color="red"),
 ],cols=2,title="What happens to the dynamic bits")
header_md("convert-wordpress-to-static","wp-to-static-header.svg","WordPress exported to static HTML files, with PHP no longer exposed to the internet")
insert_after("convert-wordpress-to-static","| Best for |","wp-to-static-paths.svg","Option A keeps WordPress private and exports HTML with Simply Static; option B exports to Markdown and builds with Jekyll or Hugo; both publish to a free host")
insert_before("convert-wordpress-to-static","## Replacing the dynamic bits","wp-to-static-dynamic.svg","Comments move to Giscus or Disqus, forms to Formspree or Netlify Forms, search to Pagefind; logins and shops still need a backend")

# php2shell
m=[logo("php",590,96,120,"text"),mini_term(740,80,230,["[[muted|POST /]]","[[yellow|aaaa…aaaa]]=[[muted|1]]","[[red|memory_limit hit]]","[[red|→ system()]]"],14)]
header(IMG+"php2shell-header.svg","PHP · CVE-2026-109618/9",["PHP2Shell:","patch PHP itself"],"Two exploited unauthenticated RCE bugs in the PHP engine",chip="8.5.12 · 8.4.27 · 8.3.36 · 8.2.35",accent="purple",chip_color="green",motif=m)
flow(IMG+"php2shell-bug.svg","CVE-2026-109618: a half-built hash entry",[
  dict(t="Huge POST field name",d="fits the body"),dict(t="Counters bumped first",d="nNumUsed++"),dict(t="Key copy blows memory_limit",d="fatal error",state="yellow"),
  dict(t="Shutdown frees $_POST",d="garbage bucket used"),dict(t="system() as www-data",state="red")],
  note="Default memory limits are enough. Needs an ASLR leak (public write-ups use PHPSESSID).",step_h=104)
timeline(IMG+"php2shell-timeline.svg",[("Oct 17","AWS sees exploit attempts","red"),("Oct 21","8.5.12, 8.4.27, 8.3.36, 8.2.35 released","green"),("Oct 26","CVE-2026-109618 added to CISA KEV","red")],title="Exploited before the patch")
matrix(IMG+"php2shell-stopgap.svg",["109618","109619","115560"],[
  ("Upgrade PHP + restart workers","8.5.12 / 8.4.27 / 8.3.36 / 8.2.35",["y","y","n"]),
  ("session.upload_progress.enabled = 0","php.ini stopgap",["n","y","y"]),
  ("Update WordPress / plugins","app layer",["n","n","n"])],
  title="What each fix actually covers",label_w=470,legend=(("y","covered"),("n","not covered")),note="CVE-2026-115560 has no PHP fix yet; the upload-progress setting is the only cover.")
header_md("php2shell","php2shell-header.svg","PHP2Shell: an oversized POST field runs PHP out of memory and ends in system() running a command")
insert_before("php2shell","### CVE-2026-109619","php2shell-bug.svg","CVE-2026-109618: a huge POST field name bumps the hash table counters, the key copy exceeds memory_limit, and at shutdown PHP frees an uninitialized bucket, leading to system() as www-data")
insert_before("php2shell","## Am I affected?","php2shell-timeline.svg","Timeline: AWS saw attempts October 17, patched PHP released October 21, CISA added CVE-2026-109618 to KEV October 26")
insert_before("php2shell","## Did someone already get in?","php2shell-stopgap.svg","Upgrading PHP covers 109618 and 109619; disabling session upload progress covers 109619 and 115560 but not 109618; updating WordPress covers none")

# lxd
m=[icon("server",590,96,120,"muted","green"),T(650,250,":8443",15,"muted",mono=True,anchor="middle")]
for i,(t,c) in enumerate((("attacker leaf","red"),("trusted cert","green"))):
    m.append(box(760,100+i*62,200,46,TINT[c],c,rx=8,sw=2)+T(778,129+i*62,t,15,c,mono=True))
m+=[link(724,150,752,150),T(860,258,"chain sent by client",13,"dim",mono=True,anchor="middle")]
header(IMG+"lxd-cve-2026-112816-header.svg","LXD · Incus · CVE-2026-112816",["Log in as any","trusted client"],"Append a trusted public cert to your TLS chain and you're in",chip="sudo snap refresh lxd",accent="orange",chip_color="green",motif=m)
compare(IMG+"lxd-cve-2026-112816-chain.svg",
  dict(kicker="before the fix",title="Any cert in the chain",items=["Handshake proves you own the leaf only","Server checks every cert against the trust store","Trusted cert at position 2 → you're that client"],state="red",foot="for _, c := range PeerCertificates"),
  dict(kicker="after the fix",title="Only the proven leaf",items=["Same handshake","Only PeerCertificates[0] is compared","Extra certs in the chain are ignored"],state="green",foot="LXD 6.10.1 · 5.21.9 · 5.0.11 · Incus 7.6.0"),title="Why the bypass works")
decision(IMG+"lxd-cve-2026-112816-exposed.svg","Is core.https_address or cluster.https_address set?",("Patch now","Until then firewall 8443 to management hosts"),("Not reachable remotely","Local Unix socket only; patch anyway"),yes_label="yes",no_label="no",title="Am I exposed?")
header_md("lxd-incus-auth-bypass","lxd-cve-2026-112816-header.svg","LXD auth bypass: the client's TLS chain holds the attacker's own leaf followed by a trusted certificate")
insert_before("lxd-incus-auth-bypass","### How hard is it to get","lxd-cve-2026-112816-chain.svg","Before the fix the server accepted any certificate in the client chain, so a trusted cert behind the attacker's leaf granted access; after it only the key-proven leaf is checked")
insert_before("lxd-incus-auth-bypass","## Fixed versions","lxd-cve-2026-112816-exposed.svg","If core.https_address or cluster.https_address is set the API is reachable: patch and firewall port 8443; otherwise LXD only listens on a local Unix socket")
