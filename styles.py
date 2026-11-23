"""CourtSense visual system - refined with UI/UX Pro Max design intelligence.

Each sport features a high-impact, athletic color theme and court blueprint artwork.
Light and dark modes share an ultra-refined design system driven by CSS variables:
  - Athletic Condensed typography (Barlow Condensed) paired with crisp modern sans-serif (Plus Jakarta Sans)
  - Bento-grid card hierarchy with subtle elevation and borders
  - Sport-specific dynamic gradients and court line art watermark
  - WCAG AAA/AA compliant contrast across light and dark modes
  - Accessible micro-interactions, responsive touch targets, and reduced-motion support
"""
from urllib.parse import quote

THEMES = {
    "Basketball": {
        "light": {
            "hero-start": "#E04F16",
            "hero-end": "#9A3412",
            "hero": "#EA580C",
            "accent": "#EA580C",
            "accent-hover": "#C2410C",
            "accent-glow": "rgba(234, 88, 12, 0.28)",
            "accent-text": "#C2410C",
            "accent-light": "#FFF7ED",
            "bubble-user-start": "#F97316",
            "bubble-user-end": "#EA580C",
        },
        "dark": {
            "hero-start": "#C2410C",
            "hero-end": "#7C2D12",
            "hero": "#9A3412",
            "accent": "#F97316",
            "accent-hover": "#FB923C",
            "accent-glow": "rgba(249, 115, 22, 0.35)",
            "accent-text": "#FB923C",
            "accent-light": "rgba(249, 115, 22, 0.12)",
            "bubble-user-start": "#EA580C",
            "bubble-user-end": "#C2410C",
        },
    },
    "Volleyball": {
        "light": {
            "hero-start": "#2563EB",
            "hero-end": "#1E40AF",
            "hero": "#1D4ED8",
            "accent": "#2563EB",
            "accent-hover": "#1D4ED8",
            "accent-glow": "rgba(37, 99, 235, 0.28)",
            "accent-text": "#1D4ED8",
            "accent-light": "#EFF6FF",
            "bubble-user-start": "#3B82F6",
            "bubble-user-end": "#2563EB",
        },
        "dark": {
            "hero-start": "#1D4ED8",
            "hero-end": "#172554",
            "hero": "#1E3A8A",
            "accent": "#3B82F6",
            "accent-hover": "#60A5FA",
            "accent-glow": "rgba(59, 130, 246, 0.35)",
            "accent-text": "#93C5FD",
            "accent-light": "rgba(59, 130, 246, 0.12)",
            "bubble-user-start": "#2563EB",
            "bubble-user-end": "#1D4ED8",
        },
    },
    "Football": {
        "light": {
            "hero-start": "#059669",
            "hero-end": "#065F46",
            "hero": "#059669",
            "accent": "#059669",
            "accent-hover": "#047857",
            "accent-glow": "rgba(5, 150, 105, 0.28)",
            "accent-text": "#047857",
            "accent-light": "#ECFDF5",
            "bubble-user-start": "#10B981",
            "bubble-user-end": "#059669",
        },
        "dark": {
            "hero-start": "#047857",
            "hero-end": "#064E3B",
            "hero": "#065F46",
            "accent": "#10B981",
            "accent-hover": "#34D399",
            "accent-glow": "rgba(16, 185, 129, 0.35)",
            "accent-text": "#6EE7B7",
            "accent-light": "rgba(16, 185, 129, 0.12)",
            "bubble-user-start": "#059669",
            "bubble-user-end": "#047857",
        },
    },
}

BASE = {
    "light": {
        "bg": "#F8FAFC",
        "panel": "#FFFFFF",
        "panel-hover": "#F8FAFC",
        "sidebar": "#F1F5F9",
        "sidebar-card": "#FFFFFF",
        "ink": "#0F172A",
        "ink-secondary": "#334155",
        "muted": "#64748B",
        "line": "#E2E8F0",
        "line-subtle": "#F1F5F9",
        "stripe": "#F8FAFC",
        "card-shadow": "0 2px 10px -2px rgba(15, 23, 42, 0.06), 0 1px 3px rgba(15, 23, 42, 0.04)",
        "card-shadow-hover": "0 10px 28px -4px rgba(15, 23, 42, 0.1), 0 3px 8px rgba(15, 23, 42, 0.04)",
    },
    "dark": {
        "bg": "#0B0F17",
        "panel": "#131924",
        "panel-hover": "#172131",
        "sidebar": "#0E131E",
        "sidebar-card": "#141C2B",
        "ink": "#F8FAFC",
        "ink-secondary": "#CBD5E1",
        "muted": "#94A3B8",
        "line": "#1E293B",
        "line-subtle": "#16202E",
        "stripe": "#161E2D",
        "card-shadow": "0 2px 12px -2px rgba(0, 0, 0, 0.4), 0 1px 3px rgba(0, 0, 0, 0.2)",
        "card-shadow-hover": "0 12px 32px -4px rgba(0, 0, 0, 0.6), 0 4px 10px rgba(0, 0, 0, 0.3)",
    },
}

