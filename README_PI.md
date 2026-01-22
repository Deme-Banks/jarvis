# JARVIS Voice Assistant - Raspberry Pi Edition

A lightweight, offline-capable voice assistant optimized for Raspberry Pi with local LLM support.

## Features

- **Offline Operation**: Works without internet using local models
- **Wake Word Detection**: PocketSphinx-based wake word detection
- **Local LLM**: Integrates with Ollama for local AI responses
- **Lightweight STT**: Vosk for offline speech recognition
- **Fast TTS**: Piper or espeak for text-to-speech
- **Interruption Handling**: Real-time speech interruption
- **Multi-Agent System**: Specialized agents for different tasks

## Hardware Requirements

- Raspberry Pi 4 (recommended) or Pi 3B+
- USB microphone or compatible audio input
- Speaker or audio output
- SD card (16GB+ recommended)

## Installation

### 1. System Setup

```bash
# Make setup script executable
chmod +x setup_pi.sh

# Run setup
./setup_pi.sh
```

### 2. Manual Setup (Alternative)

```bash
# Install system packages
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev portaudio19-dev \
    alsa-utils espeak espeak-data pocketsphinx pocketsphinx-en-us

# Install Python packages
pip3 install -r requirements_pi.txt

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:1b
```

### 3. Download Models

```bash
# Vosk STT model (~40MB)
mkdir -p models
cd models
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.22.zip
unzip vosk-model-small-en-us-0.22.zip
rm vosk-model-small-en-us-0.22.zip
cd ..
```

### 4. Configure Audio

```bash
# List audio devices
arecord -l  # Input devices
aplay -l    # Output devices

# Test audio
arecord -d 3 test.wav
aplay test.wav
```

### 5. Configure Environment

Edit `config_pi.py` or create `.env`:

```bash
# Optional: For cloud fallback
OPENAI_API_KEY=your_key_here
```

## Usage

### Start Ollama (Required)

```bash
# Start Ollama service
ollama serve

# In another terminal, verify it's running
ollama list
```

### Run JARVIS

```bash
python3 jarvis_pi.py
```

Say "jarvis" followed by your command.

## Configuration

Edit `config_pi.py` to customize:

- **Local Model**: Change `LOCAL_MODEL_NAME` (e.g., "phi3:mini", "tinyllama")
- **Wake Word**: Change `WAKE_WORD`
- **Audio Devices**: Set `INPUT_DEVICE_INDEX` and `OUTPUT_DEVICE_INDEX`
- **Performance**: Adjust `MAX_TOKENS`, `CONTEXT_MEMORY_SIZE`

## Model Recommendations for Pi

### Lightweight Models (Pi 3B+)
- `llama3.2:1b` - Fastest, good for simple tasks
- `tinyllama` - Very small, basic responses
- `phi3:mini` - Better quality, slightly slower

### Better Models (Pi 4)
- `llama3.2:3b` - Better quality
- `gemma:2b` - Good balance
- `mistral:7b` - Best quality (may be slow)

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

## Troubleshooting

### Audio Issues
```bash
# Check audio devices
arecord -l
aplay -l

# Test microphone
arecord -d 5 -f cd test.wav
aplay test.wav

# Set default audio device
sudo raspi-config  # Advanced Options → Audio
```

### Ollama Not Starting
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
pkill ollama
ollama serve
```

### Model Not Found
```bash
# List available models
ollama list

# Pull model
ollama pull llama3.2:1b
```

### Performance Issues
- Reduce `MAX_TOKENS` in `config_pi.py`
- Use smaller model (e.g., `tinyllama`)
- Disable agents: `ENABLE_ALL_AGENTS = False`
- Reduce `CONTEXT_MEMORY_SIZE`

## Advanced Usage

### Push-to-Talk Mode
Modify `jarvis_pi.py` to use button press instead of wake word.

### Cloud Fallback
Set `FALLBACK_TO_CLOUD = True` and add API keys for cloud backup.

### Custom Wake Word
Train PocketSphinx with custom wake word or use alternative detection.

## License

MIT License - See LICENSE file

## Contributing

Contributions welcome! Focus areas:
- Performance optimization
- Better wake word detection
- More efficient models
- Hardware-specific optimizations
