import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "postedit.py")).read())

# iptables
m=[icon("shield-check",600,80,190,"muted","green")]
for i,(p,c) in enumerate((("22  ssh","green"),("80  http","green"),("443 https","green"),("53  lan only","yellow"),("*   DROP","red"))):
    m.append(T(830,100+i*38,p,17,c,mono=True,bold=(c=="red")))
m.append(f'<path d="M800 92 V262" stroke="{C["line"]}" stroke-width="2"/>')
header(IMG+"iptables-header.svg","Linux · firewall",["iptables:","deny by default"],"Close everything, then open only SSH, web, NTP and DNS",chip="-P INPUT DROP",accent="green",chip_color="red",motif=m)
flow(IMG+"iptables-chain.svg","How each incoming packet is judged",[
  dict(t="Reply to our own traffic?",d="ESTABLISHED",state="green"),
  dict(t="Loopback?",d="-i lo",state="green"),
  dict(t="Allowed port or IP?",d="22 80 443 123 53",state="green"),
  dict(t="Everything else",d="policy DROP",state="red")],
  sub="Rules are checked top to bottom; the first match wins",arrows=[("no","dim",None)]*3,
  note="A match in the first three boxes means ACCEPT. Nothing matched means the default policy drops it.",step_h=100)
table(IMG+"iptables-allowed.svg",["Traffic","Port","Allowed from"],[
  ["SSH","tcp 22","anywhere"],["HTTP / HTTPS","tcp+udp 80, 443","anywhere"],["NTP","udp 123","anywhere"],
  ["DNS","udp 53","[[yellow|192.168.0.0/24 + one trusted IP]]"],["Ping","icmp 8","anywhere, to 192.168.0.103"],["Anything else","—","[[red|dropped]]"]],
  title="What the finished rules let in",widths=[240,240,440])
header_md("iptables-exmple","iptables-header.svg","iptables default-deny firewall: SSH, HTTP, HTTPS and LAN-only DNS allowed, everything else dropped")
insert_after("iptables-exmple","Allow access to port 53 from your local network.","iptables-allowed.svg","Table of traffic the finished rules allow: SSH, HTTP and HTTPS, NTP and ping from anywhere, DNS only from the LAN and one trusted IP, everything else dropped")
insert_before("iptables-exmple","Replace the COMMIT command","iptables-chain.svg","Each incoming packet is checked in order: replies to our traffic, loopback and allowed ports are accepted; anything else hits the DROP policy")

# nginx multi apps
header(IMG+"nginx-multi-apps-header.svg","Self-hosting · nginx",["Many Python apps,","one server"],"nginx as a reverse proxy, one site file per domain",chip="proxy_pass http://127.0.0.1:8000",accent="green",
  motif=[logo("nginx",600,128,104),link(724,180,790,180,"muted"),*[box(800,92+i*92,150,64,"panel","line")+logo("python",816,108+i*92,32)+T(860,130+i*92,f":{8000+i}",17,"muted",mono=True) for i in range(2)]])
body=""
for i,(d,p) in enumerate((("example1.com",8000),("example2.com",8001))):
    y=110+i*130
    body+=box(40,y,240,80,"panel","line")+T(160,y+36,d,17,"text",bold=True,mono=True,anchor="middle")+T(160,y+60,"DNS → server IP",14,"muted",anchor="middle")
    body+=arrow(284,y+40,396,195,"blue",curve=(340,y+40,340,195,))
    body+=box(720,y,240,80,"panel","line")+logo("python",740,y+24,32)+T(790,y+36,"Python app",17,"text",bold=True)+T(790,y+60,f"127.0.0.1:{p}",14,"muted",mono=True)
    body+=arrow(600,195,716,y+40,"green",curve=(660,195,660,y+40))
    body+=T(658,y+40+(-14 if i==0 else 28),f"server_name {d}",13,"dim",mono=True,anchor="middle") if False else ""
