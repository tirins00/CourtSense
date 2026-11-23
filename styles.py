"""CourtSense visual system - refined with UI/UX Pro Max design intelligence.

Each sport features a high-impact, athletic color theme and court blueprint artwork.
Light and dark modes share an ultra-refined design system driven by CSS variables:
  - Refined editorial-athletic typography (Space Grotesk display + DM Sans body + JetBrains Mono telemetry)
  - Bento-grid card hierarchy with subtle elevation and borders
  - Sport-specific dynamic gradients and court line art watermark
  - WCAG AAA/AA compliant contrast across light and dark modes
  - Accessible micro-interactions, responsive touch targets, and reduced-motion support
"""
import base64
from urllib.parse import quote

THEMES = {
    "Basketball": {
        "light": {
            "hero-start": "#1A1411",
            "hero-end": "#261B15",
            "hero": "#1A1411",
            "accent": "#C94A12",
            "accent-hover": "#A83B0B",
            "accent-edge": "#8C3008",
            "accent-text": "#B8400C",
            "accent-light": "rgba(201, 74, 18, 0.09)",
            "bubble-user": "#C94A12",
        },
        "dark": {
            "hero-start": "#15110E",
            "hero-end": "#221813",
            "hero": "#15110E",
            "accent": "#E85D1A",
            "accent-hover": "#F27130",
            "accent-edge": "#9E3B0C",
            "accent-text": "#F28B50",
            "accent-light": "rgba(232, 93, 26, 0.14)",
            "bubble-user": "#C94A12",
        },
    },
    "Volleyball": {
        "light": {
            "hero-start": "#101929",
            "hero-end": "#17253D",
            "hero": "#101929",
            "accent": "#1B4B9E",
            "accent-hover": "#153B7D",
            "accent-edge": "#0F2B5C",
            "accent-text": "#18448F",
            "accent-light": "rgba(27, 75, 158, 0.09)",
            "bubble-user": "#1B4B9E",
        },
        "dark": {
            "hero-start": "#0D1524",
            "hero-end": "#15233A",
            "hero": "#0D1524",
            "accent": "#3B77E8",
            "accent-hover": "#558DF0",
            "accent-edge": "#1F4EA6",
            "accent-text": "#7EAAFA",
            "accent-light": "rgba(59, 119, 232, 0.15)",
            "bubble-user": "#1F54B5",
        },
    },
    "Football": {
        "light": {
            "hero-start": "#0E1F17",
            "hero-end": "#142D22",
            "hero": "#0E1F17",
            "accent": "#146C43",
            "accent-hover": "#0F5534",
            "accent-edge": "#0A3D25",
            "accent-text": "#115C39",
            "accent-light": "rgba(20, 108, 67, 0.09)",
            "bubble-user": "#146C43",
        },
        "dark": {
            "hero-start": "#0B1912",
            "hero-end": "#12291E",
            "hero": "#0B1912",
            "accent": "#22A366",
            "accent-hover": "#2BB876",
            "accent-edge": "#126B41",
            "accent-text": "#5CD69C",
            "accent-light": "rgba(34, 163, 102, 0.14)",
            "bubble-user": "#146C43",
        },
    },
}

