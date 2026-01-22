"""
Slack Bot Integration - Team communication
"""
import os
import requests
from typing import Dict, Optional
from utils.cache_optimizer import SmartCache
from utils.performance_profiler import PerformanceProfiler


class SlackBot:
    """Slack bot integration for JARVIS"""
    
    def __init__(self, bot_token: Optional[str] = None):
        self.bot_token = bot_token or os.getenv("SLACK_BOT_TOKEN")
        self.api_url = "https://slack.com/api"
        self.cache = SmartCache()
        self.profiler = PerformanceProfiler()
    
    def send_message(self, channel: str, text: str, 
                    thread_ts: Optional[str] = None) -> Dict:
        """Send message to Slack channel"""
        if not self.bot_token:
            return {"error": "Slack bot token not configured"}
        
        url = f"{self.api_url}/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
        data = {
            "channel": channel,
            "text": text
        }
        if thread_ts:
            data["thread_ts"] = thread_ts
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_channel(self, name: str, is_private: bool = False) -> Dict:
        """Create a Slack channel"""
        if not self.bot_token:
            return {"error": "Slack bot token not configured"}
        
        url = f"{self.api_url}/conversations.create"
        headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
        data = {
            "name": name,
            "is_private": is_private
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_channels(self) -> Dict:
        """Get list of channels"""
        if not self.bot_token:
            return {"error": "Slack bot token not configured"}
        
        url = f"{self.api_url}/conversations.list"
        headers = {
            "Authorization": f"Bearer {self.bot_token}"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return {"success": True, "channels": response.json().get("channels", [])}
        except Exception as e:
            return {"success": False, "error": str(e)}
