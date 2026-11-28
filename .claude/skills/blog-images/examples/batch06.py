import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "postedit.py")).read())

# ---- Let's Encrypt 64 days
m=[logo("letsencrypt",590,70,56)]
for i,(lab,d,c) in enumerate((("today",90,"muted"),("Feb 2027",64,"yellow"),("2028",45,"red"))):
    y=150+i*52
    m+=[T(590,y+20,lab,14,c,mono=True),box(680,y,d*2.7,28,c,None,rx=6),T(680+d*2.7+10,y+20,f"{d}d",16,c,bold=True,mono=True)]
header(IMG+"le-64-day-header.svg","Let's Encrypt · certificates",["Certificates drop","to 64 days"],"Shorter lifetimes from Feb 2027: automate renewal or break",chip="certbot >= 4.1 with ARI",accent="yellow",motif=m)
body=T(40,52,"When does your renewal actually fire?",22,bold=True)+T(40,80,"64-day certificates unless noted; the bar is the certificate's life",15,"muted")
x0,x1=330,930; sc=(x1-x0)/90
for d in (0,30,60,90):
    xx=x0+d*sc; body+=f'<line x1="{xx:g}" y1="110" x2="{xx:g}" y2="372" stroke="{C["line"]}" stroke-dasharray="3 5"/>'+T(xx,394,f"{d}" if d<90 else "90 days",13,"dim",mono=True,anchor="middle")
rows=[("ARI, 64-day",64,43,"green","✓ renews ~day 43"),("certbot default",64,34,"green","✓ 30 days left"),("fixed “every 60d”",64,60,"yellow","⚠ 4 days of margin"),("same, 45-day cert",45,60,"red","✗ expired 15 days")]
for i,(lab,life,ren,c,note) in enumerate(rows):
    y=126+i*62
    body+=T(40,y+20,lab,16,"text",bold=True)+T(40,y+42,note,14,c)
    body+=box(x0,y+6,life*sc,22,"panel2","line",rx=5)
    body+=f'<line x1="{x0+life*sc:g}" y1="{y}" x2="{x0+life*sc:g}" y2="{y+34}" stroke="{C["red"]}" stroke-width="3"/>'
    body+=f'<circle cx="{x0+ren*sc:g}" cy="{y+17}" r="9" fill="{col(c)}"/>'
body+=f'<circle cx="48" cy="419" r="7" fill="{C["green"]}"/>'+T(62,424,"renewal attempt",14,"muted")+f'<rect x="200" y="410" width="3" height="18" fill="{C["red"]}"/>'+T(214,424,"certificate expiry",14,"muted")
raw(IMG+"le-64-day-renewal.svg",444,body)
checklist(IMG+"le-64-day-checklist.svg",[
  ("Client supports ARI","certbot ≥ 4.1 · acme.sh ≥ 3.1.4","green"),("Renewal runs at least daily","$ systemctl list-timers","green"),
  ("No hard-coded 60 / 80 / 83 days","grep your scripts and cron jobs","green"),("Services reload after renewal","deploy hooks","green"),
  ("Tested against staging","$ certbot renew --dry-run","green"),("Alert before it expires","$ openssl x509 -checkend","yellow")],title="64-day readiness check",cols=2)
header_md("lets-encrypt-64-day","le-64-day-header.svg","Let's Encrypt certificate lifetimes: 90 days today, 64 days from February 2027, 45 days in 2028")
replace_img("lets-encrypt-64-day","/static/img/le-64-day-renewal.svg","le-64-day-renewal.svg","When renewals fire on a 64-day certificate: ARI renews around day 43, certbot's default at 30 days left, a fixed every-60-days job leaves 4 days of margin, and the same job on a 45-day certificate lets it expire")
replace_img("lets-encrypt-64-day","/static/img/le-64-day-checklist.svg","le-64-day-checklist.svg","64-day readiness checklist: ARI-capable client, daily renewal, no hard-coded day counts, services reload, staging dry run, and an expiry alert")

