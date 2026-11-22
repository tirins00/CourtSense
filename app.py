"""CourtSense: a sports rules and stats helper (Streamlit + Groq)."""
import io
import os
import re
import sys
from pathlib import Path

# Ensure local imports (defenses, prompts, styles) resolve regardless of current working directory
_app_dir = Path(__file__).parent.resolve()
if str(_app_dir) not in sys.path:
    sys.path.insert(0, str(_app_dir))

import streamlit as st
from groq import Groq

import defenses
from prompts import build_system_prompt
from styles import get_css

st.set_page_config(page_title="CourtSense", page_icon=":material/sports_basketball:", layout="centered")

SPORTS = ["Basketball", "Volleyball", "Football"]
TOPICS = ["Rules", "Strategy", "Stats", "Quiz"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]
MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
TOPIC_ICONS = {
    "Rules": ":material/gavel:",
    "Strategy": ":material/schema:",
    "Stats": ":material/bar_chart:",
    "Quiz": ":material/quiz:",
}
AVATARS = {
    "Basketball": ":material/sports_basketball:",
    "Volleyball": ":material/sports_volleyball:",
    "Football": ":material/sports_soccer:",
}
TAGLINES = {
    "Rules": "Every whistle, explained.",
    "Strategy": "Why teams line up the way they do.",
    "Stats": "What the numbers actually mean.",
    "Quiz": "Five questions, one at a time.",
}
PLACEHOLDERS = {
    "Rules": "Ask about a rule, foul, or penalty",
    "Strategy": "Ask about a play or formation",
    "Stats": "Ask about a stat, or press + to attach a box score",
    "Quiz": "Type your answer, or ask for a new question",
}
STARTERS = {
    "Basketball": {
        "Rules": ["What is a travelling violation?", "How does the 3-second rule work?"],
        "Strategy": ["Explain the pick and roll", "What is a zone defense?"],
        "Stats": ["What does assist-to-turnover ratio tell me?", "What is true shooting percentage?"],
    },
    "Volleyball": {
        "Rules": ["How does rotation work?", "What is a double contact?"],
        "Strategy": ["What does a libero do?", "Explain the 5-1 system"],
        "Stats": ["What is hitting percentage?", "What counts as a dig?"],
    },
    "Football": {
        "Rules": ["How does the offside rule work?", "When is a handball a foul?"],
        "Strategy": ["Explain the 4-3-3 formation", "What is a high press?"],
        "Stats": ["What is xG (expected goals)?", "What counts as an assist?"],
    },
}

ss = st.session_state
ss.setdefault("threads", {})
ss.setdefault("queued", None)
ss.setdefault("generate", False)
ss.setdefault("sport", SPORTS[0])
ss.setdefault("topic", TOPICS[0])


sport = ss.sport
topic = ss.topic
dark = ss.get("dark", False)
thread_key = f"{sport}|{topic}"
ss.messages = ss.threads.setdefault(thread_key, [])   # each sport + topic has its own chat

st.markdown(get_css(sport, topic, dark), unsafe_allow_html=True)


def queue(text):
    ss.queued = text


def set_sport(name):
    ss.sport = name


def set_topic(name):
    ss.topic = name


def start_quiz():
    """Jump to the Quiz tab for this sport and start a quiz there."""
    ss.topic = "Quiz"
    ss.queued = f"Start a 5-question {ss.sport} trivia quiz. One question at a time."


def get_client():
    key = None
    try:
        key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    if not key:
        key = os.environ.get("GROQ_API_KEY")
    if not key:
        # Fallback: check .streamlit/secrets.toml next to app.py or in parents
        import tomllib
        for cand in [
            _app_dir / ".streamlit" / "secrets.toml",
            _app_dir.parent / ".streamlit" / "secrets.toml",
            _app_dir.parent.parent / ".streamlit" / "secrets.toml",
        ]:
            if cand.exists():
                try:
                    with open(cand, "rb") as f:
                        key = tomllib.load(f).get("GROQ_API_KEY")
                        if key:
                            break
                except Exception:
                    pass
    if not key:
        st.error("No API key found. Add GROQ_API_KEY to .streamlit/secrets.toml "
                 "(local) or to your app's Secrets (Streamlit Community Cloud).")
        st.stop()
    return Groq(api_key=key)


@st.cache_data(ttl=3600, show_spinner=False)
def list_chat_models(_client):
    """Ask Groq which chat models this key can use right now."""
    skip = ("whisper", "tts", "guard", "compound", "embed", "orpheus", "safeguard")
    try:
        ids = sorted(m.id for m in _client.models.list().data)
    except Exception:
        return MODELS
    ids = [i for i in ids if not any(k in i.lower() for k in skip)]
    return ids or MODELS


