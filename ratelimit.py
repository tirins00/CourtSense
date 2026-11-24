"""Daily prompt quota keyed to an anonymous browser cookie, stored locally."""
from contextlib import contextmanager
import json
import logging
import os
import re
import threading
import uuid
from datetime import date
from pathlib import Path

import streamlit as st

_log = logging.getLogger(__name__)
_STORE = Path(__file__).parent / ".streamlit" / "prompt_usage.json"
_LOCK = threading.Lock()
_COOKIE = "cs_client_id"
_DEFAULT_LIMIT = 20
_WARN_RATIO = 0.8


def daily_limit():
    try:
        raw = os.environ.get("PROMPT_DAILY_LIMIT") or st.secrets["PROMPT_DAILY_LIMIT"]
        n = int(raw)
        return n if 1 <= n <= 10000 else _DEFAULT_LIMIT
    except Exception:
        return _DEFAULT_LIMIT


def client_id():
    """Reuse the cookie id, else mint one and flag JS to persist it."""
    ss = st.session_state
    if _COOKIE in ss:
        return ss[_COOKIE]
    cid = None
    try:
        raw = st.context.headers.get("cookie") or st.context.headers.get("Cookie") or ""
        match = re.search(r"(?:^|;\s*)cs_client_id=([0-9a-f]{32})(?:;|$)", raw)
        if match:
            cid = match.group(1)
    except Exception:
        pass
    if not cid:
        # Fallback: check query params (for environments without JS cookie support)
        try:
            qp = st.query_params.get("cs_client_id") or ""
            if re.fullmatch(r"[0-9a-f]{32}", qp):
                cid = qp
        except Exception:
            pass
    if not cid:
        cid = uuid.uuid4().hex
        ss["_cs_new_cookie"] = True
    ss[_COOKIE] = cid
    return cid


def _read():
    try:
        data = json.loads(_STORE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _lock_file(fh):
    """Advisory file lock (best-effort, cross-platform)."""
    try:
        import msvcrt
        fh.seek(0)
        msvcrt.locking(fh.fileno(), msvcrt.LK_LOCK, 1)
    except (ImportError, OSError):
        try:
            import fcntl
            fcntl.flock(fh, fcntl.LOCK_EX)
        except (ImportError, OSError):
            pass  # no locking available — fall through


def _unlock_file(fh):
    """Release advisory file lock (best-effort, cross-platform)."""
    try:
        import msvcrt
        fh.seek(0)
        msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
    except (ImportError, OSError):
        try:
            import fcntl
            fcntl.flock(fh, fcntl.LOCK_UN)
        except (ImportError, OSError):
            pass


@contextmanager
def _locked_store():
    """Serialize read-modify-write across threads and local processes."""
    lock_fh = None
    try:
        _STORE.parent.mkdir(parents=True, exist_ok=True)
        lock_fh = open(_STORE.with_suffix(".lock"), "a+", encoding="utf-8")
        _lock_file(lock_fh)
    except Exception:
        if lock_fh:
            try:
                lock_fh.close()
            except Exception:
                pass
            lock_fh = None
    try:
        with _LOCK:
            yield
    finally:
        if lock_fh:
            try:
                _unlock_file(lock_fh)
                lock_fh.close()
            except Exception:
                pass


def _write(data):
    tmp = _STORE.with_suffix(f".{os.getpid()}.tmp")
    try:
        _STORE.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps(data), encoding="utf-8")
        os.replace(tmp, _STORE)
    except Exception:
        _log.warning("ratelimit: failed to write usage data to %s", _STORE, exc_info=True)
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass


def status():
    """(used, limit, remaining, warn, blocked) for today's client."""
    day, limit, cid = date.today().isoformat(), daily_limit(), client_id()
    with _LOCK:
        entry = _read().get(cid) or {}
    used = entry.get("used", 0) if entry.get("date") == day and isinstance(entry.get("used", 0), int) else 0
    return used, limit, max(0, limit - used), used >= max(1, int(limit * _WARN_RATIO)), used >= limit


def consume():
    """Spend one prompt if any remain; returns False at the limit."""
    day, limit, cid = date.today().isoformat(), daily_limit(), client_id()
    with _locked_store():
        data = _read()
        entry = data.get(cid) or {}
        used = entry.get("used", 0) if entry.get("date") == day and isinstance(entry.get("used", 0), int) else 0
        if used >= limit:
            return False
        data = {k: v for k, v in data.items() if isinstance(v, dict) and v.get("date") == day}
        data[cid] = {"date": day, "used": used + 1}
        _write(data)
    return True


def refund():
    """Give back one prompt credit (e.g. after a failed generation)."""
    day, cid = date.today().isoformat(), client_id()
    with _locked_store():
        data = _read()
        entry = data.get(cid) or {}
        used = entry.get("used", 0) if entry.get("date") == day and isinstance(entry.get("used", 0), int) else 0
        if used > 0:
            data[cid] = {"date": day, "used": used - 1}
            _write(data)


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as folder:
        _STORE = Path(folder) / "usage.json"
        client_id = lambda: "self-test"
        daily_limit = lambda: 20
        assert all(consume() for _ in range(20))
        assert not consume()
        assert status()[:3] == (20, 20, 0) and status()[4]
        refund()
        assert status()[:3] == (19, 20, 1) and not status()[4]
        assert consume()
        assert not consume()
        _STORE.write_text("{not json", encoding="utf-8")
        assert status()[0] == 0
        print("ratelimit self-check OK")
