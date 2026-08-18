"""Keyboard REPL."""
from __future__ import annotations

from core.boot import boot_orchestrator
from core.session import JarvisSession
from voice.tts_pi import PiTTS


def run_text() -> None:
    print("JARVIS text mode  |  Ollama first  |  type quit to exit")
    print("Ask it to write code, explain a file, or edit its own source.")
    print()
    session = JarvisSession(boot_orchestrator())
    tts = PiTTS()
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
        try:
            tts.speak_aloud(reply)
        except Exception as exc:
            print(f"Voice failed: {exc}")
