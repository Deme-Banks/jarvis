"""Keyboard REPL."""
from __future__ import annotations

from core.boot import boot_orchestrator
from core.session import JarvisSession


def run_text() -> None:
    print("JARVIS text mode  |  Ollama first  |  type quit to exit")
    print("Ask it to write code, explain a file, or edit its own source.")
    print()
    session = JarvisSession(boot_orchestrator())
    print()
    while True:
        try:
            line = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return
        if not line:
            continue
        if line.lower() in {"quit", "exit", "q"}:
            print("Bye.")
            return
        reply = session.ask(line)
        print()
        print(f"Jarvis> {reply}")
        print()
