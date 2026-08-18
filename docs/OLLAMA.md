# Jarvis + Ollama (no API key)

Jarvis answers from a local Ollama model by default.

## Install

1. Download [Ollama for Windows](https://ollama.com/download).
2. Restart the terminal so `ollama` is on PATH.
3. Pull a coding-capable model (default is `qwen2.5-coder:7b`):

```powershell
ollama pull qwen2.5-coder:7b
```

Tiny / faster coder: `ollama pull qwen2.5-coder:3b`.

## Run Jarvis (text, no microphone)

```powershell
.\venv\Scripts\python.exe run.py text
.\venv\Scripts\python.exe run.py voice
```

Or:

```powershell
.\start_jarvis.ps1 -SkipInstall -AutoStart
```

Voice mode (`-Mode pi`) still needs PyAudio. Text mode does not.

## Env vars

| Variable | Default | Meaning |
|---|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server |
| `OLLAMA_MODEL` | `qwen2.5-coder:7b` | Default coding brain. Switching models is runtime-only. |
| `JARVIS_PREFER_CLOUD` | `false` | Set `true` to use API keys first |
| `JARVIS_MAX_TOKENS` | `800` | Reply length |
| `JARVIS_AGENT_TIMEOUT` | `90` | HTTP timeout seconds |
| `JARVIS_LLM_TIMEOUT` | `120` | Ollama chat timeout seconds |

## Overseas open-weight brains (~32 GB RAM)

You talk to **JARVIS**. Other local models are specialists he consults — they are not separate assistants.

| Job | Model | Origin |
|---|---|---|
| Default conductor (`OLLAMA_MODEL`) | `qwen2.5-coder:7b` | Alibaba / China |
| Smart general | `qwen3:8b` | Alibaba / China |
| Reasoner | `deepseek-r1:8b` | DeepSeek / China |
| Fast chat | `mistral:7b` | Mistral / France |
| Bilingual | `glm4:9b` | Zhipu / China |

At most one specialist is consulted per turn (this machine has ~32 GB RAM), then Jarvis speaks.

```powershell
ollama pull qwen3:8b          # Alibaba / China — smart general (~5.2 GB)
ollama pull deepseek-r1:8b    # DeepSeek / China — reasoning (~5.2 GB)
ollama pull mistral:7b        # Mistral / France — fast chat (~4.4 GB)
ollama pull glm4:9b           # Zhipu / China — bilingual (~5.5 GB, optional)
```

Say **list models** / **what models** (or **list crew**) to see installed vs not pulled. **use qwen3** / **use deepseek** / **use mistral** / **use glm4** / **use coder** switches the conductor at runtime — you still talk to JARVIS. The UI **Brain** menu does the same. First reply after a switch can be slow while weights load into RAM. DeepSeek R1 thinks out loud; Jarvis strips that scratchpad before he answers. Skip 14B+ on this machine if Chrome is heavy; do not pull 32B/70B/671B.
