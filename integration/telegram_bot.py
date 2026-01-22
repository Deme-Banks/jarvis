"""
Telegram Bot Integration
"""
from typing import Dict, Optional, List
import requests


class TelegramBot:
    """Telegram bot integration for JARVIS"""
    
    def __init__(self, bot_token: Optional[str] = None):
        self.bot_token = bot_token
        self.api_url = f"https://api.telegram.org/bot{bot_token}" if bot_token else None
    
    def send_message(self, chat_id: str, text: str, parse_mode: str = "Markdown") -> Dict:
        """Send message to Telegram chat"""
        if not self.api_url:
            return {'success': False, 'error': 'Bot token not configured'}
        
        url = f"{self.api_url}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            return {
                'success': result.get('ok', False),
                'message_id': result.get('result', {}).get('message_id'),
                'error': result.get('description')
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_photo(self, chat_id: str, photo_path: str, caption: str = "") -> Dict:
        """Send photo to Telegram chat"""
        if not self.api_url:
            return {'success': False, 'error': 'Bot token not configured'}
        
        url = f"{self.api_url}/sendPhoto"
        
        try:
            with open(photo_path, 'rb') as photo:
                files = {'photo': photo}
                data = {
                    'chat_id': chat_id,
                    'caption': caption
                }
                response = requests.post(url, files=files, data=data, timeout=30)
                result = response.json()
                
                return {
                    'success': result.get('ok', False),
                    'message_id': result.get('result', {}).get('message_id')
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_updates(self, offset: int = 0) -> List[Dict]:
        """Get bot updates (messages)"""
        if not self.api_url:
            return []
        
        url = f"{self.api_url}/getUpdates"
        params = {'offset': offset}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            
            if result.get('ok'):
                return result.get('result', [])
        except:
            pass
        
        return []