# Court blueprint artwork - refined vectors with soft luminous stroke
_STROKE = "fill='none' stroke='white' stroke-width='2.6' stroke-opacity='0.24' stroke-linecap='round' stroke-linejoin='round'"
ART = {
    "Basketball": (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 470'><g " + _STROKE + ">"
        "<rect x='12' y='12' width='476' height='446' rx='6'/>"
        "<rect x='170' y='12' width='160' height='190'/>"
        "<circle cx='250' cy='202' r='62'/>"
        "<circle cx='250' cy='62' r='10'/>"
        "<path d='M220 40H280M200 12V12'/>"
        "<path d='M42 12V140A208 208 0 0 0 458 140V12'/>"
        "<path d='M210 62A40 40 0 0 0 290 62'/>"
        "<path d='M190 458A60 60 0 0 1 310 458'/>"
        "</g></svg>"
    ),
    "Volleyball": (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 520 270'><g " + _STROKE + ">"
        "<rect x='12' y='12' width='496' height='246' rx='6'/>"
        "<path d='M260 -10V280' stroke-width='5.5' stroke-opacity='0.36'/>"
        "<path d='M178 12V258M342 12V258'/>"
        "<path d='M178 135H342' stroke-dasharray='8 10'/>"
        "</g></svg>"
    ),
    "Football": (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 520 340'><g " + _STROKE + ">"
        "<rect x='12' y='12' width='496' height='316' rx='6'/>"
        "<path d='M260 12V328'/>"
        "<circle cx='260' cy='170' r='48'/>"
        "<rect x='12' y='95' width='86' height='150'/>"
        "<rect x='422' y='95' width='86' height='150'/>"
        "<rect x='12' y='140' width='34' height='60'/>"
        "<rect x='474' y='140' width='34' height='60'/>"
        "<path d='M98 132A48 48 0 0 1 98 208'/>"
        "<path d='M422 132A48 48 0 0 0 422 208'/>"
        "</g></svg>"
    ),
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,700;1,800&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&display=swap');

/* --- Global Reset & Modern Typography --- */
html, body, [class*="st-"] {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.stApp {
  background: var(--bg);
  color: var(--ink);
  transition: background-color 0.25s ease, color 0.25s ease;
}

.stApp, .stApp p, .stApp li, .stApp td, .stApp label, .stApp textarea, .stApp input {
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: var(--ink);
}

[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p {
  color: var(--muted);
  font-size: 0.85rem;
  line-height: 1.5;
}

#MainMenu, footer, .stAppDeployButton { visibility: hidden; display: none; }
header[data-testid="stHeader"] { background: transparent; }

.block-container {
  max-width: 880px;
  padding-top: 1.2rem;
  padding-bottom: 7.5rem;
}

[data-testid="stSidebar"] {
  background: var(--sidebar);
  border-right: 1px solid var(--line);
}

hr {
  border-color: var(--line);
  margin: 1.2rem 0;
}

/* Accessibility: Visible Focus Rings */
*:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

/* --- Hero Banner (Athletic Card Elevation) --- */
.st-key-hero {
  background-color: var(--hero);
  border-radius: 18px;
  padding: 20px 28px 12px;
  overflow: hidden;
  margin-bottom: 16px;
  box-shadow: 0 16px 36px -12px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.22);
  border: 1px solid rgba(255,255,255,0.18);
  position: relative;
  transition: all 0.3s ease;
}

.st-key-hero [data-testid="stVerticalBlock"] {
  gap: 0.4rem;
}

/* Wordmark & Pro Badge */
.wordmark-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.wordmark-badge {
  display: inline-flex;
  align-items: center;
  background: rgba(255,255,255,0.2);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.32);
  color: #FFFFFF;
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 2px 7px;
  border-radius: 4px;
}

.wordmark {
  font-family: 'Barlow Condensed', sans-serif;
  font-style: italic;
  font-weight: 800;
  font-size: 1.45rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #FFFFFF;
}

.hero-title {
  font-family: 'Barlow Condensed', sans-serif;
  font-style: italic;
  font-weight: 800;
  text-transform: uppercase;
  font-size: clamp(3rem, 8.5vw, 4.8rem);
  line-height: 0.92;
  letter-spacing: 0.02em;
  color: #FFFFFF;
  margin-top: 6px;
  text-shadow: 0 3px 14px rgba(0,0,0,0.3);
}

.stApp .hero-sub {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255,255,255,0.92);
  font-size: 1.05rem;
  font-weight: 500;
  margin: 6px 0 14px;
}

