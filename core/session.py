"""One ask() path used by text and voice."""
from __future__ import annotations

from agents.orchestrator_pi import PiOrchestrator


class JarvisSession:
    def __init__(self, orchestrator: PiOrchestrator):
        self.orchestrator = orchestrator
        self.memory: list[dict[str, str]] = []

    def ask(self, user_text: str) -> str:
        text = (user_text or "").strip()
        if not text:
            return ""
        try:
            reply = self.orchestrator.process(text)
        except Exception as exc:
            reply = f"Something went wrong: {exc}"
        self.memory.append({"user": text, "assistant": reply})
        if len(self.memory) > 20:
            self.memory = self.memory[-20:]
        return reply