def default_model_index(options):
    for pref in ("llama-3.3-70b", "llama-3.1-8b", "qwen", "llama", "70b", "120b", "8b"):
        for i, name in enumerate(options):
            if pref in name.lower():
                return i
    return 0


def trim_runaway(text, max_words=400):
    """Cut off looping or endless replies at the first repeated sentence."""
    sents = re.split(r"(?<=[.!?])\s+", text)
    seen, kept = set(), []
    for sent in sents:
        key = sent.strip().lower()
        if len(key) > 25 and key in seen:
            return " ".join(kept).strip(), True
        seen.add(key)
        kept.append(sent)
    words = text.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]).strip(), True
    return text, False


def read_upload(f):
    """Return the text of an uploaded txt/csv/md/pdf file."""
    raw = f.getvalue()
    if f.name.lower().endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(raw))
        text = "\n".join((p.extract_text() or "") for p in reader.pages)
    else:
        text = raw.decode("utf-8", errors="ignore")
    text = text.strip()
    if not text:
        raise ValueError("The uploaded file is empty or contains no readable text.")
    return text[: defenses.MAX_FILE_CHARS]


def build_messages(topic_now, level, token):
    msgs = [{"role": "system",
             "content": build_system_prompt(sport, topic_now, level, token, defenses.CANARY)}]
    hist = ss.messages
    last_att = max((i for i, m in enumerate(hist) if m.get("attachment")), default=-1)
    live = [(i, m) for i, m in enumerate(hist) if not m.get("blocked")][-12:]
    last_user = max((i for i, m in live if m["role"] == "user"), default=-1)
    for i, m in live:
        if m["role"] == "user":
            wrapped = defenses.wrap_user(m["content"], token, m["attachment"] if i == last_att else None)
            if i == last_user:
                wrapped = defenses.sandwich(wrapped, token)
            msgs.append({"role": "user", "content": wrapped})
        else:
            msgs.append({"role": "assistant", "content": m["content"]})
    return msgs


def export_markdown():
    lines = [f"# CourtSense: {sport}, {topic}", ""]
    for m in ss.messages:
        who = "You" if m["role"] == "user" else "CourtSense"
        lines += [f"**{who}:** {m['content']}", ""]
    return "\n".join(lines)


# ---------- sidebar ----------
with st.sidebar:
    st.markdown(
        '<div class="sidebar-header">'
        '<span class="sidebar-badge">PREFERENCES</span>'
        '<h3 style="margin-top:6px;margin-bottom:0;">Settings</h3>'
        '</div>',
        unsafe_allow_html=True,
    )
    level = st.radio("Detail level", LEVELS, key="level")
    model_options = list_chat_models(get_client())
    model = st.selectbox("Model", model_options, index=default_model_index(model_options), key="model")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.4, 0.1, key="temp",
                            help="Lower is more consistent. Higher is more varied.")
    st.divider()
    st.download_button("Export this chat", export_markdown(), f"courtsense_{sport}_{topic}.md".lower(),
                       icon=":material/download:", disabled=not ss.messages, use_container_width=True)
    if st.button("Clear this chat", icon=":material/delete_sweep:", use_container_width=True):
        ss.threads[thread_key] = []
        ss.queued, ss.generate = None, False
        st.rerun()
    st.divider()
    st.caption("Each sport and topic keeps its own chat. CourtSense explains rules, plays and "
               "stats. It does not give betting tips, and it only uses numbers you provide.")

# ---------- input ----------
value = st.chat_input(PLACEHOLDERS[topic], accept_file=True, file_type=["txt", "csv", "md", "pdf"])
text, files = None, []
if value:
    text = (getattr(value, "text", None) or "").strip()
    files = list(getattr(value, "files", None) or [])
if ss.queued:
    text, files, ss.queued = ss.queued, [], None

if text or files:
    text = (text or "Summarize this game from the attached data.")[: defenses.MAX_INPUT_CHARS]
    attachment, blocked, reason = None, False, None
    if not defenses.check_input(text)[0]:
        blocked = True
    elif files:
        try:
            body = read_upload(files[0])
        except Exception as exc:
            body = ""
            reason = str(exc) if isinstance(exc, ValueError) else (
                "I couldn't read that file. Try a .txt, .csv, .md or text-based .pdf."
            )
        if body:
            if defenses.check_input(body)[0]:
                attachment = {"name": files[0].name, "text": body}
            else:
                blocked, reason = True, ("That file contains instructions aimed at me, so I'm ignoring it. "
                                         "Attach plain box score data or notes instead.")
    ss.messages.append({"role": "user", "content": text, "attachment": attachment,
                        "file_name": files[0].name if files else None, "blocked": blocked})
    if blocked or reason:
        ss.messages.append({"role": "assistant", "content": reason or defenses.BLOCKED_REPLY, "blocked": True})
    else:
        ss.generate = True

