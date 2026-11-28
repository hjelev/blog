import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "postedit.py")).read())

# nginx2root
m=[logo("nginx",590,96,104),T(642,250,"5 CVEs",17,"red",bold=True,mono=True,anchor="middle"),link(708,148,770,148)]
m+=[box(780,84,180,52,TINT["red"],"red",rx=10)+T(870,116,"reload",18,"red",mono=True,bold=True,anchor="middle")]
m+=[box(780,160,180,52,TINT["green"],"green",rx=10,sw=2)+T(870,192,"restart",18,"green",mono=True,bold=True,anchor="middle")]
m+=[T(870,246,"1.30.8 / 1.31.10",14,"muted",mono=True,anchor="middle")]
header(IMG+"nginx2root-header.svg","nginx · NGINX2Root",["NGINX2Root:","update, then restart"],"Five nginx bugs, fixed versions per distro, and the traps",chip="systemctl restart nginx",accent="green",chip_color="green",motif=m)
compare(IMG+"nginx2root-reload.svg",
  dict(kicker="nginx -s reload",title="Old binary keeps running",items=["Re-reads the config only","The master process is the pre-update binary","/proc/<pid>/exe shows (deleted)"],state="red"),
  dict(kicker="systemctl restart nginx",title="New binary loaded",items=["Process stopped and started again","Runs the patched nginx","No (deleted) in /proc/<pid>/exe"],state="green"),title="Restart, don't reload")
checklist(IMG+"nginx2root-order.svg",[
  ("List every nginx","host packages, containers, proxies","blue"),("Update and restart","then check for (deleted)","green"),
  ("Recreate containers","with fixed images (NPM 2.17.1+)","green"),("Turn off HTTP/2 where no fix exists","HA NPM app, ingress-nginx, nginx-proxy","yellow"),
  ("Block SCTP on every host","one modprobe line","red")],title="What to do, in order",cols=1)
header_md("nginx2root","nginx2root-header.svg","NGINX2Root: five nginx bugs fixed in 1.30.8 and 1.31.10, and a restart rather than a reload is needed")
insert_before("nginx2root","## Block SCTP on the host","nginx2root-reload.svg","nginx -s reload only re-reads the config and keeps the old, deleted binary running; systemctl restart loads the patched nginx")
insert_after("nginx2root","## What to do, in order","nginx2root-order.svg","In order: list every nginx, update and restart, recreate containers, turn off HTTP/2 where no fix exists, block SCTP on every host")

# trending tui
m=[]
top=[("OpenCode",3114,"blue"),("Herdr",2716,"blue"),("Claude Code",1747,"orange"),("Codex",1648,"blue")]
for i,(n,v,c) in enumerate(top):
    y=74+i*56
    m+=[T(580,y+22,n,15,"text",mono=True),box(700,y+4,v*0.07,26,c,None,rx=5),T(700+v*0.07+10,y+23,f"+{v:,}",14,c,bold=True,mono=True)]
header(IMG+"trending-tui-header.svg","CLI · trending",["Trending TUI tools,","November 2026"],"Stars gained 10–24 November: AI agents take the top four",accent="blue",motif=m)
bars(IMG+"trending-tui-stars.svg",[("1 OpenCode",3114,"blue"),("2 Herdr",2716,"blue"),("3 Claude Code",1747,"blue"),("4 Codex",1648,"blue"),("5 Mole",881,"dim"),("6 Atuin",340,"green"),("7 Yazi",298,"green"),("8 dnsglobe",283,"yellow"),("9 Neovim",268,"green"),("10= fzf",264,"green"),("10= lazygit",264,"green")],
  title="GitHub stars gained, 10–24 November",sub="AI coding agents in blue; Mole's count covers only 8 days",fmt=lambda v:f"+{v:,}",label_w=180)
bars(IMG+"trending-tui-growth.svg",[("dnsglobe",20.3,"yellow"),("Herdr",5.4,"blue"),("OpenCode",1.4,"blue"),("Codex",1.2,"blue"),("Claude Code",1.1,"blue"),("Atuin",1.1,"green"),("Yazi",0.7,"green"),("Neovim",0.3,"green")],
  title="Growth relative to size",sub="stars gained as a share of total stars",unit="%",label_w=180,max_v=22)
