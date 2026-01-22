"""
Multi-Modal AI - Vision + Audio + Text
"""
import os
import base64
import requests
from typing import Dict, List, Optional
from datetime import datetime


class MultiModalAI:
    """Multi-modal AI combining vision, audio, and text"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"
    
    def analyze_multimodal(self, text: str, image_path: Optional[str] = None,
                          audio_path: Optional[str] = None) -> Dict:
        """Analyze using multiple modalities"""
        if not self.openai_api_key:
            return {"error": "OpenAI API key not configured"}
        
        try:
            messages = []
            
            # Add text
            if text:
                messages.append({
                    "role": "user",
                    "type": "text",
                    "text": text
                })
            
            # Add image
            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    image_data = f.read()
                    image_base64 = base64.b64encode(image_data).decode()
                
                messages.append({
                    "role": "user",
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                })
            
            # Add audio (convert to text first)
            if audio_path and os.path.exists(audio_path):
                # Use Whisper API for audio transcription
                audio_text = self._transcribe_audio(audio_path)
                if audio_text:
                    messages.append({
                        "role": "user",
                        "type": "text",
                        "text": f"Audio transcription: {audio_text}"
                    })
            
            # Call GPT-4 Vision
            url = f"{self.base_url}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": messages
                    }
                ],
                "max_tokens": 500
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "analysis": result["choices"][0]["message"]["content"],
                "modalities_used": {
                    "text": text is not None,
                    "image": image_path is not None,
                    "audio": audio_path is not None
                }
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _transcribe_audio(self, audio_path: str) -> Optional[str]:
        """Transcribe audio using Whisper API"""
        try:
            url = f"{self.base_url}/audio/transcriptions"
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}"
            }
            
            with open(audio_path, "rb") as f:
                files = {"file": f}
                data = {"model": "whisper-1"}
                
                response = requests.post(url, headers=headers, files=files, data=data, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                return result.get("text")
        except Exception as e:
            print(f"Audio transcription error: {e}")
            return None
    
    def generate_multimodal_response(self, prompt: str, 
                                     context_images: List[str] = None,
                                     context_audio: List[str] = None) -> Dict:
        """Generate response using multiple modalities"""
        return self.analyze_multimodal(
            text=prompt,
            image_path=context_images[0] if context_images else None,
            audio_path=context_audio[0] if context_audio else None
        )
