# JARVIS Voice Assistant - Multi-Agent System

A sophisticated voice-first AI assistant with multi-agent architecture, optimized for Raspberry Pi with local LLM support and cybersecurity testing capabilities.

## Features

### Core Capabilities
- **Voice-First Interface**: Natural speech interaction with wake word detection
- **Multi-Agent System**: Specialized agents for different tasks
- **Local LLM Support**: Works offline with Ollama
- **Raspberry Pi Optimized**: Lightweight, resource-efficient
- **Real-time Interruption**: Barge-in capability

### Cybersecurity Module
- **Malware Lab**: Educational payload creation and analysis
- **DDoS Testing**: Authorized penetration testing tools
- **VSOC Integration**: Automated reporting and analytics
- **Natural Language Commands**: Advanced NLP parsing

## Quick Start

### Raspberry Pi Setup

```bash
# Clone repository
git clone https://github.com/Deme-Banks/jarvis.git
cd jarvis

# Run setup
chmod +x setup_pi.sh
./setup_pi.sh

# Start Ollama
ollama serve

# Pull model
ollama pull llama3.2:1b

# Run JARVIS
python3 jarvis_pi.py
```

### Cybersecurity Mode

```bash
# Run cybersecurity-enabled version
python3 jarvis_cybersec.py
```

**⚠️ WARNING**: Cybersecurity module is for authorized testing and educational purposes only. See [CYBERSECURITY_WARNING.md](CYBERSECURITY_WARNING.md) for legal guidelines.

## Documentation

- [README_PI.md](README_PI.md) - Full Raspberry Pi documentation
- [QUICKSTART_PI.md](QUICKSTART_PI.md) - Quick start guide
- [README_CYBERSEC.md](README_CYBERSEC.md) - Cybersecurity module docs
- [IMPROVEMENTS.md](IMPROVEMENTS.md) - Recent improvements
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Project architecture

## Architecture

```
┌─────────────┐
│   Microphone│
└──────┬──────┘
       │
┌──────▼──────────┐
│  Wake Word      │
│  Detection      │
└──────┬──────────┘
       │
┌──────▼──────────┐
│  VAD            │
│  (Voice Activity)│
└──────┬──────────┘
       │
┌──────▼──────────┐
│  Vosk STT       │
│  (Speech→Text)  │
└──────┬──────────┘
       │
┌──────▼──────────┐
│  Orchestrator   │
│  (Multi-Agent)  │
└──────┬──────────┘
       │
┌──────▼──────────┐
│  Ollama LLM     │
│  (Local AI)     │
└──────┬──────────┘
       │
┌──────▼──────────┐
│  Piper/espeak   │
│  (Text→Speech)  │
└──────┬──────────┘
       │
┌──────▼──────┐
│   Speaker   │
└─────────────┘
```

## Requirements

### System Requirements
- Raspberry Pi 4 (recommended) or Pi 3B+
- USB microphone
- Speaker/audio output
- Python 3.8+

### Dependencies
See `requirements_pi.txt` for full list.

## Configuration

1. Copy `.env.example` to `.env`
2. Edit `config_pi.py` for customization
3. Configure audio devices
4. Set up Ollama with preferred model

## Usage Examples

### Basic Voice Commands
```
"Jarvis, what time is it?"
"Jarvis, create a keylogger for learning"
"Jarvis, run TCP flood test on localhost"
```

### Advanced Commands
```
"Jarvis, run a high-intensity TCP flood on 192.168.1.100 port 8080 for 60 seconds"
"Jarvis, create an obfuscated keylogger with base64 encoding"
"Jarvis, show attack reports"
```

## Security & Legal

**IMPORTANT**: The cybersecurity module is for:
- ✅ Authorized testing only
- ✅ Educational purposes
- ✅ Isolated test environments
- ❌ NOT for unauthorized use

Unauthorized use is illegal. See [CYBERSECURITY_WARNING.md](CYBERSECURITY_WARNING.md).

## Contributing

Contributions welcome! Focus areas:
- Performance optimization
- Better wake word detection
- More efficient models
- Hardware-specific optimizations
- Security improvements

## License

MIT License - See LICENSE file

## Author

[Deme-Banks](https://github.com/Deme-Banks)

## Acknowledgments

Built with:
- Ollama for local LLM
- Vosk for speech recognition
- Piper/espeak for text-to-speech
- PocketSphinx for wake word detection

---

**Use responsibly. Test ethically. Learn continuously.**
