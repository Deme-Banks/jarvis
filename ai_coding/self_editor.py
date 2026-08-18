"""
Scoped self-code editor: Jarvis can change files in THIS repo when asked.

Never writes outside the project root. Skips secrets, venv, and the
cybersecurity/malware folders.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BLOCKED_DIR_PARTS = {
    "cybersecurity",
    "mobile_security",
    "venv",
    ".git",
    "__pycache__",
    "node_modules",
}
BLOCKED_NAMES = {".env", ".env.local"}
ALLOWED_SUFFIXES = {".py", ".md", ".txt", ".ps1", ".bat", ".json", ".toml", ".ini", ".example"}
MAX_FILE_BYTES = 200_000

EDIT_HINTS = (
    "edit your code",
    "edit your source",
    "change your code",
    "modify your code",
    "update your code",
    "rewrite your",
    "fix your code",
    "patch yourself",
    "edit jarvis",
    "change jarvis",
    "update jarvis source",
    "modify yourself",
    "edit the file",
    "open your source",
    "patch the file",
    "apply this change",
    "write this into",
    "save this to",
    "create a file",
    "add a file",
)

SYSTEM_PROMPT = """You edit Jarvis source on disk. You can ONLY change files inside this project.
Return ONLY JSON (no markdown) with one of these shapes:
{"action":"list","summary":"short"}
{"action":"read","path":"relative/path.py","summary":"short"}
{"action":"replace","path":"relative/path.py","old_string":"exact text to find","new_string":"replacement","summary":"what changed"}
{"action":"write","path":"relative/path.py","content":"full new file text","summary":"created/overwrote"}
Rules:
- Prefer replace over write for existing files.
- Never touch .env, cybersecurity/, mobile_security/, venv/, or .git/.
- Keep edits small and on-task.
- If the request is vague, use action list.
"""


def is_edit_request(text: str) -> bool:
    lowered = (text or "").lower()
    return any(hint in lowered for hint in EDIT_HINTS)


def is_confirm(text: str) -> bool:
    lowered = (text or "").strip().lower().rstrip(".!")
    return lowered in {
        "yes",
        "y",
        "yeah",
        "yep",
        "apply",
        "apply it",
        "do it",
        "confirm",
        "go ahead",
        "make it so",
        "proceed",
        "do that",
        "ok",
        "okay",
    }


def is_cancel(text: str) -> bool:
    lowered = (text or "").strip().lower().rstrip(".!")
    return lowered in {
        "no",
        "n",
        "cancel",
        "don't",
        "dont",
        "abort",
        "never mind",
        "nevermind",
        "stop",
    }


@dataclass
class PendingEdit:
    action: str
    rel: str
    target: Path
    old: str
    new: str
    summary: str

    def preview(self) -> str:
        import difflib

        if self.action == "write":
            lines = self.new.splitlines()[:40]
            body = "\n".join(lines)
            extra = "\n..." if self.new.count("\n") > 40 else ""
            return (
                f"Proposed write to {self.rel} ({self.summary or 'new file'}).\n"
                f"{body}{extra}\n\nSay apply to write it, or cancel."
            )
        diff = list(
            difflib.unified_diff(
                self.old.splitlines(),
                self.new.splitlines(),
                fromfile=self.rel,
                tofile=self.rel,
                lineterm="",
                n=2,
            )
        )[:60]
        shown = "\n".join(diff) if diff else "(no textual diff)"
        return (
            f"Proposed change to {self.rel}: {self.summary or ''}\n{shown}\n\n"
            "Say apply to write it, or cancel."
        )

    def commit(self) -> str:
        ok, reason = _is_allowed(self.target)
        if not ok:
            return reason
        if self.action == "replace":
            current = self.target.read_text(encoding="utf-8")
            if current != self.old:
                return f"File changed since the preview. {self.rel} was not written."
            self.target.write_text(self.new, encoding="utf-8")
            return f"Applied. Updated {self.rel}."
        if self.action == "write":
            if len(self.new.encode("utf-8")) > MAX_FILE_BYTES:
                return "That file would be too large to write."
            self.target.parent.mkdir(parents=True, exist_ok=True)
            self.target.write_text(self.new, encoding="utf-8")
            return f"Applied. Wrote {self.rel}."
        return "Nothing to apply."


def _is_allowed(path: Path) -> tuple[bool, str]:
    try:
        resolved = path.resolve()
        root = PROJECT_ROOT.resolve()
        resolved.relative_to(root)
    except (OSError, ValueError):
        return False, "Path must stay inside the Jarvis project folder."
    parts = {p.lower() for p in resolved.parts}
    if parts & BLOCKED_DIR_PARTS:
        return False, "That folder is blocked from self-edits."
    if resolved.name.lower() in BLOCKED_NAMES:
        return False, "Secret files cannot be edited."
    if resolved.suffix.lower() not in ALLOWED_SUFFIXES:
        return False, f"File type {resolved.suffix or '(none)'} is not editable."
    return True, ""


def _rel(path: Path) -> str:
    return str(path.resolve().relative_to(PROJECT_ROOT.resolve())).replace("\\", "/")


def list_source_files(limit: int = 80) -> list[str]:
    out: list[str] = []
    for p in sorted(PROJECT_ROOT.rglob("*")):
        if not p.is_file():
            continue
        ok, _ = _is_allowed(p)
        if not ok:
            continue
        out.append(_rel(p))
        if len(out) >= limit:
            break
    return out


class SelfCodeEditor:
    def __init__(self, llm: Any):
        self.llm = llm

    def propose(self, instruction: str) -> tuple[str, Optional[PendingEdit]]:
        """Plan an edit. Does not write replace/write until PendingEdit.commit()."""
        lowered = (instruction or "").lower().replace("\\", "/")
        if "cybersecurity" in lowered or "mobile_security" in lowered:
            return "That folder is blocked from self-edits.", None
        if ".env" in lowered.replace(" ", ""):
            return "Secret files cannot be edited.", None
        snapshot = "\n".join(list_source_files())
        user = (
            f"Project root: {PROJECT_ROOT}\n"
            f"Known files:\n{snapshot}\n\n"
            f"User instruction:\n{instruction}\n"
        )
        try:
            raw = self.llm.chat(user, system_prompt=SYSTEM_PROMPT, temperature=0.2)
        except TypeError:
            raw = self.llm.chat(user, system_prompt=SYSTEM_PROMPT)
        plan = _parse_plan(raw)
        if not plan:
            return (
                "I heard an edit request but could not parse a file plan. Try naming the file and the change.",
                None,
            )
        action = str(plan.get("action") or "").lower()
        if action == "list":
            files = list_source_files(40)
            return (plan.get("summary") or "Project files") + ":\n" + "\n".join(files[:40]), None
        rel = str(plan.get("path") or "").strip()
        if not rel:
            return "Edit plan was missing a path.", None
        target = (PROJECT_ROOT / rel).resolve()
        ok, reason = _is_allowed(target)
        if not ok:
            return reason, None
        if action == "read":
            if not target.exists():
                return f"Not found: {rel}", None
            text = target.read_text(encoding="utf-8", errors="replace")
            if len(text) > 8000:
                text = text[:8000] + "\n...[truncated]..."
            return f"{rel}:\n{text}", None
        if action == "replace":
            if not target.exists():
                return f"Not found: {rel}", None
            original = target.read_text(encoding="utf-8")
            old = str(plan.get("old_string") or "")
            new = str(plan.get("new_string") or "")
            if not old:
                return "Replace plan needed old_string.", None
            if old not in original:
                return f"Could not find the exact text to replace in {rel}.", None
            if original.count(old) > 1:
                return f"That snippet appears more than once in {rel}. Be more specific.", None
            pending = PendingEdit(
                action="replace",
                rel=rel,
                target=target,
                old=old,
                new=original.replace(old, new, 1),
                summary=str(plan.get("summary") or ""),
            )
            return pending.preview(), pending
        if action == "write":
            content = str(plan.get("content") or "")
            if not content.strip():
                return "Write plan was empty.", None
            pending = PendingEdit(
                action="write",
                rel=rel,
                target=target,
                old="",
                new=content,
                summary=str(plan.get("summary") or ""),
            )
            return pending.preview(), pending
        return f"Unknown edit action: {action}", None

    def apply(self, instruction: str) -> str:
        """Preview only. Session commits after the user confirms."""
        message, _pending = self.propose(instruction)
        return message


def _parse_plan(raw: str) -> Optional[dict]:
    text = (raw or "").strip()
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fenced:
        text = fenced.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        data = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None
