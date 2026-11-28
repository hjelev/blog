import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "postedit.py")).read())

# plex thetvdb
m=[logo("plex",580,70,90)]
m+=[box(700,70,260,50,TINT["red"],"red",rx=10,sw=2)+T(716,102,"TheTVDB",17,"red",mono=True,bold=True)+T(944,102,"ends 3 Dec",14,"red",mono=True,anchor="end")]
m+=[box(700,140,260,50,TINT["green"],"green",rx=10,sw=2)+T(716,172,"TMDB",17,"green",mono=True,bold=True)+T(944,172,"aired order",14,"green",mono=True,anchor="end")]
m+=[box(700,210,260,50,"panel2","yellow",rx=10,sw=2)+T(716,242,"DVD / absolute",16,"yellow",mono=True,bold=True)+T(944,242,"wait",14,"yellow",mono=True,anchor="end")]
m+=[link(680,115,696,95),link(680,140,696,165),link(680,165,696,235)]
header(IMG+"plex-thetvdb-header.svg","Plex · metadata",["Plex drops TheTVDB","on 3 December"],"Switch aired-order shows to TMDB; leave DVD and absolute order alone",chip="Edit › Advanced › Episode ordering",accent="green",motif=m)
compare(IMG+"plex-thetvdb-order.svg",
  dict(kicker="Files in aired order",title="Switch to TMDB",items=["S01E01 = first episode broadcast","TMDB uses the same numbering","New episodes keep arriving"],state="green",mark="✓"),
  dict(kicker="Files in DVD or absolute order",title="Don't switch yet",items=["Firefly S01E01 on DVD = “Serenity”","In aired order that pilot comes last","Absolute 1071 has no TMDB season to map to"],state="red",mark="✗"),
  title="Why the episode order decides it",sub="Plex reads the numbers in your filenames and won't rename files")
flow(IMG+"plex-thetvdb-switch.svg","Switching to TMDB",[
  dict(t="Legacy agent?",d="move to the Plex TV agent",state="yellow"),dict(t="Edit library",d="Advanced › Episode ordering",state="blue"),
  dict(t="The Movie Database",d="save",state="green"),dict(t="Check each show",d="its setting wins",state="yellow"),dict(t="Refresh",d="spot-check E01s",state="green")],
  note="Shows you set to TheTVDB by hand keep that setting after the library changes.",step_h=104)
decision(IMG+"plex-thetvdb-options.svg","Is the show still airing?",("Pick a bridge","Wait for TMDB episode groups, run TheTVDB-Provider, or use Jellyfin's TheTVDB plugin"),("Leave it on TheTVDB","Its metadata is already complete; nothing is lost"),yes_label="yes",no_label="ended",title="DVD or absolute-order shows",yes_state="yellow",no_state="green")
header_md("plex-thetvdb-ending","plex-thetvdb-header.svg","Plex drops TheTVDB on 3 December 2026: switch aired-order shows to TMDB, leave DVD and absolute-order shows on TheTVDB for now")
insert_after("plex-thetvdb-ending","Plex won't rename your files.","plex-thetvdb-order.svg","Files numbered in aired order map cleanly to TMDB; DVD-order files like Firefly and absolute-numbered anime get the wrong titles because TMDB in Plex only has aired order")
insert_after("plex-thetvdb-ending","After switching, refresh metadata","plex-thetvdb-switch.svg","Move legacy-agent libraries to the Plex TV agent, set Episode ordering to The Movie Database, check per-show overrides because they win, then refresh and spot-check")
insert_after("plex-thetvdb-ending","For DVD-order and absolute-order shows you have three options.","plex-thetvdb-options.svg","For DVD or absolute-order shows: ended shows can stay on TheTVDB with nothing lost; ongoing ones need a bridge, either waiting for TMDB episode groups, TheTVDB-Provider, or Jellyfin")

# ai self-hosting
m=[logo("ycombinator",580,70,80),T(620,190,"#1",30,"orange",bold=True,anchor="middle"),T(620,218,"1,126 pts",14,"muted",mono=True,anchor="middle")]
m+=[mini_term(700,70,260,["[[yellow|$]] git diff --stat","[[green|+]] hosts/nas/compose.yaml","[[yellow|$]] compose config -q","[[green|✓ valid]]"],size=14)]
header(IMG+"ai-self-hosting-header.svg","Self-hosting · AI agents",["AI made self-hosting","fun again?"],"The essay, the 526-comment backlash, and a setup that doesn't break your homelab",chip="agent edits the repo, you deploy",accent="orange",chip_color="green",motif=m)
stats(IMG+"ai-self-hosting-numbers.svg",[
  ("1,126","HN points","526 comments, #1 on 27 Nov","orange"),
  ("½ day","bootc image with AI","his own estimate","green"),
  ("1 week+","the same without AI","“at least a week”","muted"),
  ("63%","avoid vibe-coded apps","selfh.st 2026 survey","red")],title="The essay and the reaction in numbers")
compare(IMG+"ai-self-hosting-models.svg",
  dict(kicker="Agent on the live server",title="What people fear",items=["Runs commands over SSH until it works","No diff, no history, no review","Secrets and data within reach","Breaks at 2am; you can't see what changed"],state="red",mark="✗"),
  dict(kicker="Agent on a Git repo",title="What Else does",items=["Edits Compose files and NixOS modules","Every change is a commit you read","Secrets stay in git-ignored .env","Bad change? Revert or roll back"],state="green",mark="✓"),
  title="Two ways to use an agent")
flow(IMG+"ai-self-hosting-loop.svg","The safe loop",[
  dict(t="Agent edits repo",d="rules in AGENTS.md",logo="git"),dict(t="Dry run",d="compose config, nixos build",state="blue"),
  dict(t="You read the diff",d="can't explain it? don't ship",state="yellow"),dict(t="Deploy",d="by hand or CI",state="green")],
  note="The agent never gets a shell on the server or the real secrets.",step_h=104)
header_md("ai-made-self-hosting","ai-self-hosting-header.svg","AI made self-hosting fun again: Jan-Lukas Else's essay hit #1 on Hacker News; the safe setup has the agent edit a Git repo while you review and deploy")
insert_after("ai-made-self-hosting","His conclusion:","ai-self-hosting-numbers.svg","1,126 Hacker News points and 526 comments; half a day to build a bootc image with AI versus at least a week without; 63% of selfh.st survey respondents avoid vibe-coded apps")
insert_after("ai-made-self-hosting","The horror stories come from the other model","ai-self-hosting-models.svg","An agent with a shell on the live server has no review or history; an agent editing a Git repo produces commits you read, with secrets out of reach and easy rollback")
insert_after("ai-made-self-hosting","Run the agent in the repository on your laptop","ai-self-hosting-loop.svg","The agent edits the repo under AGENTS.md rules, you run a dry run, read the diff, then deploy by hand or with CI")
