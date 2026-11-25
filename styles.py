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
import html
from urllib.parse import quote

THEMES = {
    "Basketball": {
        "light": {
            "hero-start": "#D94F14",
            "hero-end": "#8F2D08",
            "hero": "#C2410C",
            "hero-scrim": "rgba(122, 35, 5, 0.72)",
            "hero-scrim-mid": "rgba(122, 35, 5, 0.26)",
            "bg-glow": "rgba(201, 74, 18, 0.11)",
            "bg-glow-soft": "rgba(201, 74, 18, 0.06)",
            "accent": "#C94A12",
            "accent-hover": "#A83B0B",
            "accent-edge": "#8C3008",
            "accent-text": "#B8400C",
            "accent-light": "rgba(201, 74, 18, 0.09)",
            "bubble-user": "#C94A12",
        },
        "dark": {
            "hero-start": "#B83E0C",
            "hero-end": "#661F05",
            "hero": "#9A3412",
            "hero-scrim": "rgba(74, 22, 4, 0.74)",
            "hero-scrim-mid": "rgba(74, 22, 4, 0.28)",
            "bg-glow": "rgba(232, 93, 26, 0.14)",
            "bg-glow-soft": "rgba(232, 93, 26, 0.07)",
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
            "hero-start": "#1D56C4",
            "hero-end": "#102E78",
            "hero": "#1846A3",
            "hero-scrim": "rgba(14, 38, 102, 0.72)",
            "hero-scrim-mid": "rgba(14, 38, 102, 0.26)",
            "bg-glow": "rgba(27, 75, 158, 0.11)",
            "bg-glow-soft": "rgba(27, 75, 158, 0.06)",
            "accent": "#1B4B9E",
            "accent-hover": "#153B7D",
            "accent-edge": "#0F2B5C",
            "accent-text": "#18448F",
            "accent-light": "rgba(27, 75, 158, 0.09)",
            "bubble-user": "#1B4B9E",
        },
        "dark": {
            "hero-start": "#17429E",
            "hero-end": "#0C2157",
            "hero": "#14357D",
            "hero-scrim": "rgba(10, 26, 72, 0.76)",
            "hero-scrim-mid": "rgba(10, 26, 72, 0.30)",
            "bg-glow": "rgba(59, 119, 232, 0.15)",
            "bg-glow-soft": "rgba(59, 119, 232, 0.07)",
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
            "hero-start": "#117A4B",
            "hero-end": "#08472A",
            "hero": "#0E663E",
            "hero-scrim": "rgba(7, 56, 33, 0.72)",
            "hero-scrim-mid": "rgba(7, 56, 33, 0.26)",
            "bg-glow": "rgba(20, 108, 67, 0.11)",
            "bg-glow-soft": "rgba(20, 108, 67, 0.06)",
            "accent": "#146C43",
            "accent-hover": "#0F5534",
            "accent-edge": "#0A3D25",
            "accent-text": "#115C39",
            "accent-light": "rgba(20, 108, 67, 0.09)",
            "bubble-user": "#146C43",
        },
        "dark": {
            "hero-start": "#0D613B",
            "hero-end": "#05331E",
            "hero": "#0A4F30",
            "hero-scrim": "rgba(5, 40, 23, 0.76)",
            "hero-scrim-mid": "rgba(5, 40, 23, 0.30)",
            "bg-glow": "rgba(34, 163, 102, 0.14)",
            "bg-glow-soft": "rgba(34, 163, 102, 0.07)",
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
        "bottom-fade": "linear-gradient(180deg, rgba(243, 239, 231, 0) 0%, rgba(243, 239, 231, 0.96) 18%, #F3EFE7 34%, #F3EFE7 100%)",
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
        "bottom-fade": "linear-gradient(180deg, rgba(14, 15, 17, 0) 0%, rgba(14, 15, 17, 0.96) 18%, #0E0F11 34%, #0E0F11 100%)",
        "card-shadow": "0 1px 3px rgba(0, 0, 0, 0.35)",
        "card-shadow-hover": "0 8px 24px rgba(0, 0, 0, 0.55)",
    },
}

# Court / pitch blueprint artwork - sport-specific regulation markings sized for the landscape option card
_STROKE = "fill='none' stroke='white' stroke-width='2.4' stroke-opacity='0.38' stroke-linecap='round' stroke-linejoin='round'"
ART = {
    "Basketball": (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 560 300'>"
        # Subtle hardwood court plank texture
        "<g stroke='white' stroke-width='1' stroke-opacity='0.08'>"
        "<path d='M18 46H542M18 81H542M18 115H542M18 150H542M18 185H542M18 219H542M18 254H542'/>"
        "</g>"
        # Shaded painted keys (free-throw lanes)
        "<rect x='18' y='105.5' width='106' height='89' fill='white' fill-opacity='0.09'/>"
        "<rect x='436' y='105.5' width='106' height='89' fill='white' fill-opacity='0.10'/>"
        "<circle cx='280' cy='150' r='34' fill='white' fill-opacity='0.06'/>"
        "<g " + _STROKE + ">"
        # Outer boundary & half-court line
        "<rect x='18' y='12' width='524' height='276' rx='4'/>"
        "<path d='M280 12V288'/>"
        "<circle cx='280' cy='150' r='34'/>"
        "<circle cx='280' cy='150' r='10'/>"
        # Right half-court: paint, free-throw circle (solid + dashed), lane hashes, 3pt arc, backboard & rim
        "<rect x='436' y='105.5' width='106' height='89'/>"
        "<path d='M436 116.5A33.5 33.5 0 0 0 436 183.5'/>"
        "<path d='M436 116.5A33.5 33.5 0 0 1 436 183.5' stroke-dasharray='6 6'/>"
        "<path d='M456 99V105.5M474 99V105.5M492 99V105.5M504 98V105.5"
        "M456 194.5V201M474 194.5V201M492 194.5V201M504 194.5V202'/>"
        "<path d='M542 29H460A132 132 0 0 0 460 271H542'/>"
        "<path d='M520 133V167' stroke-width='3'/>"
        "<circle cx='513' cy='150' r='6'/>"
        "<path d='M513 128A22 22 0 0 0 513 172'/>"
        # Left half-court (mirrored)
        "<rect x='18' y='105.5' width='106' height='89'/>"
        "<path d='M124 116.5A33.5 33.5 0 0 1 124 183.5'/>"
        "<path d='M124 116.5A33.5 33.5 0 0 0 124 183.5' stroke-dasharray='6 6'/>"
        "<path d='M104 99V105.5M86 99V105.5M68 99V105.5M56 98V105.5"
        "M104 194.5V201M86 194.5V201M68 194.5V201M56 194.5V202'/>"
        "<path d='M18 29H100A132 132 0 0 1 100 271H18'/>"
        "<path d='M40 133V167' stroke-width='3'/>"
        "<circle cx='47' cy='150' r='6'/>"
        "<path d='M47 128A22 22 0 0 1 47 172'/>"
        "</g></svg>"
    ),
    "Volleyball": (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 560 300'>"
        # Two-tone indoor Taraflex attack zone shading (3-meter front zones)
        "<rect x='36' y='28' width='488' height='244' fill='white' fill-opacity='0.04'/>"
        "<rect x='199' y='28' width='162' height='244' fill='white' fill-opacity='0.11'/>"
        "<g " + _STROKE + ">"
        # Outer sidelines & endlines
        "<rect x='36' y='28' width='488' height='244' rx='3'/>"
        # 3-meter attack lines (solid inside + official FIVB dashed sideline extensions)
        "<path d='M199 28V272M361 28V272'/>"
        "<path d='M199 7V26M199 274V293M361 7V26M361 274V293' stroke-dasharray='5 5'/>"
        # Service zone tick marks behind endlines
        "<path d='M22 28H30M22 272H30M530 28H538M530 272H538'/>"
        # Center net line, net mesh ticks, antennae & net posts
        "<path d='M280 12V288' stroke-width='4.6' stroke-opacity='0.52'/>"
        "<path d='M275 38H285M275 66H285M275 94H285M275 122H285M275 150H285"
        "M275 178H285M275 206H285M275 234H285M275 262H285' stroke-width='1.5' stroke-opacity='0.34'/>"
        "<circle cx='280' cy='12' r='5' fill='white' fill-opacity='0.45'/>"
        "<circle cx='280' cy='288' r='5' fill='white' fill-opacity='0.45'/>"
        "<circle cx='280' cy='28' r='2.8' fill='white' fill-opacity='0.55' stroke='none'/>"
        "<circle cx='280' cy='272' r='2.8' fill='white' fill-opacity='0.55' stroke='none'/>"
        "</g></svg>"
    ),
    "Football": (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 560 300'>"
        # Alternating mowed stadium grass pitch stripes
        "<g fill='white' fill-opacity='0.055'>"
        "<rect x='24' y='16' width='51.2' height='268'/>"
        "<rect x='126.4' y='16' width='51.2' height='268'/>"
        "<rect x='228.8' y='16' width='51.2' height='268'/>"
        "<rect x='331.2' y='16' width='51.2' height='268'/>"
        "<rect x='433.6' y='16' width='51.2' height='268'/>"
        "</g>"
        "<g " + _STROKE + ">"
        # Touchlines, goal lines & halfway line
        "<rect x='24' y='16' width='512' height='268' rx='3'/>"
        "<path d='M280 16V284'/>"
        # Center circle & kick-off spot
        "<circle cx='280' cy='150' r='44'/>"
        "<circle cx='280' cy='150' r='3.5' fill='white' fill-opacity='0.5' stroke='none'/>"
        # Corner quarter-circle arcs
        "<path d='M24 30A14 14 0 0 0 38 16M522 16A14 14 0 0 0 536 30"
        "M24 270A14 14 0 0 1 38 284M522 284A14 14 0 0 1 536 270'/>"
        # Penalty areas (18-yard boxes) & goal areas (6-yard boxes)
        "<rect x='24' y='71' width='86' height='158'/>"
        "<rect x='450' y='71' width='86' height='158'/>"
        "<rect x='24' y='112' width='32' height='76'/>"
        "<rect x='504' y='112' width='32' height='76'/>"
        # Goal frames
        "<rect x='14' y='132' width='10' height='36'/>"
        "<rect x='536' y='132' width='10' height='36'/>"
        # Penalty spots & penalty arcs ("D")
        "<circle cx='82' cy='150' r='3' fill='white' fill-opacity='0.5' stroke='none'/>"
        "<circle cx='478' cy='150' r='3' fill='white' fill-opacity='0.5' stroke='none'/>"
        "<path d='M110 116A44 44 0 0 1 110 184'/>"
        "<path d='M450 116A44 44 0 0 0 450 184'/>"
        "</g></svg>"
    ),
}

# Compact sport-specific court markings for each sport option button
_BTN_ART_SHAPES = {
    "Basketball": (
        "<path d='M118 4H86A42 42 0 0 0 86 76H118'/>"
        "<rect x='84' y='22' width='34' height='36'/>"
        "<path d='M84 26A14 14 0 0 0 84 54'/>"
        "<circle cx='108' cy='40' r='3.5'/>"
    ),
    "Volleyball": (
        "<rect x='16' y='8' width='98' height='64' rx='2'/>"
        "<path d='M65 2V78' stroke-width='3'/>"
        "<path d='M46 8V72M84 8V72'/>"
        "<path d='M46 3V7M46 73V77M84 3V7M84 73V77' stroke-dasharray='2 2'/>"
    ),
    "Football": (
        "<rect x='14' y='8' width='100' height='64' rx='2'/>"
        "<path d='M64 8V72'/>"
        "<circle cx='64' cy='40' r='14'/>"
        "<rect x='92' y='22' width='22' height='36'/>"
        "<path d='M92 31A12 12 0 0 0 92 49'/>"
    ),
}


def _sport_btn_bg(sport_name, stroke, opacity):
    svg = (
        f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 80' fill='none' "
        f"stroke='{stroke}' stroke-width='2' stroke-opacity='{opacity}' "
        f"stroke-linecap='round' stroke-linejoin='round'>"
        f"{_BTN_ART_SHAPES[sport_name]}</svg>"
    )
    return f'url("data:image/svg+xml,{quote(svg)}")'


# Seamless tactical playbook & sports motifs for the full-page backdrop
_PAGE_BG_SHAPES = {
    "Basketball": (
        # Basketball with curved panel seams
        "<circle cx='78' cy='82' r='26'/>"
        "<path d='M52 82H104M78 56V108'/>"
        "<path d='M60 63A24 24 0 0 1 60 101M96 63A24 24 0 0 0 96 101'/>"
        # Pick-and-roll chalkboard play (O's, defender X, screen T-bar, cut arrow & pass)
        "<circle cx='216' cy='112' r='7'/><circle cx='286' cy='116' r='7'/>"
        "<path d='M244 80L256 92M256 80L244 92'/>"
        "<path d='M220 102Q244 52 294 64'/><path d='M286 58L296 64L287 72'/>"
        "<path d='M225 113L276 115' stroke-dasharray='5 5'/>"
        "<path d='M254 106L266 86M258 82L274 90'/>"
        # Mini half-court key & 3-point arc
        "<path d='M42 292H144'/><rect x='74' y='246' width='38' height='46'/>"
        "<path d='M74 246A19 19 0 0 1 112 246'/>"
        "<path d='M48 292V264A45 45 0 0 1 138 264V292'/>"
        "<circle cx='93' cy='278' r='4'/>"
        # Backboard, rim & net
        "<rect x='244' y='214' width='56' height='36' rx='2'/>"
        "<rect x='262' y='230' width='20' height='14'/>"
        "<path d='M258 244H286' stroke-width='2.2'/>"
        "<path d='M260 244L265 272H279L284 244M263 254L281 264M281 254L263 264'/>"
        # Tactical alignment ticks
        "<path d='M174 180H186M180 174V186M10 180H22M16 174V186M174 16H186M180 10V22'/>"
    ),
    "Volleyball": (
        # Volleyball with curved 6-panel seams
        "<circle cx='78' cy='82' r='26'/>"
        "<path d='M55 70Q78 62 101 70M53 88Q78 80 103 88M78 56Q90 82 78 108M66 59Q72 82 64 104'/>"
        # Set-and-spike rotation play diagram
        "<circle cx='216' cy='112' r='7'/><circle cx='258' cy='72' r='7'/><circle cx='294' cy='112' r='7'/>"
        "<path d='M252 110L264 122M264 110L252 122'/>"
        "<path d='M222 106Q238 78 250 74' stroke-dasharray='5 5'/>"
        "<path d='M266 74Q288 78 302 102'/><path d='M294 98L303 104L304 93'/>"
        # Net mesh, posts & antennae
        "<path d='M40 232V292M146 232V292' stroke-width='2.2'/>"
        "<rect x='40' y='238' width='106' height='26'/>"
        "<path d='M40 247H146M40 255H146M58 238V264M76 238V264M94 238V264M112 238V264M130 238V264'/>"
        "<path d='M48 222V238M138 222V238' stroke-dasharray='3 3'/>"
        # Mini court with 3m attack lines & net
        "<rect x='228' y='224' width='92' height='54' rx='2'/>"
        "<path d='M274 218V284' stroke-width='2.2'/>"
        "<path d='M256 224V278M292 224V278'/>"
        "<path d='M256 219V223M256 279V283M292 219V223M292 279V283' stroke-dasharray='2 2'/>"
        # Tactical alignment ticks
        "<path d='M174 180H186M180 174V186M10 180H22M16 174V186M174 16H186M180 10V22'/>"
    ),
    "Football": (
        # Classic pentagon-panel football
        "<circle cx='78' cy='82' r='26'/>"
        "<polygon points='78,72 87,79 84,90 72,90 69,79'/>"
        "<path d='M78 72V56M87 79L103 74M84 90L94 103M72 90L62 103M69 79L53 74'/>"
        # Tactical formation & overlapping wing run
        "<circle cx='214' cy='112' r='7'/><circle cx='252' cy='72' r='7'/><circle cx='286' cy='114' r='7'/>"
        "<path d='M246 102L258 114M258 102L246 114'/>"
        "<path d='M222 106L246 79' stroke-dasharray='5 5'/>"
        "<path d='M286 104Q298 68 272 54'/><path d='M279 51L270 54L276 62'/>"
        # Goal frame, net & penalty area
        "<path d='M42 238H144'/><rect x='72' y='224' width='42' height='14'/>"
        "<path d='M82 224V238M93 224V238M104 224V238M72 231H114'/>"
        "<rect x='54' y='238' width='78' height='40'/><rect x='72' y='238' width='42' height='18'/>"
        "<circle cx='93' cy='265' r='2'/>"
        "<path d='M77 278A22 22 0 0 0 109 278'/>"
        # Center circle & corner flag
        "<path d='M232 252H318'/><circle cx='275' cy='252' r='24'/><circle cx='275' cy='252' r='2.5'/>"
        "<path d='M304 218V238M304 218L318 223L304 228'/>"
        # Tactical alignment ticks
        "<path d='M174 180H186M180 174V186M10 180H22M16 174V186M174 16H186M180 10V22'/>"
    ),
}


def _page_bg_tile(sport_name, stroke, opacity):
    shapes = _PAGE_BG_SHAPES.get(sport_name, _PAGE_BG_SHAPES["Basketball"])
    svg = (
        f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 360' width='360' height='360' "
        f"fill='none' stroke='{stroke}' stroke-width='1.55' stroke-opacity='{opacity}' "
        f"stroke-linecap='round' stroke-linejoin='round'>"
        f"{shapes}</svg>"
    )
    return f'url("data:image/svg+xml,{quote(svg)}")'

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
  background-color: var(--bg);
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

#MainMenu, footer, .stAppDeployButton, [class*="viewerBadge"], [class*="creatorBadge"] { visibility: hidden; display: none; }
header[data-testid="stHeader"] { background: transparent; }

.block-container {
  max-width: 880px;
  padding-top: 1.2rem;
  padding-bottom: 8.5rem;
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
  border-radius: 12px;
  padding: 20px 26px 10px;
  overflow: hidden;
  margin-bottom: 18px;
  border: 1px solid rgba(255,255,255,0.18);
  box-shadow: 0 12px 30px rgba(0,0,0,0.22);
  position: relative;
  transition: background-color 0.25s ease, border-color 0.25s ease;
}

.st-key-hero [data-testid="stVerticalBlock"] {
  gap: 0.4rem;
}

/* Brand Crest Logo & Wordmark */
.wordmark-wrap {
  display: flex;
  align-items: center;
  gap: 11px;
}

.brand-logo {
  display: inline-block;
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
  filter: drop-shadow(0 3px 8px rgba(0, 0, 0, 0.28));
  transition: transform 0.2s ease, filter 0.2s ease;
}

.brand-logo:hover {
  transform: translateY(-1px) scale(1.04);
  filter: drop-shadow(0 5px 12px rgba(0, 0, 0, 0.36));
}

.wordmark {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 1.32rem;
  letter-spacing: -0.025em;
  line-height: 1;
  color: #FFFFFF;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.24);
}

.hero-title {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: clamp(2.5rem, 7vw, 3.8rem);
  line-height: 1;
  letter-spacing: -0.035em;
  color: #FFFFFF;
  margin-top: 8px;
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.22);
}

