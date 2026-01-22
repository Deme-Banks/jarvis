"""
Discord Bot Integration
"""
from typing import Dict, Optional, List
import requests
import json


class DiscordBot:
    """Discord bot integration for JARVIS"""
    
    def __init__(self, bot_token: Optional[str] = None):
        self.bot_token = bot_token
        self.api_url = "https://discord.com/api/v10"
        self.headers = {
            'Authorization': f'Bot {bot_token}' if bot_token else None,
            'Content-Type': 'application/json'
        }
    
    def send_message(self, channel_id: str, content: str, embed: Optional[Dict] = None) -> Dict:
        """Send message to Discord channel"""
        if not self.bot_token:
            return {'success': False, 'error': 'Discord bot token not configured'}
        
        url = f"{self.api_url}/channels/{channel_id}/messages"
        
        data = {'content': content}
        if embed:
            data['embeds'] = [embed]
        
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=10)
            result = response.json()
            
            return {
                'success': response.status_code == 200,
                'message_id': result.get('id'),
                'error': result.get('message')
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_embed(self, title: str, description: str, color: int = 0x4CAF50,
                    fields: Optional[List[Dict]] = None) -> Dict:
        """Create Discord embed"""
        embed = {
            'title': title,
            'description': description,
            'color': color,
            'timestamp': None
        }
        
        if fields:
            embed['fields'] = fields
        
        return embed
    
    def send_file(self, channel_id: str, file_path: str, content: str = "") -> Dict:
        """Send file to Discord channel"""
        if not self.bot_token:
            return {'success': False, 'error': 'Discord bot token not configured'}
        
        url = f"{self.api_url}/channels/{channel_id}/messages"
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {'content': content}
                response = requests.post(url, headers={'Authorization': f'Bot {self.bot_token}'}, 
                                       files=files, data=data, timeout=30)
                result = response.json()
                
                return {
                    'success': response.status_code == 200,
                    'message_id': result.get('id')
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}
