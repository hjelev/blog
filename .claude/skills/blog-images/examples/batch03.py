import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "postedit.py")).read())

# DNS filtering 2019
m=[icon("phone",590,96,150,"muted"),link(680,170,740,170)]
m+=[box(750,90,200,52,TINT["green"],"green",rx=10)+T(768,122,"example.com",15,"green",mono=True)]
m+=[box(750,160,200,52,TINT["red"],"red",rx=10)+T(768,192,"ads.tracker",15,"red",mono=True)]
m+=[T(850,246,"→ 0.0.0.0",17,"red",mono=True,bold=True,anchor="middle"),link(740,170,746,116,"line",3)]
header(IMG+"dns-filtering-header.svg","Networking · DNS",["Block ads by","changing your DNS"],"Free filtering resolvers that drop ad and malware domains",chip="94.140.14.14",accent="green",motif=m)
matrix(IMG+"dns-filtering-compare.svg",["ads","malware","adult"],[
  ("AdGuard DNS","94.140.14.14",["y","y","p"]),("Epsilon Eight","138.68.250.168",["y","y","n"]),
  ("CleanBrowsing","185.228.168.x",["n","y","p"]),("OpenDNS FamilyShield","208.67.222.123",["n","y","y"]),
  ("Quad9","9.9.9.9",["n","y","n"]),("Cloudflare for Families","1.1.1.2 / 1.1.1.3",["n","y","p"]),("Pi-hole (self-hosted)","your block lists",["y","p","p"])],
  title="What each service blocks",sub="ads, malware and adult content filtering at a glance",
  note="AdGuard, CleanBrowsing and Cloudflare: which filters apply depends on the IP you pick.")
body=T(40,52,"Android Private DNS",22,bold=True)+T(40,80,"Android 9+ uses it on every network, Wi-Fi and mobile data",15,"muted")
body+=box(560,40,400,300,"panel2","line",rx=18)+T(590,84,"Private DNS",20,bold=True)
for i,(lab,on) in enumerate((("Off",False),("Automatic",False),("Private DNS provider hostname",True))):
    y=120+i*44
    body+=f'<circle cx="600" cy="{y}" r="10" fill="none" stroke="{C["blue"] if on else C["dim"]}" stroke-width="2.5"/>'+(f'<circle cx="600" cy="{y}" r="5" fill="{C["blue"]}"/>' if on else "")
    body+=T(624,y+6,lab,16,"text" if on else "muted")
body+=box(590,240,340,44,"term","blue",rx=8,sw=2)+T(606,268,"dns.adguard-dns.com",16,"yellow",mono=True)
body+=T(930,318,"Save",16,"blue",bold=True,anchor="end")
ct,_=TL(40,140,"Settings › Network & internet › Private DNS",460,17,mono=True,fill="yellow")
body+=ct+icon("phone",60,200,110,"muted")
tt,_=TL(170,232,"Family filter instead: family.adguard-dns.com",330,15,fill="muted")
body+=tt
raw(IMG+"dns-filtering-android.svg",380,body)
header_md("DNS-Filtering","dns-filtering-header.svg","A filtering DNS server answers example.com normally and returns 0.0.0.0 for ad and tracker domains")
replace_img("DNS-Filtering","/static/img/dns-filtering-compare.svg","dns-filtering-compare.svg","Matrix of AdGuard DNS, Epsilon Eight, CleanBrowsing, OpenDNS FamilyShield, Quad9, Cloudflare for Families and Pi-hole by whether they block ads, malware and adult content")
replace_img("DNS-Filtering","/static/img/dns-filtering-android.svg","dns-filtering-android.svg","Android Private DNS settings with the provider hostname set to dns.adguard-dns.com")

# letsencrypt 2019
header(IMG+"letsencrypt-certbot-header.svg","Self-hosting · HTTPS",["Free HTTPS with","Let's Encrypt"],"certbot certificate for Home Assistant behind nginx",chip="certbot certonly --standalone",accent="blue",
  motif=[logo("letsencrypt",590,96,120),link(730,156,790,156),icon("cert",800,80,150,"muted","green")])
