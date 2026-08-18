"""
Jarvis's living self: who he is, and what he has learned about the operator.

Canon lives in prompts/voice_jarvis.py. This file is the part that grows.
Stored on this PC only: data/identity.json (gitignored).
"""
from __future__ import annotations

import json
import re

from core.paths import ROOT
from prompts.voice_jarvis import with_living_memory

IDENTITY_PATH = ROOT / "data" / "identity.json"
MAX_FACTS = 24

NAME_RE = re.compile(
    r"\b(?:my name is|call me|i am called)\s+([A-Za-z][A-Za-z0-9._-]{1,30})\b",
    re.IGNORECASE,
)
REMEMBER_RE = re.compile(
    r"^\s*(?:please\s+)?remember(?:\s+that)?\s+(.+)$",
    re.IGNORECASE | re.DOTALL,
)
FORGET_RE = re.compile(
    r"^\s*(?:please\s+)?forget(?:\s+that)?\s+(.+)$",
    re.IGNORECASE | re.DOTALL,
)

DEFAULT = {
    "version": 1,
    "address": "sir",
    "user_name": "",
    "facts": [
        "The operator is building me locally on a Windows PC as a personal assistant.",
    ],
}


def _load() -> dict:
    if not IDENTITY_PATH.exists():
        return dict(DEFAULT)
    try:
        data = json.loads(IDENTITY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return dict(DEFAULT)
    if not isinstance(data, dict):
        return dict(DEFAULT)
    out = dict(DEFAULT)
    out.update({k: data.get(k, out.get(k)) for k in ("version", "address", "user_name")})
    facts = data.get("facts")
    out["facts"] = [str(x) for x in facts if str(x).strip()] if isinstance(facts, list) else list(DEFAULT["facts"])
    return out


def _save(data: dict) -> None:
    IDENTITY_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "address": str(data.get("address") or "sir"),
        "user_name": str(data.get("user_name") or ""),
        "facts": list(data.get("facts") or [])[-MAX_FACTS:],
    }
    IDENTITY_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def profile_text(data: dict | None = None) -> str:
    data = data or _load()
    lines = []
    name = (data.get("user_name") or "").strip()
    address = (data.get("address") or "sir").strip() or "sir"
    if name:
        lines.append(f"The operator's name is {name}. Address them as {address}.")
    else:
        lines.append(f"You do not yet have their given name. Address them as {address}.")
    for fact in data.get("facts") or []:
        fact = str(fact).strip()
        if fact:
            lines.append(f"- {fact}")
    return "\n".join(lines)


def live_prompt() -> str:
    return with_living_memory(profile_text())


def who_am_i() -> str:
    data = _load()
    name = (data.get("user_name") or "").strip()
    address = (data.get("address") or "sir").strip() or "sir"
    if name:
        return (
            f"J.A.R.V.I.S., {address}. Just A Rather Very Intelligent System — "
            f"yours, running on this machine. I am one mind, {name}. At your service."
        )
    return (
        "J.A.R.V.I.S. — Just A Rather Very Intelligent System. "
        "I am your personal chief of staff on this machine. One mind. At your service."
    )


def greeting() -> str:
    data = _load()
    name = (data.get("user_name") or "").strip()
    address = (data.get("address") or "sir").strip() or "sir"
    if name:
        return f"Hello, {name}. JARVIS online. What do you need?"
    return f"Hello, {address}. JARVIS online. What do you need?"


def about_user() -> str:
    data = _load()
    name = (data.get("user_name") or "").strip()
    facts = [str(f).strip() for f in (data.get("facts") or []) if str(f).strip()]
    if not name and not facts:
        return "I have the shape of you, not the file yet. Tell me your name, or say remember, followed by a fact."
    bits = []
    if name:
        bits.append(f"I know you as {name}.")
    if facts:
        bits.append("I have on file: " + "; ".join(facts[-8:]) + ".")
    else:
        bits.append("No further notes yet.")
    bits.append("Correct me anytime.")
    return " ".join(bits)


def remember(fact: str) -> str:
    fact = (fact or "").strip().rstrip(".")
    if len(fact) < 3:
        return "Remember what, sir?"
    data = _load()
    facts = [str(x) for x in data.get("facts") or []]
    if fact not in facts:
        facts.append(fact)
    data["facts"] = facts[-MAX_FACTS:]
    _save(data)
    return f"Logged. I'll keep that in mind."


def forget(needle: str) -> str:
    needle = (needle or "").strip().lower()
    if not needle:
        return "Forget which note?"
    data = _load()
    facts = [str(x) for x in data.get("facts") or []]
    kept = [f for f in facts if needle not in f.lower()]
    if len(kept) == len(facts):
        return "I don't have a note matching that."
    data["facts"] = kept
    _save(data)
    return "Dropped. That note is gone."


def set_name(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]", "", (name or "").strip())
    if len(name) < 2:
        return "I didn't catch a name I can keep."
    data = _load()
    data["user_name"] = name
    # First name is fine as address once we have it
    data["address"] = name
    _save(data)
    return f"Understood. I'll call you {name}."


def observe(user_text: str) -> str | None:
    """Pull identity updates from ordinary speech. Returns a spoken confirm or None."""
    text = (user_text or "").strip()
    if not text:
        return None
    remember_hit = REMEMBER_RE.match(text)
    if remember_hit:
        return remember(remember_hit.group(1))
    forget_hit = FORGET_RE.match(text)
    if forget_hit:
        target = forget_hit.group(1).strip()
        lowered = target.lower()
        if lowered in {"me", "everything", "all that", "all of that", "what you know"}:
            data = _load()
            data["facts"] = list(DEFAULT["facts"])
            data["user_name"] = ""
            data["address"] = "sir"
            _save(data)
            return "Clean slate. I still know who I am."
        return forget(target)
    name_hit = NAME_RE.search(text)
    if name_hit:
        return set_name(name_hit.group(1))
    return None


def canned_reply(user_text: str) -> str | None:
    """Stable identity lines that should not depend on a weak model roll."""
    key = (user_text or "").lower().strip().rstrip("!?.,")
    if key in {
        "who are you",
        "who are you jarvis",
        "what's your name",
        "whats your name",
        "what is your name",
    }:
        return who_am_i()
    if key in {
        "what do you know about me",
        "what do you remember",
        "what do you remember about me",
    }:
        return about_user()
    if key in {"hello", "hi", "hey", "hi jarvis", "hello jarvis", "hey jarvis"}:
        return greeting()
    return None


def handle_turn(user_text: str) -> str | None:
    """Identity commands that Jarvis answers himself, without a specialist."""
    text = (user_text or "").strip()
    canned = canned_reply(text)
    if canned:
        return canned
    spoken = observe(text)
    if not spoken:
        return None
    if REMEMBER_RE.match(text) or FORGET_RE.match(text):
        return spoken
    if NAME_RE.search(text) and len(text) < 80:
        from ai_coding.code_brain import is_coding_request

        if is_coding_request(text):
            return None
        return spoken
    return None