.stApp .hero-sub {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  color: rgba(255, 255, 255, 0.90);
  font-size: 0.96rem;
  font-weight: 500;
  margin: 8px 0 14px;
  text-shadow: 0 1px 6px rgba(0, 0, 0, 0.2);
}

.sub-text {
  line-height: 1.35;
}

.sub-pill {
  display: inline-block;
  flex-shrink: 0;
  background: rgba(0, 0, 0, 0.24);
  border: 1px solid rgba(255, 255, 255, 0.30);
  border-radius: 4px;
  padding: 2px 8px;
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: #FFFFFF;
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
  background-color: rgba(0, 0, 0, 0.22);
  background-repeat: no-repeat;
  background-position: right 4px center;
  background-size: auto 92%;
  border: 1px solid rgba(255, 255, 255, 0.30);
  border-radius: 7px;
  min-height: 2.85rem;
  padding: 0 0.85rem;
  color: rgba(255, 255, 255, 0.94);
  box-shadow: none;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
  cursor: pointer;
}

.stApp .st-key-hero [class*="st-key-sp_"] button > div {
  gap: 0.5rem;
  justify-content: center;
}

.stApp .st-key-hero [class*="st-key-sp_"] button p {
  color: rgba(255, 255, 255, 0.94);
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 0.95rem;
  letter-spacing: -0.01em;
}

