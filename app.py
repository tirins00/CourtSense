"""CourtSense: a sports rules and stats helper (Streamlit + Groq)."""
import base64
import html
import inspect
import io
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote

# Ensure local imports (defenses, prompts, styles) resolve regardless of current working directory
_app_dir = Path(__file__).parent.resolve()
if str(_app_dir) not in sys.path:
    sys.path.insert(0, str(_app_dir))

import streamlit as st
from groq import Groq

import defenses
from prompts import build_system_prompt
from styles import get_css

_SUPPORTS_INLINE_JS = "unsafe_allow_javascript" in inspect.signature(st.html).parameters

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
ss.setdefault("queued_reply_to", None)
ss.setdefault("reply_idx", None)
ss.setdefault("generate", False)
ss.setdefault("sport", SPORTS[0])
ss.setdefault("topic", TOPICS[0])


sport = ss.sport
topic = ss.topic
dark = ss.get("dark", False)
thread_key = f"{sport}|{topic}"
ss.messages = ss.threads.setdefault(thread_key, [])   # each sport + topic has its own chat

st.markdown(get_css(sport, topic, dark), unsafe_allow_html=True)

_ACTION_SCRIPT = """
<div class="cs-script-host" style="display:none" aria-hidden="true"></div>
<script>
(function () {
  if (window.__csActionsBound) return;
  window.__csActionsBound = true;

  function decodeB64(b64) {
    if (!b64) return "";
    const bin = atob(b64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new TextDecoder("utf-8").decode(bytes);
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).catch(() => fallbackCopy(text));
    }
    return fallbackCopy(text);
  }

  function fallbackCopy(text) {
    return new Promise((resolve, reject) => {
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand("copy");
        resolve();
      } catch (e) {
        reject(e);
      } finally {
        document.body.removeChild(ta);
      }
    });
  }

  function setNativeValue(el, value) {
    const proto = el.tagName === "TEXTAREA"
      ? window.HTMLTextAreaElement.prototype
      : window.HTMLInputElement.prototype;
    const setter = Object.getOwnPropertyDescriptor(proto, "value")?.set;
    if (setter) setter.call(el, value);
    else el.value = value;
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function flashButton(btn, label, ms) {
    const span = btn.querySelector(".cs-btn-label");
    if (!span) return;
    if (!btn.dataset.origLabel) btn.dataset.origLabel = span.textContent;
    span.textContent = label;
    btn.classList.add("is-done");
    clearTimeout(btn._csTimer);
    btn._csTimer = setTimeout(() => {
      span.textContent = btn.dataset.origLabel;
      btn.classList.remove("is-done");
    }, ms || 1900);
  }

  function findTargetInput(btn) {
    const card = btn.closest('[data-testid="stChatMessage"]');
    if (card) {
      const inlineInput = card.querySelector('[data-testid="stTextInputField"]');
      if (inlineInput && !inlineInput.disabled) return inlineInput;
    }
    const chatInput = document.querySelector('[data-testid="stChatInputTextArea"]');
    if (chatInput && !chatInput.disabled) return chatInput;
    return null;
  }

  document.addEventListener("click", async function (e) {
    const btn = e.target.closest("[data-cs-action]");
    if (!btn) {
      if (!e.target.closest(".cs-share-menu")) {
        document.querySelectorAll(".cs-share-menu.is-open").forEach((m) => m.classList.remove("is-open"));
      }
      return;
    }

    const action = btn.dataset.csAction;

    if (action === "copy") {
      const text = decodeB64(btn.dataset.payload);
      try {
        await copyText(text);
        flashButton(btn, "Copied!");
      } catch (_) {
        flashButton(btn, "Copy failed");
      }
      return;
    }

    if (action === "paste") {
      const target = findTargetInput(btn);
      if (!target) {
        flashButton(btn, "No input open");
        return;
      }
      target.focus();
      target.scrollIntoView({ behavior: "smooth", block: "nearest" });
      if (navigator.clipboard && navigator.clipboard.readText) {
        try {
          const clip = (await navigator.clipboard.readText()) || "";
          if (clip.trim()) {
            const cur = target.value || "";
            const next = cur ? cur.trimEnd() + " " + clip.trim() : clip.trim();
            setNativeValue(target, next);
            flashButton(btn, "Pasted!");
          } else {
            flashButton(btn, "Clipboard empty");
          }
          return;
        } catch (_) {
          // Fall through to helpful prompt
        }
      }
      const isTouch = "ontouchstart" in window || navigator.maxTouchPoints > 0;
      flashButton(btn, isTouch ? "Tap & paste" : "Press Ctrl+V", 2200);
      return;
    }

    if (action === "share") {
      const wrap = btn.closest(".cs-actions-wrap");
      const menu = wrap ? wrap.querySelector(".cs-share-menu") : null;
      const isMobile = /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent);
      if (isMobile && navigator.share) {
        try {
          await navigator.share({
            title: decodeB64(btn.dataset.title),
            text: decodeB64(btn.dataset.shareText),
          });
          flashButton(btn, "Shared!");
          return;
        } catch (err) {
          if (err && err.name === "AbortError") return;
        }
      }
      if (menu) {
        const willOpen = !menu.classList.contains("is-open");
        document.querySelectorAll(".cs-share-menu.is-open").forEach((m) => m.classList.remove("is-open"));
        if (willOpen) menu.classList.add("is-open");
      }
      return;
    }

    if (action === "share-native" && navigator.share) {
      try {
        await navigator.share({
          title: decodeB64(btn.dataset.title),
          text: decodeB64(btn.dataset.shareText),
        });
      } catch (_) {}
      return;
    }

    if (action === "share-copy") {
      const text = decodeB64(btn.dataset.shareText);
      try {
        await copyText(text);
        flashButton(btn, "Copied Q&A!");
      } catch (_) {
        flashButton(btn, "Copy failed");
      }
      return;
    }

    if (action === "share-download") {
      const text = decodeB64(btn.dataset.shareText);
      const filename = btn.dataset.filename || "courtsense_answer.md";
      const blob = new Blob([text], { type: "text/markdown;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      flashButton(btn, "Saved!");
      return;
    }
  });
})();
</script>
"""

