"""Local conversation memory. Stays on this PC, never uploaded."""
from __future__ import annotations

import json
from pathlib import Path

from core.paths import ROOT

MEMORY_PATH = ROOT / "data" / "conversation.json"
MAX_TURNS = 40


def load_turns() -> list[dict[str, str]]:
    if not MEMORY_PATH.exists():
        return []
    try:
        data = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    turns = data.get("turns") if isinstance(data, dict) else data
    if not isinstance(turns, list):
        return []
    clean: list[dict[str, str]] = []
    for item in turns:
        if not isinstance(item, dict):
            continue
        user = str(item.get("user") or "")
        assistant = str(item.get("assistant") or "")
        if user or assistant:
            clean.append({"user": user, "assistant": assistant})
    return clean[-MAX_TURNS:]


def save_turns(turns: list[dict[str, str]]) -> None:
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"turns": turns[-MAX_TURNS:]}
    MEMORY_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def to_chat_messages(turns: list[dict[str, str]], limit: int = 8) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    for turn in turns[-limit:]:
        if turn.get("user"):
            messages.append({"role": "user", "content": turn["user"]})
        if turn.get("assistant"):
            messages.append({"role": "assistant", "content": turn["assistant"]})
    return messages
