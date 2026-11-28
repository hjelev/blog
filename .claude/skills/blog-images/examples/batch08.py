import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "postedit.py")).read())

# rpi-mqtt-monitor
m=[logo("raspberrypi",584,110,100),link(700,160,750,160),logo("mqtt",760,130,60,"text"),link(830,160,860,160),logo("homeassistant",870,128,64)]
m+=[T(634,250,"52.1 °C",16,"yellow",mono=True,anchor="middle"),T(790,250,"OK",16,"green",mono=True,bold=True,anchor="middle"),T(902,250,"sensors",14,"muted",mono=True,anchor="middle")]
header(IMG+"rpi-mqtt-monitor-header.svg","Raspberry Pi · Home Assistant",["Monitor a Pi in","Home Assistant"],"Temperature, disk, memory and power problems over MQTT",chip="rpi-mqtt-monitor --config",accent="red",motif=m)
flow(IMG+"rpi-mqtt-monitor-flow.svg","How the readings reach Home Assistant",[
  dict(t="Your Pi",d="rpi-mqtt-monitor"),dict(t="Mosquitto",d="MQTT broker",state="purple"),dict(t="Home Assistant",d="MQTT discovery",state="blue"),dict(t="Dashboard & alerts",d="sensors + buttons",state="green")],
  arrows=[("publish","blue",None),None,None],note="Run it as a systemd service: buttons in Home Assistant don't work under cron.")
cards(IMG+"rpi-mqtt-monitor-power.svg",[
  dict(name="OK",icon="check",accent="green",desc="Power and temperature are fine",border="green"),
  dict(name="Under-voltage",icon="bolt",color="red",desc="Power supply too weak: causes all sorts of strange problems",border="red"),
  dict(name="Soft temperature limit",icon="thermo",accent="orange",desc="Getting hot; check the cooler"),
  dict(name="ARM frequency capped",icon="chip",accent="yellow",desc="CPU clock limited"),
  dict(name="Throttled",icon="warning",accent="red",desc="Running slower than it should"),
 ],title="What rpi_power_status reports",sub="from vcgencmd get_throttled; turn it on for every Pi")
header_md("monitor-raspberry-pi-home-assistant","rpi-mqtt-monitor-header.svg","rpi-mqtt-monitor: a Raspberry Pi publishes temperature and power status over MQTT to Home Assistant")
insert_before("monitor-raspberry-pi-home-assistant","## What you need","rpi-mqtt-monitor-flow.svg","The Pi runs rpi-mqtt-monitor and publishes to Mosquitto; Home Assistant picks up the sensors through MQTT discovery for dashboards and alerts")
insert_before("monitor-raspberry-pi-home-assistant","## Alerts that are actually useful","rpi-mqtt-monitor-power.svg","rpi_power_status values: OK, Under-voltage, Soft temperature limit, ARM frequency capped and Throttled")

# rpi price rise
m=[icon("board",590,150,120,"muted","red")]
for i,(lab,v) in enumerate((("Jan 2025",120),("Dec 2025",145),("Feb 2026",205),("Apr 2026",305),("Nov 2026",385))):
    x=740+i*44; h=v*0.52
    m+=[box(x,290-h,30,h,"red" if i==4 else "line",None,rx=4)]
m+=[T(948,80,"$385",22,"red",bold=True,mono=True,anchor="end"),T(742,312,"$120",13,"muted",mono=True)]
header(IMG+"rpi-price-rise-header.svg","Raspberry Pi · buying guide",["The 16GB Pi 5","now costs $385"],"Current prices, a full build against a mini PC, and what to buy",chip="above ~$175: look at a mini PC",accent="red",motif=m)
bars(IMG+"rpi-price-rise-history.svg",[("Jan 2025 (launch)",120,"dim"),("Dec 1, 2025",145,"orange"),("Feb 2, 2026",205,"orange"),("Apr 1, 2026",305,"red"),("Nov 2, 2026",385,"red")],title="Raspberry Pi 5 16GB list price",sub="more than three times the launch price",fmt=lambda v:f"${v}",max_v=400)
bars(IMG+"rpi-price-rise-builds.svg",[("Pi 5 2GB build",233.40,"blue","512GB NVMe, PSU, cooler, M.2 HAT+"),("Pi 5 4GB build",265.90,"blue"),("Pi 5 8GB build",330.90,"blue"),("Pi 5 16GB build",540.90,"red"),("N150 mini PC 12GB",329,"green","Beelink Mini S13, 512GB SSD"),("N150 mini PC 16GB",349,"green")],
  title="A full home-server build vs a mini PC",fmt=lambda v:f"${v:,.2f}".replace(".00",""),max_v=560)
