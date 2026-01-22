"""
Lazy Loader - Defer imports until needed for faster startup
"""
import importlib
from typing import Dict, Any, Optional


class LazyLoader:
    """Lazy loading system for modules"""
    
    _modules: Dict[str, Any] = {}
    _imports: Dict[str, str] = {}
    
    @classmethod
    def register(cls, name: str, module_path: str):
        """Register a module for lazy loading"""
        cls._imports[name] = module_path
    
    @classmethod
    def get(cls, name: str) -> Any:
        """Get a module, loading it if needed"""
        if name not in cls._modules:
            if name not in cls._imports:
                raise ImportError(f"Module '{name}' not registered for lazy loading")
            
            module_path = cls._imports[name]
            cls._modules[name] = importlib.import_module(module_path)
        
        return cls._modules[name]
    
    @classmethod
    def preload(cls, *names: str):
        """Preload specific modules"""
        for name in names:
            cls.get(name)
    
    @classmethod
    def clear_cache(cls):
        """Clear module cache"""
        cls._modules.clear()


# Register commonly used modules for lazy loading
LazyLoader.register("orchestrator", "agents.orchestrator_pi")
LazyLoader.register("cybersecurity", "cybersecurity.enhanced_integration")
LazyLoader.register("ai_coding", "ai_coding.ai_code_generator")
LazyLoader.register("voice", "voice.voice_interface_pi")
LazyLoader.register("stt", "voice.stt_pi")
LazyLoader.register("tts", "voice.tts_pi")