BASE = {
    "light": {
        "bg": "#F3EFE7",
        "panel": "#FAF8F3",
        "panel-hover": "#FFFFFF",
        "sidebar": "#EAE4D8",
        "sidebar-card": "#FAF8F3",
        "ink": "#161513",
        "ink-secondary": "#3D3A34",
        "muted": "#666158",
        "line": "#D8D1C4",
        "line-subtle": "#E8E2D6",
        "stripe": "#EFEAE0",
        "input-bg": "#FCFBF8",
        "input-border": "#C5BEB0",
        "input-hover-bg": "rgba(22, 21, 19, 0.06)",
        "input-btn-disabled-bg": "#E4DED2",
        "input-btn-disabled-fg": "#9A9386",
        "input-chip-bg": "#EAE4D8",
        "bottom-fade": "linear-gradient(180deg, rgba(243, 239, 231, 0) 0%, rgba(243, 239, 231, 0.94) 30%, #F3EFE7 100%)",
        "card-shadow": "0 1px 2px rgba(22, 21, 19, 0.05)",
        "card-shadow-hover": "0 6px 18px rgba(22, 21, 19, 0.09)",
    },
    "dark": {
        "bg": "#0E0F11",
        "panel": "#16181C",
        "panel-hover": "#1C1F24",
        "sidebar": "#111316",
        "sidebar-card": "#16181C",
        "ink": "#F2EFE8",
        "ink-secondary": "#CCC7BC",
        "muted": "#928D83",
        "line": "#2A2D33",
        "line-subtle": "#1F2227",
        "stripe": "#1A1D22",
        "input-bg": "#131519",
        "input-border": "#363A42",
        "input-hover-bg": "rgba(242, 239, 232, 0.07)",
        "input-btn-disabled-bg": "#22252B",
        "input-btn-disabled-fg": "#5A5E66",
        "input-chip-bg": "#22252B",
        "bottom-fade": "linear-gradient(180deg, rgba(14, 15, 17, 0) 0%, rgba(14, 15, 17, 0.94) 30%, #0E0F11 100%)",
        "card-shadow": "0 1px 3px rgba(0, 0, 0, 0.35)",
        "card-shadow-hover": "0 8px 24px rgba(0, 0, 0, 0.55)",
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

FONT_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Space+Grotesk:wght@500;600;700"
    "&family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400"
    "&family=JetBrains+Mono:wght@500;600;700"
    "&display=swap"
)

CSS = """
/* --- Global Reset & Refined Typography --- */
:root {
  --font-display: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-body: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;
}

html, body, [class*="st-"] {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

.stApp {
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font-body);
  font-optical-sizing: auto;
  transition: background-color 0.25s ease, color 0.25s ease;
}

.stApp, .stApp p, .stApp li, .stApp td, .stApp label, .stApp textarea, .stApp input {
  font-family: var(--font-body);
  font-optical-sizing: auto;
  color: var(--ink);
}

.stApp button {
  font-family: var(--font-body);
}

.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
  font-family: var(--font-display);
  letter-spacing: -0.02em;
  color: var(--ink);
}

.stApp code, .stApp pre {
  font-family: var(--font-mono);
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

/* --- Hero Scoreboard Banner --- */
.st-key-hero {
  background-color: var(--hero);
  border-radius: 8px;
  padding: 20px 26px 10px;
  overflow: hidden;
  margin-bottom: 18px;
  border: 1px solid rgba(255,255,255,0.08);
  border-top: 3px solid var(--accent);
  box-shadow: 0 10px 28px rgba(0,0,0,0.22);
  position: relative;
  transition: border-color 0.25s ease;
}

.st-key-hero [data-testid="stVerticalBlock"] {
  gap: 0.4rem;
}

/* Wordmark & Credential Badge */
.wordmark-wrap {
  display: flex;
  align-items: center;
  gap: 9px;
}

.wordmark-badge {
  display: inline-flex;
  align-items: center;
  background: var(--accent);
  border: none;
  color: #FFFFFF;
  font-family: var(--font-mono);
  font-size: 0.66rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 3px 7px;
  border-radius: 3px;
}

.wordmark {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 1.25rem;
  letter-spacing: -0.02em;
  color: #F4F1EA;
}

.hero-title {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: clamp(2.5rem, 7vw, 3.8rem);
  line-height: 1;
  letter-spacing: -0.035em;
  color: #FFFFFF;
  margin-top: 8px;
}

.stApp .hero-sub {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  color: rgba(244, 241, 234, 0.78);
  font-size: 0.96rem;
  font-weight: 500;
  margin: 8px 0 14px;
}

.sub-text {
  line-height: 1.35;
}

.sub-pill {
  display: inline-block;
  flex-shrink: 0;
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 3px;
  padding: 2px 8px;
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: #F4F1EA;
}

.st-key-hero_top [data-testid="stHorizontalBlock"] {
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 0.5rem;
}

.st-key-hero_top [data-testid="stColumn"]:first-child {
  flex: 1 1 auto !important;
  width: auto !important;
  min-width: 0 !important;
}

.st-key-hero_top [data-testid="stColumn"]:last-child {
  flex: 0 0 auto !important;
  width: auto !important;
  min-width: 0 !important;
}

.st-key-dark {
  display: flex;
  justify-content: flex-end;
  width: 100%;
}

.st-key-dark label {
  white-space: nowrap;
}

.stApp .st-key-dark label p {
  color: #FFFFFF;
  font-size: 0.88rem;
  font-weight: 600;
}

/* --- Sport Selection Buttons (Athletic Segmented Control) --- */
.st-key-sports_row [data-testid="stHorizontalBlock"] {
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  gap: 0.55rem;
}

.st-key-sports_row [data-testid="stColumn"] {
  flex: 1 1 0 !important;
  width: auto !important;
  min-width: 0 !important;
}

.st-key-topics [data-testid="stHorizontalBlock"] {
  flex-direction: row !important;
  flex-wrap: nowrap;
  gap: 0.45rem;
}

.st-key-topics [data-testid="stColumn"] {
  flex: 1 1 0 !important;
  width: auto !important;
  min-width: 0 !important;
}

.stApp .st-key-hero [class*="st-key-sp_"] button {
  width: 100%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 5px;
  min-height: 2.75rem;
  padding: 0 0.8rem;
  color: rgba(244, 241, 234, 0.88);
  box-shadow: none;
  transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
  cursor: pointer;
}

.stApp .st-key-hero [class*="st-key-sp_"] button > div {
  gap: 0.5rem;
  justify-content: center;
}

.stApp .st-key-hero [class*="st-key-sp_"] button p {
  color: rgba(244, 241, 234, 0.88);
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 0.94rem;
  letter-spacing: -0.01em;
}

.stApp .st-key-hero [class*="st-key-sp_"] button:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.36);
}

.stApp .st-key-hero [class*="st-key-sp_"] button:hover p {
  color: #FFFFFF;
}

/* --- Topic Tabs Bar --- */
.st-key-topics {
  margin-top: 14px;
  padding-top: 4px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.stApp .st-key-hero [class*="st-key-tp_"] button {
  width: 100%;
  background: transparent !important;
  border: none;
  border-radius: 0;
  border-bottom: 2.5px solid transparent;
  min-height: 2.65rem;
  padding: 0 0.4rem;
  transition: border-color 0.15s ease, color 0.15s ease, background-color 0.15s ease;
  cursor: pointer;
}

.stApp .st-key-hero [class*="st-key-tp_"] button p {
  color: rgba(244, 241, 234, 0.65);
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 0.92rem;
  letter-spacing: 0.01em;
}

.stApp .st-key-hero [class*="st-key-tp_"] button:hover {
  background: rgba(255, 255, 255, 0.05) !important;
}

.stApp .st-key-hero [class*="st-key-tp_"] button:hover p {
  color: #FFFFFF;
}

/* --- Empty States (Playbook Index Card) --- */
.empty {
  background: var(--panel);
  border: 1px solid var(--line);
  border-top: 2.5px solid var(--accent);
  border-radius: 6px;
  padding: 20px 24px;
  margin: 6px 0 14px;
  box-shadow: var(--card-shadow);
  position: relative;
}

.empty-badge {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent-text);
  background: transparent;
  border: 1px solid var(--accent);
  padding: 2px 7px;
  border-radius: 3px;
  margin-bottom: 8px;
}

.empty-title {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 1.5rem;
  line-height: 1.18;
  color: var(--ink);
  letter-spacing: -0.025em;
}

.empty p {
  color: var(--muted);
  margin: 6px 0 0;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* Starter Question Cards (Tactile Playbook Index Keys) */
.stApp .st-key-starters button {
  width: 100%;
  justify-content: flex-start;
  text-align: left;
  min-height: 4.1rem;
  padding: 0.8rem 1.15rem;
  border: 1.5px solid var(--line);
  border-left: 3px solid var(--input-border);
  background: var(--panel);
  border-radius: 6px;
  box-shadow: none;
  transition: border-color 0.15s ease, background-color 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
  cursor: pointer;
}

.stApp .st-key-starters button p {
  color: var(--ink);
  font-size: 0.95rem;
  font-weight: 600;
  line-height: 1.4;
  text-align: left;
}

.stApp .st-key-starters button:hover {
  border-color: var(--accent);
  border-left-color: var(--accent);
  background: var(--panel-hover);
  transform: translate(-1.5px, -1.5px);
  box-shadow: 3px 3px 0 var(--accent);
}

.stApp .st-key-starters button:active {
  transform: translate(0, 0);
  box-shadow: none;
}

.stApp .st-key-starters button:hover p {
  color: var(--accent-text);
}

/* Quiz CTA Button (Architectural Press Plate) */
.st-key-startquiz button {
  background: var(--accent);
  border: 1.5px solid var(--accent-edge);
  border-radius: 6px;
  min-height: 3.1rem;
  padding: 0 1.6rem;
  box-shadow: 0 3px 0 var(--accent-edge);
  transition: background-color 0.15s ease, transform 0.12s ease, box-shadow 0.12s ease;
  cursor: pointer;
}

.st-key-startquiz button p {
  color: #FFFFFF;
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 1.02rem;
  letter-spacing: -0.01em;
}

.st-key-startquiz button span[data-testid="stIconMaterial"] {
  color: #FFFFFF !important;
}

.st-key-startquiz button:hover {
  background: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 0 var(--accent-edge);
}

.st-key-startquiz button:active {
  transform: translateY(2px);
  box-shadow: 0 1px 0 var(--accent-edge);
}

[data-testid="stElementContainer"]:has(.cs-script-host) {
  display: none !important;
  margin: 0 !important;
  padding: 0 !important;
}

/* --- Chat Messages & Avatars (Editorial Briefing Sheets) --- */
[data-testid="stChatMessage"] {
  border-radius: 6px;
  padding: 16px 20px;
  margin-bottom: 14px;
  background: var(--panel);
  border: 1px solid var(--line);
  border-top: 2px solid var(--accent);
  box-shadow: var(--card-shadow);
  line-height: 1.62;
}

[data-testid="stChatMessageContent"] > [data-testid="stVerticalBlock"] {
  gap: 0.55rem !important;
}

[data-testid="stChatMessageAvatarAssistant"] {
  background: var(--accent);
  border-radius: 5px;
  box-shadow: none;
}

[data-testid="stChatMessageAvatarAssistant"] * {
  color: #FFFFFF;
}

[data-testid="stChatMessageAvatarUser"] {
  display: none;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
[data-testid="stChatMessage"]:has(.cs-user-actions) {
  flex-direction: row-reverse;
  margin-left: auto;
  width: fit-content;
  max-width: 84%;
  background: var(--bubble-user);
  border: 1px solid var(--accent-edge);
  border-top: 1px solid var(--accent-edge);
  border-radius: 6px 6px 2px 6px;
  box-shadow: 2px 2px 0 var(--accent-edge);
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) li,
[data-testid="stChatMessage"]:has(.cs-user-actions) p,
[data-testid="stChatMessage"]:has(.cs-user-actions) li {
  color: #FFFFFF;
  font-weight: 500;
}

[data-testid="stChatMessage"] strong {
  color: var(--accent-text);
  font-weight: 700;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) strong,
[data-testid="stChatMessage"]:has(.cs-user-actions) strong {
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

.reply-ref {
  font-size: 0.8rem;
  line-height: 1.4;
  color: rgba(255, 255, 255, 0.92);
  background: rgba(0, 0, 0, 0.16);
  border-left: 2.5px solid rgba(255, 255, 255, 0.78);
  border-radius: 6px;
  padding: 5px 10px;
  margin-bottom: 8px;
  word-break: break-word;
}

/* User bubble inline Copy button */
.cs-user-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 6px;
}

.cs-user-copy {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(0, 0, 0, 0.16);
  border: 1px solid rgba(255, 255, 255, 0.32);
  border-radius: 4px;
  color: #FFFFFF;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 3px 9px;
  min-height: 25px;
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease;
}

.cs-user-copy:hover {
  background: rgba(255, 255, 255, 0.28);
  border-color: rgba(255, 255, 255, 0.55);
}

.cs-user-copy.is-done {
  background: rgba(255, 255, 255, 0.32);
  border-color: #FFFFFF;
}

.cs-ic {
  display: inline-block;
  width: 17px;
  height: 17px;
  flex-shrink: 0;
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}

.cs-user-copy .cs-ic {
  width: 13px;
  height: 13px;
}

/* Assistant Action Toolbar (Copy / Paste / Share icons) - sits below the response card */
.cs-actions-wrap {
  position: relative;
  margin: 0;
  padding: 0;
}

.cs-actions {
  display: flex;
  align-items: center;
  flex-wrap: nowrap;
  gap: 4px;
}

.cs-act-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: transparent;
  color: var(--muted);
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 5px 12px;
  min-height: 34px;
  font-family: var(--font-body);
  font-size: 0.82rem;
  font-weight: 600;
  line-height: 1;
  cursor: pointer;
  transition: color 0.15s ease, border-color 0.15s ease, background-color 0.15s ease, transform 0.15s ease;
}

.cs-act-btn:hover {
  color: var(--accent-text);
  border-color: var(--accent);
  background: var(--accent-light);
  transform: translateY(-1px);
}

.cs-act-btn.is-done {
  color: var(--accent-text);
  border-color: var(--accent);
  background: var(--accent-light);
}

.cs-act-btn svg {
  flex-shrink: 0;
}

/* Icon-only variant (base64 SVG icons are injected per-theme in get_css) */
.cs-act-btn.cs-icon-btn {
  position: relative;
  width: 32px;
  height: 32px;
  min-height: 32px;
  padding: 0;
  border-radius: 5px;
  border-color: transparent;
  background: transparent;
}

.cs-act-btn.cs-icon-btn:hover,
.cs-act-btn.cs-icon-btn.is-done {
  border-color: var(--input-border);
  background: var(--panel);
  color: var(--accent-text);
  transform: none;
}

.cs-act-btn.cs-icon-btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

/* Feedback tooltip ("Copied!", "Pasted!") for icon buttons */
.cs-icon-btn.is-done::after {
  content: attr(data-tip);
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  transform: translateX(-50%);
  background: var(--ink);
  color: var(--bg);
  font-size: 0.72rem;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 6px;
  white-space: nowrap;
  pointer-events: none;
  z-index: 70;
}

/* Let the share menu / tooltip overflow the toolbar's element containers */
[class*="st-key-tools_"],
[class*="st-key-tools_"] [data-testid="stElementContainer"],
[class*="st-key-tools_"] [data-testid="stHtml"] {
  overflow: visible !important;
}

/* Toolbar row beneath each assistant card */
[class*="st-key-tools_"] {
  margin: -8px 0 10px 6px;
  gap: 4px !important;
  align-items: center;
}

[class*="st-key-reply_btn_"] button {
  border-radius: 5px !important;
  border: 1px solid transparent !important;
  background: transparent !important;
  min-height: 32px !important;
  padding: 0 0.65rem !important;
  box-shadow: none !important;
  transition: border-color 0.15s ease, background-color 0.15s ease !important;
  cursor: pointer;
}

[class*="st-key-reply_btn_"] button p {
  color: var(--muted) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.74rem !important;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

[class*="st-key-reply_btn_"] button span[data-testid="stIconMaterial"] {
  color: var(--muted) !important;
  font-size: 0.95rem !important;
}

[class*="st-key-reply_btn_"] button:hover {
  border-color: var(--input-border) !important;
  background: var(--panel) !important;
}

[class*="st-key-reply_btn_"] button:hover p,
[class*="st-key-reply_btn_"] button:hover span[data-testid="stIconMaterial"] {
  color: var(--accent-text) !important;
}

/* Share Menu (floating dropdown under the share icon) */
.cs-share-menu {
  display: none;
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  z-index: 60;
  width: max-content;
  max-width: min(92vw, 420px);
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  padding: 8px 10px;
  border-radius: 12px;
  background: var(--panel);
  border: 1px solid var(--line);
  box-shadow: var(--card-shadow-hover);
}

.cs-share-menu.is-open {
  display: flex;
}

.cs-share-item {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 5px 11px;
  min-height: 32px;
  border-radius: 8px;
  border: 1px solid var(--line);
  background: var(--panel);
  color: var(--ink) !important;
  text-decoration: none !important;
  font-family: var(--font-body);
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: border-color 0.15s ease, color 0.15s ease, background-color 0.15s ease;
}

.cs-share-item:hover,
.cs-share-item.is-done {
  border-color: var(--accent);
  color: var(--accent-text) !important;
  background: var(--accent-light);
}

/* --- Markdown Tables (Sports Stat Comparisons) --- */
.stMarkdown table {
  border-collapse: separate;
  border-spacing: 0;
  width: 100%;
  margin: 12px 0;
  font-size: 0.92rem;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid var(--line);
  box-shadow: none;
}

.stMarkdown th {
  background: var(--hero);
  color: #F4F1EA;
  text-align: left;
  padding: 9px 14px;
  font-family: var(--font-mono);
  font-weight: 600;
  font-size: 0.74rem;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  border-bottom: 2px solid var(--accent);
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

/* --- Follow-Up Section, Quick Chips & Inline Reply Prompt --- */
.followup-label {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 6px 0 4px;
}

.st-key-qa_ai_followup button {
  width: 100%;
  justify-content: flex-start;
  text-align: left;
  border-radius: 5px;
  border: 1.5px solid var(--accent);
  background: var(--accent-light);
  padding: 0.45rem 0.9rem;
  min-height: 2.5rem;
  margin-bottom: 2px;
  transition: background-color 0.15s ease, transform 0.12s ease, box-shadow 0.12s ease;
  cursor: pointer;
}

.st-key-qa_ai_followup button p {
  color: var(--accent-text);
  font-weight: 600;
  font-size: 0.88rem;
  text-align: left;
  white-space: normal;
  line-height: 1.35;
}

.st-key-qa_ai_followup button:hover {
  background: var(--accent);
  border-color: var(--accent-edge);
  transform: translate(-1px, -1px);
  box-shadow: 2px 2px 0 var(--accent-edge);
}

.st-key-qa_ai_followup button:hover p {
  color: #FFFFFF;
}

.st-key-qa_chips [data-testid="stHorizontalBlock"] {
  flex-direction: row !important;
  flex-wrap: wrap !important;
  gap: 0.45rem !important;
}

.st-key-qa_chips [data-testid="stColumn"] {
  flex: 1 1 135px !important;
  width: auto !important;
  min-width: 0 !important;
}

.stApp .st-key-qa_chips button {
  border-radius: 5px;
  border: 1px solid var(--input-border);
  background: var(--stripe);
  font-weight: 600;
  font-size: 0.84rem;
  padding: 0.35rem 0.85rem;
  min-height: 2.3rem;
  box-shadow: none;
  transition: background-color 0.15s ease, border-color 0.15s ease, transform 0.12s ease, box-shadow 0.12s ease;
  cursor: pointer;
}

.stApp .st-key-qa_chips button p {
  color: var(--ink);
  font-family: var(--font-display);
  font-size: 0.84rem;
  font-weight: 600;
}

.stApp .st-key-qa_chips button span[data-testid="stIconMaterial"] {
  color: var(--accent-text);
}

.stApp .st-key-qa_chips button:hover {
  background: var(--accent);
  border-color: var(--accent-edge);
  transform: translate(-1px, -1px);
  box-shadow: 2px 2px 0 var(--accent-edge);
}

.stApp .st-key-qa_chips button:hover p,
.stApp .st-key-qa_chips button:hover span[data-testid="stIconMaterial"] {
  color: #FFFFFF;
}

/* Inline Reply / Follow-Up Form inside Cards */
[class*="st-key-followup_box_"] {
  margin-top: 6px;
}

[class*="st-key-followup_box_"] [data-testid="stForm"] {
  border: none !important;
  padding: 0 !important;
  background: transparent !important;
}

[class*="st-key-followup_box_"] [data-testid="stHorizontalBlock"] {
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  align-items: center !important;
  gap: 0.5rem !important;
}

[class*="st-key-followup_box_"] [data-testid="stColumn"]:first-child {
  flex: 1 1 auto !important;
  width: auto !important;
  min-width: 0 !important;
}

[class*="st-key-followup_box_"] [data-testid="stColumn"]:last-child {
  flex: 0 0 auto !important;
  width: auto !important;
  min-width: 0 !important;
}

[class*="st-key-followup_box_"] [data-testid="stTextInputRootElement"],
[class*="st-key-followup_box_"] [data-baseweb="input"],
[class*="st-key-followup_box_"] [data-baseweb="base-input"] {
  background-color: var(--input-bg) !important;
  border: 1.5px solid var(--input-border) !important;
  border-radius: 6px !important;
  min-height: 2.6rem;
  transition: border-color 0.15s ease, box-shadow 0.15s ease, background-color 0.2s ease !important;
}

[class*="st-key-followup_box_"] [data-testid="stTextInputRootElement"]:focus-within,
[class*="st-key-followup_box_"] [data-baseweb="input"]:focus-within {
  border-color: var(--accent) !important;
  box-shadow: 0 2px 0 var(--accent) !important;
}

[class*="st-key-followup_box_"] input,
[class*="st-key-followup_box_"] [data-testid="stTextInputField"] {
  color: var(--ink) !important;
  background-color: transparent !important;
  caret-color: var(--accent) !important;
  font-size: 0.92rem !important;
}

[class*="st-key-followup_box_"] input::placeholder,
[class*="st-key-followup_box_"] [data-testid="stTextInputField"]::placeholder {
  color: var(--muted) !important;
  opacity: 0.9 !important;
}

[class*="st-key-followup_box_"] [data-testid="stFormSubmitButton"] button {
  background-color: var(--accent) !important;
  border: 1.5px solid var(--accent-edge) !important;
  border-radius: 6px !important;
  min-height: 2.6rem;
  padding: 0 1.05rem !important;
  color: #FFFFFF !important;
  white-space: nowrap;
  box-shadow: 0 2px 0 var(--accent-edge);
  transition: background-color 0.15s ease, transform 0.12s ease, box-shadow 0.12s ease !important;
  cursor: pointer;
}

[class*="st-key-followup_box_"] [data-testid="stFormSubmitButton"] button p {
  color: #FFFFFF !important;
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 0.9rem;
}

[class*="st-key-followup_box_"] [data-testid="stFormSubmitButton"] button span[data-testid="stIconMaterial"] {
  color: #FFFFFF !important;
}

[class*="st-key-followup_box_"] [data-testid="stFormSubmitButton"] button:hover {
  background-color: var(--accent-hover) !important;
  transform: translateY(-1px);
  box-shadow: 0 3px 0 var(--accent-edge);
}

[class*="st-key-followup_box_"] [data-testid="stFormSubmitButton"] button:active {
  transform: translateY(1px);
  box-shadow: none;
}

/* Earlier Message Reply Toggle Button */
[class*="st-key-reply_toggle_"] {
  margin-top: 4px;
}

[class*="st-key-reply_toggle_"] button {
  border-radius: 999px !important;
  border: 1px solid var(--line) !important;
  background: transparent !important;
  min-height: 2.1rem;
  padding: 0.2rem 0.85rem !important;
  transition: all 0.15s ease !important;
  cursor: pointer;
}

[class*="st-key-reply_toggle_"] button p,
[class*="st-key-reply_toggle_"] button span[data-testid="stIconMaterial"] {
  color: var(--muted) !important;
  font-size: 0.82rem;
  font-weight: 600;
}

[class*="st-key-reply_toggle_"] button:hover {
  border-color: var(--accent) !important;
  background: var(--accent-light) !important;
}

[class*="st-key-reply_toggle_"] button:hover p,
[class*="st-key-reply_toggle_"] button:hover span[data-testid="stIconMaterial"] {
  color: var(--accent-text) !important;
}

/* --- Reply Dialog (pop-up text box, portaled outside .stApp) --- */
[data-testid="stDialog"] > div,
div[role="dialog"] {
  background: var(--panel) !important;
  background-color: var(--panel) !important;
  color: var(--ink) !important;
  border: 1.5px solid var(--input-border) !important;
  border-top: 3px solid var(--accent) !important;
  border-radius: 8px !important;
  box-shadow: var(--card-shadow-hover) !important;
}

[data-testid="stDialog"] [role="dialog"] {
  background: transparent !important;
  color: var(--ink) !important;
}

[data-testid="stDialog"] h1, [data-testid="stDialog"] h2, [data-testid="stDialog"] h3,
[data-testid="stDialog"] p, [data-testid="stDialog"] label, [data-testid="stDialog"] span,
div[role="dialog"] h1, div[role="dialog"] h2, div[role="dialog"] h3,
div[role="dialog"] p, div[role="dialog"] label, div[role="dialog"] span {
  color: var(--ink);
}

[data-testid="stDialog"] h2,
div[role="dialog"] h2 {
  font-family: var(--font-display) !important;
  font-weight: 700 !important;
  letter-spacing: -0.02em;
}

[data-testid="stDialog"] button[aria-label="Close"],
div[role="dialog"] button[aria-label="Close"] {
  background: transparent !important;
  color: var(--muted) !important;
}

[data-testid="stDialog"] button[aria-label="Close"]:hover,
div[role="dialog"] button[aria-label="Close"]:hover {
  color: var(--ink) !important;
}

[data-testid="stDialog"] button[aria-label="Close"] svg,
div[role="dialog"] button[aria-label="Close"] svg {
  color: inherit !important;
  stroke: currentColor !important;
}

.reply-quote {
  font-size: 0.84rem;
  line-height: 1.45;
  color: var(--ink-secondary);
  background: var(--stripe);
  border-left: 3px solid var(--accent);
  border-radius: 8px;
  padding: 8px 12px;
  margin-bottom: 4px;
  word-break: break-word;
}

/* --- Button-based Quiz --- */
.quiz-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 4px 2px 8px;
}

.quiz-count {
  font-family: var(--font-mono);
  font-weight: 600;
  font-size: 0.78rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
}

.quiz-score {
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 0.78rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--accent-text);
  background: var(--accent-light);
  padding: 3px 10px;
  border-radius: 999px;
}

.quiz-progress {
  height: 5px;
  border-radius: 2px;
  background: var(--line);
  overflow: hidden;
  margin-bottom: 14px;
}

.quiz-progress > div {
  height: 100%;
  border-radius: 2px;
  background: var(--accent);
  transition: width 0.3s ease;
}

.quiz-card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-top: 2.5px solid var(--accent);
  border-radius: 6px;
  padding: 20px 22px;
  margin-bottom: 14px;
  box-shadow: var(--card-shadow);
  position: relative;
}

.quiz-q {
  font-family: var(--font-display);
  font-size: 1.18rem;
  font-weight: 600;
  letter-spacing: -0.015em;
  line-height: 1.42;
  color: var(--ink);
}

.stApp .st-key-quiz_opts button {
  width: 100%;
  justify-content: flex-start;
  text-align: left;
  min-height: 3.3rem;
  padding: 0.7rem 1.05rem;
  border: 1.5px solid var(--line);
  background: var(--panel);
  border-radius: 6px;
  box-shadow: none;
  transition: border-color 0.14s ease, background-color 0.14s ease, transform 0.12s ease, box-shadow 0.12s ease;
  cursor: pointer;
}

.stApp .st-key-quiz_opts button p {
  color: var(--ink);
  font-size: 0.96rem;
  font-weight: 600;
  line-height: 1.35;
  text-align: left;
  white-space: normal;
}

.stApp .st-key-quiz_opts button:hover {
  border-color: var(--accent);
  background: var(--panel-hover);
  transform: translate(-1.5px, -1.5px);
  box-shadow: 3px 3px 0 var(--accent);
}

.stApp .st-key-quiz_opts button:active {
  transform: translate(0, 0);
  box-shadow: none;
}

.stApp .st-key-quiz_opts button:hover p {
  color: var(--accent-text);
}

.quiz-opts-done {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.6rem;
  margin-bottom: 12px;
}

.quiz-opt {
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 3.3rem;
  padding: 0.7rem 1.05rem;
  border: 1.5px solid var(--line);
  border-radius: 6px;
  background: var(--panel);
  color: var(--muted);
  font-size: 0.96rem;
  font-weight: 600;
  line-height: 1.35;
  opacity: 0.72;
}

.quiz-letter {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 4px;
  background: var(--stripe);
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--ink-secondary);
}

.quiz-opt.correct {
  opacity: 1;
  color: var(--ink);
  border-color: #16A34A;
  background: rgba(22, 163, 74, 0.1);
}

.quiz-opt.correct .quiz-letter {
  background: #16A34A;
  color: #FFFFFF;
}

.quiz-opt.wrong {
  opacity: 1;
  color: var(--ink);
  border-color: #DC2626;
  background: rgba(220, 38, 38, 0.1);
}

.quiz-opt.wrong .quiz-letter {
  background: #DC2626;
  color: #FFFFFF;
}

.quiz-feedback {
  border-radius: 6px;
  padding: 12px 15px;
  margin-bottom: 12px;
  font-size: 0.94rem;
  line-height: 1.5;
  color: var(--ink);
  border: 1px solid;
}

.quiz-feedback.correct {
  background: rgba(22, 163, 74, 0.08);
  border-color: rgba(22, 163, 74, 0.45);
}

.quiz-feedback.wrong {
  background: rgba(220, 38, 38, 0.08);
  border-color: rgba(220, 38, 38, 0.45);
}

.quiz-feedback.correct strong { color: #16A34A; }
.quiz-feedback.wrong strong { color: #DC2626; }

.st-key-quiz_next button,
.st-key-quiz_results button,
.st-key-quiz_again button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: var(--accent) !important;
  border: 1.5px solid var(--accent-edge) !important;
  border-radius: 6px;
  min-height: 3rem;
  box-shadow: 0 3px 0 var(--accent-edge);
  transition: background-color 0.15s ease, transform 0.12s ease, box-shadow 0.12s ease;
  cursor: pointer;
}

.st-key-quiz_next button p,
.st-key-quiz_results button p,
.st-key-quiz_again button p {
  color: #FFFFFF !important;
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 1rem;
  letter-spacing: -0.01em;
}

/* Custom SVG forward-arrow logo on the Next Question button (URI injected in get_css) */
.st-key-quiz_next button::after {
  content: "";
  display: inline-block;
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
  transition: transform 0.18s ease;
}

.st-key-quiz_next button:hover::after {
  transform: translateX(3px);
}

/* Custom SVG flag logo on the See Results button (URI injected in get_css) */
.st-key-quiz_results button::before {
  content: "";
  display: inline-block;
  width: 19px;
  height: 19px;
  flex-shrink: 0;
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}

.st-key-quiz_again button span[data-testid="stIconMaterial"] {
  color: #FFFFFF !important;
}

.st-key-quiz_next button:hover,
.st-key-quiz_results button:hover,
.st-key-quiz_again button:hover {
  background: var(--accent-hover) !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 0 var(--accent-edge);
}

.st-key-quiz_next button:active,
.st-key-quiz_results button:active,
.st-key-quiz_again button:active {
  transform: translateY(2px);
  box-shadow: 0 1px 0 var(--accent-edge);
}

.st-key-quiz_back button {
  border-radius: 6px;
  min-height: 3rem;
  border: 1.5px solid var(--input-border) !important;
  background: var(--panel) !important;
  box-shadow: 0 2px 0 var(--line);
  transition: border-color 0.15s ease, transform 0.12s ease, box-shadow 0.12s ease;
}

.st-key-quiz_back button:hover {
  border-color: var(--accent) !important;
  transform: translateY(-1px);
  box-shadow: 0 3px 0 var(--accent);
}

.st-key-quiz_back button p {
  color: var(--ink) !important;
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 1rem;
  letter-spacing: -0.01em;
}

.st-key-quiz_back button span[data-testid="stIconMaterial"] {
  color: var(--ink) !important;
}

.quiz-result {
  text-align: center;
  background: var(--panel);
  border: 1px solid var(--line);
  border-top: 3px solid var(--accent);
  border-radius: 6px;
  padding: 26px 24px 20px;
  margin: 6px 0 14px;
  box-shadow: var(--card-shadow);
}

.quiz-result-score {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 3.8rem;
  letter-spacing: -0.04em;
  line-height: 1;
  color: var(--accent-text);
  margin: 6px 0 4px;
}

.quiz-result-score span {
  font-size: 1.6rem;
  color: var(--muted);
  margin-left: 6px;
}

.quiz-result p {
  color: var(--ink-secondary);
  font-weight: 600;
  margin: 0;
}

.quiz-review {
  padding: 8px 12px;
  margin-bottom: 8px;
  border-radius: 10px;
  border-left: 3px solid;
  font-size: 0.9rem;
  color: var(--ink);
}

.quiz-review.correct { border-color: #22C55E; background: rgba(34, 197, 94, 0.08); }
.quiz-review.wrong { border-color: #EF4444; background: rgba(239, 68, 68, 0.08); }
.quiz-review-q { font-weight: 700; margin-bottom: 2px; }

[data-testid="stExpander"] details {
  background: var(--panel);
  border: 1px solid var(--line) !important;
  border-radius: 12px;
}

[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {
  color: var(--ink) !important;
}

@media (max-width: 640px) {
  .quiz-opts-done { grid-template-columns: 1fr; }
  .quiz-result-score { font-size: 3.2rem; }
}

/* --- Composer Input --- */
[data-testid="stBottom"] {
  background: transparent !important;
}

[data-testid="stBottom"] > div {
  background: var(--bottom-fade) !important;
  transition: background 0.25s ease;
}

[data-testid="stBottomBlockContainer"] {
  background: transparent !important;
  max-width: 880px !important;
  padding-top: 0.75rem !important;
  padding-bottom: 1.35rem !important;
}

[data-testid="stChatInput"] {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

[data-testid="stChatInput"] > div {
  background-color: var(--input-bg) !important;
  border: 1.5px solid var(--input-border) !important;
  border-radius: 8px !important;
  padding: 9px 12px !important;
  box-shadow: 0 2px 0 var(--line) !important;
  transition: background-color 0.2s ease, border-color 0.15s ease, box-shadow 0.15s ease !important;
}

[data-testid="stChatInput"] > div:hover {
  border-color: var(--muted) !important;
}

[data-testid="stChatInput"] > div:focus-within {
  border-color: var(--accent) !important;
  box-shadow: 0 3px 0 var(--accent) !important;
}

/* Compatibility with older BaseWeb chat input wrappers */
[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="base-input"] {
  background-color: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

[data-testid="stChatInput"] textarea,
[data-testid="stChatInputTextArea"] {
  color: var(--ink) !important;
  background-color: transparent !important;
  caret-color: var(--accent) !important;
  font-family: var(--font-body) !important;
  font-size: 0.96rem !important;
  line-height: 1.5 !important;
}

[data-testid="stChatInput"] textarea::placeholder,
[data-testid="stChatInputTextArea"]::placeholder {
  color: var(--muted) !important;
  opacity: 0.9 !important;
}

[data-testid="stChatInput"] textarea:disabled,
[data-testid="stChatInputTextArea"]:disabled {
  color: var(--muted) !important;
  -webkit-text-fill-color: var(--muted) !important;
}

/* File upload (+) button */
[data-testid="stChatInputFileUploadButton"] button {
  color: var(--muted) !important;
  background-color: transparent !important;
  border-radius: 5px !important;
  width: 2.05rem;
  height: 2.05rem;
  transition: color 0.15s ease, background-color 0.15s ease !important;
}

[data-testid="stChatInputFileUploadButton"] button:hover:not(:disabled) {
  color: var(--accent-text) !important;
  background-color: var(--input-hover-bg) !important;
}

[data-testid="stChatInputFileUploadButton"] button:disabled {
  color: var(--input-btn-disabled-fg) !important;
  background-color: transparent !important;
}

/* Submit & Stop buttons */
[data-testid="stChatInputSubmitButton"],
[data-testid="stChatInputStopButton"] {
  border-radius: 6px !important;
  transition: background-color 0.15s ease, color 0.15s ease, transform 0.12s ease !important;
}

[data-testid="stChatInputSubmitButton"]:not(:disabled),
[data-testid="stChatInputStopButton"]:not(:disabled) {
  background-color: var(--accent) !important;
  color: #FFFFFF !important;
  box-shadow: 0 2px 0 var(--accent-edge) !important;
}

[data-testid="stChatInputSubmitButton"]:not(:disabled):hover,
[data-testid="stChatInputStopButton"]:not(:disabled):hover {
  background-color: var(--accent-hover) !important;
  color: #FFFFFF !important;
  transform: translateY(-1px);
  box-shadow: 0 3px 0 var(--accent-edge) !important;
}

[data-testid="stChatInputSubmitButton"]:disabled,
[data-testid="stChatInputStopButton"]:disabled {
  background-color: var(--input-btn-disabled-bg) !important;
  color: var(--input-btn-disabled-fg) !important;
  box-shadow: none !important;
}

[data-testid="stChatInput"] button svg {
  fill: currentColor;
}

/* Attached file chips & instructions inside chat input */
[data-testid="stChatInput"] [data-testid="stFileChip"]:not([aria-invalid="true"]) {
  background-color: var(--input-chip-bg) !important;
  border: 1px solid var(--input-border) !important;
  border-radius: 10px !important;
  color: var(--ink) !important;
}

[data-testid="stChatInput"] [data-testid="stFileChip"]:not([aria-invalid="true"]) [data-testid="stFileChipName"] {
  color: var(--ink) !important;
}

[data-testid="stChatInput"] [data-testid="stFileChip"]:not([aria-invalid="true"]) small {
  color: var(--muted) !important;
}

[data-testid="stChatInput"] [data-testid="stFileChipDeleteBtn"] button {
  color: var(--muted) !important;
  background-color: transparent !important;
}

[data-testid="stChatInput"] [data-testid="stFileChipDeleteBtn"] button:hover {
  color: var(--accent-text) !important;
  background-color: var(--input-hover-bg) !important;
}

[data-testid="stChatInput"] .stChatInputInstructions {
  color: var(--muted) !important;
}

/* --- Selectbox / Model dropdown (theme-aware) ---
   Streamlit >= 1.5x renders st.selectbox with React Aria (not BaseWeb), so we target
   the stable test ids and ARIA roles. The config.toml base theme is light, which is why
   these need !important to win over Streamlit's emotion styles in dark mode. */
.stApp [data-testid="stSelectbox"] div:has(> input[role="combobox"]) {
  background-color: var(--input-bg) !important;
  border: 1.5px solid var(--input-border) !important;
  border-radius: 6px !important;
  box-shadow: none !important;
  cursor: pointer;
  transition: border-color 0.15s ease, box-shadow 0.15s ease, background-color 0.2s ease;
}

.stApp [data-testid="stSelectbox"] div:has(> input[role="combobox"]):hover {
  border-color: var(--accent) !important;
}

.stApp [data-testid="stSelectbox"] div:has(> input[role="combobox"])[data-focus-within],
.stApp [data-testid="stSelectbox"] div:has(> input[role="combobox"]):focus-within,
.stApp [data-testid="stSelectbox"] div:has(> input[aria-expanded="true"]) {
  border-color: var(--accent) !important;
  box-shadow: 0 2px 0 var(--accent) !important;
}

.stApp [data-testid="stSelectbox"] input[role="combobox"] {
  background: transparent !important;
  color: var(--ink) !important;
  -webkit-text-fill-color: var(--ink) !important;
  caret-color: var(--accent) !important;
  font-family: var(--font-body);
}

.stApp [data-testid="stSelectbox"] input[role="combobox"]::placeholder {
  color: var(--muted) !important;
  -webkit-text-fill-color: var(--muted) !important;
}

.stApp [data-testid="stSelectbox"] button {
  background: transparent !important;
  color: var(--muted) !important;
}

.stApp [data-testid="stSelectbox"] button:hover {
  color: var(--accent-text) !important;
}

.stApp [data-testid="stSelectbox"] button svg {
  color: inherit !important;
  fill: currentColor !important;
}

/* Dropdown menu (portaled outside .stApp, so no .stApp prefix) */
[data-testid="stSelectboxVirtualDropdown"] {
  background-color: var(--panel) !important;
  border: 1px solid var(--input-border) !important;
  border-radius: 12px !important;
  box-shadow: var(--card-shadow-hover) !important;
  color: var(--ink) !important;
  overflow: hidden;
}

[data-testid="stSelectboxVirtualDropdown"] [role="listbox"] {
  background-color: var(--panel) !important;
  scrollbar-color: var(--input-border) transparent;
}

[data-testid="stSelectboxVirtualDropdown"] [role="option"] {
  background-color: transparent !important;
  color: var(--ink) !important;
  font-family: var(--font-body);
}

[data-testid="stSelectboxVirtualDropdown"] [role="option"] * {
  color: inherit !important;
}

[data-testid="stSelectboxVirtualDropdown"] [role="option"] [data-item-hl] {
  border-radius: 8px;
  transition: background-color 0.15s ease;
}

[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-hovered] [data-item-hl],
[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-focused] [data-item-hl],
[data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover [data-item-hl] {
  background-color: var(--input-hover-bg) !important;
}

[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-selected],
[data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"] {
  color: var(--accent-text) !important;
  font-weight: 700;
}

[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-selected] [data-item-hl],
[data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"] [data-item-hl] {
  background-color: var(--accent-light) !important;
}

[data-testid="stSelectboxVirtualDropdown"] [role="listbox"]::-webkit-scrollbar { width: 8px; }
[data-testid="stSelectboxVirtualDropdown"] [role="listbox"]::-webkit-scrollbar-thumb {
  background: var(--input-border);
  border-radius: 8px;
}

/* --- Sidebar Styling --- */
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
  font-family: var(--font-display);
  font-weight: 700;
  letter-spacing: -0.02em;
  font-size: 1.25rem;
  color: var(--ink);
}

.sidebar-header {
  margin-bottom: 0.5rem;
}

.sidebar-badge {
  display: inline-block;
  font-size: 0.66rem;
  font-weight: 600;
  font-family: var(--font-mono);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  background: var(--accent-light);
  color: var(--accent-text);
  padding: 2px 7px;
  border-radius: 4px;
}

[data-testid="stSidebar"] .stDownloadButton > button {
  border-radius: 6px;
  border: 1.5px solid var(--accent);
  background: transparent;
  transition: background-color 0.15s ease, transform 0.12s ease, box-shadow 0.12s ease;
  cursor: pointer;
}

[data-testid="stSidebar"] .stDownloadButton > button p {
  color: var(--accent-text);
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 0.92rem;
  letter-spacing: -0.01em;
}

[data-testid="stSidebar"] .stDownloadButton > button:hover {
  background: var(--accent);
  border-color: var(--accent-edge);
  transform: translate(-1px, -1px);
  box-shadow: 2px 2px 0 var(--accent-edge);
}

[data-testid="stSidebar"] .stDownloadButton > button:hover p {
  color: #FFFFFF;
}

[data-testid="stSidebar"] .stButton > button {
  border-radius: 6px;
  border: 1.5px solid var(--input-border);
  background: var(--panel);
  color: var(--ink);
  transition: border-color 0.15s ease, background-color 0.15s ease, transform 0.12s ease, box-shadow 0.12s ease;
  cursor: pointer;
}

[data-testid="stSidebar"] .stButton > button p {
  color: var(--ink);
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 0.92rem;
  letter-spacing: -0.01em;
}

[data-testid="stSidebar"] .stButton > button:hover {
  border-color: var(--accent);
  background: var(--panel-hover);
  transform: translate(-1px, -1px);
  box-shadow: 2px 2px 0 var(--accent);
}

[data-testid="stSidebar"] .stButton > button:hover p {
  color: var(--accent-text);
}

/* --- Tablet & Mobile Responsiveness --- */
@media (max-width: 768px) {
  .block-container {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  .st-key-hero {
    padding: 18px 20px 10px;
  }
}

@media (max-width: 640px) {
  .block-container {
    padding-top: 0.75rem;
    padding-bottom: 6.5rem;
    padding-left: 0.85rem;
    padding-right: 0.85rem;
  }
  .st-key-hero {
    padding: 16px 16px 10px;
    border-radius: 16px;
    margin-bottom: 12px;
  }
  .hero-title {
    font-size: 2.65rem;
  }
  .stApp .hero-sub {
    font-size: 0.94rem;
    margin: 6px 0 12px;
  }
  .stApp .st-key-hero [class*="st-key-sp_"] button {
    padding: 0 0.4rem;
    min-height: 2.75rem;
  }
  .stApp .st-key-hero [class*="st-key-sp_"] button p {
    font-size: 0.98rem;
  }
  .stApp .st-key-hero [class*="st-key-tp_"] button {
    min-height: 2.65rem;
  }
  .stApp .st-key-hero [class*="st-key-tp_"] button p {
    font-size: 0.98rem;
  }
  .empty {
    padding: 18px 18px;
    border-radius: 14px;
  }
  .empty-title {
    font-size: 1.5rem;
  }
  [data-testid="stChatMessage"] {
    padding: 14px 14px;
    border-radius: 14px;
  }
  [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    max-width: 90%;
    padding: 12px 14px;
  }
  .stMarkdown table {
    display: block;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    white-space: nowrap;
  }
  .cs-act-btn {
    min-height: 38px;
    padding: 6px 12px;
  }
  .cs-act-btn.cs-icon-btn {
    width: 38px;
    height: 38px;
    min-height: 38px;
    padding: 0;
  }
  .cs-share-item {
    min-height: 36px;
    padding: 6px 12px;
  }
  .st-key-qa_chips [data-testid="stColumn"] {
    flex: 1 1 calc(50% - 0.5rem) !important;
    min-width: 120px !important;
  }
  [class*="st-key-followup_box_"] [data-testid="stFormSubmitButton"] button {
    padding: 0 0.8rem !important;
  }
  .stApp .st-key-starters button {
    min-height: 3.7rem;
    padding: 0.75rem 0.95rem;
  }
  [data-testid="stBottomBlockContainer"] {
    padding-left: 0.85rem !important;
    padding-right: 0.85rem !important;
    padding-bottom: 1rem !important;
  }
  [data-testid="stChatInput"] > div {
    border-radius: 15px !important;
    padding: 8px 12px !important;
  }
}

@media (max-width: 480px) {
  .st-key-topics [data-testid="stHorizontalBlock"] {
    flex-wrap: wrap !important;
    gap: 0.35rem !important;
  }
  .st-key-topics [data-testid="stColumn"] {
    flex: 1 1 calc(50% - 0.35rem) !important;
    min-width: calc(50% - 0.35rem) !important;
  }
  .st-key-sports_row button span[data-testid="stIconMaterial"] {
    display: none;
  }
  .wordmark {
    font-size: 1.25rem;
  }
}

@media (max-width: 390px) {
  .wordmark-badge {
    display: none;
  }
  .stApp .st-key-dark label p {
    font-size: 0.82rem;
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


_ICON_SHAPES = {
    "copy": "<rect x='9' y='9' width='13' height='13' rx='2' ry='2'/><path d='M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1'/>",
    "paste": "<path d='M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2'/><rect x='8' y='2' width='8' height='4' rx='1' ry='1'/><path d='M9 12h6'/><path d='M9 16h6'/>",
    "share": "<circle cx='18' cy='5' r='3'/><circle cx='6' cy='12' r='3'/><circle cx='18' cy='19' r='3'/><line x1='8.59' y1='13.51' x2='15.42' y2='17.49'/><line x1='15.41' y1='6.51' x2='8.59' y2='10.49'/>",
    "check": "<polyline points='20 6 9 17 4 12'/>",
    "arrow": "<line x1='5' y1='12' x2='19' y2='12'/><polyline points='13 6 19 12 13 18'/>",
    "flag": "<path d='M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z'/><line x1='4' y1='22' x2='4' y2='15'/>",
}


def _svg_bg(name, stroke, width=2.2):
    svg = (
        f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' "
        f"stroke='{stroke}' stroke-width='{width}' stroke-linecap='round' stroke-linejoin='round'>"
        f"{_ICON_SHAPES[name]}</svg>"
    )
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f'url("data:image/svg+xml;base64,{b64}")'


def get_css(sport="Basketball", topic="Rules", dark=False):
    mode = "dark" if dark else "light"
    theme = {**BASE[mode], **THEMES.get(sport, THEMES["Basketball"])[mode]}
    root = ":root{" + "".join(f"--{k}:{v};" for k, v in theme.items()) + "}"
    art = ART.get(sport, ART["Basketball"])
    hero_bg = (
        ".st-key-hero{"
        "background-image:linear-gradient(105deg,var(--hero-start) 48%,var(--hero-end) 100%),"
        "url(\"data:image/svg+xml," + quote(art) + "\");"
        "background-size:100% 100%,auto 130%;"
        "background-position:0 0,right -28px center;"
        "background-repeat:no-repeat;}"
    )
    m, acc = theme["muted"], theme["accent-text"]
    icons_css = (
        f".cs-ic-copy{{background-image:{_svg_bg('copy', m)};}}"
        f".cs-ic-paste{{background-image:{_svg_bg('paste', m)};}}"
        f".cs-ic-share{{background-image:{_svg_bg('share', m)};}}"
        f".cs-icon-btn:hover .cs-ic-copy{{background-image:{_svg_bg('copy', acc)};}}"
        f".cs-icon-btn:hover .cs-ic-paste{{background-image:{_svg_bg('paste', acc)};}}"
        f".cs-icon-btn:hover .cs-ic-share{{background-image:{_svg_bg('share', acc)};}}"
        f".cs-icon-btn.is-done .cs-ic{{background-image:{_svg_bg('check', acc, 2.6)};}}"
        f".cs-ic-copy-light{{background-image:{_svg_bg('copy', '#FFFFFF')};}}"
        f".cs-user-copy.is-done .cs-ic-copy-light{{background-image:{_svg_bg('check', '#FFFFFF', 2.6)};}}"
        f".st-key-quiz_next button::after{{background-image:{_svg_bg('arrow', '#FFFFFF', 2.6)};}}"
        f".st-key-quiz_results button::before{{background-image:{_svg_bg('flag', '#FFFFFF', 2.4)};}}"
    )
    sp = f".stApp .st-key-sp_{sport}"
    tp = f".stApp .st-key-tp_{topic}"
    active = (
        f"{sp} button,{sp} button:hover{{"
        f"background:var(--accent) !important;border-color:var(--accent) !important;color:#FFFFFF !important;"
        f"box-shadow:0 2px 0 var(--accent-edge) !important;}}"
        f"{sp} button p,{sp} button:hover p{{color:#FFFFFF !important;font-weight:700 !important;}}"
        f"{sp} button span[data-testid='stIconMaterial']{{color:#FFFFFF !important;}}"
        f"{tp} button{{"
        f"border-bottom-color:var(--accent) !important;background:rgba(255,255,255,0.06) !important;}}"
        f"{tp} button p{{color:#FFFFFF !important;font-weight:700 !important;}}"
        f"{tp} button span[data-testid='stIconMaterial']{{color:var(--accent) !important;}}"
    )
    font_links = (
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        f'<link rel="stylesheet" href="{FONT_URL}">'
    )
    font_import = f"@import url('{FONT_URL}');"
    # Keep <style> at column 0 of its own Markdown block (CommonMark Type 1 HTML block)
    # so blank lines inside CSS are never parsed as Markdown paragraphs.
    return "<style>" + font_import + root + CSS + hero_bg + icons_css + active + "</style>\n\n" + font_links
