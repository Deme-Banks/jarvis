"""
IFTTT/Zapier Integration - Connect to 1000+ services
"""
import os
import requests
from typing import Dict, List, Optional
from datetime import datetime


class IFTTTIntegration:
    """IFTTT webhook integration"""
    
    def __init__(self, webhook_key: Optional[str] = None):
        self.webhook_key = webhook_key or os.getenv("IFTTT_WEBHOOK_KEY")
        self.base_url = f"https://maker.ifttt.com/trigger"
    
    def trigger_event(self, event_name: str, value1: str = "",
                     value2: str = "", value3: str = "") -> Dict:
        """Trigger an IFTTT event"""
        if not self.webhook_key:
            return {"error": "IFTTT webhook key not configured"}
        
        try:
            url = f"{self.base_url}/{event_name}/with/key/{self.webhook_key}"
            data = {
                "value1": value1,
                "value2": value2,
                "value3": value3
            }
            
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            
            return {
                "success": True,
                "event": event_name,
                "message": "Event triggered successfully"
            }
        except Exception as e:
            return {"error": str(e)}


class ZapierIntegration:
    """Zapier webhook integration"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or os.getenv("ZAPIER_WEBHOOK_URL")
    
    def trigger_webhook(self, data: Dict) -> Dict:
        """Trigger a Zapier webhook"""
        if not self.webhook_url:
            return {"error": "Zapier webhook URL not configured"}
        
        try:
            response = requests.post(self.webhook_url, json=data, timeout=10)
            response.raise_for_status()
            
            return {
                "success": True,
                "message": "Webhook triggered successfully"
            }
        except Exception as e:
            return {"error": str(e)}
