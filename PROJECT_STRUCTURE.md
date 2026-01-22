# JARVIS Voice System - Project Structure

## Raspberry Pi Optimized Version

```
jarvis-voice-system/
├── config_pi.py              # Pi-optimized configuration
├── requirements_pi.txt       # Pi dependencies
├── jarvis_pi.py             # Main entry point for Pi
├── setup_pi.sh              # Automated setup script
├── README_PI.md             # Full documentation
├── QUICKSTART_PI.md         # Quick start guide
├── .env.example             # Environment variables template
│
├── prompts/                 # System prompts
│   ├── __init__.py
│   ├── orchestrator.py      # Orchestrator prompt
│   ├── specialists.py       # Specialist agent prompts
│   └── voice_jarvis.py      # Voice-first JARVIS prompt
│
├── agents/                  # Agent implementations
│   ├── __init__.py
│   ├── orchestrator.py      # Cloud orchestrator
│   └── orchestrator_pi.py   # Pi-optimized orchestrator
│
├── voice/                   # Voice processing
│   ├── __init__.py
│   ├── audio_pi.py          # Audio capture/output (Pi)
│   ├── stt_pi.py            # Speech-to-text (Vosk)
│   └── tts_pi.py            # Text-to-speech (Piper/espeak)
│
└── llm/                     # LLM integration
    ├── __init__.py
    └── local_llm.py         # Ollama/local LLM interface
```

## Key Features

### Offline-First
- **Vosk STT**: Offline speech recognition (~40MB model)
- **Ollama LLM**: Local AI models (1B-7B parameters)
- **Piper/espeak TTS**: Offline text-to-speech
- **PocketSphinx**: Wake word detection

### Optimized for Pi
- Reduced memory footprint
- Smaller audio chunks (512 vs 1024)
- Sequential agent processing
- Configurable performance settings

### Multi-Agent System
- Orchestrator routes to specialists
- Voice UX, Automation, Productivity, Security, Creative agents
- Context-aware responses

## Usage Flow

1. **Wake Word Detection** → PocketSphinx listens for "jarvis"
2. **Voice Activity Detection** → WebRTC VAD detects speech
3. **Speech-to-Text** → Vosk transcribes audio
4. **Orchestrator** → Routes to appropriate agents
5. **Local LLM** → Ollama generates response
6. **Text-to-Speech** → Piper/espeak speaks response
7. **Interruption Handling** → Real-time speech interruption

## Configuration

Edit `config_pi.py` for:
- Model selection (llama3.2:1b, phi3:mini, etc.)
- Audio device selection
- Performance tuning
- Agent enable/disable

## Next Steps

1. Run `setup_pi.sh` to install dependencies
2. Start Ollama: `ollama serve`
3. Pull model: `ollama pull llama3.2:1b`
4. Run: `python3 jarvis_pi.py`

See `QUICKSTART_PI.md` for detailed setup.
