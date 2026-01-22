"""
AI Image Generation - DALL-E, Stable Diffusion
"""
import os
import requests
import base64
from typing import Dict, Optional, List
from datetime import datetime
import config_pi as config


class ImageGenerator:
    """AI-powered image generation"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.stable_diffusion_url = os.getenv("STABLE_DIFFUSION_URL", "http://localhost:7860")
    
    def generate_dalle_image(self, prompt: str, size: str = "1024x1024", 
                            n: int = 1) -> Dict:
        """Generate image using DALL-E"""
        if not self.openai_api_key:
            return {"error": "OpenAI API key not configured"}
        
        try:
            url = "https://api.openai.com/v1/images/generations"
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "prompt": prompt,
                "n": n,
                "size": size,
                "response_format": "url"
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            images = [img["url"] for img in result.get("data", [])]
            
            return {
                "success": True,
                "images": images,
                "prompt": prompt,
                "model": "dall-e-3"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def generate_stable_diffusion_image(self, prompt: str, 
                                        negative_prompt: str = "",
                                        steps: int = 20) -> Dict:
        """Generate image using Stable Diffusion"""
        try:
            url = f"{self.stable_diffusion_url}/sdapi/v1/txt2img"
            data = {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "steps": steps,
                "width": 512,
                "height": 512
            }
            
            response = requests.post(url, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            images = result.get("images", [])
            
            # Save images
            saved_paths = []
            for i, img_data in enumerate(images):
                img_bytes = base64.b64decode(img_data)
                filename = f"generated_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.png"
                filepath = os.path.join("generated_images", filename)
                os.makedirs("generated_images", exist_ok=True)
                
                with open(filepath, "wb") as f:
                    f.write(img_bytes)
                saved_paths.append(filepath)
            
            return {
                "success": True,
                "images": saved_paths,
                "prompt": prompt,
                "model": "stable-diffusion"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def generate_image(self, prompt: str, model: str = "dalle",
                      **kwargs) -> Dict:
        """Generate image with specified model"""
        if model.lower() == "dalle" or model.lower() == "dall-e":
            return self.generate_dalle_image(prompt, **kwargs)
        elif model.lower() == "stable" or model.lower() == "stable-diffusion":
            return self.generate_stable_diffusion_image(prompt, **kwargs)
        else:
            return {"error": f"Unknown model: {model}"}
