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
             temperature: Optional[float] = None) -> str:
        """Send chat message to local LLM"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add context
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
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=config.PiConfig.AGENT_TIMEOUT
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
                timeout=config.PiConfig.AGENT_TIMEOUT
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
        except:
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
            return [m.get("name", "") for m in models]
        except:
            return []
