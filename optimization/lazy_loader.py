"""
Lazy Loading System for Faster Startup
"""
import importlib
import sys
from typing import Dict, Callable, Any, Optional


class LazyLoader:
    """Lazy load modules only when needed"""
    
    def __init__(self):
        self._modules: Dict[str, Any] = {}
        self._loaders: Dict[str, Callable] = {}
    
    def register(self, name: str, loader: Callable):
        """Register a lazy loader function"""
        self._loaders[name] = loader
    
    def get(self, name: str) -> Any:
        """Get module, loading if necessary"""
        if name not in self._modules:
            if name in self._loaders:
                self._modules[name] = self._loaders[name]()
            else:
                raise ValueError(f"No loader registered for {name}")
        return self._modules[name]
    
    def is_loaded(self, name: str) -> bool:
        """Check if module is loaded"""
        return name in self._modules


# Global lazy loader instance
_lazy_loader = LazyLoader()


def lazy_import(module_name: str, attribute: Optional[str] = None):
    """Lazy import decorator"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if attribute:
                module = importlib.import_module(module_name)
                obj = getattr(module, attribute)
            else:
                obj = importlib.import_module(module_name)
            
            return func(obj, *args, **kwargs)
        return wrapper
    return decorator


# Register common lazy loaders
def _load_malware_lab():
    from cybersecurity.enhanced_malware import EnhancedMalwareLab
    return EnhancedMalwareLab(isolated_mode=True)

def _load_ddos_tester():
    from cybersecurity.enhanced_ddos import EnhancedDDoSTester
    return EnhancedDDoSTester(max_threads=50)

def _load_usb_deployer():
    from cybersecurity.enhanced_usb import EnhancedUSBDeployment
    return EnhancedUSBDeployment()

def _load_memory_system():
    from learning.memory import MemorySystem
    return MemorySystem()

def _load_emotion_recognizer():
    from learning.emotion_recognition import EmotionRecognizer
    memory = _load_memory_system()
    return EmotionRecognizer(memory)

# Register loaders
_lazy_loader.register("malware_lab", _load_malware_lab)
_lazy_loader.register("ddos_tester", _load_ddos_tester)
_lazy_loader.register("usb_deployer", _load_usb_deployer)
_lazy_loader.register("memory_system", _load_memory_system)
_lazy_loader.register("emotion_recognizer", _load_emotion_recognizer)


def get_lazy(name: str) -> Any:
    """Get lazy-loaded module"""
    return _lazy_loader.get(name)
