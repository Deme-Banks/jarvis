# JARVIS Voice System - Dependencies Guide

Complete list of all dependencies needed for the JARVIS Voice System project.

## Quick Install

### Standard Installation (Windows/Mac/Linux)
```bash
pip install -r requirements.txt
```

### Raspberry Pi Installation
```bash
pip install -r requirements_pi.txt
```

---

## Python Dependencies

### Core Dependencies (Standard)
Located in `requirements.txt`:

```bash
# Core AI/LLM
openai>=1.12.0              # OpenAI API client
anthropic>=0.18.0           # Anthropic/Claude API client
langchain>=0.1.0            # LangChain framework
langchain-openai>=0.0.5     # LangChain OpenAI integration

# Voice & Audio
pyaudio>=0.2.14             # Audio I/O
speechrecognition>=3.10.0   # Speech recognition
pyttsx3>=2.90               # Text-to-speech
vosk>=0.3.45                # Offline speech recognition
webrtcvad>=2.0.10           # Voice activity detection
pocketsphinx>=5.0.0         # Offline speech recognition

# Streaming & Real-time
websockets>=12.0            # WebSocket support
asyncio>=3.4.3              # Async operations (built-in, but version check)

# Utilities
python-dotenv>=1.0.0        # Environment variable management
pydantic>=2.5.0             # Data validation
typing-extensions>=4.9.0    # Type hints extensions

# Optional: Advanced TTS
gTTS>=2.5.0                 # Google Text-to-Speech
pygame>=2.5.2               # Audio playback
```

### Raspberry Pi Dependencies
Located in `requirements_pi.txt`:

```bash
# Core (lightweight)
requests>=2.31.0
python-dotenv>=1.0.0

# Local LLM (Ollama)
ollama>=0.1.0

# Voice & Audio (Pi optimized)
pyaudio>=0.2.14
webrtcvad>=2.0.10
pocketsphinx>=5.0.0
vosk>=0.3.45
piper-tts>=1.0.0            # Offline TTS for Pi
pyttsx3>=2.90

# Utilities
numpy>=1.24.0               # Required by audio libs

# Cloud LLM Support
openai>=1.12.0
google-generativeai>=0.3.0  # Google Gemini
anthropic>=0.18.0

# Cybersecurity testing (authorized use only)
pynput>=1.7.6
cryptography>=41.0.0
```

---

## System Dependencies

### Windows
- **Python 3.8+** (recommended: Python 3.10+)
- **PortAudio** (for PyAudio):
  - Download from: http://portaudio.com/download.html
  - Or install via: `pip install pipwin` then `pipwin install pyaudio`

### macOS
```bash
# Install PortAudio via Homebrew
brew install portaudio

# Then install Python packages
pip install -r requirements.txt
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    portaudio19-dev \
    alsa-utils \
    libasound2-dev
```

### Raspberry Pi
```bash
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    portaudio19-dev \
    alsa-utils \
    espeak \
    espeak-data \
    pocketsphinx \
    pocketsphinx-en-us \
    libasound2-dev
```

---

## Optional Dependencies

These are used by specific features and can be installed as needed:

### Database Connectors
```bash
pip install mysql-connector-python  # MySQL
pip install psycopg2-binary         # PostgreSQL
pip install pymongo                 # MongoDB
```

### Document Processing
```bash
pip install PyPDF2                  # PDF reading
pip install pdfplumber              # PDF reading (alternative)
pip install python-docx             # Word documents
```

### Data Export
```bash
pip install pandas                  # Data manipulation
pip install openpyxl               # Excel export
pip install reportlab              # PDF generation
```

### Translation
```bash
pip install googletrans==4.0.0rc1  # Multi-language support
```

### Code Building
```bash
pip install pyinstaller             # Create executables
```

### Cybersecurity Tools (Authorized Use Only)
```bash
# System tools
sudo apt-get install nmap          # Network scanning

# Python tools
pip install frida-tools            # Dynamic instrumentation
pip install objection               # Runtime mobile exploration
```

---

## VS Code Extension Dependencies

Located in `vscode-extension/package.json`:

### Runtime Dependencies
```bash
cd vscode-extension
npm install
```