if _SUPPORTS_INLINE_JS:
    st.html(_ACTION_SCRIPT, unsafe_allow_javascript=True)


def _b64(text):
    return base64.b64encode((text or "").encode("utf-8")).decode("ascii")


def extract_followup(text):
    """Extract the short trailing follow-up question from an assistant response."""
    lines = [ln.strip() for ln in (text or "").strip().splitlines() if ln.strip()]
    if not lines:
        return None
    last_line = lines[-1]
    parts = re.split(r"(?<=[.!?])\s+", last_line)
    candidate = parts[-1].strip().strip("*_ ")
    if candidate.endswith("?") and 12 <= len(candidate) <= 115:
        return candidate
    return None


def _short_snippet(text, limit=95):
    clean = re.sub(r"\s+", " ", (text or "")).strip()
    return clean if len(clean) <= limit else clean[: limit - 1].rstrip() + "…"


def render_user_copy_bar(text):
    """Subtle inline Copy button inside a user prompt bubble."""
    if not _SUPPORTS_INLINE_JS:
        return
    payload = _b64(text)
    bar = (
        '<div class="cs-user-actions">'
        f'<button type="button" class="cs-user-copy" data-cs-action="copy" data-payload="{payload}" '
        'title="Copy prompt" aria-label="Copy prompt">'
        '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>'
        '<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>'
        '</svg>'
        '<span class="cs-btn-label">Copy</span>'
        '</button>'
        '</div>'
    )
    st.html(bar, unsafe_allow_javascript=True)


