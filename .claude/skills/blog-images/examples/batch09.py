import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "postedit.py")).read())

# kernel tcp
m=[logo("linux",590,90,100,"text")]
for i,(t,c) in enumerate((("SYN + IP options","blue"),("SYN (retransmit)","orange"),("options freed","red"))):
    m.append(box(730,82+i*62,230,46,TINT[c],c,rx=8,sw=2)+T(748,111+i*62,t,15,c,mono=True))
m+=[T(640,240,"CVSS 9.8",20,"red",bold=True,mono=True,anchor="middle"),link(700,140,722,140,"line",3)]
header(IMG+"linux-tcp-cve-2026-98432-header.svg","Linux kernel · CVE-2026-98432",["TCP use-after-free:","patch and reboot"],"A retransmitted SYN reads IPv4 options that were already freed",chip="sudo reboot",accent="red",chip_color="green",motif=m)
flow(IMG+"linux-tcp-cve-2026-98432-race.svg","The race",[
  dict(t="SYN with IPv4 options",d="stored on request sock"),dict(t="Handshake completes",d="child takes pointer"),
  dict(t="SYN retransmitted",d="other CPU builds SYN-ACK",state="yellow"),dict(t="Child destroyed",d="options kfree()d"),dict(t="SYN-ACK reads freed memory",state="red")],
  note="Fix: free the options with kfree_rcu(), so readers on other CPUs finish first.",step_h=108)
checklist(IMG+"linux-tcp-cve-2026-98432-steps.svg",[
  ("Install the fixed kernel","Ubuntu 26.04: 7.0.0-43.43 · 24.04: 6.8.0-149.149 · 22.04: 5.15.0-203.213","green"),
  ("Reboot (or livepatch)","the old kernel keeps running until you do","red"),
  ("Check the running kernel","$ uname -r","blue"),
  ("Can't reboot yet?","nftables rule dropping IPv4 TCP with IP options reduces the risk","yellow")],title="Patching is three steps, not one",sub="unattended-upgrades installs the kernel but won't reboot for you")
header_md("linux-kernel-tcp-rce","linux-tcp-cve-2026-98432-header.svg","Linux kernel TCP use-after-free: a SYN with IPv4 options, a retransmitted SYN and the options freed underneath it")
insert_before("linux-kernel-tcp-rce","The root cause goes back","linux-tcp-cve-2026-98432-race.svg","The race: options from a SYN are stored, the handshake completes and the child socket takes the pointer, a retransmitted SYN builds a SYN-ACK on another CPU while the child is destroyed and the options freed, so the SYN-ACK reads freed memory")
insert_before("linux-kernel-tcp-rce","## How to patch","linux-tcp-cve-2026-98432-steps.svg","Patching: install the fixed kernel, reboot or livepatch, check uname -r; if you can't reboot yet, an nftables rule dropping IPv4 TCP with IP options reduces risk")

# asahi
m=[logo("asahilinux",590,96,110),link(714,150,770,150)]
m+=[box(780,86,180,52,"panel","line",rx=10)+T(870,119,"MIT",20,"dim",bold=True,mono=True,anchor="middle"),f'<line x1="830" y1="112" x2="910" y2="112" stroke="{C["red"]}" stroke-width="3"/>']
m+=[box(780,166,180,52,TINT["green"],"green",rx=10,sw=2)+T(870,199,"GPL-2.0+",20,"green",bold=True,mono=True,anchor="middle")]
header(IMG+"asahi-mit-to-gpl-header.svg","Asahi Linux · licensing",["Asahi Linux goes","MIT → GPL"],"After code was copied and LLM-rewritten to hide where it came from",accent="purple",motif=m)
flow(IMG+"asahi-mit-to-gpl-what-happened.svg","What Asahi says happened",[
  dict(t="In-development code",d="personal forks"),dict(t="Lifted or LLM-rewritten",d="origin hidden",state="yellow"),dict(t="Published, no attribution",d="by would-be rivals",state="red"),dict(t="Aim: replace and monetise",state="red")],
  note="MIT allows all of this. The GPL doesn't stop copying, but it forbids closed forks and gives Asahi something to enforce.",step_h=100)
compare(IMG+"asahi-mit-to-gpl-limits.svg",
  dict(kicker="what the gpl fixes",title="Going forward",items=["Forks that ship must share their source","No proprietary products built on it","A licence the project can enforce"],state="green"),
  dict(kicker="what it can't fix",title="The past, and LLMs",items=["Code already released under MIT stays MIT","An LLM rewrite is hard to prove as copying","Copying itself is still allowed"],state="red"),title="Can a licence change stop this?")
header_md("asahi-linux-mit-to-gpl","asahi-mit-to-gpl-header.svg","Asahi Linux moves its code from the MIT licence to GPL-2.0-or-later")
insert_before("asahi-linux-mit-to-gpl","### Why this hurts Asahi","asahi-mit-to-gpl-what-happened.svg","What Asahi says happened: in-development code from personal forks was lifted or rewritten with an LLM, published without attribution, with the aim of replacing and monetising the project")
insert_before("asahi-linux-mit-to-gpl","### The bigger picture","asahi-mit-to-gpl-limits.svg","The GPL forces shipped forks to share source, bans proprietary products and is enforceable; it can't relicense code already released under MIT, and LLM rewrites are hard to prove")

