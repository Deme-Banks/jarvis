#!/bin/bash
# Raspberry Pi Setup Script for JARVIS

echo "Setting up JARVIS on Raspberry Pi..."

# Update system
sudo apt-get update

# Install system dependencies
echo "Installing system dependencies..."
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

# Install Python dependencies
echo "Installing Python packages..."
pip3 install -r requirements_pi.txt

# Install Ollama (if not already installed)
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    
    echo "Downloading lightweight model..."
    ollama pull llama3.2:1b
    # Alternatives: ollama pull phi3:mini, ollama pull tinyllama
fi

# Download Vosk model
echo "Downloading Vosk STT model..."
mkdir -p models
cd models
if [ ! -d "vosk-model-small-en-us-0.22" ]; then
    wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.22.zip
    unzip vosk-model-small-en-us-0.22.zip
    rm vosk-model-small-en-us-0.22.zip
fi
cd ..

# Setup audio
echo "Configuring audio..."
# Test audio devices
echo "Available audio devices:"
arecord -l
aplay -l

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# Optional: For cloud fallback
# OPENAI_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
EOF
fi

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Test audio: arecord -d 3 test.wav && aplay test.wav"
echo "2. Start Ollama: ollama serve"
echo "3. Run JARVIS: python3 jarvis_pi.py"
