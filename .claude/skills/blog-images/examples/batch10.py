import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "postedit.py")).read())

# free static hosting
m=[icon("globe",580,90,130,"muted","blue"),T(645,258,"example.com",15,"yellow",mono=True,anchor="middle")]
m+=fan(720,155,["github","cloudflare","codeberg","gitlab"],x=860,size=36,step=66)
header(IMG+"free-hosting-custom-domain-header.svg","Static sites · hosting",["Free static hosting,","your own domain"],"GitHub Pages, Cloudflare, Codeberg, GitLab, Netlify and Vercel compared",chip="only the domain costs money: ~$10–15/yr",accent="blue",motif=m)
cards(IMG+"free-hosting-custom-domain-pick.svg",[
  dict(name="GitHub Pages",logo="github",desc="Simple, Jekyll built in; public repo on free plan",tag="default",tag_color="green"),
  dict(name="Cloudflare",logo="cloudflare",desc="Unlimited static traffic; apex needs Cloudflare DNS",tag="generous",tag_color="green"),
  dict(name="Codeberg Pages",logo="codeberg",desc="EU non-profit, no big tech",tag="non-profit",tag_color="blue"),
  dict(name="GitLab Pages",logo="gitlab",desc="Solid; 1 GB site size limit"),
  dict(name="Netlify",logo="netlify",desc="Credit-based now; site stops at the cap",tag="watch",tag_color="yellow"),
  dict(name="Vercel Hobby",logo="vercel",desc="Personal, non-commercial use only",tag="no commercial",tag_color="red"),
 ],title="Which one to pick")
flow(IMG+"free-hosting-custom-domain-dns.svg","Putting your domain on a free host",[
  dict(t="Verify the domain",d="TXT record"),dict(t="Add it in the host",d="Settings › Pages"),dict(t="Point DNS at it",d="A/AAAA apex, CNAME www",state="blue"),dict(t="HTTPS issued",d="automatically",state="green")],
  note="Verifying first stops anyone else from claiming your domain if the site is ever deleted.")
header_md("free-static-site-hosting","free-hosting-custom-domain-header.svg","Free static hosting with your own domain: example.com pointed at GitHub Pages, Cloudflare, Codeberg or GitLab")
insert_before("free-static-site-hosting","## What \"static\" means","free-hosting-custom-domain-pick.svg","GitHub Pages is the default, Cloudflare the most generous, Codeberg Pages the non-profit option, GitLab Pages solid, Netlify credit-capped and Vercel Hobby non-commercial only")
insert_before("free-static-site-hosting","For an **apex** domain","free-hosting-custom-domain-dns.svg","Custom domain steps: verify with a TXT record, add the domain in the host's settings, point A/AAAA records for the apex and a CNAME for www, HTTPS is issued automatically")

# free dns filtering
m=[icon("laptop",580,110,110,"muted"),link(700,165,750,165)]
m+=[box(760,80,200,48,TINT["green"],"green",rx=10)+T(778,110,"example.com",15,"green",mono=True)]
m+=[box(760,142,200,48,TINT["red"],"red",rx=10)+T(778,172,"doubleclick.net",15,"red",mono=True)]
m+=[T(860,224,"→ 0.0.0.0",17,"red",mono=True,bold=True,anchor="middle")]
header(IMG+"free-dns-filtering-header.svg","Networking · DNS",["Free DNS that","blocks ads"],"AdGuard DNS, Control D, NextDNS, DNS4EU, Quad9 and more",chip="94.140.14.14",accent="green",motif=m)
flow(IMG+"free-dns-filtering-how.svg","How DNS filtering works",[
  dict(t="App asks for a name",d="ads.tracker.net"),dict(t="Filtering resolver",d="checks blocklist",state="blue"),dict(t="On the list",d="0.0.0.0",state="red"),dict(t="Ad never loads",state="green")],
  note="Names that aren't on the list get their real address, so everything else works as usual.")
