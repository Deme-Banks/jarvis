"""
Raspberry Pi Optimized Configuration
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class PiConfig:
    # Local Model Settings (Ollama, local LLM)
    USE_LOCAL_MODEL: bool = True
    LOCAL_MODEL_URL: str = "http://localhost:11434"  # Ollama default
    LOCAL_MODEL_NAME: str = "llama3.2:1b"  # Lightweight model for Pi
    # Alternatives: "phi3:mini", "tinyllama", "gemma:2b"
    
    # Fallback to cloud if local unavailable
    FALLBACK_TO_CLOUD: bool = True
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Voice Settings
    WAKE_WORD: str = "jarvis"
    WAKE_WORD_ENGINE: str = "pocketsphinx"  # Lightweight, works offline
    WAKE_WORD_SENSITIVITY: float = 0.5
    VAD_AGGRESSIVENESS: int = 2
    SAMPLE_RATE: int = 16000  # Lower for Pi
    CHUNK_SIZE: int = 512  # Smaller chunks for Pi
    
    # Audio Settings (Pi optimized)
    INPUT_DEVICE_INDEX: Optional[int] = None
    OUTPUT_DEVICE_INDEX: Optional[int] = None
    USE_ALSA: bool = True  # ALSA for Pi audio
    
    # STT (Speech-to-Text) Settings
    STT_ENGINE: str = "vosk"  # Offline, lightweight
    VOSK_MODEL_PATH: str = "./models/vosk-model-small-en-us-0.22"  # ~40MB
    # Alternative: "whisper" (heavier but more accurate)
    
    # TTS (Text-to-Speech) Settings
    TTS_ENGINE: str = "piper"  # Fast, local TTS
    # Alternatives: "pyttsx3", "espeak" (built-in on Pi)
    PIPER_MODEL_PATH: str = "./models/piper"
    TTS_RATE: int = 150
    
    # LLM Settings
    DEFAULT_MODEL: str = "local"  # Use local by default
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 300  # Lower for Pi performance
    
    # Interruption Settings
    INTERRUPTION_ENABLED: bool = True
    INTERRUPTION_THRESHOLD: float = 0.3
    
    # Context Memory (reduced for Pi)
    CONTEXT_MEMORY_SIZE: int = 5
    
    # Performance Settings
    ENABLE_ALL_AGENTS: bool = False  # Disable for performance
    AGENT_TIMEOUT: float = 15.0  # Shorter timeout
    MAX_CONCURRENT_AGENTS: int = 1  # Sequential processing
    
    # Hardware Detection
    IS_RASPBERRY_PI: bool = os.path.exists("/proc/device-tree/model")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        if cls.USE_LOCAL_MODEL:
            try:
                import requests
                response = requests.get(f"{cls.LOCAL_MODEL_URL}/api/tags", timeout=2)
                if response.status_code == 200:
                    return True
            except:
                if cls.FALLBACK_TO_CLOUD:
                    print("Local model unavailable, falling back to cloud")
                    return bool(cls.OPENAI_API_KEY or cls.ANTHROPIC_API_KEY)
                else:
                    print("Warning: Local model not available and fallback disabled")
                    return False
        return True
