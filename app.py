"""CourtSense: a sports rules and stats helper (Streamlit + OpenAI / Groq)."""
import base64
import html
import inspect
import io
import json
import os
import random
import re
import sys
from pathlib import Path
from urllib.parse import quote

# Ensure local imports (defenses, prompts, styles) resolve regardless of current working directory
_app_dir = Path(__file__).parent.resolve()
if str(_app_dir) not in sys.path:
    sys.path.insert(0, str(_app_dir))

import streamlit as st

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from groq import Groq
except ImportError:
    Groq = None

import defenses
import stats
from prompts import build_quiz_prompt, build_system_prompt
from styles import brand_logo_svg, get_css, loading_ball_html

_SUPPORTS_INLINE_JS = "unsafe_allow_javascript" in inspect.signature(st.html).parameters
_SELECTBOX_NO_TYPE = {"filter_mode": None} if "filter_mode" in inspect.signature(st.selectbox).parameters else {}

st.set_page_config(
    page_title="CourtSense",
    page_icon=brand_logo_svg(st.session_state.get("sport", "Basketball"), st.session_state.get("dark", False)),
    layout="centered",
)

SPORTS = ["Basketball", "Volleyball", "Football"]
TOPICS = ["Rules", "Strategy", "Stats", "Quiz"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]
OPENAI_BASE_URL = "https://aiki-labs.up.railway.app/api/v1"
OPENAI_MAX_COMPLETION_TOKENS = 800
OPENAI_MODELS = [
    "gpt-6-luna",
]
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "qwen/qwen3-32b",
]
MODELS = OPENAI_MODELS
PROVIDER_LABELS = {
    "openai": "OpenAI",
    "groq": "Groq",
}
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
QUIZ_LEN = 5
QUIZ_THEMES = {
    "Basketball": [
        "scoring and point values", "personal and technical fouls", "travelling and dribbling violations",
        "shot clock and game timing", "court dimensions and markings", "player positions and roles",
        "NBA history and founding", "FIBA vs NBA rule differences", "all-time records and milestones",
        "offensive plays (pick and roll, give and go)", "defensive schemes (zone, man-to-man)",
        "box score stats and terminology", "referee signals", "Olympic and international basketball",
        "WNBA history", "free throws and bonus situations", "the NBA Draft and awards",
    ],
    "Volleyball": [
        "rotation rules", "rally scoring and set length", "libero rules", "net and centre-line faults",
        "serving rules", "player positions and roles", "attacking and blocking rules",
        "beach vs indoor volleyball", "history and invention of volleyball", "Olympic volleyball",
        "stats terminology (kills, digs, aces)", "court dimensions", "substitutions and timeouts",
        "ball-handling faults (lift, double contact)", "offensive systems (5-1, 6-2)",
        "referee signals", "FIVB competitions",
    ],
    "Football": [
        "the offside rule", "fouls, yellow and red cards", "set pieces (free kicks, corners)",
        "VAR and refereeing", "formations and tactics", "FIFA World Cup history",
        "European club competitions", "player positions and roles", "goalkeeper rules",
        "match duration, stoppage time and extra time", "penalty shootouts",
        "stats terminology (xG, assists, clean sheets)", "pitch dimensions and markings",
        "all-time records and legends", "substitution rules", "the Laws of the Game and IFAB",
        "continental tournaments (Euros, Copa America, AFCON)",
    ],
}
LETTERS = "ABCD"