flow(IMG+"letsencrypt-certbot-renew.svg","Monthly renewal with the standalone plugin",[
  dict(t="Stop nginx",d="frees port 80",state="yellow"),dict(t="certbot renew",d="standalone on :80",state="blue"),
  dict(t="New cert",d="/etc/letsencrypt"),dict(t="Start nginx",d="serves new cert",state="green")],
  sub="certbot and nginx share the box, so nginx has to step aside for a minute",
  note="Cron: 0 0 1 * *  stop nginx; certbot renew; start nginx")
header_md("LetsEncrypt-Certificates","letsencrypt-certbot-header.svg","Let's Encrypt certificate issued with certbot for Home Assistant behind nginx")
remove_img("LetsEncrypt-Certificates","/static/img/letsencrypt.png")
replace_img("LetsEncrypt-Certificates","/static/img/certbot-logo.png","letsencrypt-certbot-renew.svg","Monthly renewal: stop nginx to free port 80, run certbot renew in standalone mode, the new certificate lands in /etc/letsencrypt/live, start nginx again")

# mqtt
m=[icon("thermo",590,70,64,"muted","red"),icon("power",590,160,60,"muted","yellow"),icon("board",586,244,70,"muted","red")]
m+=[link(664,105,746,180,"line",3),link(664,190,746,180,"line",3),link(664,276,746,180,"line",3)]
m+=[logo("eclipsemosquitto",756,136,88,"text"),link(856,180,880,180),logo("homeassistant",890,150,60)]
header(IMG+"mqtt-header.svg","Raspberry Pi · MQTT",["Mosquitto broker","with a password"],"Lock down MQTT before Home Assistant and sensors connect",chip="password_file /etc/mosquitto/passwordfile",accent="purple",motif=m)
flow(IMG+"mqtt-pubsub.svg","Publish and subscribe through the broker",[
  dict(t="Sensor / script",d="mosquitto_pub"),dict(t="Mosquitto",d=":1883 user+password",state="purple"),dict(t="Home Assistant",d="subscribes",state="green")],
  arrows=[("test/topic","blue",None),("test/topic","blue",None)],
  note="Without -u and -P the broker refuses the connection: allow_anonymous false.")
header_md("Install-MQTT-Broker","mqtt-header.svg","Sensors publish to a password-protected Mosquitto broker on a Raspberry Pi, and Home Assistant subscribes")
insert_before("Install-MQTT-Broker","## 5. Test it","mqtt-pubsub.svg","A sensor publishes to test/topic on the Mosquitto broker with a username and password; Home Assistant subscribes to the same topic")

# ssh keys
m=[icon("laptop",580,110,130,"muted"),icon("key",608,232,70,"yellow"),link(716,175,790,175),icon("server",800,95,150,"muted","green"),icon("lock",880,240,44,"green","green")]
header(IMG+"ssh-keys-header.svg","Linux · SSH",["SSH without","a password"],"One Ed25519 key pair, the public half on every server",chip="ssh-copy-id user@host",accent="yellow",motif=m)
body=T(40,52,"Which half goes where",22,bold=True)+T(40,80,"The private key never leaves your machine",15,"muted")
body+=box(40,110,400,200,"panel","line",rx=12)+icon("laptop",64,130,60,"muted")+T(140,162,"Your laptop",18,bold=True)
body+=T(64,216,"~/.ssh/id_ed25519",15,"red",mono=True)+T(64,240,"private: keep secret",14,"muted")
body+=T(64,276,"~/.ssh/id_ed25519.pub",15,"green",mono=True)
body+=box(560,110,400,200,"panel","line",rx=12)+icon("server",584,130,60,"muted","green")+T(660,162,"Server",18,bold=True)
body+=T(584,216,"~/.ssh/authorized_keys",15,"green",mono=True)+T(584,240,"one line per allowed key",14,"muted")
body+=T(584,276,"PasswordAuthentication no",15,"yellow",mono=True)
body+=arrow(300,272,576,224,"green",curve=(440,272,440,224))+T(500,206,"ssh-copy-id",14,"green",mono=True,anchor="middle")
raw(IMG+"ssh-keys-where.svg",350,body)
header_md("ssh-without-password","ssh-keys-header.svg","An Ed25519 key on a laptop, the public key copied to a server, and a passwordless SSH login")
insert_before("ssh-without-password","## 3. Copy the key","ssh-keys-where.svg","The private key id_ed25519 stays on your laptop; ssh-copy-id appends id_ed25519.pub to authorized_keys on the server")