**Dependencies:**
- `axios>=1.6.0` - HTTP client

### Development Dependencies
- `@types/vscode>=1.74.0` - VS Code API types
- `@types/node>=16.x` - Node.js types
- `typescript>=4.9.4` - TypeScript compiler

**Install:**
```bash
cd vscode-extension
npm install
```

---

## Claude Code Plugin Dependencies

**No runtime dependencies required!**

The everything-claude-code plugin configuration (in `.claude-plugin/`) is just configuration files. No Python packages or npm modules needed.

**Setup:**
1. Install via Claude Code settings (see `CLAUDE_CODE_SETUP.md`)
2. Or manually copy to `~/.claude/` directories

---

## Additional Requirements

### API Keys (Optional but Recommended)

Create a `.env` file in the project root:

```bash
# Cloud LLM APIs (optional - for cloud features)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here

# Other services
SLACK_BOT_TOKEN=your_token_here
TELEGRAM_BOT_TOKEN=your_token_here
```

**Setup script:**
```bash
python setup_api_keys.py <your_openai_api_key>
```

### Models & Data Files

#### Vosk Speech Recognition Model
```bash
# Download Vosk model (for offline STT)
mkdir -p models
cd models
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.22.zip
unzip vosk-model-small-en-us-0.22.zip
```

#### Ollama (for Raspberry Pi)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download lightweight model
ollama pull llama3.2:1b
# Alternatives:
# ollama pull phi3:mini
# ollama pull tinyllama
```

---

## Installation Commands

### Full Standard Installation
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install optional dependencies (if needed)
pip install pandas openpyxl reportlab
pip install PyPDF2 python-docx
pip install googletrans==4.0.0rc1

# 3. Setup API keys
python setup_api_keys.py <your_key>
```

### Raspberry Pi Installation
```bash
# 1. Run setup script (includes system deps)
bash setup_pi.sh

# Or manually:
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev portaudio19-dev alsa-utils espeak espeak-data pocketsphinx pocketsphinx-en-us libasound2-dev

# Install Python packages
pip3 install -r requirements_pi.txt

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:1b

# Download Vosk model
mkdir -p models
cd models
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.22.zip
unzip vosk-model-small-en-us-0.22.zip
```

### VS Code Extension
```bash
cd vscode-extension
npm install
npm run compile
```

---

## Verification

### Check Dependencies
```bash
python scripts/health_check.py
```

### Quick Dependency Check
```bash
python scripts/quick_start.py
```

### Test Individual Packages
```bash
python -c "import vosk; print('✓ vosk')"
python -c "import pyaudio; print('✓ pyaudio')"
python -c "import openai; print('✓ openai')"
python -c "import anthropic; print('✓ anthropic')"
```

---

## Troubleshooting

### PyAudio Installation Issues

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### Missing System Libraries

**Linux/Raspberry Pi:**
```bash
sudo apt-get update
sudo apt-get install -y build-essential python3-dev
```

### Audio Device Issues

**Test audio:**
```bash
# Linux/Pi
arecord -d 3 test.wav && aplay test.wav

# Check devices
arecord -l
aplay -l
```

---

## Minimum Requirements

### For Basic Functionality
- Python 3.8+
- `python-dotenv`
- `requests`
- `vosk` (for offline STT)
- `pyttsx3` (for TTS)

### For Full Features
- All packages in `requirements.txt`
- API keys for cloud LLM features
- Vosk model downloaded
- Audio system configured

---

## Summary

**Essential:**
- Python 3.8+
- Packages from `requirements.txt` or `requirements_pi.txt`
- System audio libraries (PortAudio)

**Recommended:**
- API keys for cloud LLM features
- Vosk model for offline STT
- Ollama (for Raspberry Pi)

**Optional:**
- Database connectors
- Document processing libraries
- VS Code extension
- Claude Code plugin (configuration only, no deps)

For detailed setup instructions, see:
- `CLAUDE_CODE_SETUP.md` - Claude Code plugin setup
- `docs/TUTORIAL.md` - General tutorial
- `docs/DEPLOYMENT.md` - Deployment guide
- `QUICKSTART_PI.md` - Raspberry Pi quick start
