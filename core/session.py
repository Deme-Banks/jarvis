"""One ask() path used by text, voice, and the UI."""
from __future__ import annotations

from ai_coding.self_editor import (
    PendingEdit,
    SelfCodeEditor,
    is_cancel,
    is_confirm,
    is_edit_request,
)
from agents.orchestrator_pi import PiOrchestrator
from core.memory import load_turns, save_turns, to_chat_messages
from core.skills import try_skill


class JarvisSession:
    def __init__(self, orchestrator: PiOrchestrator):
        self.orchestrator = orchestrator
        self.memory: list[dict[str, str]] = load_turns()
        self.pending_edit: PendingEdit | None = None
        llm = getattr(orchestrator, "llm", None)
        if llm is not None and hasattr(llm, "context"):
            llm.context = to_chat_messages(self.memory)

    def ask(self, user_text: str) -> str:
        text = (user_text or "").strip()
        if not text:
            return ""
        try:
            reply = self._route(text)
        except Exception as exc:
            reply = f"Something went wrong: {exc}"
        self.memory.append({"user": text, "assistant": reply})
        if len(self.memory) > 40:
            self.memory = self.memory[-40:]
        save_turns(self.memory)
        llm = getattr(self.orchestrator, "llm", None)
        if llm is not None and hasattr(llm, "context"):
            llm.context = to_chat_messages(self.memory)
        return reply

    def _route(self, text: str) -> str:
        if self.pending_edit:
            if is_confirm(text):
                msg = self.pending_edit.commit()
                self.pending_edit = None
                return msg
            if is_cancel(text):
                self.pending_edit = None
                return "Cancelled. No files changed."

        if is_edit_request(text):
            editor = SelfCodeEditor(self.orchestrator.llm)
            message, pending = editor.propose(text)
            self.pending_edit = pending
            return message

        skill = try_skill(text)
        if skill:
            return skill
        return self.orchestrator.process(text)

    def current_model(self) -> str:
        llm = getattr(self.orchestrator, "llm", None)
        return str(getattr(llm, "model_name", "") or "local")
