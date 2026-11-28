import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "postedit.py")).read())

# ls alternatives
header(IMG+"ls-alternatives-header.svg","CLI · file listing",["The best ls","alternatives"],"eza, lsd and colorls compared, with install commands",chip="eza -l --git --icons",accent="blue",
  motif=[mini_term(580,60,390,["[[green|$]] eza -l --git","[[green|-M]]  4.1k  [[blue|src/]]","[[dim|--]]  1.2k  [[yellow|Cargo.toml]]","[[green|N-]]  3.0k  [[text|README.md]]","[[dim|--]]  9.8k  [[text|main.rs]]"],15,"~/project")])
cards(IMG+"ls-alternatives-pick.svg",[
  dict(name="eza",icon="list",accent="green",desc="Most active, most features, best Git columns",tag="pick",tag_color="green"),
  dict(name="lsd",icon="folder",accent="blue",desc="Icons on by default, very visual layout"),
  dict(name="colorls",icon="code",accent="red",desc="Ruby gem; slower, fine if Ruby is already there"),
  dict(name="exa",icon="cross",color="dim",accent="red",desc="Unmaintained: use eza, same lineage",tag="legacy",tag_color="red"),
 ],cols=2,title="Which one to pick",sub="all of them need a Nerd Font for icons")
header_md("best-ls-alternatives","ls-alternatives-header.svg","eza -l output with Git status columns and Nerd Font icons")
insert_before("best-ls-alternatives","## Picking one","ls-alternatives-pick.svg","Pick eza for features and Git columns, lsd for icons by default, colorls if you already use Ruby; exa is unmaintained, use eza instead")

# tui file managers
body=""
m=[box(580,62,390,236,"term","line",rx=10)]
for i,x in enumerate((596,716,846)):
    m.append(f'<line x1="{x-8}" y1="74" x2="{x-8}" y2="286" stroke="{C["line"]}"/>' if i else "")
for j,(t,c) in enumerate((("home","blue"),("git","blue"),("blog","yellow"),(".config","blue"))):
    m.append(T(596,98+j*28,t,14,c,mono=True))
for j,(t,c) in enumerate((("_posts","blue"),("static","blue"),("index.html","text"),("README.md","text"))):
    if j==0: m.append(box(712,80,124,26,"panel2",None,rx=4))
    m.append(T(716,98+j*28,t,14,c,mono=True))
for j,t in enumerate(("2026-11-28-","android-17-","2026-11-25-","trending-tui")):
    m.append(T(846,98+j*28,t,13,"muted",mono=True))
m.append(T(596,278,"sb  ~/git/blog/_posts",13,"green",mono=True))
header(IMG+"tui-file-managers-header.svg","CLI · file managers",["Terminal file","managers in 2026"],"Shell Buddy, Yazi, ranger, nnn, lf, superfile, Walk and mc",accent="green",motif=m)
cards(IMG+"tui-file-managers-pick.svg",[
  dict(name="Shell Buddy",icon="terminal",accent="green",desc="Most modern: Git and file encryption built in"),
  dict(name="Yazi",icon="bolt",accent="yellow",desc="Fast async previews, images included"),
  dict(name="ranger / lf",icon="code",accent="green",desc="Vim keys; lf is the leaner Go take"),
  dict(name="nnn",icon="chip",accent="blue",desc="Smallest footprint of the lot"),
  dict(name="Walk (lk)",icon="search",accent="blue",desc="A faster cd/ls with fuzzy search"),
  dict(name="Midnight Commander",icon="window",accent="blue",desc="Two-pane classic, stable for decades"),
 ],title="Pick by what you want")
header_md("best-tui-file-managers","tui-file-managers-header.svg","A three-column terminal file manager showing folders, a selected directory and file previews")
insert_before("best-tui-file-managers","## Picking one","tui-file-managers-pick.svg","Pick Shell Buddy for Git and encryption, Yazi for image previews, ranger or lf for Vim keys, nnn for the smallest footprint, Walk for fuzzy cd, Midnight Commander for a stable classic")

# nerd fonts
m=[box(580,70,180,200,"panel","line",rx=12),box(790,70,180,200,"panel","line",rx=12)]
m+=[T(670,104,"NO NERD FONT",13,"red",mono=True,anchor="middle"),T(880,104,"NERD FONT",13,"green",mono=True,anchor="middle")]
for j,(a,b) in enumerate(((" ","src"),(" ","main"),(" ","docs"))):
    m+=[box(600,128+j*44,22,26,"none","dim",rx=3,sw=2),T(634,148+j*44,b,16,"muted",mono=True)]
m+=[icon("folder",808,126,28,"blue"),T(846,148,"src",16,"text",mono=True),icon("git",808,170,28,"orange","orange",sw=3),T(846,192,"main",16,"text",mono=True),icon("file",808,214,28,"yellow"),T(846,236,"docs",16,"text",mono=True)]
header(IMG+"nerd-fonts-header.svg","Terminal · fonts",["Nerd Fonts:","what and why"],"Why eza, Starship and Yazi show boxes, and how to fix it",chip="brew install --cask font-jetbrains-mono-nerd-font",accent="yellow",motif=m)
flow(IMG+"nerd-fonts-patching.svg","What “patched” means",[
  dict(t="A coding font",d="JetBrains Mono, Fira Code, Hack"),dict(t="+ icon sets",d="file types, OS, Git, powerline",state="yellow"),
  dict(t="Nerd Font",d="one font, thousands of glyphs",state="green"),dict(t="Your terminal",d="eza, Starship, btop, Neovim")],
  note="Every icon is a single character, so it works at any size in any app that uses the font.",step_h=100)
header_md("nerd-fonts-what-why","nerd-fonts-header.svg","Without a Nerd Font icons render as empty boxes; with one you get folder, Git branch and file glyphs")
insert_before("nerd-fonts-what-why","## Why you need them","nerd-fonts-patching.svg","A coding font such as JetBrains Mono is patched with icon sets for file types, operating systems and Git to make a Nerd Font, which tools like eza, Starship, btop and Neovim use")
