"""
Cloud LLM Integration (OpenAI ChatGPT & Google Gemini)
"""
from typing import Optional, Dict, List, Generator
import os
import requests


class CloudLLM:
    """Base class for cloud LLM providers"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = None):
        self.api_key = api_key or os.getenv('LLM_API_KEY')
        self.model = model
        self.base_url = None
    
    def chat(self, message: str, system_prompt: Optional[str] = None, 
             context: Optional[List[Dict]] = None) -> str:
        """Send chat message and get response"""
        raise NotImplementedError
    
    def stream_chat(self, message: str, system_prompt: Optional[str] = None) -> Generator[str, None, None]:
        """Stream chat response"""
        raise NotImplementedError
    
    def check_available(self) -> bool:
        """Check if API is available"""
        return self.api_key is not None


class OpenAILLM(CloudLLM):
    """OpenAI ChatGPT Integration"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        super().__init__(api_key or os.getenv('OPENAI_API_KEY'), model)
        self.base_url = "https://api.openai.com/v1"
        self.model = model or "gpt-4"
    
    def chat(self, message: str, system_prompt: Optional[str] = None,
             context: Optional[List[Dict]] = None) -> str:
        """Chat with OpenAI"""
        if not self.api_key:
            raise ValueError("OpenAI API key not set")
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if context:
            messages.extend(context)
        
        messages.append({"role": "user", "content": message})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
    
    def stream_chat(self, message: str, system_prompt: Optional[str] = None) -> Generator[str, None, None]:
        """Stream chat response from OpenAI"""
        if not self.api_key:
            raise ValueError("OpenAI API key not set")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "stream": True
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                stream=True,
                timeout=30
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]
                        if data_str == '[DONE]':
                            break
                        try:
                            import json
                            chunk = json.loads(data_str)
                            if 'choices' in chunk and len(chunk['choices']) > 0:
                                delta = chunk['choices'][0].get('delta', {})
                                content = delta.get('content', '')
                                if content:
                                    yield content
                        except:
                            pass
        except Exception as e:
            raise RuntimeError(f"OpenAI streaming error: {str(e)}")
    
    def check_available(self) -> bool:
        """Check if OpenAI API is available"""
        if not self.api_key:
            return False
        
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


class GeminiLLM(CloudLLM):
    """Google Gemini Integration"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-pro"):
        super().__init__(api_key or os.getenv('GEMINI_API_KEY'), model)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = model or "gemini-pro"
    
    def chat(self, message: str, system_prompt: Optional[str] = None,
             context: Optional[List[Dict]] = None) -> str:
        """Chat with Gemini"""
        if not self.api_key:
            raise ValueError("Gemini API key not set")
        
        # Combine system prompt and message
        full_prompt = ""
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n"
        full_prompt += message
        
        url = f"{self.base_url}/models/{self.model}:generateContent"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": full_prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000
            }
        }
        
        try:
            response = requests.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']['parts'][0]['text']
                return content
            else:
                raise RuntimeError("No response from Gemini")
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")
    
    def stream_chat(self, message: str, system_prompt: Optional[str] = None) -> Generator[str, None, None]:
        """Stream chat response from Gemini"""
        if not self.api_key:
            raise ValueError("Gemini API key not set")
        
        full_prompt = ""
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n"
        full_prompt += message
        
        url = f"{self.base_url}/models/{self.model}:streamGenerateContent"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": full_prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000
            }
        }
        
        try:
            response = requests.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=data,
                stream=True,
                timeout=30
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    try:
                        import json
                        chunk = json.loads(line)
                        if 'candidates' in chunk and len(chunk['candidates']) > 0:
                            content = chunk['candidates'][0].get('content', {}).get('parts', [{}])[0].get('text', '')
                            if content:
                                yield content
                    except:
                        pass
        except Exception as e:
            raise RuntimeError(f"Gemini streaming error: {str(e)}")
    
    def check_available(self) -> bool:
        """Check if Gemini API is available"""
        if not self.api_key:
            return False
        
        try:
            url = f"{self.base_url}/models/{self.model}"
            response = requests.get(
                f"{url}?key={self.api_key}",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


class CloudLLMManager:
    """Manage multiple cloud LLM providers"""
    
    def __init__(self):
        self.providers = {}
        self.default_provider = None
    
    def add_provider(self, name: str, provider: CloudLLM, set_default: bool = False):
        """Add LLM provider"""
        self.providers[name] = provider
        if set_default or self.default_provider is None:
            self.default_provider = name
    
    def get_provider(self, name: Optional[str] = None) -> CloudLLM:
        """Get LLM provider"""
        provider_name = name or self.default_provider
        if provider_name and provider_name in self.providers:
            return self.providers[provider_name]
        raise ValueError(f"Provider {provider_name} not found")
    
    def list_providers(self) -> List[str]:
        """List available providers"""
        return list(self.providers.keys())
    
    def auto_setup(self) -> Optional[CloudLLM]:
        """Auto-setup available providers"""
        # Try OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            openai_llm = OpenAILLM(api_key=openai_key)
            if openai_llm.check_available():
                self.add_provider('openai', openai_llm, set_default=True)
                return openai_llm
        
        # Try Gemini
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key:
            gemini_llm = GeminiLLM(api_key=gemini_key)
            if gemini_llm.check_available():
                self.add_provider('gemini', gemini_llm, set_default=True)
                return gemini_llm
        
        return None
