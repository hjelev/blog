import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "postedit.py")).read())

# free windows software
header(IMG+"free-windows-software-header.svg","Windows · free tools",["Free Windows","software I keep"],"Transfers, SSH, archives, search, USB images and services",chip="winget install 7zip.7zip",accent="blue",
  motif=[icon("windows",590,80,120,"blue","blue"),icon("folder",740,70,86,"muted","yellow"),icon("terminal",850,80,86,"muted","green"),logo("7zip",756,200,64,"text"),icon("sdcard",858,190,80,"muted","blue"),icon("search",620,224,64,"muted")])
cards(IMG+"free-windows-software-groups.svg",[
  dict(name="Files & SSH",icon="terminal",accent="green",desc="WinSCP, KiTTY, FileZilla, Everything"),
  dict(name="Disks & USB",icon="sdcard",accent="blue",desc="Rufus, Win32 Disk Imager, FAT32 Format, SD Card Formatter, MiniTool"),
  dict(name="Media & cameras",icon="camera",accent="red",desc="Yawcam, iSpy, VirtualDub, Squeezelite"),
  dict(name="Editors",icon="code",color="muted",desc="Notepad++, Inkscape, Calibre"),
  dict(name="System",icon="gear",color="muted",desc="Open Hardware Monitor, NSSM, Cmdow, 7-Zip"),
  dict(name="Android",logo="android",desc="Minimal ADB and Fastboot"),
 ],title="The list, by job",sub="21 free tools in six groups")
header_md("free-windows-software","free-windows-software-header.svg","Free Windows software: file transfer, SSH, archives, search, USB imaging and service tools")
insert_after("free-windows-software","- [Yawcam]","free-windows-software-groups.svg","The free Windows tools grouped by job: files and SSH, disks and USB, media and cameras, editors, system, and Android")
# that insert lands after the whole list (list is one block) — fine

# rpi software
header(IMG+"rpi-software-header.svg","Raspberry Pi · self-hosting",["Software for","your Raspberry Pi"],"Ad blocking, VPN, home automation and printing on a $15 board",accent="red",
  motif=[icon("board",600,110,150,"muted","red"),logo("pihole",800,70,56),logo("homeassistant",880,110,56),logo("adguard",800,160,56),icon("vpn",880,190,60,"muted","green"),link(752,185,790,185)])
cards(IMG+"rpi-software-roles.svg",[
  dict(name="Pi-hole",logo="pihole",desc="Network-wide ad blocking at the DNS level",tag="DNS",tag_color="blue"),
  dict(name="AdGuard Home",logo="adguard",desc="Pi-hole alternative with DoH/DoT built in",tag="DNS",tag_color="blue"),
  dict(name="PiVPN",icon="vpn",accent="green",desc="One-command WireGuard or OpenVPN server",tag="VPN"),
  dict(name="Home Assistant",logo="homeassistant",desc="Local home automation for every device",tag="home",tag_color="yellow"),
  dict(name="CUPS",icon="file",accent="blue",desc="Turn a USB printer into a network printer",tag="print",tag_color="purple"),
 ],title="What each one does",sub="all run happily on a Pi 3 or newer")
header_md("rpi-software","rpi-software-header.svg","Software for a Raspberry Pi: Pi-hole, AdGuard Home, PiVPN, Home Assistant and CUPS")
insert_after("rpi-software","- [CUPS]","rpi-software-roles.svg","Pi-hole and AdGuard Home block ads via DNS, PiVPN runs a VPN server, Home Assistant automates the home and CUPS shares a printer")

# web cameras
header(IMG+"web-cameras-header.svg","Fun · live webcams",["Free live","webcams"],"Sites that stream public cameras from around the world",accent="red",
  motif=[icon("globe",760,80,190,"line","blue"),icon("camera",600,130,130,"muted","red"),f'<circle cx="640" cy="160" r="9" fill="{C["red"]}"/>',
         T(600,300,"[[red|●]] LIVE",15,"muted",mono=True)])
