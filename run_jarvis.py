"""
Text-mode Jarvis. No microphone or PyAudio required.

Uses Ollama at http://localhost:11434 by default.

Usage:
    venv\\Scripts\\python.exe run_jarvis.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import utils.optimized_imports  # noqa: F401  registers lazy modules
import config_pi as config
from agents.orchestrator_pi import PiOrchestrator
from llm.local_llm import LocalLLM


def _boot() -> PiOrchestrator:
    llm = LocalLLM()
    try:
        status = llm.ensure_ready()
        print(status)
    except RuntimeError as exc:
        print(str(exc))
        has_cloud = bool(
            config.PiConfig.OPENAI_API_KEY
            or os.getenv("GEMINI_API_KEY")
            or config.PiConfig.ANTHROPIC_API_KEY
        )
        if not (config.PiConfig.FALLBACK_TO_CLOUD and has_cloud):
            print("Install Ollama from https://ollama.com/download then run:")
            print("  ollama pull qwen2.5-coder:3b")
            sys.exit(1)
        print("Ollama is down. Trying a cloud key if one is configured...")
    return PiOrchestrator(
        local_llm=llm,
        prefer_cloud=config.PiConfig.PREFER_CLOUD_LLM,
    )


def main() -> None:
    print("JARVIS text mode  |  Ollama first  |  type quit to exit")
    print("Ask it to write code, explain a file, or edit its own source.")
    print()
    orchestrator = _boot()
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
        try:
            reply = orchestrator.process(line)
        except Exception as exc:
            reply = f"Something went wrong: {exc}"
        print()
        print(f"Jarvis> {reply}")
        print()


if __name__ == "__main__":
    main()