# ubuntu gsettings
m=[icon("desktop",584,80,200,"muted")]
m+=[box(616,118,22,100,"panel2","blue",rx=6,sw=2)]+[f'<circle cx="627" cy="{136+i*22}" r="6" fill="{C["blue" if i==0 else "dim"]}"/>' for i in range(4)]
m+=[mini_term(800,90,180,["[[green|$]] gsettings","  set ... 'minimize'"],13)]
header(IMG+"ubuntu-gsettings-header.svg","Ubuntu · GNOME",["Tweak Ubuntu","from the terminal"],"gsettings one-liners for the dock, Files and wallpapers",chip="gsettings set ... click-action 'minimize'",accent="orange",motif=m)
cards(IMG+"ubuntu-gsettings-tweaks.svg",[
  dict(name="Minimize on click",icon="window",accent="orange",desc="Click a dock icon to hide its window"),
  dict(name="Transparent dock",icon="desktop",color="muted",desc="FIXED mode, background-opacity 0.2"),
  dict(name="Full path in Files",icon="folder",accent="yellow",desc="Always show the location entry"),
  dict(name="Wallpaper slideshow",icon="clock",accent="blue",desc="Random photo from a folder via cron"),
 ],cols=2,title="Four tweaks in this post",sub="each reversible with gsettings reset")
header_md("Ubuntu-Customizations-CLI","ubuntu-gsettings-header.svg","Ubuntu dock and terminal: gsettings commands for minimize-on-click and dock transparency")
insert_before("Ubuntu-Customizations-CLI","## How do I enable","ubuntu-gsettings-tweaks.svg","Four Ubuntu tweaks: minimize on click, transparent dock, full path in Files, wallpaper slideshow")

# useful cli tools
header(IMG+"useful-cli-tools-header.svg","Linux · command line",["CLI tools I install","everywhere"],"fd, jq, bat, duf, eza, btop and friends",chip="sudo apt install fd-find jq bat",accent="green",
  motif=[mini_term(590,70,370,["[[green|$]] fd -e md","[[blue|_posts/]]2026-11-28-android.md","[[green|$]] duf","[[muted|/      ]][[green|▇▇▇▇▇▇▇▁▁▁]] 68%","[[green|$]] bat config.toml"],15,"~")])
cards(IMG+"useful-cli-tools-overview.svg",[
  dict(name="fd",icon="search",accent="green",desc="Faster, friendlier find"),dict(name="jq",logo="json",logo_color="text",desc="Slice and filter JSON"),
  dict(name="bat",icon="file",accent="blue",desc="cat with syntax highlighting"),dict(name="fff",icon="folder",accent="yellow",desc="Tiny bash file manager"),
  dict(name="duf",icon="database",accent="green",desc="Readable disk usage"),dict(name="eza",icon="list",accent="blue",desc="Modern ls with git status"),
  dict(name="oh my zsh",logo="zsh",logo_color="text",desc="Themes and plugins for zsh"),dict(name="btop",icon="chart",accent="green",desc="Resource monitor"),
  dict(name="HTTPie",logo="httpie",desc="curl for humans"),
 ],title="The nine tools at a glance")
header_md("Useful-cli-tools","useful-cli-tools-header.svg","Terminal showing fd, duf and bat: command-line tools I install on every Linux machine")
insert_before("Useful-cli-tools","## fd","useful-cli-tools-overview.svg","Nine CLI tools: fd, jq, bat, fff, duf, eza, oh my zsh, btop and HTTPie, each with a one-line description")