body+=box(400,150,200,90,TINT["green"],"green",sw=2)+logo("nginx",420,176,38)+T(470,190,"nginx",18,"text",bold=True)+T(470,214,":80 / :443",14,"green",mono=True)
body+=T(40,52,"One public port, a site file per domain",22,bold=True)+T(40,80,"nginx reads the Host header and forwards to the matching local port",15,"muted")
body+=T(40,384,"Apps only listen on 127.0.0.1, so the internet can reach them only through nginx.",15,"yellow")
raw(IMG+"nginx-multi-apps-flow.svg",410,body)
header_md("How to Host Multiple","nginx-multi-apps-header.svg","nginx reverse proxy forwarding two domains to Python apps on ports 8000 and 8001")
remove_img("How to Host Multiple","/static/img/nginx-logo.svg")
insert_after("How to Host Multiple","In this tutorial we assume","nginx-multi-apps-flow.svg","example1.com and example2.com both point at the server; nginx on port 80 forwards each to its own Python app on 127.0.0.1:8000 or 8001")

# multi-room audio
m=[icon("server",590,120,110,"muted","green"),icon("wifi",700,140,60,"blue","blue")]
for i in range(3):
    y=62+i*86
    m+=[link(770,170,806,y+36,"line",3),icon("board",812,y+8,56,"muted","red"),icon("speaker",880,y,70,"muted","green")]
header(IMG+"multi-room-audio-header.svg","Raspberry Pi · audio",["Multi-room audio","with Pi Zeros"],"Logitech Media Server plus a cheap Squeezelite player in every room",chip="squeezelite -o front",accent="green",motif=m)
body=T(40,52,"One server, a player per room",22,bold=True)+T(40,80,"LMS keeps every Squeezelite player in sync over Wi-Fi",15,"muted")
body+=box(40,150,250,130,"panel","line")+icon("desktop",64,176,60,"muted","blue")+T(140,196,"Logitech Media",17,bold=True)+T(140,218,"Server",17,bold=True)+T(64,262,"Windows, Linux, NAS or Pi 3",14,"muted")
body+=icon("wifi",330,180,60,"blue","blue")
for i,r in enumerate(("Kitchen","Living room","Bedroom")):
    y=108+i*96
    body+=arrow(400,215,516,y+38,"blue",curve=(460,215,460,y+38))
    body+=box(520,y,440,76,"panel","line")+icon("board",540,y+14,48,"muted","red")+T(604,y+32,"Pi Zero W + Squeezelite",16,bold=True)+T(604,y+56,"USB sound card → speakers",14,"muted")+T(940,y+44,r,15,"green",anchor="end",mono=True)
raw(IMG+"multi-room-audio-layout.svg",420,body)
cards(IMG+"multi-room-audio-parts.svg",[
  dict(name="Pi Zero W",icon="board",accent="red",desc="Built-in Wi-Fi, one micro USB port"),
  dict(name="SD card",icon="sdcard",accent="blue",desc="Raspbian Lite fits; bigger lasts longer"),
  dict(name="USB sound card",icon="plug",accent="green",desc="A $1.5 one is fine for this"),
  dict(name="OTG adapter",icon="plug",color="muted",desc="Micro USB male to USB female"),
  dict(name="5 V supply",icon="power",accent="yellow",desc="Plus a micro USB cable"),
  dict(name="Speakers",icon="speaker",accent="green",desc="Any with a 3.5 mm input"),
 ],title="Parts for one player",sub="repeat per room")
header_md("multi-room-audio","multi-room-audio-header.svg","Multi-room audio: Logitech Media Server streams to Raspberry Pi Zero W Squeezelite players and speakers in three rooms")
remove_img("multi-room-audio","/static/img/logitech-logo.png")
insert_after("multi-room-audio","Logitec Media Server <a href","multi-room-audio-layout.svg","Logitech Media Server on a PC sends audio over Wi-Fi to a Pi Zero W running Squeezelite in the kitchen, living room and bedroom, each with a USB sound card and speakers")
insert_after("multi-room-audio","7. **USB hub**","multi-room-audio-parts.svg","Parts for one player: Pi Zero W, SD card, USB sound card, OTG adapter, 5 V supply and speakers")

# flask babel
header(IMG+"flask-babel-header.svg","Python · Flask",["Translate a Flask","site with Babel"],"Mark strings, extract them, translate, compile",chip="pybabel compile -d translations",accent="yellow",
  motif=[logo("flask",590,90,90,"text"),mini_term(700,74,270,["[[purple|gettext]]([[green|'Hello']])","→ en  Hello","→ bg  Здравей"],15,"messages.po"),T(636,230,"EN",30,"blue",bold=True,mono=True,anchor="middle"),T(636,272,"BG",30,"green",bold=True,mono=True,anchor="middle")])
