"""Voice-mode Jarvis. Prefer: python run.py voice"""
from __future__ import annotations

import run as jarvis_run
from core.voice_cli import VoiceJarvis as JarvisPi

__all__ = ["JarvisPi"]


def main() -> None:
    jarvis_run.main(["voice"])


if __name__ == "__main__":
    main()
