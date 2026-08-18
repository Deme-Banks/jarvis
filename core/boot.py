"""Start Ollama (or optional cloud fallback) and build the orchestrator."""
from __future__ import annotations

import os
import sys

from core.paths import ROOT, ensure_on_path

ensure_on_path()

import utils.optimized_imports  # noqa: F401
import config_pi as config
from agents.orchestrator_pi import PiOrchestrator
from llm.local_llm import LocalLLM


def _has_cloud_keys() -> bool:
    return bool(
        config.PiConfig.OPENAI_API_KEY
        or os.getenv("GEMINI_API_KEY")
        or config.PiConfig.ANTHROPIC_API_KEY
    )


def boot_orchestrator(*, announce: bool = True) -> PiOrchestrator:
    """
    Ready the local model and return a PiOrchestrator.
    Exits the process if nothing can answer.
    """
    os.chdir(ROOT)
    llm = LocalLLM()
    try:
        status = llm.ensure_ready()
        if announce:
            print(status)
    except RuntimeError as exc:
        if announce:
            print(str(exc))
        if not (config.PiConfig.FALLBACK_TO_CLOUD and _has_cloud_keys()):
            if announce:
                print("Install Ollama from https://ollama.com/download then run:")
                print("  ollama pull qwen2.5-coder:3b")
            sys.exit(1)
        if announce:
            print("Ollama is down. Trying a cloud key if one is configured...")
    return PiOrchestrator(
        local_llm=llm,
        prefer_cloud=config.PiConfig.PREFER_CLOUD_LLM,
    )
