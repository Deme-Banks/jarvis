"""
Telegram Bot Integration - Messaging
"""
import os
import requests
from typing import Dict, Optional
from utils.cache_optimizer import SmartCache
from utils.performance_profiler import PerformanceProfiler


class TelegramBot:
    """Telegram bot integration for JARVIS"""
    
    def __init__(self, bot_token: Optional[str] = None):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.cache = SmartCache()
        self.profiler = PerformanceProfiler()
    
    def send_message(self, chat_id: str, text: str, 
                    parse_mode: str = "HTML") -> Dict:
        """Send message to Telegram chat"""
        if not self.bot_token:
            return {"error": "Telegram bot token not configured"}
        
        url = f"{self.api_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_photo(self, chat_id: str, photo_path: str, 
                  caption: Optional[str] = None) -> Dict:
        """Send photo to Telegram chat"""
        if not self.bot_token:
            return {"error": "Telegram bot token not configured"}
        
        url = f"{self.api_url}/sendPhoto"
        with open(photo_path, 'rb') as photo:
            files = {'photo': photo}
            data = {"chat_id": chat_id}
            if caption:
                data["caption"] = caption
            
            try:
                response = requests.post(url, files=files, data=data)
                response.raise_for_status()
                return {"success": True, "data": response.json()}
            except Exception as e:
                return {"success": False, "error": str(e)}
