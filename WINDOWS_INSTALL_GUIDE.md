# Windows Installation Guide

## ✅ Successfully Installed

The following packages have been installed:
- ✅ openai, anthropic, langchain, langchain-openai
- ✅ speechrecognition, pyttsx3, vosk
- ✅ websockets, python-dotenv, pydantic
- ✅ typing-extensions, gTTS

## ⚠️ Packages Requiring Build Tools

These packages require **Microsoft Visual C++ Build Tools** to compile on Windows:

- `pyaudio` - Audio I/O
- `webrtcvad` - Voice activity detection  
- `pocketsphinx` - Offline speech recognition
- `pygame` - Audio playback (optional)

## Installation Options

### Option 1: Install Visual C++ Build Tools (Recommended)

1. Download and install **Microsoft C++ Build Tools**:
   - Visit: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Download "Build Tools for Visual Studio"
   - During installation, select "C++ build tools" workload
   - This will install ~6GB of tools

2. After installation, restart your terminal and run:
   ```bash
   python -m pip install pyaudio webrtcvad pocketsphinx
   ```

### Option 2: Use Pre-built Wheels (Easier for PyAudio)

For **pyaudio** specifically, you can use `pipwin` which provides pre-built wheels:

```bash
# Install pipwin
python -m pip install pipwin

# Install pyaudio using pipwin
pipwin install pyaudio
```

**Note:** `webrtcvad` and `pocketsphinx` may still need build tools even with pipwin.

### Option 3: Skip Optional Packages (For Now)

If you don't need audio input/output immediately, you can skip these packages:

- `pyaudio` - Only needed for microphone input
- `webrtcvad` - Only needed for voice activity detection
- `pocketsphinx` - Alternative offline STT (vosk is already installed)
- `pygame` - Only needed for advanced audio playback

The system will work with:
- ✅ `vosk` - Offline speech recognition (already installed)
- ✅ `pyttsx3` - Text-to-speech (already installed)
- ✅ `speechrecognition` - Speech recognition (already installed)

## Quick Test

Test if your installation works:

```bash
python -c "import openai, anthropic, vosk, pyttsx3; print('✓ Core packages working!')"
```

## Next Steps

1. **If you need audio input/output**: Install Visual C++ Build Tools (Option 1) or use pipwin for pyaudio (Option 2)

2. **If you just want to test the system**: You can proceed without pyaudio/webrtcvad/pocketsphinx - the system will use vosk and pyttsx3 which are already installed

3. **Setup API keys** (optional but recommended):
   ```bash
   python setup_api_keys.py <your_openai_api_key>
   ```

## Troubleshooting

### "Microsoft Visual C++ 14.0 or greater is required"

This means you need to install the build tools. See Option 1 above.

### PyAudio Installation Issues

Try using pipwin:
```bash
python -m pip install pipwin
pipwin install pyaudio
```

### Alternative: Use Conda

If you have Anaconda/Miniconda installed:
```bash
conda install pyaudio
conda install -c conda-forge pocketsphinx
```

---

**Current Status**: Core dependencies installed ✅  
**Remaining**: Audio packages (pyaudio, webrtcvad, pocketsphinx) - optional for basic functionality
