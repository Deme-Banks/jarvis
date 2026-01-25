# Installing Python 3.12 for JARVIS

## Why Python 3.12?

Python 3.14 is too new - PyAudio and other audio packages don't have pre-built wheels yet. Python 3.12 has all the wheels we need, so installation is much easier.

## Step 1: Download Python 3.12

1. **Visit:** https://www.python.org/downloads/release/python-31211/
2. **Download:** "Windows installer (64-bit)" (the .exe file)
3. **Important:** During installation, check:
   - ✅ "Add Python 3.12 to PATH"
   - ✅ "Install for all users" (optional)

## Step 2: Verify Installation

After installation, open a **new** terminal and check:

```bash
py -3.12 --version
```

Should show: `Python 3.12.11`

## Step 3: Create Virtual Environment with Python 3.12

```bash
# Navigate to project
cd c:\jarvis-voice-system

# Create venv with Python 3.12
py -3.12 -m venv venv312

# Activate it
venv312\Scripts\activate

# Verify Python version
python --version
```

Should show: `Python 3.12.11`

## Step 4: Install All Dependencies

```bash
# Make sure venv is activated (you should see (venv312) in prompt)
pip install --upgrade pip
pip install -r requirements.txt
```

This should now install **everything**, including PyAudio with pre-built wheels!

## Step 5: Verify PyAudio Installation

```bash
python -c "import pyaudio; print('✓ PyAudio installed successfully!')"
```

## Quick Setup Script

Save this as `setup_python312.ps1`:

```powershell
# Download Python 3.12 installer
Write-Host "Please download Python 3.12 from:"
Write-Host "https://www.python.org/downloads/release/python-31211/"
Write-Host ""
Write-Host "After installing Python 3.12, run:"
Write-Host "py -3.12 -m venv venv312"
Write-Host "venv312\Scripts\activate"
Write-Host "pip install -r requirements.txt"
```

## Alternative: Use pyenv-win (Advanced)

If you want to manage multiple Python versions:

```bash
# Install pyenv-win
git clone https://github.com/pyenv-win/pyenv-win.git $HOME\.pyenv

# Install Python 3.12
pyenv install 3.12.11
pyenv local 3.12.11
```

---

**After setup, you'll have:**
- ✅ Python 3.12 with all packages
- ✅ PyAudio working (pre-built wheels)
- ✅ All dependencies installed