.stApp .st-key-hero [class*="st-key-sp_"] button span[data-testid="stIconMaterial"] {
  color: rgba(255, 255, 255, 0.94);
}

.stApp .st-key-hero [class*="st-key-sp_"] button:hover {
  background-color: rgba(255, 255, 255, 0.18);
  border-color: rgba(255, 255, 255, 0.62);
  transform: translateY(-1px);
}

.stApp .st-key-hero [class*="st-key-sp_"] button:hover p {
  color: #FFFFFF;
}

/* --- Topic Tabs Bar --- */
.st-key-topics {
  margin-top: 14px;
  padding-top: 4px;
  border-top: 1px solid rgba(255, 255, 255, 0.22);
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
  color: rgba(255, 255, 255, 0.78);
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 0.92rem;
  letter-spacing: 0.01em;
}

.stApp .st-key-hero [class*="st-key-tp_"] button span[data-testid="stIconMaterial"] {
  color: rgba(255, 255, 255, 0.78);
}

.stApp .st-key-hero [class*="st-key-tp_"] button:hover {
  background: rgba(255, 255, 255, 0.10) !important;
}

.stApp .st-key-hero [class*="st-key-tp_"] button:hover p,
.stApp .st-key-hero [class*="st-key-tp_"] button:hover span[data-testid="stIconMaterial"] {
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

/* --- Chat Messages & Avatars (Refined Prompt & Response Bubbles) --- */
.stApp [data-testid="stLayoutWrapper"]:has(> [data-testid="stChatMessage"]),
.stApp [data-testid="stElementContainer"]:has(> [data-testid="stChatMessage"]) {
  display: block !important;
  width: 100% !important;
  height: auto !important;
  min-height: 0 !important;
  overflow: visible !important;
  position: relative;
  z-index: 1;
}

.stApp [data-testid="stChatMessage"] {
  position: relative;
  z-index: 1;
  box-sizing: border-box !important;
  width: 100% !important;
  margin: 0 !important;
  padding: 18px 22px !important;
  gap: 14px !important;
  align-items: flex-start !important;
  border-radius: 6px 16px 16px 16px !important;
  background: var(--panel) !important;
  border: 1px solid var(--line) !important;
  border-left: 3.5px solid var(--accent) !important;
  box-shadow: var(--card-shadow) !important;
  line-height: 1.62;
  overflow-wrap: anywhere;
}

.stApp [data-testid="stChatMessageContent"] {
  margin: 0 !important;
  flex: 1 1 auto !important;
  min-width: 0 !important;
  width: auto !important;
}

.stApp [data-testid="stChatMessageContent"] > [data-testid="stVerticalBlock"] {
  gap: 0.5rem !important;
}

.stApp [data-testid="stChatMessageContent"] p:last-child {
  margin-bottom: 0;
}

.stApp [data-testid="stChatMessageAvatarAssistant"],
.stApp [data-testid="stChatMessageAvatarCustom"] {
  width: 34px !important;
  height: 34px !important;
  min-width: 34px !important;
  background: var(--accent) !important;
  border: none !important;
  border-radius: 9px !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.14) !important;
  color: #FFFFFF !important;
}