def render_assistant_actions(idx, text, question):
    """Render responsive Copy, Paste, and Share controls inside an assistant card."""
    share_title = f"CourtSense · {sport} ({topic})"
    if question:
        share_body = f"Q: {question}\n\nA: {text}\n\n— {share_title}"
    else:
        share_body = f"{text}\n\n— {share_title}"
    filename = f"courtsense_{sport}_{topic}_{idx + 1}.md".lower().replace(" ", "_")

    if not _SUPPORTS_INLINE_JS:
        with st.popover("Copy & Share", icon=":material/share:"):
            st.code(text, language=None)
            st.download_button(
                "Save .md",
                share_body,
                file_name=filename,
                key=f"dl_ans_{idx}",
                use_container_width=True,
            )
        return

    payload = _b64(text)
    share_b64 = _b64(share_body)
    title_b64 = _b64(share_title)
    encoded_wa = quote(share_body[:1200])
    encoded_x = quote(f"{_short_snippet(text, 220)}\n\n— {share_title}")
    encoded_subj = quote(share_title)
    encoded_mail = quote(share_body[:1600])

    bar = (
        '<div class="cs-actions-wrap">'
        '<div class="cs-actions">'
        f'<button type="button" class="cs-act-btn" data-cs-action="copy" data-payload="{payload}" '
        'title="Copy answer to clipboard" aria-label="Copy answer">'
        '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>'
        '<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>'
        '</svg>'
        '<span class="cs-btn-label">Copy</span>'
        '</button>'
        '<button type="button" class="cs-act-btn" data-cs-action="paste" '
        'title="Paste clipboard into reply or chat bar" aria-label="Paste into input">'
        '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>'
        '<rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>'
        '</svg>'
        '<span class="cs-btn-label">Paste</span>'
        '</button>'
        f'<button type="button" class="cs-act-btn" data-cs-action="share" '
        f'data-title="{title_b64}" data-share-text="{share_b64}" '
        'title="Share this answer" aria-label="Share answer">'
        '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="18" cy="5" r="3"></circle>'
        '<circle cx="6" cy="12" r="3"></circle>'
        '<circle cx="18" cy="19" r="3"></circle>'
        '<line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>'
        '<line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>'
        '</svg>'
        '<span class="cs-btn-label">Share</span>'
        '</button>'
        '</div>'
        '<div class="cs-share-menu" role="menu" aria-label="Share options">'
        f'<button type="button" class="cs-share-item" data-cs-action="share-copy" data-share-text="{share_b64}">'
        '<span class="cs-btn-label">Copy Q&amp;A</span></button>'
        f'<a class="cs-share-item" href="https://wa.me/?text={encoded_wa}" target="_blank" rel="noopener noreferrer">WhatsApp</a>'
        f'<a class="cs-share-item" href="https://twitter.com/intent/tweet?text={encoded_x}" target="_blank" rel="noopener noreferrer">X</a>'
        f'<a class="cs-share-item" href="mailto:?subject={encoded_subj}&amp;body={encoded_mail}">Email</a>'
        f'<button type="button" class="cs-share-item" data-cs-action="share-download" '
        f'data-share-text="{share_b64}" data-filename="{html.escape(filename)}">'
        '<span class="cs-btn-label">Save .md</span></button>'
        '</div>'
        '</div>'
    )
    st.html(bar, unsafe_allow_javascript=True)


def queue(text, reply_to=None):
    ss.queued = text
    ss.queued_reply_to = reply_to
    ss.reply_idx = None


def toggle_reply(idx):
    ss.reply_idx = None if ss.reply_idx == idx else idx


def set_sport(name):
    ss.sport = name
    ss.reply_idx = None


def set_topic(name):
    ss.topic = name
    ss.reply_idx = None


def start_quiz():
    """Jump to the Quiz tab for this sport and start a quiz there."""
    ss.topic = "Quiz"
    ss.queued = f"Start a 5-question {ss.sport} trivia quiz. One question at a time."
    ss.queued_reply_to = None
    ss.reply_idx = None


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
            user_text = m["content"]
            if m.get("reply_to"):
                user_text = f'(Follow-up to your earlier answer: "{m["reply_to"]}")\n{user_text}'
            wrapped = defenses.wrap_user(user_text, token, m["attachment"] if i == last_att else None)
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
        ss.queued, ss.queued_reply_to, ss.reply_idx, ss.generate = None, None, None, False
        st.rerun()
    st.divider()
    st.caption("Each sport and topic keeps its own chat. CourtSense explains rules, plays and "
               "stats. It does not give betting tips, and it only uses numbers you provide.")

# ---------- input ----------
value = st.chat_input(PLACEHOLDERS[topic], accept_file=True, file_type=["txt", "csv", "md", "pdf"])
text, files, reply_to = None, [], None
if value:
    text = (getattr(value, "text", None) or "").strip()
    files = list(getattr(value, "files", None) or [])
if ss.queued:
    text, files, ss.queued = ss.queued, [], None
    reply_to, ss.queued_reply_to = ss.queued_reply_to, None

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
    ss.messages.append({
        "role": "user",
        "content": text,
        "attachment": attachment,
        "file_name": files[0].name if files else None,
        "reply_to": reply_to,
        "blocked": blocked,
    })
    if blocked or reason:
        ss.messages.append({"role": "assistant", "content": reason or defenses.BLOCKED_REPLY, "blocked": True})
    else:
        ss.generate = True

