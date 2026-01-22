"""
AI Video Analysis - Frame extraction, object detection, scene analysis
"""
import os
import cv2
import json
from typing import Dict, List, Optional
from datetime import datetime
import requests
from llm.cloud_llm import CloudLLMManager


class VideoAnalyzer:
    """AI-powered video analysis"""
    
    def __init__(self):
        self.cloud_llm = CloudLLMManager()
        self.cloud_llm.auto_setup()
    
    def extract_frames(self, video_path: str, interval: int = 30) -> List[str]:
        """Extract frames from video"""
        frames = []
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        
        os.makedirs("extracted_frames", exist_ok=True)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % interval == 0:
                filename = f"frame_{frame_count:06d}.jpg"
                filepath = os.path.join("extracted_frames", filename)
                cv2.imwrite(filepath, frame)
                frames.append(filepath)
            
            frame_count += 1
        
        cap.release()
        return frames
    
    def analyze_frame_with_ai(self, frame_path: str, prompt: str = None) -> Dict:
        """Analyze a frame using AI vision"""
        try:
            if not prompt:
                prompt = "Describe what you see in this image in detail."
            
            # Use OpenAI Vision API
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                return {"error": "OpenAI API key not configured"}
            
            # Read image and encode
            with open(frame_path, "rb") as f:
                image_data = f.read()
            
            import base64
            image_base64 = base64.b64encode(image_data).decode()
            
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
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            description = result["choices"][0]["message"]["content"]
            
            return {
                "success": True,
                "frame": frame_path,
                "description": description
            }
        except Exception as e:
            return {"error": str(e)}
    
    def detect_objects(self, frame_path: str) -> List[Dict]:
        """Detect objects in frame using OpenCV"""
        objects = []
        
        try:
            # Load frame
            frame = cv2.imread(frame_path)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Simple object detection using contours
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for i, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > 100:  # Filter small objects
                    x, y, w, h = cv2.boundingRect(contour)
                    objects.append({
                        "id": i,
                        "bbox": [x, y, w, h],
                        "area": area
                    })
            
            return objects
        except Exception as e:
            return [{"error": str(e)}]
    
    def analyze_video(self, video_path: str, analysis_type: str = "frames",
                     interval: int = 30) -> Dict:
        """Analyze video"""
        results = {
            "video_path": video_path,
            "timestamp": datetime.now().isoformat(),
            "analysis_type": analysis_type
        }
        
        if analysis_type == "frames":
            frames = self.extract_frames(video_path, interval)
            results["frames"] = frames
            results["frame_count"] = len(frames)
            
            # Analyze first few frames
            analyzed_frames = []
            for frame in frames[:5]:  # Analyze first 5 frames
                analysis = self.analyze_frame_with_ai(frame)
                analyzed_frames.append(analysis)
            results["frame_analysis"] = analyzed_frames
        
        elif analysis_type == "objects":
            frames = self.extract_frames(video_path, interval)
            all_objects = []
            for frame in frames[:10]:  # Analyze first 10 frames
                objects = self.detect_objects(frame)
                all_objects.append({
                    "frame": frame,
                    "objects": objects
                })
            results["object_detection"] = all_objects
        
        # Save results
        with open("video_analysis.json", "w") as f:
            json.dump(results, f, indent=2)
        
        return results
