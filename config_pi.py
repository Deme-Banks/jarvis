"""
Raspberry Pi Optimized Configuration
"""
import os
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}

class PiConfig:
    # Local Model Settings (Ollama) — default offline brain
    USE_LOCAL_MODEL: bool = _env_bool("JARVIS_USE_OLLAMA", True)
    LOCAL_MODEL_URL: str = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    LOCAL_MODEL_NAME: str = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:3b")
    # Windows/PC alternatives: llama3.2, llama3.1:8b, phi3, gemma2:2b
    
    # Fallback to cloud only if Ollama is down and keys exist
    FALLBACK_TO_CLOUD: bool = _env_bool("JARVIS_FALLBACK_CLOUD", True)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Voice Settings
    WAKE_WORD: str = "jarvis"
    WAKE_WORD_ENGINE: str = "pocketsphinx"  # Lightweight, works offline
    WAKE_WORD_SENSITIVITY: float = 0.5
    VAD_AGGRESSIVENESS: int = 2
    SAMPLE_RATE: int = 16000  # Lower for Pi
    CHUNK_SIZE: int = 256  # Smaller chunks for faster processing
    
    # Performance Settings
    ENABLE_RESPONSE_CACHE: bool = True
    CACHE_SIZE: int = 1000
    CACHE_TTL: int = 3600  # 1 hour
    USE_PRECOMPUTED: bool = True
    LAZY_LOADING: bool = True
    
    # Audio Settings (Pi optimized)
    INPUT_DEVICE_INDEX: Optional[int] = None
    OUTPUT_DEVICE_INDEX: Optional[int] = None
    USE_ALSA: bool = True  # ALSA for Pi audio
    
    # STT (Speech-to-Text) Settings
    STT_ENGINE: str = "vosk"  # Offline, lightweight
    VOSK_MODEL_PATH: str = "./models/vosk-model-small-en-us-0.15"  # ~40MB
    # Alternative: "whisper" (heavier but more accurate)
    
    # TTS (Text-to-Speech) Settings
    TTS_ENGINE: str = "piper"  # Fast, local TTS
    # Alternatives: "pyttsx3", "espeak" (built-in on Pi)
    PIPER_MODEL_PATH: str = "./models/piper"
    TTS_RATE: int = 150
    
    # LLM Settings
    DEFAULT_MODEL: str = "local"  # Ollama first
    
    # Cloud LLM Settings
    PREFER_CLOUD_LLM: bool = _env_bool("JARVIS_PREFER_CLOUD", False)
    OPENAI_MODEL: str = "gpt-4"  # or "gpt-3.5-turbo" for faster/cheaper
    GEMINI_MODEL: str = "gemini-pro"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = int(os.getenv("JARVIS_MAX_TOKENS", "800"))
    
    # Interruption Settings
    INTERRUPTION_ENABLED: bool = True
    INTERRUPTION_THRESHOLD: float = 0.3
    
    # Context Memory (reduced for Pi)
    CONTEXT_MEMORY_SIZE: int = 5
    
    # Performance Settings
    ENABLE_ALL_AGENTS: bool = False  # Disable for performance
    AGENT_TIMEOUT: float = float(os.getenv("JARVIS_AGENT_TIMEOUT", "90"))
    LOCAL_LLM_TIMEOUT: float = float(os.getenv("JARVIS_LLM_TIMEOUT", "120"))
    MAX_CONCURRENT_AGENTS: int = 1  # Sequential processing
    
    # Advanced Features
    ENABLE_STREAMING: bool = True  # Enable streaming STT/LLM
    ENABLE_ASYNC: bool = True  # Enable async operations
    ENABLE_ERROR_RECOVERY: bool = True  # Enable error recovery
    
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
                if cls.FALLBACK_TO_CLOUD and (cls.OPENAI_API_KEY or os.getenv("GEMINI_API_KEY")):
                    print("Ollama unavailable — falling back to cloud API if configured")
                    return True
                print("Ollama is not running. Install from https://ollama.com then: ollama pull qwen2.5-coder:3b")
                return False
        return True
