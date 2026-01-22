"""
Voice Cloning - Clone and synthesize voices
"""
import os
import json
from typing import Dict, Optional, List
from datetime import datetime
import requests


class VoiceCloner:
    """Voice cloning and synthesis"""
    
    def __init__(self):
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.base_url = "https://api.elevenlabs.io/v1"
    
    def clone_voice(self, name: str, audio_files: List[str],
                   description: str = "") -> Dict:
        """Clone a voice from audio samples"""
        if not self.elevenlabs_api_key:
            return {"error": "ElevenLabs API key not configured"}
        
        try:
            url = f"{self.base_url}/voices/add"
            headers = {
                "xi-api-key": self.elevenlabs_api_key
            }
            
            # Prepare multipart form data
            files = []
            for i, audio_file in enumerate(audio_files):
                files.append(('files', (os.path.basename(audio_file), 
                                       open(audio_file, 'rb'), 'audio/mpeg')))
            
            data = {
                'name': name,
                'description': description
            }
            
            response = requests.post(url, headers=headers, files=files, data=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "voice_id": result.get("voice_id"),
                "name": name
            }
        except Exception as e:
            return {"error": str(e)}
    
    def synthesize_speech(self, text: str, voice_id: str,
                         model: str = "eleven_monolingual_v1") -> Dict:
        """Synthesize speech using cloned voice"""
        if not self.elevenlabs_api_key:
            return {"error": "ElevenLabs API key not configured"}
        
        try:
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            headers = {
                "xi-api-key": self.elevenlabs_api_key,
                "Content-Type": "application/json"
            }
            data = {
                "text": text,
                "model_id": model
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            # Save audio
            filename = f"cloned_voice_{voice_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            filepath = os.path.join("generated_audio", filename)
            os.makedirs("generated_audio", exist_ok=True)
            
            with open(filepath, "wb") as f:
                f.write(response.content)
            
            return {
                "success": True,
                "audio_file": filepath,
                "voice_id": voice_id
            }
        except Exception as e:
            return {"error": str(e)}