ss = st.session_state
ss.setdefault("threads", {})
ss.setdefault("queued", None)
ss.setdefault("queued_reply_to", None)
ss.setdefault("reply_idx", None)
ss.setdefault("generate", False)
ss.setdefault("sport", SPORTS[0])
ss.setdefault("topic", TOPICS[0])
ss.setdefault("quizzes", {})       # sport -> active quiz state
ss.setdefault("quiz_pending", {})  # sport -> True when a new quiz should be generated
ss.setdefault("quiz_error", {})    # sport -> last generation error
ss.setdefault("quiz_seen", {})     # sport -> recent question texts (avoid repeats)
ss.setdefault("unavailable_models", set())  # models that returned 404 model_not_found

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
  if (window.__csActionsBoundV2) return;
  window.__csActionsBoundV2 = true;

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
    // Icon-only buttons show feedback as a small tooltip (data-tip); labelled buttons swap text.
    const span = btn.querySelector(".cs-btn-label");
    btn.dataset.tip = label;
    if (span) {
      if (!btn.dataset.origLabel) btn.dataset.origLabel = span.textContent;
      span.textContent = label;
    }
    btn.classList.add("is-done");
    clearTimeout(btn._csTimer);
    btn._csTimer = setTimeout(() => {
      if (span) span.textContent = btn.dataset.origLabel;
      btn.classList.remove("is-done");
    }, ms || 1900);
  }

  function findTargetInput() {
    const selectors = [
      '[role="dialog"] [data-testid="stTextInputField"]',
      '[role="dialog"] input[type="text"]',
      '[data-testid="stChatInputTextArea"]',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el && !el.disabled) return el;
    }
    return null;
  }

  // Capture phase on window so this runs first and stops older cached handlers from double-firing.
  window.addEventListener("click", async function (e) {
    const btn = e.target.closest("[data-cs-action]");
    if (!btn) {
      if (!e.target.closest(".cs-share-menu")) {
        document.querySelectorAll(".cs-share-menu.is-open").forEach((m) => m.classList.remove("is-open"));
      }
      return;
    }
    e.stopPropagation();

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
      const target = findTargetInput();
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
  }, true);
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
        '<span class="cs-ic cs-ic-copy-light" aria-hidden="true"></span>'
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
        f'<button type="button" class="cs-act-btn cs-icon-btn" data-cs-action="copy" data-payload="{payload}" '
        'title="Copy answer" aria-label="Copy answer"><span class="cs-ic cs-ic-copy" aria-hidden="true"></span></button>'
        '<button type="button" class="cs-act-btn cs-icon-btn" data-cs-action="paste" '
        'title="Paste clipboard into the chat bar" aria-label="Paste into input"><span class="cs-ic cs-ic-paste" aria-hidden="true"></span></button>'
        f'<button type="button" class="cs-act-btn cs-icon-btn" data-cs-action="share" '
        f'data-title="{title_b64}" data-share-text="{share_b64}" '
        'title="Share answer" aria-label="Share answer"><span class="cs-ic cs-ic-share" aria-hidden="true"></span></button>'
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
    st.html(bar, width="content", unsafe_allow_javascript=True)


@st.dialog("Reply or follow up", width="medium")
def reply_dialog(idx):
    """Pop-up text box for replying to (or following up on) an assistant answer."""
    msg = ss.messages[idx]
    is_latest = idx == len(ss.messages) - 1
    snippet = _short_snippet(msg["content"], 95)
    st.markdown(
        f'<div class="reply-quote">Replying to: &ldquo;{html.escape(snippet)}&rdquo;</div>',
        unsafe_allow_html=True,
    )
    with st.container(key=f"followup_box_{idx}"):
        with st.form(key=f"followup_form_{idx}", clear_on_submit=True, border=False):
            fc1, fc2 = st.columns([5.2, 1.3], vertical_alignment="center")
            follow_val = fc1.text_input(
                "Your reply",
                placeholder="Ask a follow-up about this answer…",
                label_visibility="collapsed",
                key=f"followup_in_{idx}",
            )
            sent = fc2.form_submit_button("Send", icon=":material/send:", use_container_width=True)
    if sent and follow_val and follow_val.strip():
        queue(follow_val.strip(), reply_to=None if is_latest else snippet)
        st.rerun()


