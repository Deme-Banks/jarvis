"""
JARVIS entry point.

    venv\\Scripts\\python.exe run.py
    venv\\Scripts\\python.exe run.py text
    venv\\Scripts\\python.exe run.py voice
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="JARVIS personal assistant")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=("text", "voice", "ui"),
        default="ui",
        help="ui = window (default). text = keyboard. voice = wake-word mic.",
    )
    args = parser.parse_args(argv)
    if args.mode == "voice":
        from core.voice_cli import run_voice

        run_voice()
        return
    if args.mode == "text":
        from core.text_cli import run_text

        run_text()
        return
    from core.ui_app import run_ui

    run_ui()


if __name__ == "__main__":
    main()
