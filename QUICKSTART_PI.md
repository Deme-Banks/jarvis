# Quick Start - Raspberry Pi

## 5-Minute Setup

### 1. Install Dependencies

```bash
chmod +x setup_pi.sh
./setup_pi.sh
```

### 2. Start Ollama

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Verify and pull model
ollama pull llama3.2:1b
```

### 3. Test Audio

```bash
# Record 3 seconds
arecord -d 3 test.wav

# Play it back
aplay test.wav
```

### 4. Run JARVIS

```bash
python3 jarvis_pi.py
```

Say: **"jarvis, what time is it?"**

## Troubleshooting

**No audio?**
```bash
sudo raspi-config
# Advanced Options → Audio → Select your device
```

**Ollama not found?**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Model too slow?**
```bash
# Use smaller model
ollama pull tinyllama
# Edit config_pi.py: LOCAL_MODEL_NAME = "tinyllama"
```

## Next Steps

- Customize wake word in `config_pi.py`
- Adjust performance settings
- Add cloud fallback (optional)
- See `README_PI.md` for full documentation