.stApp [data-testid="stChatMessageAvatarAssistant"] *,
.stApp [data-testid="stChatMessageAvatarCustom"] * {
  color: #FFFFFF !important;
}

.stApp [data-testid="stChatMessageAvatarUser"] {
  display: none !important;
}

.stApp [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
.stApp [data-testid="stChatMessage"]:has(.cs-user-actions) {
  display: flex !important;
  flex-direction: row !important;
  margin: 8px 0 2px auto !important;
  width: fit-content !important;
  min-width: min(140px, 100%);
  max-width: 80% !important;
  padding: 14px 18px 12px !important;
  gap: 0 !important;
  background: linear-gradient(135deg, var(--accent) 0%, var(--hero) 100%) !important;
  border: 1px solid var(--accent-edge) !important;
  border-left: 1px solid var(--accent-edge) !important;
  border-radius: 16px 16px 4px 16px !important;
  box-shadow: 0 4px 14px -4px rgba(0, 0, 0, 0.24) !important;
}

.stApp [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"],
.stApp [data-testid="stChatMessage"]:has(.cs-user-actions) [data-testid="stChatMessageContent"] {
  flex: 0 1 auto !important;
  max-width: 100%;
}

.stApp [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p,
.stApp [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) li,
.stApp [data-testid="stChatMessage"]:has(.cs-user-actions) p,
.stApp [data-testid="stChatMessage"]:has(.cs-user-actions) li {
  color: #FFFFFF !important;
  font-weight: 500;
  line-height: 1.5;
}

.stApp [data-testid="stChatMessage"] strong {
  color: var(--accent-text);
  font-weight: 700;
}

.stApp [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) strong,
.stApp [data-testid="stChatMessage"]:has(.cs-user-actions) strong {
  color: #FFFFFF !important;
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
  background: rgba(0, 0, 0, 0.18);
  border-left: 2.5px solid rgba(255, 255, 255, 0.78);
  border-radius: 6px;
  padding: 5px 10px;
  margin-bottom: 8px;
  word-break: break-word;
}

/* User bubble inline Copy button */
.stApp [data-testid="stElementContainer"]:has(.cs-user-actions) {
  width: 100% !important;
  min-width: 0;
  margin: 0 !important;
  padding: 0 !important;
}

.cs-user-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 10px;
  margin-top: 2px;
}

.cs-user-copy {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(0, 0, 0, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.30);
  border-radius: 999px;
  color: #FFFFFF;
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  padding: 2px 10px;
  min-height: 24px;
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

/* Toolbar row beneath each assistant card (strictly positive margins so bubbles never collide) */
[class*="st-key-tools_"] {
  position: relative;
  z-index: 2;
  margin: 0 0 10px 4px !important;
  gap: 4px !important;
  align-items: center;
}

[class*="st-key-tools_"]:has(.cs-share-menu.is-open) {
  z-index: 80 !important;
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
  color: #FFFFFF;
  text-align: left;
  padding: 9px 14px;
  font-family: var(--font-mono);
  font-weight: 600;
  font-size: 0.74rem;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  border-bottom: 2px solid var(--accent-edge);
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
.stApp [data-testid="stElementContainer"]:has(.followup-label) {
  margin-top: 14px !important;
  margin-bottom: 6px !important;
}

.followup-label {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  line-height: 1.2;
  margin: 0;
  padding: 12px 0 6px;
  border-top: 1px solid var(--line-subtle);
}

.st-key-qa_ai_followup {
  margin-bottom: 8px !important;
}

.st-key-qa_ai_followup button {
  width: 100%;
  justify-content: flex-start;
  text-align: left;
  border-radius: 5px;
  border: 1.5px solid var(--accent);
  background: var(--accent-light);
  padding: 0.55rem 0.95rem;
  min-height: 2.6rem;
  margin-bottom: 0;
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
  gap: 0.55rem !important;
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

[data-testid="stBottomBlockContainer"] [data-testid="stVerticalBlock"] {
  gap: 0.45rem !important;
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

/* File upload (+) button - matches Send button color */
[data-testid="stChatInputFileUploadButton"] button {
  background-color: var(--accent) !important;
  color: #FFFFFF !important;
  border-radius: 6px !important;
  width: 2.05rem;
  height: 2.05rem;
  box-shadow: 0 2px 0 var(--accent-edge) !important;
  transition: background-color 0.15s ease, color 0.15s ease, transform 0.12s ease, box-shadow 0.12s ease !important;
}

[data-testid="stChatInputFileUploadButton"] button:hover:not(:disabled) {
  background-color: var(--accent-hover) !important;
  color: #FFFFFF !important;
  transform: translateY(-1px);
  box-shadow: 0 3px 0 var(--accent-edge) !important;
}

[data-testid="stChatInputFileUploadButton"] button:disabled {
  background-color: var(--input-btn-disabled-bg) !important;
  color: var(--input-btn-disabled-fg) !important;
  box-shadow: none !important;
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
  fill: currentColor !important;
  stroke: none !important;
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
  caret-color: transparent !important;
  cursor: pointer !important;
  user-select: none;
  -webkit-user-select: none;
  font-family: var(--font-body);
}

.stApp [data-testid="stSelectbox"] input[role="combobox"]::placeholder {
  color: var(--muted) !important;
  -webkit-text-fill-color: var(--muted) !important;
}

.stApp [data-testid="stSelectbox"] div:has(> input[role="combobox"]) button {
  background: transparent !important;
  color: var(--muted) !important;
}

.stApp [data-testid="stSelectbox"] div:has(> input[role="combobox"]) button:hover {
  color: var(--accent-text) !important;
}

.stApp [data-testid="stSelectbox"] div:has(> input[role="combobox"]) button svg {
  color: inherit !important;
  fill: currentColor !important;
}

/* --- Widget Help Tooltips (?) (consistent & theme-aware) --- */
.stApp [data-testid="stTooltipIcon"] button {
  background: transparent !important;
  color: var(--muted) !important;
}

.stApp [data-testid="stTooltipIcon"] svg,
.stApp [data-testid="stTooltipIcon"] svg.icon {
  fill: none !important;
  stroke: var(--muted) !important;
  color: var(--muted) !important;
  transition: stroke 0.15s ease, color 0.15s ease;
}

.stApp [data-testid="stTooltipIcon"]:hover svg,
.stApp [data-testid="stTooltipIcon"]:hover svg.icon,
.stApp [data-testid="stTooltipIcon"] button:focus-visible svg {
  fill: none !important;
  stroke: var(--accent-text) !important;
  color: var(--accent-text) !important;
}

/* Tooltip popup (portaled outside .stApp, so no .stApp prefix) */
[data-testid="stTooltipContent"] {
  background-color: var(--panel) !important;
  color: var(--ink) !important;
  border: 1px solid var(--input-border) !important;
  box-shadow: var(--card-shadow-hover) !important;
}

[data-testid="stTooltipContent"] p,
[data-testid="stTooltipContent"] span,
[data-testid="stTooltipContent"] li {
  color: var(--ink) !important;
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
/* Sidebar expand/collapse toggles (config.toml uses base="light", so override Emotion's dark fadedText60 icon color) */
button[data-testid="stExpandSidebarButton"],
[data-testid="stExpandSidebarButton"] button,
[data-testid="stSidebarCollapseButton"] button,
button[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] button {
  color: var(--ink-secondary) !important;
  background-color: transparent !important;
  border-radius: 6px !important;
  transition: color 0.15s ease, background-color 0.15s ease !important;
}

button[data-testid="stExpandSidebarButton"]:hover,
[data-testid="stExpandSidebarButton"] button:hover,
[data-testid="stSidebarCollapseButton"] button:hover,
button[data-testid="stSidebarCollapseButton"]:hover,
[data-testid="collapsedControl"] button:hover {
  color: var(--accent-text) !important;
  background-color: var(--input-hover-bg) !important;
}

button[data-testid="stExpandSidebarButton"] span[data-testid="stIconMaterial"],
[data-testid="stExpandSidebarButton"] button span[data-testid="stIconMaterial"],
[data-testid="stSidebarCollapseButton"] button span[data-testid="stIconMaterial"],
button[data-testid="stSidebarCollapseButton"] span[data-testid="stIconMaterial"],
[data-testid="collapsedControl"] button span[data-testid="stIconMaterial"] {
  color: var(--ink-secondary) !important;
}

button[data-testid="stExpandSidebarButton"]:hover span[data-testid="stIconMaterial"],
[data-testid="stExpandSidebarButton"] button:hover span[data-testid="stIconMaterial"],
[data-testid="stSidebarCollapseButton"] button:hover span[data-testid="stIconMaterial"],
button[data-testid="stSidebarCollapseButton"]:hover span[data-testid="stIconMaterial"],
[data-testid="collapsedControl"] button:hover span[data-testid="stIconMaterial"] {
  color: var(--accent-text) !important;
}

button[data-testid="stExpandSidebarButton"] svg,
[data-testid="stExpandSidebarButton"] button svg,
[data-testid="stSidebarCollapseButton"] button svg,
button[data-testid="stSidebarCollapseButton"] svg,
[data-testid="collapsedControl"] button svg {
  color: var(--ink-secondary) !important;
  fill: currentColor !important;
}

button[data-testid="stExpandSidebarButton"]:hover svg,
[data-testid="stExpandSidebarButton"] button:hover svg,
[data-testid="stSidebarCollapseButton"] button:hover svg,
button[data-testid="stSidebarCollapseButton"]:hover svg,
[data-testid="collapsedControl"] button:hover svg {
  color: var(--accent-text) !important;
  fill: currentColor !important;
}

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
/* Lift chat composer above Streamlit Community Cloud's bottom-right badge/icons on narrow & mobile screens */
@media (max-width: 1080px) {
  .block-container {
    padding-bottom: 12rem;
  }
  .stApp [data-testid="stBottomBlockContainer"] {
    padding-bottom: calc(4.75rem + env(safe-area-inset-bottom, 0px)) !important;
  }
}

@media (max-width: 768px) {
  .block-container {
    padding-left: 1rem;
    padding-right: 1rem;
    padding-bottom: 12.5rem;
  }
  .stApp [data-testid="stBottomBlockContainer"] {
    padding-bottom: calc(5.5rem + env(safe-area-inset-bottom, 0px)) !important;
  }
  .st-key-hero {
    padding: 18px 20px 10px;
  }
}

@media (max-width: 640px) {
  .block-container {
    padding-top: 0.75rem;
    padding-bottom: 12.5rem;
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
  .stApp [data-testid="stChatMessage"] {
    padding: 14px 16px !important;
    gap: 10px !important;
    border-radius: 6px 14px 14px 14px !important;
  }
  .stApp [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
  .stApp [data-testid="stChatMessage"]:has(.cs-user-actions) {
    max-width: 88% !important;
    padding: 13px 15px 11px !important;
    border-radius: 14px 14px 4px 14px !important;
  }
  .cs-user-copy {
    min-height: 36px;
    padding: 5px 12px;
    font-size: 0.72rem;
  }
  .stMarkdown table {
    display: block;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    white-space: nowrap;
  }
  .cs-act-btn {
    min-height: 44px;
    padding: 8px 14px;
  }
  .cs-act-btn.cs-icon-btn {
    width: 44px;
    height: 44px;
    min-height: 44px;
    padding: 0;
  }
  [class*="st-key-reply_btn_"] button {
    min-height: 44px !important;
    padding: 0 0.85rem !important;
  }
  .cs-share-menu {
    max-width: calc(100vw - 2rem);
    box-sizing: border-box;
  }
  .cs-share-item {
    min-height: 42px;
    padding: 8px 14px;
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
  .stApp [data-testid="stBottomBlockContainer"] {
    padding-left: 0.85rem !important;
    padding-right: 0.85rem !important;
    padding-bottom: calc(5.5rem + env(safe-area-inset-bottom, 0px)) !important;
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
  .stApp .st-key-hero [class*="st-key-sp_"] button {
    padding: 0 0.35rem;
  }
  .stApp .st-key-hero [class*="st-key-sp_"] button p {
    font-size: 0.88rem;
    white-space: nowrap;
  }
  .brand-logo {
    width: 34px;
    height: 34px;
  }
  .wordmark {
    font-size: 1.18rem;
  }
}

@media (max-width: 390px) {
  .stApp .st-key-dark label p {
    font-size: 0.82rem;
  }
  .st-key-sports_row [data-testid="stHorizontalBlock"] {
    gap: 0.35rem;
  }
  .stApp .st-key-hero [class*="st-key-sp_"] button p {
    font-size: 0.82rem;
  }
}

/* --- Sport Bouncing Ball Loader --- */
.stApp [data-testid="stChatMessage"]:has(.cs-loader) {
  align-items: center !important;
  padding-top: 16px !important;
  padding-bottom: 16px !important;
}

.stApp [data-testid="stChatMessage"]:has(.cs-loader) [data-testid="stMarkdownContainer"] {
  margin: 0 !important;
  padding: 0 !important;
  width: 100%;
}

.cs-loader {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  box-sizing: border-box;
  gap: 11px;
  padding: 2px 0;
  margin: 0;
}

.stApp [data-testid="stChatMessage"] .cs-loader {
  padding-right: 48px;
}

.cs-loader.cs-loader-card {
  display: flex;
  justify-content: center;
  background: var(--panel);
  border: 1px solid var(--line);
  border-top: 2.5px solid var(--accent);
  border-radius: 6px;
  padding: 20px 24px;
  margin: 6px 0 14px;
  box-shadow: var(--card-shadow);
}

.cs-ball-stage {
  position: relative;
  display: inline-flex;
  align-items: flex-end;
  justify-content: center;
  width: 34px;
  height: 38px;
  flex-shrink: 0;
}

.cs-ball {
  position: relative;
  z-index: 2;
  width: 24px;
  height: 24px;
  margin-bottom: 4px;
  transform-origin: center bottom;
  animation: cs-ball-bounce 0.72s cubic-bezier(0.28, 0.84, 0.42, 1) infinite;
  will-change: transform;
}

.cs-ball-art {
  display: block;
  width: 100%;
  height: 100%;
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
  animation: cs-ball-spin 1.9s linear infinite;
  will-change: transform;
}

.cs-ball-shadow {
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 20px;
  height: 4px;
  margin-left: -10px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.24);
  filter: blur(1px);
  transform-origin: center center;
  animation: cs-shadow-pulse 0.72s cubic-bezier(0.28, 0.84, 0.42, 1) infinite;
  will-change: transform, opacity;
}

.cs-loader-text {
  font-family: var(--font-body);
  font-size: 0.93rem;
  font-weight: 500;
  line-height: 1.2;
  color: var(--muted);
  letter-spacing: -0.005em;
  padding-top: 3px;
}

@media (max-width: 640px) {
  .stApp [data-testid="stChatMessage"] .cs-loader {
    padding-right: 28px;
  }
}

@keyframes cs-ball-bounce {
  0%, 100% {
    transform: translateY(0) scaleX(1.13) scaleY(0.85);
  }
  14% {
    transform: translateY(-3px) scaleX(0.93) scaleY(1.08);
  }
  48% {
    transform: translateY(-11px) scaleX(1) scaleY(1);
  }
  86% {
    transform: translateY(-2px) scaleX(0.96) scaleY(1.05);
  }
}

@keyframes cs-ball-spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes cs-shadow-pulse {
  0%, 100% {
    transform: scaleX(1.14);
    opacity: 0.52;
  }
  48% {
    transform: scaleX(0.54);
    opacity: 0.16;
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


def brand_logo_svg(sport="Basketball", dark=False):
    """Build the CourtSense geometric sports-crest vector logo (pure vector paths, no text)."""
    mode = "dark" if dark else "light"
    accent_hex = THEMES.get(sport, THEMES["Basketball"])[mode]["accent"]
    return (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 60' fill='none'>"
        "<defs>"
        "<linearGradient id='cs-bg' x1='0' y1='0' x2='1' y2='1'>"
        "<stop offset='0%' stop-color='#1B2230' stop-opacity='0.88'/>"
        "<stop offset='100%' stop-color='#090C12' stop-opacity='0.96'/>"
        "</linearGradient>"
        "<linearGradient id='cs-rim' x1='0' y1='0' x2='0' y2='1'>"
        "<stop offset='0%' stop-color='#FFFFFF' stop-opacity='0.98'/>"
        "<stop offset='100%' stop-color='#FFFFFF' stop-opacity='0.65'/>"
        "</linearGradient>"
        "<clipPath id='cs-clip'>"
        "<path d='M12 6 H48 L54 12 V28.5 C54 40.5 43.8 49 30 54.6 C16.2 49 6 40.5 6 28.5 V12 Z'/>"
        "</clipPath>"
        "</defs>"
        # Outer sculpted athletic shield
        "<path d='M11 4 H49 L56 11 V29 C56 42 45 51 30 57 C15 51 4 42 4 29 V11 Z' "
        "fill='url(#cs-bg)' stroke='url(#cs-rim)' stroke-width='2.4' stroke-linejoin='round'/>"
        # Clipped interior: broadcast specular sheen + court center-circle blueprint
        "<g clip-path='url(#cs-clip)'>"
        "<path d='M4 4 H56 V19 L4 34 Z' fill='#FFFFFF' fill-opacity='0.09'/>"
        "<path d='M6 29 H54' stroke='#FFFFFF' stroke-opacity='0.18' stroke-width='1.1'/>"
        "<circle cx='30' cy='29' r='13.5' stroke='#FFFFFF' stroke-opacity='0.22' stroke-width='1.1'/>"
        "<path d='M14 50 H46' stroke='#FFFFFF' stroke-opacity='0.16' stroke-width='1.1'/>"
        "</g>"
        # Inner hairline shield bevel
        "<path d='M13 8.2 H47 L51.8 13 V28.2 C51.8 38.6 42.6 46.2 30 51.3 "
        "C17.4 46.2 8.2 38.6 8.2 28.2 V13 Z' "
        "stroke='#FFFFFF' stroke-opacity='0.22' stroke-width='1'/>"
        # Top crest intelligence diamond & tactical wings
        "<path d='M20 12.2 H25.2 M34.8 12.2 H40' stroke='#FFFFFF' stroke-opacity='0.55' "
        "stroke-width='1.4' stroke-linecap='round'/>"
        f"<polygon points='30,9.2 33,12.2 30,15.2 27,12.2' fill='{accent_hex}' "
        "stroke='#FFFFFF' stroke-width='1'/>"
        # Bespoke geometric athletic 'C' & 'S' vector monogram (pure paths, zero <text>)
        "<path d='M26.5 19.5 H19 L15 23.5 V34.5 L19 38.5 H26.5' "
        "stroke='#FFFFFF' stroke-width='3.4' stroke-linecap='square' stroke-linejoin='miter'/>"
        "<path d='M44.5 19.5 H36.5 L33 23 V26 L36.5 29 H41.5 L45 32 V35 L41.5 38.5 H33' "
        "stroke='#FFFFFF' stroke-width='3.4' stroke-linecap='square' stroke-linejoin='miter'/>"
        # Lower court-tip chevron accent
        f"<path d='M25.5 44.5 L30 47.6 L34.5 44.5' stroke='{accent_hex}' "
        "stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/>"
        "</svg>"
    )


def _brand_logo_bg(sport="Basketball", dark=False):
    b64 = base64.b64encode(brand_logo_svg(sport, dark).encode("utf-8")).decode("ascii")
    return f'url("data:image/svg+xml;base64,{b64}")'


_BALL_SHAPES = {
    "Basketball": (
        "<circle cx='24' cy='24' r='20.5'/>"
        "<g clip-path='url(#cs-ball-clip)'>"
        "<path d='M3.5 24H44.5'/>"
        "<path d='M24 3.5V44.5'/>"
        "<path d='M10.5 8.5C18.5 16.5 18.5 31.5 10.5 39.5'/>"
        "<path d='M37.5 8.5C29.5 16.5 29.5 31.5 37.5 39.5'/>"
        "</g>"
    ),
    "Volleyball": (
        "<circle cx='24' cy='24' r='20.5'/>"
        "<g clip-path='url(#cs-ball-clip)'>"
        "<path d='M24 24Q20 13.5 24 3.5'/>"
        "<path d='M24 24Q34 25.5 41.8 34.2'/>"
        "<path d='M24 24Q15 30 6.2 34.2'/>"
        "<path d='M23 14.5Q33 13 43.5 20.5'/>"
        "<path d='M24.5 8.5Q34 7.5 41 13'/>"
        "<path d='M33.5 29.5Q24 36 14.5 29.5'/>"
        "<path d='M37.5 36.5Q24 43 10.5 36.5'/>"
        "<path d='M14.5 29Q11 19 16 8.5'/>"
        "<path d='M8.8 27Q6.2 18 11 10.5'/>"
        "</g>"
    ),
    "Football": (
        "<circle cx='24' cy='24' r='20.5'/>"
        "<g clip-path='url(#cs-ball-clip)'>"
        "<polygon points='24,16 31.6,21.5 28.7,30.4 19.3,30.4 16.4,21.5'/>"
        "<path d='M24 16V9.2M18.5 6.2L24 9.2L29.5 6.2'/>"
        "<path d='M31.6 21.5L38.2 19.4M39.5 13.2L38.2 19.4L42.8 23.6'/>"
        "<path d='M28.7 30.4L32.8 36.2M38.8 35.6L32.8 36.2L30.2 41.8'/>"
        "<path d='M19.3 30.4L15.2 36.2M17.8 41.8L15.2 36.2L9.2 35.6'/>"
        "<path d='M16.4 21.5L9.8 19.4M5.2 23.6L9.8 19.4L8.5 13.2'/>"
        "</g>"
    ),
}


def _ball_svg(sport="Basketball", stroke="#C94A12"):
    shapes = _BALL_SHAPES.get(sport, _BALL_SHAPES["Basketball"])
    return (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48' "
        f"fill='none' stroke='{stroke}' stroke-width='2.3' "
        "stroke-linecap='round' stroke-linejoin='round'>"
        "<defs><clipPath id='cs-ball-clip'><circle cx='24' cy='24' r='20.5'/></clipPath></defs>"
        f"{shapes}</svg>"
    )


def _ball_svg_bg(sport="Basketball", stroke="#C94A12"):
    b64 = base64.b64encode(_ball_svg(sport, stroke).encode("utf-8")).decode("ascii")
    return f'url("data:image/svg+xml;base64,{b64}")'


def loading_ball_html(sport="Basketball", label="Generating response…", card=False):
    """Return single-line HTML for a sport-specific bouncing ball loader."""
    slug = sport.lower() if sport in _BALL_SHAPES else "basketball"
    cls = "cs-loader cs-loader-card" if card else "cs-loader"
    safe_label = html.escape(label or "")
    return (
        f'<div class="{cls}" role="status" aria-live="polite">'
        f'<span class="cs-ball-stage" aria-hidden="true">'
        f'<span class="cs-ball"><span class="cs-ball-art cs-ball-{slug}"></span></span>'
        f'<span class="cs-ball-shadow"></span>'
        f'</span>'
        f'<span class="cs-loader-text">{safe_label}</span>'
        f'</div>'
    )


def get_css(sport="Basketball", topic="Rules", dark=False):
    mode = "dark" if dark else "light"
    theme = {**BASE[mode], **THEMES.get(sport, THEMES["Basketball"])[mode]}
    root = ":root{" + "".join(f"--{k}:{v};" for k, v in theme.items()) + "}"
    art = ART.get(sport, ART["Basketball"])
    page_tile = _page_bg_tile(sport, theme["accent"], 0.115 if dark else 0.105)
    page_bg = (
        ".stApp{"
        "background-image:"
        "radial-gradient(ellipse 960px 440px at 50% -40px,var(--bg-glow) 0%,transparent 72%),"
        "radial-gradient(ellipse 560px 440px at 0% 100%,var(--bg-glow-soft) 0%,transparent 70%),"
        "radial-gradient(ellipse 560px 440px at 100% 95%,var(--bg-glow-soft) 0%,transparent 70%),"
        f"{page_tile};"
        "background-size:100% 100%,100% 100%,100% 100%,360px 360px;"
        "background-position:center top,left bottom,right bottom,center top;"
        "background-repeat:no-repeat,no-repeat,no-repeat,repeat;"
        "background-attachment:fixed,fixed,fixed,fixed;}"
        "@media (max-width:768px){.stApp{background-attachment:scroll,scroll,scroll,scroll;}}"
    )
    hero_bg = (
        ".st-key-hero{"
        "background-image:"
        "linear-gradient(95deg,var(--hero-scrim) 0%,var(--hero-scrim-mid) 38%,rgba(0,0,0,0) 72%),"
        "url(\"data:image/svg+xml," + quote(art) + "\"),"
        "linear-gradient(125deg,var(--hero-start) 0%,var(--hero-end) 100%);"
        "background-size:100% 100%,auto 106%,100% 100%;"
        "background-position:0 0,right 6px center,0 0;"
        "background-repeat:no-repeat;}"
        "@media (max-width:640px){.st-key-hero{"
        "background-size:100% 100%,auto 100%,100% 100%;"
        "background-position:0 0,right -28px center,0 0;}}"
    )
    sport_btns_css = "".join(
        f".stApp .st-key-sp_{name} button{{background-image:{_sport_btn_bg(name, '#FFFFFF', 0.22)};}}"
        for name in _BTN_ART_SHAPES
    )
    active_btn_art = _sport_btn_bg(sport if sport in _BTN_ART_SHAPES else "Basketball", theme["hero"], 0.16)
    m, acc = theme["muted"], theme["accent-text"]
    ball_css = "".join(
        f".cs-ball-{name.lower()}{{background-image:{_ball_svg_bg(name, THEMES[name][mode]['accent-text'])};}}"
        for name in _BALL_SHAPES
    )
    icons_css = (
        f".brand-logo{{background-image:{_brand_logo_bg(sport, dark)};}}"
        f"{ball_css}"
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
        f"background-color:#FFFFFF !important;background-image:{active_btn_art} !important;"
        f"border-color:#FFFFFF !important;color:var(--hero) !important;"
        f"transform:translateY(-1px);box-shadow:0 5px 16px rgba(0,0,0,0.24) !important;}}"
        f"{sp} button p,{sp} button:hover p{{color:var(--hero) !important;font-weight:700 !important;}}"
        f"{sp} button span[data-testid='stIconMaterial']{{color:var(--hero) !important;}}"
        f"{tp} button{{"
        f"border-bottom-color:#FFFFFF !important;background:rgba(255,255,255,0.16) !important;}}"
        f"{tp} button p{{color:#FFFFFF !important;font-weight:700 !important;}}"
        f"{tp} button span[data-testid='stIconMaterial']{{color:#FFFFFF !important;}}"
    )
    font_links = (
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        f'<link rel="stylesheet" href="{FONT_URL}">'
    )
    font_import = f"@import url('{FONT_URL}');"
    # Keep <style> at column 0 of its own Markdown block (CommonMark Type 1 HTML block)
    # so blank lines inside CSS are never parsed as Markdown paragraphs.
    return "<style>" + font_import + root + CSS + page_bg + hero_bg + sport_btns_css + icons_css + active + "</style>\n\n" + font_links
