"""CourtSense: a sports rules and stats helper (Streamlit + Groq)."""
import io
import os
import re

import streamlit as st
from groq import Groq

import defenses
from prompts import build_system_prompt
from styles import CSS

st.set_page_config(page_title="CourtSense", page_icon=":material/sports_basketball:", layout="centered")
st.markdown(CSS, unsafe_allow_html=True)

SPORTS = ["Basketball", "Volleyball", "Football", "More"]
OTHER_SPORTS = ["Tennis", "Badminton", "Baseball", "Table tennis", "Rugby", "Cricket", "Athletics", "Swimming"]
TOPICS = ["Rules", "Strategy", "Stats", "Quiz", "Watch-along"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]
MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
AVATARS = {
    "Basketball": ":material/sports_basketball:",
    "Volleyball": ":material/sports_volleyball:",
    "Football": ":material/sports_soccer:",
}
PLACEHOLDERS = {
    "Rules": "Ask about a rule, foul, or penalty",
    "Strategy": "Ask about a play or formation",
    "Stats": "Ask about a stat, or press + to attach a box score",
    "Quiz": "Type your answer, or ask for a new question",
    "Watch-along": "Describe what just happened",
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

# ---------- state ----------
ss = st.session_state
ss.setdefault("messages", [])
ss.setdefault("queued", None)
ss.setdefault("generate", False)


def queue(text):
    ss.queued = text


def current_sport():
    s = ss.get("sport") or "Basketball"
    return ss.get("more_sport", OTHER_SPORTS[0]) if s == "More" else s


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


def build_messages(sport, topic, level, token):
    msgs = [{"role": "system",
             "content": build_system_prompt(sport, topic, level, token, defenses.CANARY)}]
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
    lines = ["# CourtSense chat", ""]
    for m in ss.messages:
        who = "You" if m["role"] == "user" else "CourtSense"
        lines += [f"**{who}:** {m['content']}", ""]
    return "\n".join(lines)


# ---------- sidebar ----------
with st.sidebar:
    st.subheader("Game settings")
    level = st.radio("Detail level", LEVELS, key="level")
    model_options = list_chat_models(get_client())
    model = st.selectbox("Model", model_options, index=default_model_index(model_options), key="model")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.4, 0.1, key="temp",
                            help="Lower is more consistent. Higher is more varied.")
    st.divider()
    st.download_button("Export chat", export_markdown(), "courtsense_chat.md",
                       disabled=not ss.messages, use_container_width=True)
    if st.button("New game (clear chat)", use_container_width=True):
        ss.messages, ss.queued, ss.generate = [], None, False
        st.rerun()
    st.caption("CourtSense explains rules, plays and stats. It does not give betting "
               "tips, and it only uses numbers you provide.")

sport = current_sport()
topic = ss.get("topic") or "Rules"

# ---------- input ----------
value = st.chat_input(PLACEHOLDERS[topic], accept_file=True,
                      file_type=["txt", "csv", "md", "pdf"])
text, files = None, []
if value:
    text = (getattr(value, "text", None) or "").strip()
    files = list(getattr(value, "files", None) or [])
if ss.queued:
    text, files, ss.queued = ss.queued, [], None

if text or files:
    text = (text or "Summarize this game from the attached data.")[: defenses.MAX_INPUT_CHARS]
    attachment, blocked, reason = None, False, None
    safe, _ = defenses.check_input(text)
    if not safe:
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
        ss.messages.append({"role": "assistant", "content": reason or defenses.BLOCKED_REPLY,
                            "blocked": True})
    else:
        ss.generate = True

# ---------- header ----------
st.markdown(
    f"""<div class="board">
      <div class="brand">CourtSense<small>Rules, plays and stats, explained.</small></div>
      <div class="cells">
        <div class="cell"><span class="k">Sport</span><span class="v">{sport}</span></div>
        <div class="cell"><span class="k">Topic</span><span class="v">{topic}</span></div>
        <div class="cell"><span class="k">Level</span><span class="v">{level}</span></div>
      </div></div>""",
    unsafe_allow_html=True,
)
st.pills("Sport", SPORTS, default="Basketball", key="sport", label_visibility="collapsed")
if ss.get("sport") == "More":
    st.selectbox("Pick a sport", OTHER_SPORTS, key="more_sport", label_visibility="collapsed")
st.pills("Topic", TOPICS, default="Rules", key="topic", label_visibility="collapsed")

icon = AVATARS.get(sport, ":material/sports:")

# ---------- empty state ----------
if not ss.messages:
    if topic == "Watch-along":
        st.markdown('<p class="hint">Describe what just happened, like "the ref whistled the '
                    'point guard after two steps", and I will explain the call.</p>',
                    unsafe_allow_html=True)
    elif topic == "Quiz":
        st.markdown('<p class="hint">Five questions, one at a time.</p>', unsafe_allow_html=True)
        st.button(f"Start a {sport} quiz", on_click=queue,
                  args=(f"Start a 5-question {sport} trivia quiz. One question at a time.",))
    else:
        options = STARTERS.get(sport, {}).get(topic) or [f"Give me a beginner's guide to {sport}"]
        st.markdown('<p class="hint">Try one of these, or type your own question.</p>', unsafe_allow_html=True)
        for i, q in enumerate(options):
            st.markdown('<div class="starter">', unsafe_allow_html=True)
            st.button(q, key=f"starter_{i}", on_click=queue, args=(q,))
            st.markdown("</div>", unsafe_allow_html=True)

# ---------- history ----------
last = len(ss.messages) - 1
for i, m in enumerate(ss.messages):
    with st.chat_message(m["role"], avatar=icon if m["role"] == "assistant" else ":material/person:"):
        st.markdown(m["content"])
        if m.get("file_name") and m["role"] == "user":
            st.markdown(f'<span class="attach">Attached: {m["file_name"]}</span>', unsafe_allow_html=True)
        if i == last and m["role"] == "assistant" and not m.get("blocked") and not ss.generate:
            c1, c2, c3, _ = st.columns([1.2, 1, 1.2, 2])
            c1.button("Show example", key="qa_ex", on_click=queue,
                      args=("Show me one real-game example of that.",))
            c2.button("Quiz me", key="qa_quiz", on_click=queue,
                      args=("Quiz me on this, one question at a time.",))
            c3.button("Explain simpler", key="qa_simple", on_click=queue,
                      args=("Explain that again in simpler words.",))

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
            stream = client.chat.completions.create(
                model=model, temperature=temperature, max_tokens=500, stream=True,
                messages=build_messages(sport, topic_now, level, token),
            )
            for chunk in stream:
                reply += chunk.choices[0].delta.content or ""
                reply, stop = trim_runaway(reply)
                box.markdown(reply + "▌")
                if stop:
                    break
        except Exception as e:
            detail = str(e).replace(os.environ.get("GROQ_API_KEY", "\x00"), "***")[:300]
            reply = ("I couldn't reach the AI service just now.\n\n"
                     f"Error: `{type(e).__name__}` {detail}")
        if defenses.leaked(reply):
            reply = defenses.LEAK_REPLY
        box.markdown(reply)
    ss.messages.append({"role": "assistant", "content": reply})
    st.rerun()
