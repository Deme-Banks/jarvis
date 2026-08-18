"""
Jarvis is the only voice. Other local models are specialists he consults.

You talk to JARVIS. Coder / reasoner / general drafts stay backstage.
On ~32 GB RAM we consult at most one specialist per turn, then Jarvis speaks.
"""
from __future__ import annotations

import re
from typing import Any, Optional

from ai_coding.code_brain import CodeBrain, is_coding_request
from core.identity import live_prompt

THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)

# Preferred Ollama tags per job. First installed match wins.
ROLE_TAGS: dict[str, tuple[str, ...]] = {
    "conductor": (
        "qwen2.5-coder:7b",
        "qwen3:8b",
        "mistral:7b",
        "llama3.2",
    ),
    "coder": (
        "qwen2.5-coder:7b",
        "qwen2.5-coder:3b",
    ),
    "reasoner": (
        "deepseek-r1:8b",
        "deepseek-r1:14b",
        "qwen3:8b",
    ),
    "general": (
        "qwen3:8b",
        "glm4:9b",
        "mistral:7b",
        "llama3.2",
        "qwen2.5-coder:7b",
    ),
}

REASON_HINTS = (
    "calculate",
    "math problem",
    "solve for",
    "prove ",
    "proof",
    "step by step",
    "reason about",
    "logic puzzle",
    "sudoku",
    "big-o",
    "time complexity",
    "probability",
    "derivative",
    "integral",
    "think hard",
    "think carefully",
    "riddle",
)

SPECIALIST_BRIEF = (
    "You draft notes for JARVIS. Be technical and complete. "
    "No greeting, no 'as an AI', no mention of model names. "
    "JARVIS will speak to the user."
)

SYNTH_TAIL = """
A specialist drafted notes for you. Answer the user as JARVIS — one mind, your identity, not a summary bot.
Keep facts, numbers, and every markdown code fence unchanged.
Do not name Qwen, DeepSeek, Mistral, Ollama, or specialists unless asked how you work.
"""


def strip_think(text: str) -> str:
    cleaned = THINK_RE.sub("", text or "")
    return cleaned.strip()


def is_reasoning_request(text: str) -> bool:
    lowered = (text or "").lower()
    return any(hint in lowered for hint in REASON_HINTS)


def classify(text: str) -> str | None:
    """Which specialist Jarvis should consult, or None for Jarvis-only."""
    if is_coding_request(text):
        return "coder"
    if is_reasoning_request(text):
        return "reasoner"
    return None


def match_installed(tag: str, installed: list[str]) -> str | None:
    wanted = (tag or "").strip()
    if not wanted:
        return None
    for name in installed:
        if name == wanted or name.startswith(wanted):
            return name
    return None


def pick_role(
    role: str,
    installed: list[str],
    *,
    preferred: str | None = None,
) -> str | None:
    tags: list[str] = []
    if preferred:
        tags.append(preferred)
    tags.extend(ROLE_TAGS.get(role, ()))
    seen: set[str] = set()
    for tag in tags:
        if tag in seen:
            continue
        seen.add(tag)
        hit = match_installed(tag, installed)
        if hit:
            return hit
    return None


class ModelView:
    """Call one Ollama tag without stealing Jarvis's conversation memory."""

    def __init__(self, llm: Any, tag: str):
        self._llm = llm
        self.model_name = tag

    def chat(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        context: Optional[list] = None,
        **kwargs: Any,
    ) -> str:
        if hasattr(self._llm, "complete"):
            return self._llm.complete(
                message,
                model=self.model_name,
                system_prompt=system_prompt,
                temperature=temperature,
                context=context or [],
            )
        return self._llm.chat(
            message,
            system_prompt=system_prompt,
            temperature=temperature,
            context=context or [],
        )


class JarvisCrew:
    """Jarvis conducts; specialists draft when the job needs them."""

    def __init__(self, llm: Any):
        self.llm = llm
        self.preferred_conductor: str | None = None

    def installed(self) -> list[str]:
        if self.llm is None or not hasattr(self.llm, "list_models"):
            return []
        return list(self.llm.list_models() or [])

    def conductor_tag(self) -> str:
        installed = self.installed()
        preferred = self.preferred_conductor or getattr(self.llm, "model_name", None)
        return pick_role("conductor", installed, preferred=preferred) or preferred or "local"

    def role_tag(self, role: str) -> str | None:
        return pick_role(role, self.installed())

    def coder_view(self) -> Any:
        tag = self.role_tag("coder") or self.conductor_tag()
        return ModelView(self.llm, tag)

    def status_line(self) -> str:
        parts = ["JARVIS"]
        for role in ("coder", "reasoner", "general"):
            tag = self.role_tag(role)
            parts.append(f"{role}:{'ready' if tag else 'offline'}")
        return "  ·  ".join(parts) + "  |  local, personal"

    def roster_text(self) -> str:
        installed = self.installed()
        lines = [
            "I am JARVIS. The other local models work with me, they are not separate assistants.",
            f"I speak. Conductor weights: {self.conductor_tag()}.",
        ]
        for role, title in (
            ("coder", "Coder (Qwen2.5-Coder, China)"),
            ("reasoner", "Reasoner (DeepSeek-R1, China)"),
            ("general", "General (Qwen3 / GLM-4 / Mistral)"),
        ):
            tag = pick_role(role, installed)
            mark = tag if tag else "not pulled yet"
            lines.append(f"- {title}: {mark}")
        lines.append("Say list crew anytime. Prefer a specialist with: use coder, use deepseek, use qwen3.")
        return "\n".join(lines)

    def prefer(self, tag: str) -> str:
        from core.models import switch_runtime

        msg = switch_runtime(self.llm, tag)
        if "not installed" in msg.lower():
            return msg
        self.preferred_conductor = getattr(self.llm, "model_name", tag)
        return (
            f"Still JARVIS. I'll lean on {self.preferred_conductor} as a faculty. "
            "I remain one mind."
        )

    def reply(self, user_request: str, context: Optional[list] = None) -> str:
        role = classify(user_request)
        conductor = self.conductor_tag()
        specialist = self.role_tag(role) if role else None

        if role == "coder":
            draft = strip_think(CodeBrain(self.coder_view()).answer(user_request))
            if not specialist or specialist == conductor:
                return draft
            return self._as_jarvis(user_request, draft, context=context, keep_code=True)

        if role == "reasoner" and specialist and specialist != conductor:
            draft = strip_think(
                self._ask(
                    specialist,
                    user_request,
                    system=SPECIALIST_BRIEF + " Reason carefully. Put the answer first.",
                )
            )
            return self._as_jarvis(user_request, draft, context=context)

        return strip_think(
            self._ask(
                conductor,
                user_request,
                system=live_prompt(),
                context=context,
            )
        )

    def _ask(
        self,
        model: str,
        message: str,
        *,
        system: str,
        context: Optional[list] = None,
        temperature: Optional[float] = None,
    ) -> str:
        view = ModelView(self.llm, model)
        return view.chat(
            message,
            system_prompt=system,
            temperature=temperature,
            context=context,
        )

    def _as_jarvis(
        self,
        user_request: str,
        draft: str,
        *,
        context: Optional[list] = None,
        keep_code: bool = False,
    ) -> str:
        extra = " Keep every code fence byte-for-byte." if keep_code else ""
        prompt = (
            f"User: {user_request}\n\nSpecialist notes:\n{draft}\n\n"
            "Now answer the user."
        )
        return strip_think(
            self._ask(
                self.conductor_tag(),
                prompt,
                system=live_prompt() + SYNTH_TAIL + extra,
                context=context,
            )
        )