# ---- OpenCode vs Claude Code
m=[box(580,70,170,200,"panel","line",rx=12),box(800,70,170,200,"panel","line",rx=12)]
m+=[T(665,130,"opencode",22,"text",bold=True,mono=True,anchor="middle"),T(665,160,"open source",14,"muted",anchor="middle"),T(665,182,"any model",14,"muted",anchor="middle"),icon("code",640,204,50,"blue")]
m+=[logo("claude",855,96,60),T(885,190,"Claude Code",18,"text",bold=True,anchor="middle"),T(885,214,"Anthropic",14,"muted",anchor="middle"),T(885,236,"Claude models",14,"muted",anchor="middle")]
m+=[T(775,178,"vs",20,"yellow",bold=True,anchor="middle")]
header(IMG+"opencode-vs-claude-code-header.svg","AI · coding agents",["OpenCode vs","Claude Code"],"Open source and model-agnostic, or built around Claude",accent="orange",motif=m)
terminal(IMG+"claude-code-session.svg",[
  ("text","[[orange|>]] The tag page 404s on mobile. Find out why and fix it."),("",""),
  ("text",'[[green|●]] **Search**[[muted|(pattern: "tags", path: "_layouts")]]'),("dim","  ⎿  Found 3 files"),
  ("text","[[green|●]] **Read**[[muted|(_includes/nav.html)]]"),("dim","  ⎿  Read 48 lines"),
  ("text","[[text|●]] The mobile menu links to /tags but the page lives at /categories/."),
  ("text","[[green|●]] **Update**[[muted|(_includes/nav.html)]]"),
  ("err",'  - <a href="/tags">Tags</a>'),("okb",'  + <a href="/categories/">Tags</a>'),
  ("text","[[green|●]] **Bash**[[muted|(bundle exec jekyll build)]]"),("dim","  ⎿  done in 1.9 seconds."),
  ("dim","⏵⏵ accept edits on (shift+tab to cycle)")],win="~/git/blog — claude",size=15)
body=""
for i,(name,surf,sub,provs,foot,c) in enumerate((
  ("OpenCode","TUI · Desktop · IDE","client / server",[("Anthropic","anthropic"),("OpenAI","openai"),("Google · others",None),("Ollama (local)",None)],"Bring your own key, or use OpenCode's pay-as-you-go model gateway","blue"),
  ("Claude Code","CLI · IDE · Desktop · Web · Mobile","one engine, many surfaces",[("Claude subscription","claude"),("API · Bedrock · Vertex",None)],"Claude models only (Opus, Sonnet, Haiku), tuned end to end for them","orange"))):
    x=40+i*480
    body+=box(x,30,440,400,"panel","line",rx=12)+f'<rect x="{x}" y="30" width="440" height="6" rx="3" fill="{col(c)}"/>'
    body+=T(x+28,78,name,22,bold=True)+T(x+28,104,surf,14,"muted",mono=True)
    body+=box(x+28,124,384,50,TINT[c],c,sw=2)+T(x+220,155,sub,15,c,anchor="middle",mono=True)
    for j,(p,lg) in enumerate(provs):
        yy=226+j*40
        body+=arrow(x+220,174,x+60,yy-6,"line",head=False) if False else ""
        body+=box(x+28,yy-22,384,32,"panel2","line",rx=8)+(logo(lg,x+42,yy-16,20,"text" if lg!="claude" else None) if lg else f'<circle cx="{x+52}" cy="{yy-6}" r="6" fill="{C["dim"]}"/>')+T(x+76,yy,p,15,"text")
    ft,_=TL(x+28,384,foot,380,14,fill="muted")
    body+=ft

raw(IMG+"opencode-vs-claude-code-models.svg",460,body)
header_md("opencode-vs-claude-code","opencode-vs-claude-code-header.svg","OpenCode, open source and model-agnostic, versus Claude Code, built by Anthropic for Claude models")
replace_img("opencode-vs-claude-code","/static/img/claude-code-session.svg","claude-code-session.svg","Claude Code session: asked why the tag page 404s on mobile, it searches the layouts, reads nav.html, fixes the link from /tags to /categories/ and rebuilds the site")
replace_img("opencode-vs-claude-code","/static/img/opencode-vs-claude-code-models.svg","opencode-vs-claude-code-models.svg","OpenCode connects to Anthropic, OpenAI, Google and local Ollama models with your own key or its gateway; Claude Code uses Claude models through a subscription, the API, Bedrock or Vertex")

# ---- Vibe vs spec
m=[box(580,62,190,236,"panel","line",rx=12),box(800,62,170,236,"panel","line",rx=12),T(785,186,"vs",18,"yellow",bold=True,anchor="middle")]
for j,(t,me) in enumerate((("make it look cooler ✨",True),("done! changed 14 files",False),("now it's broken, fix",True),("fixed! changed 9 files",False))):
    y=82+j*52; xx=596 if me else 606
    m+=[box(xx,y,158,38,TINT["orange"] if me else "panel2",None,rx=10),T(xx+10,y+24,t,12.5 if False else 13,"orange" if me else "muted")]
for j,(t,ok) in enumerate((("spec.md",1),("plan.md",1),("tasks.md",1),("implement",0))):
    y=86+j*52
    m+=[f'<circle cx="826" cy="{y+14}" r="13" fill="{TINT["blue"]}" stroke="{C["blue"]}" stroke-width="2"/>',T(826,y+19,str(j+1),14,"blue",bold=True,mono=True,anchor="middle"),T(850,y+19,t,15,"text",mono=True),T(952,y+19,"✓" if ok else "…",15,"green" if ok else "dim",anchor="end")]
