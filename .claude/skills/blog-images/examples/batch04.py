import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "postedit.py")).read())

# how i like my ubuntu
m=[icon("desktop",584,70,210,"muted"),box(608,206,162,16,"panel2","orange",rx=4,sw=1.5)]+[f'<circle cx="{622+i*18}" cy="214" r="4" fill="{C["orange" if i==0 else "dim"]}"/>' for i in range(5)]
m+=[T(740,130,"12:45",22,"text",bold=True,mono=True,anchor="end"),logo("ubuntu",620,100,44)]
m+=fan(800,170,["gnome",("icon","package","yellow"),("icon","window","orange")],x=880,size=40,step=82)
header(IMG+"my-ubuntu-header.svg","Ubuntu · GNOME",["How I like","my Ubuntu"],"The extensions and apps I add after every fresh install",chip="sudo apt install gnome-shell-extension-manager",accent="orange",motif=m)
cards(IMG+"my-ubuntu-setup.svg",[
  dict(name="Dash to Panel",logo="gnome",logo_color="text",desc="Dock and top bar merged into one taskbar",tag="extension",tag_color="orange"),
  dict(name="Desktop Clock",icon="clock",accent="orange",desc="A clock widget on the desktop",tag="extension",tag_color="orange"),
  dict(name="ArcMenu",icon="list",accent="orange",desc="Start-menu style app launcher",tag="extension",tag_color="orange"),
  dict(name="Variety",icon="desktop",accent="blue",desc="Downloads and rotates wallpapers",tag="app",tag_color="blue"),
  dict(name="AppImageLauncher",icon="package",accent="yellow",desc="Integrates AppImages into the menu",tag="app",tag_color="blue"),
 ],title="What goes on",sub="three extensions, two apps")
header_md("how-i-like-my-ubuntu","my-ubuntu-header.svg","Ubuntu desktop with a single taskbar, desktop clock and the GNOME extensions I install")
insert_before("how-i-like-my-ubuntu","## Installing GNOME extensions","my-ubuntu-setup.svg","Dash to Panel, Desktop Clock and ArcMenu extensions plus the Variety and AppImageLauncher apps")

# squeezelite
m=[icon("speaker",590,90,140,"muted","green"),link(700,160,760,160)]
m+=[box(770,86,190,52,TINT["red"],"red",rx=10)+T(790,118,"system service",15,"red",mono=True)]
m+=[box(770,170,190,52,TINT["green"],"green",rx=10)+T(790,202,"user autostart",15,"green",mono=True)]
header(IMG+"squeezelite-header.svg","Linux · audio",["Squeezelite won't","share the speakers"],"Why the systemd service blocks other audio, and the fix",chip="squeezelite -o pipewire",accent="green",motif=m)
compare(IMG+"squeezelite-compare.svg",
  dict(kicker="system service",title="Runs as a system user",items=["hw: device: takes the card exclusively","default / pulse: “Host is down”","No access to your PipeWire session"],state="red",foot="systemctl disable squeezelite"),
  dict(kicker="user autostart",title="Runs in your session",items=["Starts when you log in","Talks to PipeWire like any app","Mixes with browser and desktop sound"],state="green",foot="~/.config/autostart/squeezelite.desktop"),title="Why moving it fixes the sound")
header_md("squeezelite-wont-mix","squeezelite-header.svg","Squeezelite as a system service blocks other audio; as a user autostart app it mixes through PipeWire")
insert_before("squeezelite-wont-mix","## ✅ The Easy Fix","squeezelite-compare.svg","As a system service Squeezelite either grabs the sound card exclusively or fails with Host is down; as a user autostart app it joins the PipeWire session and mixes with other audio")

# wireguard mikrotik
m=[logo("mikrotik",590,128,96,"text"),T(638,262,"10.0.0.1",14,"muted",mono=True,anchor="middle"),logo("wireguard",728,150,52)]
m+=[link(700,176,722,176,"line",3),link(786,176,852,110,"muted",3),link(786,176,852,240,"muted",3)]
m+=[icon("phone",860,60,90,"muted"),icon("laptop",860,196,90,"muted"),T(905,166,"10.0.0.2",13,"muted",mono=True,anchor="middle"),T(905,306,"10.0.0.3",13,"muted",mono=True,anchor="middle")]
header(IMG+"wireguard-header.svg","Networking · VPN",["WireGuard on","a MikroTik router"],"RouterOS 7 server with Android and Windows 11 clients",chip="udp 13231 › accept",accent="red",motif=m)
body=T(40,52,"The finished setup",22,bold=True)+T(40,80,"One wireguard1 interface, one /32 peer per device",15,"muted")
body+=box(40,120,250,230,"panel","line",rx=12)+icon("phone",60,140,52,"muted")+T(120,164,"Android",17,bold=True)+T(120,186,"10.0.0.2",14,"muted",mono=True)
body+=T(60,232,"AllowedIPs",13,"dim",mono=True)+T(60,256,"0.0.0.0/0",15,"yellow",mono=True)+T(60,280,"full tunnel",14,"muted")
body+=T(60,316,"or 192.168.88.0/24",14,"muted",mono=True)
body+=box(710,120,250,230,"panel","line",rx=12)+icon("laptop",730,140,52,"muted")+T(790,164,"Windows 11",17,bold=True)+T(790,186,"10.0.0.3",14,"muted",mono=True)
body+=T(730,232,"AllowedIPs",13,"dim",mono=True)+T(730,256,"192.168.88.0/24",15,"green",mono=True)+T(730,280,"split tunnel",14,"muted")
body+=box(370,150,260,170,TINT["red"],"red",rx=12,sw=2)+logo("mikrotik",392,172,40,"text")+T(446,192,"MikroTik",17,bold=True)+T(446,214,"wireguard1",14,"muted",mono=True)
body+=T(392,252,"10.0.0.1/24",15,"text",mono=True)+T(392,276,"udp 13231 open",15,"green",mono=True)+T(392,300,"LAN 192.168.88.0/24",14,"muted",mono=True)
body+=arrow(294,235,366,235,"blue",dash="6 5")+arrow(706,235,634,235,"blue",dash="6 5")
body+=T(500,378,"Each peer's /32 on the router must match the client's Address, or you get 0 B received.",15,"yellow",anchor="middle")
raw(IMG+"wireguard-topology.svg",400,body)
checklist(IMG+"wireguard-0b-received.svg",[
  ("Key swap","The router holds the client's public key, the client holds the router's","yellow"),
  ("Address mismatch","Client 10.0.0.3 must match the peer's Allowed Address 10.0.0.3/32","blue"),
  ("CGNAT or dynamic IP","Behind carrier NAT a direct handshake can't work; use Cloud DDNS for a changing IP","red")],title="“Active” but 0 B received?",sub="the handshake is failing; check these three")
header_md("WireGuard-VPN-on-MikroTik","wireguard-header.svg","MikroTik router running WireGuard at 10.0.0.1 with an Android phone at 10.0.0.2 and a Windows laptop at 10.0.0.3")
insert_before("WireGuard-VPN-on-MikroTik","## Phase 1","wireguard-topology.svg","Topology: MikroTik wireguard1 at 10.0.0.1/24 listening on UDP 13231; Android peer 10.0.0.2 with full tunnel 0.0.0.0/0, Windows peer 10.0.0.3 with split tunnel 192.168.88.0/24")
insert_after("WireGuard-VPN-on-MikroTik","If your client says \"Active\"","wireguard-0b-received.svg","0 B received checklist: swapped public keys, client address not matching the peer's /32, CGNAT or a dynamic public IP")
