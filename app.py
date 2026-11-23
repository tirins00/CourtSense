"""CourtSense: a sports rules and stats helper (Streamlit + Groq)."""
import io
import os
import re

import streamlit as st
from groq import Groq

import defenses
import stats
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
    "Stats": "Ask about a stat, a player or a league table, or press + to attach a box score",
    "Quiz": "Type your answer, or ask for a new question",
}
STARTERS = {
    "Basketball": {
        "Rules": ["What is a travelling violation?", "How does the 3-second rule work?"],
        "Strategy": ["Explain the pick and roll", "What is a zone defense?"],
        "Stats": ["How many points is LeBron James averaging?", "Show the NBA standings"],
    },
    "Volleyball": {
        "Rules": ["How does rotation work?", "What is a double contact?"],
        "Strategy": ["What does a libero do?", "Explain the 5-1 system"],
        "Stats": ["What is hitting percentage?", "Show the SuperLega standings"],
    },
    "Football": {
        "Rules": ["How does the offside rule work?", "When is a handball a foul?"],
        "Strategy": ["Explain the 4-3-3 formation", "What is a high press?"],
        "Stats": ["How many goals has Haaland scored this season?", "Show the Premier League table"],
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
        key = os.environ.get("GROQ_API_KEY")
    if not key:
        st.error("No API key found. Add GROQ_API_KEY to .streamlit/secrets.toml "
                 "(local) or to your app's Secrets (Streamlit Community Cloud).")
        st.stop()
    return Groq(api_key=key)


def get_vb_key():
    """Optional free API-Sports key for volleyball league data. None is fine."""
    try:
        return st.secrets["API_SPORTS_KEY"]
    except Exception:
        return os.environ.get("API_SPORTS_KEY")


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
    for pref in ("llama-3.3-70b", "70b", "120b", "llama-3.1-8b"):
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
    return text[: defenses.MAX_FILE_CHARS]


def build_messages(topic_now, level, token, live_data=None):
    msgs = [{"role": "system",
             "content": build_system_prompt(sport, topic_now, level, token, defenses.CANARY, live_data)}]
    hist = ss.messages
    last_att = max((i for i, m in enumerate(hist) if m.get("attachment")), default=-1)
    live = [(i, m) for i, m in enumerate(hist) if not m.get("blocked")][-12:]
    for i, m in live:
        if m["role"] == "user":
            wrapped = defenses.wrap_user(m["content"], token, m["attachment"] if i == last_att else None)
            if i == len(hist) - 1:
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
    st.subheader("Settings")
    level = st.radio("Detail level", LEVELS, key="level")
    model_options = list_chat_models(get_client())
    model = st.selectbox("Model", model_options, index=default_model_index(model_options), key="model")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.4, 0.1, key="temp",
                            help="Lower is more consistent. Higher is more varied.")
    st.divider()
    st.download_button("Export this chat", export_markdown(), f"courtsense_{sport}_{topic}.md".lower(),
                       disabled=not ss.messages, use_container_width=True)
    if st.button("Clear this chat", use_container_width=True):
        ss.threads[thread_key] = []
        ss.queued, ss.generate = None, False
        st.rerun()
    st.caption("Each sport and topic keeps its own chat. CourtSense explains rules, plays and "
               "stats, with live player and league numbers from ESPN (basketball, football) and "
               "API-Sports (volleyball) when available. It does not give betting tips.")

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
        except Exception:
            body, reason = "", "I couldn't read that file. Try a .txt, .csv, .md or text-based .pdf."
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
    c1.markdown('<span class="wordmark">CourtSense</span>', unsafe_allow_html=True)
    c2.toggle("Dark mode", key="dark")
    st.markdown(f'<div class="hero-title">{sport}</div><p class="hero-sub">{TAGLINES[topic]}</p>',
                unsafe_allow_html=True)
    cols = st.columns([1, 1, 1, 0.9])
    for col, name in zip(cols, SPORTS):
        col.button(name, key=f"sp_{name}", icon=AVATARS[name], on_click=set_sport, args=(name,),
                   use_container_width=True)
    with st.container(key="topics"):
        cols = st.columns([1, 1, 1, 1, 1.4])
        for col, name in zip(cols, TOPICS):
            col.button(name, key=f"tp_{name}", icon=TOPIC_ICONS[name], on_click=set_topic, args=(name,),
                       use_container_width=True)

icon = AVATARS[sport]

# ---------- empty state ----------
if not ss.messages:
    if topic == "Quiz":
        st.markdown(f'<div class="empty"><div class="empty-title">Test your {sport.lower()} knowledge</div>'
                    '<p>Five multiple-choice questions, one at a time, with a score at the end.</p></div>',
                    unsafe_allow_html=True)
        st.button(f"Start the {sport} quiz", key="startquiz", on_click=queue,
                  args=(f"Start a 5-question {sport} trivia quiz. One question at a time.",))
    else:
        st.markdown(f'<div class="empty"><div class="empty-title">{topic} in {sport.lower()}</div>'
                    '<p>Pick a starter or type your own question below.</p></div>', unsafe_allow_html=True)
        with st.container(key="starters"):
            cols = st.columns(2)
            for i, q in enumerate(STARTERS[sport][topic]):
                cols[i % 2].button(q, key=f"starter_{i}", on_click=queue, args=(q,), use_container_width=True)

# ---------- history ----------
last = len(ss.messages) - 1
for i, m in enumerate(ss.messages):
    with st.chat_message(m["role"], avatar=icon if m["role"] == "assistant" else ":material/person:"):
        st.markdown(m["content"])
        if m.get("file_name") and m["role"] == "user":
            st.markdown(f'<span class="attach">Attached: {m["file_name"]}</span>', unsafe_allow_html=True)
        if i == last and m["role"] == "assistant" and not m.get("blocked") and not ss.generate:
            c1, c2, c3, _ = st.columns([1.3, 1.1, 1.4, 1.6])
            c1.button("Show example", key="qa_ex", on_click=queue, args=("Show me one real-game example of that.",))
            c2.button("Quiz me", key="qa_quiz", on_click=start_quiz)
            c3.button("Explain simpler", key="qa_simple", on_click=queue, args=("Explain that again in simpler words.",))

# ---------- generate ----------
if ss.generate:
    ss.generate = False
    client = get_client()
    token = defenses.new_token()
    with st.chat_message("assistant", avatar=icon):
        box, reply = st.empty(), ""
        try:
            last_user = ss.messages[-1]["content"].lower()
            topic_now = "Quiz" if "quiz" in last_user else topic
            live_data = None
            if topic_now == "Stats" or (topic_now != "Quiz" and stats.HINT.search(last_user)):
                with st.spinner("Fetching live stats…"):
                    route = stats.route_question(client, sport, ss.messages[-1]["content"], model)
                    live_data = stats.fetch_live_data(sport, route, get_vb_key())
            stream = client.chat.completions.create(
                model=model, temperature=temperature,
                max_tokens=900 if live_data else 500, stream=True,
                messages=build_messages(topic_now, level, token, live_data),
            )
            for chunk in stream:
                reply += chunk.choices[0].delta.content or ""
                reply, stop = trim_runaway(reply)
                box.markdown(reply + "▌")
                if stop:
                    break
        except Exception as e:
            detail = str(e).replace(os.environ.get("GROQ_API_KEY", "\x00"), "***")[:300]
            reply = f"I couldn't reach the AI service just now.\n\nError: `{type(e).__name__}` {detail}"
        if defenses.leaked(reply):
            reply = defenses.LEAK_REPLY
        box.markdown(reply)
    ss.messages.append({"role": "assistant", "content": reply})
    st.rerun()