# ---------- hero: title, sport buttons, topic tabs ----------
with st.container(key="hero"):
    with st.container(key="hero_top"):
        c1, c2 = st.columns([3, 1.4], vertical_alignment="center")
        c1.markdown('<div class="wordmark-wrap"><span class="wordmark-badge">SPORTS INTEL</span><span class="wordmark">CourtSense</span></div>', unsafe_allow_html=True)
        c2.toggle("Dark mode", key="dark")
    st.markdown(f'<div class="hero-title">{sport}</div>'
                f'<div class="hero-sub"><span class="sub-pill">{topic}</span><span class="sub-text">{TAGLINES[topic]}</span></div>',
                unsafe_allow_html=True)
    with st.container(key="sports_row"):
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
    is_user = m["role"] == "user"
    with st.chat_message(m["role"], avatar=icon if not is_user else ":material/person:"):
        if is_user and m.get("reply_to"):
            st.markdown(
                f'<div class="reply-ref">Replying to: &ldquo;{html.escape(m["reply_to"])}&rdquo;</div>',
                unsafe_allow_html=True,
            )
        st.markdown(m["content"])
        if is_user:
            if m.get("file_name"):
                st.markdown(
                    f'<span class="attach">Attached: {html.escape(m["file_name"])}</span>',
                    unsafe_allow_html=True,
                )
            render_user_copy_bar(m["content"])
        elif not ss.generate:
            prev_q = ss.messages[i - 1]["content"] if i > 0 and ss.messages[i - 1]["role"] == "user" else ""
            render_assistant_actions(i, m["content"], prev_q)

            if not m.get("blocked"):
                is_latest = i == last
                snippet = _short_snippet(m["content"], 95)

                if is_latest:
                    followup_q = extract_followup(m["content"])
                    st.markdown('<div class="followup-label">FOLLOW UP</div>', unsafe_allow_html=True)
                    if followup_q and "quiz" not in followup_q.lower():
                        with st.container(key="qa_ai_followup"):
                            st.button(
                                followup_q,
                                key="qa_suggested",
                                icon=":material/subdirectory_arrow_right:",
                                on_click=queue,
                                args=(f"Yes — {followup_q}",),
                                use_container_width=True,
                            )
                    with st.container(key="qa_chips"):
                        c1, c2, c3 = st.columns(3)
                        c1.button("Show example", key="qa_ex", icon=":material/visibility:", on_click=queue,
                                  args=("Show me one real-game example of that.",), use_container_width=True)
                        c2.button("Explain simpler", key="qa_simple", icon=":material/lightbulb:", on_click=queue,
                                  args=("Explain that again in simpler words.",), use_container_width=True)
                        c3.button("Quiz me", key="qa_quiz", icon=":material/quiz:", on_click=start_quiz,
                                  use_container_width=True)

                    with st.container(key=f"followup_box_{i}"):
                        with st.form(key=f"followup_form_{i}", clear_on_submit=True, border=False):
                            fc1, fc2 = st.columns([5.2, 1.3], vertical_alignment="center")
                            follow_val = fc1.text_input(
                                "Reply or follow up",
                                placeholder="Reply or ask a follow-up about this…",
                                label_visibility="collapsed",
                                key=f"followup_in_{i}",
                            )
                            sent = fc2.form_submit_button("Reply", icon=":material/send:", use_container_width=True)
                        if sent and follow_val and follow_val.strip():
                            queue(follow_val.strip())
                            st.rerun()
                else:
                    is_open = ss.reply_idx == i
                    with st.container(key=f"reply_toggle_{i}"):
                        st.button(
                            "Close reply" if is_open else "Reply",
                            key=f"reply_btn_{i}",
                            icon=":material/close:" if is_open else ":material/reply:",
                            on_click=toggle_reply,
                            args=(i,),
                        )
                    if is_open:
                        with st.container(key=f"followup_box_{i}"):
                            with st.form(key=f"followup_form_{i}", clear_on_submit=True, border=False):
                                fc1, fc2 = st.columns([5.2, 1.3], vertical_alignment="center")
                                follow_val = fc1.text_input(
                                    "Reply to this answer",
                                    placeholder="Ask a follow-up about this answer…",
                                    label_visibility="collapsed",
                                    key=f"followup_in_{i}",
                                )
                                sent = fc2.form_submit_button("Reply", icon=":material/send:", use_container_width=True)
                            if sent and follow_val and follow_val.strip():
                                queue(follow_val.strip(), reply_to=snippet)
                                st.rerun()

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
