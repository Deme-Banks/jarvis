# Ollama (offline LLM for Jarvis)

Jarvis uses **Ollama** as the default brain. No API key is required.

## Install

1. Download: https://ollama.com/download
2. Or on Windows (winget): `winget install Ollama.Ollama --source winget`
3. Open a new terminal after install so `ollama` is on PATH.

## First run

```bat
ollama serve
ollama pull qwen2.5-coder:7b
```

`qwen2.5-coder:7b` is the default coding brain. Faster fallback: `qwen2.5-coder:3b`. General chat: `llama3.2`.

```powershell
$env:OLLAMA_MODEL = "qwen2.5-coder:3b"
```

## Point Jarvis at it

Copy `.env.example` to `.env` if you do not already have one. The local path works with **no keys**:

```
JARVIS_PREFER_CLOUD=false
JARVIS_FALLBACK_CLOUD=true
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:7b
```

## Start Jarvis (Windows, no mic)

```powershell
.\start_jarvis.ps1 -AutoStart -Mode text
venv\Scripts\python.exe run_jarvis.py
```

Voice mode uses `sounddevice` on Python 3.14 (no PyAudio wheel). Text mode does not need a microphone:

```powershell
venv\Scripts\python.exe run.py text
```

## Self-edit

From the text REPL, instruct Jarvis to change its own project files, for example:

`edit your code to add a comment at the top of run_jarvis.py`

Edits stay inside this repo. `.env`, `venv/`, `.git/`, and `cybersecurity/` are blocked.