header_md("trending-tui-tools","trending-tui-header.svg","Trending TUI tools: OpenCode, Herdr, Claude Code and Codex gained the most GitHub stars from 10 to 24 November")
insert_after("trending-tui-tools","| 10= | [lazygit]","trending-tui-stars.svg","Stars gained 10 to 24 November: OpenCode 3,114, Herdr 2,716, Claude Code 1,747, Codex 1,648, Mole about 881, then Atuin, Yazi, dnsglobe, Neovim, fzf and lazygit between 340 and 264")
insert_before("trending-tui-tools","## 1. OpenCode","trending-tui-growth.svg","Growth as a share of total stars: dnsglobe 20.3%, Herdr 5.4%, the other tools between 0.3% and 1.4%")

# rpi kernel cve
m=[logo("raspberrypi",590,96,100)]
for i,(t,c,s) in enumerate((("trixie 6.18.60","green","fixed"),("bookworm 6.12.115","green","fixed"),("bullseye 6.1.21","red","no fix"),("buster 5.10.103","red","no fix"))):
    y=70+i*56
    m+=[box(720,y,240,44,TINT[c],c,rx=8,sw=1.5),T(736,y+28,t,14,"text",mono=True),T(946,y+28,s,13,c,mono=True,bold=True,anchor="end")]
header(IMG+"rpi-kernel-cve-2026-98432-header.svg","Raspberry Pi OS · CVE-2026-98432",["Your Pi's kernel","may never be fixed"],"Fixed kernels for trixie and bookworm; nothing for older releases",chip="sudo apt full-upgrade && sudo reboot",accent="red",chip_color="green",motif=m)
flow(IMG+"rpi-kernel-cve-2026-98432-traps.svg","Three ways to stay vulnerable after “updating”",[
  dict(t="apt update",d="stale lists = no new kernel",state="yellow"),dict(t="apt full-upgrade",d="apt-get upgrade holds it back",state="yellow"),dict(t="Reboot",d="old kernel runs until then",state="yellow"),dict(t="uname -r",d="6.18.56+ / 6.12.113+",state="green")],
  note="Each yellow box is a trap from the post: skip it and the Pi stays on the vulnerable kernel.",step_h=104)
decision(IMG+"rpi-kernel-cve-2026-98432-which.svg","Is the Pi on trixie or bookworm?",("Patch now","apt update, apt full-upgrade, reboot, check uname -r"),("No fix will come","Add the nftables rule, remove port forwards, plan a trixie reinstall"),yes_label="yes",no_label="bullseye / buster",title="What to do with each Pi")
header_md("raspberry-pi-kernel-cve","rpi-kernel-cve-2026-98432-header.svg","Raspberry Pi OS kernels and CVE-2026-98432: trixie and bookworm fixed, bullseye and buster left vulnerable")
insert_before("raspberry-pi-kernel-cve","### Trap 1","rpi-kernel-cve-2026-98432-traps.svg","Run apt update so the lists are fresh, use apt full-upgrade because apt-get upgrade holds the kernel back, reboot, then check uname -r shows 6.18.56+ or 6.12.113+")
insert_after("raspberry-pi-kernel-cve","## What to do, in order","rpi-kernel-cve-2026-98432-which.svg","Trixie or bookworm: apt update, full-upgrade, reboot and check uname -r. Bullseye or buster: no fix will come, so add the nftables rule, remove port forwards and plan a trixie reinstall")

# shirudo
m=[icon("shield",590,80,140,"muted","blue"),logo("linux",630,120,60,"text")]
m+=[box(760,80,200,46,"panel2","line",rx=8)+T(778,109,"upatch (signed)",15,"blue",mono=True)]
m+=[box(760,142,200,46,TINT["green"],"green",rx=8,sw=2)+T(778,171,"bug path blocked",15,"green",mono=True)]
m+=[box(760,204,200,46,TINT["red"],"red",rx=8,sw=2)+T(778,233,"other eBPF refused",15,"red",mono=True)]
m+=[link(736,150,752,103,"line",3)]
header(IMG+"shirudo-header.svg","eBPF · Isovalent / Cisco",["Shirudo: eBPF","shields for bugs"],"Signed upatches block an exploit until you can patch; pre-release",chip="FAQ: production-ready? “Not yet.”",accent="blue",chip_color="orange",motif=m)
flow(IMG+"shirudo-how.svg","How it works",[
  dict(t="Operator signs upatch",d="ML-DSA-87 key"),dict(t="Pushed to OCI registry"),dict(t="Target pulls on a timer",d="no daemon, no port"),dict(t="Kernel checks signature",d="sealed .bpf keyring",state="blue"),dict(t="TPM records the load",d="shirudo attest",state="green")],step_h=104)
