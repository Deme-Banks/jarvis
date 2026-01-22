"""
Configuration for JARVIS Multi-Agent Voice System
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Voice Settings
    WAKE_WORD: str = "jarvis"
    WAKE_WORD_SENSITIVITY: float = 0.5
    VAD_AGGRESSIVENESS: int = 2  # 0-3, higher = more aggressive
    SAMPLE_RATE: int = 16000
    CHUNK_SIZE: int = 1024
    
    # Audio Settings
    INPUT_DEVICE_INDEX: Optional[int] = None  # None = default
    OUTPUT_DEVICE_INDEX: Optional[int] = None
    
    # LLM Settings
    DEFAULT_MODEL: str = "gpt-4-turbo-preview"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 500
    
    # Voice Response Settings
    TTS_ENGINE: str = "pyttsx3"  # or "gtts" or "openai"
    TTS_RATE: int = 150  # words per minute
    TTS_VOICE_INDEX: int = 0
    
    # Interruption Settings
    INTERRUPTION_ENABLED: bool = True
    INTERRUPTION_THRESHOLD: float = 0.3  # seconds of speech to trigger
    
    # Context Memory
    CONTEXT_MEMORY_SIZE: int = 10  # number of exchanges to remember
    
    # Agent Settings
    ENABLE_ALL_AGENTS: bool = True
    AGENT_TIMEOUT: float = 30.0  # seconds
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            print("Warning: No API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY")
            return False
        return True