# HA marketplace
m=[logo("homeassistant",590,100,100),T(640,240,"2026.11",16,"muted",mono=True,anchor="middle"),link(706,150,760,150)]
m+=[box(770,86,190,52,"panel","line",rx=10)+T(865,119,"HACS",19,"dim",bold=True,mono=True,anchor="middle"),f'<line x1="828" y1="112" x2="902" y2="112" stroke="{C["dim"]}" stroke-width="3"/>']
m+=[box(770,166,190,52,TINT["blue"],"blue",rx=10,sw=2)+icon("store",786,178,28,"blue")+T(824,199,"Marketplace",17,"blue",bold=True)]
header(IMG+"ha-marketplace-2026-11-header.svg","Home Assistant · 2026.11",["HACS becomes","the Marketplace"],"What the automatic migration keeps, and what stops updating",chip="Settings › Marketplace",accent="blue",motif=m)
cards(IMG+"ha-marketplace-2026-11-migration.svg",[
  dict(name="Integrations, cards, themes",icon="package",accent="green",desc="Stay installed and keep getting updates",tag="updated",tag_color="green"),
  dict(name="Custom repositories",icon="git",accent="green",desc="Carry over if they have a hacs.json",tag="updated",tag_color="green"),
  dict(name="Repos without hacs.json",icon="warning",accent="yellow",color="yellow",desc="Stay installed, but the Marketplace can't update them",tag="frozen",tag_color="yellow"),
  dict(name="AppDaemon, Python scripts",icon="code",accent="red",desc="Stay where they are, no more updates",tag="frozen",tag_color="red"),
 ],cols=2,title="What the migration does to your HACS stuff")
checklist(IMG+"ha-marketplace-2026-11-checklist.svg",[
  ("Full backup","Settings › System › Backups: restoring is the only rollback","red"),
  ("Update everything in HACS first","while it's still HACS","blue"),
  ("Check custom repos for hacs.json","no file means no updates after migration","yellow"),
  ("Integrations ready for 2026.11","big release with breaking changes","blue"),
  ("Anything calling HACS directly","integration_entities('hacs') → 'marketplace'","blue")],title="Before you update",cols=1)
header_md("home-assistant-2026-11-hacs","ha-marketplace-2026-11-header.svg","Home Assistant 2026.11 replaces HACS with the built-in Marketplace")
insert_before("home-assistant-2026-11-hacs","## Before you update","ha-marketplace-2026-11-migration.svg","Migration: integrations, cards, themes and custom repos with hacs.json keep updating; repos without hacs.json and AppDaemon or Python scripts stay installed but stop updating")
insert_after("home-assistant-2026-11-hacs","## Before you update: a checklist","ha-marketplace-2026-11-checklist.svg","Before updating: full backup, update everything in HACS, check custom repos for hacs.json, check integrations support 2026.11, fix anything calling HACS directly")

# codeberg
m=[logo("codeberg",590,96,100),T(640,240,"codeberg.org",15,"muted",mono=True,anchor="middle"),link(704,150,770,150)]
m+=[box(780,96,180,70,TINT["red"],"red",rx=10,sw=2)+T(870,128,"clientHold",19,"red",bold=True,mono=True,anchor="middle")+T(870,152,"05:52 → 11:02 UTC",13,"muted",mono=True,anchor="middle")]
m+=[T(870,214,"NXDOMAIN",17,"red",mono=True,anchor="middle"),T(870,240,"web · git · CI · registry",13,"dim",mono=True,anchor="middle")]
header(IMG+"codeberg-clienthold-header.svg","Domains · registrars",["Codeberg vanished","for five hours"],"NameSilo put codeberg.org on clientHold without warning",chip="check your domain status, not just uptime",accent="red",motif=m)
timeline(IMG+"codeberg-clienthold-timeline.svg",[("05:52","registry record set to clientHold","red"),("07:20","users report it doesn't resolve","orange"),("08:07","incident opened on codeberg.eu","yellow"),("11:02","hold removed (RDAP)","green"),("11:23","“slowly recovering”","green")],title="November 18, 2026 (UTC)")
flow(IMG+"codeberg-clienthold-flow.svg","What clientHold does",[
  dict(t="Registrar sets clientHold",d="NameSilo",state="red"),dict(t="Registry drops it from the .org zone"),dict(t="Name stops resolving",d="NXDOMAIN"),dict(t="Everything breaks",d="web, git, CI, packages",state="red")],
  note="The servers kept running the whole time. Nobody could find them.",step_h=100)
checklist(IMG+"codeberg-clienthold-lessons.svg",[
  ("Monitor domain status","RDAP shows clientHold; uptime checks don't"),("Keep the registrar account boring","contact email off the domain, 2FA, auto-renew"),
  ("Pick a registrar with a human process","for domains you can't lose"),("Spread risk where it's cheap","status page and alerts on another domain"),
  ("Mirror the forge","push to a second remote"),("Careful with IPs shared in an outage","only published addresses, never skip cert warnings","yellow")],title="What to do about it",cols=2)
header_md("codeberg-domain-suspended","codeberg-clienthold-header.svg","codeberg.org put on clientHold by its registrar NameSilo from 05:52 to 11:02 UTC, so it stopped resolving")
insert_after("codeberg-domain-suspended","| 11:23 |","codeberg-clienthold-timeline.svg","Timeline on November 18: clientHold set at 05:52 UTC, users report failures at 07:20, incident opened on codeberg.eu at 08:07, hold removed at 11:02, recovery announced at 11:23")
insert_before("codeberg-domain-suspended","### What broke","codeberg-clienthold-flow.svg","clientHold: the registrar sets the status, the registry drops the domain from the .org zone, the name stops resolving, and the website, Git, CI and package registry break although the servers keep running")
insert_before("codeberg-domain-suspended","### 1. Monitor your domain","codeberg-clienthold-lessons.svg","Six lessons: monitor domain status, keep the registrar account verified, use a registrar with a human process, spread risk across domains, mirror your forge, don't trust random IPs during an outage")
