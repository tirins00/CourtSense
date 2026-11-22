"""CourtSense visual system.

Each sport has its own colour theme and court-line artwork. Light and dark
modes share the same layout; everything is driven by CSS variables.
"""
from urllib.parse import quote

# hero = banner colour, accent = buttons / user bubble, accent-text = emphasis on page background
THEMES = {
    "Basketball": {
        "light": {"hero": "#E4520D", "accent": "#D9480F", "accent-text": "#C2410C"},
        "dark": {"hero": "#A63A0B", "accent": "#E4520D", "accent-text": "#FF9A5C"},
    },
    "Volleyball": {
        "light": {"hero": "#1D4ED8", "accent": "#1D4ED8", "accent-text": "#1D4ED8"},
        "dark": {"hero": "#1B3A94", "accent": "#3B63E0", "accent-text": "#8FAEFF"},
    },
    "Football": {
        "light": {"hero": "#0F7B3F", "accent": "#0F7B3F", "accent-text": "#0B6633"},
        "dark": {"hero": "#0B5E31", "accent": "#17A257", "accent-text": "#52D98C"},
    },
}

BASE = {
    "light": {"bg": "#EEF0F3", "panel": "#FFFFFF", "sidebar": "#E3E7EC", "ink": "#12171E",
              "muted": "#566170", "line": "#D5DAE1", "stripe": "#F4F6F8"},
    "dark": {"bg": "#0E1116", "panel": "#171B22", "sidebar": "#12161C", "ink": "#EDEFF2",
             "muted": "#9AA4B2", "line": "#2A313C", "stripe": "#1C212A"},
}