.sub-pill {
  display: inline-block;
  background: rgba(0,0,0,0.22);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  border: 1px solid rgba(255,255,255,0.25);
  border-radius: 999px;
  padding: 2px 10px;
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #FFFFFF;
}

.st-key-dark {
  display: flex;
  justify-content: flex-end;
  width: 100%;
}

.stApp .st-key-dark label p {
  color: #FFFFFF;
  font-size: 0.88rem;
  font-weight: 600;
}

/* --- Sport Selection Buttons (Athletic Segmented Control) --- */
.st-key-hero [data-testid="stHorizontalBlock"] {
  flex-wrap: nowrap;
  gap: 0.6rem;
}

.st-key-hero [data-testid="stColumn"] {
  min-width: 0;
}

.stApp .st-key-hero [class*="st-key-sp_"] button {
  width: 100%;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1.5px solid rgba(255, 255, 255, 0.32);
  border-radius: 10px;
  min-height: 2.85rem;
  padding: 0 0.8rem;
  color: #FFFFFF;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
}

.stApp .st-key-hero [class*="st-key-sp_"] button > div {
  gap: 0.5rem;
  justify-content: center;
}

.stApp .st-key-hero [class*="st-key-sp_"] button p {
  color: #FFFFFF;
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 1.15rem;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}

.stApp .st-key-hero [class*="st-key-sp_"] button:hover {
  background: rgba(255, 255, 255, 0.22);
  border-color: rgba(255, 255, 255, 0.7);
  transform: translateY(-1.5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.18);
}

/* --- Topic Tabs Bar --- */
.st-key-topics {
  margin-top: 14px;
  padding-top: 6px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.stApp .st-key-hero [class*="st-key-tp_"] button {
  width: 100%;
  background: transparent !important;
  border: none;
  border-radius: 8px;
  border-bottom: 3px solid transparent;
  min-height: 2.75rem;
  padding: 0 0.4rem;
  transition: all 0.2s ease;
  cursor: pointer;
}

.stApp .st-key-hero [class*="st-key-tp_"] button p {
  color: rgba(255, 255, 255, 0.75);
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 600;
  font-size: 1.15rem;
  letter-spacing: 0.02em;
}

.stApp .st-key-hero [class*="st-key-tp_"] button:hover {
  background: rgba(255, 255, 255, 0.1) !important;
}

.stApp .st-key-hero [class*="st-key-tp_"] button:hover p {
  color: #FFFFFF;
}

/* --- Empty States (Bento Card Styling) --- */
.empty {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 22px 26px;
  margin: 6px 0 16px;
  box-shadow: var(--card-shadow);
  position: relative;
  overflow: hidden;
  transition: border-color 0.2s ease;
}

.empty::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: var(--accent);
}

.empty-badge {
  display: inline-block;
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent-text);
  background: var(--accent-light);
  padding: 3px 8px;
  border-radius: 4px;
  margin-bottom: 8px;
}

.empty-title {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 800;
  font-size: 1.7rem;
  line-height: 1.15;
  color: var(--ink);
  letter-spacing: 0.01em;
  text-transform: uppercase;
}

.empty p {
  color: var(--muted);
  margin: 6px 0 0;
  font-size: 0.96rem;
  line-height: 1.5;
}

/* Starter Question Cards */
.stApp .st-key-starters button {
  width: 100%;
  justify-content: flex-start;
  text-align: left;
  min-height: 4.4rem;
  padding: 0.85rem 1.25rem;
  border: 1.5px solid var(--line);
  background: var(--panel);
  border-radius: 14px;
  box-shadow: var(--card-shadow);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
}

.stApp .st-key-starters button p {
  color: var(--ink);
  font-size: 0.98rem;
  font-weight: 600;
  line-height: 1.4;
  text-align: left;
}

.stApp .st-key-starters button:hover {
  border-color: var(--accent);
  background: var(--panel-hover);
  transform: translateY(-2px);
  box-shadow: var(--card-shadow-hover);
}