# samba fstab
m=[icon("server",590,90,130,"muted","green"),link(730,155,790,155),icon("folder",800,96,130,"muted"),T(865,252,"/mnt/share",15,"yellow",mono=True,anchor="middle"),T(655,252,"//nas/share",15,"muted",mono=True,anchor="middle")]
header(IMG+"samba-fstab-header.svg","Ubuntu · Samba",["Mount a Samba share","at boot"],"One line in /etc/fstab and a root-only credentials file",chip="credentials=/root/.smbcredentials",accent="yellow",motif=m)
compare(IMG+"samba-fstab-compare.svg",
  dict(kicker="quick version",title="Password in fstab",items=["Password written into /etc/fstab","/etc/fstab is world-readable","Every user can read the password"],state="red",foot="username=...,password=..."),
  dict(kicker="safer version",title="Credentials file",items=["Password in /root/.smbcredentials","chmod 600: only root can read it","fstab only points at the file"],state="green",foot="credentials=/root/.smbcredentials"))
header_md("mount-sama-share-fstab","samba-fstab-header.svg","Samba share //nas/share mounted at /mnt/share on boot through /etc/fstab")
insert_before("mount-sama-share-fstab","## Safer version","samba-fstab-compare.svg","Quick version puts the password in world-readable /etc/fstab; safer version keeps it in /root/.smbcredentials with chmod 600")

# git credentials
m=[mini_term(580,70,380,["[[green|$]] git push","Username: you","Password: [[red|●●●●●●●●]]","[[red|remote: Support for password]]","[[red|authentication was removed]]"],14)]
header(IMG+"git-credentials-header.svg","Git · GitHub",["Stop typing your","GitHub token"],"Credential helper, token URL or the GitHub CLI",chip="gh auth login",accent="orange",motif=m)
matrix(IMG+"git-credentials-options.svg",["token stored","scope"],[
  ("Token in the remote URL","git remote set-url",["[[red|.git/config, plain]]","one repo"]),
  ("credential.helper store","git config --global",["[[red|~/.git-credentials]]","all repos"]),
  ("credential.helper cache","--timeout=3600",["[[yellow|memory, 1 hour]]","all repos"]),
  ("GitHub CLI (recommended)","gh auth login",["[[green|managed by gh]]","all repos"])],
  title="The options compared",legend=False,label_w=400)
header_md("set-git-origin","git-credentials-header.svg","git push asking for a GitHub password and failing, fixed with a credential helper or gh auth login")
insert_before("set-git-origin","## Check which remote","git-credentials-options.svg","Comparison: token in remote URL and credential.helper store keep the token in plain text; cache and the GitHub CLI do not; only the URL method is per repository")

# bluetooth rename
m=[logo("bluetooth",600,110,110),link(724,165,780,165),box(790,110,170,48,"panel","line",rx=8)+T(808,141,"S530",17,"dim",mono=True),
   f'<line x1="800" y1="134" x2="880" y2="134" stroke="{C["red"]}" stroke-width="3"/>',box(790,180,170,48,TINT["green"],"green",rx=8,sw=2)+T(808,211,"S530 Blue",17,"green",mono=True)]
header(IMG+"bt-rename-header.svg","Ubuntu · Bluetooth",["Rename a","Bluetooth device"],"Give paired devices a readable alias from the terminal",chip='bt-device --set S530 Alias "S530 Blue"',accent="blue",motif=m)
terminal(IMG+"bt-rename-terminal.svg",[("$","bluetoothctl"),("out","[bluetooth]# devices"),("out","Device AA:BB:CC:DD:EE:FF S530"),("out","[bluetooth]# connect AA:BB:CC:DD:EE:FF"),("hl","[S530]# set-alias \"S530 Blue\""),("ok","Changing S530 Blue succeeded"),("out","[S530 Blue]# exit")],title="Option 2 in one bluetoothctl session")
header_md("ubuntu-rename-bluetooth","bt-rename-header.svg","Renaming a paired Bluetooth device from S530 to S530 Blue in Ubuntu")
insert_before("ubuntu-rename-bluetooth","## Option 2","bt-rename-terminal.svg","bluetoothctl session: list devices, connect to the S530, set-alias S530 Blue, exit")