cards(IMG+"web-cameras-sites.svg",[
  dict(name="EarthCam",icon="camera",accent="red",desc="Biggest network, with search"),
  dict(name="Lookr",icon="globe",accent="blue",desc="Scenic places, timelapses"),
  dict(name="WebcamHopper",icon="search",desc="Jump between random cams"),
  dict(name="weather-webcam.eu",icon="thermo",accent="yellow",desc="Bulgaria and Europe weather cams"),
 ],cols=2,title="Where to watch")
header_md("web-cameras","web-cameras-header.svg","Free live webcams: sites that stream public cameras from around the world")
remove_img("web-cameras","/static/img/ip-camera.png")
insert_after("web-cameras","- [weather-webcam.eu]","web-cameras-sites.svg","Four webcam sites: EarthCam, Lookr, WebcamHopper and weather-webcam.eu")

# python modules
header(IMG+"python-modules-header.svg","Python · libraries",["Python modules","I actually use"],"Small libraries for parsing, scraping, MQTT and SSH automation",accent="yellow",
  motif=[logo("python",600,70,110),mini_term(740,90,230,["[[purple|import]] feedparser","[[purple|import]] paho.mqtt","[[purple|from]] bs4 [[purple|import]] ..","[[purple|import]] fabric"],13)])
cards(IMG+"python-modules-groups.svg",[
  dict(name="Text & web",icon="code",accent="yellow",desc="Markdown, BeautifulSoup, FeedParser, tldextract, web.py"),
  dict(name="Remote & APIs",icon="terminal",accent="green",desc="Fabric (SSH), Python JIRA, EasyWebDAV"),
  dict(name="Hardware & IoT",logo="mqtt",desc="Paho-MQTT, Adafruit DHT sensor library"),
  dict(name="Storage",icon="database",accent="blue",desc="Pickle for saving Python objects to disk"),
 ],cols=2,title="Grouped by what they're for")
header_md("python-modules","python-modules-header.svg","Python modules I use: feedparser, paho-mqtt, BeautifulSoup and Fabric")
insert_after("python-modules","- [Markdown]","python-modules-groups.svg","Python modules grouped: text and web parsing, remote and APIs, hardware and IoT, storage")

# rpi os
header(IMG+"rpi-os-header.svg","Raspberry Pi · operating systems",["Raspberry Pi","OS beyond Raspbian"],"Distros for gaming, media, cameras and minimal servers",accent="red",
  motif=[icon("sdcard",590,90,120,"muted"),icon("sdcard",680,110,120,"blue"),icon("sdcard",770,90,120,"red"),icon("sdcard",860,110,110,"green"),
         T(650,270,"DietPi",14,"muted",mono=True,anchor="middle"),T(740,290,"RetroPie",14,"blue",mono=True,anchor="middle"),T(830,270,"Volumio",14,"red",mono=True,anchor="middle"),T(915,290,"motionEye",14,"green",mono=True,anchor="middle")])
cards(IMG+"rpi-os-uses.svg",[
  dict(name="Gaming",icon="chip",accent="blue",desc="RetroPie, Recalbox, PiPlay"),
  dict(name="Music & TV",icon="speaker",accent="red",desc="Volumio, Pi MusicBox, OpenELEC"),
  dict(name="Cameras",icon="camera",accent="green",desc="motionEyeOS"),
  dict(name="Lightweight server",icon="server",accent="green",desc="DietPi, Minibian"),
  dict(name="Desktop",logo="ubuntu",desc="Ubuntu MATE, SUSE"),
  dict(name="Beginners",icon="package",accent="yellow",desc="NOOBS"),
 ],title="Pick by what the Pi will do")
header_md("rpi-os-distributions","rpi-os-header.svg","Raspberry Pi operating systems: DietPi, RetroPie, Volumio and motionEyeOS SD cards")
insert_after("rpi-os-distributions","- [motionEyeOS]","rpi-os-uses.svg","Raspberry Pi distributions by use: gaming, music and TV, cameras, lightweight server, desktop, beginners")