header(IMG+"vibe-vs-spec-header.svg","AI · ways of working",["Vibe coding vs","spec-driven"],"Two ways to work with AI coding agents, and when each fits",accent="blue",motif=m)
body=T(40,52,"Vibe coding",22,bold=True)+T(40,80,"one tight loop: prompt, look, react",15,"muted")
xs=[40,270,500,730]; labs=[("Idea / prompt",None),("AI writes code",None),("Run it, see what happens",None),("“Looks good” → ship","yellow")]
for x,(t,c) in zip(xs,labs):
    body+=box(x,108,200,64,TINT["orange"] if not c else TINT["yellow"],"orange" if not c else "yellow",rx=10,sw=1.5)
    ll=wrap(t,180,15,bold=True)
    for k,l in enumerate(ll): body+=T(x+100,145-(len(ll)-1)*10+k*20,l,15,bold=True,anchor="middle")
for a,b in zip(xs,xs[1:]): body+=arrow(a+204,140,b-6,140,"orange")
body+=arrow(600,172,140,176,"orange",curve=(600,240,140,240))+T(370,252,"“still broken, try again” / “now add…”",14,"orange",anchor="middle")
body+=f'<line x1="40" y1="282" x2="960" y2="282" stroke="{C["line"]}" stroke-width="2" stroke-dasharray="6 6"/>'
body+=T(40,326,"Spec-driven development",22,bold=True)+T(40,354,"intent is written down first; the spec is the source of truth",15,"muted")
steps=[("Specify","what & why"),("Plan","stack, design"),("Tasks","small, testable"),("Implement","AI writes code"),("Verify vs spec","tests, acceptance")]
for i,(t,d) in enumerate(steps):
    x=40+i*186
    last=i==4
    body+=box(x,382,160,66,TINT["green"] if last else TINT["blue"],"green" if last else "blue",rx=10,sw=1.5)+T(x+80,410,t,15,bold=True,anchor="middle")+T(x+80,432,d,13,"muted",anchor="middle")
    if i<4: body+=arrow(x+164,415,x+180,415,"blue")
body+=arrow(860,448,120,452,"dim",dash="5 4",curve=(860,510,120,510))+T(490,530,"requirements change? update the spec, then regenerate the plan and tasks",14,"muted",anchor="middle")
body+=T(40,566,"Human review gates sit between every step on the bottom row, not just at the end.",14,"yellow")
raw(IMG+"vibe-vs-spec-workflow.svg",590,body)
# quadrant
body=T(500,48,"When does each approach fit?",22,bold=True,anchor="middle")
X0,Y0,W,H=130,80,830,440
quad=[(X0,Y0,"Vibe it, but keep a safety net","yellow",["Hackathon demo for a client","Internal admin page"]),
      (X0+W/2,Y0,"Spec-driven sweet spot","blue",["Payment / auth / billing","Team project, many contributors","Long-lived service or API"]),
      (X0,Y0+H/2,"Vibe coding sweet spot","orange",["Weekend side project","Throwaway script / one-off tool","UI prototype to test an idea"]),
      (X0+W/2,Y0+H/2,"Light spec (a few bullet points)","green",["Personal tool you'll keep for years","Home-lab automation"])]
for x,y,t,c,items in quad:
    body+=box(x+4,y+4,W/2-8,H/2-8,TINT[c],c,rx=12,sw=1.5)+T(x+24,y+36,t,16,c,bold=True)
    for k,it in enumerate(items): body+=T(x+24,y+76+k*34,"• "+it,15,"text")
body+=arrow(X0,Y0+H+24,X0+W,Y0+H+24,"dim")+T(X0+W/2,Y0+H+50,"Lifespan & complexity of the code →",14,"muted",anchor="middle")
body+=arrow(X0-24,Y0+H,X0-24,Y0,"dim")+T(96,Y0+H/2,"Visibility / cost of a bug →",14,"muted",anchor="middle",extra=f'transform="rotate(-90 96 {Y0+H/2})"')
raw(IMG+"vibe-vs-spec-when.svg",590,body)
header_md("vibe-coding-vs-spec","vibe-vs-spec-header.svg","Vibe coding as a back-and-forth chat with the AI versus spec-driven development as numbered spec, plan, tasks and implement steps")
replace_img("vibe-coding-vs-spec","/static/img/vibe-vs-spec-workflow.svg","vibe-vs-spec-workflow.svg","Vibe coding loop: prompt, AI writes code, run it, ship or try again; spec-driven pipeline: specify, plan, tasks, implement, verify against the spec, with changes going back to the spec")
replace_img("vibe-coding-vs-spec","/static/img/vibe-vs-spec-when.svg","vibe-vs-spec-when.svg","Quadrant by code lifespan and cost of a bug: vibe coding for throwaway and side projects, a safety net for demos and internal pages, a light spec for long-lived personal tools, full spec-driven for payments, team projects and long-lived services")