# ---------- hero: title, sport buttons, topic tabs ----------
with st.container(key="hero"):
    c1, c2 = st.columns([3, 1.4], vertical_alignment="center")
    c1.markdown('<div class="wordmark-wrap"><span class="wordmark-badge">SPORTS INTEL</span><span class="wordmark">CourtSense</span></div>', unsafe_allow_html=True)
    c2.toggle("Dark mode", key="dark")
    st.markdown(f'<div class="hero-title">{sport}</div>'
                f'<div class="hero-sub"><span class="sub-pill">{topic}</span> {TAGLINES[topic]}</div>',
                unsafe_allow_html=True)
    cols = st.columns(3)
    for col, name in zip(cols, SPORTS):
        col.button(name, key=f"sp_{name}", icon=AVATARS[name], on_click=set_sport, args=(name,),
                   use_container_width=True)
    with st.container(key="topics"):
        cols = st.columns(4)
        for col, name in zip(cols, TOPICS):
            col.button(name, key=f"tp_{name}", icon=TOPIC_ICONS[name], on_click=set_topic, args=(name,),
                       use_container_width=True)

icon = AVATARS[sport]

# ---------- empty state ----------
if not ss.messages:
    if topic == "Quiz":
        st.markdown(
            f'<div class="empty">'
            f'<span class="empty-badge">TRIVIA CHALLENGE</span>'
            f'<div class="empty-title">Test your {sport} IQ</div>'
            f'<p>Five multiple-choice questions, one at a time, with live feedback and scoring.</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.button(f"Start the {sport} quiz", key="startquiz", on_click=queue,
                  args=(f"Start a 5-question {sport} trivia quiz. One question at a time.",),
                  icon=":material/play_circle:", use_container_width=True)
    else:
        st.markdown(
            f'<div class="empty">'
            f'<span class="empty-badge">{topic} PLAYBOOK</span>'
            f'<div class="empty-title">{sport} {topic}</div>'
            f'<p>Pick a starter question below or ask anything in plain language.</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
        with st.container(key="starters"):
            cols = st.columns(2)
            for i, q in enumerate(STARTERS[sport][topic]):
                cols[i % 2].button(q, key=f"starter_{i}", on_click=queue, args=(q,),
                                   icon=":material/arrow_forward:", use_container_width=True)

# ---------- history ----------
last = len(ss.messages) - 1
for i, m in enumerate(ss.messages):
    with st.chat_message(m["role"], avatar=icon if m["role"] == "assistant" else ":material/person:"):
        st.markdown(m["content"])
        if m.get("file_name") and m["role"] == "user":
            st.markdown(f'<span class="attach">Attached: {m["file_name"]}</span>', unsafe_allow_html=True)
        if i == last and m["role"] == "assistant" and not m.get("blocked") and not ss.generate:
            c1, c2, c3 = st.columns(3)
            c1.button("Show example", key="qa_ex", icon=":material/visibility:", on_click=queue,
                      args=("Show me one real-game example of that.",), use_container_width=True)
            c2.button("Quiz me", key="qa_quiz", icon=":material/quiz:", on_click=start_quiz,
                      use_container_width=True)
            c3.button("Explain simpler", key="qa_simple", icon=":material/lightbulb:", on_click=queue,
                      args=("Explain that again in simpler words.",), use_container_width=True)

# ---------- generate ----------
if ss.generate:
    ss.generate = False
    client = get_client()
    token = defenses.new_token()
    with st.chat_message("assistant", avatar=icon):
        box, reply = st.empty(), ""
        try:
            stream = client.chat.completions.create(
                model=model, temperature=temperature, max_tokens=500, stream=True,
                messages=build_messages(topic, level, token),
            )
            for chunk in stream:
                reply += chunk.choices[0].delta.content or ""
                reply, stop = trim_runaway(reply)
                box.markdown(reply + "▌")
                if stop:
                    break
        except Exception as e:
            detail = str(e)
            secret_values = [os.environ.get("GROQ_API_KEY")]
            try:
                secret_values.append(st.secrets["GROQ_API_KEY"])
            except Exception:
                pass
            for secret in secret_values:
                if secret:
                    detail = detail.replace(secret, "***")
            detail = detail[:300]
            reply = f"I couldn't reach the AI service just now.\n\nError: `{type(e).__name__}` {detail}"
        if defenses.leaked(reply):
            reply = defenses.LEAK_REPLY
        box.markdown(reply)
    ss.messages.append({"role": "assistant", "content": reply})
    st.rerun()
