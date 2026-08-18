# Jarvis + Ollama (no API key)

Jarvis answers from a local Ollama model by default.

## Install

1. Download [Ollama for Windows](https://ollama.com/download).
2. Restart the terminal so `ollama` is on PATH.
3. Pull a coding-capable model (default):

```powershell
ollama pull qwen2.5-coder:3b
```

General chat alternative:

```powershell
ollama pull llama3.2
$env:OLLAMA_MODEL = "llama3.2"
```

Larger machines can use `llama3.1:8b` or `qwen2.5-coder:7b` (better at code):

```powershell
ollama pull qwen2.5-coder:7b
$env:OLLAMA_MODEL = "qwen2.5-coder:7b"
```

## Run Jarvis (text, no microphone)

```powershell
.\venv\Scripts\python.exe run_jarvis.py
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
| `OLLAMA_MODEL` | `qwen2.5-coder:3b` | Model name (`llama3.2` is pulled too) |
| `JARVIS_PREFER_CLOUD` | `false` | Set `true` to use API keys first |
| `JARVIS_MAX_TOKENS` | `800` | Reply length |
| `JARVIS_AGENT_TIMEOUT` | `90` | HTTP timeout seconds |
| `JARVIS_LLM_TIMEOUT` | `120` | Ollama chat timeout seconds |
