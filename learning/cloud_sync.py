"""
Cloud Sync for Learning Data (Optional)
"""
import json
import os
from typing import Dict, Optional
import requests
from datetime import datetime


class CloudSync:
    """Optional cloud sync for learning data"""
    
    def __init__(self, api_endpoint: Optional[str] = None, api_key: Optional[str] = None):
        self.api_endpoint = api_endpoint or os.getenv("JARVIS_CLOUD_ENDPOINT")
        self.api_key = api_key or os.getenv("JARVIS_CLOUD_API_KEY")
        self.enabled = bool(self.api_endpoint and self.api_key)
    
    def sync_memory(self, memory_data: Dict, user_id: str) -> bool:
        """Sync memory data to cloud"""
        if not self.enabled:
            return False
        
        try:
            payload = {
                "user_id": user_id,
                "memory_data": memory_data,
                "timestamp": datetime.now().isoformat()
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{self.api_endpoint}/sync/memory",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"Cloud sync error: {e}")
            return False
    
    def download_memory(self, user_id: str) -> Optional[Dict]:
        """Download memory data from cloud"""
        if not self.enabled:
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.get(
                f"{self.api_endpoint}/sync/memory/{user_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Cloud download error: {e}")
        
        return None
    
    def export_to_file(self, memory_data: Dict, filepath: str) -> bool:
        """Export memory data to file (local backup)"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(memory_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False
    
    def import_from_file(self, filepath: str) -> Optional[Dict]:
        """Import memory data from file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Import error: {e}")
            return None
    
    def sync_preferences(self, preferences: Dict, user_id: str) -> bool:
        """Sync only preferences"""
        return self.sync_memory({"preferences": preferences}, user_id)
    
    def sync_knowledge(self, knowledge: Dict, user_id: str) -> bool:
        """Sync only knowledge base"""
        return self.sync_memory({"knowledge": knowledge}, user_id)
