"""
Discord Bot Integration - Community integration
"""
import os
import requests
from typing import Dict, Optional
from utils.cache_optimizer import SmartCache
from utils.performance_profiler import PerformanceProfiler


class DiscordBot:
    """Discord bot integration for JARVIS"""
    
    def __init__(self, bot_token: Optional[str] = None):
        self.bot_token = bot_token or os.getenv("DISCORD_BOT_TOKEN")
        self.api_url = "https://discord.com/api/v10"
        self.cache = SmartCache()
        self.profiler = PerformanceProfiler()
    
    def send_message(self, channel_id: str, content: str, 
                    embed: Optional[Dict] = None) -> Dict:
        """Send message to Discord channel"""
        if not self.bot_token:
            return {"error": "Discord bot token not configured"}
        
        url = f"{self.api_url}/channels/{channel_id}/messages"
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json"
        }
        data = {"content": content}
        if embed:
            data["embeds"] = [embed]
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_channel(self, guild_id: str, name: str, 
                      channel_type: int = 0) -> Dict:
        """Create a Discord channel"""
        if not self.bot_token:
            return {"error": "Discord bot token not configured"}
        
        url = f"{self.api_url}/guilds/{guild_id}/channels"
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json"
        }
        data = {
            "name": name,
            "type": channel_type
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