def render_message_tools(idx, msg):
    """Icon toolbar (copy / paste / share) and a Reply button, shown below an assistant card."""
    prev_q = ss.messages[idx - 1]["content"] if idx > 0 and ss.messages[idx - 1]["role"] == "user" else ""
    with st.container(key=f"tools_{idx}", horizontal=True, vertical_alignment="center", gap="small"):
        render_assistant_actions(idx, msg["content"], prev_q)
        if not msg.get("blocked"):
            if st.button("Reply", key=f"reply_btn_{idx}", icon=":material/reply:",
                         help="Reply or ask a follow-up about this answer"):
                reply_dialog(idx)


def queue(text, reply_to=None):
    ss.queued = text
    ss.queued_reply_to = reply_to
    ss.reply_idx = None


def set_sport(name):
    ss.sport = name
    ss.reply_idx = None


def set_topic(name):
    ss.topic = name
    ss.reply_idx = None


def start_quiz():
    """Jump to the Quiz tab for this sport and generate a fresh, random quiz."""
    ss.topic = "Quiz"
    ss.quiz_pending[ss.sport] = True
    ss.quiz_error.pop(ss.sport, None)
    ss.reply_idx = None


def answer_quiz(choice):
    quiz = ss.quizzes.get(ss.sport)
    if not quiz or len(quiz["picks"]) > quiz["idx"]:
        return
    quiz["picks"].append(choice)
    if choice == quiz["questions"][quiz["idx"]]["answer"]:
        quiz["score"] += 1


def next_question():
    quiz = ss.quizzes.get(ss.sport)
    if quiz:
        quiz["idx"] += 1


def _strip_letter(text):
    return re.sub(r"^\(?[A-Da-d][\).:]\s+", "", str(text or "")).strip()


def parse_quiz(raw, n):
    """Validate the model's JSON quiz and shuffle answer positions."""
    cleaned = re.sub(r"<think>.*?</think>", "", raw or "", flags=re.S).strip()
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.I).strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}|\[.*\]", cleaned, re.S)
        if not m:
            raise ValueError("The model returned a quiz I couldn't read. Try again.")
        data = json.loads(m.group(0))
    items = data.get("questions", []) if isinstance(data, dict) else data
    out = []
    for item in items or []:
        if not isinstance(item, dict):
            continue
        question = str(item.get("question", "")).strip()
        options = [_strip_letter(o) for o in (item.get("options") or []) if str(o).strip()]
        ans = item.get("answer")
        idx = None
        if isinstance(ans, int) and 0 <= ans < len(options):
            idx = ans
        else:
            a = _strip_letter(ans)
            lowered = [o.lower() for o in options]
            if a.lower() in lowered:
                idx = lowered.index(a.lower())
            elif len(a) == 1 and a.upper() in LETTERS[: len(options)]:
                idx = LETTERS.index(a.upper())
        if not question or len(options) != 4 or idx is None or len({o.lower() for o in options}) < 4:
            continue
        correct = options[idx]
        random.shuffle(options)
        out.append({
            "question": question,
            "options": options,
            "answer": options.index(correct),
            "explanation": str(item.get("explanation", "")).strip(),
        })
    if len(out) < 3:
        raise ValueError("The model returned a quiz I couldn't use. Try again, or pick another model.")
    return out[:n]


def generate_quiz(n=QUIZ_LEN):
    """Ask the model for n random multiple-choice questions about the current sport."""
    themes = random.sample(QUIZ_THEMES[sport], k=min(n, len(QUIZ_THEMES[sport])))
    seen = ss.quiz_seen.setdefault(sport, [])
    prompt = build_quiz_prompt(sport, level, themes, seen[-25:], random.randint(10000, 99999))
    quiz_messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Write {n} new {sport} quiz questions as JSON."},
    ]
    resp = None
    last_err = None
    for cand_provider, cand_client, cand_model in _provider_attempts(provider, model, model_options):
        max_out = OPENAI_MAX_COMPLETION_TOKENS if cand_provider == "openai" else 2000
        try:
            resp = _create_completion(
                cand_client,
                cand_provider,
                cand_model,
                quiz_messages,
                temperature=max(0.9, temperature),
                max_out=max_out,
                response_format={"type": "json_object"},
            )
            break
        except Exception as e:
            if _is_model_not_found(e):
                ss.unavailable_models.add(f"{cand_provider}:{cand_model}")
            last_err = e
            continue
    if resp is None:
        raise last_err or RuntimeError("No accessible chat model found for the configured API key(s).")
    questions = parse_quiz(resp.choices[0].message.content, n)
    seen.extend(q["question"] for q in questions)
    del seen[:-60]
    return questions


