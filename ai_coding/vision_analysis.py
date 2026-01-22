"""
Vision Analysis for Images and Videos
"""
import os
import base64
from typing import Dict, List, Optional
from llm.cloud_llm import CloudLLMManager, OpenAILLM, GeminiLLM
from llm.local_llm import LocalLLM


class VisionAnalyzer:
    """AI-powered vision analysis"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self._setup_llm()
    
    def _setup_llm(self):
        """Setup LLM with vision capabilities"""
        if self.llm is None:
            # Prefer cloud LLMs for vision (better support)
            manager = CloudLLMManager()
            manager.auto_setup()
            
            if manager.list_providers():
                self.llm = manager.get_provider()
            else:
                local_llm = LocalLLM()
                if local_llm.check_available():
                    self.llm = local_llm
    
    def analyze_image(self, image_path: str, prompt: str = "Describe this image in detail") -> Dict:
        """Analyze image with AI"""
        if not os.path.exists(image_path):
            return {'success': False, 'error': f'Image not found: {image_path}'}
        
        # Encode image
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
                image_base64 = base64.b64encode(image_data).decode()
        except Exception as e:
            return {'success': False, 'error': str(e)}
        
        # Use vision-capable model
        if isinstance(self.llm, OpenAILLM):
            # OpenAI vision API
            return self._analyze_with_openai_vision(image_base64, prompt)
        elif isinstance(self.llm, GeminiLLM):
            # Gemini vision
            return self._analyze_with_gemini_vision(image_base64, prompt)
        else:
            return {
                'success': False,
                'error': 'Vision not supported with current LLM. Use OpenAI or Gemini.'
            }
    
    def _analyze_with_openai_vision(self, image_base64: str, prompt: str) -> Dict:
        """Analyze with OpenAI vision"""
        import requests
        import os
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return {'success': False, 'error': 'OpenAI API key not set'}
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 500
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            result = response.json()
            
            if 'choices' in result:
                return {
                    'success': True,
                    'analysis': result['choices'][0]['message']['content']
                }
            else:
                return {'success': False, 'error': result.get('error', {}).get('message', 'Unknown error')}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _analyze_with_gemini_vision(self, image_base64: str, prompt: str) -> Dict:
        """Analyze with Gemini vision"""
        import requests
        import os
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return {'success': False, 'error': 'Gemini API key not set'}
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"
        
        data = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_base64
                        }
                    }
                ]
            }]
        }
        
        try:
            response = requests.post(f"{url}?key={api_key}", json=data, timeout=30)
            result = response.json()
            
            if 'candidates' in result:
                content = result['candidates'][0]['content']['parts'][0]['text']
                return {
                    'success': True,
                    'analysis': content
                }
            else:
                return {'success': False, 'error': 'No response from Gemini'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def extract_text_from_image(self, image_path: str) -> Dict:
        """Extract text from image (OCR)"""
        # Use vision model for OCR
        return self.analyze_image(image_path, "Extract all text from this image. Return only the text, no descriptions.")