# court line art (white strokes, drawn faint). Coordinates are simple and hand-built.
_STROKE = "fill='none' stroke='white' stroke-width='3' stroke-opacity='0.28'"
ART = {
    "Basketball": (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 470'><g " + _STROKE + ">"
        "<rect x='10' y='10' width='480' height='450'/><rect x='170' y='10' width='160' height='190'/>"
        "<circle cx='250' cy='200' r='60'/><circle cx='250' cy='60' r='9'/>"
        "<path d='M220 40H280M200 10V10'/><path d='M40 10V140A210 210 0 0 0 460 140V10'/>"
        "<path d='M210 60A40 40 0 0 0 290 60'/><path d='M190 460A60 60 0 0 1 310 460'/></g></svg>"
    ),
    "Volleyball": (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 520 270'><g " + _STROKE + ">"
        "<rect x='10' y='10' width='500' height='250'/><path d='M260 -10V280' stroke-width='6'/>"
        "<path d='M177 10V260M343 10V260'/><path d='M177 135H343' stroke-dasharray='8 10'/></g></svg>"
    ),
    "Football": (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 520 340'><g " + _STROKE + ">"
        "<rect x='10' y='10' width='500' height='320'/><path d='M260 10V330'/><circle cx='260' cy='170' r='46'/>"
        "<rect x='10' y='95' width='84' height='150'/><rect x='426' y='95' width='84' height='150'/>"
        "<rect x='10' y='140' width='32' height='60'/><rect x='478' y='140' width='32' height='60'/>"
        "<path d='M94 133A46 46 0 0 1 94 207'/><path d='M426 133A46 46 0 0 0 426 207'/></g></svg>"
    ),
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,500;0,600;0,700;0,800;1,700;1,800&family=Barlow:wght@400;500;600&display=swap');

.stApp { background: var(--bg); }
.stApp, .stApp p, .stApp li, .stApp td, .stApp label, .stApp textarea, .stApp input {
  font-family: 'Barlow', sans-serif; color: var(--ink); }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p { color: var(--muted); }
#MainMenu, footer, .stAppDeployButton { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 880px; padding-top: 1.2rem; padding-bottom: 7rem; }
[data-testid="stSidebar"] { background: var(--sidebar); }
hr { border-color: var(--line); }

/* hero */
.st-key-hero { background-color: var(--hero); border-radius: 16px; padding: 16px 28px 0;
  overflow: hidden; margin-bottom: 14px; box-shadow: 0 14px 30px -18px rgba(0,0,0,.55);
  background-repeat: no-repeat; }
.st-key-hero [data-testid="stVerticalBlock"] { gap: .35rem; }
.wordmark { font-family:'Barlow Condensed',sans-serif; font-style: italic; font-weight: 800;
  font-size: 1.3rem; letter-spacing: .09em; text-transform: uppercase; color:#fff; }
.hero-title { font-family:'Barlow Condensed',sans-serif; font-style: italic; font-weight: 800;
  text-transform: uppercase; font-size: clamp(2.9rem, 9vw, 4.9rem); line-height: .92;
  letter-spacing: .01em; color:#fff; margin-top: 8px; }
.stApp .hero-sub { color: rgba(255,255,255,.9); font-size: 1.1rem; margin: 6px 0 12px; }
.stApp .st-key-dark label p { color:#fff; font-size:.9rem; }
.st-key-dark { display:flex; justify-content:flex-end; width:100%; }

/* sport and topic buttons (real buttons, styled by key) */
.st-key-hero [data-testid="stHorizontalBlock"] { flex-wrap: nowrap; gap: .5rem; }
.st-key-hero [data-testid="stColumn"] { min-width: 0; }
.stApp .st-key-hero button { color:#fff; }
.stApp .st-key-hero [class*="st-key-sp_"] button { width:100%; background:transparent;
  border:2px solid rgba(255,255,255,.6); border-radius:6px; transform:skewX(-9deg);
  min-height:2.9rem; padding:0 .8rem; }
.stApp .st-key-hero [class*="st-key-sp_"] button > div { transform:skewX(9deg); gap:.45rem; justify-content:center; }
.stApp .st-key-hero [class*="st-key-sp_"] button p { color:inherit; font-family:'Barlow Condensed',sans-serif;
  font-weight:700; font-size:1.2rem; letter-spacing:.02em; }
.stApp .st-key-hero [class*="st-key-sp_"] button:hover { background:rgba(255,255,255,.16); border-color:#fff; }
.st-key-topics { margin-top:14px; border-top:1px solid rgba(255,255,255,.3); }
.stApp .st-key-hero [class*="st-key-tp_"] button { width:100%; background:transparent !important; border:none;
  border-bottom:4px solid transparent; border-radius:0; min-height:3rem; padding:0 .4rem; }
.stApp .st-key-hero [class*="st-key-tp_"] button p { color:rgba(255,255,255,.76); font-family:'Barlow Condensed',sans-serif;
  font-weight:600; font-size:1.2rem; }
.stApp .st-key-hero [class*="st-key-tp_"] button:hover p { color:#fff; }

/* empty state */
.empty { background: var(--panel); border: 1px solid var(--line); border-radius: 14px; padding: 20px 22px; margin: 4px 0 12px; }
.empty-title { font-family:'Barlow Condensed',sans-serif; font-weight: 700; font-size: 1.6rem; line-height:1.1; }
.empty p { color: var(--muted); margin: 4px 0 0; }
.stApp .st-key-starters button { width:100%; justify-content:flex-start; text-align:left; min-height:4rem;
  padding:.7rem 1.1rem; border:1.5px solid var(--line); background:var(--panel); border-radius:12px; }
.stApp .st-key-starters button p { color:var(--ink); font-size:1rem; font-weight:500; text-align:left; }
.stApp .st-key-starters button:hover { border-color:var(--accent); background:var(--panel); }
.stApp .st-key-starters button:hover p { color:var(--accent-text); }
.st-key-startquiz button { background: var(--accent); border: none; border-radius: 10px; min-height: 3rem; padding: 0 1.6rem; }
.st-key-startquiz button p { color:#fff; font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:1.25rem; }
.st-key-startquiz button:hover { filter: brightness(1.1); }

/* chat */
[data-testid="stChatMessage"] { border-radius: 14px; padding: 14px 18px; margin-bottom: 10px;
  background: var(--panel); border: 1px solid var(--line); }
[data-testid="stChatMessageAvatarAssistant"] { background: var(--accent); border-radius: 50%; }
[data-testid="stChatMessageAvatarAssistant"] * { color:#fff; }
[data-testid="stChatMessageAvatarUser"] { display: none; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
  flex-direction: row-reverse; margin-left: auto; width: fit-content; max-width: 86%;
  background: var(--accent); border-color: var(--accent); border-radius: 16px 16px 4px 16px; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) li { color:#fff; }
[data-testid="stChatMessage"] strong { color: var(--accent-text); }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) strong { color:#fff; }
.attach { display:inline-block; margin-top:6px; padding:2px 10px; border:1px solid rgba(255,255,255,.6);
  border-radius:999px; font-size:.82rem; color:#fff; }

/* stat tables */
.stMarkdown table { border-collapse: collapse; width: 100%; margin: 6px 0; font-size: .93rem; }
.stMarkdown th { background: var(--hero); color:#fff; text-align:left; padding: 7px 10px;
  font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:1.05rem; }
.stMarkdown td { padding: 7px 10px; border-bottom: 1px solid var(--line); color: var(--ink); }
.stMarkdown tr:nth-child(even) td { background: var(--stripe); }

/* buttons under answers */
.stButton > button, .stDownloadButton > button { border-radius: 999px; border: 1.5px solid var(--accent);
  background: transparent; font-weight: 600; padding: .15rem 1rem; }
.stButton > button p, .stDownloadButton > button p { color: var(--accent-text); }
.stButton > button:hover, .stDownloadButton > button:hover { background: var(--accent); border-color: var(--accent); }
.stButton > button:hover p, .stDownloadButton > button:hover p { color:#fff; }

/* composer */
[data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] { background: var(--bg); }
[data-testid="stChatInput"] { background: var(--panel); border: 2px solid var(--line); border-radius: 14px; }
[data-testid="stChatInput"]:focus-within { border-color: var(--accent); }
[data-testid="stChatInput"] textarea { color: var(--ink); background: transparent; }
[data-testid="stChatInput"] button { color: var(--accent-text); }
[data-baseweb="select"] > div { background: var(--panel); border: 1px solid var(--line); }
[data-baseweb="select"] * { color: var(--ink); }
div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li { background: var(--panel); color: var(--ink); }

@media (max-width: 640px) {
  .st-key-hero { padding: 14px 14px 0; }
  .stApp .st-key-hero [class*="st-key-sp_"] button { padding: 0 .3rem; }
  .stApp .st-key-hero [class*="st-key-sp_"] button p { font-size: 1rem; }
  .stApp .st-key-hero [class*="st-key-tp_"] button p { font-size: 1.02rem; }
  .st-key-hero button span[data-testid="stIconMaterial"] { display: none; }
}
"""


def get_css(sport="Basketball", topic="Rules", dark=False):
    mode = "dark" if dark else "light"
    theme = {**BASE[mode], **THEMES.get(sport, THEMES["Basketball"])[mode]}
    root = ":root{" + "".join(f"--{k}:{v};" for k, v in theme.items()) + "}"
    art = ART.get(sport, ART["Basketball"])
    hero_bg = (
        ".st-key-hero{background-image:linear-gradient(90deg,var(--hero) 40%,transparent 80%),"
        "url(\"data:image/svg+xml," + quote(art) + "\");"
        "background-size:100% 100%,auto 125%;background-position:0 0,right -50px center;}"
    )
    sp, tp = f".stApp .st-key-sp_{sport}", f".stApp .st-key-tp_{topic}"
    active = (
        f"{sp} button,{sp} button:hover{{background:#fff !important;border-color:#fff !important;color:var(--hero) !important;}}"
        f"{sp} button p,{sp} button:hover p{{color:var(--hero) !important;}}"
        f"{tp} button{{border-bottom-color:#fff !important;}}"
        f"{tp} button p{{color:#fff !important;font-weight:700;}}"
    )
    return "<style>" + root + CSS + hero_bg + active + "</style>"