def _get_secret(name):
    """Look up a secret from st.secrets, environment variables, or local secrets.toml."""
    try:
        val = st.secrets[name]
        if val:
            return str(val).strip()
    except Exception:
        pass
    val = os.environ.get(name)
    if val:
        return val.strip()
    import tomllib
    for cand in [
        _app_dir / ".streamlit" / "secrets.toml",
        _app_dir.parent / ".streamlit" / "secrets.toml",
        _app_dir.parent.parent / ".streamlit" / "secrets.toml",
    ]:
        if cand.exists():
            try:
                with open(cand, "rb") as f:
                    found = tomllib.load(f).get(name)
                    if found:
                        return str(found).strip()
            except Exception:
                pass
    return None


def _openai_key():
    return _get_secret("OPENAI_API_KEY") or _get_secret("AIKI_API_KEY")


def _openai_base_url():
    return _get_secret("OPENAI_BASE_URL") or _get_secret("AIKI_BASE_URL") or OPENAI_BASE_URL


def _groq_key():
    return _get_secret("GROQ_API_KEY")


def available_providers():
    """Return configured LLM providers in priority order (OpenAI primary, Groq fallback)."""
    out = []
    if OpenAI is not None and _openai_key():
        out.append("openai")
    if Groq is not None and _groq_key():
        out.append("groq")
    return out


def get_client(selected_provider=None):
    providers = available_providers()
    target = selected_provider if selected_provider in providers else (providers[0] if providers else None)
    if target == "openai":
        return OpenAI(api_key=_openai_key(), base_url=_openai_base_url())
    if target == "groq":
        return Groq(api_key=_groq_key())
    st.error("No API key found. Add OPENAI_API_KEY (or optional fallback GROQ_API_KEY) to "
             ".streamlit/secrets.toml (local) or to your app's Secrets (Streamlit Community Cloud).")
    st.stop()


def get_vb_key():
    """Optional free API-Sports key for volleyball league data. None is fine."""
    return _get_secret("API_SPORTS_KEY")


def _is_model_not_found(exc):
    msg = str(exc).lower()
    return type(exc).__name__ == "NotFoundError" or "model_not_found" in msg or "does not exist" in msg


def _provider_models(selected_provider):
    return OPENAI_MODELS if selected_provider == "openai" else GROQ_MODELS


def _candidate_models(selected, options, selected_provider="openai"):
    seen, out = set(), []
    for m in [selected, *options, *_provider_models(selected_provider)]:
        key = f"{selected_provider}:{m}"
        if m and m not in seen and key not in ss.unavailable_models and m not in ss.unavailable_models:
            seen.add(m)
            out.append(m)
    return out


@st.cache_data(ttl=3600, show_spinner=False)
def _list_chat_models_cached(_client, selected_provider):
    """Ask the provider which active chat models this key can use right now."""
    skip = ("whisper", "tts", "guard", "compound", "embed", "orpheus", "safeguard", "prompt-guard", "dall-e", "moderation")
    models = _client.models.list().data
    ids = []
    for m in models:
        extra = getattr(m, "model_extra", None) or {}
        if extra.get("active") is False or getattr(m, "active", True) is False:
            continue
        if any(k in m.id.lower() for k in skip):
            continue
        ids.append(m.id)
    return sorted(ids)


