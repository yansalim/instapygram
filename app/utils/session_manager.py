import json
from pathlib import Path
from typing import Any, Dict, Optional

SESSIONS_DIR = Path(__file__).resolve().parent.parent.parent / "sessions"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

def _session_path(username: str) -> Path:
    return SESSIONS_DIR / f"{username}.json"

def save_session(username: str, session: Dict[str, Any]) -> None:
    _session_path(username).write_text(json.dumps(session, indent=2), encoding="utf-8")

def load_session(username: str) -> Optional[Dict[str, Any]]:
    p = _session_path(username)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))

def delete_session(username: str) -> bool:
    p = _session_path(username)
    if p.exists():
        p.unlink()
        return True
    return False

def session_exists(username: str) -> bool:
    return _session_path(username).exists()
