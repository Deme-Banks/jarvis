"""
Overseas + open-weight models Jarvis can run locally via Ollama.

All of these are free to download. Licenses are Apache-2.0 or MIT unless noted.
We do not ship weights in git — Ollama stores them on disk.
"""
from __future__ import annotations

from dataclasses import dataclass

import config_pi as config


@dataclass(frozen=True)
class LocalModel:
    tag: str
    lab: str
    country: str
    size: str
    role: str
    license: str
    fits: str  # RAM guidance


# Picks that actually fit this machine (~32 GB RAM). Bigger tags are listed
# but marked as "needs more RAM".
CATALOG: list[LocalModel] = [
    LocalModel(
        "qwen2.5-coder:7b",
        "Alibaba Qwen",
        "China",
        "~4.7 GB",
        "Coding (current Jarvis default)",
        "Apache-2.0",
        "comfortable",
    ),
    LocalModel(
        "qwen3:8b",
        "Alibaba Qwen",
        "China",
        "~5.2 GB",
        "Smart general + thinking; strong multilingual",
        "Apache-2.0",
        "comfortable",
    ),
    LocalModel(
        "deepseek-r1:8b",
        "DeepSeek",
        "China",
        "~5.2 GB",
        "Reasoning / math / hard problems (thinks out loud)",
        "MIT",
        "comfortable",
    ),
    LocalModel(
        "mistral:7b",
        "Mistral AI",
        "France",
        "~4.4 GB",
        "Fast European chat; punches above size",
        "Apache-2.0",
        "comfortable",
    ),
    LocalModel(
        "glm4:9b",
        "Zhipu AI",
        "China",
        "~5.5 GB",
        "Bilingual Chinese/English general chat",
        "Zhipu GLM-4 license",
        "comfortable",
    ),
    LocalModel(
        "qwen2.5-coder:3b",
        "Alibaba Qwen",
        "China",
        "~1.9 GB",
        "Fast tiny coder",
        "Apache-2.0",
        "easy",
    ),
    LocalModel(
        "deepseek-r1:14b",
        "DeepSeek",
        "China",
        "~9 GB",
        "Stronger reasoning if you close other apps",
        "MIT",
        "tight on 32 GB if Chrome is heavy",
    ),
    LocalModel(
        "qwen3:14b",
        "Alibaba Qwen",
        "China",
        "~9.3 GB",
        "Smarter general; slower",
        "Apache-2.0",
        "tight on 32 GB if Chrome is heavy",
    ),
]


def catalog_text(*, installed: list[str] | None = None) -> str:
    lines = [
        "I am JARVIS. These open-weight models work with me locally (no API key):",
    ]
    installed_l = [n.lower() for n in (installed or [])]
    for item in CATALOG:
        mark = "ready" if any(item.tag in h or h.startswith(item.tag) for h in installed_l) else "not pulled"
        lines.append(
            f"- {item.tag} — {item.lab} ({item.country}), {item.size}, {item.license}. "
            f"{item.role}. [{mark}]"
        )
    lines.append(
        "They form one assistant. Say list crew, or prefer weights with "
        "use qwen3 / use deepseek / use mistral / use glm4 / use coder."
    )
    return "\n".join(lines)


def resolve_alias(text: str) -> str | None:
    lowered = (text or "").lower()
    aliases = {
        "qwen3": "qwen3:8b",
        "qwen 3": "qwen3:8b",
        "deepseek": "deepseek-r1:8b",
        "deep seek": "deepseek-r1:8b",
        "r1": "deepseek-r1:8b",
        "mistral": "mistral:7b",
        "france": "mistral:7b",
        "glm4": "glm4:9b",
        "glm 4": "glm4:9b",
        "zhipu": "glm4:9b",
        "coder": "qwen2.5-coder:7b",
        "coding": "qwen2.5-coder:7b",
        "qwen coder": "qwen2.5-coder:7b",
        "tiny": "qwen2.5-coder:3b",
        "fast": "qwen2.5-coder:3b",
    }
    for key, tag in aliases.items():
        if key in lowered:
            return tag
    # raw tag in the sentence
    for item in CATALOG:
        if item.tag in lowered:
            return item.tag
    return None


def switch_runtime(llm, tag: str) -> str:
    """Point the live LocalLLM at an already-pulled model."""
    names = llm.list_models()
    chosen = None
    for name in names:
        if name == tag or name.startswith(tag):
            chosen = name
            break
    if not chosen:
        return (
            f"{tag} is not installed yet. In a terminal run: ollama pull {tag}\n"
            "Then say use that model again."
        )
    llm.model_name = chosen
    if hasattr(llm, "context"):
        llm.context = []
    config.PiConfig.LOCAL_MODEL_NAME = chosen
    return f"Switched brain to {chosen}. Ready."