flow(IMG+"flask-babel-flow.svg","From source strings to a translated site",[
  dict(t="Tag strings",d="gettext() / _()"),dict(t="Extract",d="messages.pot",state="blue"),
  dict(t="Init locale",d="bg/messages.po"),dict(t="Translate",d="edit .po",state="yellow"),dict(t="Compile",d="messages.mo",state="green")],
  note="Changed strings later? Re-run extract, then pybabel update instead of init, then compile again.")
terminal(IMG+"flask-babel-commands.svg",[("$","pybabel extract -F babel.cfg -o messages.pot --input-dirs=."),("$","pybabel init -i messages.pot -d translations -l bg"),("dim","# translate translations/bg/LC_MESSAGES/messages.po"),("$","pybabel compile -d translations"),("ok","compiling catalog translations/bg/LC_MESSAGES/messages.po"),("",""),("dim","# later, after changing strings:"),("$","pybabel update -i messages.pot -d translations")],title="The whole cycle in four commands")
header_md("How-to-translate-your-flask","flask-babel-header.svg","Translate a Flask site with Flask-Babel: gettext strings compiled into English and Bulgarian catalogs")
insert_before("How-to-translate-your-flask","## Install Flask-Babel","flask-babel-flow.svg","Flask-Babel workflow: tag strings with gettext, extract to messages.pot, init a locale, translate the .po file, compile to .mo; on changes re-extract and update")
insert_before("How-to-translate-your-flask","## Updating locales","flask-babel-commands.svg","Terminal: pybabel extract, init, compile, and later pybabel update")

# pelican
header(IMG+"pelican-static-site-header.svg","Static sites · Python",["Build a static site","with Pelican"],"Markdown in, plain HTML out, hosted free on GitHub Pages",chip="pelican content",accent="blue",
  motif=[icon("file",580,110,110,"muted","blue"),link(690,165,740,165),logo("pelican",750,120,90,"text"),link(850,165,880,165),logo("github",890,135,60)])
flow(IMG+"pelican-static-site-flow.svg","From Markdown to a live site",[
  dict(t="Write posts",d="content/*.md"),dict(t="pelican content",d="builds HTML",state="blue"),dict(t="output/",d="html, css, images"),
  dict(t="Preview",d="http.server :8000"),dict(t="GitHub Pages",d="git push",state="green")],
  note="No database and no server code: the output folder is the whole site.")
header_md("How-to-create-a-static-site","pelican-static-site-header.svg","Build a static site with Pelican: Markdown files become HTML, hosted on GitHub Pages")
remove_img("How-to-create-a-static-site","/static/img/python_pelican.png")
replace_img("How-to-create-a-static-site","/static/img/github_logo.png","pelican-static-site-flow.svg","Pelican workflow: write Markdown in content, run pelican content, get HTML in output, preview locally, push to GitHub Pages")

# win autologin
header(IMG+"win-autologin-header.svg","Windows 10 / 11",["Sign in to Windows","automatically"],"Skip the password prompt on a home PC with netplwiz",chip="Win+R › netplwiz",accent="blue",
  motif=[icon("desktop",600,80,170,"muted"),icon("windows",655,112,60,"blue","blue"),box(800,110,160,44,"panel","line",rx=8)+T(818,138,"••••••••",18,"dim",mono=True),f'<line x1="796" y1="132" x2="964" y2="132" stroke="{C["red"]}" stroke-width="4" stroke-linecap="round"/>',ok_disc(880,220,30)])
checklist(IMG+"win-autologin-steps.svg",[
  ("Open netplwiz","Press Windows+R, type netplwiz, press Enter"),
  ("Untick the password checkbox","“Users must enter a user name and password to use this computer”"),
  ("Enter your password twice","Windows stores it so it can sign you in"),
  ("Restart to test","Checkbox missing? Turn off “only allow Windows Hello sign-in” in Settings › Accounts › Sign-in options","yellow")],
  title="Method 1 in four steps")
header_md("How-to-make-win-10-auto-login","win-autologin-header.svg","Windows automatic sign-in: the password prompt is skipped by unticking a box in netplwiz")
insert_before("How-to-make-win-10-auto-login","## Method 1","win-autologin-steps.svg","Four steps: open netplwiz, untick the password checkbox, enter your password twice, restart; if the checkbox is missing turn off the Windows Hello only option")