header_md("raspberry-pi-price-rise","rpi-price-rise-header.svg","Raspberry Pi 5 16GB price rising from $120 at launch to $385 in November 2026")
insert_after("raspberry-pi-price-rise","| November 2, 2026 |","rpi-price-rise-history.svg","Raspberry Pi 5 16GB price: $120 at launch, $145 December 2025, $205 February 2026, $305 April 2026, $385 November 2026")
insert_before("raspberry-pi-price-rise","### Performance and power","rpi-price-rise-builds.svg","Full build totals: Pi 5 2GB $233.40, 4GB $265.90, 8GB $330.90, 16GB $540.90, against N150 mini PCs at $329 and $349")

# wp core upgrade rce
m=[logo("wordpress",590,96,96,"text"),mini_term(720,70,250,["[[muted|updating core…]]","[[yellow|wp-content/upgrade/]]","[[red|GET …/upgrade/x.php]]","[[red|200 OK]]"],14)]
header(IMG+"wp-cve-2026-119977-header.svg","WordPress · CVE-2026-119977",["RCE during a","core update"],"The staging folder is reachable for a few seconds",chip="block /wp-content/upgrade/ first",accent="blue",chip_color="red",motif=m)
flow(IMG+"wp-cve-2026-119977-window.svg","The upgrade window",[
  dict(t="Core update starts",d="auto or manual"),dict(t="Release unpacked",d="…/upgrade/",state="yellow"),dict(t="Reachable over HTTP",d="a few seconds",state="red"),dict(t="Attacker hits PHP file",d="code runs",state="red"),dict(t="Update finishes",d="folder removed",dashed=True)],
  note="Attackers poll the folder constantly. Blocking /wp-content/upgrade/ in the web server closes the window.")
checklist(IMG+"wp-cve-2026-119977-order.svg",[
  ("Block the staging folder","deny /wp-content/upgrade/ in nginx or Apache","red"),
  ("Update WordPress","7.1.4 · 7.0.8 · 6.9.11 · 6.8.12 (4.7.39 on 4.7)","green"),
  ("Don't rely on a plugin firewall alone","a direct hit on a staged PHP file may never load the plugin","yellow"),
  ("Check your logs","requests to /wp-content/upgrade/ around your last update","blue")],title="Do it in this order")
header_md("wordpress-core-upgrade-rce","wp-cve-2026-119977-header.svg","WordPress upgrade-window RCE: during a core update an attacker requests a PHP file from wp-content/upgrade and gets 200 OK")
insert_before("wordpress-core-upgrade-rce","### How sure is the CVE number?","wp-cve-2026-119977-window.svg","The upgrade window: a core update unpacks the release into wp-content/upgrade, which is reachable over HTTP for a few seconds, letting an attacker run a PHP file before the folder is removed")
insert_before("wordpress-core-upgrade-rce","### 1. If you aren't patched","wp-cve-2026-119977-order.svg","Order: block /wp-content/upgrade/ first, update WordPress, don't rely only on a plugin firewall, then check logs for requests to the upgrade folder")

# ubuntu 26.10
m=[logo("ubuntu",590,100,110),T(645,260,"26.04 LTS",15,"muted",mono=True,anchor="middle"),link(716,155,790,155),box(800,110,160,90,TINT["orange"],"orange",rx=12,sw=2),T(880,150,"26.10",28,"orange",bold=True,mono=True,anchor="middle"),T(880,180,"Stonking Stingray",13,"muted",anchor="middle"),T(880,240,"do-release-upgrade -d",13,"dim",mono=True,anchor="middle")]
header(IMG+"ubuntu-2610-upgrade-header.svg","Ubuntu · upgrade",["Upgrade 26.04","to 26.10?"],"Why it isn't offered yet, what breaks, and how to do it",accent="orange",motif=m)
bars(IMG+"ubuntu-2610-support.svg",[("26.04 LTS",60,"green","standard support, no required upgrade for years"),("26.10",9,"orange","until July 2027, then upgrade to 27.04")],title="How long each release is supported",unit=" months",max_v=64,label_w=160)
decision(IMG+"ubuntu-2610-should-i.svg","TPM-backed disk encryption, or /boot encrypted, on Btrfs, XFS, ZFS or RAID-5/6?",("Stay on 26.04 LTS","These setups can fail to boot after the upgrade"),("You can upgrade","Install all 26.04 updates first, then do-release-upgrade -d"),yes_label="yes",no_label="no",title="Should this machine upgrade?",yes_state="orange",no_state="green")
header_md("upgrade-ubuntu-26-04-to-26-10","ubuntu-2610-upgrade-header.svg","Upgrading Ubuntu 26.04 LTS to 26.10 with do-release-upgrade -d")
insert_after("upgrade-ubuntu-26-04-to-26-10","| **Good for** |","ubuntu-2610-support.svg","Support length: 26.04 LTS gets 5 years of standard support, 26.10 gets 9 months until July 2027")
insert_before("upgrade-ubuntu-26-04-to-26-10","### TPM-backed disk encryption","ubuntu-2610-should-i.svg","If the disk uses TPM-backed encryption or /boot is encrypted, on Btrfs, XFS, ZFS or RAID-5/6, stay on 26.04; otherwise install all updates and upgrade with do-release-upgrade -d")
