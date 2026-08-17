"""
Coding brain: explain, generate, debug, and (when asked) edit Jarvis files.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ai_coding.self_editor import (
    PROJECT_ROOT,
    SelfCodeEditor,
    _is_allowed,
    is_edit_request,
    list_source_files,
)
from prompts.coding import CODING_PROMPT

PATH_RE = re.compile(
    r"(?:(?:[A-Za-z]:)?[\\/])?(?:[\w.-]+[\\/])*[\w.-]+\.(?:py|js|ts|tsx|jsx|md|json|ps1|bat|toml|ini)"
)

CODE_HINTS = (
    "code",
    "coding",
    "python",
    "javascript",
    "typescript",
    "function",
    "class ",
    "traceback",
    "stack trace",
    "syntax error",
    "debug",
    "refactor",
    "implement",
    "write a",
    "write me",
    "script",
    "module",
    "import ",
    "def ",
    "explain this file",
    "explain this function",
    "what does this",
    "read the file",
    "open the file",
    "source code",
    "this repo",
    "this project",
    "pull request",
    "unit test",
    "pytest",
    "type hint",
    "api endpoint",
    "this repo",
    "this project",
    "jarvis source",
    "how does jarvis",
    "bug",
    "compile",
    "runtime error",
    "null pointer",
    "indexerror",
    "keyerror",
    "typeerror",
)


def is_coding_request(text: str) -> bool:
    lowered = (text or "").lower()
    if is_edit_request(lowered):
        return True
    if PATH_RE.search(text or ""):
        return True
    if "```" in (text or ""):
        return True
    return any(hint in lowered for hint in CODE_HINTS)


def _guess_paths(text: str) -> list[Path]:
    found: list[Path] = []
    for match in PATH_RE.findall(text or ""):
        raw = match.replace("\\", "/")
        candidate = (PROJECT_ROOT / raw).resolve()
        ok, _ = _is_allowed(candidate)
        if ok and candidate.exists() and candidate.is_file():
            found.append(candidate)
            continue
        name = Path(raw).name
        for hit in PROJECT_ROOT.rglob(name):
            ok, _ = _is_allowed(hit)
            if ok and hit.is_file():
                found.append(hit)
                break
    # de-dupe
    unique: list[Path] = []
    seen = set()
    for path in found:
        key = str(path)
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique[:4]


def _rel(path: Path) -> str:
    return str(path.resolve().relative_to(PROJECT_ROOT.resolve())).replace("\\", "/")


def _read_snippet(path: Path, limit: int = 12000) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > limit:
        text = text[:limit] + "\n...[truncated]..."
    return text


class CodeBrain:
    """Routes coding asks: self-edit, file-aware explain, or generate."""

    def __init__(self, llm: Any):
        self.llm = llm
        self.editor = SelfCodeEditor(llm)

    def answer(self, user_request: str) -> str:
        if is_edit_request(user_request):
            return self.editor.apply(user_request)

        context_blocks = self._collect_context(user_request)
        prompt = user_request
        if context_blocks:
            prompt = (
                "Use the project files below as context. Answer the user with "
                "accurate, file-aware coding help.\n\n"
                + "\n\n".join(context_blocks)
                + "\n\nUser request:\n"
                + user_request
            )
        return self.llm.chat(prompt, system_prompt=CODING_PROMPT, temperature=0.2)

    def _collect_context(self, user_request: str) -> list[str]:
        blocks: list[str] = []
        paths = _guess_paths(user_request)
        for path in paths:
            blocks.append(f"FILE {_rel(path)}:\n```\n{_read_snippet(path)}\n```")

        lowered = user_request.lower()
        wants_project = any(
            phrase in lowered
            for phrase in (
                "this repo",
                "this project",
                "your code",
                "jarvis source",
                "how does jarvis",
                "project structure",
            )
        )
        if wants_project and not paths:
            files = list_source_files(50)
            blocks.append("PROJECT FILES:\n" + "\n".join(files))
            readme = PROJECT_ROOT / "README.md"
            if readme.exists():
                blocks.append("FILE README.md:\n```\n" + _read_snippet(readme, 6000) + "\n```")
        return blocks