.stApp .st-key-starters button:hover p {
  color: var(--accent-text);
}

/* Quiz CTA Button */
.st-key-startquiz button {
  background: var(--accent);
  border: none;
  border-radius: 12px;
  min-height: 3.2rem;
  padding: 0 1.8rem;
  box-shadow: 0 4px 14px var(--accent-glow);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
}

.st-key-startquiz button p {
  color: #FFFFFF;
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 800;
  font-size: 1.3rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.st-key-startquiz button:hover {
  filter: brightness(1.1);
  transform: translateY(-1.5px);
  box-shadow: 0 6px 20px var(--accent-glow);
}

/* --- Chat Messages & Avatars --- */
[data-testid="stChatMessage"] {
  border-radius: 16px;
  padding: 16px 20px;
  margin-bottom: 14px;
  background: var(--panel);
  border: 1px solid var(--line);
  box-shadow: var(--card-shadow);
  line-height: 1.6;
}

[data-testid="stChatMessageAvatarAssistant"] {
  background: var(--accent);
  border-radius: 50%;
  box-shadow: 0 2px 8px var(--accent-glow);
}

[data-testid="stChatMessageAvatarAssistant"] * {
  color: #FFFFFF;
}

[data-testid="stChatMessageAvatarUser"] {
  display: none;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
  flex-direction: row-reverse;
  margin-left: auto;
  width: fit-content;
  max-width: 84%;
  background: var(--bubble-user-start);
  background: linear-gradient(135deg, var(--bubble-user-start) 0%, var(--bubble-user-end) 100%);
  border: 1px solid transparent;
  border-radius: 18px 18px 4px 18px;
  box-shadow: 0 4px 14px var(--accent-glow);
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) li {
  color: #FFFFFF;
  font-weight: 500;
}

[data-testid="stChatMessage"] strong {
  color: var(--accent-text);
  font-weight: 700;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) strong {
  color: #FFFFFF;
}

.attach {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
  padding: 3px 12px;
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.45);
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 600;
  color: #FFFFFF;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

/* --- Markdown Tables (Sports Stat Comparisons) --- */
.stMarkdown table {
  border-collapse: separate;
  border-spacing: 0;
  width: 100%;
  margin: 12px 0;
  font-size: 0.94rem;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--line);
  box-shadow: var(--card-shadow);
}

.stMarkdown th {
  background: var(--hero);
  background: linear-gradient(135deg, var(--hero-start) 0%, var(--hero-end) 100%);
  color: #FFFFFF;
  text-align: left;
  padding: 10px 14px;
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 1.08rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  border: none;
}

.stMarkdown td {
  padding: 9px 14px;
  border-bottom: 1px solid var(--line);
  color: var(--ink);
  font-feature-settings: "tnum";
}

.stMarkdown tr:last-child td {
  border-bottom: none;
}

.stMarkdown tr:nth-child(even) td {
  background: var(--stripe);
}

.stMarkdown tr:hover td {
  background: var(--accent-light);
}

/* --- Quick Action Chips & Buttons Under Answers --- */
.stApp [class*="st-key-qa_"] button {
  border-radius: 999px;
  border: 1.5px solid var(--accent);
  background: var(--panel);
  font-weight: 600;
  font-size: 0.88rem;
  padding: 0.3rem 1.1rem;
  min-height: 2.3rem;
  box-shadow: var(--card-shadow);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
}

.stApp [class*="st-key-qa_"] button p {
  color: var(--accent-text);
}

.stApp [class*="st-key-qa_"] button:hover {
  background: var(--accent);
  border-color: var(--accent);
  transform: translateY(-1.5px);
  box-shadow: 0 4px 12px var(--accent-glow);
}

.stApp [class*="st-key-qa_"] button:hover p {
  color: #FFFFFF;
}

/* --- Composer Input --- */
[data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] {
  background: var(--bg);
}

[data-testid="stChatInput"] {
  background: var(--panel);
  border: 1.5px solid var(--line);
  border-radius: 16px;
  box-shadow: var(--card-shadow);
  transition: border-color 0.2s, box-shadow 0.2s;
}

[data-testid="stChatInput"]:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-glow), var(--card-shadow-hover);
}

[data-testid="stChatInput"] textarea {
  color: var(--ink);
  background: transparent;
  font-size: 0.96rem;
}

[data-testid="stChatInput"] button {
  color: var(--accent-text);
  transition: color 0.15s ease, transform 0.15s ease;
}

[data-testid="stChatInput"] button:hover {
  color: var(--accent-hover);
  transform: scale(1.06);
}

