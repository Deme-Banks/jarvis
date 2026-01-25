# PyAudio Installation on Windows - Python 3.14 Issue

## Problem

You're using **Python 3.14**, which is very new. PyAudio doesn't have pre-built wheels for Python 3.14 on Windows yet, so it needs to be compiled from source.

## Solutions

### Option 1: Install Visual C++ Build Tools (Recommended)

This allows you to compile PyAudio from source:

1. **Download Microsoft C++ Build Tools:**
   - Visit: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Download "Build Tools for Visual Studio 2022"
   - Run the installer

2. **During installation:**
   - Select "C++ build tools" workload
   - Make sure "Windows 10/11 SDK" is checked
   - Install (~6GB download)

3. **After installation:**
   - **Restart your terminal/command prompt** (important!)
   - Run:
     ```bash
     python -m pip install pyaudio
     ```

### Option 2: Use Python 3.11 or 3.12 (Easier)

Python 3.11 and 3.12 have pre-built wheels available:

1. **Install Python 3.12** from python.org
2. Create a virtual environment:
   ```bash
   python3.12 -m venv venv
   venv\Scripts\activate
   ```
3. Install packages:
   ```bash
   pip install -r requirements.txt
   ```

### Option 3: Skip PyAudio (For Now)

The system can work without PyAudio:
- ✅ `vosk` - Already installed, works for offline STT
- ✅ `pyttsx3` - Already installed, works for TTS
- ✅ `speechrecognition` - Already installed

PyAudio is only needed for:
- Direct microphone input
- Real-time audio streaming

You can add it later when you need those features.

## Current Status

✅ **Core packages installed:**
- openai, anthropic, langchain
- vosk, pyttsx3, speechrecognition
- All other dependencies

⚠️ **Missing (optional):**
- pyaudio (needs build tools or Python 3.11/3.12)
- webrtcvad (needs build tools)
- pocketsphinx (needs build tools)
- pygame (needs build tools)

## Recommendation

**For immediate use:** Skip PyAudio for now - the system works with vosk and pyttsx3.

**For full audio features:** Install Visual C++ Build Tools (Option 1) or switch to Python 3.12 (Option 2).

---

**Note:** On macOS/Linux, you would use `brew install portaudio`, but on Windows, PortAudio comes bundled when you compile PyAudio with the build tools.
