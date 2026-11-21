"""Visual styling. Palette: court blue, scoreboard amber, line-marking white."""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap');

.stApp, .stApp p, .stApp li, .stApp td, .stApp label, .stApp textarea { font-family: 'Barlow', sans-serif; }
#MainMenu, footer, .stAppDeployButton { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 860px; padding-top: 1.4rem; padding-bottom: 6rem; }
[data-testid="stSidebar"] { background: #DCE3EB; }

/* scoreboard */
.board { background:#0F2340; border-bottom:4px solid #F2B632; border-radius:6px;
  padding:14px 18px; display:flex; align-items:center; justify-content:space-between;
  gap:16px; flex-wrap:wrap; margin-bottom:14px; }
.board .brand { font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:2.1rem;
  color:#fff; line-height:1; }
.board .brand small { display:block; font-family:'Barlow',sans-serif; font-weight:500;
  font-size:.8rem; color:#9FB3CC; margin-top:5px; }
.board .cells { display:flex; gap:8px; }
.board .cell { background:#07142A; border:1px solid #243B5E; border-radius:4px;
  padding:6px 12px; min-width:96px; text-align:center; }
.board .k { display:block; font-size:.72rem; color:#8EA4C2; }
.board .v { display:block; font-family:'Barlow Condensed',sans-serif; font-size:1.5rem;
  font-weight:600; color:#FFC247; line-height:1.1; white-space:nowrap; }
@media (max-width: 640px) {
  .board .cell { min-width:0; padding:5px 8px; }
  .board .v { font-size:1.15rem; }
  .board .brand { font-size:1.7rem; }
}

/* chat */
[data-testid="stChatMessage"] { background:#fff; border:1px solid #D3DAE3;
  border-left:5px solid #F2B632; border-radius:4px; padding:14px 16px; margin-bottom:10px; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
  background:#14305A; border-color:#14305A; border-left-color:#14305A; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) li { color:#fff; }
[data-testid="stChatMessage"] strong { color:#14305A; }
.attach { display:inline-block; margin-top:6px; padding:2px 8px; border:1px solid #6B86AD;
  border-radius:3px; font-size:.82rem; color:#C9D6E8; }

/* stat tables */
.stMarkdown table { border-collapse:collapse; width:100%; margin:6px 0; font-size:.93rem; }
.stMarkdown th { background:#0F2340; color:#fff; text-align:left; padding:6px 10px;
  font-family:'Barlow Condensed',sans-serif; font-weight:600; font-size:1.02rem; }
.stMarkdown td { padding:6px 10px; border-bottom:1px solid #D8DFE8; }
.stMarkdown tr:nth-child(even) td { background:#F3F6F9; }

/* buttons: quick actions and starters */
.stButton > button { border-radius:999px; border:1.5px solid #14305A; background:#fff;
  color:#14305A; font-weight:600; padding:.15rem .95rem; }
.stButton > button:hover { background:#14305A; color:#fff; border-color:#14305A; }
.stButton > button:hover p { color:#fff; }
.starter .stButton > button { border-radius:4px; text-align:left; width:100%;
  border-left:5px solid #F2B632; padding:.6rem .9rem; font-weight:500; }

.hint { color:#4A5B70; font-size:.95rem; margin:4px 0 12px; }
</style>
"""
