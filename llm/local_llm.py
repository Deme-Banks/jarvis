"""
Local LLM Integration (Ollama)
"""
import requests
from typing import Optional, List, Dict, Any
import config_pi as config


class LocalLLM:
    """Interface to local LLM (Ollama)"""
    
    def __init__(self, base_url: Optional[str] = None, model_name: Optional[str] = None):
        self.base_url = base_url or config.PiConfig.LOCAL_MODEL_URL
        self.model_name = model_name or config.PiConfig.LOCAL_MODEL_NAME
        self.context: List[Dict[str, str]] = []
    
    def chat(self, message: str, system_prompt: Optional[str] = None, 
             temperature: Optional[float] = None, context: Optional[List[Dict[str, str]]] = None,
             **kwargs) -> str:
        """Send chat message to local LLM"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if context:
            messages.extend(context[-config.PiConfig.CONTEXT_MEMORY_SIZE:])
        else:
            messages.extend(self.context[-config.PiConfig.CONTEXT_MEMORY_SIZE:])
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature or config.PiConfig.TEMPERATURE,
                "num_predict": config.PiConfig.MAX_TOKENS
            }
        }
        
        try:
            chosen = self.pick_installed_model()
            if self.check_available() and not chosen:
                raise Exception("Ollama has no models. Run: ollama pull qwen2.5-coder:3b")
            if chosen:
                self.model_name = chosen
                payload["model"] = chosen
            timeout = getattr(config.PiConfig, "LOCAL_LLM_TIMEOUT", 120)
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            
            result = response.json()
            assistant_message = result.get("message", {}).get("content", "")
            
            # Update context
            self.context.append({"role": "user", "content": message})
            self.context.append({"role": "assistant", "content": assistant_message})
            
            # Trim context
            if len(self.context) > config.PiConfig.CONTEXT_MEMORY_SIZE * 2:
                self.context = self.context[-config.PiConfig.CONTEXT_MEMORY_SIZE * 2:]
            
            return assistant_message
        except requests.exceptions.RequestException as e:
            raise Exception(f"Local LLM error: {e}")
    
    def stream_chat(self, message: str, system_prompt: Optional[str] = None):
        """Stream chat response"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.extend(self.context[-config.PiConfig.CONTEXT_MEMORY_SIZE:])
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": config.PiConfig.TEMPERATURE,
                "num_predict": config.PiConfig.MAX_TOKENS
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                stream=True,
                timeout=getattr(config.PiConfig, "LOCAL_LLM_TIMEOUT", 120)
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    try:
                        import json
                        chunk = json.loads(line)
                        content = chunk.get("message", {}).get("content", "")
                        if content:
                            yield content
                    except:
                        continue
        except requests.exceptions.RequestException as e:
            raise Exception(f"Local LLM streaming error: {e}")
    
    def check_available(self) -> bool:
        """Check if local LLM is available"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=2
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def list_models(self) -> List[str]:
        """List available local models"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=2
            )
            response.raise_for_status()
            models = response.json().get("models", [])
            return [m.get("name", "") for m in models if m.get("name")]
        except Exception:
            return []

    def pick_installed_model(self) -> Optional[str]:
        """Use configured model if present, else the first pulled Ollama model."""
        names = self.list_models()
        if not names:
            return None
        wanted = (self.model_name or "").strip()
        for name in names:
            if name == wanted or name.startswith(wanted + ":"):
                return name
        return names[0]

    def ensure_ready(self) -> str:
        """
        Make sure Ollama is up and a model is selected.
        Returns a short status line. Raises if Ollama is down.
        """
        if not self.check_available():
            raise RuntimeError(
                "Ollama is not running at "
                f"{self.base_url}. Install https://ollama.com/download then "
                "run `ollama serve` and `ollama pull qwen2.5-coder:3b`."
            )
        chosen = self.pick_installed_model()
        if not chosen:
            raise RuntimeError(
                "Ollama is running but has no models. Run: ollama pull qwen2.5-coder:3b"
            )
        self.model_name = chosen
        return f"Ollama online · model {self.model_name} @ {self.base_url}"