[data-baseweb="select"] > div {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 10px;
}

[data-baseweb="select"] * {
  color: var(--ink);
}

div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li {
  background: var(--panel);
  color: var(--ink);
}

/* --- Sidebar Styling --- */
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 800;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  font-size: 1.35rem;
  color: var(--ink);
}

.sidebar-header {
  margin-bottom: 0.5rem;
}

.sidebar-badge {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  font-family: 'Barlow Condensed', sans-serif;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: var(--accent-light);
  color: var(--accent-text);
  padding: 2px 7px;
  border-radius: 4px;
}

[data-testid="stSidebar"] .stDownloadButton > button {
  border-radius: 10px;
  border: 1.5px solid var(--accent);
  background: transparent;
  font-weight: 700;
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 1.05rem;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  transition: all 0.2s ease;
  cursor: pointer;
}

[data-testid="stSidebar"] .stDownloadButton > button p {
  color: var(--accent-text);
}

[data-testid="stSidebar"] .stDownloadButton > button:hover {
  background: var(--accent);
  border-color: var(--accent);
  box-shadow: 0 4px 12px var(--accent-glow);
}

[data-testid="stSidebar"] .stDownloadButton > button:hover p {
  color: #FFFFFF;
}

[data-testid="stSidebar"] .stButton > button {
  border-radius: 10px;
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 1.05rem;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  transition: all 0.2s ease;
  cursor: pointer;
}

/* --- Mobile Responsiveness --- */
@media (max-width: 640px) {
  .block-container {
    padding-top: 0.8rem;
    padding-bottom: 6.5rem;
    padding-left: 0.9rem;
    padding-right: 0.9rem;
  }
  .st-key-hero {
    padding: 16px 16px 8px;
    border-radius: 14px;
  }
  .hero-title {
    font-size: 2.7rem;
  }
  .stApp .st-key-hero [class*="st-key-sp_"] button {
    padding: 0 0.35rem;
    min-height: 2.6rem;
  }
  .stApp .st-key-hero [class*="st-key-sp_"] button p {
    font-size: 0.98rem;
  }
  .stApp .st-key-hero [class*="st-key-tp_"] button p {
    font-size: 0.98rem;
  }
  .st-key-hero button span[data-testid="stIconMaterial"] {
    display: none;
  }
  [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    max-width: 92%;
  }
  .stApp .st-key-starters button {
    min-height: 3.8rem;
    padding: 0.7rem 0.9rem;
  }
}

/* --- Reduced Motion Accessibility --- */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    transform: none !important;
  }
}
"""


def get_css(sport="Basketball", topic="Rules", dark=False):
    mode = "dark" if dark else "light"
    theme = {**BASE[mode], **THEMES.get(sport, THEMES["Basketball"])[mode]}
    root = ":root{" + "".join(f"--{k}:{v};" for k, v in theme.items()) + "}"
    art = ART.get(sport, ART["Basketball"])
    hero_bg = (
        ".st-key-hero{"
        "background-image:linear-gradient(90deg,var(--hero-start) 35%,rgba(0,0,0,0.1) 85%),"
        "radial-gradient(circle at 90% 40%,rgba(255,255,255,0.12) 0%,transparent 50%),"
        "url(\"data:image/svg+xml," + quote(art) + "\");"
        "background-size:100% 100%,100% 100%,auto 130%;"
        "background-position:0 0,0 0,right -30px center;"
        "background-repeat:no-repeat;}"
    )
    sp = f".stApp .st-key-sp_{sport}"
    tp = f".stApp .st-key-tp_{topic}"
    active = (
        f"{sp} button,{sp} button:hover{{"
        f"background:#FFFFFF !important;border-color:#FFFFFF !important;color:var(--hero) !important;"
        f"transform:translateY(-1.5px);box-shadow:0 6px 18px rgba(0,0,0,0.25) !important;}}"
        f"{sp} button p,{sp} button:hover p{{color:var(--hero) !important;font-weight:800 !important;}}"
        f"{sp} button span[data-testid='stIconMaterial']{{color:var(--hero) !important;}}"
        f"{tp} button{{"
        f"border-bottom-color:#FFFFFF !important;background:rgba(255,255,255,0.16) !important;}}"
        f"{tp} button p{{color:#FFFFFF !important;font-weight:800 !important;}}"
        f"{tp} button span[data-testid='stIconMaterial']{{color:#FFFFFF !important;}}"
    )
    return "<style>" + root + CSS + hero_bg + active + "</style>"
