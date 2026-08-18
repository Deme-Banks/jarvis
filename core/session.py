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
            editor = SelfCodeEditor(self.orchestrator.crew.coder_view())
            message, pending = editor.propose(text)
            self.pending_edit = pending
            return message

        from core.identity import handle_turn

        ident = handle_turn(text)
        if ident:
            return ident

        model_reply = self._maybe_switch_model(text)
        if model_reply:
            return model_reply

        skill = try_skill(text)
        if skill:
            return skill
        return self.orchestrator.process(text)

    def _maybe_switch_model(self, text: str) -> str | None:
        from core.models import catalog_text, resolve_alias, switch_runtime

        lowered = text.lower().strip()
        llm = getattr(self.orchestrator, "llm", None)
        installed = llm.list_models() if llm and hasattr(llm, "list_models") else []
        crew = getattr(self.orchestrator, "crew", None)
        if (
            "list models" in lowered
            or "what models" in lowered
            or "which model" in lowered
            or "list crew" in lowered
            or "who is working" in lowered
            or lowered in {"models", "crew"}
        ):
            if crew is not None:
                return crew.roster_text() + "\n\n" + catalog_text(installed=installed)
            return catalog_text(installed=installed)
        if lowered.startswith("use ") or lowered.startswith("switch to ") or "switch model" in lowered:
            tag = resolve_alias(text)
            if not tag:
                return catalog_text(installed=installed)
            if crew is not None:
                return crew.prefer(tag)
            if not llm:
                return "No local model runtime."
            return switch_runtime(llm, tag)
        return None

    def installed_models(self) -> list[str]:
        llm = getattr(self.orchestrator, "llm", None)
        if llm is None or not hasattr(llm, "list_models"):
            return []
        return llm.list_models()

    def switch_to(self, tag: str) -> str:
        crew = getattr(self.orchestrator, "crew", None)
        if crew is not None:
            return crew.prefer(tag)
        from core.models import switch_runtime

        llm = getattr(self.orchestrator, "llm", None)
        if llm is None:
            return "No local model runtime."
        return switch_runtime(llm, tag)

    def current_model(self) -> str:
        crew = getattr(self.orchestrator, "crew", None)
        if crew is not None:
            return crew.conductor_tag()
        llm = getattr(self.orchestrator, "llm", None)
        return str(getattr(llm, "model_name", "") or "local")

    def status_line(self) -> str:
        crew = getattr(self.orchestrator, "crew", None)
        if crew is not None:
            return crew.status_line()
        return f"JARVIS  ·  {self.current_model()}  |  local, personal"