def list_chat_models(client, selected_provider="openai"):
    defaults = list(_provider_models(selected_provider))
    try:
        ids = _list_chat_models_cached(client, selected_provider)
    except Exception:
        ids = list(defaults)
    if selected_provider == "openai":
        # Always include the configured default OpenAI model(s) (e.g. gpt-6-luna)
        for m in reversed(defaults):
            if m not in ids:
                ids.insert(0, m)
    usable = [
        i for i in ids
        if f"{selected_provider}:{i}" not in ss.unavailable_models and i not in ss.unavailable_models
    ]
    return usable or defaults


def default_model_index(options, selected_provider="openai"):
    prefs = (
        ("gpt-6-luna", "gpt-6", "gpt-5", "gpt-4")
        if selected_provider == "openai"
        else ("llama-3.3-70b", "gpt-oss-120b", "gpt-oss-20b", "qwen", "llama-4", "llama", "70b", "120b", "20b")
    )
    for pref in prefs:
        for i, name in enumerate(options):
            if pref in name.lower():
                return i
    return 0


def _provider_attempts(primary_provider, primary_model, primary_options):
    """Yield (provider, client, model) tuples: primary provider first, then optional Groq fallback."""
    primary_client = get_client(primary_provider)
    for m in _candidate_models(primary_model, primary_options, primary_provider):
        yield primary_provider, primary_client, m
    if primary_provider == "openai" and "groq" in available_providers():
        groq_client = get_client("groq")
        groq_options = list_chat_models(groq_client, "groq")
        groq_default = groq_options[default_model_index(groq_options, "groq")]
        for m in _candidate_models(groq_default, groq_options, "groq"):
            yield "groq", groq_client, m


def _create_completion(client, selected_provider, model_name, messages, temperature, max_out,
                       stream=False, response_format=None):
    """Call chat.completions.create with provider-appropriate token cap and safe parameter fallbacks."""
    kwargs = {"model": model_name, "messages": messages, "temperature": temperature}
    if stream:
        kwargs["stream"] = True
    if selected_provider == "openai":
        kwargs["max_completion_tokens"] = min(max_out, OPENAI_MAX_COMPLETION_TOKENS)
    else:
        kwargs["max_tokens"] = max_out

    def _invoke(extra=None):
        call_kwargs = {**kwargs, **(extra or {})}
        try:
            return client.chat.completions.create(**call_kwargs)
        except Exception as exc:
            if "temperature" in str(exc).lower() and "temperature" in call_kwargs:
                call_kwargs.pop("temperature", None)
                return client.chat.completions.create(**call_kwargs)
            raise

    if response_format is not None:
        try:
            return _invoke({"response_format": response_format})
        except Exception as exc:
            if _is_model_not_found(exc):
                raise
            return _invoke()
    return _invoke()


def _fallback_router_target(primary_provider):
    """Return a (client, model, provider) tuple for Groq fallback routing if available."""
    if primary_provider == "openai" and "groq" in available_providers():
        fb_client = get_client("groq")
        fb_opts = list_chat_models(fb_client, "groq")
        return (fb_client, fb_opts[default_model_index(fb_opts, "groq")], "groq")
    return None


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


def build_messages(topic_now, level, token, live_data=None):
    msgs = [{"role": "system",
             "content": build_system_prompt(sport, topic_now, level, token, defenses.CANARY, live_data)}]
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
    if topic == "Quiz":
        quiz = ss.quizzes.get(sport)
        if quiz:
            for n, (q, pick) in enumerate(zip(quiz["questions"], quiz["picks"]), 1):
                mark = "Correct" if pick == q["answer"] else "Wrong"
                lines += [f"**Q{n}. {q['question']}**", f"- Your answer: {q['options'][pick]} ({mark})",
                          f"- Correct answer: {q['options'][q['answer']]}", ""]
            lines.append(f"**Score: {quiz['score']} / {len(quiz['questions'])}**")
        return "\n".join(lines)
    for m in ss.messages:
        who = "You" if m["role"] == "user" else "CourtSense"
        lines += [f"**{who}:** {m['content']}", ""]
    return "\n".join(lines)


