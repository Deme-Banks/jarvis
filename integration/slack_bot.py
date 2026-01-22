"""
Slack Bot Integration
"""
from typing import Dict, Optional
import requests
import json


class SlackBot:
    """Slack bot integration for JARVIS"""
    
    def __init__(self, webhook_url: Optional[str] = None, token: Optional[str] = None):
        self.webhook_url = webhook_url
        self.token = token
        self.api_url = "https://slack.com/api"
    
    def send_message(self, channel: str, text: str, blocks: Optional[list] = None) -> Dict:
        """Send message to Slack channel"""
        if not self.token:
            return {'success': False, 'error': 'Slack token not configured'}
        
        url = f"{self.api_url}/chat.postMessage"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'channel': channel,
            'text': text
        }
        
        if blocks:
            data['blocks'] = blocks
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            result = response.json()
            
            return {
                'success': result.get('ok', False),
                'message_ts': result.get('ts'),
                'error': result.get('error')
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_webhook_message(self, text: str, username: str = "JARVIS") -> Dict:
        """Send message via webhook"""
        if not self.webhook_url:
            return {'success': False, 'error': 'Webhook URL not configured'}
        
        data = {
            'text': text,
            'username': username
        }
        
        try:
            response = requests.post(self.webhook_url, json=data, timeout=10)
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_rich_message(self, title: str, text: str, color: str = "good") -> list:
        """Create rich message blocks"""
        return [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": title
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            },
            {
                "type": "divider"
            }
        ]