cards(IMG+"free-dns-filtering-pick.svg",[
  dict(name="AdGuard DNS",logo="adguard",desc="Block ads, no account: 94.140.14.14",tag="easiest",tag_color="green"),
  dict(name="Control D free",icon="gear",accent="blue",desc="Separate resolvers for ads, social, family"),
  dict(name="NextDNS",logo="nextdns",desc="Your own lists and logs, 300k queries/month"),
  dict(name="DNS4EU",icon="globe",accent="blue",desc="EU-run “no ads” profile: 86.54.11.13"),
  dict(name="Quad9",logo="quad9",desc="Malware only, no ad blocking; not in France",tag="no ads",tag_color="yellow"),
  dict(name="AdGuard Home / Pi-hole",logo="pihole",desc="Self-host for full control at home",tag="self-host",tag_color="blue"),
 ],title="Which one to pick")
header_md("free-dns-ad-blocking","free-dns-filtering-header.svg","Free filtering DNS: example.com resolves normally while doubleclick.net gets 0.0.0.0")
insert_before("free-dns-ad-blocking","## How DNS filtering works","free-dns-filtering-pick.svg","Pick AdGuard DNS for no-account ad blocking, Control D for separate resolvers, NextDNS for custom lists, DNS4EU for EU-run, Quad9 for malware only, AdGuard Home or Pi-hole to self-host")
insert_before("free-dns-ad-blocking","## The comparison","free-dns-filtering-how.svg","An app asks for ads.tracker.net, the filtering resolver checks its blocklist, answers 0.0.0.0, and the ad never loads")

# adguard home 1.0
m=[logo("adguard",590,100,100),T(640,246,"0.107.80",15,"dim",mono=True,anchor="middle"),link(706,150,770,150)]
m+=[box(780,104,180,92,TINT["green"],"green",rx=12,sw=2),T(870,148,"1.0.0",30,"green",bold=True,mono=True,anchor="middle"),T(870,178,"schema 35",14,"muted",mono=True,anchor="middle")]
header(IMG+"adguard-home-1-0-header.svg","AdGuard Home · upgrade",["AdGuard Home 1.0","upgrade guide"],"New UI, Quad9 default dropped, removed APIs and flags",chip="cp AdGuardHome.yaml AdGuardHome.yaml.bak",accent="green",motif=m)
compare(IMG+"adguard-home-1-0-upstream.svg",
  dict(kicker="0.107.x default",title="Quad9",items=["https://dns10.quad9.net/dns-query","Bootstrap 9.9.9.10, 149.112.112.10","Stopped serving France on 24 Nov"],state="red",mark="•"),
  dict(kicker="1.0 default",title="Cloudflare",items=["https://cloudflare-dns.com/dns-query","Bootstrap 1.1.1.1, 1.0.0.1","Only for new installs: upgrades keep your setting"],state="green",mark="•"),title="The new default upstream")
cards(IMG+"adguard-home-1-0-should-i.svg",[
  dict(name="Default home setup",icon="check",accent="green",desc="Upgrade: copy the config and go",tag="go",tag_color="green"),
  dict(name="Advanced features",icon="warning",color="yellow",desc="Per-client services, access lists, DNSCrypt or self-rewrites: wait for 1.0.1",tag="wait",tag_color="yellow"),
  dict(name="Screen reader",icon="user",accent="yellow",desc="Stay on 0.107.80 for now",tag="wait",tag_color="yellow"),
  dict(name="Home Assistant app",logo="homeassistant",desc="Wait for the add-on update",tag="wait",tag_color="yellow"),
 ],cols=2,title="Should you upgrade now?")
header_md("adguard-home-1-0-upgrade","adguard-home-1-0-header.svg","AdGuard Home upgrade from 0.107.80 to 1.0.0 with config schema 35")
insert_after("adguard-home-1-0-upgrade","| Bootstrap (IPv6) |","adguard-home-1-0-upstream.svg","The old default upstream was Quad9, which stopped serving France on 24 November; the 1.0 default is Cloudflare DNS, but upgrades keep your existing setting")
insert_after("adguard-home-1-0-upgrade","## Should you upgrade now?","adguard-home-1-0-should-i.svg","Upgrade now on a default home setup; wait for 1.0.1 if you use per-client blocked services, access lists, DNSCrypt or self-rewrites; stay on 0.107.80 with a screen reader; wait for the Home Assistant app update")