def render_quiz():
    """Button-based multiple-choice quiz for the current sport (no typing)."""
    quiz = ss.quizzes.get(sport)
    error = ss.quiz_error.get(sport)

    if not quiz:
        st.markdown(
            f'<div class="empty">'
            f'<span class="empty-badge">TRIVIA CHALLENGE</span>'
            f'<div class="empty-title">Test your {sport} IQ</div>'
            f'<p>{QUIZ_LEN} fresh multiple-choice questions, generated at random every time. '
            f'Tap an answer to lock it in.</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if error:
            st.error(error, icon=":material/error:")
        st.button("Try again" if error else f"Start the {sport} quiz", key="startquiz", on_click=start_quiz,
                  icon=":material/refresh:" if error else ":material/play_circle:",
                  use_container_width=True)
        return

    questions, idx, score = quiz["questions"], quiz["idx"], quiz["score"]
    total = len(questions)

    # ----- finished: results -----
    if idx >= total:
        pct = score / total
        verdict = ("Hall of Fame performance!" if pct == 1 else "Great game!" if pct >= 0.8
                   else "Solid effort." if pct >= 0.5 else "Keep practising, you'll get there.")
        st.markdown(
            f'<div class="quiz-result">'
            f'<span class="empty-badge">FINAL SCORE</span>'
            f'<div class="quiz-result-score">{score}<span>/ {total}</span></div>'
            f'<p>{verdict}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
        with st.expander("Review your answers", icon=":material/fact_check:"):
            for n, (q, pick) in enumerate(zip(questions, quiz["picks"]), 1):
                ok = pick == q["answer"]
                st.markdown(
                    f'<div class="quiz-review {"correct" if ok else "wrong"}">'
                    f'<div class="quiz-review-q">{n}. {html.escape(q["question"])}</div>'
                    f'<div>Your answer: {html.escape(q["options"][pick])}</div>'
                    + ("" if ok else f'<div>Correct: {html.escape(q["options"][q["answer"]])}</div>')
                    + '</div>',
                    unsafe_allow_html=True,
                )
        with st.container(key="quiz_end_actions"):
            c1, c2 = st.columns(2)
            c1.button("New random quiz", key="quiz_again", icon=":material/shuffle:", on_click=start_quiz,
                      use_container_width=True)
            c2.button("Back to Rules", key="quiz_back", icon=":material/gavel:", on_click=set_topic,
                      args=("Rules",), use_container_width=True)
        return

    # ----- in progress: one question at a time -----
    q = questions[idx]
    answered = len(quiz["picks"]) > idx
    progress = (idx + (1 if answered else 0)) / total * 100
    st.markdown(
        f'<div class="quiz-head">'
        f'<span class="quiz-count">Question {idx + 1} of {total}</span>'
        f'<span class="quiz-score">Score {score}</span>'
        f'</div>'
        f'<div class="quiz-progress"><div style="width:{progress:.0f}%"></div></div>'
        f'<div class="quiz-card"><div class="quiz-q">{html.escape(q["question"])}</div></div>',
        unsafe_allow_html=True,
    )

    if not answered:
        with st.container(key="quiz_opts"):
            cols = st.columns(2)
            for j, opt in enumerate(q["options"]):
                cols[j % 2].button(f"{LETTERS[j]}.  {opt}", key=f"quiz_opt_{idx}_{j}", on_click=answer_quiz,
                                   args=(j,), use_container_width=True)
        return

    pick = quiz["picks"][idx]
    is_right = pick == q["answer"]
    opts_html = "".join(
        f'<div class="quiz-opt{" correct" if j == q["answer"] else " wrong" if j == pick else ""}">'
        f'<span class="quiz-letter">{LETTERS[j]}</span>{html.escape(opt)}</div>'
        for j, opt in enumerate(q["options"])
    )
    st.markdown(
        f'<div class="quiz-opts-done">{opts_html}</div>'
        f'<div class="quiz-feedback {"correct" if is_right else "wrong"}">'
        f'<strong>{"Correct!" if is_right else "Not quite."}</strong> '
        f'{html.escape(q["explanation"]) if q["explanation"] else ""}</div>',
        unsafe_allow_html=True,
    )
    last_q = idx == total - 1
    st.button(
        "See results" if last_q else "Next question",
        key="quiz_results" if last_q else "quiz_next",
        on_click=next_question,
        use_container_width=True,
    )


# ---------- sidebar ----------
with st.sidebar:
    st.markdown(
        '<div class="sidebar-header">'
        '<span class="sidebar-badge">PREFERENCES</span>'
        '<h3 style="margin-top:6px;margin-bottom:0;">Settings</h3>'
        '</div>',
        unsafe_allow_html=True,
    )
    level = st.radio(
        "Detail level",
        LEVELS,
        key="level",
        help="Controls explanation depth and quiz difficulty. Beginner uses plain language, Intermediate adds sports terminology, and Advanced covers tactical detail.",
    )
    providers = available_providers()
    if not providers:
        get_client()  # displays configuration error and stops
    if len(providers) > 1:
        if ss.get("provider") not in providers:
            ss.provider = providers[0]
        provider = st.selectbox(
            "Provider",
            providers,
            format_func=lambda p: PROVIDER_LABELS.get(p, p),
            key="provider",
            help="Primary is OpenAI (Aiki Labs). Groq is used automatically as a fallback if needed.",
            **_SELECTBOX_NO_TYPE,
        )
    else:
        provider = providers[0]
    model_options = list_chat_models(get_client(provider), provider)
    if ss.get("model") not in model_options:
        ss.pop("model", None)
    model = st.selectbox(
        "Model",
        model_options,
        index=default_model_index(model_options, provider),
        key="model",
        **_SELECTBOX_NO_TYPE,
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.4, 0.1, key="temp",
                            help="Lower is more consistent. Higher is more varied.")
    st.divider()
    has_content = bool(ss.quizzes.get(sport, {}).get("picks")) if topic == "Quiz" else bool(ss.messages)
    st.download_button("Export this quiz" if topic == "Quiz" else "Export this chat", export_markdown(),
                       f"courtsense_{sport}_{topic}.md".lower(),
                       icon=":material/download:", disabled=not has_content, use_container_width=True)
    if st.button("Reset this quiz" if topic == "Quiz" else "Clear this chat", icon=":material/delete_sweep:",
                 use_container_width=True):
        if topic == "Quiz":
            ss.quizzes.pop(sport, None)
            ss.quiz_error.pop(sport, None)
            ss.quiz_pending.pop(sport, None)
        ss.threads[thread_key] = []
        ss.queued, ss.queued_reply_to, ss.reply_idx, ss.generate = None, None, None, False
        st.rerun()
    st.divider()
    st.caption("Each sport and topic keeps its own chat. CourtSense explains rules, plays and "
               "stats, with live player and league numbers from ESPN (basketball, football) and "
               "API-Sports (volleyball) when available. It does not give betting tips.")

# ---------- input (hidden in Quiz mode: the quiz is button-based) ----------
value = None
if topic != "Quiz":
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
        c1.markdown(
            '<div class="wordmark-wrap">'
            '<span class="brand-logo" role="img" aria-label="CourtSense logo"></span>'
            '<span class="wordmark">CourtSense</span>'
            '</div>',
            unsafe_allow_html=True,
        )
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

# ---------- quiz mode (button-based, replaces the chat) ----------
if topic == "Quiz":
    if ss.quiz_pending.get(sport):
        ss.quiz_pending[sport] = False
        quiz_loader = st.empty()
        quiz_loader.markdown(
            loading_ball_html(sport, f"Building a fresh {sport} quiz…", card=True),
            unsafe_allow_html=True,
        )
        try:
            ss.quizzes[sport] = {"questions": generate_quiz(), "idx": 0, "score": 0, "picks": []}
            ss.quiz_error.pop(sport, None)
        except Exception as e:
            ss.quizzes.pop(sport, None)
            detail = str(e)[:200] if isinstance(e, ValueError) else f"{type(e).__name__}"
            ss.quiz_error[sport] = f"I couldn't build a quiz just now ({detail})."
        finally:
            quiz_loader.empty()
        st.rerun()
    render_quiz()

# ---------- empty state ----------
elif not ss.messages:
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
for i, m in enumerate(ss.messages if topic != "Quiz" else []):
    is_user = m["role"] == "user"
    with st.chat_message(m["role"], avatar=icon if not is_user else "user"):
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
        elif not ss.generate and not m.get("blocked") and i == last:
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
                          args=("Show me one real-game example of that.",),
                          use_container_width=True)
                c2.button("Explain simpler", key="qa_simple", icon=":material/lightbulb:", on_click=queue,
                          args=("Explain that again in simpler words.",),
                          use_container_width=True)
                c3.button("Quiz me", key="qa_quiz", icon=":material/quiz:", on_click=start_quiz,
                          use_container_width=True)
    # Copy / paste / share icons + Reply button sit below each completed response card
    if not is_user:
        render_message_tools(i, m)

# ---------- generate ----------
if ss.generate and topic != "Quiz":
    ss.generate = False
    client = get_client(provider)
    token = defenses.new_token()
    with st.chat_message("assistant", avatar=icon):
        box, reply = st.empty(), ""
        try:
            last_user = ss.messages[-1]["content"].lower()
            topic_now = "Quiz" if "quiz" in last_user else topic
            live_data = None
            active_model = model
            box.markdown(loading_ball_html(sport, "Generating response…"), unsafe_allow_html=True)
            if topic_now == "Stats" or (topic_now != "Quiz" and stats.HINT.search(last_user)):
                context = "\n".join(f"{m['role'].capitalize()}: {m['content'][:250]}" for m in ss.messages[-4:-1])
                route = stats.route_question(
                    client,
                    sport,
                    ss.messages[-1]["content"],
                    active_model,
                    context=context,
                    provider=provider,
                    fallback=_fallback_router_target(provider),
                )
                if route:
                    vb_key = get_vb_key() if sport == "Volleyball" else None
                    is_live_fetch = not (
                        sport == "Volleyball" and (route["kind"] in ("player", "leaders") or not vb_key)
                    )
                    if is_live_fetch:
                        box.markdown(loading_ball_html(sport, "Fetching live stats…"), unsafe_allow_html=True)
                    live_data = stats.fetch_live_data(sport, route, vb_key)
                    if is_live_fetch:
                        box.markdown(loading_ball_html(sport, "Generating response…"), unsafe_allow_html=True)
            msgs = build_messages(topic_now, level, token, live_data)
            last_err = None
            streamed = False
            for cand_provider, cand_client, cand_model in _provider_attempts(provider, active_model, model_options):
                max_out = (700 if live_data else 450) if cand_provider == "openai" else (900 if live_data else 500)
                try:
                    stream = _create_completion(
                        cand_client,
                        cand_provider,
                        cand_model,
                        msgs,
                        temperature=temperature,
                        max_out=max_out,
                        stream=True,
                    )
                    reply = ""
                    for chunk in stream:
                        if not getattr(chunk, "choices", None):
                            continue
                        delta = chunk.choices[0].delta.content or ""
                        if not delta:
                            continue
                        reply += delta
                        reply, stop = trim_runaway(reply)
                        box.markdown(reply + "▌")
                        if stop:
                            break
                    if reply:
                        streamed = True
                        break
                except Exception as e:
                    if _is_model_not_found(e):
                        ss.unavailable_models.add(f"{cand_provider}:{cand_model}")
                    last_err = e
                    if reply:
                        raise
                    continue
            if not streamed and not reply:
                raise last_err or RuntimeError("No accessible chat model found for the configured API key(s).")
        except Exception as e:
            detail = str(e)
            secret_values = [_openai_key(), _groq_key(), get_vb_key()]
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