cards(IMG+"shirudo-breaks.svg",[
  dict(name="Tracing",icon="search",accent="red",desc="bpftrace, bcc, anything on libbpf"),
  dict(name="Networking",icon="globe",accent="red",desc="Cilium datapath, XDP and tc programs"),
  dict(name="Security agents",icon="shield",accent="red",desc="Tetragon, Falco's eBPF driver"),
  dict(name="systemd sandboxing",icon="gear",color="yellow",desc="IPAddressDeny= and friends silently stop applying",border="yellow"),
  dict(name="Container devices",icon="package",accent="red",desc="Docker/Podman cgroup v2 device rules"),
  dict(name="Boot tricks",icon="power",accent="red",desc="kexec, kdump, hibernation, soft reboot"),
 ],title="What stops working",sub="every BPF load that isn't a signed upatch is refused, even from root")
header_md("shirudo-ebpf","shirudo-header.svg","Shirudo: a signed upatch blocks a bug's code path while all other eBPF is refused")
insert_before("shirudo-ebpf","The AI part is about","shirudo-how.svg","The operator signs a upatch with an ML-DSA-87 key and pushes it to an OCI registry; targets pull on a timer, the kernel checks the signature against a sealed keyring and the TPM records each load")
insert_after("shirudo-ebpf","This is the part the announcements leave out.","shirudo-breaks.svg","Shirudo refuses all other BPF: bpftrace and bcc, Cilium, XDP and tc, Tetragon and Falco's eBPF driver, systemd sandboxing settings, container device rules, and kexec, kdump and hibernation")

# reddit rss
m=[logo("reddit",590,96,100),link(704,150,760,150)]
m+=[box(770,90,190,62,TINT["red"],"red",rx=10,sw=2)+logo("rss",788,106,30,"red")+T(830,128,"404",24,"red",bold=True,mono=True)]
m+=[T(865,190,"empty Atom feed",14,"muted",mono=True,anchor="middle"),T(865,214,"/r/selfhosted/.rss",14,"dim",mono=True,anchor="middle")]
header(IMG+"reddit-rss-shutdown-header.svg","RSS · Reddit",["Reddit's RSS","feeds are gone"],"What the old URLs return now, and where to follow instead",chip="grep reddit.com feeds.opml",accent="orange",motif=m)
cards(IMG+"reddit-rss-shutdown-options.svg",[
  dict(name="RSS-Bridge",icon="rss",accent="orange",desc="With your own Reddit API app. Short-term: likely breaks with the 2027 API changes",tag="short-term",tag_color="yellow"),
  dict(name="Redlib",icon="globe",accent="blue",desc="Privacy front end for Reddit; RSS is off by default (ENABLE_RSS)",tag="option 2",tag_color="blue"),
  dict(name="Follow elsewhere",icon="users",accent="green",desc="Lemmy, Hacker News and newsletters still publish feeds",tag="long-term",tag_color="green"),
 ],title="Your options")
flow(IMG+"reddit-rss-shutdown-silent.svg","Why you might not notice",[
  dict(t="Reader fetches .rss",d="as usual"),dict(t="Reddit answers 404",d="+ empty Atom feed",state="red"),dict(t="Some readers see a valid feed",d="no error shown",state="yellow"),dict(t="Feed just goes quiet",dashed=True)],
  note="Export OPML and grep for reddit.com to find every dead feed.")
header_md("reddit-rss-feeds","reddit-rss-shutdown-header.svg","Reddit RSS is gone: /r/selfhosted/.rss now returns 404 with an empty Atom feed")
insert_before("reddit-rss-feeds","## Find the dead feeds","reddit-rss-shutdown-silent.svg","The reader fetches the .rss URL, Reddit answers 404 with an empty Atom feed, some readers treat it as valid, so the feed just goes quiet")
insert_before("reddit-rss-feeds","## Option 1","reddit-rss-shutdown-options.svg","Options: RSS-Bridge with your own Reddit API app as a short-term fix, Redlib's built-in RSS, or following the same topics on Lemmy, Hacker News and newsletters")
